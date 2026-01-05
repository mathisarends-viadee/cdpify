"""CDP Accessibility Domain"""

from .client import AccessibilityClient
from .commands import *
from .events import *
from .types import *

__all__ = ["AccessibilityClient"]
