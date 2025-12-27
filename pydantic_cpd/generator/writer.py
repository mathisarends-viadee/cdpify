from pathlib import Path
from pydantic_cpd.generator.models import Domain

DOMAINS_DIR = Path(__file__).parent.parent / "domains"


def generate_domain(domain: Domain) -> None:
    output_path = DOMAINS_DIR / f"{domain.domain.lower()}.py"

    code = f'''"""Generated from CDP spec: {domain.domain} domain"""

from pydantic import BaseModel
from typing import Optional, Literal, Any


# TODO: Generate types
# TODO: Generate command params/results
# TODO: Generate client class
'''

    output_path.write_text(code)
    print(f"  ✓ Generated {output_path.name}")


def generate_all_domains(domains: list[Domain]) -> None:
    DOMAINS_DIR.mkdir(exist_ok=True)

    print("\n📝 Generating domain modules...")
    for domain in domains:
        generate_domain(domain)

    # Generate __init__.py
    init_code = '"""Generated CDP domains"""\n\n'
    init_code += "\n".join(
        f"from pydantic_cpd.domains.{d.domain.lower()} import {d.domain}Client"
        for d in domains
    )
    init_code += (
        "\n\n__all__ = [" + ", ".join(f'"{d.domain}Client"' for d in domains) + "]\n"
    )

    (DOMAINS_DIR / "__init__.py").write_text(init_code)
    print("  ✓ Generated __init__.py")
