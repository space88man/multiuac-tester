import logging

from sippy.SipVia import SipVia

LOG = logging.getLogger("multiuac.tasks")


class UAMixin:
    def hook_via(self, resp):
        if not self.enable_via_hook:
            return
        via = resp.getHFs("via")[0].getBody()
        received = via.params["received"]
        rport = int(via.params["rport"])
        if ":" in received and not received.startswith("["):
            received = f"[{received}]"

        if rport != self.contact_address[1] or received != self.contact_address[0]:
            LOG.info(
                "Contact address has changed %s -> %s",
                self.contact_address,
                (received, rport),
            )

            self.contact_address = (received, rport)
            self.via = SipVia(
                f"SIP/2.0/{self.proto} {self.contact_address[0]}:{self.contact_address[1]};rport;alias;branch={self.via_branch}"
            )
            self.via.parse()
