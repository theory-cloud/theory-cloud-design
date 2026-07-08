/**
 * FaceTheory compatibility contract.
 *
 * theory-cloud-design is the brand-pack source of truth. It should not force
 * a published FaceTheory peer dependency just to expose token values, but the
 * token objects must still remain assignable to FaceTheory's `StitchTokenSet`
 * surface contract. This file is included only in the validation tsconfig.
 */

import type { StitchTokenSet } from "@theory-cloud/facetheory/stitch-tokens";

import {
  theoryCloudAuthTokens,
  theoryCloudBaseTokens,
  theoryCloudCoreTokens,
  theoryCloudMcpTokens,
} from "../src/tokens/index.js";

const facetheoryCompatibleTokenSets = [
  theoryCloudBaseTokens,
  theoryCloudCoreTokens,
  theoryCloudMcpTokens,
  theoryCloudAuthTokens,
] satisfies readonly StitchTokenSet[];

void facetheoryCompatibleTokenSets;
