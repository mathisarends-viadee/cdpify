from pydantic_cpd.generator.models import CDPSpecs, Domain
from pydantic_cpd.generator.config import DOMAINS_TO_GENERATE


def filter_domains(specs: CDPSpecs) -> list[Domain]:
    domains = []

    for domain_name in DOMAINS_TO_GENERATE:
        domain = specs.get_domain(domain_name)
        if domain:
            domains.append(domain)
            print(
                f"  ✓ {domain_name}: {len(domain.commands)} commands, {len(domain.events)} events"
            )
        else:
            print(f"  ✗ {domain_name}: NOT FOUND")

    return domains
