import asyncio
import os
from datetime import datetime, timedelta
import logging

from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from env_channel.client import EnvChannelPublisher

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

publisher = EnvChannelPublisher(
    server_url="ws://localhost:8765",
    auto_connect=True,
    auto_reconnect=True,
)

mcp = FastMCP(
    name="Channel-world-stramable",
    host="0.0.0.0",
    port=int(os.getenv("PORT", 8081)),
    log_level="INFO",
)


async def _background_task() -> None:
    """
    Background async task triggered by hello_world_sse.

    轮询 3 分钟，每次间隔 5 秒发送一条带时间（年月日时分秒）的消息。
    """
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    end_time = datetime.now() + timedelta(minutes=3)
    while datetime.now() < end_time:
        current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        send_message = f"start:{start_time},Channel env-channel at {current_time_str}"
        logger.info(f"send message: {send_message}")
        await publisher.publish(
            topic="demo-channel",
            message={
                "text": send_message,
                "time": current_time_str,
            },
        )
        await asyncio.sleep(5)


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
