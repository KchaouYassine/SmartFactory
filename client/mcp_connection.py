# client/mcp_connection.py

import asyncio
from contextlib import asynccontextmanager

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@asynccontextmanager
async def open_mcp_session(command: str = "aas-mcp"):
    """
    Öffnet eine MCP-Session zu aas-mcp und schließt sie automatisch wieder.
    """
    server_params = StdioServerParameters(
        command=command,
        args=[],
        env=None, 
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            try:
                yield session
            finally:
                pass
