/**
 * Theory Cloud — Auth surface variant.
 *
 * Surface: `autheory.app` — authentication, session continuity,
 * cross-platform identity.
 *
 * §29.F Surface Accent Strategy for Auth:
 *   "Primary emphasis: more restrained palette usage, higher
 *    white/neutral balance in some flows if needed, calmer,
 *    trust-forward compositions. Desired feeling: secure, quiet,
 *    dependable, foundational."
 *
 * The Auth shift is deliberately the quietest of the three. Primary
 * stays Core Blue (master identity) but surface elevation drops its
 * accent tint entirely — `surfaceTint` becomes Steel, so M3 elevation
 * overlays read as neutral lift rather than colored wash. That's what
 * "calmer, trust-forward" means in token terms: less accent saturation
 * in the elevation system, not a new palette.
 *
 * Note on §29.F "higher white/neutral balance in some flows if needed":
 * v1 is dark-first across all surfaces (§29.B). That guidance applies
 * to composition choices inside Auth screens (more whitespace, quieter
 * accents) rather than to a light-mode palette; the brand pack does
 * not ship a light-mode variant.
 */

import {
  brandSteel,
  theoryCloudBaseTokens,
} from "./base.js";
import type { TheoryCloudTokenSet } from "./types.js";

export const theoryCloudAuthTokens: TheoryCloudTokenSet = {
  ...theoryCloudBaseTokens,
  palette: {
    ...theoryCloudBaseTokens.palette,
    // Drop the accent cast on surface elevation: Steel makes container
    // overlays read as structural, trust-forward lift rather than
    // colored emphasis. Core Blue remains the primary accent for
    // buttons, focus rings, and active states — the master identity
    // is preserved.
    surfaceTint: brandSteel,
  },
};
