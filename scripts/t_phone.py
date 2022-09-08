import anyio
import logging
import os
import argparse

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
CALLER_NAME = os.getenv("MULTIUAC_CALLER_NAME")
CALLER_ID = os.getenv("MULTIUAC_CALLER_ID")
CALLER_PASSWORD = os.getenv("MULTIUAC_CALLER_PASSWORD")
SIP_INSTANCE = os.getenv("MULTIUAC_SIP_INSTANCE")
SIP_REGID = os.getenv("MULTIUAC_SIP_REGID")


assert (
    DOMAIN
    and PORT
    and WEB_PORT
    and CALLER_NAME
    and CALLER_ID
    and CALLER_PASSWORD
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


@app.route("/calls")
async def calls():
    return {"calls": list(gl0bal.phone.calls.keys())}


@app.post("/calls")
async def make_call():
    data = await request.get_json()
    if "callee" not in data:
        return
    else:
        await gl0bal.phone.make_call(data["callee"])

    return {"result": f"Call to {data['callee']} initiated"}


async def _quit():
    await anyio.sleep(5.0)
    sys.exit(0)


@app.route("/shutdown")
async def shutdown():
    gl0bal.phone.shutdown()
    gl0bal.tg.start_soon(_quit)
    return {"result": "Shutdown initiated"}


@app.route("/calls/<call_id>/hangup")
async def hangup0(call_id):
    await gl0bal.phone.hangup(call_id)
    return {"result": f"Hang-up of call {call_id} initiated"}


@app.delete("/calls/<call_id>")
async def hangup(call_id):
    await gl0bal.phone.hangup(call_id)
    return {"result": f"Hang-up of call {call_id} initiated"}


# ======================================================
async def app_task(args):

    domain = DOMAIN
    caller_id = CALLER_ID
    caller_name = CALLER_NAME
    password = CALLER_PASSWORD

    parser = argparse.ArgumentParser()
    parser.add_argument('--novia-hook', action='store_true')
    opts = parser.parse_args(args)

    phone = Phone(
        caller_id,
        password,
        domain,
        caller_name,
        (domain, 5061),
        f"sip:{domain}",
        enable_via_hook=not opts.novia_hook,
        instance=SIP_INSTANCE,
        reg_id=SIP_REGID
    )

    phone.stm = global_config["_sip_tm"] = SipTransactionManager(global_config, req_cb=phone.recv_request)
    gl0bal.phone = phone

    ED2.servers = []

    async with anyio.create_task_group() as app_tg:
        gl0bal.app_tg = app_tg
        await app_tg.start(ED2.aloop)
        await phone.run()

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
    logging.getLogger("multiuac").propagate = False
    logging.getLogger("multiuac").addHandler(console)

    main(sys.argv[1:])
