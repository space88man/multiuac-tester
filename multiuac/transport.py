from socket import AddressFamily
from typing import Union
import logging
import random
import ssl
import os

# anyio
from anyio import (
    connect_tcp,
    create_task_group,
    create_memory_object_stream,
    Lock,
    TASK_STATUS_IGNORED,
    CancelScope,
)
from anyio.abc import TaskStatus
from anyio.abc import SocketAttribute
from anyio.streams.buffered import BufferedByteReceiveStream
from anyio import sleep

LOG = logging.getLogger("multiuac.transport")


class TLSOpts:
    def __init__(self, transport):
        self.transport = transport

    def getSIPaddr(self):
        if self.transport.family == AddressFamily.AF_INET:
            return self.transport.local_address
        return (
            "[%s]" % self.transport.local_address[0],
            self.transport.local_address[1],
        )

    def isWildCard(self):
        return False


def protocol_fn(x: int) -> int:
    match x:
        case 0:
            protocol = ssl.PROTOCOL_TLSv1
        case 1:
            protocol = ssl.PROTOCOL_TLSv1_1
        case 2:
            protocol = ssl.PROTOCOL_TLSv1_2
        case 3:
            protocol = ssl.PROTOCOL_TLS

    return protocol


class TLSClient:
    client = None
    (qsend, qrecv) = (None, None)
    _lock = None
    is_running = True

    def __init__(self, address, data_callback):
        self.qsend, self.qrecv = create_memory_object_stream(256)
        self._send_lock = Lock()
        self.host = address[0]
        self.port = address[1]
        self.data_callback = data_callback

        self.uopts = TLSOpts(self)

        self.local_address = None
        self.remote_address = None
        self.family = None
        self._scope = None

    async def run(self, *, task_status: TaskStatus = TASK_STATUS_IGNORED):

        if (force := int(os.getenv("MULTIUAC_PROTOCOL_FORCE", "-1"))) >= 0:
            protocol = protocol_fn(force)
        else:
            protocol = protocol_fn(
                random.randint(
                    int(os.getenv("MULTIUAC_PROTOCOL_MIN", "2")),
                    int(os.getenv("MULTIUAC_PROTOCOL_MAX", "3")),
                )
            )

        async with create_task_group() as self._tg:
            LOG.warning('Starting TLSClient("%s", %d)', self.host, self.port)
            self._tg.start_soon(self.handle_outgoing)
            async with await connect_tcp(
                self.host,
                self.port,
                tls=True,
                ssl_context=ssl.SSLContext(protocol=protocol),
            ) as self.client:
                buffer = BufferedByteReceiveStream(self.client)
                self.local_address = self.client.transport_stream.extra_attributes[
                    SocketAttribute.local_address
                ]()
                self.remote_address = self.client.transport_stream.extra_attributes[
                    SocketAttribute.remote_address
                ]()

                self.family = self.client.transport_stream.extra_attributes[
                    SocketAttribute.family
                ]()

                if self.family == AddressFamily.AF_INET6:
                    self.local_address = (
                        f"[{self.local_address[0]}]",
                        self.local_address[1],
                    )
                LOG.warning('local_address = ("%s", %d)', *self.local_address)
                LOG.warning('remote_address = ("%s", %d)', *self.remote_address)

                task_status.started()
                self._pong = 0

                while self.is_running:
                    data_in = b""
                    length = 0
                    while True:
                        header_line = await buffer.receive_until(b"\r\n", 65536)
                        data_in += header_line + b"\r\n"
                        if len(header_line) == 0:
                            break
                        header_str = header_line.decode()
                        if header_str.startswith("Content-Length:"):
                            length = int(header_str[15:])

                    if length:
                        data_in += await buffer.receive_exactly(length)
                    if len(data_in) == 2:
                        LOG.info("receive pong...%d", self._pong)
                        self._scope.cancel()
                        self._pong += 1
                        if self._ping != self._pong:
                            LOG.warning(
                                "ping/ping mismatch pong = %d, ping = %d",
                                self._ping,
                                self._pong,
                            )
                            self._pong = self._ping
                        continue
                    self._tg.start_soon(self.handle_incoming, data_in)

        LOG.warning("Ending TLSClient(%s, %d)", self.host, self.port)

    async def handle_outgoing(self):
        async with self.qrecv:
            async for packet in self.qrecv:
                if not self.is_running:
                    return
                if isinstance(packet, str):
                    packet = packet.encode()
                async with self._send_lock:
                    await self.client.send(packet)

    async def handle_incoming(self, data_in):
        await self.data_callback(self, data_in)

    async def asend_to(self, data: Union[str, bytes], address: tuple[str, int]):
        await self.qsend.send(data)

    async def _keepalive(self, interval):
        self._ping = 0
        while True:
            LOG.info("send ping...%d", self._ping)
            await self.asend_to(b"\r\n\r\n", self.remote_address)
            self._ping += 1
            self._scope = await self._tg.start(self.ping_timer)
            await sleep(0.80 * interval + random.random() * 0.20 * interval)

    def keepalive(self, interval=120.0):
        self._tg.start_soon(self._keepalive, interval)

    def cancel(self):
        self.is_running = False
        self._tg.cancel_scope.cancel()

    async def ping_timer(self, *, task_status=TASK_STATUS_IGNORED):
        with CancelScope() as scope:
            task_status.started(scope)
            await sleep(10.0)
            LOG.error("Timeout waiting for pong")
