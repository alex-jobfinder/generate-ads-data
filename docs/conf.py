import os
import sys
from datetime import datetime
import types

# Ensure the project root is importable (cli.py lives at repo root)
sys.path.insert(0, os.path.abspath(".."))

project = "generate-ads-data"
author = "Your Name"
copyright = f"{datetime.utcnow().year}, {author}"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.githubpages",
    "sphinx.ext.autosummary",
]
# Make sphinx-click optional for environments without the plugin
try:  # type: ignore
    import sphinx_click  # noqa: F401

    extensions.append("sphinx_click")
except Exception:
    pass

# Optionally enable typehint rendering extension if installed
try:  # type: ignore
    import sphinx_autodoc_typehints  # noqa: F401

    extensions.append("sphinx_autodoc_typehints")
except Exception:
    pass

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

# Avoid import errors for optional/heavy deps when building docs
# Mock heavy/optional dependencies and local service layers to avoid
# side effects during autodoc imports. This keeps CLI docs generation
# fast and stable even if services are unavailable.
autodoc_mock_imports = [
    # External heavy deps
    "dbt-duckdb",
    "dbt_metricflow",
    "pandas",
    "sqlalchemy",
    "rich",
    "faker",
    # Project modules that perform IO/DB or import heavy stacks
    "db_utils",
    "factories",
    "factories.faker_providers",
    "models",
    "models.registry",
    "services",
    "services.generator",
    "services.performance_ext",
    "services.processor",
    "services.campaign_service",
    "services.export_service",
    "services.comparison_service",
    "services.optimization_service",
    "services.forecasting_service",
    "services.creative_service",
    "services.ab_testing_service",
    "services.analytics_service",
    "services.campaign_variation_service",
    "services.erd_service",
]

# Ensure these modules are importable for sphinx-click as well by injecting
# lightweight shims into sys.modules before Sphinx imports the project.
_MOCK_MODULES = list(autodoc_mock_imports)
for _mod in _MOCK_MODULES:
    if _mod not in sys.modules:
        # Create a module placeholder with permissive attribute access
        m = types.ModuleType(_mod)
        def _getattr(name, _m=m):  # type: ignore
            # Return a dummy callable/type for any attribute
            d = types.SimpleNamespace()
            setattr(_m, name, d)
            return d
        m.__getattr__ = _getattr  # type: ignore
        sys.modules[_mod] = m

# Theme (fallback to alabaster if RTD theme is unavailable)
try:  # type: ignore
    import sphinx_rtd_theme  # noqa: F401

    html_theme = "sphinx_rtd_theme"
except Exception:
    html_theme = "alabaster"
html_static_path = ["_static"]

# Autosummary settings
autosummary_generate = True
