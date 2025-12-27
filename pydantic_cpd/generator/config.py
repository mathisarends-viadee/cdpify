from enum import StrEnum


class CDPDomain(StrEnum):
    PAGE = "Page"
    DOM = "DOM"
    INPUT = "Input"
    NETWORK = "Network"
    TARGET = "Target"
    RUNTIME = "Runtime"
    CONSOLE = "Console"

    DEBUGGER = "Debugger"
    PROFILER = "Profiler"
    HEAP_PROFILER = "HeapProfiler"
    PERFORMANCE = "Performance"

    CSS = "CSS"
    OVERLAY = "Overlay"
    ANIMATION = "Animation"
    LAYER_TREE = "LayerTree"

    STORAGE = "Storage"
    DATABASE = "Database"
    INDEXED_DB = "IndexedDB"
    CACHE_STORAGE = "CacheStorage"
    DOM_STORAGE = "DOMStorage"
    APPLICATION_CACHE = "ApplicationCache"

    FETCH = "Fetch"
    WEB_AUDIO = "WebAudio"
    WEB_AUTHN = "WebAuthn"
    MEDIA = "Media"
    SERVICE_WORKER = "ServiceWorker"
    BACKGROUND_SERVICE = "BackgroundService"

    EMULATION = "Emulation"
    DEVICE_ORIENTATION = "DeviceOrientation"

    BROWSER = "Browser"
    SYSTEM_INFO = "SystemInfo"
    SECURITY = "Security"
    LOG = "Log"
    TETHERING = "Tethering"

    ACCESSIBILITY = "Accessibility"
    AUDITS = "Audits"

    TRACING = "Tracing"
    SCHEMA = "Schema"
    CAST = "Cast"
    DOM_SNAPSHOT = "DOMSnapshot"
    DOM_DEBUGGER = "DOMDebugger"
    EVENT_BREAKPOINTS = "EventBreakpoints"
    IO = "IO"
    MEMORY = "Memory"


DOMAINS_TO_GENERATE: set[CDPDomain] = {
    CDPDomain.PAGE,  # Navigation, Screenshots, Lifecycle
    CDPDomain.DOM,  # DOM manipulation
    CDPDomain.INPUT,  # Mouse, Keyboard, Touch
    CDPDomain.NETWORK,  # Request monitoring
    CDPDomain.TARGET,  # Tab/Page management
    CDPDomain.RUNTIME,  # JavaScript execution
    CDPDomain.CONSOLE,  # Console API
}
