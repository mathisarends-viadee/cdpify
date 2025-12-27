from pydantic_cpd.generator.models import Parameter


_BASIC_TYPE_MAPPING = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
    "object": "dict[str, Any]",
    "any": "Any",
}


def _get_array_item_type(item_spec: dict) -> str:
    if "$ref" in item_spec:
        return item_spec["$ref"]

    if "type" in item_spec:
        return _BASIC_TYPE_MAPPING.get(item_spec["type"], "Any")

    return "Any"


def _create_enum_literal(enum_values: list[str]) -> str:
    quoted_values = ", ".join(f'"{value}"' for value in enum_values)
    return f"Literal[{quoted_values}]"


def _create_array_type(items: dict | None) -> str:
    if not items:
        return "list[Any]"

    item_type = _get_array_item_type(items)
    return f"list[{item_type}]"


def _get_base_type(param: Parameter) -> str:
    if param.ref:
        return param.ref

    if param.type in _BASIC_TYPE_MAPPING:
        return _BASIC_TYPE_MAPPING[param.type]

    if param.type == "array":
        return _create_array_type(param.items)

    return "Any"


def _make_optional(type_annotation: str) -> str:
    return f"{type_annotation} | None"


def map_cdp_type(param: Parameter) -> str:
    base_type = _get_base_type(param)

    if param.enum:
        base_type = _create_enum_literal(param.enum)

    if param.optional:
        return _make_optional(base_type)

    return base_type


def to_snake_case(name: str) -> str:
    chars = []
    for i, char in enumerate(name):
        if char.isupper() and i > 0:
            chars.append("_")
        chars.append(char.lower())
    return "".join(chars)
