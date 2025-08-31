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

.PHONY: help Makefile

help:
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
