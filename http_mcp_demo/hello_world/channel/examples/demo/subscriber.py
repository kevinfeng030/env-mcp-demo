"""
Demo Subscriber: subscribe and print messages.

Run (ensure server is up):
    uv run --active examples/demo/subscriber.py
"""

import asyncio
import logging

from env_channel.client import EnvChannelSubscriber
from env_channel.common.message import EnvChannelMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main() -> None:
    url = "ws://localhost:8765"
    # Enable auto_reconnect; also enable auto_connect to skip explicit connect()
    subscriber = EnvChannelSubscriber(
        server_url=url,
        auto_reconnect=True,
        auto_connect=True,
    )

    async def handle_message(msg: EnvChannelMessage) -> None:
        logger.info("Subscriber received: %s", msg.message)

    await subscriber.subscribe(topics=["demo-channel"], handler=handle_message)
    logger.info("Subscriber subscribed to demo-channel at %s", url)

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping subscriber...")
    finally:
        await subscriber.unsubscribe(["demo-channel"])
        await subscriber.disconnect()
        logger.info("Subscriber disconnected")


if __name__ == "__main__":
    asyncio.run(main())

