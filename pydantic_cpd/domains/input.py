"""Generated from CDP specification"""

from pydantic import BaseModel, Field
from typing import Literal, Any

# Domain Types


class TouchPoint(BaseModel):
    x: float
    y: float
    radius_x: float | None = None
    radius_y: float | None = None
    rotation_angle: float | None = None
    force: float | None = None
    tangential_pressure: float | None = None
    tilt_x: float | None = None
    tilt_y: float | None = None
    twist: int | None = None
    id: float | None = None


GestureSourceType = Literal["default", "touch", "mouse"]
MouseButton = Literal["none", "left", "middle", "right", "back", "forward"]
TimeSinceEpoch = float


class DragDataItem(BaseModel):
    mime_type: str
    data: str
    title: str | None = None
    base_u_r_l: str | None = None


class DragData(BaseModel):
    items: list[DragDataItem]
    files: list[str] | None = None
    drag_operations_mask: int


# Command Parameters and Results


class DispatchdrageventParams(BaseModel):
    """Dispatches a drag event into the page."""

    type: Literal["dragEnter", "dragOver", "drop", "dragCancel"] = Field(alias="type")
    x: float = Field(alias="x")
    y: float = Field(alias="y")
    data: DragData = Field(alias="data")
    modifiers: int | None = Field(default=None, alias="modifiers")


class DispatchkeyeventParams(BaseModel):
    """Dispatches a key event to the page."""

    type: Literal["keyDown", "keyUp", "rawKeyDown", "char"] = Field(alias="type")
    modifiers: int | None = Field(default=None, alias="modifiers")
    timestamp: TimeSinceEpoch | None = Field(default=None, alias="timestamp")
    text: str | None = Field(default=None, alias="text")
    unmodified_text: str | None = Field(default=None, alias="unmodifiedText")
    key_identifier: str | None = Field(default=None, alias="keyIdentifier")
    code: str | None = Field(default=None, alias="code")
    key: str | None = Field(default=None, alias="key")
    windows_virtual_key_code: int | None = Field(
        default=None, alias="windowsVirtualKeyCode"
    )
    native_virtual_key_code: int | None = Field(
        default=None, alias="nativeVirtualKeyCode"
    )
    auto_repeat: bool | None = Field(default=None, alias="autoRepeat")
    is_keypad: bool | None = Field(default=None, alias="isKeypad")
    is_system_key: bool | None = Field(default=None, alias="isSystemKey")
    location: int | None = Field(default=None, alias="location")
    commands: list[str] | None = Field(default=None, alias="commands")


class InserttextParams(BaseModel):
    """This method emulates inserting text that doesn't come from a key press,
    for example an emoji keyboard or an IME."""

    text: str = Field(alias="text")


class ImesetcompositionParams(BaseModel):
    """This method sets the current candidate text for IME.
    Use imeCommitComposition to commit the final text.
    Use imeSetComposition with empty string as text to cancel composition."""

    text: str = Field(alias="text")
    selection_start: int = Field(alias="selectionStart")
    selection_end: int = Field(alias="selectionEnd")
    replacement_start: int | None = Field(default=None, alias="replacementStart")
    replacement_end: int | None = Field(default=None, alias="replacementEnd")


class DispatchmouseeventParams(BaseModel):
    """Dispatches a mouse event to the page."""

    type: Literal["mousePressed", "mouseReleased", "mouseMoved", "mouseWheel"] = Field(
        alias="type"
    )
    x: float = Field(alias="x")
    y: float = Field(alias="y")
    modifiers: int | None = Field(default=None, alias="modifiers")
    timestamp: TimeSinceEpoch | None = Field(default=None, alias="timestamp")
    button: MouseButton | None = Field(default=None, alias="button")
    buttons: int | None = Field(default=None, alias="buttons")
    click_count: int | None = Field(default=None, alias="clickCount")
    force: float | None = Field(default=None, alias="force")
    tangential_pressure: float | None = Field(default=None, alias="tangentialPressure")
    tilt_x: float | None = Field(default=None, alias="tiltX")
    tilt_y: float | None = Field(default=None, alias="tiltY")
    twist: int | None = Field(default=None, alias="twist")
    delta_x: float | None = Field(default=None, alias="deltaX")
    delta_y: float | None = Field(default=None, alias="deltaY")
    pointer_type: Literal["mouse", "pen"] | None = Field(
        default=None, alias="pointerType"
    )


class DispatchtoucheventParams(BaseModel):
    """Dispatches a touch event to the page."""

    type: Literal["touchStart", "touchEnd", "touchMove", "touchCancel"] = Field(
        alias="type"
    )
    touch_points: list[TouchPoint] = Field(alias="touchPoints")
    modifiers: int | None = Field(default=None, alias="modifiers")
    timestamp: TimeSinceEpoch | None = Field(default=None, alias="timestamp")


class EmulatetouchfrommouseeventParams(BaseModel):
    """Emulates touch event from the mouse event parameters."""

    type: Literal["mousePressed", "mouseReleased", "mouseMoved", "mouseWheel"] = Field(
        alias="type"
    )
    x: int = Field(alias="x")
    y: int = Field(alias="y")
    button: MouseButton = Field(alias="button")
    timestamp: TimeSinceEpoch | None = Field(default=None, alias="timestamp")
    delta_x: float | None = Field(default=None, alias="deltaX")
    delta_y: float | None = Field(default=None, alias="deltaY")
    modifiers: int | None = Field(default=None, alias="modifiers")
    click_count: int | None = Field(default=None, alias="clickCount")


class SetignoreinputeventsParams(BaseModel):
    """Ignores input events (useful while auditing page)."""

    ignore: bool = Field(alias="ignore")


class SetinterceptdragsParams(BaseModel):
    """Prevents default drag and drop behavior and instead emits `Input.dragIntercepted` events.
    Drag and drop behavior can be directly controlled via `Input.dispatchDragEvent`."""

    enabled: bool = Field(alias="enabled")


class SynthesizepinchgestureParams(BaseModel):
    """Synthesizes a pinch gesture over a time period by issuing appropriate touch events."""

    x: float = Field(alias="x")
    y: float = Field(alias="y")
    scale_factor: float = Field(alias="scaleFactor")
    relative_speed: int | None = Field(default=None, alias="relativeSpeed")
    gesture_source_type: GestureSourceType | None = Field(
        default=None, alias="gestureSourceType"
    )


class SynthesizescrollgestureParams(BaseModel):
    """Synthesizes a scroll gesture over a time period by issuing appropriate touch events."""

    x: float = Field(alias="x")
    y: float = Field(alias="y")
    x_distance: float | None = Field(default=None, alias="xDistance")
    y_distance: float | None = Field(default=None, alias="yDistance")
    x_overscroll: float | None = Field(default=None, alias="xOverscroll")
    y_overscroll: float | None = Field(default=None, alias="yOverscroll")
    prevent_fling: bool | None = Field(default=None, alias="preventFling")
    speed: int | None = Field(default=None, alias="speed")
    gesture_source_type: GestureSourceType | None = Field(
        default=None, alias="gestureSourceType"
    )
    repeat_count: int | None = Field(default=None, alias="repeatCount")
    repeat_delay_ms: int | None = Field(default=None, alias="repeatDelayMs")
    interaction_marker_name: str | None = Field(
        default=None, alias="interactionMarkerName"
    )


class SynthesizetapgestureParams(BaseModel):
    """Synthesizes a tap gesture over a time period by issuing appropriate touch events."""

    x: float = Field(alias="x")
    y: float = Field(alias="y")
    duration: int | None = Field(default=None, alias="duration")
    tap_count: int | None = Field(default=None, alias="tapCount")
    gesture_source_type: GestureSourceType | None = Field(
        default=None, alias="gestureSourceType"
    )


# Client


class InputClient:
    """Input domain client"""

    def __init__(self, cdp_client: Any) -> None:
        self._cdp = cdp_client

    async def dispatch_drag_event(
        self,
        type: Literal["dragEnter", "dragOver", "drop", "dragCancel"],
        x: float,
        y: float,
        data: DragData,
        modifiers: int | None = None,
    ) -> None:
        """Dispatches a drag event into the page."""
        params = DispatchdrageventParams(
            type=type,
            x=x,
            y=y,
            data=data,
            modifiers=modifiers,
        )
        result = await self._cdp.call(
            "Input.dispatchDragEvent",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def dispatch_key_event(
        self,
        type: Literal["keyDown", "keyUp", "rawKeyDown", "char"],
        modifiers: int | None = None,
        timestamp: TimeSinceEpoch | None = None,
        text: str | None = None,
        unmodified_text: str | None = None,
        key_identifier: str | None = None,
        code: str | None = None,
        key: str | None = None,
        windows_virtual_key_code: int | None = None,
        native_virtual_key_code: int | None = None,
        auto_repeat: bool | None = None,
        is_keypad: bool | None = None,
        is_system_key: bool | None = None,
        location: int | None = None,
        commands: list[str] | None = None,
    ) -> None:
        """Dispatches a key event to the page."""
        params = DispatchkeyeventParams(
            type=type,
            modifiers=modifiers,
            timestamp=timestamp,
            text=text,
            unmodified_text=unmodified_text,
            key_identifier=key_identifier,
            code=code,
            key=key,
            windows_virtual_key_code=windows_virtual_key_code,
            native_virtual_key_code=native_virtual_key_code,
            auto_repeat=auto_repeat,
            is_keypad=is_keypad,
            is_system_key=is_system_key,
            location=location,
            commands=commands,
        )
        result = await self._cdp.call(
            "Input.dispatchKeyEvent",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def insert_text(self, text: str) -> None:
        """This method emulates inserting text that doesn't come from a key press,
        for example an emoji keyboard or an IME."""
        params = InserttextParams(
            text=text,
        )
        result = await self._cdp.call(
            "Input.insertText", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def ime_set_composition(
        self,
        text: str,
        selection_start: int,
        selection_end: int,
        replacement_start: int | None = None,
        replacement_end: int | None = None,
    ) -> None:
        """This method sets the current candidate text for IME.
        Use imeCommitComposition to commit the final text.
        Use imeSetComposition with empty string as text to cancel composition."""
        params = ImesetcompositionParams(
            text=text,
            selection_start=selection_start,
            selection_end=selection_end,
            replacement_start=replacement_start,
            replacement_end=replacement_end,
        )
        result = await self._cdp.call(
            "Input.imeSetComposition",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def dispatch_mouse_event(
        self,
        type: Literal["mousePressed", "mouseReleased", "mouseMoved", "mouseWheel"],
        x: float,
        y: float,
        modifiers: int | None = None,
        timestamp: TimeSinceEpoch | None = None,
        button: MouseButton | None = None,
        buttons: int | None = None,
        click_count: int | None = None,
        force: float | None = None,
        tangential_pressure: float | None = None,
        tilt_x: float | None = None,
        tilt_y: float | None = None,
        twist: int | None = None,
        delta_x: float | None = None,
        delta_y: float | None = None,
        pointer_type: Literal["mouse", "pen"] | None = None,
    ) -> None:
        """Dispatches a mouse event to the page."""
        params = DispatchmouseeventParams(
            type=type,
            x=x,
            y=y,
            modifiers=modifiers,
            timestamp=timestamp,
            button=button,
            buttons=buttons,
            click_count=click_count,
            force=force,
            tangential_pressure=tangential_pressure,
            tilt_x=tilt_x,
            tilt_y=tilt_y,
            twist=twist,
            delta_x=delta_x,
            delta_y=delta_y,
            pointer_type=pointer_type,
        )
        result = await self._cdp.call(
            "Input.dispatchMouseEvent",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def dispatch_touch_event(
        self,
        type: Literal["touchStart", "touchEnd", "touchMove", "touchCancel"],
        touch_points: list[TouchPoint],
        modifiers: int | None = None,
        timestamp: TimeSinceEpoch | None = None,
    ) -> None:
        """Dispatches a touch event to the page."""
        params = DispatchtoucheventParams(
            type=type,
            touch_points=touch_points,
            modifiers=modifiers,
            timestamp=timestamp,
        )
        result = await self._cdp.call(
            "Input.dispatchTouchEvent",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def cancel_dragging(self) -> None:
        """Cancels any active dragging in the page."""
        result = await self._cdp.call("Input.cancelDragging", {})
        return None

    async def emulate_touch_from_mouse_event(
        self,
        type: Literal["mousePressed", "mouseReleased", "mouseMoved", "mouseWheel"],
        x: int,
        y: int,
        button: MouseButton,
        timestamp: TimeSinceEpoch | None = None,
        delta_x: float | None = None,
        delta_y: float | None = None,
        modifiers: int | None = None,
        click_count: int | None = None,
    ) -> None:
        """Emulates touch event from the mouse event parameters."""
        params = EmulatetouchfrommouseeventParams(
            type=type,
            x=x,
            y=y,
            button=button,
            timestamp=timestamp,
            delta_x=delta_x,
            delta_y=delta_y,
            modifiers=modifiers,
            click_count=click_count,
        )
        result = await self._cdp.call(
            "Input.emulateTouchFromMouseEvent",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def set_ignore_input_events(self, ignore: bool) -> None:
        """Ignores input events (useful while auditing page)."""
        params = SetignoreinputeventsParams(
            ignore=ignore,
        )
        result = await self._cdp.call(
            "Input.setIgnoreInputEvents",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def set_intercept_drags(self, enabled: bool) -> None:
        """Prevents default drag and drop behavior and instead emits `Input.dragIntercepted` events.
        Drag and drop behavior can be directly controlled via `Input.dispatchDragEvent`."""
        params = SetinterceptdragsParams(
            enabled=enabled,
        )
        result = await self._cdp.call(
            "Input.setInterceptDrags",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def synthesize_pinch_gesture(
        self,
        x: float,
        y: float,
        scale_factor: float,
        relative_speed: int | None = None,
        gesture_source_type: GestureSourceType | None = None,
    ) -> None:
        """Synthesizes a pinch gesture over a time period by issuing appropriate touch events."""
        params = SynthesizepinchgestureParams(
            x=x,
            y=y,
            scale_factor=scale_factor,
            relative_speed=relative_speed,
            gesture_source_type=gesture_source_type,
        )
        result = await self._cdp.call(
            "Input.synthesizePinchGesture",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def synthesize_scroll_gesture(
        self,
        x: float,
        y: float,
        x_distance: float | None = None,
        y_distance: float | None = None,
        x_overscroll: float | None = None,
        y_overscroll: float | None = None,
        prevent_fling: bool | None = None,
        speed: int | None = None,
        gesture_source_type: GestureSourceType | None = None,
        repeat_count: int | None = None,
        repeat_delay_ms: int | None = None,
        interaction_marker_name: str | None = None,
    ) -> None:
        """Synthesizes a scroll gesture over a time period by issuing appropriate touch events."""
        params = SynthesizescrollgestureParams(
            x=x,
            y=y,
            x_distance=x_distance,
            y_distance=y_distance,
            x_overscroll=x_overscroll,
            y_overscroll=y_overscroll,
            prevent_fling=prevent_fling,
            speed=speed,
            gesture_source_type=gesture_source_type,
            repeat_count=repeat_count,
            repeat_delay_ms=repeat_delay_ms,
            interaction_marker_name=interaction_marker_name,
        )
        result = await self._cdp.call(
            "Input.synthesizeScrollGesture",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def synthesize_tap_gesture(
        self,
        x: float,
        y: float,
        duration: int | None = None,
        tap_count: int | None = None,
        gesture_source_type: GestureSourceType | None = None,
    ) -> None:
        """Synthesizes a tap gesture over a time period by issuing appropriate touch events."""
        params = SynthesizetapgestureParams(
            x=x,
            y=y,
            duration=duration,
            tap_count=tap_count,
            gesture_source_type=gesture_source_type,
        )
        result = await self._cdp.call(
            "Input.synthesizeTapGesture",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None
