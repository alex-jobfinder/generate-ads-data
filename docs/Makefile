# Minimal Sphinx makefile
#
# Usage:
#   make html

SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
AUTOBUILD     = sphinx-autobuild
SOURCEDIR     = .
BUILDDIR      = _build
PORT          = 8000

.PHONY: help Makefile cli-guide

help:
	@echo "Available commands:"
	@echo "  html          - Build HTML documentation"
	@echo "  html-strict   - Build HTML with warnings as errors"
	@echo "  serve         - Serve documentation with auto-reload on port $(PORT)"
	@echo "  clean         - Remove build files"
	@echo "  cli-guide     - Show CLI development guide and file locations"
	@echo ""
	@echo "For Sphinx-specific help:"
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

html:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

html-strict:
	@$(SPHINXBUILD) -W -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)

serve:
	@$(AUTOBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O) \
		--watch .. --port $(PORT) --ignore "$(BUILDDIR)/*"

clean:
	rm -rf "$(BUILDDIR)"

# CLI Development Guide - Shows files to edit when adding/editing/removing CLI methods
cli-guide:
	@echo "=========================================="
	@echo "CLI DEVELOPMENT GUIDE"
	@echo "=========================================="
	@echo ""
	@echo "📁 FILES TO EDIT WHEN ADDING/EDITING/REMOVING CLI METHODS:"
	@echo ""
	@echo "1️⃣  CLI GROUP IMPLEMENTATION FILES:"
	@echo "   📄 cli_groups/campaign.py     - Campaign commands (create, list, export, etc.)"
	@echo "   📄 cli_groups/analysis.py     - Analysis commands (compare, forecast, ROI, etc.)"
	@echo "   📄 cli_groups/system.py       - System commands (schemas, status)"
	@echo "   📄 cli_groups/db.py           - Database commands (init, migrate)"
	@echo "   📄 cli_groups/variation.py    - Variation commands (create, list templates)"
	@echo ""
	@echo "2️⃣  DOCUMENTATION FILES:"
	@echo "   📄 docs/api/cli.rst           - Main CLI autosummary (add cmd_<name> entries)"
	@echo "   📄 docs/api/campaign_api.rst  - Campaign callback documentation"
	@echo "   📄 docs/api/analysis_api.rst  - Analysis callback documentation"
	@echo "   📄 docs/api/system_api.rst    - System callback documentation"
	@echo "   📄 docs/api/db_api.rst        - Database callback documentation"
	@echo "   📄 docs/api/variation_api.rst - Variation callback documentation"
	@echo ""
	@echo "3️⃣  MAIN CLI FILE:"
	@echo "   📄 cli.py                     - Main CLI entry point (if adding new groups)"
	@echo ""
	@echo "=========================================="
	@echo "STEP-BY-STEP INSTRUCTIONS:"
	@echo "=========================================="
	@echo ""
	@echo "🆕 ADDING A NEW CLI METHOD:"
	@echo "   1. Add @<group>.command('method-name') function in cli_groups/<group>.py"
	@echo "   2. Add cb_<method_name> = cmd_<method_name>.callback alias at bottom of file"
	@echo "   3. Add cli.cmd_<method_name> entry to docs/api/cli.rst autosummary"
	@echo "   4. Add cb_<method_name> to docs/api/<group>_api.rst members list"
	@echo "   5. Run 'make html' to rebuild documentation"
	@echo ""
	@echo "✏️  EDITING AN EXISTING CLI METHOD:"
	@echo "   1. Modify the @<group>.command function in cli_groups/<group>.py"
	@echo "   2. Update docstring if needed (Args/Returns/Examples)"
	@echo "   3. Run 'make html' to rebuild documentation"
	@echo ""
	@echo "🗑️  REMOVING A CLI METHOD:"
	@echo "   1. Remove @<group>.command function from cli_groups/<group>.py"
	@echo "   2. Remove cb_<method_name> alias from cli_groups/<group>.py"
	@echo "   3. Remove cli.cmd_<method_name> entry from docs/api/cli.rst"
	@echo "   4. Remove cb_<method_name> from docs/api/<group>_api.rst members list"
	@echo "   5. Run 'make html' to rebuild documentation"
	@echo ""
	@echo "🆕 ADDING A NEW CLI GROUP:"
	@echo "   1. Create cli_groups/<new_group>.py with @click.group decorator"
	@echo "   2. Add import and group registration in cli_groups/__init__.py"
	@echo "   3. Add group to main CLI in cli.py"
	@echo "   4. Create docs/api/<new_group>_api.rst file"
	@echo "   5. Add docs/api/<new_group>_api to docs/index.rst toctree"
	@echo "   6. Run 'make html' to rebuild documentation"
	@echo ""
	@echo "=========================================="
	@echo "QUICK NAVIGATION COMMANDS:"
	@echo "=========================================="
	@echo ""
	@echo "📂 Navigate to CLI groups:"
	@echo "   cd ../cli_groups"
	@echo ""
	@echo "📂 Navigate to docs:"
	@echo "   cd docs"
	@echo ""
	@echo "📂 Navigate to API docs:"
	@echo "   cd docs/api"
	@echo ""
	@echo "🔍 View current callback aliases:"
	@echo "   grep -r 'cb_.*=.*\.callback' ../cli_groups/"
	@echo ""
	@echo "🔍 View current CLI commands in docs:"
	@echo "   grep -A 20 'autosummary::' docs/api/cli.rst"
	@echo ""
	@echo "=========================================="
	@echo "USEFUL COMMANDS:"
	@echo "=========================================="
	@echo ""
	@echo "📖 Build documentation:"
	@echo "   make html"
	@echo ""
	@echo "🌐 Serve documentation locally:"
	@echo "   make serve"
	@echo ""
	@echo "🧹 Clean build files:"
	@echo "   make clean"
	@echo ""
	@echo "❓ Show this guide again:"
	@echo "   make cli-guide"
	@echo ""
	@echo "=========================================="
