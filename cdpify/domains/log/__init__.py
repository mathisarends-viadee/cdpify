"""CDP Log Domain"""

from .client import LogClient
from .commands import *
from .events import *
from .types import *

__all__ = ["LogClient"]
