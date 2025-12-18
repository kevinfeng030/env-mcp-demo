"""
Demo Server: start Channel Server.

Run:
    uv run --active examples/demo/server.py
"""

import asyncio
import logging

from env_channel.server import EnvChannelServer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main() -> None:
    server = EnvChannelServer(host="0.0.0.0", port=8765)
    await server.start()
    logger.info("Server started at ws://0.0.0.0:8765 (Ctrl+C to stop)")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping server...")
    finally:
        await server.stop()
        logger.info("Server stopped")


if __name__ == "__main__":
    asyncio.run(main())

