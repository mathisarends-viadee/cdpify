import pytest

from pydantic_cpd.generator.generators.client import ClientGenerator
from pydantic_cpd.generator.models import Command, Domain, Parameter


@pytest.fixture
def client_generator() -> ClientGenerator:
    return ClientGenerator()


@pytest.fixture
def empty_domain() -> Domain:
    return Domain(domain="TestDomain", commands=[])


@pytest.fixture
def domain_with_simple_command() -> Domain:
    command = Command(
        name="testCommand",
        parameters=[
            Parameter(name="value", type="string", optional=False),
        ],
        returns=[
            Parameter(name="success", type="boolean", optional=False),
        ],
    )
    return Domain(domain="TestDomain", commands=[command])


@pytest.fixture
def domain_with_no_param_command() -> Domain:
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


class TestClientGeneratorGenerate:
    def test_generate_creates_client_class(
        self, client_generator: ClientGenerator, domain_with_simple_command: Domain
    ) -> None:
        result = client_generator.generate(domain_with_simple_command)
        assert "class TestDomainClient:" in result

    def test_generate_includes_init_method(
        self, client_generator: ClientGenerator, domain_with_simple_command: Domain
    ) -> None:
        result = client_generator.generate(domain_with_simple_command)
        assert "def __init__(self, client: CDPClient) -> None:" in result
        assert "self._client = client" in result

    def test_generate_creates_async_method_for_command(
        self, client_generator: ClientGenerator, domain_with_simple_command: Domain
    ) -> None:
        result = client_generator.generate(domain_with_simple_command)
        assert "async def test_command(" in result

    def test_generate_includes_cdp_client_type_checking_import(
        self, client_generator: ClientGenerator, domain_with_simple_command: Domain
    ) -> None:
        result = client_generator.generate(domain_with_simple_command)
        assert "if TYPE_CHECKING:" in result
        assert "from pydantic_cpd.client import CDPClient" in result

    def test_generate_with_command_params_imports_params_model(
        self, client_generator: ClientGenerator, domain_with_simple_command: Domain
    ) -> None:
        result = client_generator.generate(domain_with_simple_command)
        assert "from .commands import (" in result
        assert "TestCommandParams" in result

    def test_generate_with_command_returns_imports_result_model(
        self, client_generator: ClientGenerator, domain_with_simple_command: Domain
    ) -> None:
        result = client_generator.generate(domain_with_simple_command)
        assert "TestCommandResult" in result


class TestClientGeneratorMethodGeneration:
    def test_generate_method_with_params_includes_parameter_list(
        self, client_generator: ClientGenerator, domain_with_simple_command: Domain
    ) -> None:
        result = client_generator.generate(domain_with_simple_command)
        assert "value: str," in result

    def test_generate_method_with_optional_params_adds_none_default(
        self, client_generator: ClientGenerator, domain_with_optional_params: Domain
    ) -> None:
        result = client_generator.generate(domain_with_optional_params)
        assert "optional: int | None = None," in result

    def test_generate_method_always_includes_session_id_param(
        self, client_generator: ClientGenerator, domain_with_no_param_command: Domain
    ) -> None:
        result = client_generator.generate(domain_with_no_param_command)
        assert "session_id: str | None = None" in result

    def test_generate_method_with_params_creates_params_object(
        self, client_generator: ClientGenerator, domain_with_simple_command: Domain
    ) -> None:
        result = client_generator.generate(domain_with_simple_command)
        assert "params = TestCommandParams(value=value)" in result

    def test_generate_method_calls_send_raw_with_method_name(
        self, client_generator: ClientGenerator, domain_with_simple_command: Domain
    ) -> None:
        result = client_generator.generate(domain_with_simple_command)
        assert 'method="TestDomain.testCommand"' in result

    def test_generate_method_with_params_sends_params_dict(
        self, client_generator: ClientGenerator, domain_with_simple_command: Domain
    ) -> None:
        result = client_generator.generate(domain_with_simple_command)
        assert "params=params.to_cdp_params()" in result

    def test_generate_method_without_params_sends_none(
        self, client_generator: ClientGenerator, domain_with_no_param_command: Domain
    ) -> None:
        result = client_generator.generate(domain_with_no_param_command)
        assert "params=None" in result

    def test_generate_method_with_returns_validates_result(
        self, client_generator: ClientGenerator, domain_with_simple_command: Domain
    ) -> None:
        result = client_generator.generate(domain_with_simple_command)
        assert "return TestCommandResult.model_validate(result)" in result

    def test_generate_method_without_returns_returns_raw_dict(
        self, client_generator: ClientGenerator, domain_with_no_param_command: Domain
    ) -> None:
        result = client_generator.generate(domain_with_no_param_command)
        assert "return result" in result

    def test_generate_method_with_returns_has_result_return_type(
        self, client_generator: ClientGenerator, domain_with_simple_command: Domain
    ) -> None:
        result = client_generator.generate(domain_with_simple_command)
        assert ") -> TestCommandResult:" in result

    def test_generate_method_without_returns_has_dict_return_type(
        self, client_generator: ClientGenerator, domain_with_no_param_command: Domain
    ) -> None:
        result = client_generator.generate(domain_with_no_param_command)
        assert ") -> dict[str, Any]:" in result


class TestClientGeneratorParameterHandling:
    def test_resolve_param_name_converts_to_snake_case(
        self, client_generator: ClientGenerator
    ) -> None:
        command = Command(name="test", parameters=[], returns=[])
        param = Parameter(name="myValue", type="string", optional=False)
        result = client_generator._resolve_param_name(command, param)
        assert result == "my_value"

    def test_resolve_param_name_renames_session_id_conflict(
        self, client_generator: ClientGenerator
    ) -> None:
        command = Command(name="testCommand", parameters=[], returns=[])
        param = Parameter(name="sessionId", type="string", optional=False)
        result = client_generator._resolve_param_name(command, param)
        assert result == "test_command_session_id"

    def test_build_params_includes_self_first(
        self, client_generator: ClientGenerator
    ) -> None:
        command = Command(name="test", parameters=[], returns=[])
        result = client_generator._build_params(command)
        assert result[0] == "self"

    def test_build_params_with_parameters_includes_asterisk(
        self, client_generator: ClientGenerator
    ) -> None:
        command = Command(
            name="test",
            parameters=[Parameter(name="value", type="string", optional=False)],
            returns=[],
        )
        result = client_generator._build_params(command)
        assert "*" in result

    def test_build_params_always_includes_session_id_last(
        self, client_generator: ClientGenerator
    ) -> None:
        command = Command(name="test", parameters=[], returns=[])
        result = client_generator._build_params(command)
        assert result[-1] == "session_id: str | None = None"
