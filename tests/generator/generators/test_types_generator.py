import pytest

from pydantic_cpd.generator.generators.types import TypesGenerator
from pydantic_cpd.generator.models import Domain, Parameter, TypeDefinition


@pytest.fixture
def types_generator() -> TypesGenerator:
    return TypesGenerator()


@pytest.fixture
def empty_domain() -> Domain:
    return Domain(domain="TestDomain", types=[])


@pytest.fixture
def domain_with_simple_type() -> Domain:
    type_def = TypeDefinition(
        id="SimpleType",
        type="object",
        description="A simple type",
        properties=[
            Parameter(name="value", type="string", optional=False),
        ],
    )
    return Domain(domain="TestDomain", types=[type_def])


@pytest.fixture
def domain_with_enum_type() -> Domain:
    type_def = TypeDefinition(
        id="StatusType",
        type="string",
        enum=["active", "inactive", "pending"],
    )
    return Domain(domain="TestDomain", types=[type_def])


@pytest.fixture
def domain_with_array_type() -> Domain:
    type_def = TypeDefinition(
        id="ListType",
        type="array",
        items={"type": "string"},
    )
    return Domain(domain="TestDomain", types=[type_def])


@pytest.fixture
def domain_with_cross_domain_ref() -> Domain:
    type_def = TypeDefinition(
        id="ComplexType",
        type="object",
        properties=[
            Parameter(name="node", ref="dom.Node", optional=False),
        ],
    )
    return Domain(domain="Network", types=[type_def])


class TestTypesGeneratorGenerate:
    def test_generate_with_empty_domain_contains_no_types_comment(
        self, types_generator: TypesGenerator, empty_domain: Domain
    ) -> None:
        result = types_generator.generate(empty_domain)
        assert "# No types defined" in result

    def test_generate_with_simple_type_creates_model(
        self, types_generator: TypesGenerator, domain_with_simple_type: Domain
    ) -> None:
        result = types_generator.generate(domain_with_simple_type)
        assert "class SimpleType(CDPModel):" in result
        assert "value: str" in result

    def test_generate_with_enum_type_creates_literal_alias(
        self, types_generator: TypesGenerator, domain_with_enum_type: Domain
    ) -> None:
        result = types_generator.generate(domain_with_enum_type)
        assert "StatusType = " in result
        assert 'Literal["active", "inactive", "pending"]' in result

    def test_generate_with_array_type_creates_list_alias(
        self, types_generator: TypesGenerator, domain_with_array_type: Domain
    ) -> None:
        result = types_generator.generate(domain_with_array_type)
        assert "ListType = list[Any]" in result

    def test_generate_includes_cdp_model_import(
        self, types_generator: TypesGenerator, domain_with_simple_type: Domain
    ) -> None:
        result = types_generator.generate(domain_with_simple_type)
        assert "from pydantic_cpd.domains.base import CDPModel" in result

    def test_generate_with_cross_domain_ref_includes_type_checking_import(
        self, types_generator: TypesGenerator, domain_with_cross_domain_ref: Domain
    ) -> None:
        result = types_generator.generate(domain_with_cross_domain_ref)
        assert "if TYPE_CHECKING:" in result
        assert "from pydantic_cpd.domains import dom" in result

    def test_generate_includes_header_comment(
        self, types_generator: TypesGenerator, domain_with_simple_type: Domain
    ) -> None:
        result = types_generator.generate(domain_with_simple_type)
        assert "# AUTO-GENERATED" in result or "Generated" in result


class TestTypesGeneratorTypeAliases:
    def test_create_type_alias_for_string_without_enum_uses_basic_type(
        self, types_generator: TypesGenerator
    ) -> None:
        type_def = TypeDefinition(
            id="MyString",
            type="string",
        )
        result = types_generator._create_type_alias(type_def)
        assert "MyString = str" in result

    def test_create_type_alias_for_array_without_items_generates_list_any(
        self, types_generator: TypesGenerator
    ) -> None:
        type_def = TypeDefinition(
            id="MyArray",
            type="array",
        )
        result = types_generator._create_type_alias(type_def)
        assert "MyArray = list[Any]" in result

    def test_create_type_alias_for_simple_type_uses_mapping(
        self, types_generator: TypesGenerator
    ) -> None:
        type_def = TypeDefinition(
            id="MyString",
            type="string",
        )
        result = types_generator._create_type_alias(type_def)
        assert "MyString = str" in result


class TestTypesGeneratorObjectModels:
    def test_create_object_model_with_properties_generates_class(
        self, types_generator: TypesGenerator
    ) -> None:
        type_def = TypeDefinition(
            id="MyObject",
            type="object",
            properties=[
                Parameter(name="field", type="string", optional=False),
            ],
        )
        result = types_generator._create_object_model(type_def)
        assert "class MyObject(CDPModel):" in result
        assert "field: str" in result

    def test_create_object_model_with_no_properties_only_has_class_definition(
        self, types_generator: TypesGenerator
    ) -> None:
        type_def = TypeDefinition(
            id="EmptyObject",
            type="object",
            properties=[],
        )
        result = types_generator._create_object_model(type_def)
        assert "class EmptyObject(CDPModel):" in result
        assert len(result.strip().split("\n")) == 1

    def test_create_object_model_with_description_includes_docstring(
        self, types_generator: TypesGenerator
    ) -> None:
        type_def = TypeDefinition(
            id="DocumentedObject",
            type="object",
            description="This is a test description",
            properties=[],
        )
        result = types_generator._create_object_model(type_def)
        assert '"""' in result
        assert "This is a test description" in result
