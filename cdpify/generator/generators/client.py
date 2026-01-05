from cdpify.generator.generators.base import BaseGenerator
from cdpify.generator.generators.utils import (
    map_cdp_type,
    to_pascal_case,
    to_snake_case,
)
from cdpify.generator.models import Command, Domain, Parameter


class ClientGenerator(BaseGenerator):
    def generate(self, domain: Domain) -> str:
        self._reset_tracking()

        sections = [
            self._header(),
            self._imports(domain),
            self._client_class(domain),
        ]

        return "\n\n".join(sections)

    def _imports(self, domain: Domain) -> str:
        lines = [
            "from __future__ import annotations",
            "",
            "from typing import TYPE_CHECKING, Any, Literal",
            "",
            "if TYPE_CHECKING:",
            "    from cdpify.client import CDPClient",
            "",
        ]

        if domain.commands:
            lines.extend(self._build_command_imports(domain))
            self._pre_scan_for_types(domain)
            lines.extend(self._build_type_imports(domain))

            if self._cross_domain_refs:
                lines.append(self._cross_domain_imports())

        return "\n".join(lines)

    def _build_command_imports(self, domain: Domain) -> list[str]:
        param_classes = {
            f"{to_pascal_case(cmd.name)}Params"
            for cmd in domain.commands
            if cmd.parameters
        }
        return_classes = {
            f"{to_pascal_case(cmd.name)}Result"
            for cmd in domain.commands
            if cmd.returns
        }

        all_classes = sorted(param_classes | return_classes)
        if not all_classes:
            return []

        lines = ["from .commands import ("]
        for cls in all_classes:
            lines.append(f"    {cls},")
        lines.append(")")
        lines.append("")

        return lines

    def _build_type_imports(self, domain: Domain) -> list[str]:
        type_imports = self._collect_type_imports(domain)
        if not type_imports:
            return []

        lines = ["from .types import ("]
        for type_name in sorted(type_imports):
            lines.append(f"    {type_name},")
        lines.append(")")
        lines.append("")

        return lines

    def _pre_scan_for_types(self, domain: Domain) -> None:
        for command in domain.commands:
            if not command.parameters:
                continue

            for param in command.parameters:
                param_type = map_cdp_type(param)
                self._track_type_usage(param_type)

    def _cross_domain_imports(self) -> str:
        return self._build_cross_domain_imports(use_type_checking=False)

    def _collect_type_imports(self, domain: Domain) -> set[str]:
        type_imports = set()

        for command in domain.commands:
            if not command.parameters:
                continue

            for param in command.parameters:
                self._add_direct_type_reference(param, type_imports)
                self._add_array_item_reference(param, type_imports)

        return type_imports

    def _add_direct_type_reference(
        self, param: Parameter, type_imports: set[str]
    ) -> None:
        if not param.ref or "." in param.ref:
            return
        type_imports.add(param.ref)

    def _add_array_item_reference(
        self, param: Parameter, type_imports: set[str]
    ) -> None:
        if param.type != "array" or not param.items:
            return

        ref = param.items.get("$ref")
        if ref and "." not in ref:
            type_imports.add(ref)

    def _client_class(self, domain: Domain) -> str:
        class_name = f"{domain.domain}Client"

        lines = [f"class {class_name}:"]
        lines.append("    def __init__(self, client: CDPClient) -> None:")
        lines.append("        self._client = client")

        for command in domain.commands:
            lines.append("")
            lines.append(self._generate_method(command, domain.domain))

        return "\n".join(lines)

    def _generate_method(self, command: Command, domain_name: str) -> str:
        method_name = to_snake_case(command.name)
        cdp_method = f"{domain_name}.{command.name}"

        params = self._build_params(command)
        return_type = self._get_return_type(command)
        method_body = self._build_method_body(command, cdp_method)

        lines = [f"    async def {method_name}("]

        for param in params:
            lines.append(f"        {param},")

        lines.append(f"    ) -> {return_type}:")
        lines.extend(f"        {line}" for line in method_body)

        return "\n".join(lines)

    def _build_params(self, command: Command) -> list[str]:
        params = ["self"]

        if not command.parameters:
            params.append("session_id: str | None = None")
            return params

        params.append("*")

        for param in command.parameters:
            param_signature = self._build_param_signature(command, param)
            params.append(param_signature)

        params.append("session_id: str | None = None")
        return params

    def _build_param_signature(self, command: Command, param) -> str:
        param_name = self._resolve_param_name(command, param)
        base_type = self._resolve_base_param_type(param)

        if param.optional:
            return f"{param_name}: {base_type} | None = None"
        return f"{param_name}: {base_type}"

    def _resolve_param_name(self, command: Command, param: Parameter) -> str:
        param_name = to_snake_case(param.name)

        if param_name == "session_id":
            return f"{to_snake_case(command.name)}_session_id"

        return param_name

    def _resolve_base_param_type(self, param) -> str:
        param_type = map_cdp_type(param)
        self._track_type_usage(param_type)
        return param_type.removesuffix(" | None")

    def _build_method_body(self, command: Command, cdp_method: str) -> list[str]:
        lines = []

        if command.parameters:
            lines.extend(self._build_params_construction(command))
            lines.append("")
            lines.extend(self._build_send_with_params(cdp_method))
        else:
            lines.extend(self._build_send_without_params(cdp_method))

        lines.extend(self._build_return_statement(command))
        return lines

    def _build_params_construction(self, command: Command) -> list[str]:
        param_class = f"{to_pascal_case(command.name)}Params"
        param_mapping = self._build_param_name_mapping(command)

        constructor_args = ", ".join(
            f"{cdp_name}={kwarg_name}" for cdp_name, kwarg_name in param_mapping.items()
        )

        return [f"params = {param_class}({constructor_args})"]

    def _build_param_name_mapping(self, command: Command) -> dict[str, str]:
        return {
            param.name: self._resolve_param_name(command, param)
            for param in command.parameters
        }

    def _build_send_with_params(self, cdp_method: str) -> list[str]:
        return [
            "result = await self._client.send_raw(",
            f'    method="{cdp_method}",',
            "    params=params.to_cdp_params(),",
            "    session_id=session_id,",
            ")",
        ]

    def _build_send_without_params(self, cdp_method: str) -> list[str]:
        return [
            "result = await self._client.send_raw(",
            f'    method="{cdp_method}",',
            "    params=None,",
            "    session_id=session_id,",
            ")",
        ]

    def _build_return_statement(self, command: Command) -> list[str]:
        if command.returns:
            result_class = f"{to_pascal_case(command.name)}Result"
            return [f"return {result_class}.model_validate(result)"]
        return ["return result"]

    def _get_return_type(self, command: Command) -> str:
        if command.returns:
            return f"{to_pascal_case(command.name)}Result"
        return "dict[str, Any]"
