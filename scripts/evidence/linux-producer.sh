#!/usr/bin/env bash
# Purpose: produce the evidence records inside the repository's pinned producer.
#
# The registry declares one proof profile, `linux-arm64`, and every record must
# be produced under it. The producer is the `node:24-slim` image pinned by
# digest below, run arm64 under colima on the steward host. Its Debian release
# supplies git, python3 and libcairo2; the raster toolchain comes from
# scripts/requirements.txt inside the image, so no toolchain is taken from the
# host.
#
# The tree is copied into the container and given its own git index there. This
# checkout's `.git` is a file that points at the parent Factory git directory,
# which does not exist inside the container, and the container must never write
# to it. Collection therefore runs against a content-identical copy, and only
# the records are copied back. The digests in a record are over file content, so
# `make verify-evidence` on the host proves the copy carried this exact tree.
#
# The record's proof profile declares the resulting Node major, Python
# major.minor and libcairo version. Moving the image digest or the Debian
# release therefore fails the producing-environment check until the profile
# declaration is updated in the same commit.
#
# Usage: scripts/evidence/linux-producer.sh [collect arguments]
#   scripts/evidence/linux-producer.sh --all
#   scripts/evidence/linux-producer.sh --gate checks
#   scripts/evidence/linux-producer.sh --all --force
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

producer_image="node@sha256:dc26ae92c9fb15cf6b1d63e20f0944b2efe0f115b20e00be48fb23fceb061c54" # node:24-slim

if ! command -v docker >/dev/null 2>&1; then
  echo "linux-producer: FAIL (docker is required; the raster claim is only reproducible with the Linux toolchain)" >&2
  exit 1
fi

exec docker run --rm --platform linux/arm64 \
  --volume "${repo_root}:/host" \
  "${producer_image}" \
  bash -lc '
    set -euo pipefail

    export DEBIAN_FRONTEND=noninteractive
    apt-get update -qq
    apt-get install -y -qq --no-install-recommends git libcairo2 python3 python3-venv >/dev/null

    # A pristine copy with its own index: /host/.git points at the parent
    # Factory git directory and must not be touched from here.
    mkdir -p /work
    tar -C /host --exclude=./.git --exclude=./.DS_Store \
      --exclude=./ts/node_modules --exclude=./ts/dist -cf - . | tar -C /work -xf -
    cd /work
    git init -q -b staging
    git add -A
    # A baseline commit so `git status` can prove the copy started clean; it
    # never leaves the container.
    git -c user.email=evidence@localhost -c user.name="evidence producer" commit -q -m "evidence baseline"

    python3 -m venv /opt/raster
    /opt/raster/bin/pip install --quiet --disable-pip-version-check -r scripts/requirements.txt
    export PATH="/opt/raster/bin:${PATH}"

    python3 scripts/evidence/validation_evidence.py --root /work collect "$@"

    mkdir -p /host/evidence
    cp -a /work/evidence/. /host/evidence/
    echo "linux-producer: records copied back to evidence/"
  ' linux-producer "$@"
