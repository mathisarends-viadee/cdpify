"""Generated from CDP specification"""

from pydantic import BaseModel, Field
from typing import Literal, Any

from pydantic_cpd.domains import dom
from pydantic_cpd.domains import debugger
from pydantic_cpd.domains import emulation
from pydantic_cpd.domains import io
from pydantic_cpd.domains import network
from pydantic_cpd.domains import runtime

# Alias for cross-domain type references
DOM = dom
Debugger = debugger
Emulation = emulation
IO = io
Network = network
Runtime = runtime

# Domain Types

FrameId = str
AdFrameType = Literal["none", "child", "root"]
AdFrameExplanation = Literal["ParentIsAd", "CreatedByAdScript", "MatchedBlockingRule"]


class AdFrameStatus(BaseModel):
    """Indicates whether a frame has been identified as an ad and why."""

    ad_frame_type: AdFrameType
    explanations: list[AdFrameExplanation] | None = None


class AdScriptId(BaseModel):
    """Identifies the script which caused a script or frame to be labelled as an
    ad."""

    script_id: Runtime.ScriptId
    debugger_id: Runtime.UniqueDebuggerId


class AdScriptAncestry(BaseModel):
    """Encapsulates the script ancestry and the root script filterlist rule that
    caused the frame to be labelled as an ad. Only created when `ancestryChain`
    is not empty."""

    ancestry_chain: list[AdScriptId]
    root_script_filterlist_rule: str | None = None


SecureContextType = Literal[
    "Secure", "SecureLocalhost", "InsecureScheme", "InsecureAncestor"
]
CrossOriginIsolatedContextType = Literal[
    "Isolated", "NotIsolated", "NotIsolatedFeatureDisabled"
]
GatedAPIFeatures = Literal[
    "SharedArrayBuffers",
    "SharedArrayBuffersTransferAllowed",
    "PerformanceMeasureMemory",
    "PerformanceProfile",
]
PermissionsPolicyFeature = Literal[
    "accelerometer",
    "all-screens-capture",
    "ambient-light-sensor",
    "aria-notify",
    "attribution-reporting",
    "autofill",
    "autoplay",
    "bluetooth",
    "browsing-topics",
    "camera",
    "captured-surface-control",
    "ch-dpr",
    "ch-device-memory",
    "ch-downlink",
    "ch-ect",
    "ch-prefers-color-scheme",
    "ch-prefers-reduced-motion",
    "ch-prefers-reduced-transparency",
    "ch-rtt",
    "ch-save-data",
    "ch-ua",
    "ch-ua-arch",
    "ch-ua-bitness",
    "ch-ua-high-entropy-values",
    "ch-ua-platform",
    "ch-ua-model",
    "ch-ua-mobile",
    "ch-ua-form-factors",
    "ch-ua-full-version",
    "ch-ua-full-version-list",
    "ch-ua-platform-version",
    "ch-ua-wow64",
    "ch-viewport-height",
    "ch-viewport-width",
    "ch-width",
    "clipboard-read",
    "clipboard-write",
    "compute-pressure",
    "controlled-frame",
    "cross-origin-isolated",
    "deferred-fetch",
    "deferred-fetch-minimal",
    "device-attributes",
    "digital-credentials-create",
    "digital-credentials-get",
    "direct-sockets",
    "direct-sockets-multicast",
    "direct-sockets-private",
    "display-capture",
    "document-domain",
    "encrypted-media",
    "execution-while-out-of-viewport",
    "execution-while-not-rendered",
    "fenced-unpartitioned-storage-read",
    "focus-without-user-activation",
    "fullscreen",
    "frobulate",
    "gamepad",
    "geolocation",
    "gyroscope",
    "hid",
    "identity-credentials-get",
    "idle-detection",
    "interest-cohort",
    "join-ad-interest-group",
    "keyboard-map",
    "language-detector",
    "language-model",
    "local-fonts",
    "local-network",
    "local-network-access",
    "loopback-network",
    "magnetometer",
    "manual-text",
    "media-playback-while-not-visible",
    "microphone",
    "midi",
    "on-device-speech-recognition",
    "otp-credentials",
    "payment",
    "picture-in-picture",
    "private-aggregation",
    "private-state-token-issuance",
    "private-state-token-redemption",
    "publickey-credentials-create",
    "publickey-credentials-get",
    "record-ad-auction-events",
    "rewriter",
    "run-ad-auction",
    "screen-wake-lock",
    "serial",
    "shared-storage",
    "shared-storage-select-url",
    "smart-card",
    "speaker-selection",
    "storage-access",
    "sub-apps",
    "summarizer",
    "sync-xhr",
    "translator",
    "unload",
    "usb",
    "usb-unrestricted",
    "vertical-scroll",
    "web-app-installation",
    "web-printing",
    "web-share",
    "window-management",
    "writer",
    "xr-spatial-tracking",
]
PermissionsPolicyBlockReason = Literal[
    "Header", "IframeAttribute", "InFencedFrameTree", "InIsolatedApp"
]


class PermissionsPolicyBlockLocator(BaseModel):
    frame_id: FrameId
    block_reason: PermissionsPolicyBlockReason


class PermissionsPolicyFeatureState(BaseModel):
    feature: PermissionsPolicyFeature
    allowed: bool
    locator: PermissionsPolicyBlockLocator | None = None


OriginTrialTokenStatus = Literal[
    "Success",
    "NotSupported",
    "Insecure",
    "Expired",
    "WrongOrigin",
    "InvalidSignature",
    "Malformed",
    "WrongVersion",
    "FeatureDisabled",
    "TokenDisabled",
    "FeatureDisabledForUser",
    "UnknownTrial",
]
OriginTrialStatus = Literal[
    "Enabled", "ValidTokenNotProvided", "OSNotSupported", "TrialNotAllowed"
]
OriginTrialUsageRestriction = Literal["None", "Subset"]


class OriginTrialToken(BaseModel):
    origin: str
    match_sub_domains: bool
    trial_name: str
    expiry_time: Network.TimeSinceEpoch
    is_third_party: bool
    usage_restriction: OriginTrialUsageRestriction


class OriginTrialTokenWithStatus(BaseModel):
    raw_token_text: str
    parsed_token: OriginTrialToken | None = None
    status: OriginTrialTokenStatus


class OriginTrial(BaseModel):
    trial_name: str
    status: OriginTrialStatus
    tokens_with_status: list[OriginTrialTokenWithStatus]


class SecurityOriginDetails(BaseModel):
    """Additional information about the frame document's security origin."""

    is_localhost: bool


class Frame(BaseModel):
    """Information about the Frame on the page."""

    id: FrameId
    parent_id: FrameId | None = None
    loader_id: Network.LoaderId
    name: str | None = None
    url: str
    url_fragment: str | None = None
    domain_and_registry: str
    security_origin: str
    security_origin_details: SecurityOriginDetails | None = None
    mime_type: str
    unreachable_url: str | None = None
    ad_frame_status: AdFrameStatus | None = None
    secure_context_type: SecureContextType
    cross_origin_isolated_context_type: CrossOriginIsolatedContextType
    gated_a_p_i_features: list[GatedAPIFeatures]


class FrameResource(BaseModel):
    """Information about the Resource on the page."""

    url: str
    type: Network.ResourceType
    mime_type: str
    last_modified: Network.TimeSinceEpoch | None = None
    content_size: float | None = None
    failed: bool | None = None
    canceled: bool | None = None


class FrameResourceTree(BaseModel):
    """Information about the Frame hierarchy along with their cached resources."""

    frame: Frame
    child_frames: list[FrameResourceTree] | None = None
    resources: list[FrameResource]


class FrameTree(BaseModel):
    """Information about the Frame hierarchy."""

    frame: Frame
    child_frames: list[FrameTree] | None = None


ScriptIdentifier = str
TransitionType = Literal[
    "link",
    "typed",
    "address_bar",
    "auto_bookmark",
    "auto_subframe",
    "manual_subframe",
    "generated",
    "auto_toplevel",
    "form_submit",
    "reload",
    "keyword",
    "keyword_generated",
    "other",
]


class NavigationEntry(BaseModel):
    """Navigation history entry."""

    id: int
    url: str
    user_typed_u_r_l: str
    title: str
    transition_type: TransitionType


class ScreencastFrameMetadata(BaseModel):
    """Screencast frame metadata."""

    offset_top: float
    page_scale_factor: float
    device_width: float
    device_height: float
    scroll_offset_x: float
    scroll_offset_y: float
    timestamp: Network.TimeSinceEpoch | None = None


DialogType = Literal["alert", "confirm", "prompt", "beforeunload"]


class AppManifestError(BaseModel):
    """Error while paring app manifest."""

    message: str
    critical: int
    line: int
    column: int


class AppManifestParsedProperties(BaseModel):
    """Parsed app manifest properties."""

    scope: str


class LayoutViewport(BaseModel):
    """Layout viewport position and dimensions."""

    page_x: int
    page_y: int
    client_width: int
    client_height: int


class VisualViewport(BaseModel):
    """Visual viewport position, dimensions, and scale."""

    offset_x: float
    offset_y: float
    page_x: float
    page_y: float
    client_width: float
    client_height: float
    scale: float
    zoom: float | None = None


class Viewport(BaseModel):
    """Viewport for capturing screenshot."""

    x: float
    y: float
    width: float
    height: float
    scale: float


class FontFamilies(BaseModel):
    """Generic font families collection."""

    standard: str | None = None
    fixed: str | None = None
    serif: str | None = None
    sans_serif: str | None = None
    cursive: str | None = None
    fantasy: str | None = None
    math: str | None = None


class ScriptFontFamilies(BaseModel):
    """Font families collection for a script."""

    script: str
    font_families: FontFamilies


class FontSizes(BaseModel):
    """Default font sizes."""

    standard: int | None = None
    fixed: int | None = None


ClientNavigationReason = Literal[
    "anchorClick",
    "formSubmissionGet",
    "formSubmissionPost",
    "httpHeaderRefresh",
    "initialFrameNavigation",
    "metaTagRefresh",
    "other",
    "pageBlockInterstitial",
    "reload",
    "scriptInitiated",
]
ClientNavigationDisposition = Literal["currentTab", "newTab", "newWindow", "download"]


class InstallabilityErrorArgument(BaseModel):
    name: str
    value: str


class InstallabilityError(BaseModel):
    """The installability error"""

    error_id: str
    error_arguments: list[InstallabilityErrorArgument]


ReferrerPolicy = Literal[
    "noReferrer",
    "noReferrerWhenDowngrade",
    "origin",
    "originWhenCrossOrigin",
    "sameOrigin",
    "strictOrigin",
    "strictOriginWhenCrossOrigin",
    "unsafeUrl",
]


class CompilationCacheParams(BaseModel):
    """Per-script compilation cache parameters for `Page.produceCompilationCache`"""

    url: str
    eager: bool | None = None


class FileFilter(BaseModel):
    name: str | None = None
    accepts: list[str] | None = None


class FileHandler(BaseModel):
    action: str
    name: str
    icons: list[ImageResource] | None = None
    accepts: list[FileFilter] | None = None
    launch_type: str


class ImageResource(BaseModel):
    """The image definition used in both icon and screenshot."""

    url: str
    sizes: str | None = None
    type: str | None = None


class LaunchHandler(BaseModel):
    client_mode: str


class ProtocolHandler(BaseModel):
    protocol: str
    url: str


class RelatedApplication(BaseModel):
    id: str | None = None
    url: str


class ScopeExtension(BaseModel):
    origin: str
    has_origin_wildcard: bool


class Screenshot(BaseModel):
    image: ImageResource
    form_factor: str
    label: str | None = None


class ShareTarget(BaseModel):
    action: str
    method: str
    enctype: str
    title: str | None = None
    text: str | None = None
    url: str | None = None
    files: list[FileFilter] | None = None


class Shortcut(BaseModel):
    name: str
    url: str


class WebAppManifest(BaseModel):
    background_color: str | None = None
    description: str | None = None
    dir: str | None = None
    display: str | None = None
    display_overrides: list[str] | None = None
    file_handlers: list[FileHandler] | None = None
    icons: list[ImageResource] | None = None
    id: str | None = None
    lang: str | None = None
    launch_handler: LaunchHandler | None = None
    name: str | None = None
    orientation: str | None = None
    prefer_related_applications: bool | None = None
    protocol_handlers: list[ProtocolHandler] | None = None
    related_applications: list[RelatedApplication] | None = None
    scope: str | None = None
    scope_extensions: list[ScopeExtension] | None = None
    screenshots: list[Screenshot] | None = None
    share_target: ShareTarget | None = None
    short_name: str | None = None
    shortcuts: list[Shortcut] | None = None
    start_url: str | None = None
    theme_color: str | None = None


NavigationType = Literal["Navigation", "BackForwardCacheRestore"]
BackForwardCacheNotRestoredReason = Literal[
    "NotPrimaryMainFrame",
    "BackForwardCacheDisabled",
    "RelatedActiveContentsExist",
    "HTTPStatusNotOK",
    "SchemeNotHTTPOrHTTPS",
    "Loading",
    "WasGrantedMediaAccess",
    "DisableForRenderFrameHostCalled",
    "DomainNotAllowed",
    "HTTPMethodNotGET",
    "SubframeIsNavigating",
    "Timeout",
    "CacheLimit",
    "JavaScriptExecution",
    "RendererProcessKilled",
    "RendererProcessCrashed",
    "SchedulerTrackedFeatureUsed",
    "ConflictingBrowsingInstance",
    "CacheFlushed",
    "ServiceWorkerVersionActivation",
    "SessionRestored",
    "ServiceWorkerPostMessage",
    "EnteredBackForwardCacheBeforeServiceWorkerHostAdded",
    "RenderFrameHostReused_SameSite",
    "RenderFrameHostReused_CrossSite",
    "ServiceWorkerClaim",
    "IgnoreEventAndEvict",
    "HaveInnerContents",
    "TimeoutPuttingInCache",
    "BackForwardCacheDisabledByLowMemory",
    "BackForwardCacheDisabledByCommandLine",
    "NetworkRequestDatapipeDrainedAsBytesConsumer",
    "NetworkRequestRedirected",
    "NetworkRequestTimeout",
    "NetworkExceedsBufferLimit",
    "NavigationCancelledWhileRestoring",
    "NotMostRecentNavigationEntry",
    "BackForwardCacheDisabledForPrerender",
    "UserAgentOverrideDiffers",
    "ForegroundCacheLimit",
    "BrowsingInstanceNotSwapped",
    "BackForwardCacheDisabledForDelegate",
    "UnloadHandlerExistsInMainFrame",
    "UnloadHandlerExistsInSubFrame",
    "ServiceWorkerUnregistration",
    "CacheControlNoStore",
    "CacheControlNoStoreCookieModified",
    "CacheControlNoStoreHTTPOnlyCookieModified",
    "NoResponseHead",
    "Unknown",
    "ActivationNavigationsDisallowedForBug1234857",
    "ErrorDocument",
    "FencedFramesEmbedder",
    "CookieDisabled",
    "HTTPAuthRequired",
    "CookieFlushed",
    "BroadcastChannelOnMessage",
    "WebViewSettingsChanged",
    "WebViewJavaScriptObjectChanged",
    "WebViewMessageListenerInjected",
    "WebViewSafeBrowsingAllowlistChanged",
    "WebViewDocumentStartJavascriptChanged",
    "WebSocket",
    "WebTransport",
    "WebRTC",
    "MainResourceHasCacheControlNoStore",
    "MainResourceHasCacheControlNoCache",
    "SubresourceHasCacheControlNoStore",
    "SubresourceHasCacheControlNoCache",
    "ContainsPlugins",
    "DocumentLoaded",
    "OutstandingNetworkRequestOthers",
    "RequestedMIDIPermission",
    "RequestedAudioCapturePermission",
    "RequestedVideoCapturePermission",
    "RequestedBackForwardCacheBlockedSensors",
    "RequestedBackgroundWorkPermission",
    "BroadcastChannel",
    "WebXR",
    "SharedWorker",
    "SharedWorkerMessage",
    "SharedWorkerWithNoActiveClient",
    "WebLocks",
    "WebHID",
    "WebBluetooth",
    "WebShare",
    "RequestedStorageAccessGrant",
    "WebNfc",
    "OutstandingNetworkRequestFetch",
    "OutstandingNetworkRequestXHR",
    "AppBanner",
    "Printing",
    "WebDatabase",
    "PictureInPicture",
    "SpeechRecognizer",
    "IdleManager",
    "PaymentManager",
    "SpeechSynthesis",
    "KeyboardLock",
    "WebOTPService",
    "OutstandingNetworkRequestDirectSocket",
    "InjectedJavascript",
    "InjectedStyleSheet",
    "KeepaliveRequest",
    "IndexedDBEvent",
    "Dummy",
    "JsNetworkRequestReceivedCacheControlNoStoreResource",
    "WebRTCUsedWithCCNS",
    "WebTransportUsedWithCCNS",
    "WebSocketUsedWithCCNS",
    "SmartCard",
    "LiveMediaStreamTrack",
    "UnloadHandler",
    "ParserAborted",
    "ContentSecurityHandler",
    "ContentWebAuthenticationAPI",
    "ContentFileChooser",
    "ContentSerial",
    "ContentFileSystemAccess",
    "ContentMediaDevicesDispatcherHost",
    "ContentWebBluetooth",
    "ContentWebUSB",
    "ContentMediaSessionService",
    "ContentScreenReader",
    "ContentDiscarded",
    "EmbedderPopupBlockerTabHelper",
    "EmbedderSafeBrowsingTriggeredPopupBlocker",
    "EmbedderSafeBrowsingThreatDetails",
    "EmbedderAppBannerManager",
    "EmbedderDomDistillerViewerSource",
    "EmbedderDomDistillerSelfDeletingRequestDelegate",
    "EmbedderOomInterventionTabHelper",
    "EmbedderOfflinePage",
    "EmbedderChromePasswordManagerClientBindCredentialManager",
    "EmbedderPermissionRequestManager",
    "EmbedderModalDialog",
    "EmbedderExtensions",
    "EmbedderExtensionMessaging",
    "EmbedderExtensionMessagingForOpenPort",
    "EmbedderExtensionSentMessageToCachedFrame",
    "RequestedByWebViewClient",
    "PostMessageByWebViewClient",
    "CacheControlNoStoreDeviceBoundSessionTerminated",
    "CacheLimitPrunedOnModerateMemoryPressure",
    "CacheLimitPrunedOnCriticalMemoryPressure",
]
BackForwardCacheNotRestoredReasonType = Literal[
    "SupportPending", "PageSupportNeeded", "Circumstantial"
]


class BackForwardCacheBlockingDetails(BaseModel):
    url: str | None = None
    function: str | None = None
    line_number: int
    column_number: int


class BackForwardCacheNotRestoredExplanation(BaseModel):
    type: BackForwardCacheNotRestoredReasonType
    reason: BackForwardCacheNotRestoredReason
    context: str | None = None
    details: list[BackForwardCacheBlockingDetails] | None = None


class BackForwardCacheNotRestoredExplanationTree(BaseModel):
    url: str
    explanations: list[BackForwardCacheNotRestoredExplanation]
    children: list[BackForwardCacheNotRestoredExplanationTree]


# Command Parameters and Results


class AddscripttoevaluateonloadParams(BaseModel):
    """Deprecated, please use addScriptToEvaluateOnNewDocument instead."""

    script_source: str = Field(alias="scriptSource")


class AddscripttoevaluateonloadResult(BaseModel):
    identifier: ScriptIdentifier = Field(alias="identifier")


class AddscripttoevaluateonnewdocumentParams(BaseModel):
    """Evaluates given script in every frame upon creation (before loading frame's scripts)."""

    source: str = Field(alias="source")
    world_name: str | None = Field(default=None, alias="worldName")
    include_command_line_a_p_i: bool | None = Field(
        default=None, alias="includeCommandLineAPI"
    )
    run_immediately: bool | None = Field(default=None, alias="runImmediately")


class AddscripttoevaluateonnewdocumentResult(BaseModel):
    identifier: ScriptIdentifier = Field(alias="identifier")


class CapturescreenshotParams(BaseModel):
    """Capture page screenshot."""

    format: Literal["jpeg", "png", "webp"] | None = Field(default=None, alias="format")
    quality: int | None = Field(default=None, alias="quality")
    clip: Viewport | None = Field(default=None, alias="clip")
    from_surface: bool | None = Field(default=None, alias="fromSurface")
    capture_beyond_viewport: bool | None = Field(
        default=None, alias="captureBeyondViewport"
    )
    optimize_for_speed: bool | None = Field(default=None, alias="optimizeForSpeed")


class CapturescreenshotResult(BaseModel):
    data: str = Field(alias="data")


class CapturesnapshotParams(BaseModel):
    """Returns a snapshot of the page as a string. For MHTML format, the serialization includes
    iframes, shadow DOM, external resources, and element-inline styles."""

    format: Literal["mhtml"] | None = Field(default=None, alias="format")


class CapturesnapshotResult(BaseModel):
    data: str = Field(alias="data")


class CreateisolatedworldParams(BaseModel):
    """Creates an isolated world for the given frame."""

    frame_id: FrameId = Field(alias="frameId")
    world_name: str | None = Field(default=None, alias="worldName")
    grant_univeral_access: bool | None = Field(
        default=None, alias="grantUniveralAccess"
    )


class CreateisolatedworldResult(BaseModel):
    execution_context_id: Runtime.ExecutionContextId = Field(alias="executionContextId")


class DeletecookieParams(BaseModel):
    """Deletes browser cookie with given name, domain and path."""

    cookie_name: str = Field(alias="cookieName")
    url: str = Field(alias="url")


class EnableParams(BaseModel):
    """Enables page domain notifications."""

    enable_file_chooser_opened_event: bool | None = Field(
        default=None, alias="enableFileChooserOpenedEvent"
    )


class GetappmanifestParams(BaseModel):
    """Gets the processed manifest for this current document.
    This API always waits for the manifest to be loaded.
    If manifestId is provided, and it does not match the manifest of the
      current document, this API errors out.
    If there is not a loaded page, this API errors out immediately."""

    manifest_id: str | None = Field(default=None, alias="manifestId")


class GetappmanifestResult(BaseModel):
    url: str = Field(alias="url")
    errors: list[AppManifestError] = Field(alias="errors")
    data: str | None = Field(default=None, alias="data")
    parsed: AppManifestParsedProperties | None = Field(default=None, alias="parsed")
    manifest: WebAppManifest = Field(alias="manifest")


class GetinstallabilityerrorsResult(BaseModel):
    installability_errors: list[InstallabilityError] = Field(
        alias="installabilityErrors"
    )


class GetmanifesticonsResult(BaseModel):
    primary_icon: str | None = Field(default=None, alias="primaryIcon")


class GetappidResult(BaseModel):
    app_id: str | None = Field(default=None, alias="appId")
    recommended_id: str | None = Field(default=None, alias="recommendedId")


class GetadscriptancestryParams(BaseModel):
    frame_id: FrameId = Field(alias="frameId")


class GetadscriptancestryResult(BaseModel):
    ad_script_ancestry: AdScriptAncestry | None = Field(
        default=None, alias="adScriptAncestry"
    )


class GetframetreeResult(BaseModel):
    frame_tree: FrameTree = Field(alias="frameTree")


class GetlayoutmetricsResult(BaseModel):
    layout_viewport: LayoutViewport = Field(alias="layoutViewport")
    visual_viewport: VisualViewport = Field(alias="visualViewport")
    content_size: DOM.Rect = Field(alias="contentSize")
    css_layout_viewport: LayoutViewport = Field(alias="cssLayoutViewport")
    css_visual_viewport: VisualViewport = Field(alias="cssVisualViewport")
    css_content_size: DOM.Rect = Field(alias="cssContentSize")


class GetnavigationhistoryResult(BaseModel):
    current_index: int = Field(alias="currentIndex")
    entries: list[NavigationEntry] = Field(alias="entries")


class GetresourcecontentParams(BaseModel):
    """Returns content of the given resource."""

    frame_id: FrameId = Field(alias="frameId")
    url: str = Field(alias="url")


class GetresourcecontentResult(BaseModel):
    content: str = Field(alias="content")
    base64_encoded: bool = Field(alias="base64Encoded")


class GetresourcetreeResult(BaseModel):
    frame_tree: FrameResourceTree = Field(alias="frameTree")


class HandlejavascriptdialogParams(BaseModel):
    """Accepts or dismisses a JavaScript initiated dialog (alert, confirm, prompt, or onbeforeunload)."""

    accept: bool = Field(alias="accept")
    prompt_text: str | None = Field(default=None, alias="promptText")


class NavigateParams(BaseModel):
    """Navigates current page to the given URL."""

    url: str = Field(alias="url")
    referrer: str | None = Field(default=None, alias="referrer")
    transition_type: TransitionType | None = Field(default=None, alias="transitionType")
    frame_id: FrameId | None = Field(default=None, alias="frameId")
    referrer_policy: ReferrerPolicy | None = Field(default=None, alias="referrerPolicy")


class NavigateResult(BaseModel):
    frame_id: FrameId = Field(alias="frameId")
    loader_id: Network.LoaderId | None = Field(default=None, alias="loaderId")
    error_text: str | None = Field(default=None, alias="errorText")
    is_download: bool | None = Field(default=None, alias="isDownload")


class NavigatetohistoryentryParams(BaseModel):
    """Navigates current page to the given history entry."""

    entry_id: int = Field(alias="entryId")


class PrinttopdfParams(BaseModel):
    """Print page as PDF."""

    landscape: bool | None = Field(default=None, alias="landscape")
    display_header_footer: bool | None = Field(
        default=None, alias="displayHeaderFooter"
    )
    print_background: bool | None = Field(default=None, alias="printBackground")
    scale: float | None = Field(default=None, alias="scale")
    paper_width: float | None = Field(default=None, alias="paperWidth")
    paper_height: float | None = Field(default=None, alias="paperHeight")
    margin_top: float | None = Field(default=None, alias="marginTop")
    margin_bottom: float | None = Field(default=None, alias="marginBottom")
    margin_left: float | None = Field(default=None, alias="marginLeft")
    margin_right: float | None = Field(default=None, alias="marginRight")
    page_ranges: str | None = Field(default=None, alias="pageRanges")
    header_template: str | None = Field(default=None, alias="headerTemplate")
    footer_template: str | None = Field(default=None, alias="footerTemplate")
    prefer_c_s_s_page_size: bool | None = Field(default=None, alias="preferCSSPageSize")
    transfer_mode: Literal["ReturnAsBase64", "ReturnAsStream"] | None = Field(
        default=None, alias="transferMode"
    )
    generate_tagged_p_d_f: bool | None = Field(default=None, alias="generateTaggedPDF")
    generate_document_outline: bool | None = Field(
        default=None, alias="generateDocumentOutline"
    )


class PrinttopdfResult(BaseModel):
    data: str = Field(alias="data")
    stream: IO.StreamHandle | None = Field(default=None, alias="stream")


class ReloadParams(BaseModel):
    """Reloads given page optionally ignoring the cache."""

    ignore_cache: bool | None = Field(default=None, alias="ignoreCache")
    script_to_evaluate_on_load: str | None = Field(
        default=None, alias="scriptToEvaluateOnLoad"
    )
    loader_id: Network.LoaderId | None = Field(default=None, alias="loaderId")


class RemovescripttoevaluateonloadParams(BaseModel):
    """Deprecated, please use removeScriptToEvaluateOnNewDocument instead."""

    identifier: ScriptIdentifier = Field(alias="identifier")


class RemovescripttoevaluateonnewdocumentParams(BaseModel):
    """Removes given script from the list."""

    identifier: ScriptIdentifier = Field(alias="identifier")


class ScreencastframeackParams(BaseModel):
    """Acknowledges that a screencast frame has been received by the frontend."""

    session_id: int = Field(alias="sessionId")


class SearchinresourceParams(BaseModel):
    """Searches for given string in resource content."""

    frame_id: FrameId = Field(alias="frameId")
    url: str = Field(alias="url")
    query: str = Field(alias="query")
    case_sensitive: bool | None = Field(default=None, alias="caseSensitive")
    is_regex: bool | None = Field(default=None, alias="isRegex")


class SearchinresourceResult(BaseModel):
    result: list[Debugger.SearchMatch] = Field(alias="result")


class SetadblockingenabledParams(BaseModel):
    """Enable Chrome's experimental ad filter on all sites."""

    enabled: bool = Field(alias="enabled")


class SetbypasscspParams(BaseModel):
    """Enable page Content Security Policy by-passing."""

    enabled: bool = Field(alias="enabled")


class GetpermissionspolicystateParams(BaseModel):
    """Get Permissions Policy state on given frame."""

    frame_id: FrameId = Field(alias="frameId")


class GetpermissionspolicystateResult(BaseModel):
    states: list[PermissionsPolicyFeatureState] = Field(alias="states")


class GetorigintrialsParams(BaseModel):
    """Get Origin Trials on given frame."""

    frame_id: FrameId = Field(alias="frameId")


class GetorigintrialsResult(BaseModel):
    origin_trials: list[OriginTrial] = Field(alias="originTrials")


class SetdevicemetricsoverrideParams(BaseModel):
    """Overrides the values of device screen dimensions (window.screen.width, window.screen.height,
    window.innerWidth, window.innerHeight, and "device-width"/"device-height"-related CSS media
    query results)."""

    width: int = Field(alias="width")
    height: int = Field(alias="height")
    device_scale_factor: float = Field(alias="deviceScaleFactor")
    mobile: bool = Field(alias="mobile")
    scale: float | None = Field(default=None, alias="scale")
    screen_width: int | None = Field(default=None, alias="screenWidth")
    screen_height: int | None = Field(default=None, alias="screenHeight")
    position_x: int | None = Field(default=None, alias="positionX")
    position_y: int | None = Field(default=None, alias="positionY")
    dont_set_visible_size: bool | None = Field(default=None, alias="dontSetVisibleSize")
    screen_orientation: Emulation.ScreenOrientation | None = Field(
        default=None, alias="screenOrientation"
    )
    viewport: Viewport | None = Field(default=None, alias="viewport")


class SetdeviceorientationoverrideParams(BaseModel):
    """Overrides the Device Orientation."""

    alpha: float = Field(alias="alpha")
    beta: float = Field(alias="beta")
    gamma: float = Field(alias="gamma")


class SetfontfamiliesParams(BaseModel):
    """Set generic font families."""

    font_families: FontFamilies = Field(alias="fontFamilies")
    for_scripts: list[ScriptFontFamilies] | None = Field(
        default=None, alias="forScripts"
    )


class SetfontsizesParams(BaseModel):
    """Set default font sizes."""

    font_sizes: FontSizes = Field(alias="fontSizes")


class SetdocumentcontentParams(BaseModel):
    """Sets given markup as the document's HTML."""

    frame_id: FrameId = Field(alias="frameId")
    html: str = Field(alias="html")


class SetdownloadbehaviorParams(BaseModel):
    """Set the behavior when downloading a file."""

    behavior: Literal["deny", "allow", "default"] = Field(alias="behavior")
    download_path: str | None = Field(default=None, alias="downloadPath")


class SetgeolocationoverrideParams(BaseModel):
    """Overrides the Geolocation Position or Error. Omitting any of the parameters emulates position
    unavailable."""

    latitude: float | None = Field(default=None, alias="latitude")
    longitude: float | None = Field(default=None, alias="longitude")
    accuracy: float | None = Field(default=None, alias="accuracy")


class SetlifecycleeventsenabledParams(BaseModel):
    """Controls whether page will emit lifecycle events."""

    enabled: bool = Field(alias="enabled")


class SettouchemulationenabledParams(BaseModel):
    """Toggles mouse event-based touch event emulation."""

    enabled: bool = Field(alias="enabled")
    configuration: Literal["mobile", "desktop"] | None = Field(
        default=None, alias="configuration"
    )


class StartscreencastParams(BaseModel):
    """Starts sending each frame using the `screencastFrame` event."""

    format: Literal["jpeg", "png"] | None = Field(default=None, alias="format")
    quality: int | None = Field(default=None, alias="quality")
    max_width: int | None = Field(default=None, alias="maxWidth")
    max_height: int | None = Field(default=None, alias="maxHeight")
    every_nth_frame: int | None = Field(default=None, alias="everyNthFrame")


class SetweblifecyclestateParams(BaseModel):
    """Tries to update the web lifecycle state of the page.
    It will transition the page to the given state according to:
    https://github.com/WICG/web-lifecycle/"""

    state: Literal["frozen", "active"] = Field(alias="state")


class ProducecompilationcacheParams(BaseModel):
    """Requests backend to produce compilation cache for the specified scripts.
    `scripts` are appended to the list of scripts for which the cache
    would be produced. The list may be reset during page navigation.
    When script with a matching URL is encountered, the cache is optionally
    produced upon backend discretion, based on internal heuristics.
    See also: `Page.compilationCacheProduced`."""

    scripts: list[CompilationCacheParams] = Field(alias="scripts")


class AddcompilationcacheParams(BaseModel):
    """Seeds compilation cache for given url. Compilation cache does not survive
    cross-process navigation."""

    url: str = Field(alias="url")
    data: str = Field(alias="data")


class SetspctransactionmodeParams(BaseModel):
    """Sets the Secure Payment Confirmation transaction mode.
    https://w3c.github.io/secure-payment-confirmation/#sctn-automation-set-spc-transaction-mode"""

    mode: Literal[
        "none", "autoAccept", "autoChooseToAuthAnotherWay", "autoReject", "autoOptOut"
    ] = Field(alias="mode")


class SetrphregistrationmodeParams(BaseModel):
    """Extensions for Custom Handlers API:
    https://html.spec.whatwg.org/multipage/system-state.html#rph-automation"""

    mode: Literal["none", "autoAccept", "autoReject"] = Field(alias="mode")


class GeneratetestreportParams(BaseModel):
    """Generates a report for testing."""

    message: str = Field(alias="message")
    group: str | None = Field(default=None, alias="group")


class SetinterceptfilechooserdialogParams(BaseModel):
    """Intercept file chooser requests and transfer control to protocol clients.
    When file chooser interception is enabled, native file chooser dialog is not shown.
    Instead, a protocol event `Page.fileChooserOpened` is emitted."""

    enabled: bool = Field(alias="enabled")
    cancel: bool | None = Field(default=None, alias="cancel")


class SetprerenderingallowedParams(BaseModel):
    """Enable/disable prerendering manually.

    This command is a short-term solution for https://crbug.com/1440085.
    See https://docs.google.com/document/d/12HVmFxYj5Jc-eJr5OmWsa2bqTJsbgGLKI6ZIyx0_wpA
    for more details.

    TODO(https://crbug.com/1440085): Remove this once Puppeteer supports tab targets."""

    is_allowed: bool = Field(alias="isAllowed")


class GetannotatedpagecontentParams(BaseModel):
    """Get the annotated page content for the main frame.
    This is an experimental command that is subject to change."""

    include_actionable_information: bool | None = Field(
        default=None, alias="includeActionableInformation"
    )


class GetannotatedpagecontentResult(BaseModel):
    content: str = Field(alias="content")


# Client


class PageClient:
    """Actions and events related to the inspected page belong to the page domain."""

    def __init__(self, cdp_client: Any) -> None:
        self._cdp = cdp_client

    async def add_script_to_evaluate_on_load(
        self, script_source: str
    ) -> AddscripttoevaluateonloadResult:
        """Deprecated, please use addScriptToEvaluateOnNewDocument instead."""
        params = AddscripttoevaluateonloadParams(
            script_source=script_source,
        )
        result = await self._cdp.call(
            "Page.addScriptToEvaluateOnLoad",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return AddscripttoevaluateonloadResult(**result)

    async def add_script_to_evaluate_on_new_document(
        self,
        source: str,
        world_name: str | None = None,
        include_command_line_a_p_i: bool | None = None,
        run_immediately: bool | None = None,
    ) -> AddscripttoevaluateonnewdocumentResult:
        """Evaluates given script in every frame upon creation (before loading frame's scripts)."""
        params = AddscripttoevaluateonnewdocumentParams(
            source=source,
            world_name=world_name,
            include_command_line_a_p_i=include_command_line_a_p_i,
            run_immediately=run_immediately,
        )
        result = await self._cdp.call(
            "Page.addScriptToEvaluateOnNewDocument",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return AddscripttoevaluateonnewdocumentResult(**result)

    async def bring_to_front(self) -> None:
        """Brings page to front (activates tab)."""
        result = await self._cdp.call("Page.bringToFront", {})
        return None

    async def capture_screenshot(
        self,
        format: Literal["jpeg", "png", "webp"] | None = None,
        quality: int | None = None,
        clip: Viewport | None = None,
        from_surface: bool | None = None,
        capture_beyond_viewport: bool | None = None,
        optimize_for_speed: bool | None = None,
    ) -> CapturescreenshotResult:
        """Capture page screenshot."""
        params = CapturescreenshotParams(
            format=format,
            quality=quality,
            clip=clip,
            from_surface=from_surface,
            capture_beyond_viewport=capture_beyond_viewport,
            optimize_for_speed=optimize_for_speed,
        )
        result = await self._cdp.call(
            "Page.captureScreenshot",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return CapturescreenshotResult(**result)

    async def capture_snapshot(
        self, format: Literal["mhtml"] | None = None
    ) -> CapturesnapshotResult:
        """Returns a snapshot of the page as a string. For MHTML format, the serialization includes
        iframes, shadow DOM, external resources, and element-inline styles."""
        params = CapturesnapshotParams(
            format=format,
        )
        result = await self._cdp.call(
            "Page.captureSnapshot", params.model_dump(by_alias=True, exclude_none=True)
        )
        return CapturesnapshotResult(**result)

    async def clear_device_metrics_override(self) -> None:
        """Clears the overridden device metrics."""
        result = await self._cdp.call("Page.clearDeviceMetricsOverride", {})
        return None

    async def clear_device_orientation_override(self) -> None:
        """Clears the overridden Device Orientation."""
        result = await self._cdp.call("Page.clearDeviceOrientationOverride", {})
        return None

    async def clear_geolocation_override(self) -> None:
        """Clears the overridden Geolocation Position and Error."""
        result = await self._cdp.call("Page.clearGeolocationOverride", {})
        return None

    async def create_isolated_world(
        self,
        frame_id: FrameId,
        world_name: str | None = None,
        grant_univeral_access: bool | None = None,
    ) -> CreateisolatedworldResult:
        """Creates an isolated world for the given frame."""
        params = CreateisolatedworldParams(
            frame_id=frame_id,
            world_name=world_name,
            grant_univeral_access=grant_univeral_access,
        )
        result = await self._cdp.call(
            "Page.createIsolatedWorld",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return CreateisolatedworldResult(**result)

    async def delete_cookie(self, cookie_name: str, url: str) -> None:
        """Deletes browser cookie with given name, domain and path."""
        params = DeletecookieParams(
            cookie_name=cookie_name,
            url=url,
        )
        result = await self._cdp.call(
            "Page.deleteCookie", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def disable(self) -> None:
        """Disables page domain notifications."""
        result = await self._cdp.call("Page.disable", {})
        return None

    async def enable(
        self, enable_file_chooser_opened_event: bool | None = None
    ) -> None:
        """Enables page domain notifications."""
        params = EnableParams(
            enable_file_chooser_opened_event=enable_file_chooser_opened_event,
        )
        result = await self._cdp.call(
            "Page.enable", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def get_app_manifest(
        self, manifest_id: str | None = None
    ) -> GetappmanifestResult:
        """Gets the processed manifest for this current document.
        This API always waits for the manifest to be loaded.
        If manifestId is provided, and it does not match the manifest of the
          current document, this API errors out.
        If there is not a loaded page, this API errors out immediately."""
        params = GetappmanifestParams(
            manifest_id=manifest_id,
        )
        result = await self._cdp.call(
            "Page.getAppManifest", params.model_dump(by_alias=True, exclude_none=True)
        )
        return GetappmanifestResult(**result)

    async def get_installability_errors(self) -> GetinstallabilityerrorsResult:
        result = await self._cdp.call("Page.getInstallabilityErrors", {})
        return GetinstallabilityerrorsResult(**result)

    async def get_manifest_icons(self) -> GetmanifesticonsResult:
        """Deprecated because it's not guaranteed that the returned icon is in fact the one used for PWA installation."""
        result = await self._cdp.call("Page.getManifestIcons", {})
        return GetmanifesticonsResult(**result)

    async def get_app_id(self) -> GetappidResult:
        """Returns the unique (PWA) app id.
        Only returns values if the feature flag 'WebAppEnableManifestId' is enabled"""
        result = await self._cdp.call("Page.getAppId", {})
        return GetappidResult(**result)

    async def get_ad_script_ancestry(
        self, frame_id: FrameId
    ) -> GetadscriptancestryResult:
        params = GetadscriptancestryParams(
            frame_id=frame_id,
        )
        result = await self._cdp.call(
            "Page.getAdScriptAncestry",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return GetadscriptancestryResult(**result)

    async def get_frame_tree(self) -> GetframetreeResult:
        """Returns present frame tree structure."""
        result = await self._cdp.call("Page.getFrameTree", {})
        return GetframetreeResult(**result)

    async def get_layout_metrics(self) -> GetlayoutmetricsResult:
        """Returns metrics relating to the layouting of the page, such as viewport bounds/scale."""
        result = await self._cdp.call("Page.getLayoutMetrics", {})
        return GetlayoutmetricsResult(**result)

    async def get_navigation_history(self) -> GetnavigationhistoryResult:
        """Returns navigation history for the current page."""
        result = await self._cdp.call("Page.getNavigationHistory", {})
        return GetnavigationhistoryResult(**result)

    async def reset_navigation_history(self) -> None:
        """Resets navigation history for the current page."""
        result = await self._cdp.call("Page.resetNavigationHistory", {})
        return None

    async def get_resource_content(
        self, frame_id: FrameId, url: str
    ) -> GetresourcecontentResult:
        """Returns content of the given resource."""
        params = GetresourcecontentParams(
            frame_id=frame_id,
            url=url,
        )
        result = await self._cdp.call(
            "Page.getResourceContent",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return GetresourcecontentResult(**result)

    async def get_resource_tree(self) -> GetresourcetreeResult:
        """Returns present frame / resource tree structure."""
        result = await self._cdp.call("Page.getResourceTree", {})
        return GetresourcetreeResult(**result)

    async def handle_java_script_dialog(
        self, accept: bool, prompt_text: str | None = None
    ) -> None:
        """Accepts or dismisses a JavaScript initiated dialog (alert, confirm, prompt, or onbeforeunload)."""
        params = HandlejavascriptdialogParams(
            accept=accept,
            prompt_text=prompt_text,
        )
        result = await self._cdp.call(
            "Page.handleJavaScriptDialog",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def navigate(
        self,
        url: str,
        referrer: str | None = None,
        transition_type: TransitionType | None = None,
        frame_id: FrameId | None = None,
        referrer_policy: ReferrerPolicy | None = None,
    ) -> NavigateResult:
        """Navigates current page to the given URL."""
        params = NavigateParams(
            url=url,
            referrer=referrer,
            transition_type=transition_type,
            frame_id=frame_id,
            referrer_policy=referrer_policy,
        )
        result = await self._cdp.call(
            "Page.navigate", params.model_dump(by_alias=True, exclude_none=True)
        )
        return NavigateResult(**result)

    async def navigate_to_history_entry(self, entry_id: int) -> None:
        """Navigates current page to the given history entry."""
        params = NavigatetohistoryentryParams(
            entry_id=entry_id,
        )
        result = await self._cdp.call(
            "Page.navigateToHistoryEntry",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def print_to_p_d_f(
        self,
        landscape: bool | None = None,
        display_header_footer: bool | None = None,
        print_background: bool | None = None,
        scale: float | None = None,
        paper_width: float | None = None,
        paper_height: float | None = None,
        margin_top: float | None = None,
        margin_bottom: float | None = None,
        margin_left: float | None = None,
        margin_right: float | None = None,
        page_ranges: str | None = None,
        header_template: str | None = None,
        footer_template: str | None = None,
        prefer_c_s_s_page_size: bool | None = None,
        transfer_mode: Literal["ReturnAsBase64", "ReturnAsStream"] | None = None,
        generate_tagged_p_d_f: bool | None = None,
        generate_document_outline: bool | None = None,
    ) -> PrinttopdfResult:
        """Print page as PDF."""
        params = PrinttopdfParams(
            landscape=landscape,
            display_header_footer=display_header_footer,
            print_background=print_background,
            scale=scale,
            paper_width=paper_width,
            paper_height=paper_height,
            margin_top=margin_top,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            page_ranges=page_ranges,
            header_template=header_template,
            footer_template=footer_template,
            prefer_c_s_s_page_size=prefer_c_s_s_page_size,
            transfer_mode=transfer_mode,
            generate_tagged_p_d_f=generate_tagged_p_d_f,
            generate_document_outline=generate_document_outline,
        )
        result = await self._cdp.call(
            "Page.printToPDF", params.model_dump(by_alias=True, exclude_none=True)
        )
        return PrinttopdfResult(**result)

    async def reload(
        self,
        ignore_cache: bool | None = None,
        script_to_evaluate_on_load: str | None = None,
        loader_id: Network.LoaderId | None = None,
    ) -> None:
        """Reloads given page optionally ignoring the cache."""
        params = ReloadParams(
            ignore_cache=ignore_cache,
            script_to_evaluate_on_load=script_to_evaluate_on_load,
            loader_id=loader_id,
        )
        result = await self._cdp.call(
            "Page.reload", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def remove_script_to_evaluate_on_load(
        self, identifier: ScriptIdentifier
    ) -> None:
        """Deprecated, please use removeScriptToEvaluateOnNewDocument instead."""
        params = RemovescripttoevaluateonloadParams(
            identifier=identifier,
        )
        result = await self._cdp.call(
            "Page.removeScriptToEvaluateOnLoad",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def remove_script_to_evaluate_on_new_document(
        self, identifier: ScriptIdentifier
    ) -> None:
        """Removes given script from the list."""
        params = RemovescripttoevaluateonnewdocumentParams(
            identifier=identifier,
        )
        result = await self._cdp.call(
            "Page.removeScriptToEvaluateOnNewDocument",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def screencast_frame_ack(self, session_id: int) -> None:
        """Acknowledges that a screencast frame has been received by the frontend."""
        params = ScreencastframeackParams(
            session_id=session_id,
        )
        result = await self._cdp.call(
            "Page.screencastFrameAck",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def search_in_resource(
        self,
        frame_id: FrameId,
        url: str,
        query: str,
        case_sensitive: bool | None = None,
        is_regex: bool | None = None,
    ) -> SearchinresourceResult:
        """Searches for given string in resource content."""
        params = SearchinresourceParams(
            frame_id=frame_id,
            url=url,
            query=query,
            case_sensitive=case_sensitive,
            is_regex=is_regex,
        )
        result = await self._cdp.call(
            "Page.searchInResource", params.model_dump(by_alias=True, exclude_none=True)
        )
        return SearchinresourceResult(**result)

    async def set_ad_blocking_enabled(self, enabled: bool) -> None:
        """Enable Chrome's experimental ad filter on all sites."""
        params = SetadblockingenabledParams(
            enabled=enabled,
        )
        result = await self._cdp.call(
            "Page.setAdBlockingEnabled",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def set_bypass_c_s_p(self, enabled: bool) -> None:
        """Enable page Content Security Policy by-passing."""
        params = SetbypasscspParams(
            enabled=enabled,
        )
        result = await self._cdp.call(
            "Page.setBypassCSP", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def get_permissions_policy_state(
        self, frame_id: FrameId
    ) -> GetpermissionspolicystateResult:
        """Get Permissions Policy state on given frame."""
        params = GetpermissionspolicystateParams(
            frame_id=frame_id,
        )
        result = await self._cdp.call(
            "Page.getPermissionsPolicyState",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return GetpermissionspolicystateResult(**result)

    async def get_origin_trials(self, frame_id: FrameId) -> GetorigintrialsResult:
        """Get Origin Trials on given frame."""
        params = GetorigintrialsParams(
            frame_id=frame_id,
        )
        result = await self._cdp.call(
            "Page.getOriginTrials", params.model_dump(by_alias=True, exclude_none=True)
        )
        return GetorigintrialsResult(**result)

    async def set_device_metrics_override(
        self,
        width: int,
        height: int,
        device_scale_factor: float,
        mobile: bool,
        scale: float | None = None,
        screen_width: int | None = None,
        screen_height: int | None = None,
        position_x: int | None = None,
        position_y: int | None = None,
        dont_set_visible_size: bool | None = None,
        screen_orientation: Emulation.ScreenOrientation | None = None,
        viewport: Viewport | None = None,
    ) -> None:
        """Overrides the values of device screen dimensions (window.screen.width, window.screen.height,
        window.innerWidth, window.innerHeight, and "device-width"/"device-height"-related CSS media
        query results)."""
        params = SetdevicemetricsoverrideParams(
            width=width,
            height=height,
            device_scale_factor=device_scale_factor,
            mobile=mobile,
            scale=scale,
            screen_width=screen_width,
            screen_height=screen_height,
            position_x=position_x,
            position_y=position_y,
            dont_set_visible_size=dont_set_visible_size,
            screen_orientation=screen_orientation,
            viewport=viewport,
        )
        result = await self._cdp.call(
            "Page.setDeviceMetricsOverride",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def set_device_orientation_override(
        self, alpha: float, beta: float, gamma: float
    ) -> None:
        """Overrides the Device Orientation."""
        params = SetdeviceorientationoverrideParams(
            alpha=alpha,
            beta=beta,
            gamma=gamma,
        )
        result = await self._cdp.call(
            "Page.setDeviceOrientationOverride",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def set_font_families(
        self,
        font_families: FontFamilies,
        for_scripts: list[ScriptFontFamilies] | None = None,
    ) -> None:
        """Set generic font families."""
        params = SetfontfamiliesParams(
            font_families=font_families,
            for_scripts=for_scripts,
        )
        result = await self._cdp.call(
            "Page.setFontFamilies", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def set_font_sizes(self, font_sizes: FontSizes) -> None:
        """Set default font sizes."""
        params = SetfontsizesParams(
            font_sizes=font_sizes,
        )
        result = await self._cdp.call(
            "Page.setFontSizes", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def set_document_content(self, frame_id: FrameId, html: str) -> None:
        """Sets given markup as the document's HTML."""
        params = SetdocumentcontentParams(
            frame_id=frame_id,
            html=html,
        )
        result = await self._cdp.call(
            "Page.setDocumentContent",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def set_download_behavior(
        self,
        behavior: Literal["deny", "allow", "default"],
        download_path: str | None = None,
    ) -> None:
        """Set the behavior when downloading a file."""
        params = SetdownloadbehaviorParams(
            behavior=behavior,
            download_path=download_path,
        )
        result = await self._cdp.call(
            "Page.setDownloadBehavior",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def set_geolocation_override(
        self,
        latitude: float | None = None,
        longitude: float | None = None,
        accuracy: float | None = None,
    ) -> None:
        """Overrides the Geolocation Position or Error. Omitting any of the parameters emulates position
        unavailable."""
        params = SetgeolocationoverrideParams(
            latitude=latitude,
            longitude=longitude,
            accuracy=accuracy,
        )
        result = await self._cdp.call(
            "Page.setGeolocationOverride",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def set_lifecycle_events_enabled(self, enabled: bool) -> None:
        """Controls whether page will emit lifecycle events."""
        params = SetlifecycleeventsenabledParams(
            enabled=enabled,
        )
        result = await self._cdp.call(
            "Page.setLifecycleEventsEnabled",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def set_touch_emulation_enabled(
        self, enabled: bool, configuration: Literal["mobile", "desktop"] | None = None
    ) -> None:
        """Toggles mouse event-based touch event emulation."""
        params = SettouchemulationenabledParams(
            enabled=enabled,
            configuration=configuration,
        )
        result = await self._cdp.call(
            "Page.setTouchEmulationEnabled",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def start_screencast(
        self,
        format: Literal["jpeg", "png"] | None = None,
        quality: int | None = None,
        max_width: int | None = None,
        max_height: int | None = None,
        every_nth_frame: int | None = None,
    ) -> None:
        """Starts sending each frame using the `screencastFrame` event."""
        params = StartscreencastParams(
            format=format,
            quality=quality,
            max_width=max_width,
            max_height=max_height,
            every_nth_frame=every_nth_frame,
        )
        result = await self._cdp.call(
            "Page.startScreencast", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def stop_loading(self) -> None:
        """Force the page stop all navigations and pending resource fetches."""
        result = await self._cdp.call("Page.stopLoading", {})
        return None

    async def crash(self) -> None:
        """Crashes renderer on the IO thread, generates minidumps."""
        result = await self._cdp.call("Page.crash", {})
        return None

    async def close(self) -> None:
        """Tries to close page, running its beforeunload hooks, if any."""
        result = await self._cdp.call("Page.close", {})
        return None

    async def set_web_lifecycle_state(self, state: Literal["frozen", "active"]) -> None:
        """Tries to update the web lifecycle state of the page.
        It will transition the page to the given state according to:
        https://github.com/WICG/web-lifecycle/"""
        params = SetweblifecyclestateParams(
            state=state,
        )
        result = await self._cdp.call(
            "Page.setWebLifecycleState",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def stop_screencast(self) -> None:
        """Stops sending each frame in the `screencastFrame`."""
        result = await self._cdp.call("Page.stopScreencast", {})
        return None

    async def produce_compilation_cache(
        self, scripts: list[CompilationCacheParams]
    ) -> None:
        """Requests backend to produce compilation cache for the specified scripts.
        `scripts` are appended to the list of scripts for which the cache
        would be produced. The list may be reset during page navigation.
        When script with a matching URL is encountered, the cache is optionally
        produced upon backend discretion, based on internal heuristics.
        See also: `Page.compilationCacheProduced`."""
        params = ProducecompilationcacheParams(
            scripts=scripts,
        )
        result = await self._cdp.call(
            "Page.produceCompilationCache",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def add_compilation_cache(self, url: str, data: str) -> None:
        """Seeds compilation cache for given url. Compilation cache does not survive
        cross-process navigation."""
        params = AddcompilationcacheParams(
            url=url,
            data=data,
        )
        result = await self._cdp.call(
            "Page.addCompilationCache",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def clear_compilation_cache(self) -> None:
        """Clears seeded compilation cache."""
        result = await self._cdp.call("Page.clearCompilationCache", {})
        return None

    async def set_s_p_c_transaction_mode(
        self,
        mode: Literal[
            "none",
            "autoAccept",
            "autoChooseToAuthAnotherWay",
            "autoReject",
            "autoOptOut",
        ],
    ) -> None:
        """Sets the Secure Payment Confirmation transaction mode.
        https://w3c.github.io/secure-payment-confirmation/#sctn-automation-set-spc-transaction-mode"""
        params = SetspctransactionmodeParams(
            mode=mode,
        )
        result = await self._cdp.call(
            "Page.setSPCTransactionMode",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def set_r_p_h_registration_mode(
        self, mode: Literal["none", "autoAccept", "autoReject"]
    ) -> None:
        """Extensions for Custom Handlers API:
        https://html.spec.whatwg.org/multipage/system-state.html#rph-automation"""
        params = SetrphregistrationmodeParams(
            mode=mode,
        )
        result = await self._cdp.call(
            "Page.setRPHRegistrationMode",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def generate_test_report(
        self, message: str, group: str | None = None
    ) -> None:
        """Generates a report for testing."""
        params = GeneratetestreportParams(
            message=message,
            group=group,
        )
        result = await self._cdp.call(
            "Page.generateTestReport",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def wait_for_debugger(self) -> None:
        """Pauses page execution. Can be resumed using generic Runtime.runIfWaitingForDebugger."""
        result = await self._cdp.call("Page.waitForDebugger", {})
        return None

    async def set_intercept_file_chooser_dialog(
        self, enabled: bool, cancel: bool | None = None
    ) -> None:
        """Intercept file chooser requests and transfer control to protocol clients.
        When file chooser interception is enabled, native file chooser dialog is not shown.
        Instead, a protocol event `Page.fileChooserOpened` is emitted."""
        params = SetinterceptfilechooserdialogParams(
            enabled=enabled,
            cancel=cancel,
        )
        result = await self._cdp.call(
            "Page.setInterceptFileChooserDialog",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def set_prerendering_allowed(self, is_allowed: bool) -> None:
        """Enable/disable prerendering manually.

        This command is a short-term solution for https://crbug.com/1440085.
        See https://docs.google.com/document/d/12HVmFxYj5Jc-eJr5OmWsa2bqTJsbgGLKI6ZIyx0_wpA
        for more details.

        TODO(https://crbug.com/1440085): Remove this once Puppeteer supports tab targets."""
        params = SetprerenderingallowedParams(
            is_allowed=is_allowed,
        )
        result = await self._cdp.call(
            "Page.setPrerenderingAllowed",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def get_annotated_page_content(
        self, include_actionable_information: bool | None = None
    ) -> GetannotatedpagecontentResult:
        """Get the annotated page content for the main frame.
        This is an experimental command that is subject to change."""
        params = GetannotatedpagecontentParams(
            include_actionable_information=include_actionable_information,
        )
        result = await self._cdp.call(
            "Page.getAnnotatedPageContent",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return GetannotatedpagecontentResult(**result)
