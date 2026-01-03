from pydantic_cpd.generator.generators.utils import (
    format_docstring,
    map_cdp_type,
    to_pascal_case,
    to_snake_case,
)
from pydantic_cpd.generator.models import Parameter


class TestToPascalCase:
    def test_to_pascal_case_empty_string_returns_empty_string(self) -> None:
        result = to_pascal_case("")
        assert result == ""

    def test_to_pascal_case_single_lowercase_letter_returns_uppercase(self) -> None:
        result = to_pascal_case("a")
        assert result == "A"

    def test_to_pascal_case_already_pascal_returns_unchanged(self) -> None:
        result = to_pascal_case("MyClass")
        assert result == "MyClass"

    def test_to_pascal_case_lowercase_word_returns_capitalized(self) -> None:
        result = to_pascal_case("myClass")
        assert result == "MyClass"

    def test_to_pascal_case_snake_case_returns_first_char_uppercase(self) -> None:
        result = to_pascal_case("my_class")
        assert result == "My_class"


class TestToSnakeCase:
    def test_to_snake_case_empty_string_returns_empty_string(self) -> None:
        result = to_snake_case("")
        assert result == ""

    def test_to_snake_case_single_lowercase_letter_returns_unchanged(self) -> None:
        result = to_snake_case("a")
        assert result == "a"

    def test_to_snake_case_pascal_case_returns_snake_case(self) -> None:
        result = to_snake_case("MyClass")
        assert result == "my_class"

    def test_to_snake_case_camel_case_returns_snake_case(self) -> None:
        result = to_snake_case("myVariable")
        assert result == "my_variable"

    def test_to_snake_case_multiple_uppercase_letters_adds_underscore_before_each(
        self,
    ) -> None:
        result = to_snake_case("HTTPSConnection")
        assert result == "h_t_t_p_s_connection"

    def test_to_snake_case_already_snake_case_returns_lowercase(self) -> None:
        result = to_snake_case("my_variable")
        assert result == "my_variable"


class TestFormatDocstring:
    def test_format_docstring_empty_string_returns_empty_string(self) -> None:
        result = format_docstring("")
        assert result == ""

    def test_format_docstring_short_text_wraps_in_triple_quotes(self) -> None:
        result = format_docstring("Short description", indent=0)
        assert result == '"""\nShort description\n"""'

    def test_format_docstring_adds_correct_indentation(self) -> None:
        result = format_docstring("Test", indent=4)
        lines = result.split("\n")
        assert lines[0] == '    """'
        assert lines[1] == "    Test"
        assert lines[2] == '    """'

    def test_format_docstring_wraps_long_text_to_line_limit(self) -> None:
        long_text = " ".join(["word"] * 50)
        result = format_docstring(long_text, indent=0)
        lines = result.split("\n")

        for line in lines[1:-1]:
            assert len(line) <= 88

    def test_format_docstring_preserves_word_boundaries(self) -> None:
        text = "This is a test with multiple words"
        result = format_docstring(text, indent=0)
        assert "This is a test" in result
        assert "multiple words" in result

    def test_format_docstring_with_custom_indent(self) -> None:
        result = format_docstring("Test", indent=8)
        lines = result.split("\n")
        assert lines[0] == '        """'
        assert lines[1] == "        Test"
        assert lines[2] == '        """'


class TestMapCdpType:
    def test_map_cdp_type_string_returns_str(self) -> None:
        param = Parameter(name="test", type="string", optional=False)
        result = map_cdp_type(param)
        assert result == "str"

    def test_map_cdp_type_integer_returns_int(self) -> None:
        param = Parameter(name="test", type="integer", optional=False)
        result = map_cdp_type(param)
        assert result == "int"

    def test_map_cdp_type_number_returns_float(self) -> None:
        param = Parameter(name="test", type="number", optional=False)
        result = map_cdp_type(param)
        assert result == "float"

    def test_map_cdp_type_boolean_returns_bool(self) -> None:
        param = Parameter(name="test", type="boolean", optional=False)
        result = map_cdp_type(param)
        assert result == "bool"

    def test_map_cdp_type_object_returns_dict_annotation(self) -> None:
        param = Parameter(name="test", type="object", optional=False)
        result = map_cdp_type(param)
        assert result == "dict[str, Any]"

    def test_map_cdp_type_any_returns_any(self) -> None:
        param = Parameter(name="test", type="any", optional=False)
        result = map_cdp_type(param)
        assert result == "Any"

    def test_map_cdp_type_optional_string_returns_optional_type(self) -> None:
        param = Parameter(name="test", type="string", optional=True)
        result = map_cdp_type(param)
        assert result == "str | None"

    def test_map_cdp_type_optional_object_returns_optional_dict(self) -> None:
        param = Parameter(name="test", type="object", optional=True)
        result = map_cdp_type(param)
        assert result == "dict[str, Any] | None"

    def test_map_cdp_type_with_ref_returns_ref_name(self) -> None:
        param = Parameter(name="test", ref="CustomType", optional=False)
        result = map_cdp_type(param)
        assert result == "CustomType"

    def test_map_cdp_type_with_optional_ref_returns_optional_ref(self) -> None:
        param = Parameter(name="test", ref="CustomType", optional=True)
        result = map_cdp_type(param)
        assert result == "CustomType | None"

    def test_map_cdp_type_array_without_items_returns_list_any(self) -> None:
        param = Parameter(name="test", type="array", optional=False)
        result = map_cdp_type(param)
        assert result == "list[Any]"

    def test_map_cdp_type_array_with_string_items_returns_list_str(self) -> None:
        param = Parameter(
            name="test", type="array", items={"type": "string"}, optional=False
        )
        result = map_cdp_type(param)
        assert result == "list[str]"

    def test_map_cdp_type_array_with_ref_items_returns_list_with_module_ref(
        self,
    ) -> None:
        param = Parameter(
            name="test",
            type="array",
            items={"$ref": "dom.Node"},
            optional=False,
        )
        result = map_cdp_type(param)
        assert result == "list[dom.Node]"

    def test_map_cdp_type_array_with_integer_items_returns_list_int(self) -> None:
        param = Parameter(
            name="test", type="array", items={"type": "integer"}, optional=False
        )
        result = map_cdp_type(param)
        assert result == "list[int]"

    def test_map_cdp_type_optional_array_returns_optional_list(self) -> None:
        param = Parameter(
            name="test", type="array", items={"type": "string"}, optional=True
        )
        result = map_cdp_type(param)
        assert result == "list[str] | None"

    def test_map_cdp_type_enum_returns_literal_type(self) -> None:
        param = Parameter(
            name="test",
            type="string",
            enum=["value1", "value2", "value3"],
            optional=False,
        )
        result = map_cdp_type(param)
        assert result == 'Literal["value1", "value2", "value3"]'

    def test_map_cdp_type_optional_enum_returns_optional_literal(self) -> None:
        param = Parameter(
            name="test",
            type="string",
            enum=["active", "inactive"],
            optional=True,
        )
        result = map_cdp_type(param)
        assert result == 'Literal["active", "inactive"] | None'

    def test_map_cdp_type_unknown_type_returns_any(self) -> None:
        param = Parameter(name="test", type="unknown_type", optional=False)
        result = map_cdp_type(param)
        assert result == "Any"
