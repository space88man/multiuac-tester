from typing import Callable

from .SipResponse import SipResponse
from .SipRequest import SipRequest
from .Udp_server import Udp_server
from .Time.MonoTime import MonoTime

Address = tuple[str, int]


class SipTransaction:
    pass


class SipTransactionManager:
    async def newTransaction(
        self,
        msg: SipRequest,
        resp_cb: Callable[[SipResponse, SipTransaction], None] = None,
        laddress: Address = None, # used if userv==None
        userv=None,
        cb_ifver: int = 1,
        compact: bool = False,
        t: SipTransaction = None,
    ):
        pass

    async def handleIncoming(
        self, data_in: bytes, address: Address, server: Udp_server, rtime: MonoTime
    ):
        pass
