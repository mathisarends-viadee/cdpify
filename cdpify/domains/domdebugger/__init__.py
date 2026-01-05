"""CDP DOMDebugger Domain"""

from .client import DOMDebuggerClient
from .commands import *
from .events import *
from .types import *

__all__ = ["DOMDebuggerClient"]
