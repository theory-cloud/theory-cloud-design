# Changelog

All notable changes to `theory-cloud-design` are recorded here.
This file is maintained by
[release-please](https://github.com/googleapis/release-please) from
Conventional Commits on the `staging → premain → main` branch flow.
Do not hand-edit released sections; add a Conventional Commit and let
the release pipeline populate the next entry.

## [3.0.0](https://github.com/theory-cloud/theory-cloud-design/compare/v2.1.1...v3.0.0) (2026-05-11)


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
* **release:** make all commit types release-bearing ([6fcb5bc](https://github.com/theory-cloud/theory-cloud-design/commit/6fcb5bc5a8672c1b65cb888ff5a1f771cb635aef))
* **release:** repair release PR workflow guards ([d10a101](https://github.com/theory-cloud/theory-cloud-design/commit/d10a1013ec9ec7430ac550ea6800eb478373fd02))
* **release:** stop release PR self-triggers ([3f8981a](https://github.com/theory-cloud/theory-cloud-design/commit/3f8981a1dbef33b91d1922d41342ae8929a7e204))


### Documentation

* **changelog:** clean 2.1.1 release notes ([61050b3](https://github.com/theory-cloud/theory-cloud-design/commit/61050b3e7dc0bb518618aa5a0672896356bca7d4))
* **changelog:** seed CHANGELOG.md for release-please ([e730c44](https://github.com/theory-cloud/theory-cloud-design/commit/e730c443a728d2688ed30c39e1729427f658965f))
* **readme:** fix install command to pin FaceTheory peer tarball ([a0d5a63](https://github.com/theory-cloud/theory-cloud-design/commit/a0d5a639403df9121d6d8f0cdbf2c27ed5ee1b6f))


### Maintenance

* add repo-level gitignore ([ba812ea](https://github.com/theory-cloud/theory-cloud-design/commit/ba812ea5a8d4893b98a1ee876665586f8dbe15b5))
* **main:** release 1.0.0 ([5a66b2c](https://github.com/theory-cloud/theory-cloud-design/commit/5a66b2cda9aea01eb8cc4b9add6775f28b04e729))
* **main:** release 1.0.0 ([a6d2ecf](https://github.com/theory-cloud/theory-cloud-design/commit/a6d2ecfda1043573c7c8a389962147978185d793))
* **main:** release 2.0.0 ([6201ac0](https://github.com/theory-cloud/theory-cloud-design/commit/6201ac0162715289fab1a828c7a4d3b41a5c0415))
* **main:** release 2.0.0 ([7d22644](https://github.com/theory-cloud/theory-cloud-design/commit/7d2264473b6ce14f4ac5307382defc9118b8d0ba))
* **main:** release 2.1.0 ([cbcbc54](https://github.com/theory-cloud/theory-cloud-design/commit/cbcbc544a996e7e589f994d5368747990e8014e8))
* **main:** release 2.1.0 ([21e2611](https://github.com/theory-cloud/theory-cloud-design/commit/21e2611a223923b97697ac6ce942d693f42cfc31))
* **main:** release 2.1.1 ([d95520a](https://github.com/theory-cloud/theory-cloud-design/commit/d95520ac23d2d0978c221dce24131f47bde215c7))
* **main:** release 2.1.1 ([f133b55](https://github.com/theory-cloud/theory-cloud-design/commit/f133b5572a145bc2297d597325aa548f2e955c88))
* **package:** pin FaceTheory v3.0.0 ([0c2272c](https://github.com/theory-cloud/theory-cloud-design/commit/0c2272c1f62cda8638f29bb67f97ded7aac08a24))
* **package:** pin FaceTheory v3.1.0 ([52c878c](https://github.com/theory-cloud/theory-cloud-design/commit/52c878ccd386c5e3822d58cb928276a021417668))
* **premain:** release 2.0.0-rc ([b749049](https://github.com/theory-cloud/theory-cloud-design/commit/b7490496c05093b5795ba9fc249108393c9a3482))
* **premain:** release 2.0.0-rc ([fb3987b](https://github.com/theory-cloud/theory-cloud-design/commit/fb3987bf97346f89e738158561ad00b3e77536e9))
* **premain:** release 2.0.0-rc.1 ([c22d341](https://github.com/theory-cloud/theory-cloud-design/commit/c22d3410ca460c9960db77806c61941b555b355d))
* **premain:** release 2.0.0-rc.1 ([14a28f8](https://github.com/theory-cloud/theory-cloud-design/commit/14a28f8251414229c67d97a3fabfefb9201579a9))
* **premain:** release 2.1.1-rc ([961ec70](https://github.com/theory-cloud/theory-cloud-design/commit/961ec7033ac6991fce2b6c0829db83ca99cd43c3))
* **premain:** release 2.1.1-rc ([6bf25ce](https://github.com/theory-cloud/theory-cloud-design/commit/6bf25ce89a4ff62d418f94b4940fc85162b50062))
* **release:** fix premain pipeline to cut proper RCs ([356d420](https://github.com/theory-cloud/theory-cloud-design/commit/356d420ccaeb5302c52d47330a2224feed4a5147))
* **release:** sync main into staging ([346fcd6](https://github.com/theory-cloud/theory-cloud-design/commit/346fcd6da69e247e50de2640f755483a1380d127))
* **release:** sync premain manifest to 1.0.0 and scope prerelease strategy ([3efbf07](https://github.com/theory-cloud/theory-cloud-design/commit/3efbf070563795952fc6417e3e476f6fe67c38c9))


### Continuous Integration

* **assets:** fail when committed rasters drift from SVG masters ([7edfa9f](https://github.com/theory-cloud/theory-cloud-design/commit/7edfa9f1fa5cca4b1c7661bb3f7f85e5bc4d253d))
* **release:** add release-please pipeline ([5138622](https://github.com/theory-cloud/theory-cloud-design/commit/51386229616a6e36532491b5e0e7be5367e0bec4))

## [2.1.1](https://github.com/theory-cloud/theory-cloud-design/compare/v2.1.0...v2.1.1) (2026-05-11)


### Bug Fixes

* **release:** make all commit types release-bearing ([6fcb5bc](https://github.com/theory-cloud/theory-cloud-design/commit/6fcb5bc5a8672c1b65cb888ff5a1f771cb635aef))
* **release:** stop release PR self-triggers ([3f8981a](https://github.com/theory-cloud/theory-cloud-design/commit/3f8981a9da8e09ee3f6ac1d197a0837773e6e67a))


### Maintenance

* **package:** pin FaceTheory v3.0.0 ([0c2272c](https://github.com/theory-cloud/theory-cloud-design/commit/0c2272c1f62cda8638f29bb67f97ded7aac08a24))
* **package:** pin FaceTheory v3.1.0 ([52c878c](https://github.com/theory-cloud/theory-cloud-design/commit/52c878ccd386c5e3822d58cb928276a021417668))
* **release:** sync main into staging ([346fcd6](https://github.com/theory-cloud/theory-cloud-design/commit/346fcd6da69e247e50de2640f755483a1380d127))

## [2.1.1-rc](https://github.com/theory-cloud/theory-cloud-design/compare/v2.1.0...v2.1.1-rc) (2026-05-11)


### Bug Fixes

* **release:** make all commit types release-bearing ([6fcb5bc](https://github.com/theory-cloud/theory-cloud-design/commit/6fcb5bc5a8672c1b65cb888ff5a1f771cb635aef))


### Maintenance

* **package:** pin FaceTheory v3.0.0 ([0c2272c](https://github.com/theory-cloud/theory-cloud-design/commit/0c2272c1f62cda8638f29bb67f97ded7aac08a24))
* **package:** pin FaceTheory v3.1.0 ([52c878c](https://github.com/theory-cloud/theory-cloud-design/commit/52c878ccd386c5e3822d58cb928276a021417668))
* **release:** sync main into staging ([346fcd6](https://github.com/theory-cloud/theory-cloud-design/commit/346fcd6da69e247e50de2640f755483a1380d127))

## [2.1.0](https://github.com/theory-cloud/theory-cloud-design/compare/v2.0.0...v2.1.0) (2026-04-17)


### Features

* **pkg:** expose raw brand assets via wildcard exports subpath ([d08ff49](https://github.com/theory-cloud/theory-cloud-design/commit/d08ff496fdafd349d3c260c35dbc1f94d74035a4))
* **pkg:** expose raw brand assets via wildcard exports subpath ([2c349b7](https://github.com/theory-cloud/theory-cloud-design/commit/2c349b710177165505a72a28e63884552d8e5968))


### Bug Fixes

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
