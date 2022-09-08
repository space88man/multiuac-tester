import anyio
import random


def gen_tag():
    return "".join(random.choices("0123456789abcdef", k=32))


async def timeout_end(task_group, end=120.0):
    await anyio.sleep(end)
    task_group.cancel_scope.cancel()
