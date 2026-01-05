"""CDP EventBreakpoints Domain"""

from .client import EventBreakpointsClient
from .commands import *
from .events import *
from .types import *

__all__ = ["EventBreakpointsClient"]
