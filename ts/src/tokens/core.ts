/**
 * Theory Cloud — Core surface variant.
 *
 * Surface: `theorycloud.ai` — the platform brand core, application
 * hosting, deployment management.
 *
 * §29.F Surface Accent Strategy for Core:
 *   "Primary emphasis: Midnight, Core Blue, balanced blue-to-violet
 *    gradient. Desired feeling: core platform, stable, authoritative,
 *    orchestration and control."
 *
 * Core is the *balanced* surface — the neutral expression of the
 * Theory Cloud master identity. The variant therefore sits on the base
 * token set with no overrides; it exists as a named surface identity so
 * consumers import it as `theoryCloudCoreTokens` and downstream work
 * has a clear place to evolve Core-only choices if the brand doc ever
 * requires them. Treating Core as a synonym for "base" at runtime is
 * intentional and matches §29.A (branded house, Pattern 2 endorsed
 * header); deviation from that assumption is a spec-level question,
 * not a token addition.
 */

import { theoryCloudBaseTokens } from "./base.js";
import type { TheoryCloudTokenSet } from "./types.js";

export const theoryCloudCoreTokens: TheoryCloudTokenSet = {
  ...theoryCloudBaseTokens,
  palette: {
    ...theoryCloudBaseTokens.palette,
    // Core is the balanced reference. Surface-level tinting stays on
    // Core Blue — consumers composing surface elevation see blue-cast
    // overlays, which aligns with "orchestration and control."
  },
};
