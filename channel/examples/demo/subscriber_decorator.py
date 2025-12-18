"""
Demo Subscriber with Decorator: subscribe using @env_channel_sub.

Run (ensure server is up):
    uv run --active examples/demo/subscriber_decorator.py
"""

import asyncio
import logging

from env_channel.client import EnvChannelSubscriber, env_channel_sub
from env_channel.common.message import EnvChannelMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 使用装饰器定义消息处理函数（演示自定义自动重连参数）
@env_channel_sub(
    server_url="ws://localhost:8765",
    topics=["demo-channel"],
    auto_connect=True,
    auto_reconnect=True,
    reconnect_interval=10.0,
)
async def handle_demo_messages(msg: EnvChannelMessage) -> None:
    """Handle messages from demo-channel topic."""
    logger.info("Subscriber received (decorator): %s", msg.message)


# 可以定义多个处理函数，订阅不同的 topics，这里使用默认自动重连参数
@env_channel_sub(
    server_url="ws://localhost:8765",
    topics=["demo-channel", "another-channel"],
)
async def handle_multiple_topics(msg: EnvChannelMessage) -> None:
    """Handle messages from multiple topics."""
    logger.info("Subscriber received (multiple topics): %s", msg.message)

async def main() -> None:

    try:
        logger.info("Listening for messages... (Press Ctrl+C to stop)")
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping subscriber...")
    finally:
        logger.info("Subscriber disconnected")


if __name__ == "__main__":
    asyncio.run(main())


