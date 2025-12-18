"""Full example: Server, Publisher, and Subscriber working together."""

import asyncio
import logging

from env_channel.server import EnvChannelServer
from env_channel.client import EnvChannelPublisher, EnvChannelSubscriber
from env_channel.common.message import EnvChannelMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_server():
    """Run the Channel Server."""
    server = EnvChannelServer(host="0.0.0.0", port=8765)
    await server.start()
    logger.info("Server started")
    return server


async def run_publisher():
    """Run a Publisher that sends messages."""
    await asyncio.sleep(1)  # Wait for server to start

    publisher = EnvChannelPublisher(server_url="ws://localhost:8765")
    await publisher.connect()

    for i in range(3):
        await publisher.publish(
            topic="test-channel",
            message={"text": f"Hello {i+1}", "number": i + 1},
        )
        await asyncio.sleep(1)

    await publisher.disconnect()


async def run_subscriber():
    """Run a Subscriber that receives messages."""
    await asyncio.sleep(1.5)  # Wait for server to start

    subscriber = EnvChannelSubscriber(server_url="ws://localhost:8765")

    async def handle_message(message: EnvChannelMessage):
        logger.info(f"Subscriber received: {message.message}")

    await subscriber.connect()
    await subscriber.subscribe(
        topics=["test-channel"],
        handler=handle_message,
    )

    # Keep listening
    await asyncio.sleep(5)
    await subscriber.disconnect()


async def main():
    """Run the full example."""
    # Start server
    server = await run_server()

    try:
        # Run publisher and subscriber concurrently
        await asyncio.gather(
            run_publisher(),
            run_subscriber(),
        )
    finally:
        await server.stop()


if __name__ == "__main__":
    asyncio.run(main())

