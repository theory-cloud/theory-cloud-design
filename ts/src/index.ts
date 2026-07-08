/**
 * Theory Cloud — brand pack entry point.
 *
 * Consumers can:
 *
 *   import {
 *     theoryCloudBaseTokens,
 *     theoryCloudCoreTokens,
 *     theoryCloudMcpTokens,
 *     theoryCloudAuthTokens,
 *   } from "@theory-cloud/design";
 *
 * or pull individual surfaces through their subpath exports:
 *
 *   import { theoryCloudMcpTokens } from "@theory-cloud/design/tokens/mcp";
 *
 * Icon and asset paths live under the `./assets` subpath:
 *
 *   import { iconPath } from "@theory-cloud/design/assets";
 *
 * The tokens publish a local structural contract and are validated against
 * `StitchTokenSet` from `@theory-cloud/facetheory/stitch-tokens` during
 * package checks. This package is the Theory Cloud instance of that
 * brand-agnostic primitive without forcing a FaceTheory install for every
 * design-pack consumer.
 */

export {
  theoryCloudBaseTokens,
  theoryCloudCoreTokens,
  theoryCloudMcpTokens,
  theoryCloudAuthTokens,
  brandMidnight,
  brandCoreBlue,
  brandVioletSignal,
  brandIceWhite,
  brandSteel,
  brandMist,
  brandGraphite,
  brandPhiGold,
  type TheoryCloudColorValue,
  type TheoryCloudPaletteTokens,
  type TheoryCloudTypographyTokens,
  type TheoryCloudRoundnessTokens,
  type TheoryCloudSpacingTokens,
  type TheoryCloudTokenSet,
} from "./tokens/index.js";

export {
  iconPath,
  iconMonoLightPath,
  iconMonoDarkPath,
  faviconIcoPath,
  faviconDir,
  faviconPngPaths,
  ogCardSvgPath,
  ogCardPngPath,
  theoryCloudAssets,
  type TheoryCloudAssets,
} from "./assets.js";
