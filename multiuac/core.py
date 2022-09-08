import logging
import random
import anyio
import os

from sippy.UA import UA
from sippy.SipRequest import SipRequest
from sippy.SipVia import SipVia
from sippy.SipFrom import SipFrom
from sippy.SipTo import SipTo
from sippy.SipContact import SipContact
from sippy.SipSupported import SipSupported
from sippy.SipHeader import SipHeader
from sippy.SipURL import SipURL

LOG = logging.getLogger("multiuac.core")


def gen_tag():
    return "".join(random.choices("0123456789abcdef", k=32))


def gen_call_id():
    return "".join(
        random.choices(
            "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.-", k=32
        )
    )


async def timeout_end(task_group, end=120.0):
    await anyio.sleep(end)
    task_group.cancel_scope.cancel()


class UA2(UA):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enable_via_hook = True

    def update_ua(self, msg):
        super().update_ua(msg)

        if not self.enable_via_hook or isinstance(msg, SipRequest):
            return
        via = msg.getHFs("via")[0].getBody()
        received = via.params["received"]
        rport = int(via.params["rport"])
        if ":" in received and not received.startswith("["):
            received = f"[{received}]"

        url = self.lContact.address.url
        host = url.getHost()
        port = url.getPort()

        if rport != port or received != host:

            LOG.info(
                "Contact address has changed %s -> %s", (host, port), (received, rport)
            )

            url.setAddr((received, rport))
            self.source_via = SipVia(
                sipver=self.source_via.sipver,
                hostname=received,
                port=rport,
                params=self.source_via.params,
            )


def prepare_caller(
    ctx,
    event_cb,
    name,
    fr0m,
    port=5060,
    t0=None,
    uri_params=";transport=tls",
):
    address = ctx.transport.local_address
    uaO = UA(
        ctx.stm.global_config,
        nh_address=(ctx.domain, port),
        event_cb=event_cb,
        username=ctx.username,
        password=ctx.password,
    )
    uaO.myname = name
    uaO.source_address = address

    uaO.lUri = SipFrom(f"<{fr0m}>")
    uaO.lUri.parse()
    uaO.lUri.setTag(uaO.lTag)

    if t0:
        uaO.rUri = SipTo(f"<{t0}>")
        uaO.rUri.parse()
        uaO.rTarget = SipURL(t0)

    via_s = os.getenv("SIP_VIA_S", None)
    if via_s is None:
        uaO.source_via = SipVia(
            hostname=address[0],
            port=address[1],
            sipver="SIP/2.0/TLS",
            params={"rport": None},
        )
    else:
        uaO.source_via = SipVia(via_s)
        uaO.source_via.parse()

    uaO.source_via.genBranch()
    contact_s = os.getenv("SIP_CONTACT", None)
    if contact_s is None:
        if uri_params.find(";transport=tls") != -1:
            uri_params = uri_params.replace(";transport=tls", "")
            scheme = "sips"
        else:
            scheme = "sip"

        contact_s = f"{scheme}:{ctx.username}@{address[0]}:{address[1]}{uri_params}"

    uaO.lContact = SipContact(f"<{contact_s}>")
    uaO.lContact.parse()
    uaO.extra_headers = [SipHeader(body=SipSupported("outbound,path"))]

    return uaO
