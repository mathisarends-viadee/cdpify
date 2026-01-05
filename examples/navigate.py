import asyncio

import httpx

from cdpify import CDPClient
from cdpify.domains import PageClient


async def get_ws_url() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:9222/json")
        pages = response.json()
        if not pages:
            raise RuntimeError(
                "No pages found. Is Chrome running with --remote-debugging-port=9222?"
            )
        return pages[0]["webSocketDebuggerUrl"]


async def test_basic():
    print("=== Test 1: Basic Navigation ===")

    ws_url = await get_ws_url()
    print(f"Connecting to: {ws_url}")

    async with CDPClient(ws_url) as client:
        page_client = PageClient(client)

        result = await page_client.navigate(url="https://example.com")
        print(f"Navigation Result: {result}")


if __name__ == "__main__":
    asyncio.run(test_basic())
