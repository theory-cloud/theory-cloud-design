/**
 * Theory Cloud — base token set.
 *
 * Dark-first StitchTokenSet shared by all three Theory Cloud surfaces
 * (Core / MCP / Auth). Per-surface variants in `./core`, `./mcp`, and
 * `./auth` compose over this set with narrow, calibrated accent shifts
 * — they never duplicate values that belong in the base.
 *
 * Brand-document references:
 *   §6   Color System             — Midnight, Core Blue, Violet Signal,
 *                                   Ice White, Steel, Mist, Graphite, Phi Gold.
 *   §7   Typography               — neutral modern sans + mono companion.
 *   §8   Shape Language           — modular blocks, spiral-informed radii,
 *                                   "slightly rounded, never cartoonish."
 *   §27.C Color Standards         — the formal hex locks for the palette.
 *   §27.D Typography Standards    — Inter / Geist system pairing; mono ref.
 *   §27.G Shape and Layout        — modular rectangular segmentation;
 *                                   phi-adjacent proportional thinking.
 *   §29.E Shared vs Distinct      — the base palette is shared identity;
 *                                   surface variants add only a light layer.
 *
 * Dark-first (§11, §29.B) is enforced here by `mode: "dark"`; v1 does not
 * ship a light-mode variant.
 *
 * This module's published type is local to the brand pack so installation
 * does not force a FaceTheory pin. Compatibility with the `StitchTokenSet`
 * shape from `@theory-cloud/facetheory` is enforced by the contract
 * typecheck in `contracts/facetheory-stitch-token-set.ts`.
 */

import type { TheoryCloudTokenSet } from "./types.js";

/* ---------------------------------------------------------------------------
 * Brand hex locks (§27.C).
 *
 * These are the *only* places these literals should appear in the package.
 * Everywhere else in the token sets references the `brand*` constants below.
 * Drift in a button, a background, or an outline is easier to catch when
 * the inputs are named.
 * ------------------------------------------------------------------------ */

/** Midnight — deep base for product and brand surfaces. */
export const brandMidnight = "#081226";

/** Core Blue — system intelligence / clarity. Primary accent. */
export const brandCoreBlue = "#2EA7FF";

/** Violet Signal — generative core / memory / energy. Secondary accent. */
export const brandVioletSignal = "#7A5CFF";

/** Ice White — typography and high-contrast interface text. */
export const brandIceWhite = "#F4F8FF";

/** Steel — neutral UI linework. */
export const brandSteel = "#6F7D95";

/** Mist — soft background tint; quiet on-surface variant text. */
export const brandMist = "#DCE6F5";

/** Graphite — light-mode dark text; dark-mode subtle inverse text. */
export const brandGraphite = "#1C2433";

/** Phi Gold — reserve accent for diagrams, premium moments, phi references. */
export const brandPhiGold = "#C9A96B";

/* ---------------------------------------------------------------------------
 * Derived Midnight elevation ramp (dark-first).
 *
 * The brand doc does not enumerate a full elevation ramp; these values
 * are calibrated from Midnight toward Ice White along a perceptual luma
 * line so that the M3 surface container layers feel like one material
 * rather than arbitrary greys. "Structured, living systems" (§16) reads
 * as a quiet, confident depth — not spectacle.
 * ------------------------------------------------------------------------ */

/** One tick below Midnight. Used for surfaceDim / surfaceContainerLowest. */
const midnightDepth = "#050A1A";

/** Midnight with a faint lift — one step up from base surface. */
const midnightLift1 = "#0B172D";

/** Midnight containers — typical card/panel ground. */
const midnightLift2 = "#111E38";

/** Midnight raised — hovered/active containers. */
const midnightLift3 = "#17264A";

/** Midnight highest — focused or elevated panels. */
const midnightLift4 = "#1D2E5C";

/** Dimmer Steel for outlineVariant (less insistent separators). */
const steelDim = "#3B465C";

/**
 * Dark red calibrated to sit on Midnight without shouting. Functional
 * system color only — §6 does not define an error hue, so this is the
 * minimum viable addition consistent with "precise, calm, technical."
 * Reconsider if the brand doc later specifies a canonical error color.
 */
const systemError = "#FF5A65";

/** Deep container tint for error surfaces on Midnight. */
const systemErrorContainer = "#4A1720";

/* ---------------------------------------------------------------------------
 * Primary-container tints (Core Blue on Midnight, Violet Signal on Midnight,
 * Phi Gold on Midnight). Hand-picked to preserve identity at low luminance.
 * ------------------------------------------------------------------------ */

/** Core Blue × Midnight — deep blue container for primary surfaces. */
const coreBlueContainerDark = "#143B5C";

/** Core Blue lifted — for *Fixed* slots (surface-agnostic emphasis). */
const coreBlueFixed = "#7FC7FF";

/** Core Blue fixed-dim — less emphatic fixed surface. */
const coreBlueFixedDim = "#5CB5FF";

/** Core Blue inverted — for light surfaces quoting back a primary color. */
const coreBlueInverse = "#1274BF";

/** Violet Signal × Midnight — deep violet container. */
const violetSignalContainerDark = "#2C1F6B";

/** Violet Signal lifted. */
const violetSignalFixed = "#B6A4FF";

/** Violet Signal fixed-dim. */
const violetSignalFixedDim = "#9B85FF";

/** Phi Gold × Midnight — deep gold container. */
const phiGoldContainerDark = "#3B2F16";

/** Phi Gold lifted. */
const phiGoldFixed = "#E6D09A";

/** Phi Gold fixed-dim. */
const phiGoldFixedDim = "#D8BF85";

/* ---------------------------------------------------------------------------
 * Typography stacks (§7, §27.D).
 *
 * System fonts only — the wordmark direction ("Adjusted Neutral Sans", §23)
 * is expressed through the logo assets, not through body/label typography.
 * Inter and Geist are the recommended references; Geist leads `displayFont`
 * because its display-weight refinements read as "clean and spacious"
 * (§27.D typography roles) without going decorative.
 * ------------------------------------------------------------------------ */

const sansStack =
  "Inter, Geist, -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif";

const displayStack =
  "Geist, Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif";

/* ---------------------------------------------------------------------------
 * Shape / spacing scale (§8, §27.G).
 *
 * Rounded, not cartoonish. The `xl` value matches the 14 px outer radius
 * of the icon on its 64 px viewBox — keeping the largest brand shape
 * coherent with the icon's own geometry.
 * ------------------------------------------------------------------------ */

const baseSpacingUnit = 4;

/* ---------------------------------------------------------------------------
 * The base token set.
 * ------------------------------------------------------------------------ */

export const theoryCloudBaseTokens: TheoryCloudTokenSet = {
  mode: "dark",
  palette: {
    // Primary — Core Blue (§29.F: shared identity; surfaces re-weight only).
    primary: brandCoreBlue,
    primaryContainer: coreBlueContainerDark,
    primaryFixed: coreBlueFixed,
    primaryFixedDim: coreBlueFixedDim,
    onPrimary: brandMidnight,
    onPrimaryContainer: brandIceWhite,
    onPrimaryFixed: brandMidnight,
    onPrimaryFixedVariant: brandGraphite,
    inversePrimary: coreBlueInverse,
    surfaceTint: brandCoreBlue,

    // Secondary — Violet Signal (memory / agent / generative energy).
    secondary: brandVioletSignal,
    secondaryContainer: violetSignalContainerDark,
    secondaryFixed: violetSignalFixed,
    secondaryFixedDim: violetSignalFixedDim,
    onSecondary: brandIceWhite,
    onSecondaryContainer: brandIceWhite,
    onSecondaryFixed: brandMidnight,
    onSecondaryFixedVariant: brandGraphite,

    // Tertiary — Phi Gold (accent reserve, §27.C; sparingly by rule).
    tertiary: brandPhiGold,
    tertiaryContainer: phiGoldContainerDark,
    tertiaryFixed: phiGoldFixed,
    tertiaryFixedDim: phiGoldFixedDim,
    onTertiary: brandMidnight,
    onTertiaryContainer: brandIceWhite,
    onTertiaryFixed: brandMidnight,
    onTertiaryFixedVariant: brandGraphite,

    // Surface / background — Midnight elevation ramp.
    background: brandMidnight,
    surface: brandMidnight,
    surfaceBright: midnightLift4,
    surfaceDim: midnightDepth,
    surfaceContainerLowest: midnightDepth,
    surfaceContainerLow: midnightLift1,
    surfaceContainer: midnightLift2,
    surfaceContainerHigh: midnightLift3,
    surfaceContainerHighest: midnightLift4,
    surfaceVariant: midnightLift3,

    // Inverse surfaces — Ice White ground for dark-on-light contexts
    // (toasts, snackbars, selective doc surfaces).
    inverseSurface: brandIceWhite,
    inverseOnSurface: brandGraphite,

    // On-background / on-surface typography colors.
    onBackground: brandIceWhite,
    onSurface: brandIceWhite,
    onSurfaceVariant: brandMist,

    // Outlines — Steel and a dimmer derivative for "restrained linework."
    outline: brandSteel,
    outlineVariant: steelDim,

    // System error — calibrated red, not defined in the brand doc.
    error: systemError,
    errorContainer: systemErrorContainer,
    onError: brandIceWhite,
    onErrorContainer: brandIceWhite,
  },
  typography: {
    displayFont: displayStack,
    bodyFont: sansStack,
    labelFont: sansStack,
  },
  roundness: {
    // Small — inputs, chips, inline controls.
    sm: 2,
    // Medium — buttons, cards at dense density.
    md: 4,
    // Large — panels, standard cards.
    lg: 8,
    // Extra-large — hero cards; matches the icon's 14 px outer radius.
    xl: 14,
  },
  spacing: {
    baseUnit: baseSpacingUnit,
  },
};
