from typing import Callable

from sippy.SipResponse import SipResponse
from sippy.SipRequest import SipRequest

Callbacks = tuple[
    SipResponse, Callable[[float, SipRequest], None], Callable[[float], None]
]
