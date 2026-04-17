# Changelog

All notable changes to `theory-cloud-design` are recorded here.
This file is maintained by
[release-please](https://github.com/googleapis/release-please) from
Conventional Commits on the `staging → premain → main` branch flow.
Do not hand-edit released sections; add a Conventional Commit and let
the release pipeline populate the next entry.

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
