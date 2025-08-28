# !cli.py
"""
CLI entrypoints for DB initialization and demo data creation.

Streamlining plan:
- Keep this file as thin command wrappers around `db_utils` functions.
- Push all validation, building, and persistence to services/repositories.
- Add a `report` subcommand group for JSON exports and health checks.
- Validate incompatible flags early (e.g., manual params with `--auto`).
- Consider migrating to Typer for typed params and better help.
"""
from __future__ import annotations

import json
from typing import Optional
import subprocess
import sys

import click

from db_utils import (
    get_logger, setup_env, init_db, migrate_db, build_auto_campaign, 
    persist_campaign, generate_performance, generate_hourly_performance
)
from models.registry import registry
from factories.faker_providers import (
    fake_advertiser,
    ProfileName,
)
from services.generator import create_advertiser_payload


@click.group()
def cli() -> None:
    """Root command group for ads demo utilities."""
    pass


@cli.command("init-db")
@click.option("--log-level", type=str, required=False)
@click.option("--db-url", type=str, required=False)
@click.option("--seed", type=int, required=False)
def cmd_init_db(log_level: Optional[str] = None, db_url: Optional[str] = None, seed: Optional[int] = None) -> None:
    """Initialize a fresh database using the configured URL."""
    setup_env(log_level, db_url, seed)
    init_db()
    get_logger(__name__).info("Initialized SQLite database")


@cli.command("migrate-db")
@click.option("--log-level", type=str, required=False)
@click.option("--db-url", type=str, required=False)
def cmd_migrate_db(log_level: Optional[str] = None, db_url: Optional[str] = None) -> None:
    """Apply database migrations for the current schema version."""
    setup_env(log_level, db_url)
    get_logger(__name__).info("Applying DB migrations")
    migrate_db()
    get_logger(__name__).info("Applied migrations")


@cli.command("create-advertiser")
@click.option("--name", required=False, type=str)
@click.option("--email", required=False, type=str)
@click.option("--brand", required=False, type=str)
@click.option("--agency", required=False, type=str)
@click.option("--auto", is_flag=True, default=False)
@click.option("--log-level", type=str, required=False)
@click.option("--db-url", type=str, required=False)
@click.option("--seed", type=int, required=False)
def cmd_create_advertiser(name: Optional[str], email: Optional[str], brand: Optional[str], agency: Optional[str], auto: bool, log_level: Optional[str] = None, db_url: Optional[str] = None, seed: Optional[int] = None) -> None:
    """Create an advertiser; use --auto or provide name and email."""
    setup_env(log_level, db_url, seed)
    if auto or not (name and email):
        n, e, b, a = fake_advertiser()
        name = name or n
        email = email or e
        brand = brand or b
        agency = agency or a
    payload = registry.AdvertiserCreate(name=name or "", contact_email=email or "", brand=brand, agency_name=agency)
    adv = create_advertiser_payload(payload)
    from db_utils import session_scope
    with session_scope() as s:
        s.add(adv)
        s.flush()
        print(json.dumps({"advertiser_id": adv.id}))


@cli.command("create-campaign")
@click.option("--advertiser-id", required=True, type=int)
@click.option("--auto", is_flag=True, default=False)
@click.option("--profile", type=click.Choice(["AWARENESS", "CONSIDERATION", "CONVERSION"]))
@click.option("--log-level", type=str, required=False)
@click.option("--db-url", type=str, required=False)
@click.option("--seed", type=int, required=False)
@click.option("--generate-performance/--no-generate-performance", default=False, show_default=True)
def cmd_create_campaign(advertiser_id: Optional[int], auto: bool, profile: Optional[ProfileName] = None, log_level: Optional[str] = None, db_url: Optional[str] = None, seed: Optional[int] = None, generate_performance: bool = False) -> None:
    """Create a demo campaign for an advertiser; requires --auto for v1."""
    setup_env(log_level, db_url, seed)
    if not auto:
        raise click.UsageError("For v1, use --auto to generate a demo campaign")
    campaign = build_auto_campaign(advertiser_id, profile)
    result = persist_campaign(advertiser_id, campaign, return_ids=True)
    if generate_performance and isinstance(result, dict):
        cid = result.get("campaign_id")
        if cid is not None:
            _ = generate_hourly_performance(int(cid), seed=seed, replace=True)



@cli.command("generate-performance")
@click.option("--campaign-id", required=True, type=int)
@click.option("--seed", required=False, type=int)
@click.option("--replace/--no-replace", default=True, show_default=True)
def cmd_generate_performance(campaign_id: int, seed: Optional[int] = None, replace: bool = True) -> None:
    """Generate synthetic hourly performance rows for a campaign."""
    result = generate_performance(campaign_id, seed=seed, replace=replace)
    print(json.dumps(result))

@cli.command("generate-performance-ext")
@click.option("--campaign-id", required=True, type=int)
@click.option("--seed", required=False, type=int)
@click.option("--replace/--no-replace", default=True, show_default=True)
def cmd_generate_performance_ext(campaign_id: int, seed: Optional[int] = None, replace: bool = True) -> None:
    """Generate synthetic hourly extended performance rows for a campaign."""
    from services.performance_ext import generate_hourly_performance_ext
    rows = generate_hourly_performance_ext(campaign_id, seed=seed, replace=True)
    print(json.dumps({"campaign_id": campaign_id, "rows": rows, "type": "extended"}))


# =============================================================================
# NEW STREAMLINED COMMANDS
# =============================================================================

@cli.command("create-example")
@click.option("--template", required=True, type=str, help="Path to template file")
@click.option("--example", required=True, type=str, help="Name of example to generate")
@click.option("--seed", type=int, help="Seed for reproducible generation")
@click.option("--performance-only", is_flag=True, help="Generate only performance data for existing entities")
@click.option("--log-level", type=str, required=False)
@click.option("--db-url", type=str, required=False)
def cmd_create_example(template: str, example: str, seed: Optional[int] = None, performance_only: bool = False, log_level: Optional[str] = None, db_url: Optional[str] = None) -> None:
    """Create complete Netflix ads example from template with auto-performance generation."""
    setup_env(log_level, db_url, seed)
    
    try:
        # Import the new streamlined processor
        from services.streamlined_processor import create_example_from_template
        
        result = create_example_from_template(template, example, performance_only=performance_only)
        print(json.dumps(result, indent=2))
        
    except ImportError:
        print("Streamlined processor not implemented yet. Use create-from-config instead.")
        print("Example: python cli.py create-from-config --path config.yml --generate-performance")
        raise click.UsageError("Streamlined processor not available")


@cli.command("test-fields")
@click.option("--template", required=True, type=str, help="Path to field testing template")
@click.option("--focus", required=True, type=str, help="Comma-separated list of fields to test")
@click.option("--seed", type=int, help="Seed for reproducible generation")
@click.option("--auto-performance/--no-auto-performance", default=True, help="Auto-generate performance data")
@click.option("--log-level", type=str, required=False)
@click.option("--db-url", type=str, required=False)
def cmd_test_fields(template: str, focus: str, seed: Optional[int] = None, auto_performance: bool = True, log_level: Optional[str] = None, db_url: Optional[str] = None) -> None:
    """Test specific fields while auto-generating realistic context."""
    setup_env(log_level, db_url, seed)
    
    try:
        # Import the new streamlined processor
        from services.streamlined_processor import test_specific_fields
        
        focus_fields = [f.strip() for f in focus.split(",")]
        result = test_specific_fields(template, focus_fields, auto_performance=auto_performance)
        print(json.dumps(result, indent=2))
        
    except ImportError:
        print("Streamlined processor not implemented yet. Use create-from-config instead.")
        print("Example: python cli.py create-from-config --path config.yml --generate-performance")
        raise click.UsageError("Streamlined processor not available")


@cli.command("create-profile")
@click.option("--name", required=True, type=str, help="Profile name from campaign-profiles.yml")
@click.option("--test-fields", type=str, help="Comma-separated list of fields to override")
@click.option("--seed", type=int, help="Seed for reproducible generation")
@click.option("--performance-only", is_flag=True, help="Generate only performance data for existing entities")
@click.option("--log-level", type=str, required=False)
@click.option("--db-url", type=str, required=False)
def cmd_create_profile(name: str, test_fields: Optional[str] = None, seed: Optional[int] = None, performance_only: bool = False, log_level: Optional[str] = None, db_url: Optional[str] = None) -> None:
    """Create campaign from pre-built profile with smart defaults."""
    setup_env(log_level, db_url, seed)
    
    try:
        # Import the new streamlined processor
        from services.streamlined_processor import create_campaign_from_profile
        
        override_fields = {}
        if test_fields:
            for field in test_fields.split(","):
                field = field.strip()
                if "=" in field:
                    key, value = field.split("=", 1)
                    override_fields[key.strip()] = value.strip()
        
        result = create_campaign_from_profile(name, override_fields, performance_only=performance_only)
        print(json.dumps(result, indent=2))
        
    except ImportError:
        print("Streamlined processor not implemented yet. Use create-from-config instead.")
        print("Example: python cli.py create-from-config --path config.yml --generate-performance")
        raise click.UsageError("Streamlined processor not available")


@cli.command("test-scenario")
@click.option("--name", required=True, type=str, help="Scenario name from testing-scenarios.yml")
@click.option("--seed", type=int, help="Seed for reproducible generation")
@click.option("--log-level", type=str, required=False)
@click.option("--db-url", type=str, required=False)
def cmd_test_scenario(name: str, seed: Optional[int] = None, log_level: Optional[str] = None, db_url: Optional[str] = None) -> None:
    """Test common scenarios with one command."""
    setup_env(log_level, db_url, seed)
    
    try:
        # Import the new streamlined processor
        from services.streamlined_processor import test_prebuilt_scenario
        
        result = test_prebuilt_scenario(name)
        print(json.dumps(result, indent=2))
        
    except ImportError:
        print("Streamlined processor not implemented yet. Use create-from-config instead.")
        print("Example: python cli.py create-from-config --path config.yml --generate-performance")
        raise click.UsageError("Streamlined processor not available")


if __name__ == "__main__":
    cli()


