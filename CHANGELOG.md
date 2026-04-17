# Changelog

All notable changes to `theory-cloud-design` are recorded here.
This file is maintained by
[release-please](https://github.com/googleapis/release-please) from
Conventional Commits on the `staging → premain → main` branch flow.
Do not hand-edit released sections; add a Conventional Commit and let
the release pipeline populate the next entry.

## [2.0.0-rc.2](https://github.com/theory-cloud/theory-cloud-design/compare/v2.0.0-rc.1...v2.0.0-rc.2) (2026-04-17)


### ⚠ BREAKING CHANGES

* **assets:** the primary Theory Cloud mark geometry, the monochrome variants, the favicon set, and the OG card all change visibly. Every consumer app (FaceTheory, autheory, theory-mcp-server) will render a different brand surface when it re-pins the next `@theory-cloud/design` release.
* **deps:** the peer-dependency range no longer accepts FaceTheory 0.5.x. Consumer apps (FaceTheory itself, autheory, theory-mcp-server) must install `theory-cloud-facetheory-0.6.0.tgz` (or any newer `^0.6.0`) alongside the next `@theory-cloud/design` release tarball.

### Features

* **assets:** adopt new Theory Cloud mark and wordmark lockup ([585c72e](https://github.com/theory-cloud/theory-cloud-design/commit/585c72e2c0020a55b80cbb758a62575356d6e3d5))
* **assets:** complete icon asset set ([2016024](https://github.com/theory-cloud/theory-cloud-design/commit/2016024a967069cd43f65d5d5bf52a74638f67ee))
* **deps:** bump @theory-cloud/facetheory peer to ^0.6.0 ([7e730d2](https://github.com/theory-cloud/theory-cloud-design/commit/7e730d21805c75f7e12908a2cd83216ef08492c2))
* **package:** scaffold @theory-cloud/design package ([ebd2b0e](https://github.com/theory-cloud/theory-cloud-design/commit/ebd2b0e78d6b43667638e7e0680a5c04c7941d94))
* **pkg:** expose raw brand assets via wildcard exports subpath ([d08ff49](https://github.com/theory-cloud/theory-cloud-design/commit/d08ff496fdafd349d3c260c35dbc1f94d74035a4))
* **pkg:** expose raw brand assets via wildcard exports subpath ([2c349b7](https://github.com/theory-cloud/theory-cloud-design/commit/2c349b710177165505a72a28e63884552d8e5968))
* theory-cloud-design v0.1.0 brand-pack foundation ([3a92528](https://github.com/theory-cloud/theory-cloud-design/commit/3a925289e5f7ff24335923743f0de453bf580c8c))
* **tokens:** add Core, MCP, and Auth surface variants ([efd4713](https://github.com/theory-cloud/theory-cloud-design/commit/efd471389d324dcae3bcdfa6ab6529fe78765308))
* **tokens:** add Theory Cloud base token palette ([89e2584](https://github.com/theory-cloud/theory-cloud-design/commit/89e2584ed46054e8b125a6442920149120e1cede))


### Bug Fixes

* **assets:** make OG card self-contained and render-deterministic ([f0cf83b](https://github.com/theory-cloud/theory-cloud-design/commit/f0cf83b901b409ce0c579c4a2ac60574d0c7f3b2))
* **ci:** drop developer-editable files from release-pr paths-ignore ([3bbda67](https://github.com/theory-cloud/theory-cloud-design/commit/3bbda67864391c37377ed2637179623cf25a9221))
* **ci:** drop developer-editable files from release-pr paths-ignore ([dcaa2b7](https://github.com/theory-cloud/theory-cloud-design/commit/dcaa2b7f38e48d2f97234dca7a47eb4b4b39ed5b))

## [2.0.0-rc.1](https://github.com/theory-cloud/theory-cloud-design/compare/v2.0.0-rc...v2.0.0-rc.1) (2026-04-17)


### Features

* **pkg:** expose raw brand assets via wildcard exports subpath ([d08ff49](https://github.com/theory-cloud/theory-cloud-design/commit/d08ff496fdafd349d3c260c35dbc1f94d74035a4))
* **pkg:** expose raw brand assets via wildcard exports subpath ([2c349b7](https://github.com/theory-cloud/theory-cloud-design/commit/2c349b710177165505a72a28e63884552d8e5968))


### Bug Fixes

* **ci:** drop developer-editable files from release-pr paths-ignore ([3bbda67](https://github.com/theory-cloud/theory-cloud-design/commit/3bbda67864391c37377ed2637179623cf25a9221))
* **ci:** drop developer-editable files from release-pr paths-ignore ([dcaa2b7](https://github.com/theory-cloud/theory-cloud-design/commit/dcaa2b7f38e48d2f97234dca7a47eb4b4b39ed5b))

## [2.0.0-rc](https://github.com/theory-cloud/theory-cloud-design/compare/v1.0.0...v2.0.0-rc) (2026-04-17)


### ⚠ BREAKING CHANGES

* **assets:** the primary Theory Cloud mark geometry, the monochrome variants, the favicon set, and the OG card all change visibly. Every consumer app (FaceTheory, autheory, theory-mcp-server) will render a different brand surface when it re-pins the next `@theory-cloud/design` release.
* **deps:** the peer-dependency range no longer accepts FaceTheory 0.5.x. Consumer apps (FaceTheory itself, autheory, theory-mcp-server) must install `theory-cloud-facetheory-0.6.0.tgz` (or any newer `^0.6.0`) alongside the next `@theory-cloud/design` release tarball.

### Features

* **assets:** adopt new Theory Cloud mark and wordmark lockup ([585c72e](https://github.com/theory-cloud/theory-cloud-design/commit/585c72e2c0020a55b80cbb758a62575356d6e3d5))
* **deps:** bump @theory-cloud/facetheory peer to ^0.6.0 ([7e730d2](https://github.com/theory-cloud/theory-cloud-design/commit/7e730d21805c75f7e12908a2cd83216ef08492c2))

## 1.0.0 (2026-04-17)


### Features

* **assets:** complete icon asset set ([2016024](https://github.com/theory-cloud/theory-cloud-design/commit/2016024a967069cd43f65d5d5bf52a74638f67ee))
* **package:** scaffold @theory-cloud/design package ([ebd2b0e](https://github.com/theory-cloud/theory-cloud-design/commit/ebd2b0e78d6b43667638e7e0680a5c04c7941d94))
* theory-cloud-design v0.1.0 brand-pack foundation ([3a92528](https://github.com/theory-cloud/theory-cloud-design/commit/3a925289e5f7ff24335923743f0de453bf580c8c))
* **tokens:** add Core, MCP, and Auth surface variants ([efd4713](https://github.com/theory-cloud/theory-cloud-design/commit/efd471389d324dcae3bcdfa6ab6529fe78765308))
* **tokens:** add Theory Cloud base token palette ([89e2584](https://github.com/theory-cloud/theory-cloud-design/commit/89e2584ed46054e8b125a6442920149120e1cede))


### Bug Fixes

* **assets:** make OG card self-contained and render-deterministic ([f0cf83b](https://github.com/theory-cloud/theory-cloud-design/commit/f0cf83b901b409ce0c579c4a2ac60574d0c7f3b2))

## [Unreleased]

The next release will be cut by release-please when this milestone PR
merges to `main` and the subsequently opened release PR is merged.
Expected contents for the first release (`v0.1.0`):

- **Base token palette** (`@theory-cloud/design/tokens`) — dark-first
  StitchTokenSet populated with Midnight, Core Blue, Violet Signal,
  Ice White, Steel, Mist, Graphite, Phi Gold, aligned with §27.C.
- **Surface variants** — `theoryCloudCoreTokens`,
  `theoryCloudMcpTokens`, `theoryCloudAuthTokens`, composing over the
  base per §29.F Surface Accent Strategy.
- **Icon asset set** — primary SVG, Ice White and Graphite monochrome
  variants, favicon PNGs at 16 / 32 / 48 / 192 / 512 px, multi-
  resolution favicon.ico, and a 1200 × 630 OG card generated from an
  SVG master.
- **Package scaffold** — `@theory-cloud/design` with subpath exports
  for `.`, `./tokens`, `./tokens/core`, `./tokens/mcp`, `./tokens/auth`,
  `./assets`; peer-dependency on `@theory-cloud/facetheory@^0.5.0`.
- **Release pipeline** — release-please on the three-branch flow,
  producing an immutable `theory-cloud-design-${VERSION}.tgz` asset on
  each published release.

Once cut, `v0.1.0` will be pinnable at:

```
https://github.com/theory-cloud/theory-cloud-design/releases/download/v0.1.0/theory-cloud-design-0.1.0.tgz
```
