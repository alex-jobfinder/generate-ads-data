Docs Guide
==========

This guide explains how to build and preview the documentation locally, how it
is structured, and how to prepare for production publishing.

Local Development
-----------------

- Install dev dependencies:

  .. code-block:: bash

     poetry install

- Live preview with auto-reload:

  .. code-block:: bash

     make docs-serve

  Opens a live server at http://127.0.0.1:8000 that rebuilds on file changes.

- One-off build:

  .. code-block:: bash

     make docs-html

  Open ``docs/_build/html/index.html`` in your browser.

- Strict build (warnings as errors):

  .. code-block:: bash

     make docs-html-strict


Structure
---------

- ``docs/cli_commands.rst`` uses ``sphinx-click`` to render the actual Click
  command tree from ``cli.py`` (names, options, help). This is the best source
  for CLI usage documentation.
- ``docs/api/cli.rst`` uses ``autodoc`` and Napoleon (Google-style docstrings)
  to render the Python API reference for the CLI module and its functions.
- ``docs/conf.py`` configures Sphinx, enables ``autodoc``, ``napoleon``,
  ``autosummary``, and ``sphinx-click``. It also mocks heavy project modules
  so docs build without requiring services or a database.


Writing Docstrings
------------------

- Use Google-style (Napoleon) docstrings for functions and modules:

  .. code-block:: python

     def cmd_init_db(log_level: str | None = None) -> None:
         """Initialize a fresh database.

         Args:
             log_level: Log verbosity (e.g., "INFO", "DEBUG").

         Returns:
             None

         Examples:
             CLI:
                 $ python cli.py init-db --log-level INFO
         """

- For CLI commands, keep the first line short (one-sentence summary) and add a
  short CLI example when helpful.


Testing Docs
------------

- A small smoke test is provided at ``tests/test_docs_cli.py``:

  - Validates that the `init-db` command is registered in the Click tree and
    has a docstring.
  - Builds a temporary docs site and ensures the key pages exist.


Preparing for Production
------------------------

- CI: A workflow is included at ``.github/workflows/docs-ci.yml`` that builds
  the docs in strict mode and runs tests on push/PR.

- Publishing to GitHub Pages (example):

  1. Enable GitHub Pages in your repo (Settings → Pages), selecting the
     ``gh-pages`` branch (Deploy from a branch) or GitHub Actions.
  2. Add a deploy workflow. For example, using ``peaceiris/actions-gh-pages``:

     .. code-block:: yaml

        name: Deploy Docs
        on:
          push:
            branches: [ main ]

        jobs:
          deploy:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v4
              - uses: actions/setup-python@v5
                with:
                  python-version: '3.10'
              - uses: snok/install-poetry@v1
              - run: poetry install --no-interaction
              - run: make docs-html
              - name: Deploy to GitHub Pages
                uses: peaceiris/actions-gh-pages@v3
                with:
                  github_token: ${{ secrets.GITHUB_TOKEN }}
                  publish_dir: docs/_build/html

  3. After the first successful run, your docs will be available at the Pages
     URL shown in your repo settings.


Troubleshooting
---------------

- If imports fail during docs build, add the offending module path to
  ``autodoc_mock_imports`` in ``docs/conf.py``.
- If you see type-hint resolution warnings from Click, consider disabling
  rendering of typehints with:

  .. code-block:: python

     autodoc_typehints = "none"

- On strict builds, tune or suppress warnings as needed, or run the non-strict
  target locally (``make docs-html``).

