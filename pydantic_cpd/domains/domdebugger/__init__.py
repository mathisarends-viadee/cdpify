"""CDP DOMDebugger Domain"""

from .types import *
from .commands import *
from .events import *
from .library import DOMDebuggerClient

__all__ = ["DOMDebuggerClient"]
