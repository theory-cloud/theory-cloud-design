#!/usr/bin/env bash
# Purpose: produce the reviewed evidence records for approved gates.
#
# The collector executes only the command IDs in
# scripts/evidence/validation-gates.json, records their real exit codes, and
# binds the exact working-tree inputs they ran against. It refuses a dirty tree,
# and it refuses to publish a PASS when inputs changed during the run.
#
# Every record is produced inside the pinned Linux producer container, because
# the raster claim is only reproducible with the Linux raster toolchain. Use
# scripts/evidence/linux-producer.sh; calling this script directly on the macOS
# host fails the proof profile's environment check on purpose.
#
# Usage:
#   scripts/evidence/collect.sh --all
#   scripts/evidence/collect.sh --gate checks --gate package
#   scripts/evidence/collect.sh --gate raster --force
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/../.."

exec python3 scripts/evidence/validation_evidence.py collect "$@"
