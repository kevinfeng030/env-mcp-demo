import asyncio
import os
from datetime import datetime, timedelta
import logging

from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from env_channel.client import EnvChannelPublisher

from env_channel.client.decorators import env_channel_sub

from env_channel.common.message import EnvChannelMessage

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

publisher = EnvChannelPublisher(
    #server_url="ws://localhost:8765/channel",
    server_url="ws://localhost:8765/channel",
    auto_connect=True,
    auto_reconnect=True,
)


@env_channel_sub(
    #server_url="ws://mcp.aworldagents.com/vpc-pre/stream/sandbox_id_1111111111152/channel",
    server_url="ws://localhost:8765/channel",
    topics=["demo-channel-new"],
    auto_connect=True,
    auto_reconnect=True,
    reconnect_interval=10.0,
    auto_start=True #（默认）：导入模块后自动启动订阅线程
)
async def handle_demo(msg: EnvChannelMessage):
    logger.info("env_channel_sub decorator received: %s", msg.message)

mcp = FastMCP(
    name="Channel-world-stramable",
    host="0.0.0.0",
    port=8082,
    log_level="INFO",
)


async def _background_task() -> None:
    """
    Background async task triggered by hello_world_sse.

    轮询 3 分钟，每次间隔 5 秒发送一条带时间（年月日时分秒）的消息。
    """
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for count in range(1, 51):
        current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        send_message = f"count:{count},start:{start_time},Channel env-channel at {current_time_str}"
        logger.info(f"send message: {send_message}")
        await publisher.publish(
            topic="demo-channel-new",
            message={
                "text": send_message,
                "time": current_time_str,
            },
        )
        await asyncio.sleep(10)


@mcp.tool()
async def hello_world_sse() -> str:
    """
    Output a hello world message.

    This tool simply returns a greeting message "Hello World!".
    """
    logger.info("Channel_world tool called")
    # 提交一个异步后台任务（无需等待完成）
    asyncio.create_task(_background_task())
    return "Channel World SSE!"


@mcp.custom_route("/health", methods=["GET"])
async def health(request: Request) -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse({"status": "healthy", "server": "hello-world-stramable"})


async def main():
    logger.info(
        f"Starting hello-world-stramable MCP server on port {os.getenv('PORT', 8082)}!"
    )
    await mcp.run_streamable_http_async()


if __name__ == "__main__":
    asyncio.run(main())
