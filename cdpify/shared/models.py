import re
import sys
from dataclasses import asdict, dataclass, fields, is_dataclass
from typing import Any, ClassVar, Self, get_args, get_origin, get_type_hints


@dataclass
class CDPModel:
    _ACRONYMS: ClassVar[frozenset[str]] = frozenset(
        {
            "api",
            "css",
            "dom",
            "html",
            "json",
            "pdf",
            "spc",
            "ssl",
            "url",
            "uuid",
            "xml",
            "xhr",
            "ax",
            "cpu",
            "gpu",
            "io",
            "js",
            "os",
            "ui",
            "uri",
            "usb",
            "wasm",
            "http",
            "https",
        }
    )

    def to_cdp_params(self) -> dict[str, Any]:
        return {self._to_camel(k): v for k, v in asdict(self).items() if v is not None}

    @classmethod
    def from_cdp(cls, data: dict) -> Self:
        snake_data = {cls._to_snake(k): v for k, v in data.items()}
        resolved_types = cls._resolve_field_types()

        converted = {}
        for field_name, value in snake_data.items():
            if field_name not in resolved_types:
                continue

            field_type = resolved_types[field_name]
            if field_type is Any:
                converted[field_name] = value
            else:
                converted[field_name] = cls._deserialize_field(value, field_type)

        return cls(**converted)

    @classmethod
    def _resolve_field_types(cls) -> dict[str, Any]:
        """
        Resolve type hints field by field, falling back to Any for unresolvable types.
        """
        try:
            return get_type_hints(cls)
        except Exception:
            pass

        # Fallback: resolve each annotation individually
        module = sys.modules.get(cls.__module__)
        globalns = getattr(module, "__dict__", {}) if module else {}

        resolved = {}
        for f in fields(cls):
            annotation = cls.__annotations__.get(f.name, f.type)

            if not isinstance(annotation, str):
                resolved[f.name] = annotation
                continue

            try:
                resolved[f.name] = eval(annotation, globalns)
            except Exception:
                resolved[f.name] = Any

        return resolved

    @classmethod
    def _to_camel(cls, s: str) -> str:
        parts = s.split("_")

        if not parts:
            return s

        result = [parts[0].lower()]

        for part in parts[1:]:
            lower = part.lower()
            result.append(part.upper() if lower in cls._ACRONYMS else part.capitalize())

        return "".join(result)

    @classmethod
    def _to_snake(cls, s: str) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()

    @classmethod
    def _deserialize_field(cls, value: Any, field_type: type) -> Any:
        if value is None:
            return None

        origin = get_origin(field_type)
        args = get_args(field_type)

        if args and type(None) in args:
            non_none_types = [arg for arg in args if arg is not type(None)]
            if len(non_none_types) == 1:
                return cls._deserialize_field(value, non_none_types[0])

        if origin is list and args:
            item_type = args[0]
            return [cls._deserialize_field(item, item_type) for item in value]

        if isinstance(value, dict) and cls._is_cdp_model(field_type):
            return field_type.from_cdp(value)

        return value

    @staticmethod
    def _is_cdp_model(field_type: type) -> bool:
        try:
            return is_dataclass(field_type) and issubclass(field_type, CDPModel)
        except TypeError:
            return False
