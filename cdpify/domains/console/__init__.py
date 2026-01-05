"""CDP Console Domain"""

from .client import ConsoleClient
from .commands import *
from .events import *
from .types import *

__all__ = ["ConsoleClient"]
