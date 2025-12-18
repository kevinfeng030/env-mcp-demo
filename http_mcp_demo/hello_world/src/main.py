import asyncio
import os
from datetime import datetime, timedelta
import logging

from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

mcp = FastMCP(
    name="hello-world-stramable",
    host="0.0.0.0",
    port=int(os.getenv("PORT", 8081)),
    log_level="INFO",
)


@mcp.tool()
async def hello_world_sse() -> str:
    """
    Output a hello world message.

    This tool simply returns a greeting message "Hello World!".
    """
    logger.info("hello_world tool called")
    # 提交一个异步后台任务（无需等待完成）
    return "Hello World SSE!"


@mcp.custom_route("/health", methods=["GET"])
async def health(request: Request) -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse({"status": "healthy", "server": "hello-world-stramable"})


async def main():
    logger.info(
        f"Starting hello-world-stramable MCP server on port {os.getenv('PORT', 8081)}!"
    )
    await mcp.run_streamable_http_async()


if __name__ == "__main__":
    asyncio.run(main())
