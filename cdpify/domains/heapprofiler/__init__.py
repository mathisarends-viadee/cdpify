"""CDP HeapProfiler Domain"""

from .client import HeapProfilerClient
from .commands import *
from .events import *
from .types import *

__all__ = ["HeapProfilerClient"]
