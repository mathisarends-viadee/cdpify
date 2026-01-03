import pytest

from pydantic_cpd.generator.generators.events import EventsGenerator
from pydantic_cpd.generator.models import Domain, Event, Parameter


@pytest.fixture
def events_generator() -> EventsGenerator:
    return EventsGenerator()


@pytest.fixture
def empty_domain() -> Domain:
    return Domain(domain="TestDomain", events=[])


@pytest.fixture
def domain_with_simple_event() -> Domain:
    event = Event(
        name="testEvent",
        description="A test event",
        parameters=[
            Parameter(name="value", type="string", optional=False),
        ],
    )
    return Domain(domain="TestDomain", events=[event])


@pytest.fixture
def domain_with_multiple_events() -> Domain:
    event1 = Event(
        name="firstEvent",
        parameters=[
            Parameter(name="id", type="integer", optional=False),
        ],
    )
    event2 = Event(
        name="secondEvent",
        parameters=[
            Parameter(name="data", type="object", optional=True),
        ],
    )
    return Domain(domain="TestDomain", events=[event1, event2])


@pytest.fixture
def domain_with_event_no_params() -> Domain:
    event = Event(name="emptyEvent", parameters=[])
    return Domain(domain="TestDomain", events=[event])


@pytest.fixture
def domain_with_cross_domain_ref() -> Domain:
    event = Event(
        name="testEvent",
        parameters=[
            Parameter(name="node", ref="dom.Node", optional=False),
        ],
    )
    return Domain(domain="Network", events=[event])


class TestEventsGeneratorGenerate:
    def test_generate_with_empty_domain_contains_no_events_comment(
        self, events_generator: EventsGenerator, empty_domain: Domain
    ) -> None:
        result = events_generator.generate(empty_domain)
        assert "# No events defined" in result

    def test_generate_with_simple_event_creates_event_enum(
        self, events_generator: EventsGenerator, domain_with_simple_event: Domain
    ) -> None:
        result = events_generator.generate(domain_with_simple_event)
        assert "class TestDomainEvent(StrEnum):" in result
        assert 'TEST_EVENT = "TestDomain.testEvent"' in result

    def test_generate_with_simple_event_creates_event_model(
        self, events_generator: EventsGenerator, domain_with_simple_event: Domain
    ) -> None:
        result = events_generator.generate(domain_with_simple_event)
        assert "class TestEventEvent(CDPModel):" in result
        assert "value: str" in result

    def test_generate_with_event_no_params_includes_pass_statement(
        self, events_generator: EventsGenerator, domain_with_event_no_params: Domain
    ) -> None:
        result = events_generator.generate(domain_with_event_no_params)
        assert "class EmptyEventEvent(CDPModel):" in result
        assert "    pass" in result

    def test_generate_with_multiple_events_creates_all_enum_entries(
        self, events_generator: EventsGenerator, domain_with_multiple_events: Domain
    ) -> None:
        result = events_generator.generate(domain_with_multiple_events)
        assert 'FIRST_EVENT = "TestDomain.firstEvent"' in result
        assert 'SECOND_EVENT = "TestDomain.secondEvent"' in result

    def test_generate_with_optional_param_adds_none_default(
        self, events_generator: EventsGenerator, domain_with_multiple_events: Domain
    ) -> None:
        result = events_generator.generate(domain_with_multiple_events)
        assert "data: dict[str, Any] | None = None" in result

    def test_generate_includes_strenumimport(
        self, events_generator: EventsGenerator, domain_with_simple_event: Domain
    ) -> None:
        result = events_generator.generate(domain_with_simple_event)
        assert "from enum import StrEnum" in result

    def test_generate_includes_cdp_model_import(
        self, events_generator: EventsGenerator, domain_with_simple_event: Domain
    ) -> None:
        result = events_generator.generate(domain_with_simple_event)
        assert "from pydantic_cpd.domains.base import CDPModel" in result

    def test_generate_with_cross_domain_ref_includes_type_checking_import(
        self, events_generator: EventsGenerator, domain_with_cross_domain_ref: Domain
    ) -> None:
        result = events_generator.generate(domain_with_cross_domain_ref)
        assert "if TYPE_CHECKING:" in result
        assert "from pydantic_cpd.domains import dom" in result

    def test_generate_includes_header_comment(
        self, events_generator: EventsGenerator, domain_with_simple_event: Domain
    ) -> None:
        result = events_generator.generate(domain_with_simple_event)
        assert "# AUTO-GENERATED" in result or "Generated" in result


class TestEventsGeneratorEnumGeneration:
    def test_to_enum_name_converts_camel_to_upper_snake(
        self, events_generator: EventsGenerator
    ) -> None:
        result = events_generator._to_enum_name("myTestEvent")
        assert result == "MY_TEST_EVENT"

    def test_to_enum_name_handles_single_word(
        self, events_generator: EventsGenerator
    ) -> None:
        result = events_generator._to_enum_name("event")
        assert result == "EVENT"


class TestEventsGeneratorTypeResolution:
    def test_resolve_type_with_simple_type_returns_mapped_type(
        self, events_generator: EventsGenerator
    ) -> None:
        param = Parameter(name="test", type="string", optional=False)
        result = events_generator._resolve_type(param)
        assert result == "str"

    def test_resolve_type_with_optional_adds_none_union(
        self, events_generator: EventsGenerator
    ) -> None:
        param = Parameter(name="test", type="integer", optional=True)
        result = events_generator._resolve_type(param)
        assert result == "int | None"

    def test_resolve_type_with_cross_domain_ref_includes_module_prefix(
        self, events_generator: EventsGenerator
    ) -> None:
        param = Parameter(name="test", ref="dom.Node", optional=False)
        result = events_generator._resolve_type(param)
        assert result == "dom.Node"

    def test_resolve_type_with_cross_domain_ref_does_not_add_none_when_not_optional(
        self, events_generator: EventsGenerator
    ) -> None:
        param = Parameter(name="test", ref="page.Frame", optional=False)
        result = events_generator._resolve_type(param)
        assert " | None" not in result
