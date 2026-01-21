import asyncio
import base64
import logging
from pathlib import Path

import httpx

from cdpify import CDPClient
from cdpify.domains.page.events import PageEvent, ScreencastFrameEvent

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def save_frame(frame_data: str, frame_number: int, output_dir: Path) -> None:
    image_bytes = base64.b64decode(frame_data)
    output_path = output_dir / f"frame_{frame_number:04d}.jpg"
    output_path.write_bytes(image_bytes)
    print(f"✓ Saved frame {frame_number}")


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

    ws_url = await get_ws_url()
    print(f"Connecting to: {ws_url}\n")

    async with CDPClient(ws_url) as client:
        # Enable page domain
        print("📄 Enabling Page domain...")
        await client.page.enable()

        print("🎬 Starting screencast...")
        await client.page.start_screencast(
            format="jpeg",
            quality=80,
            max_width=1280,
            max_height=720,
            every_nth_frame=1,
        )

        print("🎥 Recording screencast... Press Ctrl+C to stop\n")

        frame_count = 0
        try:
            async for event in client.listen(
                event_name=PageEvent.SCREENCAST_FRAME,
                event_type=ScreencastFrameEvent,
            ):
                frame_count += 1
                print(f"🎬 Frame {frame_count} received!")

                await client.page.screencast_frame_ack(
                    screencast_frame_ack_session_id=event.session_id
                )

                # Save frame
                await save_frame(event.data, frame_count, output_dir)
        except KeyboardInterrupt:
            print("\n⏹️  Stopping...")
        except asyncio.TimeoutError:
            print("\n⏱️  Timeout reached...")
        finally:
            print("🛑 Stopping screencast...")
            await client.page.stop_screencast()
            print(f"📹 Recorded {frame_count} frames to {output_dir.absolute()}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n✅ Done!")
