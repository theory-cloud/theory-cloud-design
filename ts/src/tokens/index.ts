/**
 * Theory Cloud — token set entry point.
 *
 * Re-exports the base token set and the brand hex locks. Per-surface
 * variants (Core / MCP / Auth) arrive in task 1.2; when they land they
 * are re-exported from this file under stable names so consumers can
 * import them as `@theory-cloud/design/tokens`.
 */

export {
  theoryCloudBaseTokens,
  brandMidnight,
  brandCoreBlue,
  brandVioletSignal,
  brandIceWhite,
  brandSteel,
  brandMist,
  brandGraphite,
  brandPhiGold,
} from "./base.js";
