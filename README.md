# 自定义MCP Server接入示例


## 1. 使用 STDIO 协议的 MCP Server

示例工程: stdio_mcp_server

核心逻辑：根据 mcp_config.json mcpServers 下的第1个配置启动 Stdio 服务。

注意事项：不要直接在 start.sh 中直接启动 Stdio MCP Server


## 2. 使用 HTTP 协议的 MCP Server

包括使用 SSE、StramableHTTP 协议的 MCP Server

核心逻辑：在 start.sh 中启动 SSE、StramableHTTP 协议的 MCP Server，env_server 使用 mcp_config.json mcpServers 下的第1个配置去连接刚刚启动的 MCP Server

