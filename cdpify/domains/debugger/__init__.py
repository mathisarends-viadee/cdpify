"""CDP Debugger Domain"""

from .client import DebuggerClient
from .commands import *
from .events import *
from .types import *

__all__ = ["DebuggerClient"]
