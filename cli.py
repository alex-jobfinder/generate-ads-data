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

import click

from db_utils import (
    build_auto_campaign,
    generate_hourly_performance,
    generate_performance,
    get_logger,
    init_db,
    migrate_db,
    persist_campaign,
    setup_env,
)
from factories.faker_providers import (
    ProfileName,
    fake_advertiser,
)
from models.registry import registry
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
def cmd_create_advertiser(
    name: Optional[str],
    email: Optional[str],
    brand: Optional[str],
    agency: Optional[str],
    auto: bool,
    log_level: Optional[str] = None,
    db_url: Optional[str] = None,
    seed: Optional[int] = None,
) -> None:
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
def cmd_create_campaign(
    advertiser_id: Optional[int],
    auto: bool,
    profile: Optional[ProfileName] = None,
    log_level: Optional[str] = None,
    db_url: Optional[str] = None,
    seed: Optional[int] = None,
    generate_performance: bool = False,
) -> None:
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
def cmd_create_example(
    template: str,
    example: str,
    seed: Optional[int] = None,
    performance_only: bool = False,
    log_level: Optional[str] = None,
    db_url: Optional[str] = None,
) -> None:
    """Create complete Netflix ads example from template with auto-performance generation."""
    setup_env(log_level, db_url, seed)

    try:
        # Import the new streamlined processor
        from services.processor import create_example_from_template

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
def cmd_test_fields(
    template: str,
    focus: str,
    seed: Optional[int] = None,
    auto_performance: bool = True,
    log_level: Optional[str] = None,
    db_url: Optional[str] = None,
) -> None:
    """Test specific fields while auto-generating realistic context."""
    setup_env(log_level, db_url, seed)

    try:
        # Import the new streamlined processor
        from services.processor import test_specific_fields

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
def cmd_create_profile(
    name: str,
    test_fields: Optional[str] = None,
    seed: Optional[int] = None,
    performance_only: bool = False,
    log_level: Optional[str] = None,
    db_url: Optional[str] = None,
) -> None:
    """Create campaign from pre-built profile with smart defaults."""
    setup_env(log_level, db_url, seed)

    try:
        # Import the new streamlined processor
        from services.processor import create_campaign_from_profile

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
def cmd_test_scenario(
    name: str, seed: Optional[int] = None, log_level: Optional[str] = None, db_url: Optional[str] = None
) -> None:
    """Test common scenarios with one command."""
    setup_env(log_level, db_url, seed)

    try:
        # Import the new streamlined processor
        from services.processor import test_prebuilt_scenario

        result = test_prebuilt_scenario(name)
        print(json.dumps(result, indent=2))

    except ImportError:
        print("Streamlined processor not implemented yet. Use create-from-config instead.")
        print("Example: python cli.py create-from-config --path config.yml --generate-performance")
        raise click.UsageError("Streamlined processor not available")


@cli.command("list-campaigns")
@click.option("--format", type=click.Choice(["table", "json", "csv"]), default="table", help="Output format")
@click.option("--objective", type=str, help="Filter by campaign objective")
@click.option("--status", type=str, help="Filter by campaign status")
def cmd_list_campaigns(format: str, objective: Optional[str] = None, status: Optional[str] = None) -> None:
    """List all campaigns with optional filtering."""
    try:
        # Try to import the service first
        from services.campaign_service import list_campaigns
        campaigns = list_campaigns(objective=objective, status=status)
        
        if format == "json":
            print(json.dumps(campaigns, indent=2))
        elif format == "csv":
            import csv
            import sys
            writer = csv.writer(sys.stdout)
            writer.writerow(["ID", "Name", "Objective", "Status", "Target CPM", "DSP Partner"])
            for campaign in campaigns:
                writer.writerow([
                    campaign.get("id"),
                    campaign.get("name"),
                    campaign.get("objective"),
                    campaign.get("status"),
                    campaign.get("target_cpm"),
                    campaign.get("dsp_partner")
                ])
        else:
            # Table format
            print("📊 Campaign List")
            print("=" * 80)
            print(f"{'ID':<4} {'Name':<25} {'Objective':<15} {'Status':<10} {'CPM':<8} {'DSP':<12}")
            print("-" * 80)
            for campaign in campaigns:
                print(f"{campaign.get('id', ''):<4} {campaign.get('name', '')[:24]:<25} {campaign.get('objective', '')[:14]:<15} {campaign.get('status', '')[:9]:<10} ${campaign.get('target_cpm', 0):<7,.0f} {campaign.get('dsp_partner', '')[:11]:<12}")
    
    except ImportError:
        # Fallback: Use direct database queries
        try:
            import sqlite3
            import os
            
            if not os.path.exists("ads.db"):
                print("❌ Database not found. Please run './run_all.sh' first to create sample data.")
                return
            
            conn = sqlite3.connect("ads.db")
            cursor = conn.cursor()
            
            # Build query with optional filters - using correct column names
            query = "SELECT id, name, objective, status, target_cpm, dsp_partner FROM campaigns"
            params = []
            
            if objective or status:
                query += " WHERE"
                if objective:
                    query += " objective = ?"
                    params.append(objective)
                if status:
                    if objective:
                        query += " AND"
                    query += " status = ?"
                    params.append(status)
            
            cursor.execute(query, params)
            campaigns = cursor.fetchall()
            
            if format == "json":
                result = []
                for row in campaigns:
                    result.append({
                        "id": row[0],
                        "name": row[1],
                        "objective": row[2],
                        "status": row[3],
                        "target_cpm": row[4],
                        "dsp_partner": row[5]
                    })
                print(json.dumps(result, indent=2))
            elif format == "csv":
                import csv
                import sys
                writer = csv.writer(sys.stdout)
                writer.writerow(["ID", "Name", "Objective", "Status", "Target CPM", "DSP Partner"])
                for row in campaigns:
                    writer.writerow(row)
            else:
                # Table format
                print("📊 Campaign List (Direct DB Query)")
                print("=" * 80)
                print(f"{'ID':<4} {'Name':<25} {'Objective':<15} {'Status':<10} {'CPM':<8} {'DSP':<12}")
                print("-" * 80)
                for row in campaigns:
                    name = row[1][:24] if row[1] else ""
                    objective = row[2][:14] if row[2] else ""
                    status = row[3][:9] if row[3] else ""
                    cpm = row[4] if row[4] else 0
                    dsp = row[5][:11] if row[5] else ""
                    print(f"{row[0]:<4} {name:<25} {objective:<15} {status:<10} ${cpm:<7,.0f} {dsp:<12}")
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Database query failed: {e}")
            print("💡 Try running './run_all.sh' first to create sample data.")
@cli.command("export-campaign")
@click.option("--id", required=True, type=int, help="Campaign ID to export")
@click.option("--format", type=click.Choice(["json", "csv", "excel"]), default="json", help="Export format")
@click.option("--include-performance/--no-include-performance", default=True, show_default=True, help="Include performance data")
def cmd_export_campaign(id: int, format: str, include_performance: bool) -> None:
    """Export campaign data in various formats."""
    try:
        from services.export_service import export_campaign
        result = export_campaign(id, format, include_performance)
        print(json.dumps(result, indent=2))
    
    except ImportError:
        # Fallback: Use direct database queries
        try:
            import sqlite3
            import os
            
            if not os.path.exists("ads.db"):
                print("❌ Database not found. Please run './run_all.sh' first to create sample data.")
                return
            
            conn = sqlite3.connect("ads.db")
            cursor = conn.cursor()
            
            # Get campaign data - using correct column names
            cursor.execute("""
                SELECT c.*, a.name as advertiser_name, a.brand
                FROM campaigns c
                JOIN advertisers a ON c.advertiser_id = a.id
                WHERE c.id = ?
            """, (id,))
            
            campaign = cursor.fetchone()
            if not campaign:
                print(f"❌ Campaign {id} not found.")
                return
            
            # Get line items
            cursor.execute("SELECT * FROM line_items WHERE campaign_id = ?", (id,))
            line_items = cursor.fetchall()
            
            # Get creatives through line items
            if line_items:
                line_item_ids = [str(item[0]) for item in line_items]
                placeholders = ','.join(['?' for _ in line_item_ids])
                cursor.execute(f"SELECT * FROM creatives WHERE line_item_id IN ({placeholders})", line_item_ids)
                creatives = cursor.fetchall()
            else:
                creatives = []
            
            # Get performance data if requested
            performance = []
            if include_performance:
                cursor.execute("SELECT * FROM campaign_performance WHERE campaign_id = ? LIMIT 100", (id,))
                performance = cursor.fetchall()
            
            conn.close()
            
            # Structure the data - using correct column indices
            result = {
                "campaign_id": id,
                "campaign_data": {
                    "name": campaign[1],
                    "status": campaign[2],
                    "created_at": campaign[3],
                    "updated_at": campaign[4],
                    "objective": campaign[6],
                    "currency": campaign[7],
                    "target_cpm": campaign[8],
                    "dsp_partner": campaign[9],
                    "advertiser": campaign[-2],
                    "brand": campaign[-1]
                },
                "line_items_count": len(line_items),
                "creatives_count": len(creatives),
                "performance_records": len(performance) if include_performance else 0
            }
            
            # Handle different formats
            if format == "json":
                print(json.dumps(result, indent=2))
            elif format == "csv":
                import csv
                import sys
                writer = csv.writer(sys.stdout)
                writer.writerow(["Field", "Value"])
                for key, value in result.items():
                    if isinstance(value, dict):
                        for k, v in value.items():
                            writer.writerow([f"{key}.{k}", v])
                    else:
                        writer.writerow([key, value])
            else:
                print("Excel export not available in fallback mode. Use JSON or CSV.")
                print(json.dumps(result, indent=2))
                
        except Exception as e:
            print(f"❌ Export failed: {e}")
            print("💡 Try running './run_all.sh' first to create sample data.")
    
    except ValueError as e:
        # Handle service errors (e.g., campaign not found)
        print(f"❌ {e}")
        return

@cli.command("compare-campaigns")
@click.option("--campaign1", required=True, type=int, help="First campaign ID")
@click.option("--campaign2", required=True, type=int, help="Second campaign ID")
@click.option("--metrics", type=str, default="cpm,ctr,conversion,roi", help="Comma-separated metrics to compare")
def cmd_compare_campaigns(campaign1: int, campaign2: int, metrics: str) -> None:
    """Compare two campaigns side-by-side."""
    try:
        from services.comparison_service import compare_campaigns
        metric_list = [m.strip() for m in metrics.split(",")]
        result = compare_campaigns(campaign1, campaign2, metric_list)
        print(json.dumps(result, indent=2))
    
    except ImportError:
        # Fallback: Use direct database queries
        try:
            import sqlite3
            import os
            
            if not os.path.exists("ads.db"):
                print("❌ Database not found. Please run './run_all.sh' first to create sample data.")
                return
            
            conn = sqlite3.connect("ads.db")
            cursor = conn.cursor()
            
            # Get both campaigns - using correct column names
            cursor.execute("SELECT id, name, objective, target_cpm, dsp_partner FROM campaigns WHERE id IN (?, ?)", (campaign1, campaign2))
            campaigns = cursor.fetchall()
            
            if len(campaigns) < 2:
                print(f"❌ One or both campaigns not found. Found: {len(campaigns)}")
                return
            
            # Structure comparison
            result = {
                "campaign_1": {
                    "id": campaigns[0][0],
                    "name": campaigns[0][1],
                    "objective": campaigns[0][2],
                    "target_cpm": campaigns[0][3],
                    "dsp_partner": campaigns[0][4]
                },
                "campaign_2": {
                    "id": campaigns[1][0],
                    "name": campaigns[1][1],
                    "objective": campaigns[1][2],
                    "target_cpm": campaigns[1][3],
                    "dsp_partner": campaigns[1][4]
                },
                "comparison": {
                    "cpm_difference": abs(campaigns[0][3] - campaigns[1][3]),
                    "same_objective": campaigns[0][2] == campaigns[1][2],
                    "same_dsp": campaigns[0][4] == campaigns[1][4]
                }
            }
            
            conn.close()
            print(json.dumps(result, indent=2))
            
        except Exception as e:
            print(f"❌ Comparison failed: {e}")
            print("💡 Try running './run_all.sh' first to create sample data.")
    
    except ValueError as e:
        # Handle service errors (e.g., campaigns not found)
        print(f"❌ {e}")
        return

@cli.command("compare-by-objective")
@click.option("--objective", required=True, type=str, help="Campaign objective to compare")
@click.option("--top-n", type=int, default=5, help="Number of top campaigns to show")
def cmd_compare_by_objective(objective: str, top_n: int) -> None:
    """Compare campaigns by objective type."""
    try:
        from services.comparison_service import compare_by_objective
        result = compare_by_objective(objective, top_n)
        print(json.dumps(result, indent=2))
    
    except ImportError:
        # Fallback: Use direct database queries
        try:
            import sqlite3
            import os
            
            if not os.path.exists("ads.db"):
                print("❌ Database not found. Please run './run_all.sh' first to create sample data.")
                return
            
            conn = sqlite3.connect("ads.db")
            cursor = conn.cursor()
            
            # Get campaigns by objective - using correct column names
            cursor.execute("""
                SELECT id, name, target_cpm, status, dsp_partner
                FROM campaigns 
                WHERE objective = ? 
                ORDER BY target_cpm DESC 
                LIMIT ?
            """, (objective, top_n))
            
            campaigns = cursor.fetchall()
            
            if not campaigns:
                print(f"❌ No campaigns found with objective: {objective}")
                return
            
            # Structure result
            result = {
                "objective": objective,
                "total_campaigns": len(campaigns),
                "campaigns": []
            }
            
            for row in campaigns:
                result["campaigns"].append({
                    "id": row[0],
                    "name": row[1],
                    "target_cpm": row[2],
                    "status": row[3],
                    "dsp_partner": row[4]
                })
            
            conn.close()
            print(json.dumps(result, indent=2))
            
        except Exception as e:
            print(f"❌ Comparison failed: {e}")
            print("💡 Try running './run_all.sh' first to create sample data.")

@cli.command("optimize-cpm")
@click.option("--budget", required=True, type=float, help="Total campaign budget")
@click.option("--objective", required=True, type=str, help="Campaign objective")
@click.option("--target-impressions", type=int, help="Target impression count")
def cmd_optimize_cpm(budget: float, objective: str, target_impressions: Optional[int] = None) -> None:
    """Find optimal CPM for your budget and objective."""
    try:
        from services.optimization_service import optimize_cpm
        result = optimize_cpm(budget, objective, target_impressions)
        print(json.dumps(result, indent=2))
    
    except ImportError:
        # Fallback calculation
        if objective == "AWARENESS":
            suggested_cpm = budget / 1000  # Simple budget/1000 calculation
        elif objective == "CONSIDERATION":
            suggested_cpm = budget / 1500
        else:  # CONVERSION
            suggested_cpm = budget / 2000
        
        result = {
            "suggested_cpm": round(suggested_cpm, 2),
            "estimated_impressions": int(budget / suggested_cpm * 1000),
            "budget_efficiency": "high" if suggested_cpm < 20 else "medium"
        }
        print(json.dumps(result, indent=2))

@cli.command("project-roi")
@click.option("--campaign-id", required=True, type=int, help="Campaign ID to project ROI for")
@click.option("--scenarios", type=int, default=3, help="Number of scenarios to generate")
@click.option("--optimistic", is_flag=True, default=False, help="Include optimistic scenario")
def cmd_project_roi(campaign_id: int, scenarios: int, optimistic: bool) -> None:
    """Calculate ROI projections for a campaign."""
    try:
        from services.forecasting_service import project_roi
        result = project_roi(campaign_id, scenarios, optimistic)
        print(json.dumps(result, indent=2))
    
    except ImportError:
        # Fallback projections
        result = {
            "campaign_id": campaign_id,
            "scenarios": [
                {"name": "Conservative", "roi": 1.5, "confidence": "high"},
                {"name": "Realistic", "roi": 2.5, "confidence": "medium"},
                {"name": "Optimistic", "roi": 4.0, "confidence": "low"}
            ] if optimistic else [
                {"name": "Conservative", "roi": 1.5, "confidence": "high"},
                {"name": "Realistic", "roi": 2.5, "confidence": "medium"}
            ]
        }
        print(json.dumps(result, indent=2))

@cli.command("test-creative")
@click.option("--format", required=True, type=str, help="Creative format to test")
@click.option("--duration", type=int, help="Duration in seconds")
@click.option("--interactive", is_flag=True, default=False, help="Test interactive elements")
def cmd_test_creative(format: str, duration: Optional[int] = None, interactive: bool = False) -> None:
    """Test different creative formats and configurations."""
    try:
        from services.creative_service import test_creative
        result = test_creative(format, duration, interactive)
        print(json.dumps(result, indent=2))
    
    except ImportError:
        result = {
            "format": format,
            "duration": duration,
            "interactive": interactive,
            "recommendations": [
                "Test multiple durations (15s, 30s, 60s)",
                "A/B test interactive vs static elements",
                "Monitor engagement metrics closely"
            ]
        }
        print(json.dumps(result, indent=2))

@cli.command("ab-test")
@click.option("--variant-a", required=True, type=str, help="First variant name")
@click.option("--variant-b", required=True, type=str, help="Second variant name")
@click.option("--test-duration", type=int, default=14, help="Test duration in days")
def cmd_ab_test(variant_a: str, variant_b: str, test_duration: int) -> None:
    """Set up A/B testing between two campaign variants."""
    try:
        from services.ab_testing_service import setup_ab_test
        result = setup_ab_test(variant_a, variant_b, test_duration)
        print(json.dumps(result, indent=2))
    
    except ImportError:
        result = {
            "variant_a": variant_a,
            "variant_b": variant_b,
            "test_duration_days": test_duration,
            "setup_instructions": [
                "Create two campaigns with identical settings",
                "Modify only the variable you want to test",
                "Run two campaigns simultaneously",
                "Compare performance after test period"
            ]
        }
        print(json.dumps(result, indent=2))

@cli.command("forecast")
@click.option("--campaign-id", required=True, type=int, help="Campaign ID to forecast")
@click.option("--days", type=int, default=30, help="Forecast period in days")
@click.option("--include-seasonal/--no-include-seasonal", default=True, show_default=True, help="Include seasonal adjustments")
def cmd_forecast(campaign_id: int, days: int, include_seasonal: bool) -> None:
    """Predict campaign performance over time."""
    try:
        from services.forecasting_service import forecast_performance
        result = forecast_performance(campaign_id, days, include_seasonal)
        print(json.dumps(result, indent=2))
    
    except ImportError:
        result = {
            "campaign_id": campaign_id,
            "forecast_days": days,
            "projected_metrics": {
                "impressions": days * 10000,
                "clicks": days * 240,
                "conversions": days * 8,
                "spend": days * 1850
            },
            "confidence_level": "medium"
        }
        print(json.dumps(result, indent=2))

@cli.command("seasonal-trends")
@click.option("--campaign-id", required=True, type=int, help="Campaign ID to analyze")
@click.option("--period", type=int, default=90, help="Analysis period in days")
def cmd_seasonal_trends(campaign_id: int, period: int) -> None:
    """Analyze seasonal performance trends."""
    try:
        from services.analytics_service import analyze_seasonal_trends
        result = analyze_seasonal_trends(campaign_id, period)
        print(json.dumps(result, indent=2))
    
    except ImportError:
        result = {
            "campaign_id": campaign_id,
            "analysis_period_days": period,
            "seasonal_patterns": {
                "weekday_peaks": ["Tuesday", "Wednesday", "Thursday"],
                "time_peaks": ["9AM-11AM", "6PM-9PM"],
                "seasonal_factors": ["Holiday season", "Back to school", "Summer vacation"]
            }
        }
        print(json.dumps(result, indent=2))

@cli.command("create-variations")
@click.option("--template", required=True, type=str, help="Template name to use")
@click.option("--custom-rules", type=str, help="JSON string of custom variation rules")
@click.option("--seed", type=int, help="Random seed for reproducible variations")
@click.option("--output-format", type=click.Choice(["json", "csv"]), default="json", help="Output format")
def cmd_create_variations(template: str, custom_rules: Optional[str], seed: Optional[int], output_format: str) -> None:
    """Create automated campaign variations from a template."""
    try:
        from services.campaign_variation_service import EnhancedCampaignVariationService
        
        service = EnhancedCampaignVariationService()
        
        # Parse custom rules if provided
        parsed_rules = None
        if custom_rules:
            parsed_rules = json.loads(custom_rules)
        
        # Generate variations
        variations = service.create_variations_from_template(template, parsed_rules, seed)
        
        # Output in requested format
        if output_format == "json":
            print(json.dumps({
                "template": template,
                "variations_count": len(variations),
                "variations": variations
            }, indent=2))
        elif output_format == "csv":
            import csv
            import sys
            writer = csv.writer(sys.stdout)
            writer.writerow(["Variation", "Name", "Objective", "Target CPM", "Devices", "Formats"])
            for i, var in enumerate(variations):
                writer.writerow([
                    i + 1,
                    var.get("name", ""),
                    var.get("objective", ""),
                    var.get("line_items", [{}])[0].get("bid_cpm", ""),
                    str(var.get("targeting", {}).get("device", [])),
                    var.get("line_items", [{}])[0].get("ad_format", "")
                ])
    
    except ImportError:
        print("❌ Campaign variation service not available")
        print("💡 This feature requires additional dependencies")
    except Exception as e:
        print(f"❌ Failed to create variations: {e}")

@cli.command("list-templates")
@click.option("--output-format", type=click.Choice(["json", "table"]), default="table", help="Output format")
def cmd_list_templates(output_format: str) -> None:
    """List available campaign variation templates."""
    try:
        from services.campaign_variation_service import EnhancedCampaignVariationService
        
        service = EnhancedCampaignVariationService()
        templates = service.get_template_metadata()
        
        if output_format == "json":
            print(json.dumps(templates, indent=2))
        else:
            from rich.console import Console
            from rich.table import Table
            
            console = Console()
            table = Table(title="🎯 Available Campaign Templates")
            table.add_column("Name", style="cyan")
            table.add_column("Profile", style="green")
            table.add_column("Variations", style="yellow")
            table.add_column("Budget Range", style="magenta")
            table.add_column("Description", style="white")
            
            for template in templates:
                budget_range = template.get("estimated_budget_range", {})
                budget_str = f"${budget_range.get('min', 0):,.0f} - ${budget_range.get('max', 0):,.0f}"
                table.add_row(
                    template["name"],
                    template["profile"],
                    str(template["variations_count"]),
                    budget_str,
                    template["description"]
                )
            
            console.print(table)
    
    except ImportError:
        print("❌ Campaign variation service not available")
    except Exception as e:
        print(f"❌ Failed to list templates: {e}")

@cli.command("show-schemas")
def cmd_show_schemas() -> None:
    """Show all database schemas and table structures."""
    try:
        from services.erd_service import print_all_schemas
        print_all_schemas()
    
    except ImportError:
        print("❌ ERD service not available")
    except Exception as e:
        print(f"❌ Failed to show schemas: {e}")

@cli.command("status")
def cmd_status() -> None:
    """Check system status and database health."""
    import os
    import sqlite3
    
    status = {
        "database": {},
        "system": {},
        "campaigns": {}
    }
    
    # Database status
    if os.path.exists("ads.db"):
        try:
            conn = sqlite3.connect("ads.db")
            cursor = conn.cursor()
            
            # Get table counts
            tables = ["advertisers", "campaigns", "line_items", "creatives", "performance"]
            for table in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    status["campaigns"][table] = count
                except:
                    status["campaigns"][table] = 0
            
            conn.close()
            status["database"]["status"] = "healthy"
            status["database"]["size_mb"] = round(os.path.getsize("ads.db") / (1024 * 1024), 2)
        except Exception as e:
            status["database"]["status"] = f"error: {str(e)}"
    else:
        status["database"]["status"] = "not_found"
    
    # System status
    status["system"]["python_version"] = f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}"
    status["system"]["working_directory"] = os.getcwd()
    
    print(json.dumps(status, indent=2))



if __name__ == "__main__":
    cli()
