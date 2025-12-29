import asyncio
import os
from datetime import datetime, timedelta
import logging

from mcp.server.fastmcp import FastMCP
from pydantic import Field
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
    topics=["add-tool-channel"],
    auto_connect=True,
    auto_reconnect=True,
    reconnect_interval=10.0,
    auto_start=True #（默认）：导入模块后自动启动订阅线程
)
async def handle_demo(msg: EnvChannelMessage):
    logger.info("add-tool-channel-local decorator received: %s", msg.message)

mcp = FastMCP(
    name="Channel-world-stramable",
    host="0.0.0.0",
    port=8082,
    log_level="INFO",
)


async def _background_task(augend: float, addend: float) -> None:
    """
    Background async task triggered by hello_world_sse.

    循环发送50次消息，每次包含加法计算结果和时间。
    """
    result = augend + addend
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for count in range(1, 51):
        current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        send_message = f"第{count}次推送: {augend} + {addend} = {result}, 时间: {current_time_str}"
        logger.info(f"send message: {send_message}")
        await publisher.publish(
            topic="env-tool-message-topic",
            message={
                "text": send_message,
                "result": result,
                "augend": augend,
                "addend": addend,
                "count": count,
                "time": current_time_str,
                "start_time": start_time,
            },
        )
        await asyncio.sleep(1)


@mcp.tool()
async def add(
    augend: float = Field(
        0.0,
        description="被加数，加法运算中的第一个数（默认值：0.0）"
    ),
    addend: float = Field(
        0.0,
        description="加数，加法运算中的第二个数（默认值：0.0）"
    )
) -> str:
    """
    执行加法运算，异步推送计算结果。

    该工具会异步执行加法运算，并在后台循环推送50次计算结果和时间信息。
    调用后立即返回提示信息，实际计算和推送在后台进行。

    Returns:
        str: 固定返回字符串：'正在计算中，请等待'
    """
    logger.info(f"Channel_world tool called with augend={augend}, addend={addend}")
    # 提交一个异步后台任务（无需等待完成）
    asyncio.create_task(_background_task(augend, addend))
    return "正在计算中，请等待"


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
