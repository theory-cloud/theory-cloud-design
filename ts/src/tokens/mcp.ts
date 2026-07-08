/**
 * Theory Cloud — MCP surface variant.
 *
 * Surface: `theorymcp.ai` — MCP endpoints, agentic interface, memory
 * and knowledge access.
 *
 * §29.F Surface Accent Strategy for MCP:
 *   "Primary emphasis: slightly stronger Violet Signal usage, more
 *    dynamic signal-path graphics, modular interaction motifs. Desired
 *    feeling: active, connected, agentic, interface-rich."
 *
 * The identity rule in §29.E holds: master icon, wordmark, palette,
 * and motion language stay shared across surfaces. The MCP shift is a
 * *light layer* — Violet Signal becomes the surface-tint seed (so M3
 * elevation overlays carry a faint violet cast), and `inversePrimary`
 * quotes back in violet rather than blue. Primary itself remains Core
 * Blue: the master brand does not change per surface.
 *
 * The brand doc forbids wholesale re-identity per surface (§29.E
 * "distinct surface cues"). These overrides are the minimum that still
 * reads as "active, connected, agentic" within the shared system.
 */

import {
  brandVioletSignal,
  theoryCloudBaseTokens,
} from "./base.js";
import type { TheoryCloudTokenSet } from "./types.js";

/**
 * Violet Signal inverted — for light-on-dark quotes of the secondary
 * accent on inverse surfaces. Calibrated analogous to the base's
 * `inversePrimary` (a mid-luma derivative of Core Blue).
 */
const violetSignalInverse = "#5A3FDB";

export const theoryCloudMcpTokens: TheoryCloudTokenSet = {
  ...theoryCloudBaseTokens,
  palette: {
    ...theoryCloudBaseTokens.palette,
    // Surface-tint seed moves from Core Blue to Violet Signal: surface
    // containers gain a faint violet cast under M3 elevation, giving
    // MCP its "active / agentic" feel without re-identifying the
    // primary accent.
    surfaceTint: brandVioletSignal,
    // Inverse primary quotes Violet Signal rather than Core Blue when
    // MCP content is shown on light-mode inverse surfaces (toasts,
    // snackbars).
    inversePrimary: violetSignalInverse,
  },
};
