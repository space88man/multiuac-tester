import logging

from .common import call_id


class VLogger:

    app = None
    logger = None
    pid = None

    def __init__(self, app, logger=logging.getLogger("multiuac.logger"), pid=""):
        self.app = "/" + app
        self.logger = logger
        self.pid = pid
        self.call_id = call_id

    def write(self, *args, **kwargs):

        self.logger.info(
            "%s%s%s:\n%s",
            call_id.get(),
            self.app,
            f"[{self.pid}]" if self.pid else "",
            "".join([str(x) for x in args]),
        )
