# theory-cloud-design

The **Theory Cloud brand pack** — a publishable TypeScript package of
populated design tokens and canonical brand assets consumed by
FaceTheory-based Theory Cloud applications.

This repo is the authoritative source for:

- the Theory Cloud **token sets** — a dark-first base plus per-surface
  variants for **Core**, **MCP**, and **Auth** — all shape-compatible
  with `StitchTokenSet` from `@theory-cloud/facetheory`;
- the **icon and asset set** — primary icon, monochrome variants,
  favicon family, and social / OG card, generated from SVG masters;
- the **master brand document** (`theory_cloud_branding_package.md`) —
  the specification every token, asset, and rule in this repo
  implements.

theory-cloud-design is **not open source** and **not published to npm**.
It ships as pinned GitHub release tarballs, consumed through
`package.json` by each downstream Theory Cloud app.

## Installation

Consumers pin the tarball asset directly from the corresponding GitHub
release:

```bash
export THEORY_CLOUD_DESIGN_VERSION=0.0.0 # x-release-please-version
npm install --save-exact \
  "https://github.com/theory-cloud/theory-cloud-design/releases/download/v${THEORY_CLOUD_DESIGN_VERSION}/theory-cloud-design-${THEORY_CLOUD_DESIGN_VERSION}.tgz"
```

`@theory-cloud/facetheory` is a peer dependency — consumers install
both packages side-by-side.

## Usage

```ts
import { theoryCloudCoreTokens } from "@theory-cloud/design/tokens/core";
import { theoryCloudMcpTokens  } from "@theory-cloud/design/tokens/mcp";
import { theoryCloudAuthTokens } from "@theory-cloud/design/tokens/auth";
import { iconPath, ogCardPngPath } from "@theory-cloud/design/assets";
```

Every surface composes over a shared base, so drift between surfaces
stays narrow by construction — see §29.E of the brand document.

## Surfaces

| Surface | Domain           | Accent emphasis                                        |
| ------- | ---------------- | ------------------------------------------------------ |
| Core    | `theorycloud.ai` | Balanced Core Blue; stable, authoritative              |
| MCP     | `theorymcp.ai`   | Slightly stronger Violet Signal; active, agentic       |
| Auth    | `autheory.app`   | Restrained accent, neutral surface tint; trust-forward |

The three surfaces always carry the **Theory Cloud [Surface]** header
pattern (§30.C). Consumer apps consume this pack through
FaceTheory's `BrandHeader` primitive; the surface chip sits beside the
Theory Cloud wordmark, never replaces it.

## Layout

```
theory-cloud-design/
├── assets/                       canonical SVG masters + generated rasters
│   ├── icon.svg                  primary full-color icon
│   ├── icon-mono-light.svg       Ice White monochrome (for dark surfaces)
│   ├── icon-mono-dark.svg        Graphite monochrome (for light surfaces)
│   ├── favicon/                  PNG favicon set (16/32/48/192/512)
│   ├── favicon.ico               multi-resolution ICO bundle
│   ├── og-card.svg               social / OG card master
│   └── og-card.png               social / OG card (1200×630)
├── scripts/
│   ├── build-assets.py           regenerates raster derivatives from SVG
│   └── build-release-assets.sh   packages the release tarball
├── ts/
│   ├── package.json              @theory-cloud/design — published shape
│   ├── tsconfig.json             ESM + declaration output
│   ├── src/
│   │   ├── index.ts              top-level re-exports
│   │   ├── assets.ts             typed asset path constants
│   │   └── tokens/
│   │       ├── base.ts           shared Theory Cloud StitchTokenSet
│   │       ├── core.ts           Core variant
│   │       ├── mcp.ts            MCP variant
│   │       ├── auth.ts           Auth variant
│   │       └── index.ts
│   └── scripts/copy-assets.mjs   stages assets/ into ts/dist/assets/
├── theory_cloud_branding_package.md   master brand specification
├── VERSION                       tracked by release-please
├── release-please-config.json            stable release pipeline
└── release-please-config.premain.json    prerelease pipeline
```

## Development

```bash
make install     # npm ci inside ts/
make assets      # regenerate raster assets from SVG masters
make build       # tsc + stage assets into ts/dist/
make typecheck   # tsc --noEmit
make check       # typecheck (placeholder for lint + tests)
make pack        # npm pack --dry-run inside ts/
```

The raster pipeline uses `cairosvg` and `Pillow` (Python). SVG stays
the authoring format; rasters are always regenerated from the vector
masters.

## Release cadence

theory-cloud-design follows the same three-branch release flow as
FaceTheory, AppTheory, and TableTheory:

```
feature/*  ──merge──▶  staging  ──merge PR──▶  premain  ──merge PR──▶  main
                          ▲                     │                      │
                          └────── back-merge ───┴──────────────────────┘
                                     after stable release
```

- **`staging`** — integration branch. All work lands here first.
- **`premain`** — prerelease branch. Merges from `staging` trigger
  `v0.Y.Z-rc.N` prerelease tags via release-please.
- **`main`** — stable branch. Merges from `premain` trigger `v0.Y.Z`
  stable tags via release-please.

Releases are **immutable**. Published tags are never retagged; release
assets are never overwritten. The pipeline refuses to re-upload to an
already-published release — any change requires a new version moving
through the pipeline.

Conventional Commits drive the version bump:

- `feat:` → minor
- `fix:` → patch
- `feat!:` / `fix!:` / `BREAKING CHANGE:` → major (pre-1.0 per semver convention)
- `docs:` / `chore:` / `refactor:` / `style:` / `test:` / `ci:` — no release

Each release uploads one asset:

```
theory-cloud-design-${VERSION}.tgz
```

reachable at

```
https://github.com/theory-cloud/theory-cloud-design/releases/download/v${VERSION}/theory-cloud-design-${VERSION}.tgz
```

## Ownership

This repo is stewarded as the Theory Cloud brand pack. Consumers
— FaceTheory, autheory, theory-mcp-server — pin release tarballs and
reskin against this package; they do not edit it. Changes that ripple
downstream are coordinated through the
`Theory Cloud Design System — v1 Rollout` Linear project.
