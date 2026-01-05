"""CDP DOMSnapshot Domain"""

from .client import DOMSnapshotClient
from .commands import *
from .events import *
from .types import *

__all__ = ["DOMSnapshotClient"]
