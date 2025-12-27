"""Generated CDP domains"""

from pydantic_cpd.domains.page import PageClient
from pydantic_cpd.domains.target import TargetClient
from pydantic_cpd.domains.input import InputClient
from pydantic_cpd.domains.console import ConsoleClient
from pydantic_cpd.domains.network import NetworkClient
from pydantic_cpd.domains.runtime import RuntimeClient
from pydantic_cpd.domains.dom import DOMClient

__all__ = [
    "PageClient",
    "TargetClient",
    "InputClient",
    "ConsoleClient",
    "NetworkClient",
    "RuntimeClient",
    "DOMClient",
]
