"""Example: Publishing messages to Channel Server."""

import asyncio
import logging

from env_channel.client import EnvChannelPublisher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Run the Publisher example."""
    # Create Publisher
    publisher = EnvChannelPublisher(server_url="ws://localhost:8765")

    try:
        # Connect to server
        await publisher.connect()
        logger.info("Connected to Channel Server")

        # Publish messages
        for i in range(5):
            await publisher.publish(
                topic="task-updates",
                message={
                    "task_id": f"task-{i}",
                    "status": "in_progress",
                    "progress": i * 20,
                },
                tags=["task", "update"],
            )
            logger.info(f"Published message {i+1}")
            await asyncio.sleep(1)

        # Publish a completion message
        await publisher.publish(
            channel="task-updates",
            data={
                "task_id": "task-4",
                "status": "completed",
                "result": "All tasks completed successfully",
            },
            tags=["task", "completed"],
        )
        logger.info("Published completion message")

    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        await publisher.disconnect()
        logger.info("Disconnected from server")


if __name__ == "__main__":
    asyncio.run(main())

