"""Generated from CDP specification"""

from pydantic import BaseModel, Field
from typing import Literal, Any

from pydantic_cpd.domains import dom
from pydantic_cpd.domains import page
from pydantic_cpd.domains import runtime

# Alias for cross-domain type references
DOM = dom
Page = page
Runtime = runtime

# Domain Types

NodeId = int
BackendNodeId = int
StyleSheetId = str


class BackendNode(BaseModel):
    """Backend node with a friendly name."""

    node_type: int
    node_name: str
    backend_node_id: BackendNodeId


PseudoType = Literal[
    "first-line",
    "first-letter",
    "checkmark",
    "before",
    "after",
    "picker-icon",
    "interest-hint",
    "marker",
    "backdrop",
    "column",
    "selection",
    "search-text",
    "target-text",
    "spelling-error",
    "grammar-error",
    "highlight",
    "first-line-inherited",
    "scroll-marker",
    "scroll-marker-group",
    "scroll-button",
    "scrollbar",
    "scrollbar-thumb",
    "scrollbar-button",
    "scrollbar-track",
    "scrollbar-track-piece",
    "scrollbar-corner",
    "resizer",
    "input-list-button",
    "view-transition",
    "view-transition-group",
    "view-transition-image-pair",
    "view-transition-group-children",
    "view-transition-old",
    "view-transition-new",
    "placeholder",
    "file-selector-button",
    "details-content",
    "picker",
    "permission-icon",
    "overscroll-area-parent",
]
ShadowRootType = Literal["user-agent", "open", "closed"]
CompatibilityMode = Literal["QuirksMode", "LimitedQuirksMode", "NoQuirksMode"]
PhysicalAxes = Literal["Horizontal", "Vertical", "Both"]
LogicalAxes = Literal["Inline", "Block", "Both"]
ScrollOrientation = Literal["horizontal", "vertical"]


class Node(BaseModel):
    """DOM interaction is implemented in terms of mirror objects that represent the actual DOM nodes.
    DOMNode is a base node mirror type."""

    node_id: NodeId
    parent_id: NodeId | None = None
    backend_node_id: BackendNodeId
    node_type: int
    node_name: str
    local_name: str
    node_value: str
    child_node_count: int | None = None
    children: list[Node] | None = None
    attributes: list[str] | None = None
    document_u_r_l: str | None = None
    base_u_r_l: str | None = None
    public_id: str | None = None
    system_id: str | None = None
    internal_subset: str | None = None
    xml_version: str | None = None
    name: str | None = None
    value: str | None = None
    pseudo_type: PseudoType | None = None
    pseudo_identifier: str | None = None
    shadow_root_type: ShadowRootType | None = None
    frame_id: Page.FrameId | None = None
    content_document: Node | None = None
    shadow_roots: list[Node] | None = None
    template_content: Node | None = None
    pseudo_elements: list[Node] | None = None
    imported_document: Node | None = None
    distributed_nodes: list[BackendNode] | None = None
    is_s_v_g: bool | None = None
    compatibility_mode: CompatibilityMode | None = None
    assigned_slot: BackendNode | None = None
    is_scrollable: bool | None = None
    affected_by_starting_styles: bool | None = None
    adopted_style_sheets: list[StyleSheetId] | None = None


class DetachedElementInfo(BaseModel):
    """A structure to hold the top-level node of a detached tree and an array of its retained descendants."""

    tree_node: Node
    retained_node_ids: list[NodeId]


class RGBA(BaseModel):
    """A structure holding an RGBA color."""

    r: int
    g: int
    b: int
    a: float | None = None


Quad = list[Any]


class BoxModel(BaseModel):
    """Box model."""

    content: Quad
    padding: Quad
    border: Quad
    margin: Quad
    width: int
    height: int
    shape_outside: ShapeOutsideInfo | None = None


class ShapeOutsideInfo(BaseModel):
    """CSS Shape Outside details."""

    bounds: Quad
    shape: list[Any]
    margin_shape: list[Any]


class Rect(BaseModel):
    """Rectangle."""

    x: float
    y: float
    width: float
    height: float


class CSSComputedStyleProperty(BaseModel):
    name: str
    value: str


# Command Parameters and Results


class CollectclassnamesfromsubtreeParams(BaseModel):
    """Collects class names for the node with given id and all of it's child nodes."""

    node_id: NodeId = Field(alias="nodeId")


class CollectclassnamesfromsubtreeResult(BaseModel):
    class_names: list[str] = Field(alias="classNames")


class CopytoParams(BaseModel):
    """Creates a deep copy of the specified node and places it into the target container before the
    given anchor."""

    node_id: NodeId = Field(alias="nodeId")
    target_node_id: NodeId = Field(alias="targetNodeId")
    insert_before_node_id: NodeId | None = Field(
        default=None, alias="insertBeforeNodeId"
    )


class CopytoResult(BaseModel):
    node_id: NodeId = Field(alias="nodeId")


class DescribenodeParams(BaseModel):
    """Describes node given its id, does not require domain to be enabled. Does not start tracking any
    objects, can be used for automation."""

    node_id: NodeId | None = Field(default=None, alias="nodeId")
    backend_node_id: BackendNodeId | None = Field(default=None, alias="backendNodeId")
    object_id: Runtime.RemoteObjectId | None = Field(default=None, alias="objectId")
    depth: int | None = Field(default=None, alias="depth")
    pierce: bool | None = Field(default=None, alias="pierce")


class DescribenodeResult(BaseModel):
    node: Node = Field(alias="node")


class ScrollintoviewifneededParams(BaseModel):
    """Scrolls the specified rect of the given node into view if not already visible.
    Note: exactly one between nodeId, backendNodeId and objectId should be passed
    to identify the node."""

    node_id: NodeId | None = Field(default=None, alias="nodeId")
    backend_node_id: BackendNodeId | None = Field(default=None, alias="backendNodeId")
    object_id: Runtime.RemoteObjectId | None = Field(default=None, alias="objectId")
    rect: Rect | None = Field(default=None, alias="rect")


class DiscardsearchresultsParams(BaseModel):
    """Discards search results from the session with the given id. `getSearchResults` should no longer
    be called for that search."""

    search_id: str = Field(alias="searchId")


class EnableParams(BaseModel):
    """Enables DOM agent for the given page."""

    include_whitespace: Literal["none", "all"] | None = Field(
        default=None, alias="includeWhitespace"
    )


class FocusParams(BaseModel):
    """Focuses the given element."""

    node_id: NodeId | None = Field(default=None, alias="nodeId")
    backend_node_id: BackendNodeId | None = Field(default=None, alias="backendNodeId")
    object_id: Runtime.RemoteObjectId | None = Field(default=None, alias="objectId")


class GetattributesParams(BaseModel):
    """Returns attributes for the specified node."""

    node_id: NodeId = Field(alias="nodeId")


class GetattributesResult(BaseModel):
    attributes: list[str] = Field(alias="attributes")


class GetboxmodelParams(BaseModel):
    """Returns boxes for the given node."""

    node_id: NodeId | None = Field(default=None, alias="nodeId")
    backend_node_id: BackendNodeId | None = Field(default=None, alias="backendNodeId")
    object_id: Runtime.RemoteObjectId | None = Field(default=None, alias="objectId")


class GetboxmodelResult(BaseModel):
    model: BoxModel = Field(alias="model")


class GetcontentquadsParams(BaseModel):
    """Returns quads that describe node position on the page. This method
    might return multiple quads for inline nodes."""

    node_id: NodeId | None = Field(default=None, alias="nodeId")
    backend_node_id: BackendNodeId | None = Field(default=None, alias="backendNodeId")
    object_id: Runtime.RemoteObjectId | None = Field(default=None, alias="objectId")


class GetcontentquadsResult(BaseModel):
    quads: list[Quad] = Field(alias="quads")


class GetdocumentParams(BaseModel):
    """Returns the root DOM node (and optionally the subtree) to the caller.
    Implicitly enables the DOM domain events for the current target."""

    depth: int | None = Field(default=None, alias="depth")
    pierce: bool | None = Field(default=None, alias="pierce")


class GetdocumentResult(BaseModel):
    root: Node = Field(alias="root")


class GetflatteneddocumentParams(BaseModel):
    """Returns the root DOM node (and optionally the subtree) to the caller.
    Deprecated, as it is not designed to work well with the rest of the DOM agent.
    Use DOMSnapshot.captureSnapshot instead."""

    depth: int | None = Field(default=None, alias="depth")
    pierce: bool | None = Field(default=None, alias="pierce")


class GetflatteneddocumentResult(BaseModel):
    nodes: list[Node] = Field(alias="nodes")


class GetnodesforsubtreebystyleParams(BaseModel):
    """Finds nodes with a given computed style in a subtree."""

    node_id: NodeId = Field(alias="nodeId")
    computed_styles: list[CSSComputedStyleProperty] = Field(alias="computedStyles")
    pierce: bool | None = Field(default=None, alias="pierce")


class GetnodesforsubtreebystyleResult(BaseModel):
    node_ids: list[NodeId] = Field(alias="nodeIds")


class GetnodeforlocationParams(BaseModel):
    """Returns node id at given location. Depending on whether DOM domain is enabled, nodeId is
    either returned or not."""

    x: int = Field(alias="x")
    y: int = Field(alias="y")
    include_user_agent_shadow_d_o_m: bool | None = Field(
        default=None, alias="includeUserAgentShadowDOM"
    )
    ignore_pointer_events_none: bool | None = Field(
        default=None, alias="ignorePointerEventsNone"
    )


class GetnodeforlocationResult(BaseModel):
    backend_node_id: BackendNodeId = Field(alias="backendNodeId")
    frame_id: Page.FrameId = Field(alias="frameId")
    node_id: NodeId | None = Field(default=None, alias="nodeId")


class GetouterhtmlParams(BaseModel):
    """Returns node's HTML markup."""

    node_id: NodeId | None = Field(default=None, alias="nodeId")
    backend_node_id: BackendNodeId | None = Field(default=None, alias="backendNodeId")
    object_id: Runtime.RemoteObjectId | None = Field(default=None, alias="objectId")
    include_shadow_d_o_m: bool | None = Field(default=None, alias="includeShadowDOM")


class GetouterhtmlResult(BaseModel):
    outer_h_t_m_l: str = Field(alias="outerHTML")


class GetrelayoutboundaryParams(BaseModel):
    """Returns the id of the nearest ancestor that is a relayout boundary."""

    node_id: NodeId = Field(alias="nodeId")


class GetrelayoutboundaryResult(BaseModel):
    node_id: NodeId = Field(alias="nodeId")


class GetsearchresultsParams(BaseModel):
    """Returns search results from given `fromIndex` to given `toIndex` from the search with the given
    identifier."""

    search_id: str = Field(alias="searchId")
    from_index: int = Field(alias="fromIndex")
    to_index: int = Field(alias="toIndex")


class GetsearchresultsResult(BaseModel):
    node_ids: list[NodeId] = Field(alias="nodeIds")


class MovetoParams(BaseModel):
    """Moves node into the new container, places it before the given anchor."""

    node_id: NodeId = Field(alias="nodeId")
    target_node_id: NodeId = Field(alias="targetNodeId")
    insert_before_node_id: NodeId | None = Field(
        default=None, alias="insertBeforeNodeId"
    )


class MovetoResult(BaseModel):
    node_id: NodeId = Field(alias="nodeId")


class PerformsearchParams(BaseModel):
    """Searches for a given string in the DOM tree. Use `getSearchResults` to access search results or
    `cancelSearch` to end this search session."""

    query: str = Field(alias="query")
    include_user_agent_shadow_d_o_m: bool | None = Field(
        default=None, alias="includeUserAgentShadowDOM"
    )


class PerformsearchResult(BaseModel):
    search_id: str = Field(alias="searchId")
    result_count: int = Field(alias="resultCount")


class PushnodebypathtofrontendParams(BaseModel):
    """Requests that the node is sent to the caller given its path. // FIXME, use XPath"""

    path: str = Field(alias="path")


class PushnodebypathtofrontendResult(BaseModel):
    node_id: NodeId = Field(alias="nodeId")


class PushnodesbybackendidstofrontendParams(BaseModel):
    """Requests that a batch of nodes is sent to the caller given their backend node ids."""

    backend_node_ids: list[BackendNodeId] = Field(alias="backendNodeIds")


class PushnodesbybackendidstofrontendResult(BaseModel):
    node_ids: list[NodeId] = Field(alias="nodeIds")


class QueryselectorParams(BaseModel):
    """Executes `querySelector` on a given node."""

    node_id: NodeId = Field(alias="nodeId")
    selector: str = Field(alias="selector")


class QueryselectorResult(BaseModel):
    node_id: NodeId = Field(alias="nodeId")


class QueryselectorallParams(BaseModel):
    """Executes `querySelectorAll` on a given node."""

    node_id: NodeId = Field(alias="nodeId")
    selector: str = Field(alias="selector")


class QueryselectorallResult(BaseModel):
    node_ids: list[NodeId] = Field(alias="nodeIds")


class GettoplayerelementsResult(BaseModel):
    node_ids: list[NodeId] = Field(alias="nodeIds")


class GetelementbyrelationParams(BaseModel):
    """Returns the NodeId of the matched element according to certain relations."""

    node_id: NodeId = Field(alias="nodeId")
    relation: Literal["PopoverTarget", "InterestTarget", "CommandFor"] = Field(
        alias="relation"
    )


class GetelementbyrelationResult(BaseModel):
    node_id: NodeId = Field(alias="nodeId")


class RemoveattributeParams(BaseModel):
    """Removes attribute with given name from an element with given id."""

    node_id: NodeId = Field(alias="nodeId")
    name: str = Field(alias="name")


class RemovenodeParams(BaseModel):
    """Removes node with given id."""

    node_id: NodeId = Field(alias="nodeId")


class RequestchildnodesParams(BaseModel):
    """Requests that children of the node with given id are returned to the caller in form of
    `setChildNodes` events where not only immediate children are retrieved, but all children down to
    the specified depth."""

    node_id: NodeId = Field(alias="nodeId")
    depth: int | None = Field(default=None, alias="depth")
    pierce: bool | None = Field(default=None, alias="pierce")


class RequestnodeParams(BaseModel):
    """Requests that the node is sent to the caller given the JavaScript node object reference. All
    nodes that form the path from the node to the root are also sent to the client as a series of
    `setChildNodes` notifications."""

    object_id: Runtime.RemoteObjectId = Field(alias="objectId")


class RequestnodeResult(BaseModel):
    node_id: NodeId = Field(alias="nodeId")


class ResolvenodeParams(BaseModel):
    """Resolves the JavaScript node object for a given NodeId or BackendNodeId."""

    node_id: NodeId | None = Field(default=None, alias="nodeId")
    backend_node_id: DOM.BackendNodeId | None = Field(
        default=None, alias="backendNodeId"
    )
    object_group: str | None = Field(default=None, alias="objectGroup")
    execution_context_id: Runtime.ExecutionContextId | None = Field(
        default=None, alias="executionContextId"
    )


class ResolvenodeResult(BaseModel):
    object: Runtime.RemoteObject = Field(alias="object")


class SetattributevalueParams(BaseModel):
    """Sets attribute for an element with given id."""

    node_id: NodeId = Field(alias="nodeId")
    name: str = Field(alias="name")
    value: str = Field(alias="value")


class SetattributesastextParams(BaseModel):
    """Sets attributes on element with given id. This method is useful when user edits some existing
    attribute value and types in several attribute name/value pairs."""

    node_id: NodeId = Field(alias="nodeId")
    text: str = Field(alias="text")
    name: str | None = Field(default=None, alias="name")


class SetfileinputfilesParams(BaseModel):
    """Sets files for the given file input element."""

    files: list[str] = Field(alias="files")
    node_id: NodeId | None = Field(default=None, alias="nodeId")
    backend_node_id: BackendNodeId | None = Field(default=None, alias="backendNodeId")
    object_id: Runtime.RemoteObjectId | None = Field(default=None, alias="objectId")


class SetnodestacktracesenabledParams(BaseModel):
    """Sets if stack traces should be captured for Nodes. See `Node.getNodeStackTraces`. Default is disabled."""

    enable: bool = Field(alias="enable")


class GetnodestacktracesParams(BaseModel):
    """Gets stack traces associated with a Node. As of now, only provides stack trace for Node creation."""

    node_id: NodeId = Field(alias="nodeId")


class GetnodestacktracesResult(BaseModel):
    creation: Runtime.StackTrace | None = Field(default=None, alias="creation")


class GetfileinfoParams(BaseModel):
    """Returns file information for the given
    File wrapper."""

    object_id: Runtime.RemoteObjectId = Field(alias="objectId")


class GetfileinfoResult(BaseModel):
    path: str = Field(alias="path")


class GetdetacheddomnodesResult(BaseModel):
    detached_nodes: list[DetachedElementInfo] = Field(alias="detachedNodes")


class SetinspectednodeParams(BaseModel):
    """Enables console to refer to the node with given id via $x (see Command Line API for more details
    $x functions)."""

    node_id: NodeId = Field(alias="nodeId")


class SetnodenameParams(BaseModel):
    """Sets node name for a node with given id."""

    node_id: NodeId = Field(alias="nodeId")
    name: str = Field(alias="name")


class SetnodenameResult(BaseModel):
    node_id: NodeId = Field(alias="nodeId")


class SetnodevalueParams(BaseModel):
    """Sets node value for a node with given id."""

    node_id: NodeId = Field(alias="nodeId")
    value: str = Field(alias="value")


class SetouterhtmlParams(BaseModel):
    """Sets node HTML markup, returns new node id."""

    node_id: NodeId = Field(alias="nodeId")
    outer_h_t_m_l: str = Field(alias="outerHTML")


class GetframeownerParams(BaseModel):
    """Returns iframe node that owns iframe with the given domain."""

    frame_id: Page.FrameId = Field(alias="frameId")


class GetframeownerResult(BaseModel):
    backend_node_id: BackendNodeId = Field(alias="backendNodeId")
    node_id: NodeId | None = Field(default=None, alias="nodeId")


class GetcontainerfornodeParams(BaseModel):
    """Returns the query container of the given node based on container query
    conditions: containerName, physical and logical axes, and whether it queries
    scroll-state or anchored elements. If no axes are provided and
    queriesScrollState is false, the style container is returned, which is the
    direct parent or the closest element with a matching container-name."""

    node_id: NodeId = Field(alias="nodeId")
    container_name: str | None = Field(default=None, alias="containerName")
    physical_axes: PhysicalAxes | None = Field(default=None, alias="physicalAxes")
    logical_axes: LogicalAxes | None = Field(default=None, alias="logicalAxes")
    queries_scroll_state: bool | None = Field(default=None, alias="queriesScrollState")
    queries_anchored: bool | None = Field(default=None, alias="queriesAnchored")


class GetcontainerfornodeResult(BaseModel):
    node_id: NodeId | None = Field(default=None, alias="nodeId")


class GetqueryingdescendantsforcontainerParams(BaseModel):
    """Returns the descendants of a container query container that have
    container queries against this container."""

    node_id: NodeId = Field(alias="nodeId")


class GetqueryingdescendantsforcontainerResult(BaseModel):
    node_ids: list[NodeId] = Field(alias="nodeIds")


class GetanchorelementParams(BaseModel):
    """Returns the target anchor element of the given anchor query according to
    https://www.w3.org/TR/css-anchor-position-1/#target."""

    node_id: NodeId = Field(alias="nodeId")
    anchor_specifier: str | None = Field(default=None, alias="anchorSpecifier")


class GetanchorelementResult(BaseModel):
    node_id: NodeId = Field(alias="nodeId")


class ForceshowpopoverParams(BaseModel):
    """When enabling, this API force-opens the popover identified by nodeId
    and keeps it open until disabled."""

    node_id: NodeId = Field(alias="nodeId")
    enable: bool = Field(alias="enable")


class ForceshowpopoverResult(BaseModel):
    node_ids: list[NodeId] = Field(alias="nodeIds")


# Client


class DOMClient:
    """This domain exposes DOM read/write operations. Each DOM Node is represented with its mirror object
    that has an `id`. This `id` can be used to get additional information on the Node, resolve it into
    the JavaScript object wrapper, etc. It is important that client receives DOM events only for the
    nodes that are known to the client. Backend keeps track of the nodes that were sent to the client
    and never sends the same node twice. It is client's responsibility to collect information about
    the nodes that were sent to the client. Note that `iframe` owner elements will return
    corresponding document elements as their child nodes."""

    def __init__(self, cdp_client: Any) -> None:
        self._cdp = cdp_client

    async def collect_class_names_from_subtree(
        self, node_id: NodeId
    ) -> CollectclassnamesfromsubtreeResult:
        """Collects class names for the node with given id and all of it's child nodes."""
        params = CollectclassnamesfromsubtreeParams(
            node_id=node_id,
        )
        result = await self._cdp.call(
            "DOM.collectClassNamesFromSubtree",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return CollectclassnamesfromsubtreeResult(**result)

    async def copy_to(
        self,
        node_id: NodeId,
        target_node_id: NodeId,
        insert_before_node_id: NodeId | None = None,
    ) -> CopytoResult:
        """Creates a deep copy of the specified node and places it into the target container before the
        given anchor."""
        params = CopytoParams(
            node_id=node_id,
            target_node_id=target_node_id,
            insert_before_node_id=insert_before_node_id,
        )
        result = await self._cdp.call(
            "DOM.copyTo", params.model_dump(by_alias=True, exclude_none=True)
        )
        return CopytoResult(**result)

    async def describe_node(
        self,
        node_id: NodeId | None = None,
        backend_node_id: BackendNodeId | None = None,
        object_id: Runtime.RemoteObjectId | None = None,
        depth: int | None = None,
        pierce: bool | None = None,
    ) -> DescribenodeResult:
        """Describes node given its id, does not require domain to be enabled. Does not start tracking any
        objects, can be used for automation."""
        params = DescribenodeParams(
            node_id=node_id,
            backend_node_id=backend_node_id,
            object_id=object_id,
            depth=depth,
            pierce=pierce,
        )
        result = await self._cdp.call(
            "DOM.describeNode", params.model_dump(by_alias=True, exclude_none=True)
        )
        return DescribenodeResult(**result)

    async def scroll_into_view_if_needed(
        self,
        node_id: NodeId | None = None,
        backend_node_id: BackendNodeId | None = None,
        object_id: Runtime.RemoteObjectId | None = None,
        rect: Rect | None = None,
    ) -> None:
        """Scrolls the specified rect of the given node into view if not already visible.
        Note: exactly one between nodeId, backendNodeId and objectId should be passed
        to identify the node."""
        params = ScrollintoviewifneededParams(
            node_id=node_id,
            backend_node_id=backend_node_id,
            object_id=object_id,
            rect=rect,
        )
        result = await self._cdp.call(
            "DOM.scrollIntoViewIfNeeded",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def disable(self) -> None:
        """Disables DOM agent for the given page."""
        result = await self._cdp.call("DOM.disable", {})
        return None

    async def discard_search_results(self, search_id: str) -> None:
        """Discards search results from the session with the given id. `getSearchResults` should no longer
        be called for that search."""
        params = DiscardsearchresultsParams(
            search_id=search_id,
        )
        result = await self._cdp.call(
            "DOM.discardSearchResults",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def enable(
        self, include_whitespace: Literal["none", "all"] | None = None
    ) -> None:
        """Enables DOM agent for the given page."""
        params = EnableParams(
            include_whitespace=include_whitespace,
        )
        result = await self._cdp.call(
            "DOM.enable", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def focus(
        self,
        node_id: NodeId | None = None,
        backend_node_id: BackendNodeId | None = None,
        object_id: Runtime.RemoteObjectId | None = None,
    ) -> None:
        """Focuses the given element."""
        params = FocusParams(
            node_id=node_id,
            backend_node_id=backend_node_id,
            object_id=object_id,
        )
        result = await self._cdp.call(
            "DOM.focus", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def get_attributes(self, node_id: NodeId) -> GetattributesResult:
        """Returns attributes for the specified node."""
        params = GetattributesParams(
            node_id=node_id,
        )
        result = await self._cdp.call(
            "DOM.getAttributes", params.model_dump(by_alias=True, exclude_none=True)
        )
        return GetattributesResult(**result)

    async def get_box_model(
        self,
        node_id: NodeId | None = None,
        backend_node_id: BackendNodeId | None = None,
        object_id: Runtime.RemoteObjectId | None = None,
    ) -> GetboxmodelResult:
        """Returns boxes for the given node."""
        params = GetboxmodelParams(
            node_id=node_id,
            backend_node_id=backend_node_id,
            object_id=object_id,
        )
        result = await self._cdp.call(
            "DOM.getBoxModel", params.model_dump(by_alias=True, exclude_none=True)
        )
        return GetboxmodelResult(**result)

    async def get_content_quads(
        self,
        node_id: NodeId | None = None,
        backend_node_id: BackendNodeId | None = None,
        object_id: Runtime.RemoteObjectId | None = None,
    ) -> GetcontentquadsResult:
        """Returns quads that describe node position on the page. This method
        might return multiple quads for inline nodes."""
        params = GetcontentquadsParams(
            node_id=node_id,
            backend_node_id=backend_node_id,
            object_id=object_id,
        )
        result = await self._cdp.call(
            "DOM.getContentQuads", params.model_dump(by_alias=True, exclude_none=True)
        )
        return GetcontentquadsResult(**result)

    async def get_document(
        self, depth: int | None = None, pierce: bool | None = None
    ) -> GetdocumentResult:
        """Returns the root DOM node (and optionally the subtree) to the caller.
        Implicitly enables the DOM domain events for the current target."""
        params = GetdocumentParams(
            depth=depth,
            pierce=pierce,
        )
        result = await self._cdp.call(
            "DOM.getDocument", params.model_dump(by_alias=True, exclude_none=True)
        )
        return GetdocumentResult(**result)

    async def get_flattened_document(
        self, depth: int | None = None, pierce: bool | None = None
    ) -> GetflatteneddocumentResult:
        """Returns the root DOM node (and optionally the subtree) to the caller.
        Deprecated, as it is not designed to work well with the rest of the DOM agent.
        Use DOMSnapshot.captureSnapshot instead."""
        params = GetflatteneddocumentParams(
            depth=depth,
            pierce=pierce,
        )
        result = await self._cdp.call(
            "DOM.getFlattenedDocument",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return GetflatteneddocumentResult(**result)

    async def get_nodes_for_subtree_by_style(
        self,
        node_id: NodeId,
        computed_styles: list[CSSComputedStyleProperty],
        pierce: bool | None = None,
    ) -> GetnodesforsubtreebystyleResult:
        """Finds nodes with a given computed style in a subtree."""
        params = GetnodesforsubtreebystyleParams(
            node_id=node_id,
            computed_styles=computed_styles,
            pierce=pierce,
        )
        result = await self._cdp.call(
            "DOM.getNodesForSubtreeByStyle",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return GetnodesforsubtreebystyleResult(**result)

    async def get_node_for_location(
        self,
        x: int,
        y: int,
        include_user_agent_shadow_d_o_m: bool | None = None,
        ignore_pointer_events_none: bool | None = None,
    ) -> GetnodeforlocationResult:
        """Returns node id at given location. Depending on whether DOM domain is enabled, nodeId is
        either returned or not."""
        params = GetnodeforlocationParams(
            x=x,
            y=y,
            include_user_agent_shadow_d_o_m=include_user_agent_shadow_d_o_m,
            ignore_pointer_events_none=ignore_pointer_events_none,
        )
        result = await self._cdp.call(
            "DOM.getNodeForLocation",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return GetnodeforlocationResult(**result)

    async def get_outer_h_t_m_l(
        self,
        node_id: NodeId | None = None,
        backend_node_id: BackendNodeId | None = None,
        object_id: Runtime.RemoteObjectId | None = None,
        include_shadow_d_o_m: bool | None = None,
    ) -> GetouterhtmlResult:
        """Returns node's HTML markup."""
        params = GetouterhtmlParams(
            node_id=node_id,
            backend_node_id=backend_node_id,
            object_id=object_id,
            include_shadow_d_o_m=include_shadow_d_o_m,
        )
        result = await self._cdp.call(
            "DOM.getOuterHTML", params.model_dump(by_alias=True, exclude_none=True)
        )
        return GetouterhtmlResult(**result)

    async def get_relayout_boundary(self, node_id: NodeId) -> GetrelayoutboundaryResult:
        """Returns the id of the nearest ancestor that is a relayout boundary."""
        params = GetrelayoutboundaryParams(
            node_id=node_id,
        )
        result = await self._cdp.call(
            "DOM.getRelayoutBoundary",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return GetrelayoutboundaryResult(**result)

    async def get_search_results(
        self, search_id: str, from_index: int, to_index: int
    ) -> GetsearchresultsResult:
        """Returns search results from given `fromIndex` to given `toIndex` from the search with the given
        identifier."""
        params = GetsearchresultsParams(
            search_id=search_id,
            from_index=from_index,
            to_index=to_index,
        )
        result = await self._cdp.call(
            "DOM.getSearchResults", params.model_dump(by_alias=True, exclude_none=True)
        )
        return GetsearchresultsResult(**result)

    async def hide_highlight(self) -> None:
        """Hides any highlight."""
        result = await self._cdp.call("DOM.hideHighlight", {})
        return None

    async def highlight_node(self) -> None:
        """Highlights DOM node."""
        result = await self._cdp.call("DOM.highlightNode", {})
        return None

    async def highlight_rect(self) -> None:
        """Highlights given rectangle."""
        result = await self._cdp.call("DOM.highlightRect", {})
        return None

    async def mark_undoable_state(self) -> None:
        """Marks last undoable state."""
        result = await self._cdp.call("DOM.markUndoableState", {})
        return None

    async def move_to(
        self,
        node_id: NodeId,
        target_node_id: NodeId,
        insert_before_node_id: NodeId | None = None,
    ) -> MovetoResult:
        """Moves node into the new container, places it before the given anchor."""
        params = MovetoParams(
            node_id=node_id,
            target_node_id=target_node_id,
            insert_before_node_id=insert_before_node_id,
        )
        result = await self._cdp.call(
            "DOM.moveTo", params.model_dump(by_alias=True, exclude_none=True)
        )
        return MovetoResult(**result)

    async def perform_search(
        self, query: str, include_user_agent_shadow_d_o_m: bool | None = None
    ) -> PerformsearchResult:
        """Searches for a given string in the DOM tree. Use `getSearchResults` to access search results or
        `cancelSearch` to end this search session."""
        params = PerformsearchParams(
            query=query,
            include_user_agent_shadow_d_o_m=include_user_agent_shadow_d_o_m,
        )
        result = await self._cdp.call(
            "DOM.performSearch", params.model_dump(by_alias=True, exclude_none=True)
        )
        return PerformsearchResult(**result)

    async def push_node_by_path_to_frontend(
        self, path: str
    ) -> PushnodebypathtofrontendResult:
        """Requests that the node is sent to the caller given its path. // FIXME, use XPath"""
        params = PushnodebypathtofrontendParams(
            path=path,
        )
        result = await self._cdp.call(
            "DOM.pushNodeByPathToFrontend",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return PushnodebypathtofrontendResult(**result)

    async def push_nodes_by_backend_ids_to_frontend(
        self, backend_node_ids: list[BackendNodeId]
    ) -> PushnodesbybackendidstofrontendResult:
        """Requests that a batch of nodes is sent to the caller given their backend node ids."""
        params = PushnodesbybackendidstofrontendParams(
            backend_node_ids=backend_node_ids,
        )
        result = await self._cdp.call(
            "DOM.pushNodesByBackendIdsToFrontend",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return PushnodesbybackendidstofrontendResult(**result)

    async def query_selector(
        self, node_id: NodeId, selector: str
    ) -> QueryselectorResult:
        """Executes `querySelector` on a given node."""
        params = QueryselectorParams(
            node_id=node_id,
            selector=selector,
        )
        result = await self._cdp.call(
            "DOM.querySelector", params.model_dump(by_alias=True, exclude_none=True)
        )
        return QueryselectorResult(**result)

    async def query_selector_all(
        self, node_id: NodeId, selector: str
    ) -> QueryselectorallResult:
        """Executes `querySelectorAll` on a given node."""
        params = QueryselectorallParams(
            node_id=node_id,
            selector=selector,
        )
        result = await self._cdp.call(
            "DOM.querySelectorAll", params.model_dump(by_alias=True, exclude_none=True)
        )
        return QueryselectorallResult(**result)

    async def get_top_layer_elements(self) -> GettoplayerelementsResult:
        """Returns NodeIds of current top layer elements.
        Top layer is rendered closest to the user within a viewport, therefore its elements always
        appear on top of all other content."""
        result = await self._cdp.call("DOM.getTopLayerElements", {})
        return GettoplayerelementsResult(**result)

    async def get_element_by_relation(
        self,
        node_id: NodeId,
        relation: Literal["PopoverTarget", "InterestTarget", "CommandFor"],
    ) -> GetelementbyrelationResult:
        """Returns the NodeId of the matched element according to certain relations."""
        params = GetelementbyrelationParams(
            node_id=node_id,
            relation=relation,
        )
        result = await self._cdp.call(
            "DOM.getElementByRelation",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return GetelementbyrelationResult(**result)

    async def redo(self) -> None:
        """Re-does the last undone action."""
        result = await self._cdp.call("DOM.redo", {})
        return None

    async def remove_attribute(self, node_id: NodeId, name: str) -> None:
        """Removes attribute with given name from an element with given id."""
        params = RemoveattributeParams(
            node_id=node_id,
            name=name,
        )
        result = await self._cdp.call(
            "DOM.removeAttribute", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def remove_node(self, node_id: NodeId) -> None:
        """Removes node with given id."""
        params = RemovenodeParams(
            node_id=node_id,
        )
        result = await self._cdp.call(
            "DOM.removeNode", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def request_child_nodes(
        self, node_id: NodeId, depth: int | None = None, pierce: bool | None = None
    ) -> None:
        """Requests that children of the node with given id are returned to the caller in form of
        `setChildNodes` events where not only immediate children are retrieved, but all children down to
        the specified depth."""
        params = RequestchildnodesParams(
            node_id=node_id,
            depth=depth,
            pierce=pierce,
        )
        result = await self._cdp.call(
            "DOM.requestChildNodes", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def request_node(
        self, object_id: Runtime.RemoteObjectId
    ) -> RequestnodeResult:
        """Requests that the node is sent to the caller given the JavaScript node object reference. All
        nodes that form the path from the node to the root are also sent to the client as a series of
        `setChildNodes` notifications."""
        params = RequestnodeParams(
            object_id=object_id,
        )
        result = await self._cdp.call(
            "DOM.requestNode", params.model_dump(by_alias=True, exclude_none=True)
        )
        return RequestnodeResult(**result)

    async def resolve_node(
        self,
        node_id: NodeId | None = None,
        backend_node_id: DOM.BackendNodeId | None = None,
        object_group: str | None = None,
        execution_context_id: Runtime.ExecutionContextId | None = None,
    ) -> ResolvenodeResult:
        """Resolves the JavaScript node object for a given NodeId or BackendNodeId."""
        params = ResolvenodeParams(
            node_id=node_id,
            backend_node_id=backend_node_id,
            object_group=object_group,
            execution_context_id=execution_context_id,
        )
        result = await self._cdp.call(
            "DOM.resolveNode", params.model_dump(by_alias=True, exclude_none=True)
        )
        return ResolvenodeResult(**result)

    async def set_attribute_value(self, node_id: NodeId, name: str, value: str) -> None:
        """Sets attribute for an element with given id."""
        params = SetattributevalueParams(
            node_id=node_id,
            name=name,
            value=value,
        )
        result = await self._cdp.call(
            "DOM.setAttributeValue", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def set_attributes_as_text(
        self, node_id: NodeId, text: str, name: str | None = None
    ) -> None:
        """Sets attributes on element with given id. This method is useful when user edits some existing
        attribute value and types in several attribute name/value pairs."""
        params = SetattributesastextParams(
            node_id=node_id,
            text=text,
            name=name,
        )
        result = await self._cdp.call(
            "DOM.setAttributesAsText",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def set_file_input_files(
        self,
        files: list[str],
        node_id: NodeId | None = None,
        backend_node_id: BackendNodeId | None = None,
        object_id: Runtime.RemoteObjectId | None = None,
    ) -> None:
        """Sets files for the given file input element."""
        params = SetfileinputfilesParams(
            files=files,
            node_id=node_id,
            backend_node_id=backend_node_id,
            object_id=object_id,
        )
        result = await self._cdp.call(
            "DOM.setFileInputFiles", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def set_node_stack_traces_enabled(self, enable: bool) -> None:
        """Sets if stack traces should be captured for Nodes. See `Node.getNodeStackTraces`. Default is disabled."""
        params = SetnodestacktracesenabledParams(
            enable=enable,
        )
        result = await self._cdp.call(
            "DOM.setNodeStackTracesEnabled",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def get_node_stack_traces(self, node_id: NodeId) -> GetnodestacktracesResult:
        """Gets stack traces associated with a Node. As of now, only provides stack trace for Node creation."""
        params = GetnodestacktracesParams(
            node_id=node_id,
        )
        result = await self._cdp.call(
            "DOM.getNodeStackTraces",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return GetnodestacktracesResult(**result)

    async def get_file_info(
        self, object_id: Runtime.RemoteObjectId
    ) -> GetfileinfoResult:
        """Returns file information for the given
        File wrapper."""
        params = GetfileinfoParams(
            object_id=object_id,
        )
        result = await self._cdp.call(
            "DOM.getFileInfo", params.model_dump(by_alias=True, exclude_none=True)
        )
        return GetfileinfoResult(**result)

    async def get_detached_dom_nodes(self) -> GetdetacheddomnodesResult:
        """Returns list of detached nodes"""
        result = await self._cdp.call("DOM.getDetachedDomNodes", {})
        return GetdetacheddomnodesResult(**result)

    async def set_inspected_node(self, node_id: NodeId) -> None:
        """Enables console to refer to the node with given id via $x (see Command Line API for more details
        $x functions)."""
        params = SetinspectednodeParams(
            node_id=node_id,
        )
        result = await self._cdp.call(
            "DOM.setInspectedNode", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def set_node_name(self, node_id: NodeId, name: str) -> SetnodenameResult:
        """Sets node name for a node with given id."""
        params = SetnodenameParams(
            node_id=node_id,
            name=name,
        )
        result = await self._cdp.call(
            "DOM.setNodeName", params.model_dump(by_alias=True, exclude_none=True)
        )
        return SetnodenameResult(**result)

    async def set_node_value(self, node_id: NodeId, value: str) -> None:
        """Sets node value for a node with given id."""
        params = SetnodevalueParams(
            node_id=node_id,
            value=value,
        )
        result = await self._cdp.call(
            "DOM.setNodeValue", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def set_outer_h_t_m_l(self, node_id: NodeId, outer_h_t_m_l: str) -> None:
        """Sets node HTML markup, returns new node id."""
        params = SetouterhtmlParams(
            node_id=node_id,
            outer_h_t_m_l=outer_h_t_m_l,
        )
        result = await self._cdp.call(
            "DOM.setOuterHTML", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def undo(self) -> None:
        """Undoes the last performed action."""
        result = await self._cdp.call("DOM.undo", {})
        return None

    async def get_frame_owner(self, frame_id: Page.FrameId) -> GetframeownerResult:
        """Returns iframe node that owns iframe with the given domain."""
        params = GetframeownerParams(
            frame_id=frame_id,
        )
        result = await self._cdp.call(
            "DOM.getFrameOwner", params.model_dump(by_alias=True, exclude_none=True)
        )
        return GetframeownerResult(**result)

    async def get_container_for_node(
        self,
        node_id: NodeId,
        container_name: str | None = None,
        physical_axes: PhysicalAxes | None = None,
        logical_axes: LogicalAxes | None = None,
        queries_scroll_state: bool | None = None,
        queries_anchored: bool | None = None,
    ) -> GetcontainerfornodeResult:
        """Returns the query container of the given node based on container query
        conditions: containerName, physical and logical axes, and whether it queries
        scroll-state or anchored elements. If no axes are provided and
        queriesScrollState is false, the style container is returned, which is the
        direct parent or the closest element with a matching container-name."""
        params = GetcontainerfornodeParams(
            node_id=node_id,
            container_name=container_name,
            physical_axes=physical_axes,
            logical_axes=logical_axes,
            queries_scroll_state=queries_scroll_state,
            queries_anchored=queries_anchored,
        )
        result = await self._cdp.call(
            "DOM.getContainerForNode",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return GetcontainerfornodeResult(**result)

    async def get_querying_descendants_for_container(
        self, node_id: NodeId
    ) -> GetqueryingdescendantsforcontainerResult:
        """Returns the descendants of a container query container that have
        container queries against this container."""
        params = GetqueryingdescendantsforcontainerParams(
            node_id=node_id,
        )
        result = await self._cdp.call(
            "DOM.getQueryingDescendantsForContainer",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return GetqueryingdescendantsforcontainerResult(**result)

    async def get_anchor_element(
        self, node_id: NodeId, anchor_specifier: str | None = None
    ) -> GetanchorelementResult:
        """Returns the target anchor element of the given anchor query according to
        https://www.w3.org/TR/css-anchor-position-1/#target."""
        params = GetanchorelementParams(
            node_id=node_id,
            anchor_specifier=anchor_specifier,
        )
        result = await self._cdp.call(
            "DOM.getAnchorElement", params.model_dump(by_alias=True, exclude_none=True)
        )
        return GetanchorelementResult(**result)

    async def force_show_popover(
        self, node_id: NodeId, enable: bool
    ) -> ForceshowpopoverResult:
        """When enabling, this API force-opens the popover identified by nodeId
        and keeps it open until disabled."""
        params = ForceshowpopoverParams(
            node_id=node_id,
            enable=enable,
        )
        result = await self._cdp.call(
            "DOM.forceShowPopover", params.model_dump(by_alias=True, exclude_none=True)
        )
        return ForceshowpopoverResult(**result)
