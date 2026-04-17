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
 * The tokens are shape-compatible with `StitchTokenSet` from
 * `@theory-cloud/facetheory/stitch-tokens` — this package is the Theory
 * Cloud instance of that brand-agnostic primitive (FaceTheory does not
 * depend on this package; only consumer apps do).
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
