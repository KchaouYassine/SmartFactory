import asyncio
import json
from typing import List, Dict

from mcp import types as mcp_types
from client.mcp_connection import open_mcp_session


async def get_all_shells() -> List[Dict]:
    """
    Ruft get_shells über MCP auf und gibt die Liste der Shell-Objekte zurück.
    """
    async with open_mcp_session() as session:
        result = await session.call_tool("get_shells", {})

        if result.isError:
            messages = [
                part.text
                for part in result.content
                if isinstance(part, mcp_types.TextContent)
            ]
            raise RuntimeError("get_shells failed: " + " | ".join(messages))

        text_parts = [
            part.text
            for part in result.content
            if isinstance(part, mcp_types.TextContent)
        ]
        if not text_parts:
            raise RuntimeError("No text content in get_shells result")

        data = json.loads(text_parts[0])

        # data hat Struktur: {"paging_metadata": {...}, "result": [ ...Shells... ]}
        shells = data["result"]
        return shells


async def get_kuba_shells() -> List[Dict]:
    """
    Gibt alle Shells zurück, deren namespace-Erweiterung '_KUBA' ist.
    """
    shells = await get_all_shells()

    kuba_shells = [
        s for s in shells
        if any(
            ext.get("name") == "namespace" and ext.get("value") == "_KUBA"
            for ext in s.get("extensions", [])
        )
    ]

    return kuba_shells


if __name__ == "__main__":
    async def _test():
        kuba_shells = await get_kuba_shells()
        print(f"Shells mit namespace='_KUBA': {len(kuba_shells)}\n")
        for shell in kuba_shells:
            asset_type = shell.get("assetInformation", {}).get("assetType")
            print(
                f"- idShort={shell.get('idShort'):25} "
                f"| id={shell.get('id'):6} "
                f"| assetType={asset_type}"
            )

    asyncio.run(_test())
