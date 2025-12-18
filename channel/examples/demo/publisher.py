"""
Demo Publisher: send messages to Channel Server.

Run (ensure server is up):
    uv run --active examples/demo/publisher.py
"""

import asyncio
import logging

from env_channel.client import EnvChannelPublisher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main() -> None:
    url = "ws://localhost:8765"
    publisher = EnvChannelPublisher(server_url=url,auto_connect=True)
   ## await publisher.connect()
    logger.info("Publisher connected: %s", url)

    try:
        for i in range(3):
            await publisher.publish(
                topic="demo-channel",
                message={"text": f"hello-{i+1}", "index": i + 1},
            )
            logger.info("Published message %d", i + 1)
            await asyncio.sleep(0.5)
    finally:
        await publisher.disconnect()
        logger.info("Publisher disconnected")


if __name__ == "__main__":
    asyncio.run(main())

