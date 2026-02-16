import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClientWrapper:
    def __init__(self, module_path: str):
        self.module_path = module_path

    async def _call(self, tool_name: str, arguments: dict):
        server_params = StdioServerParameters(
            command="python",
            args=["-m", self.module_path],
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
                return result.content[0].text

    def call(self, tool_name: str, arguments: dict):
        return asyncio.run(self._call(tool_name, arguments))


news_client = MCPClientWrapper("mcp_servers.news_server.server")
mail_client = MCPClientWrapper("mcp_servers.mail_server.server")
