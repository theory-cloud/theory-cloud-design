# Theory Cloud — theory-cloud-design Makefile.
#
# Convenience targets that wrap the npm scripts inside `ts/` and the
# repo-level asset build. Mirrors FaceTheory's Makefile conventions so
# downstream stewards see a consistent shape across Theory Cloud repos.

.PHONY: help install build typecheck check clean assets pack

TS_DIR := ts

help:
	@echo "theory-cloud-design targets:"
	@echo "  install    — npm ci inside ts/"
	@echo "  assets     — rebuild raster assets from SVG masters"
	@echo "  build      — tsc + stage assets into ts/dist/"
	@echo "  typecheck  — tsc --noEmit"
	@echo "  check      — typecheck (placeholder for lint + tests)"
	@echo "  pack       — npm pack --dry-run inside ts/"
	@echo "  clean      — remove ts/dist and ts/node_modules"

install:
	cd $(TS_DIR) && npm ci

assets:
	python3 scripts/build-assets.py

build:
	cd $(TS_DIR) && npm run build

typecheck:
	cd $(TS_DIR) && npm run typecheck

check:
	cd $(TS_DIR) && npm run check

pack:
	cd $(TS_DIR) && npm pack --dry-run

clean:
	cd $(TS_DIR) && npm run clean && rm -rf node_modules
