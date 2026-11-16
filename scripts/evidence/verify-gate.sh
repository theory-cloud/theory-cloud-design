#!/usr/bin/env bash
# Purpose: verify one gate's tracked evidence record against this tree.
#
# This is the CI entry point, and it verifies only. CI never executes a gate:
# gates are verified once, on the pull request into staging, from a record the
# steward produced locally. A record applies when its recorded input digests,
# its proof profile and its approved command set all match this tree, and a
# catch-all gate's composed dependencies still apply too. A missing, stale,
# mismatched or failed record fails the job with the command that produces one
# locally.
#
# Fork pull requests are not special-cased: a fork cannot carry a record
# produced here, so it fails closed like any other untrusted origin. External
# contributions arrive through a pre-arranged branch negotiated with CODEOWNERS,
# and a code owner carries the change into staging with local evidence.
#
# Exit codes: 0 the record applies to this tree; 1 no applicable record.
#
# Usage: scripts/evidence/verify-gate.sh --gate <gate-id> [--profile <id>]
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${repo_root}"

gate=""
profile=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --gate)
      gate="${2:-}"
      shift 2
      ;;
    --profile)
      profile="${2:-}"
      shift 2
      ;;
    --help|-h)
      cat <<'USAGE'
usage: scripts/evidence/verify-gate.sh --gate <gate-id> [--profile <id>]

Verifies the gate's reviewed evidence record for the requested proof profile.
Nothing is executed: when no record applies, this prints the local collection
command and exits 1.
USAGE
      exit 0
      ;;
    *)
      echo "verify-gate: FAIL (unknown argument: $1)" >&2
      exit 1
      ;;
  esac
done

if [[ -z "${gate}" ]]; then
  echo "verify-gate: FAIL (--gate is required)" >&2
  exit 1
fi

profile_args=()
if [[ -n "${profile}" ]]; then
  profile_args=(--profile "${profile}")
fi

summary_line() {
  if [[ -n "${GITHUB_STEP_SUMMARY:-}" ]]; then
    printf '%s\n' "$1" >>"${GITHUB_STEP_SUMMARY}"
  fi
}

verify_stderr="$(mktemp)"
trap 'rm -f "${verify_stderr}"' EXIT

if python3 scripts/evidence/validation_evidence.py verify --gate "${gate}" "${profile_args[@]}" 2>"${verify_stderr}"; then
  cat "${verify_stderr}" >&2 || true
  echo "gate ${gate}: evidence-verified (no command executed in this run)"
  summary_line "- \`${gate}\`: evidence-verified from the reviewed local record (not executed in this run)"
  exit 0
fi

cat "${verify_stderr}" >&2 || true
reason="$(grep -m1 'validation-evidence: FAIL' "${verify_stderr}" || true)"
echo "gate ${gate}: no applicable evidence record (${reason:-no applicable record})" >&2
echo "produce evidence locally: run 'make rubric' on this tree and commit the record it writes; CI verifies records and never executes a gate" >&2
summary_line "- \`${gate}\`: FAILED, no applicable evidence record; produce evidence locally"
exit 1
