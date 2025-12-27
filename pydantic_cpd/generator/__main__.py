import asyncio
from pydantic_cpd.generator.downloader import download_specs
from pydantic_cpd.generator.parser import filter_domains
from pydantic_cpd.generator.writer import generate_all_domains


async def main() -> None:
    print("🚀 Starting CDP Pydantic Generator\n")

    specs = await download_specs()

    print(f"\n📊 CDP Version: {specs.version_string}")
    print(f"📊 Total domains available: {len(specs.all_domains)}")

    print("\n🔍 Filtering domains...")
    domains = filter_domains(specs)
    print(f"✅ Selected {len(domains)} domains for generation")

    generate_all_domains(domains)

    print("\n✅ Generation complete!")


if __name__ == "__main__":
    asyncio.run(main())
