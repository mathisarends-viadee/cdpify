import pytest

from cdpify.generator.generators.commands import CommandsGenerator
from cdpify.generator.models import Command, Domain, Parameter


@pytest.fixture
def commands_generator() -> CommandsGenerator:
    return CommandsGenerator()


@pytest.fixture
def empty_domain() -> Domain:
    return Domain(domain="TestDomain", commands=[])


@pytest.fixture
def domain_with_simple_command() -> Domain:
    command = Command(
        name="testCommand",
        description="A test command",
        parameters=[
            Parameter(name="value", type="string", optional=False),
        ],
        returns=[
            Parameter(name="result", type="boolean", optional=False),
        ],
    )
    return Domain(domain="TestDomain", commands=[command])


@pytest.fixture
def domain_with_command_no_params() -> Domain:
    command = Command(
        name="simpleCommand",
        parameters=[],
        returns=[],
    )
    return Domain(domain="TestDomain", commands=[command])


@pytest.fixture
def domain_with_optional_params() -> Domain:
    command = Command(
        name="flexibleCommand",
        parameters=[
            Parameter(name="required", type="string", optional=False),
            Parameter(name="optional", type="integer", optional=True),
        ],
        returns=[],
    )
    return Domain(domain="TestDomain", commands=[command])


@pytest.fixture
def domain_with_cross_domain_ref() -> Domain:
    command = Command(
        name="testCommand",
        parameters=[
            Parameter(name="nodeId", ref="dom.NodeId", optional=False),
        ],
        returns=[],
    )
    return Domain(domain="Network", commands=[command])


class TestCommandsGeneratorGenerate:
    def test_generate_with_empty_domain_contains_no_commands_comment(
        self, commands_generator: CommandsGenerator, empty_domain: Domain
    ) -> None:
        result = commands_generator.generate(empty_domain)
        assert "# No commands defined" in result

    def test_generate_with_simple_command_creates_params_model(
        self, commands_generator: CommandsGenerator, domain_with_simple_command: Domain
    ) -> None:
        result = commands_generator.generate(domain_with_simple_command)
        assert "class TestCommandParams(CDPModel):" in result
        assert "value: str" in result

    def test_generate_with_simple_command_creates_result_model(
        self, commands_generator: CommandsGenerator, domain_with_simple_command: Domain
    ) -> None:
        result = commands_generator.generate(domain_with_simple_command)
        assert "class TestCommandResult(CDPModel):" in result
        assert "result: bool" in result

    def test_generate_with_command_no_params_has_no_params_model(
        self,
        commands_generator: CommandsGenerator,
        domain_with_command_no_params: Domain,
    ) -> None:
        result = commands_generator.generate(domain_with_command_no_params)
        assert "SimpleCommandParams" not in result

    def test_generate_with_optional_params_adds_none_default(
        self, commands_generator: CommandsGenerator, domain_with_optional_params: Domain
    ) -> None:
        result = commands_generator.generate(domain_with_optional_params)
        assert "optional: int | None = None" in result

    def test_generate_with_required_params_has_no_default(
        self, commands_generator: CommandsGenerator, domain_with_optional_params: Domain
    ) -> None:
        result = commands_generator.generate(domain_with_optional_params)
        assert "required: str\n" in result or "required: str " in result

    def test_generate_includes_cdp_model_import(
        self, commands_generator: CommandsGenerator, domain_with_simple_command: Domain
    ) -> None:
        result = commands_generator.generate(domain_with_simple_command)
        assert "from cdpify.domains.base import CDPModel" in result

    def test_generate_with_cross_domain_ref_includes_import(
        self,
        commands_generator: CommandsGenerator,
        domain_with_cross_domain_ref: Domain,
    ) -> None:
        result = commands_generator.generate(domain_with_cross_domain_ref)
        assert "from cdpify.domains import dom" in result

    def test_generate_includes_header_comment(
        self, commands_generator: CommandsGenerator, domain_with_simple_command: Domain
    ) -> None:
        result = commands_generator.generate(domain_with_simple_command)
        assert "# AUTO-GENERATED" in result or "Generated" in result


class TestCommandsGeneratorModelCreation:
    def test_create_field_with_simple_type_returns_typed_field(
        self, commands_generator: CommandsGenerator
    ) -> None:
        param = Parameter(name="testValue", type="string", optional=False)
        result = commands_generator._create_field(param)
        assert result == "test_value: str"

    def test_create_field_with_optional_adds_none_default(
        self, commands_generator: CommandsGenerator
    ) -> None:
        param = Parameter(name="optionalValue", type="integer", optional=True)
        result = commands_generator._create_field(param)
        assert result == "optional_value: int | None = None"

    def test_create_field_with_ref_uses_ref_type(
        self, commands_generator: CommandsGenerator
    ) -> None:
        param = Parameter(name="nodeId", ref="NodeId", optional=False)
        result = commands_generator._create_field(param)
        assert result == "node_id: NodeId"

    def test_create_field_tracks_cross_domain_refs(
        self, commands_generator: CommandsGenerator
    ) -> None:
        commands_generator._reset_tracking()
        param = Parameter(name="frameId", ref="page.FrameId", optional=False)
        commands_generator._create_field(param)
        assert "page.FrameId" in commands_generator._cross_domain_refs
