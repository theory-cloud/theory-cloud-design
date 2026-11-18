# Theory Cloud — theory-cloud-design Makefile.
#
# Convenience targets that wrap the npm scripts inside `ts/` and the
# repo-level asset build. Mirrors FaceTheory's Makefile conventions so
# downstream stewards see a consistent shape across Theory Cloud repos.

.PHONY: help install build typecheck check clean assets pack rubric rubric-force verify-evidence

TS_DIR := ts

help:
	@echo "theory-cloud-design targets:"
	@echo "  install         — npm ci inside ts/"
	@echo "  assets          — rebuild raster assets from SVG masters"
	@echo "  build           — tsc + stage assets into ts/dist/"
	@echo "  typecheck       — tsc --noEmit"
	@echo "  check           — typecheck + the FaceTheory StitchTokenSet contract typecheck"
	@echo "  pack            — npm pack --dry-run inside ts/"
	@echo "  clean           — remove ts/dist and ts/node_modules"
	@echo "  rubric          — produce the evidence records in the pinned Linux producer"
	@echo "  rubric-force    — re-execute every gate even when a record already applies"
	@echo "  verify-evidence — verify the committed records (what CI runs)"

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

# The evidence record is produced in the pinned Linux producer, never on the
# macOS host: the favicon ICO frames are zlib-compressed and only the Linux
# raster toolchain reproduces the committed bytes. See scripts/evidence/README.md.
rubric:
	scripts/evidence/linux-producer.sh --all

rubric-force:
	scripts/evidence/linux-producer.sh --all --force

verify-evidence:
	scripts/evidence/verify-gate.sh --gate rubric
