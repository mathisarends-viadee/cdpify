"""Generated from CDP specification"""

from pydantic import BaseModel, Field
from typing import Literal, Any

# Domain Types

ScriptId = str


class SerializationOptions(BaseModel):
    """Represents options for serialization. Overrides `generatePreview` and `returnByValue`."""

    serialization: Literal["deep", "json", "idOnly"]
    max_depth: int | None = None
    additional_parameters: dict[str, Any] | None = None


class DeepSerializedValue(BaseModel):
    """Represents deep serialized value."""

    type: Literal[
        "undefined",
        "null",
        "string",
        "number",
        "boolean",
        "bigint",
        "regexp",
        "date",
        "symbol",
        "array",
        "object",
        "function",
        "map",
        "set",
        "weakmap",
        "weakset",
        "error",
        "proxy",
        "promise",
        "typedarray",
        "arraybuffer",
        "node",
        "window",
        "generator",
    ]
    value: Any | None = None
    object_id: str | None = None
    weak_local_object_reference: int | None = None


RemoteObjectId = str
UnserializableValue = str


class RemoteObject(BaseModel):
    """Mirror object referencing original JavaScript object."""

    type: Literal[
        "object",
        "function",
        "undefined",
        "string",
        "number",
        "boolean",
        "symbol",
        "bigint",
    ]
    subtype: (
        Literal[
            "array",
            "null",
            "node",
            "regexp",
            "date",
            "map",
            "set",
            "weakmap",
            "weakset",
            "iterator",
            "generator",
            "error",
            "proxy",
            "promise",
            "typedarray",
            "arraybuffer",
            "dataview",
            "webassemblymemory",
            "wasmvalue",
            "trustedtype",
        ]
        | None
    ) = None
    class_name: str | None = None
    value: Any | None = None
    unserializable_value: UnserializableValue | None = None
    description: str | None = None
    deep_serialized_value: DeepSerializedValue | None = None
    object_id: RemoteObjectId | None = None
    preview: ObjectPreview | None = None
    custom_preview: CustomPreview | None = None


class CustomPreview(BaseModel):
    header: str
    body_getter_id: RemoteObjectId | None = None


class ObjectPreview(BaseModel):
    """Object containing abbreviated remote object value."""

    type: Literal[
        "object",
        "function",
        "undefined",
        "string",
        "number",
        "boolean",
        "symbol",
        "bigint",
    ]
    subtype: (
        Literal[
            "array",
            "null",
            "node",
            "regexp",
            "date",
            "map",
            "set",
            "weakmap",
            "weakset",
            "iterator",
            "generator",
            "error",
            "proxy",
            "promise",
            "typedarray",
            "arraybuffer",
            "dataview",
            "webassemblymemory",
            "wasmvalue",
            "trustedtype",
        ]
        | None
    ) = None
    description: str | None = None
    overflow: bool
    properties: list[PropertyPreview]
    entries: list[EntryPreview] | None = None


class PropertyPreview(BaseModel):
    name: str
    type: Literal[
        "object",
        "function",
        "undefined",
        "string",
        "number",
        "boolean",
        "symbol",
        "accessor",
        "bigint",
    ]
    value: str | None = None
    value_preview: ObjectPreview | None = None
    subtype: (
        Literal[
            "array",
            "null",
            "node",
            "regexp",
            "date",
            "map",
            "set",
            "weakmap",
            "weakset",
            "iterator",
            "generator",
            "error",
            "proxy",
            "promise",
            "typedarray",
            "arraybuffer",
            "dataview",
            "webassemblymemory",
            "wasmvalue",
            "trustedtype",
        ]
        | None
    ) = None


class EntryPreview(BaseModel):
    key: ObjectPreview | None = None
    value: ObjectPreview


class PropertyDescriptor(BaseModel):
    """Object property descriptor."""

    name: str
    value: RemoteObject | None = None
    writable: bool | None = None
    get: RemoteObject | None = None
    set: RemoteObject | None = None
    configurable: bool
    enumerable: bool
    was_thrown: bool | None = None
    is_own: bool | None = None
    symbol: RemoteObject | None = None


class InternalPropertyDescriptor(BaseModel):
    """Object internal property descriptor. This property isn't normally visible in JavaScript code."""

    name: str
    value: RemoteObject | None = None


class PrivatePropertyDescriptor(BaseModel):
    """Object private field descriptor."""

    name: str
    value: RemoteObject | None = None
    get: RemoteObject | None = None
    set: RemoteObject | None = None


class CallArgument(BaseModel):
    """Represents function call argument. Either remote object id `objectId`, primitive `value`,
    unserializable primitive value or neither of (for undefined) them should be specified."""

    value: Any | None = None
    unserializable_value: UnserializableValue | None = None
    object_id: RemoteObjectId | None = None


ExecutionContextId = int


class ExecutionContextDescription(BaseModel):
    """Description of an isolated world."""

    id: ExecutionContextId
    origin: str
    name: str
    unique_id: str
    aux_data: dict[str, Any] | None = None


class ExceptionDetails(BaseModel):
    """Detailed information about exception (or error) that was thrown during script compilation or
    execution."""

    exception_id: int
    text: str
    line_number: int
    column_number: int
    script_id: ScriptId | None = None
    url: str | None = None
    stack_trace: StackTrace | None = None
    exception: RemoteObject | None = None
    execution_context_id: ExecutionContextId | None = None
    exception_meta_data: dict[str, Any] | None = None


Timestamp = float
TimeDelta = float


class CallFrame(BaseModel):
    """Stack entry for runtime errors and assertions."""

    function_name: str
    script_id: ScriptId
    url: str
    line_number: int
    column_number: int


class StackTrace(BaseModel):
    """Call frames for assertions or error messages."""

    description: str | None = None
    call_frames: list[CallFrame]
    parent: StackTrace | None = None
    parent_id: StackTraceId | None = None


UniqueDebuggerId = str


class StackTraceId(BaseModel):
    """If `debuggerId` is set stack trace comes from another debugger and can be resolved there. This
    allows to track cross-debugger calls. See `Runtime.StackTrace` and `Debugger.paused` for usages."""

    id: str
    debugger_id: UniqueDebuggerId | None = None


# Command Parameters and Results


class AwaitpromiseParams(BaseModel):
    """Add handler to promise with given promise object id."""

    promise_object_id: RemoteObjectId = Field(alias="promiseObjectId")
    return_by_value: bool | None = Field(default=None, alias="returnByValue")
    generate_preview: bool | None = Field(default=None, alias="generatePreview")


class AwaitpromiseResult(BaseModel):
    result: RemoteObject = Field(alias="result")
    exception_details: ExceptionDetails | None = Field(
        default=None, alias="exceptionDetails"
    )


class CallfunctiononParams(BaseModel):
    """Calls function with given declaration on the given object. Object group of the result is
    inherited from the target object."""

    function_declaration: str = Field(alias="functionDeclaration")
    object_id: RemoteObjectId | None = Field(default=None, alias="objectId")
    arguments: list[CallArgument] | None = Field(default=None, alias="arguments")
    silent: bool | None = Field(default=None, alias="silent")
    return_by_value: bool | None = Field(default=None, alias="returnByValue")
    generate_preview: bool | None = Field(default=None, alias="generatePreview")
    user_gesture: bool | None = Field(default=None, alias="userGesture")
    await_promise: bool | None = Field(default=None, alias="awaitPromise")
    execution_context_id: ExecutionContextId | None = Field(
        default=None, alias="executionContextId"
    )
    object_group: str | None = Field(default=None, alias="objectGroup")
    throw_on_side_effect: bool | None = Field(default=None, alias="throwOnSideEffect")
    unique_context_id: str | None = Field(default=None, alias="uniqueContextId")
    serialization_options: SerializationOptions | None = Field(
        default=None, alias="serializationOptions"
    )


class CallfunctiononResult(BaseModel):
    result: RemoteObject = Field(alias="result")
    exception_details: ExceptionDetails | None = Field(
        default=None, alias="exceptionDetails"
    )


class CompilescriptParams(BaseModel):
    """Compiles expression."""

    expression: str = Field(alias="expression")
    source_u_r_l: str = Field(alias="sourceURL")
    persist_script: bool = Field(alias="persistScript")
    execution_context_id: ExecutionContextId | None = Field(
        default=None, alias="executionContextId"
    )


class CompilescriptResult(BaseModel):
    script_id: ScriptId | None = Field(default=None, alias="scriptId")
    exception_details: ExceptionDetails | None = Field(
        default=None, alias="exceptionDetails"
    )


class EvaluateParams(BaseModel):
    """Evaluates expression on global object."""

    expression: str = Field(alias="expression")
    object_group: str | None = Field(default=None, alias="objectGroup")
    include_command_line_a_p_i: bool | None = Field(
        default=None, alias="includeCommandLineAPI"
    )
    silent: bool | None = Field(default=None, alias="silent")
    context_id: ExecutionContextId | None = Field(default=None, alias="contextId")
    return_by_value: bool | None = Field(default=None, alias="returnByValue")
    generate_preview: bool | None = Field(default=None, alias="generatePreview")
    user_gesture: bool | None = Field(default=None, alias="userGesture")
    await_promise: bool | None = Field(default=None, alias="awaitPromise")
    throw_on_side_effect: bool | None = Field(default=None, alias="throwOnSideEffect")
    timeout: TimeDelta | None = Field(default=None, alias="timeout")
    disable_breaks: bool | None = Field(default=None, alias="disableBreaks")
    repl_mode: bool | None = Field(default=None, alias="replMode")
    allow_unsafe_eval_blocked_by_c_s_p: bool | None = Field(
        default=None, alias="allowUnsafeEvalBlockedByCSP"
    )
    unique_context_id: str | None = Field(default=None, alias="uniqueContextId")
    serialization_options: SerializationOptions | None = Field(
        default=None, alias="serializationOptions"
    )


class EvaluateResult(BaseModel):
    result: RemoteObject = Field(alias="result")
    exception_details: ExceptionDetails | None = Field(
        default=None, alias="exceptionDetails"
    )


class GetisolateidResult(BaseModel):
    id: str = Field(alias="id")


class GetheapusageResult(BaseModel):
    used_size: float = Field(alias="usedSize")
    total_size: float = Field(alias="totalSize")
    embedder_heap_used_size: float = Field(alias="embedderHeapUsedSize")
    backing_storage_size: float = Field(alias="backingStorageSize")


class GetpropertiesParams(BaseModel):
    """Returns properties of a given object. Object group of the result is inherited from the target
    object."""

    object_id: RemoteObjectId = Field(alias="objectId")
    own_properties: bool | None = Field(default=None, alias="ownProperties")
    accessor_properties_only: bool | None = Field(
        default=None, alias="accessorPropertiesOnly"
    )
    generate_preview: bool | None = Field(default=None, alias="generatePreview")
    non_indexed_properties_only: bool | None = Field(
        default=None, alias="nonIndexedPropertiesOnly"
    )


class GetpropertiesResult(BaseModel):
    result: list[PropertyDescriptor] = Field(alias="result")
    internal_properties: list[InternalPropertyDescriptor] | None = Field(
        default=None, alias="internalProperties"
    )
    private_properties: list[PrivatePropertyDescriptor] | None = Field(
        default=None, alias="privateProperties"
    )
    exception_details: ExceptionDetails | None = Field(
        default=None, alias="exceptionDetails"
    )


class GloballexicalscopenamesParams(BaseModel):
    """Returns all let, const and class variables from global scope."""

    execution_context_id: ExecutionContextId | None = Field(
        default=None, alias="executionContextId"
    )


class GloballexicalscopenamesResult(BaseModel):
    names: list[str] = Field(alias="names")


class QueryobjectsParams(BaseModel):
    prototype_object_id: RemoteObjectId = Field(alias="prototypeObjectId")
    object_group: str | None = Field(default=None, alias="objectGroup")


class QueryobjectsResult(BaseModel):
    objects: RemoteObject = Field(alias="objects")


class ReleaseobjectParams(BaseModel):
    """Releases remote object with given id."""

    object_id: RemoteObjectId = Field(alias="objectId")


class ReleaseobjectgroupParams(BaseModel):
    """Releases all remote objects that belong to a given group."""

    object_group: str = Field(alias="objectGroup")


class RunscriptParams(BaseModel):
    """Runs script with given id in a given context."""

    script_id: ScriptId = Field(alias="scriptId")
    execution_context_id: ExecutionContextId | None = Field(
        default=None, alias="executionContextId"
    )
    object_group: str | None = Field(default=None, alias="objectGroup")
    silent: bool | None = Field(default=None, alias="silent")
    include_command_line_a_p_i: bool | None = Field(
        default=None, alias="includeCommandLineAPI"
    )
    return_by_value: bool | None = Field(default=None, alias="returnByValue")
    generate_preview: bool | None = Field(default=None, alias="generatePreview")
    await_promise: bool | None = Field(default=None, alias="awaitPromise")


class RunscriptResult(BaseModel):
    result: RemoteObject = Field(alias="result")
    exception_details: ExceptionDetails | None = Field(
        default=None, alias="exceptionDetails"
    )


class SetasynccallstackdepthParams(BaseModel):
    """Enables or disables async call stacks tracking."""

    max_depth: int = Field(alias="maxDepth")


class SetcustomobjectformatterenabledParams(BaseModel):
    enabled: bool = Field(alias="enabled")


class SetmaxcallstacksizetocaptureParams(BaseModel):
    size: int = Field(alias="size")


class AddbindingParams(BaseModel):
    """If executionContextId is empty, adds binding with the given name on the
    global objects of all inspected contexts, including those created later,
    bindings survive reloads.
    Binding function takes exactly one argument, this argument should be string,
    in case of any other input, function throws an exception.
    Each binding function call produces Runtime.bindingCalled notification."""

    name: str = Field(alias="name")
    execution_context_id: ExecutionContextId | None = Field(
        default=None, alias="executionContextId"
    )
    execution_context_name: str | None = Field(
        default=None, alias="executionContextName"
    )


class RemovebindingParams(BaseModel):
    """This method does not remove binding function from global object but
    unsubscribes current runtime agent from Runtime.bindingCalled notifications."""

    name: str = Field(alias="name")


class GetexceptiondetailsParams(BaseModel):
    """This method tries to lookup and populate exception details for a
    JavaScript Error object.
    Note that the stackTrace portion of the resulting exceptionDetails will
    only be populated if the Runtime domain was enabled at the time when the
    Error was thrown."""

    error_object_id: RemoteObjectId = Field(alias="errorObjectId")


class GetexceptiondetailsResult(BaseModel):
    exception_details: ExceptionDetails | None = Field(
        default=None, alias="exceptionDetails"
    )


# Client


class RuntimeClient:
    """Runtime domain exposes JavaScript runtime by means of remote evaluation and mirror objects.
    Evaluation results are returned as mirror object that expose object type, string representation
    and unique identifier that can be used for further object reference. Original objects are
    maintained in memory unless they are either explicitly released or are released along with the
    other objects in their object group."""

    def __init__(self, cdp_client: Any) -> None:
        self._cdp = cdp_client

    async def await_promise(
        self,
        promise_object_id: RemoteObjectId,
        return_by_value: bool | None = None,
        generate_preview: bool | None = None,
    ) -> AwaitpromiseResult:
        """Add handler to promise with given promise object id."""
        params = AwaitpromiseParams(
            promise_object_id=promise_object_id,
            return_by_value=return_by_value,
            generate_preview=generate_preview,
        )
        result = await self._cdp.call(
            "Runtime.awaitPromise", params.model_dump(by_alias=True, exclude_none=True)
        )
        return AwaitpromiseResult(**result)

    async def call_function_on(
        self,
        function_declaration: str,
        object_id: RemoteObjectId | None = None,
        arguments: list[CallArgument] | None = None,
        silent: bool | None = None,
        return_by_value: bool | None = None,
        generate_preview: bool | None = None,
        user_gesture: bool | None = None,
        await_promise: bool | None = None,
        execution_context_id: ExecutionContextId | None = None,
        object_group: str | None = None,
        throw_on_side_effect: bool | None = None,
        unique_context_id: str | None = None,
        serialization_options: SerializationOptions | None = None,
    ) -> CallfunctiononResult:
        """Calls function with given declaration on the given object. Object group of the result is
        inherited from the target object."""
        params = CallfunctiononParams(
            function_declaration=function_declaration,
            object_id=object_id,
            arguments=arguments,
            silent=silent,
            return_by_value=return_by_value,
            generate_preview=generate_preview,
            user_gesture=user_gesture,
            await_promise=await_promise,
            execution_context_id=execution_context_id,
            object_group=object_group,
            throw_on_side_effect=throw_on_side_effect,
            unique_context_id=unique_context_id,
            serialization_options=serialization_options,
        )
        result = await self._cdp.call(
            "Runtime.callFunctionOn",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return CallfunctiononResult(**result)

    async def compile_script(
        self,
        expression: str,
        source_u_r_l: str,
        persist_script: bool,
        execution_context_id: ExecutionContextId | None = None,
    ) -> CompilescriptResult:
        """Compiles expression."""
        params = CompilescriptParams(
            expression=expression,
            source_u_r_l=source_u_r_l,
            persist_script=persist_script,
            execution_context_id=execution_context_id,
        )
        result = await self._cdp.call(
            "Runtime.compileScript", params.model_dump(by_alias=True, exclude_none=True)
        )
        return CompilescriptResult(**result)

    async def disable(self) -> None:
        """Disables reporting of execution contexts creation."""
        result = await self._cdp.call("Runtime.disable", {})
        return None

    async def discard_console_entries(self) -> None:
        """Discards collected exceptions and console API calls."""
        result = await self._cdp.call("Runtime.discardConsoleEntries", {})
        return None

    async def enable(self) -> None:
        """Enables reporting of execution contexts creation by means of `executionContextCreated` event.
        When the reporting gets enabled the event will be sent immediately for each existing execution
        context."""
        result = await self._cdp.call("Runtime.enable", {})
        return None

    async def evaluate(
        self,
        expression: str,
        object_group: str | None = None,
        include_command_line_a_p_i: bool | None = None,
        silent: bool | None = None,
        context_id: ExecutionContextId | None = None,
        return_by_value: bool | None = None,
        generate_preview: bool | None = None,
        user_gesture: bool | None = None,
        await_promise: bool | None = None,
        throw_on_side_effect: bool | None = None,
        timeout: TimeDelta | None = None,
        disable_breaks: bool | None = None,
        repl_mode: bool | None = None,
        allow_unsafe_eval_blocked_by_c_s_p: bool | None = None,
        unique_context_id: str | None = None,
        serialization_options: SerializationOptions | None = None,
    ) -> EvaluateResult:
        """Evaluates expression on global object."""
        params = EvaluateParams(
            expression=expression,
            object_group=object_group,
            include_command_line_a_p_i=include_command_line_a_p_i,
            silent=silent,
            context_id=context_id,
            return_by_value=return_by_value,
            generate_preview=generate_preview,
            user_gesture=user_gesture,
            await_promise=await_promise,
            throw_on_side_effect=throw_on_side_effect,
            timeout=timeout,
            disable_breaks=disable_breaks,
            repl_mode=repl_mode,
            allow_unsafe_eval_blocked_by_c_s_p=allow_unsafe_eval_blocked_by_c_s_p,
            unique_context_id=unique_context_id,
            serialization_options=serialization_options,
        )
        result = await self._cdp.call(
            "Runtime.evaluate", params.model_dump(by_alias=True, exclude_none=True)
        )
        return EvaluateResult(**result)

    async def get_isolate_id(self) -> GetisolateidResult:
        """Returns the isolate id."""
        result = await self._cdp.call("Runtime.getIsolateId", {})
        return GetisolateidResult(**result)

    async def get_heap_usage(self) -> GetheapusageResult:
        """Returns the JavaScript heap usage.
        It is the total usage of the corresponding isolate not scoped to a particular Runtime."""
        result = await self._cdp.call("Runtime.getHeapUsage", {})
        return GetheapusageResult(**result)

    async def get_properties(
        self,
        object_id: RemoteObjectId,
        own_properties: bool | None = None,
        accessor_properties_only: bool | None = None,
        generate_preview: bool | None = None,
        non_indexed_properties_only: bool | None = None,
    ) -> GetpropertiesResult:
        """Returns properties of a given object. Object group of the result is inherited from the target
        object."""
        params = GetpropertiesParams(
            object_id=object_id,
            own_properties=own_properties,
            accessor_properties_only=accessor_properties_only,
            generate_preview=generate_preview,
            non_indexed_properties_only=non_indexed_properties_only,
        )
        result = await self._cdp.call(
            "Runtime.getProperties", params.model_dump(by_alias=True, exclude_none=True)
        )
        return GetpropertiesResult(**result)

    async def global_lexical_scope_names(
        self, execution_context_id: ExecutionContextId | None = None
    ) -> GloballexicalscopenamesResult:
        """Returns all let, const and class variables from global scope."""
        params = GloballexicalscopenamesParams(
            execution_context_id=execution_context_id,
        )
        result = await self._cdp.call(
            "Runtime.globalLexicalScopeNames",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return GloballexicalscopenamesResult(**result)

    async def query_objects(
        self, prototype_object_id: RemoteObjectId, object_group: str | None = None
    ) -> QueryobjectsResult:
        params = QueryobjectsParams(
            prototype_object_id=prototype_object_id,
            object_group=object_group,
        )
        result = await self._cdp.call(
            "Runtime.queryObjects", params.model_dump(by_alias=True, exclude_none=True)
        )
        return QueryobjectsResult(**result)

    async def release_object(self, object_id: RemoteObjectId) -> None:
        """Releases remote object with given id."""
        params = ReleaseobjectParams(
            object_id=object_id,
        )
        result = await self._cdp.call(
            "Runtime.releaseObject", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def release_object_group(self, object_group: str) -> None:
        """Releases all remote objects that belong to a given group."""
        params = ReleaseobjectgroupParams(
            object_group=object_group,
        )
        result = await self._cdp.call(
            "Runtime.releaseObjectGroup",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def run_if_waiting_for_debugger(self) -> None:
        """Tells inspected instance to run if it was waiting for debugger to attach."""
        result = await self._cdp.call("Runtime.runIfWaitingForDebugger", {})
        return None

    async def run_script(
        self,
        script_id: ScriptId,
        execution_context_id: ExecutionContextId | None = None,
        object_group: str | None = None,
        silent: bool | None = None,
        include_command_line_a_p_i: bool | None = None,
        return_by_value: bool | None = None,
        generate_preview: bool | None = None,
        await_promise: bool | None = None,
    ) -> RunscriptResult:
        """Runs script with given id in a given context."""
        params = RunscriptParams(
            script_id=script_id,
            execution_context_id=execution_context_id,
            object_group=object_group,
            silent=silent,
            include_command_line_a_p_i=include_command_line_a_p_i,
            return_by_value=return_by_value,
            generate_preview=generate_preview,
            await_promise=await_promise,
        )
        result = await self._cdp.call(
            "Runtime.runScript", params.model_dump(by_alias=True, exclude_none=True)
        )
        return RunscriptResult(**result)

    async def set_async_call_stack_depth(self, max_depth: int) -> None:
        """Enables or disables async call stacks tracking."""
        params = SetasynccallstackdepthParams(
            max_depth=max_depth,
        )
        result = await self._cdp.call(
            "Runtime.setAsyncCallStackDepth",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def set_custom_object_formatter_enabled(self, enabled: bool) -> None:
        params = SetcustomobjectformatterenabledParams(
            enabled=enabled,
        )
        result = await self._cdp.call(
            "Runtime.setCustomObjectFormatterEnabled",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def set_max_call_stack_size_to_capture(self, size: int) -> None:
        params = SetmaxcallstacksizetocaptureParams(
            size=size,
        )
        result = await self._cdp.call(
            "Runtime.setMaxCallStackSizeToCapture",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def terminate_execution(self) -> None:
        """Terminate current or next JavaScript execution.
        Will cancel the termination when the outer-most script execution ends."""
        result = await self._cdp.call("Runtime.terminateExecution", {})
        return None

    async def add_binding(
        self,
        name: str,
        execution_context_id: ExecutionContextId | None = None,
        execution_context_name: str | None = None,
    ) -> None:
        """If executionContextId is empty, adds binding with the given name on the
        global objects of all inspected contexts, including those created later,
        bindings survive reloads.
        Binding function takes exactly one argument, this argument should be string,
        in case of any other input, function throws an exception.
        Each binding function call produces Runtime.bindingCalled notification."""
        params = AddbindingParams(
            name=name,
            execution_context_id=execution_context_id,
            execution_context_name=execution_context_name,
        )
        result = await self._cdp.call(
            "Runtime.addBinding", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def remove_binding(self, name: str) -> None:
        """This method does not remove binding function from global object but
        unsubscribes current runtime agent from Runtime.bindingCalled notifications."""
        params = RemovebindingParams(
            name=name,
        )
        result = await self._cdp.call(
            "Runtime.removeBinding", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def get_exception_details(
        self, error_object_id: RemoteObjectId
    ) -> GetexceptiondetailsResult:
        """This method tries to lookup and populate exception details for a
        JavaScript Error object.
        Note that the stackTrace portion of the resulting exceptionDetails will
        only be populated if the Runtime domain was enabled at the time when the
        Error was thrown."""
        params = GetexceptiondetailsParams(
            error_object_id=error_object_id,
        )
        result = await self._cdp.call(
            "Runtime.getExceptionDetails",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return GetexceptiondetailsResult(**result)
