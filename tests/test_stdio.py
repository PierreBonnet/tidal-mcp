import asyncio
import sys

from mcp import Client
from mcp.client.stdio import StdioServerParameters


def test_stdio_discovery_and_safe_auth_status_from_another_directory(tmp_path):
    async def scenario():
        parameters = StdioServerParameters(
            command=sys.executable,
            args=["-m", "tidal_mcp"],
            cwd=tmp_path,
            env={
                "TIDAL_MCP_DATA_DIR": str(tmp_path),
                "TIDAL_MCP_SESSION_FILE": str(tmp_path / "absent.json"),
                "TIDAL_MCP_ENABLE_WRITES": "false",
            },
        )
        async with Client(parameters) as client:
            tools = await client.list_tools()
            assert any(tool.name == "tidal_auth_status" for tool in tools.tools)
            result = await client.call_tool("tidal_auth_status", {})
            assert result.is_error is False
            assert result.structured_content["authenticated"] is False

    asyncio.run(asyncio.wait_for(scenario(), timeout=20))
