import anyio
import logging

from sippy.Time.MonoTime import MonoTime
from sippy.UaStateDead import UaStateDead
from sippy.SipURL import SipURL

from .transport import TLSClient
from .tasks.register import UATaskREGISTER
from .tasks.call import UATaskCall
from .core import prepare_caller

LOG = logging.getLogger("multiuac.PHONE")
GC_LOG = logging.getLogger("multiuac.gc")


class Call:
    pass


class Phone:
    def __init__(
        self,
        username,
        password,
        domain,
        caller_name,
        outbound_proxy,
        registrar,
        enable_via_hook=True,
        instance=None,
        reg_id=0,
    ):
        self.username = username
        self.password = password
        self.outbound_proxy = outbound_proxy
        self.registrar = registrar
        self.domain = domain
        self.caller_name = caller_name

        self.transport = None

        self.stm = None
        self.calls = {}

        self.enable_via_hook = enable_via_hook
        self.instance = instance
        assert instance is None or isinstance(instance, str)
        self.reg_id = reg_id

    def shutdown(self):
        self.task.shutdown()

    async def hangup(self, call_id):
        if call_id in self.calls:
            self.tg.start_soon(self.calls[call_id].hangup)

    async def garbage(self):
        GC_LOG.info("Garbage collection task is started")
        while True:
            await anyio.sleep(60.0)
            GC_LOG.info("Garbage collection is running")
            for k, v in list(self.calls.items()):
                if isinstance(v.ua.state, UaStateDead):
                    GC_LOG.info("Cleaning up call %s", k)
                    del self.calls[k]

    async def run(self):
        assert self.stm and self.username and self.password
        assert self.domain and self.caller_name

        self.transport = TLSClient(self.outbound_proxy, self.data_callback)

        async with anyio.create_task_group() as self.tg:
            await self.tg.start(self.transport.run)

            LOG.info("local_address = %s", self.transport.local_address)
            self.stm.l4r.fixed = False
            self.stm.l4r.cache_l2s[self.transport.local_address] = self.transport

            self.transport.keepalive()
            self.tg.start_soon(self.garbage)
            self.task = UATaskREGISTER(
                self.stm,
                self.username,
                self.password,
                f"sip:{self.username}@{self.domain}",
                f"sip:{self.domain}",
                self.transport.local_address,
                "TLS",
                instance=self.instance,
                reg_id=self.reg_id,
            )
            self.task.uri_params = ";ob;transport=tls"
            self.task.enable_via_hook = self.enable_via_hook
            self.tg.start_soon(self.task.run)

            while True:
                await anyio.sleep(120.0)

    async def data_callback(self, transport, data_in):
        await self.stm.handleIncoming(
            data_in, (transport.host, transport.port), transport, MonoTime()
        )

    async def recv_request(self, req, sip_t):

        if req.getMethod() != "INVITE":
            return

        task_uas = UATaskCall()
        uas = prepare_caller(
            self,
            task_uas.event_cb,
            "UAS",
            f"sip:{self.username}@{self.domain}",
            uri_params=";transport=tls;ob"
            if self.instance is not None
            else ";transport=tls",
        )
        uas.enable_via_hook = self.enable_via_hook
        await self.tg.start(
            task_uas.run_uas, uas, call_id := str(req.getHF("call-id").getBody())
        )
        self.calls[call_id] = task_uas

        return await uas.recvRequest(req, sip_t)

    async def make_call(self, callee, tls=True):
        if not callee.startswith("sip:") and not callee.startswith("sips:"):
            called_id = callee
            to_url_s = f"{'sips' if tls else 'sip'}:{callee}@{self.domain}"
        else:
            called_id = SipURL(callee).username
            to_url_s = callee

        task_uac = UATaskCall(self.caller_name, called_id)
        print("=================> to_url_s =", to_url_s)

        ua = prepare_caller(
            self,
            task_uac.event_cb,
            f"UAC({called_id})",
            f"sip:{self.username}@{self.domain}",
            t0=to_url_s,
            uri_params=";transport=tls;ob"
            if self.instance is not None
            else ";transport=tls",
        )
        ua.enable_via_hook = self.enable_via_hook
        await self.tg.start(task_uac.run, ua)
        self.calls[str(task_uac.call_id)] = task_uac
