from multiuac.controller import (TLSClient, UATaskREGISTER)
import os
from dotenv import load_dotenv


class App:

    def __init__(self):
        load_dotenv()

    async def run(self, global_config):
        nursery = global_config["_nursery"]
        self.global_config = global_config
        tls_client = TLSClient(
            global_config,
            "kamailio-testing.testing.tbs",
            5061,
            global_config["_sip_tm"].handleIncoming
        )

        await nursery.start(tls_client.run)
        uac_task_info = UATaskREGISTER(
            os.getenv('MULTIUAC_USER'),
            os.getenv('MULTIUAC_PASSWORD'),
            global_config,
            "kamailio-testing.testing.tbs",
            5061,
            "TLS",
            tls_client.local_address,
            tls_client
        )

        nursery.start_soon(uac_task_info.run)


app = App()
