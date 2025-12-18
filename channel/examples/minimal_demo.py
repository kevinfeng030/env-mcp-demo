"""
Minimal demo: start server, publish from one client, subscribe from another.

Steps:
1) Start ChannelServer
2) Subscriber connects and subscribes
3) Publisher connects and sends messages
4) Subscriber prints received messages
"""

import asyncio
import logging

from env_channel.server import EnvChannelServer
from env_channel.client import EnvChannelPublisher, EnvChannelSubscriber
from env_channel.common.message import EnvChannelMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_server(host: str = "0.0.0.0", port: int = 8765) -> EnvChannelServer:
    server = EnvChannelServer(host=host, port=port)
    await server.start()
    logger.info("Server started at ws://%s:%d", host, port)
    return server


async def run_subscriber(url: str) -> None:
    subscriber = EnvChannelSubscriber(server_url=url, auto_reconnect=False)

    async def handle_message(msg: EnvChannelMessage) -> None:
        logger.info("Subscriber received: %s", msg.message)

    await subscriber.connect()
    await subscriber.subscribe(topics=["demo-channel"], handler=handle_message)
    logger.info("Subscriber subscribed to demo-channel")

    # Keep listening for a short period
    await asyncio.sleep(5)
    await subscriber.disconnect()


async def run_publisher(url: str) -> None:
    # Wait a bit to ensure subscriber is ready
    await asyncio.sleep(0.5)

    publisher = EnvChannelPublisher(server_url=url)
    await publisher.connect()

    for i in range(3):
        await publisher.publish(
            topic="demo-channel",
            message={"text": f"hello-{i+1}", "index": i + 1},
        )
        logger.info("Publisher sent message %d", i + 1)
        await asyncio.sleep(0.3)

    await publisher.disconnect()


async def main() -> None:
    server = await run_server()
    url = "ws://localhost:8765"

    try:
        await asyncio.gather(
            run_subscriber(url),
            run_publisher(url),
        )
    finally:
        await server.stop()
        logger.info("Server stopped")


if __name__ == "__main__":
    asyncio.run(main())

