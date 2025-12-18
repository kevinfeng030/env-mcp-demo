"""Example: Subscribing to messages from Channel Server."""

import asyncio
import logging

from env_channel.client import EnvChannelSubscriber
from env_channel.common.filter import MessageFilter
from env_channel.common.message import EnvChannelMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def handle_message(message: EnvChannelMessage):
    """Handle received messages."""
    logger.info(f"Received message: {message.topic} - {message.message}")


async def main():
    """Run the Subscriber example."""
    # Create Subscriber
    subscriber = EnvChannelSubscriber(
        server_url="ws://localhost:8765",
        auto_reconnect=True,
    )

    try:
        # Connect to server
        await subscriber.connect()
        logger.info("Connected to Channel Server")

        # Create filter (optional)
        filter = MessageFilter(
            topics=["task-updates"],
            tags=["task"],
        )

        # Subscribe to channels
        await subscriber.subscribe(
            topics=["task-updates"],
            handler=handle_message,
            filter=filter,
        )
        logger.info("Subscribed to 'task-updates' channel")

        # Keep listening for messages
        logger.info("Listening for messages... (Press Ctrl+C to stop)")
        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        logger.info("Stopping subscriber...")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        await subscriber.unsubscribe(["task-updates"])
        await subscriber.disconnect()
        logger.info("Disconnected from server")


if __name__ == "__main__":
    asyncio.run(main())

