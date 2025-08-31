"""
CLI entrypoints for DB initialization and demo data creation.

The CLI is composed from modular subcommand groups in `cli_groups/`.
Root-level command names are preserved via aliases for backward
compatibility, while grouped commands enable a cleaner structure.
"""
from __future__ import annotations

import click

# Domain groups (Click Group objects)
from cli_groups import db as db_group
from cli_groups import campaign as campaign_group
from cli_groups import analysis as analysis_group
from cli_groups import variation as variation_group
from cli_groups import system as system_group

# Import command objects from groups to expose root-level aliases and keep
# Sphinx autodoc references (e.g., cli.cmd_init_db) intact.
from cli_groups.db import cmd_init_db, cmd_migrate_db
from cli_groups.campaign import (
    cmd_create_advertiser,
    cmd_create_campaign,
    cmd_generate_performance,
    cmd_generate_performance_ext,
    cmd_create_example,
    cmd_test_fields,
    cmd_create_profile,
    cmd_test_scenario,
    cmd_list_campaigns,
    cmd_export_campaign,
)
from cli_groups.analysis import (
    cmd_compare_campaigns,
    cmd_compare_by_objective,
    cmd_optimize_cpm,
    cmd_project_roi,
    cmd_test_creative,
    cmd_ab_test,
    cmd_forecast,
    cmd_seasonal_trends,
)
from cli_groups.variation import cmd_create_variations, cmd_list_templates
from cli_groups.system import cmd_show_schemas, cmd_status


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(package_name="generate-ads-data", prog_name="generate-ads-data")
def cli() -> None:
    """Root command group for ads demo utilities.

    Use ``-h/--help`` on any command to see options and defaults.
    """
    pass


# Register groups on the root
cli.add_command(db_group, name="db")
cli.add_command(campaign_group, name="campaign")
cli.add_command(analysis_group, name="analysis")
cli.add_command(variation_group, name="variation")
cli.add_command(system_group, name="system")


# Note: root-level aliases (e.g., `init-db`) have been removed to
# encourage the grouped style: `cli db init`, `cli campaign create-campaign`, etc.


if __name__ == "__main__":
    cli()
