/**
 * Theory Cloud — token set entry point.
 *
 * Re-exports the base token set, the three per-surface variants
 * (Core / MCP / Auth), and the named brand hex locks.
 *
 * Consumers should import the variant whose surface they render:
 *
 *   import { theoryCloudCoreTokens } from "@theory-cloud/design/tokens/core";
 *   import { theoryCloudMcpTokens  } from "@theory-cloud/design/tokens/mcp";
 *   import { theoryCloudAuthTokens } from "@theory-cloud/design/tokens/auth";
 *
 * The subpath imports are the canonical path; consumers must not read
 * raw hex values around the typed exports (§29.E "shared vs distinct
 * identity rules" — drift in consumers usually starts with a hardcoded
 * off-brand color).
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

export { theoryCloudCoreTokens } from "./core.js";
export { theoryCloudMcpTokens } from "./mcp.js";
export { theoryCloudAuthTokens } from "./auth.js";
