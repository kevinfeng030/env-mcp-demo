# 自定义MCP Server接入示例

setup.sh：用于设置项目前置依赖，包括启动 SSE / StreamableHTTP MCP Server

mcp_config.json：用于连接到当前mcp server


## 1. 使用 STDIO 协议的 MCP Server

示例工程: stdio_mcp_server

工作原理：根据 mcp_config.json mcpServers 下的第1个配置启动 Stdio 服务。

注意事项：不要直接在 setup.sh 中直接启动 Stdio MCP Server


## 2. 使用 HTTP 协议的 MCP Server

示例工程：http_mcp_demo

包括使用 SSE、StramableHTTP 协议的 MCP Server

工作原理：在 setup.sh 中启动 SSE、StramableHTTP 协议的 MCP Server，env_server 使用 mcp_config.json mcpServers 下的第1个配置连接刚刚启动的 MCP Server

注意事项：setup.sh 启动 SSE、StreamableHTTP MCP Server `不要放入后台运行`，否则会重复启动