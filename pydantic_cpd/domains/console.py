"""Generated from CDP specification"""

from pydantic import BaseModel
from typing import Literal, Any

# Domain Types


class ConsoleMessage(BaseModel):
    """Console message."""

    source: Literal[
        "xml",
        "javascript",
        "network",
        "console-api",
        "storage",
        "appcache",
        "rendering",
        "security",
        "other",
        "deprecation",
        "worker",
    ]
    level: Literal["log", "warning", "error", "debug", "info"]
    text: str
    url: str | None = None
    line: int | None = None
    column: int | None = None


# Command Parameters and Results

# Client


class ConsoleClient:
    """This domain is deprecated - use Runtime or Log instead."""

    def __init__(self, cdp_client: Any) -> None:
        self._cdp = cdp_client

    async def clear_messages(self) -> None:
        """Does nothing."""
        result = await self._cdp.call("Console.clearMessages", {})
        return None

    async def disable(self) -> None:
        """Disables console domain, prevents further console messages from being reported to the client."""
        result = await self._cdp.call("Console.disable", {})
        return None

    async def enable(self) -> None:
        """Enables console domain, sends the messages collected so far to the client by means of the
        `messageAdded` notification."""
        result = await self._cdp.call("Console.enable", {})
        return None
