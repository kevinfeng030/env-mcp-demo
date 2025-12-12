import asyncio
import os
from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

mcp = FastMCP(
    name="hello-world-stdio",
    log_level="INFO",
)


@mcp.tool()
async def hello_world_stdio() -> str:
    """
    Output a hello world message.

    This tool simply returns a greeting message "Hello World!".
    """
    logger.info("hello_world tool called")
    return "Hello World STDIO!"


@mcp.custom_route("/health", methods=["GET"])
async def health(request: Request) -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse({"status": "healthy", "server": "hello-world-stdio"})


async def main():
    logger.info(
        f"Starting hello-world-stdio MCP server!"
    )
    await mcp.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())
