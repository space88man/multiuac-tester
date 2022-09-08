from contextvars import ContextVar


call_id = ContextVar("call_id", default="GLOBAL")
user_id = ContextVar("user_id", default="USER_ID")
