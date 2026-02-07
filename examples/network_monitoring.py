import asyncio
import logging

import httpx

from cdpify import CDPClient
from cdpify.domains.network.events import (
    LoadingFailedEvent,
    LoadingFinishedEvent,
    NetworkEvent,
    RequestWillBeSentEvent,
    ResponseReceivedEvent,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def get_ws_url() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:9222/json")
        pages = response.json()

        if not pages:
            raise RuntimeError(
                "No pages found. Is Chrome running with --remote-debugging-port=9222?"
            )

        return pages[0]["webSocketDebuggerUrl"]


async def monitor_requests(client: CDPClient) -> None:
    async for event in client.listen(
        event_name=NetworkEvent.REQUEST_WILL_BE_SENT,
        event_type=RequestWillBeSentEvent,
    ):
        url = event.request.url
        method = event.request.method
        print(f"📤 Request: {method} {url}")


async def monitor_responses(client: CDPClient) -> None:
    async for event in client.listen(
        event_name=NetworkEvent.RESPONSE_RECEIVED,
        event_type=ResponseReceivedEvent,
    ):
        url = event.response.url
        status = event.response.status
        mime_type = event.response.mime_type
        print(f"📥 Response: {status} {url} ({mime_type})")


async def monitor_loading_finished(client: CDPClient) -> None:
    async for event in client.listen(
        event_name=NetworkEvent.LOADING_FINISHED,
        event_type=LoadingFinishedEvent,
    ):
        request_id = event.request_id
        print(f"✓ Loading finished: {request_id}")


async def monitor_loading_failed(client: CDPClient) -> None:
    async for event in client.listen(
        event_name=NetworkEvent.LOADING_FAILED,
        event_type=LoadingFailedEvent,
    ):
        request_id = event.request_id
        error_text = event.error_text
        print(f"✗ Loading failed: {request_id} - {error_text}")


async def main() -> None:
    ws_url = await get_ws_url()
    print(f"Connecting to: {ws_url}\n")

    async with CDPClient(ws_url) as client:
        await client.network.enable()

        print("🌐 Network monitoring started...")
        print("Press Ctrl+C to stop\n")

        tasks = [
            asyncio.create_task(monitor_requests(client)),
            asyncio.create_task(monitor_responses(client)),
            asyncio.create_task(monitor_loading_finished(client)),
            asyncio.create_task(monitor_loading_failed(client)),
        ]

        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            print("\n⏹️  Stopping...")
        finally:
            for task in tasks:
                task.cancel()
            print("✅ Network monitoring stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n✅ Done!")
