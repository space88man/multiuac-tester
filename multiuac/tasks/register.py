from enum import IntEnum
import logging
import random
import os

import anyio

# sippy
from sippy.SipCallId import SipCallId
from sippy.SipFrom import SipFrom
from sippy.SipTo import SipTo
from sippy.SipURL import SipURL
from sippy.SipVia import SipVia
from sippy.SipRequest import SipRequest
from sippy.SipResponse import SipResponse
from sippy.SipTransactionManager import SipTransaction
from sippy.SipContact import SipContact
from sippy.SipExpires import SipExpires
from sippy.SipHeader import SipHeader

from .common import UAMixin
from ..utils import timeout_end, gen_tag
from ..common import call_id, user_id


LOG = logging.getLogger("multiuac.register")


class RegState(IntEnum):
    NONE = 0
    WWW = 1
    SLEEP = 2
    SHUTDOWN = 3
    DEAD = 98
    ERROR = 99


class UATaskREGISTER(UAMixin):
    def __init__(
        self,
        stm,
        username,
        password,
        my_uri,
        registrar,
        local_address,
        proto,
        instance=None,
        reg_id=0,
    ):

        self.stm = stm
        self.username = username
        self.password = password
        self.my_uri = my_uri
        self.registrar = registrar
        self.local_address = local_address
        self.proto = proto

        self.contact_address = local_address
        self.ruri = SipURL(f"{self.registrar}")

        self.cseq = random.randrange(10000, 29999)
        self.events = {}
        self.auth_hf = None
        self.count = 0
        self.call_id = SipCallId()
        self.state = RegState.NONE

        via_s = os.getenv("SIP_VIA_S", None)
        if via_s is None:
            via_s = f"SIP/2.0/{proto} {local_address[0]}:{local_address[1]};rport;alias"

        self.via = SipVia(via_s)
        self.via.parse()
        self.via.genBranch()
        self.via_branch = self.via.getBranch()
        self.enable_via_hook = True
        self.uri_params = ""

        self.run_once = False
        self.expires = 600
        self.is_running = True

        self.instance = instance
        self.reg_id = reg_id

    @property
    def contact_hf(self):
        cs = os.getenv("SIP_CONTACT", None)
        if cs is None:
            if self.instance is not None:
                if self.uri_params.find(";ob") == -1:
                    self.uri_params += ";ob"
            body = f"<sip:{self.username}@{self.contact_address[0]}:{self.contact_address[1]}{self.uri_params}>"
            if self.instance is not None:
                assert self.reg_id != 0
                body += f';+sip.instance="{self.instance}";reg-id={self.reg_id}'
        else:
            body = f"<{os.getenv('SIP_CONTACT')}>{os.getenv('SIP_REG_PARAM')}"

        return SipContact(body)

    async def forever_loop(self, expires, *, task_status=anyio.TASK_STATUS_IGNORED):

        auth_fail = 0
        t0, fr0m = self._t0, self._fr0m
        self.state = RegState.NONE
        with anyio.CancelScope() as scope:
            task_status.started(scope)

            while True:
                if self.state == RegState.ERROR:
                    break
                elif self.state == RegState.SLEEP:
                    await anyio.sleep(300.0 + random.random()*120.0)
                    self.state = RegState.NONE

                expires
                self.events[self.cseq] = [anyio.Event(), expires, 0]

                if self.state == RegState.NONE:
                    req = SipRequest(
                        method="REGISTER",
                        ruri=self.ruri,
                        to=t0,
                        fr0m=fr0m,
                        via=self.via,
                        cseq=self.cseq,
                        callid=self.call_id,
                        contact=self.contact_hf,
                        expires=SipExpires(str(expires)),
                        user_agent="TBS MultiUAC",
                    )
                    req.appendHeader(SipHeader("Supported: outbound,path"))
                    if self.auth_hf:
                        req.appendHeader(SipHeader(body=self.auth_hf))

                elif self.state == RegState.WWW:
                    assert self.auth_hf and self.call_id
                    req = SipRequest(
                        method="REGISTER",
                        ruri=self.ruri,
                        to=t0,
                        fr0m=fr0m,
                        via=self.via,
                        callid=self.call_id,
                        cseq=self.cseq,
                        contact=self.contact_hf,
                        expires=SipExpires(str(expires)),
                        user_agent="TBS MultiUAC",
                    )
                    req.appendHeader(SipHeader("Supported: outbound,path"))
                    req.appendHeader(SipHeader(body=self.auth_hf))

                await self.stm.newTransaction(
                    req,
                    self.resp_cb,
                    cb_ifver=2,
                    compact=False,
                    laddress=self.local_address,
                )

                await (ret := self.events[self.cseq])[0].wait()
                resp = ret[2]
                if resp.scode == 401:
                    if auth_fail > 5:
                        auth_fail = 0
                        self.state = RegState.SLEEP
                        self.auth_hf = None
                        LOG.warning("Authentication failed, retrying in 300.0 secs")
                        continue
                    else:
                        auth_fail += 1
                    www_auth = resp.getHF("www-authenticate").getBody()
                    self.auth_hf = www_auth.genAuthHF(
                        self.username,
                        self.password,
                        "REGISTER",
                        self.ruri.localStr(),
                        qop=www_auth.qop[0] if www_auth.qop else None,
                    )
                    self.state = RegState.WWW
                elif resp.scode == 408:
                    auth_fail = 0
                    self.state = RegState.SLEEP
                    self.auth_hf = None

                    if expires == 0:
                        return
                    LOG.warning("REGISTER timeout, retrying in 300.0 secs")
                    continue
                elif resp.scode == 200:
                    auth_fail = 0
                    if ret[1] == 0:  # de-REGISTER request
                        LOG.info("UA is successfully de-registered")
                        break
                    else:
                        LOG.info("[%s]UA is successfully registered", user_id.get())
                        self.state = RegState.SLEEP

                self.events.pop(self.cseq)
                self.cseq += 1

    async def run(self):
        LOG.info("UATaskREGISTER is starting")
        call_id.set(self.call_id)
        user_id.set(self.username)

        self._t0 = SipTo(f"<{self.my_uri}>")
        self._fr0m = SipFrom(f"<{self.my_uri}>")
        self._fr0m.parse()
        self._fr0m.setTag(gen_tag())

        self.state = RegState.NONE
        async with anyio.create_task_group() as self.tg:
            self.forever = await self.tg.start(self.forever_loop, self.expires)
            self.is_ended = anyio.Event()
            await self.is_ended.wait()

        self.state = RegState.DEAD
        LOG.info("UATaskREGISTER is exiting")

    def shutdown(self):
        if self.expires:
            self.expires = 0
            self.forever.cancel()
            self.tg.start_soon(self.forever_loop, 0)
            self.is_ended.set()

    async def resp_cb(self, resp: SipResponse, t: SipTransaction):

        if self.state == RegState.DEAD:
            return

        self.hook_via(resp)

        cseq = resp.getHF("cseq").getBody().cseq
        if cseq in self.events:
            self.events[cseq][2] = resp
            self.events[cseq][0].set()
