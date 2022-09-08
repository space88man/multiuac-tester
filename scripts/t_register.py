import anyio
import logging
import os
import argparse
import uuid
import random

from hypercorn.config import Config
from hypercorn.asyncio import serve
from quart import Quart, request

from sippy.SipTransactionManager import SipTransactionManager
from sippy.Core.EventDispatcher import ED2

from multiuac.phone import Phone
from multiuac.logger import VLogger

from dotenv import load_dotenv

load_dotenv(".env")

# =================================================
DOMAIN = os.getenv("MULTIUAC_DOMAIN")
PORT = os.getenv("MULTIUAC_PORT")
WEB_PORT = os.getenv("MULTIUAC_WEB_PORT", "8080")
PREFIX = os.getenv("MULTIUAC_PREFIX")


assert (
    DOMAIN
    and PORT
    and WEB_PORT
    and PREFIX
)
# =================================================

global_config = {
    "_sip_address": DOMAIN,
    "_sip_port": PORT,
    "_sip_logger": VLogger("multiuac")
}


# =======================================================
class Globals:
    pass


gl0bal = Globals()
gl0bal.phone = None


app = Quart(__name__)
config = Config()
config.bind = ["localhost:" + WEB_PORT]


@app.route("/version")
async def hello():
    return {"version": "1.0"}


@app.post("/command")
async def command():
    data = await request.get_json()
    result = "FAIL"
    if (command := data.get("command", None)) == "quit":
        ED2.breakLoop()
        gl0bal.app_tg.cancel_scope.cancel()
        result = "OK"
    elif command == "start":
        gl0bal.tg.start_soon(app_task)
        result = "OK"

    return {"result": result}


async def _quit():
    await anyio.sleep(5.0)
    sys.exit(0)


@app.route("/shutdown")
async def shutdown():
    # gl0bal.phone.shutdown()
    gl0bal.tg.start_soon(_quit)
    return {"result": "Shutdown initiated"}


async def jitter(p):
    interval = float(os.getenv("MULTIUAC_JITTER", "60.0"))
    await anyio.sleep(random.random()*interval)
    try:
        await p.run()
    except Exception as exc:
        LOG.exception("%s has failed", p.username)


# ======================================================
async def app_task(args):

    domain = DOMAIN
    limit = int(os.getenv("MULTIUAC_LIMIT", "100"))

    parser = argparse.ArgumentParser()
    parser.add_argument('--novia-hook', action='store_true')
    opts = parser.parse_args(args)

    global_config["_sip_tm"] = SipTransactionManager(global_config)
    phones = []
    start_idx = int(os.getenv("MULTIUAC_START_IDX", "1210"))
    for i in range(0, limit):

        phone = Phone(
            f"{PREFIX}{i+start_idx:04d}",
            "password",
            domain,
            f"{PREFIX.capitalize()} {i+start_idx:04d}",
            (domain, 5061),
            f"sip:{domain}",
            enable_via_hook=not opts.novia_hook,
            instance=str(uuid.uuid4()),
            reg_id=1
        )
        phone.stm = global_config["_sip_tm"]
        phones.append(phone)

    ED2.servers = []

    async with anyio.create_task_group() as app_tg:
        gl0bal.app_tg = app_tg
        await app_tg.start(ED2.aloop)
        LOG.warning("Launching %d bots...", len(phones))
        for p in phones:
            LOG.warning("Launching %s...", p.username)
            app_tg.start_soon(jitter, p)

    print("========> app_task() is exiting")


async def amain(args):
    async with anyio.create_task_group() as tg:
        gl0bal.tg = tg
        tg.start_soon(serve, app, config)
        tg.start_soon(app_task, args)


def main(args):
    import uvloop
    uvloop.install()

    anyio.run(amain, args)


if __name__ == "__main__":
    import logging.config
    import sys
    logging.basicConfig(level="INFO")

    brief = logging.Formatter(fmt='%(asctime)s %(name)s [%(levelname)s]: %(message)s')
    console = logging.StreamHandler(stream=sys.stdout)
    console.setFormatter(brief)

    LOG = logging.getLogger("multiuac")
    LOG.propagate = False
    LOG.addHandler(console)
    logging.getLogger("multiuac.logger").setLevel("WARN")
    logging.getLogger("multiuac.gc").setLevel("WARN")
    # logging.getLogger("multiuac.transport").setLevel("WARN")

    main(sys.argv[1:])
