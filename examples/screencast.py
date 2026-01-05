import asyncio
import base64
import logging
from pathlib import Path

import httpx

from cdpify import CDPClient
from cdpify.domains import PageClient
from cdpify.domains.page.events import PageEvent

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def save_frame(frame_data: str, frame_number: int, output_dir: Path) -> None:
    try:
        image_bytes = base64.b64decode(frame_data)
        output_path = output_dir / f"frame_{frame_number:04d}.jpg"
        output_path.write_bytes(image_bytes)
        print(f"✓ Saved frame {frame_number}")
    except Exception as e:
        print(f"❌ Error saving frame {frame_number}: {e}")


async def get_ws_url() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:9222/json")
        pages = response.json()

        if not pages:
            raise RuntimeError(
                "No pages found. Is Chrome running with --remote-debugging-port=9222?"
            )

        return pages[0]["webSocketDebuggerUrl"]


async def main():
    output_dir = Path("screencast_frames")
    output_dir.mkdir(exist_ok=True)

    frame_count = 0
    background_tasks = set()

    ws_url = await get_ws_url()
    print(f"Connecting to: {ws_url}\n")

    async with CDPClient(ws_url) as client:
        page = PageClient(client)

        async def process_frame(frame_data: str, session_id: int, frame_num: int):
            try:
                await page.screencast_frame_ack(
                    screencast_frame_ack_session_id=session_id
                )
                await save_frame(frame_data, frame_num, output_dir)
            except Exception as e:
                print(f"❌ Error processing frame {frame_num}: {e}")

        @client.on(PageEvent.SCREENCAST_FRAME)
        async def on_frame(params, cdp_session_id):
            nonlocal frame_count
            frame_count += 1

            # Extract data
            frame_data = params["data"] if isinstance(params, dict) else params.data
            screencast_session_id = (
                params["sessionId"] if isinstance(params, dict) else params.session_id
            )

            print(f"🎬 Frame {frame_count} received!")

            # Process frame in background (ACK + Save)
            task = asyncio.create_task(
                process_frame(frame_data, screencast_session_id, frame_count)
            )
            background_tasks.add(task)
            task.add_done_callback(background_tasks.discard)

        # Enable page domain
        print("📄 Enabling Page domain...")
        await page.enable()

        print("🎬 Starting screencast...")
        await page.start_screencast(
            format="jpeg",
            quality=80,
            max_width=1280,
            max_height=720,
            every_nth_frame=1,
        )

        print("🎥 Recording screencast... Press Ctrl+C to stop\n")

        try:
            await asyncio.sleep(30)
        except KeyboardInterrupt:
            print("\n⏹️  Stopping...")
        finally:
            print("🛑 Stopping screencast...")
            await page.stop_screencast()

            if background_tasks:
                print(f"⏳ Waiting for {len(background_tasks)} frames...")
                await asyncio.gather(*background_tasks, return_exceptions=True)

            print(f"📹 Recorded {frame_count} frames to {output_dir.absolute()}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n✅ Done!")
