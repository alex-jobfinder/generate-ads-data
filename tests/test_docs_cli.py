from __future__ import annotations

from pathlib import Path

import click
import pytest


def test_cli_registry_has_init_db() -> None:
    """Verify Click has registered the 'init-db' command and its docstring."""
    from cli import cli as root

    ctx = click.Context(root)
    commands = root.list_commands(ctx)
    assert "init-db" in commands, "'init-db' should be registered on the root CLI"

    cmd = root.get_command(ctx, "init-db")
    assert cmd is not None, "Click command object for 'init-db' not found"
    assert cmd.callback.__doc__ and "Initialize a fresh database" in cmd.callback.__doc__


def test_docs_smoke_build_cli_pages(tmp_path: Path) -> None:
    """Build docs and ensure CLI pages are generated (smoke test only)."""
    pytest.importorskip("sphinx")
    from sphinx.cmd.build import main as sphinx_build_main  # type: ignore

    repo_root = Path(__file__).resolve().parents[1]
    docs_src = repo_root / "docs"
    outdir = tmp_path / "html"

    rc = sphinx_build_main(["-b", "html", "-q", str(docs_src), str(outdir)])
    assert rc == 0, "Sphinx build failed"

    # Ensure both API and CLI pages exist
    assert (outdir / "api" / "cli.html").exists()
    assert (outdir / "cli_commands.html").exists()
