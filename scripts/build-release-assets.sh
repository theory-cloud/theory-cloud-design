#!/usr/bin/env bash
# Build the theory-cloud-design release tarball asset.
#
# Usage:   scripts/build-release-assets.sh <VERSION> <OUT_DIR>
# Example: scripts/build-release-assets.sh 0.1.0 dist
#
# Produces:
#   <OUT_DIR>/theory-cloud-design-<VERSION>.tgz
#
# The tarball is the output of `npm pack` inside `ts/`. `prepack`
# takes care of `npm run clean && npm run build` before pack, so the
# artifact is always a fresh, deterministic build.

set -euo pipefail

VERSION="${1:-}"
OUT_DIR="${2:-dist}"

if [[ -z "${VERSION}" ]]; then
  echo "build-release-assets: FAIL (missing VERSION argument)" >&2
  echo "usage: scripts/build-release-assets.sh <VERSION> <OUT_DIR>" >&2
  exit 1
fi

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TS_DIR="${REPO_ROOT}/ts"

# Resolve OUT_DIR as absolute if given relative, so OUT_PATH never
# concatenates into something like `${REPO}//tmp/x`.
if [[ "${OUT_DIR}" = /* ]]; then
  OUT_PATH="${OUT_DIR}"
else
  OUT_PATH="${REPO_ROOT}/${OUT_DIR}"
fi

mkdir -p "${OUT_PATH}"

# Align ts/package.json + lockfile version to the release version so
# `npm pack` produces `theory-cloud-design-<VERSION>.tgz`. Release-please
# is expected to have updated these already on the release commit; this
# step is a defensive alignment in case the workflow runs against a
# detached tag checkout or a developer invokes this script locally.
#
# Snapshot the original version and restore it after pack so local
# invocations do not leave the working tree dirty.
ORIG_VERSION="$(node -p "require('${TS_DIR}/package.json').version" 2>/dev/null || echo '')"

restore_version() {
  if [[ -n "${ORIG_VERSION}" && "${ORIG_VERSION}" != "${VERSION}" ]]; then
    (
      cd "${TS_DIR}"
      npm pkg set version="${ORIG_VERSION}" >/dev/null
      if [[ -f package-lock.json ]]; then
        npm install --package-lock-only --silent
      fi
    )
  fi
}
trap restore_version EXIT

(
  cd "${TS_DIR}"
  npm pkg set version="${VERSION}" >/dev/null
  if [[ -f package-lock.json ]]; then
    npm install --package-lock-only --silent
  fi
  npm pack --pack-destination "${OUT_PATH}"
)

EXPECTED="${OUT_PATH}/theory-cloud-design-${VERSION}.tgz"
if [[ ! -f "${EXPECTED}" ]]; then
  echo "build-release-assets: FAIL (expected ${EXPECTED} missing)" >&2
  ls -la "${OUT_PATH}" >&2
  exit 1
fi

echo "build-release-assets: ${EXPECTED}"
