import random
import logging
import anyio
from jinja2 import Template
import re

# sippy
from sippy.SipCallId import SipCallId
from sippy.CCEvents import (
    CCEventTry,
    CCEventDisconnect,
    CCEventConnect,
    CCEventInfo,
    CCEventFail,
    CCEventRing,
)
from sippy.MsgBody import MsgBody
from sippy.UaStateConnected import UaStateConnected
from sippy.UaStateDead import UaStateDead
from sippy.UasStateRinging import UasStateRinging
from sippy.UasStateTrying import UasStateTrying

from ..msg_templates import sdp_offer_j2, sdp_answer_j2
from ..core import gen_call_id
from ..common import call_id
from .common import UAMixin

LOG = logging.getLogger("multiuac.call")


class UATaskCall(UAMixin):
    def __init__(self, caller_name=None, callee_id=None, tg=None):

        self.caller_name = caller_name
        self.callee_id = callee_id
        self.ext_tg = None

        self.session_id = None
        self.session_ver = None

    async def disconnect_cb(self, ua, rtime, origin):
        LOG.info("[CALLBACK Disconnect] rtime=%s, origin=%s", rtime, origin)
        if origin == "myself":
            self.tg.cancel_scope.cancel()
            LOG.info("%s: phone call %s is disconnected", ua.myname, ua.cId)

    async def connect_cb(self, ua, rtime, origin):
        LOG.info("[CALLBACK Connect] rtime=%s, origin=%s", rtime, origin)
        if origin == "myself":
            LOG.info("%s: phone call %s is connected", ua.myname, ua.cId)

    async def ring_cb(self, ua, rtime, origin, code):
        LOG.info("[CALLBACK Ring] rtime=%s, origin=%s, code=%s", rtime, origin, code)
        if origin == "myself":
            LOG.info("%s: phone call %s is ringing", ua.myname, ua.cId)

    def contact_ip(self) -> str:
        assert self.ua

        contact_ip = self.ua.source_address[0]
        if ":" in contact_ip:
            contact_ip = contact_ip[1:-1]

        return contact_ip

    async def run(self, ua, *, task_status=anyio.TASK_STATUS_IGNORED):
        self._role = "UAC"
        self.ua = ua
        self.ua.disc_cbs = (self.disconnect_cb,)
        self.ua.conn_cbs = (self.connect_cb,)
        self.ua.ring_cbs = (self.ring_cb,)
        self.session_id = random.randrange(2000000000, 4999999999)
        self.session_ver = self.session_id
        context = {
            "rtp_port": 32768,
            "rtcp_port": 32769,
            "session_id": self.session_id,
            "session_ver": self.session_ver,
            "contact_ip": self.contact_ip(),
        }
        SDP = Template(sdp_offer_j2, keep_trailing_newline=True).render(context)
        self.call_id = SipCallId(gen_call_id())
        call_id.set(self.call_id)
        task_status.started()

        async with anyio.create_task_group() as self.tg:
            await ua.recvEvent(
                CCEventTry(
                    data=(
                        self.call_id,
                        ua.username,
                        self.callee_id,
                        MsgBody(content=SDP),
                        None,
                        self.caller_name,
                    ),
                    origin="myself",
                )
            )

            while True:
                await anyio.sleep(32.0)
                LOG.info("%s:ua.state = %s", self.call_id, ua.state)
                if isinstance(ua.state, UaStateDead):
                    self.tg.cancel_scope.cancel()

        LOG.info("UATaskCall(UAC:%s) is exiting", self.call_id)

    async def run_uas(self, ua, call_id, *, task_status=anyio.TASK_STATUS_IGNORED):
        self._role = "UAS"
        self.call_id = call_id
        self.ua = ua
        self.ua.disc_cbs = (self.disconnect_cb,)
        self.ua.conn_cbs = (self.connect_cb,)
        self.ua.ring_cbs = (self.ring_cb,)

        async with anyio.create_task_group() as self.tg:
            task_status.started()

            while True:
                await anyio.sleep(32.0)
                LOG.info("%s:ua.state = %s", call_id, ua.state)
                if isinstance(ua.state, UaStateDead):
                    self.tg.cancel_scope.cancel()

        LOG.info("UATaskCall(UAS:%s) is exiting", call_id)

    async def hangup(self):
        if isinstance(self.ua.state, UaStateConnected):
            await self.ua.recvEvent(CCEventDisconnect(data=None, origin="myself"))

    async def answer_task(self, event, ua):
        await anyio.sleep(2.0 + random.random() * 2.0)
        if not (
            isinstance(ua.state, UasStateTrying)
            or isinstance(ua.state, UasStateRinging)
        ):
            LOG.info("Aborting answer_task")
            return
        cId, x, y, body, auth, name = event.getData()
        LOG.info("answer_task x=%s y=%s name=%s state=%s", x, y, name, ua.state)

        offer_sdp = str(body)
        if m := re.search(
            r"^o=[^\s]+\s+(?P<session_id>\d+)\s+(?P<session_ver>\d+)",
            offer_sdp,
            flags=re.MULTILINE,
        ):
            LOG.info(
                "Found SDP session_id and session_ver:%s %s",
                m.group("session_id"),
                m.group("session_ver"),
            )

            self.session_id = int(m.group("session_id"))
            self.session_ver = int(m.group("session_ver"))
            self.answer_session_ver = self.session_ver + 1
        else:
            self.session_id = 1000000000
            self.session_ver = 1000000000
            self.answer_session_ver = 1000000001

        context = {
            "rtp_port": 40000,
            "rtcp_port": 40001,
            "session_id": self.session_id,
            "session_ver": self.answer_session_ver,
            "contact_ip": self.contact_ip(),
        }
        SDP_answer = Template(sdp_answer_j2, keep_trailing_newline=True).render(context)

        try:
            await ua.recvEvent(
                CCEventConnect(
                    data=(200, "OK", MsgBody(content=SDP_answer)), origin="myself"
                )
            )
        except Exception as exc:
            LOG.exception(exc)
            ua.state = UaStateDead(ua)

        LOG.info("answer_task is completed")

    async def event_cb(self, event, ua):
        if event.data:
            LOG.info(
                f"[EVENT] {ua.myname}/{ua.state}/{event.origin}:{event.name}:{len(event.data)}:{event.data}"
            )
        else:
            LOG.info(f"[EVENT] {ua.myname}/{ua.state}/{event.origin}:{event.name}")

        if isinstance(event, CCEventTry):  # UAS
            await anyio.sleep(1.0)
            await ua.recvEvent(CCEventRing(data=None, origin="myself"))
            self.tg.start_soon(self.answer_task, event, ua)
        elif isinstance(event, CCEventConnect):
            LOG.info("%s: phone call %s is connected", ua.myname, ua.cId)
        elif isinstance(event, CCEventDisconnect):  # UA
            self.tg.cancel_scope.cancel()
            LOG.info("%s: phone call %s is disconnected", ua.myname, ua.cId)
        elif isinstance(event, CCEventFail):  # UA
            self.tg.cancel_scope.cancel()
            LOG.info("%s: phone call %s is unsuccessful", ua.myname, ua.cId)
        elif isinstance(event, CCEventRing):
            LOG.info("%s: phone call %s is ringing", ua.myname, ua.cId)
