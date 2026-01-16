import asyncio
import json
import logging
from collections.abc import AsyncIterator
from typing import Any, Self, TypeVar

import websockets
from websockets.asyncio.client import ClientConnection, connect

from cdpify.domains.shared import CDPModel
from cdpify.events import EventDispatcher
from cdpify.exceptions import (
    CDPCommandException,
    CDPConnectionException,
    CDPTimeoutException,
)

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=CDPModel)


class CDPClient:
    def __init__(
        self,
        url: str,
        *,
        additional_headers: dict[str, str] | None = None,
        max_frame_size: int = 100 * 1024 * 1024,
        default_timeout: float = 30.0,
    ) -> None:
        self.url: str = url
        self._additional_headers: dict[str, str] | None = additional_headers
        self._max_frame_size: int = max_frame_size
        self._default_timeout: float = default_timeout

        self._ws: ClientConnection | None = None
        self._next_message_id: int = 0
        self._pending_requests: dict[int, asyncio.Future[dict[str, Any]]] = {}
        self._message_loop_task: asyncio.Task[None] | None = None
        self._events: EventDispatcher = EventDispatcher()
        self._is_shutting_down: bool = False

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.disconnect()

    @property
    def is_connected(self) -> bool:
        return self._ws is not None

    async def listen(
        self, event_name: str, event_type: type[T], timeout: float | None = None
    ) -> AsyncIterator[T]:
        """
        Listen to typed CDP events.

        Usage:
            async for frame in client.listen(
                "Page.screencastFrame", ScreencastFrameEvent
            ):
                print(frame.data, frame.session_id)
        """
        queue: asyncio.Queue[T] = asyncio.Queue()

        async def handler(params: dict[str, Any]) -> None:
            typed_event = event_type.from_cdp(params)
            await queue.put(typed_event)

        self._events.add_handler(event_name, handler)

        try:
            while True:
                event = await asyncio.wait_for(queue.get(), timeout=timeout)
                yield event
        finally:
            self._events.remove_handler(event_name, handler)

    async def connect(self) -> None:
        if self._ws is not None:
            raise CDPConnectionException("Already connected")

        logger.info(f"Connecting to {self.url}")

        try:
            self._ws = await connect(
                self.url,
                max_size=self._max_frame_size,
                additional_headers=self._additional_headers,
            )
            self._is_shutting_down = False
            self._message_loop_task = asyncio.create_task(self._run_message_loop())
            logger.info("Connected")
        except Exception as e:
            raise CDPConnectionException(f"Connection failed: {e}") from e

    async def disconnect(self) -> None:
        if self._is_shutting_down:
            return

        self._is_shutting_down = True
        logger.info("Disconnecting...")

        await self._stop_message_loop()
        self._cancel_pending_requests()
        await self._close_websocket()

        logger.info("Disconnected")

    async def send_raw(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        session_id: str | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        if not self.is_connected:
            raise CDPConnectionException("Not connected")

        timeout = timeout or self._default_timeout
        msg_id = self._next_message_id
        self._next_message_id += 1

        message = self._build_message(msg_id, method, params, session_id)
        future = self._create_pending_request(msg_id)

        try:
            await self._send(msg_id, method, message)
            return await self._await_response(msg_id, method, future, timeout)
        finally:
            self._pending_requests.pop(msg_id, None)

    def _build_message(
        self,
        msg_id: int,
        method: str,
        params: dict[str, Any] | None,
        session_id: str | None,
    ) -> dict[str, Any]:
        message = {"id": msg_id, "method": method, "params": params or {}}
        if session_id:
            message["sessionId"] = session_id
        return message

    def _create_pending_request(self, msg_id: int) -> asyncio.Future[dict[str, Any]]:
        future: asyncio.Future[dict[str, Any]] = asyncio.Future()
        self._pending_requests[msg_id] = future
        return future

    async def _send(self, msg_id: int, method: str, message: dict[str, Any]) -> None:
        logger.debug(f"→ #{msg_id}: {method}")
        await self._ws.send(json.dumps(message))

    async def _await_response(
        self, msg_id: int, method: str, future: asyncio.Future, timeout: float
    ) -> dict[str, Any]:
        try:
            result = await asyncio.wait_for(future, timeout=timeout)
            logger.debug(f"← #{msg_id}: OK")
            return result
        except asyncio.TimeoutError:
            raise CDPTimeoutException(f"{method} timed out after {timeout}s") from None

    async def _run_message_loop(self) -> None:
        try:
            async for raw_message in self._ws:
                if self._is_shutting_down:
                    break
                await self._process_message(raw_message)
        except websockets.exceptions.ConnectionClosed:
            logger.info("Connection closed")
        except asyncio.CancelledError:
            logger.debug("Message loop cancelled")
            raise
        except Exception:
            logger.exception("Message loop error")
        finally:
            if not self._is_shutting_down:
                await self.disconnect()

    async def _process_message(self, raw: str) -> None:
        msg = json.loads(raw)

        if self._is_cdp_response(msg):
            await self._handle_response(msg)
        elif self._is_cdp_event(msg):
            await self._handle_event(msg)
        else:
            logger.warning(f"Unknown CDP message format: {msg}")

    def _is_cdp_response(self, msg: dict[str, Any]) -> bool:
        """CDP responses contain an 'id' field"""
        return "id" in msg

    def _is_cdp_event(self, msg: dict[str, Any]) -> bool:
        """CDP events contain a 'method' field"""
        return "method" in msg

    async def _handle_response(self, msg: dict[str, Any]) -> None:
        msg_id = msg["id"]
        future = self._pending_requests.get(msg_id)

        if not future or future.done():
            return

        if "error" in msg:
            future.set_exception(CDPCommandException(msg["error"]))
        else:
            future.set_result(msg.get("result", {}))

    async def _handle_event(self, msg: dict[str, Any]) -> None:
        method = msg["method"]
        params = msg.get("params", {})

        logger.debug(f"Event: {method}")
        handled = await self._events.dispatch(method, params)

        if not handled:
            logger.debug(f"Unhandled event: {method}")

    async def _stop_message_loop(self) -> None:
        if self._message_loop_task and not self._message_loop_task.done():
            self._message_loop_task.cancel()
            try:
                await self._message_loop_task
            except asyncio.CancelledError:
                pass

    def _cancel_pending_requests(self) -> None:
        error = CDPConnectionException("Disconnected")
        for future in self._pending_requests.values():
            if not future.done():
                future.set_exception(error)
        self._pending_requests.clear()

    async def _close_websocket(self) -> None:
        if self._ws:
            try:
                await self._ws.close()
            except Exception as e:
                logger.debug(f"Websocket close error: {e}")
            finally:
                self._ws = None
