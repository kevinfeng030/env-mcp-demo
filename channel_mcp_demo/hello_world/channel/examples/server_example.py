"""Example: Starting a Channel Server."""

import asyncio
import logging

from env_channel.server import EnvChannelServer
from env_channel.common.message import EnvChannelMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Run the Channel Server example."""
    # Create and start Channel Server
    server = EnvChannelServer(host="0.0.0.0", port=8765)
    await server.start()

    logger.info("Channel Server is running on ws://0.0.0.0:8765")
    logger.info("Press Ctrl+C to stop")

    try:
        # Keep server running
        while True:
            await asyncio.sleep(1)

            # Example: Publish a test message every 5 seconds
            # In real usage, this would be triggered by MCP server events
            # message = EnvChannelMessage(
            #     channel="test-channel",
            #     data={"message": "Hello from server"},
            # )
            # await server.publish(message)
    except KeyboardInterrupt:
        logger.info("Stopping server...")
        await server.stop()


if __name__ == "__main__":
    asyncio.run(main())

