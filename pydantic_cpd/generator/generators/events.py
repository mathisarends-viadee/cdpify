from pydantic_cpd.generator.generators.base import BaseGenerator
from pydantic_cpd.generator.generators.utils import (
    format_docstring,
    map_cdp_type,
    to_pascal_case,
    to_snake_case,
)
from pydantic_cpd.generator.models import Domain, Event, Parameter


class EventsGenerator(BaseGenerator):
    def generate(self, domain: Domain) -> str:
        self._reset_tracking()

        event_enum = self._generate_event_enum(domain)
        event_models = self._generate_event_models(domain)

        sections = [
            self._header(),
            self._imports(bool(event_models)),
        ]

        if self._cross_domain_refs:
            sections.append(self._cross_domain_imports())

        if event_enum:
            sections.append(event_enum)

        sections.append(event_models if event_models else "# No events defined")

        return "\n\n".join(sections)

    def _imports(self, has_models: bool) -> str:
        lines = []

        typing_imports = self._build_typing_imports()
        if typing_imports:
            lines.append(typing_imports)

        lines.append("from enum import StrEnum")
        lines.append("from pydantic_cpd.cdp.base import CDPModel")

        if has_models:
            lines.append("")
            lines.append("from .types import *")

        return "\n".join(lines)

    def _cross_domain_imports(self) -> str:
        return self._build_cross_domain_imports(use_type_checking=True)

    def _generate_event_enum(self, domain: Domain) -> str:
        if not domain.events:
            return ""

        class_name = f"{domain.domain}Event"
        lines = [f"class {class_name}(StrEnum):"]

        for event in domain.events:
            enum_name = self._to_enum_name(event.name)
            event_value = f"{domain.domain}.{event.name}"
            lines.append(f'    {enum_name} = "{event_value}"')

        return "\n".join(lines)

    def _to_enum_name(self, name: str) -> str:
        snake = to_snake_case(name)
        return snake.upper()

    def _generate_event_models(self, domain: Domain) -> str:
        if not domain.events:
            return ""

        return "\n\n".join(self._create_event_model(event) for event in domain.events)

    def _create_event_model(self, event: Event) -> str:
        class_name = f"{to_pascal_case(event.name)}Event"

        lines = [f"class {class_name}(CDPModel):"]

        if event.description:
            doc = format_docstring(event.description, indent=4)
            lines.extend(doc.rstrip().splitlines())

        if event.parameters:
            for param in event.parameters:
                lines.append(f"    {self._create_field(param)}")
        else:
            lines.append("    pass")

        return "\n".join(lines)

    def _create_field(self, param: Parameter) -> str:
        field_name = to_snake_case(param.name)
        py_type = self._resolve_type(param)

        if param.ref and "." in param.ref:
            self._cross_domain_refs.add(param.ref)

        self._track_type_usage(py_type)

        return f"{field_name}: {py_type}" + (" = None" if param.optional else "")

    def _resolve_type(self, param: Parameter) -> str:
        if param.ref and "." in param.ref:
            parts = param.ref.split(".")
            domain_lower = parts[0].lower()
            type_name = parts[1]
            base_type = f"{domain_lower}.{type_name}"
        else:
            base_type = map_cdp_type(param)

        if param.optional and " | None" not in base_type:
            return f"{base_type} | None"

        return base_type
