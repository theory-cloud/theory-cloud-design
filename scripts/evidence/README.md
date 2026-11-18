# Evidence and rubric

This repository has one rubric entry point and one record. `make rubric` runs
every gate locally and writes the records under `evidence/`; CI runs only the
verification, on pull requests to `staging`.

## What "passing" means

- An item passes when its verifier result is in a locally produced, input-bound
  record that CI verifies on pull requests to `staging`.
- The record binds the exact tracked inputs the verifier ran against. CI
  recomputes those projections and checks the record still applies to the pull
  request tree. It never executes a gate.
- A missing, stale or non-`PASS` record fails the pull request with "produce
  evidence locally" and the command that produces one.
- No gate runs on a push, and no gate runs on a release-branch pull request: the
  merged tree is the tree the pull request already verified.

## The rubric

| Gate | Scope | Commands | Profile |
| --- | --- | --- | --- |
| `raster` | `assets/`, `scripts/build-assets.py`, `scripts/requirements.txt` | `python3 scripts/build-assets.py`, `git diff --exit-code -- assets/` | `linux-arm64` |
| `checks` | `ts/` | `npm ci`, `npm run check` (`typecheck` + `typecheck:facetheory`) | `linux-arm64` |
| `package` | `ts/`, `assets/` | `npm run build`, `npm pack --dry-run` | `linux-arm64` |
| `rubric` | `**` | none; composes `raster`, `checks` and `package` | `linux-arm64` |

The npm commands run with `ts/` as their working directory, matching the
Makefile.

`rubric` is the catch-all gate. Its scope is every tracked path, so an edit to
the evidence tooling, the registry, a workflow or this document stales it and
forces a fresh local run. It is the gate CI verifies.

## Producing a record

```bash
make rubric            # every gate, in the pinned producer
make rubric-force      # re-execute even when a record already applies
```

Both targets run `scripts/evidence/linux-producer.sh`, which starts the pinned
producer image (`node:24-slim` by digest, arm64 under colima) and collects the
gates inside it. The record must be produced there: the favicon ICO frames are
zlib-compressed, so only the Linux raster toolchain reproduces the committed
bytes, and the macOS host produces a different ICO. Collecting on the host fails
the profile's environment check on purpose.

Then:

1. Commit the record **records-only**. The commit touches nothing outside
   `evidence/`. A paired reviewer checks that commit's diff.
2. CI verifies it: `bash scripts/evidence/verify-gate.sh --gate rubric`.

## Verifying locally

```bash
make verify-evidence   # what CI runs
```

## Changing the gate set

Edit `scripts/evidence/validation-gates.json`. Pin tools; never use `latest`. A
gate's scope must name every tracked input its commands read, and its record must
be re-produced in the same pull request. Do not add a second CI command set: a
gate that runs in CI as well as locally is verified twice, and the second run is
the one that flakes.
