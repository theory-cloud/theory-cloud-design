/**
 * Theory Cloud — asset paths.
 *
 * Exports absolute filesystem paths to every canonical brand asset
 * shipped in the package tarball. Consumers import these paths from
 * `@theory-cloud/design/assets` rather than by string convention.
 *
 * Resolution works because `scripts/copy-assets.mjs` stages the `assets/`
 * tree from the repo root into `ts/dist/assets/` at build time, so the
 * compiled `dist/assets.js` module sits next to `dist/assets/` in the
 * published tarball.
 *
 * For browser / bundler consumption (Vite, Webpack, etc.), consumers
 * should prefer their bundler's URL-import mechanism. These Node-side
 * filesystem paths are the minimum-viable export for v0.1.0.
 */

import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));

/** Directory inside the installed package that holds every brand asset. */
const assetsRoot = join(here, "assets");

/** Primary full-color icon (Core Blue → Violet Signal gradient ground). */
export const iconPath = join(assetsRoot, "icon.svg");

/** Monochrome icon, Ice White on transparent (for dark surfaces). */
export const iconMonoLightPath = join(assetsRoot, "icon-mono-light.svg");

/** Monochrome icon, Graphite on transparent (for light surfaces). */
export const iconMonoDarkPath = join(assetsRoot, "icon-mono-dark.svg");

/**
 * Primary horizontal wordmark lockup — icon + "Theory Cloud" set in
 * Graphite, with the icon rendered in the Core Blue → Violet Signal
 * gradient. Use for masthead, documentation covers, and any surface
 * where the full brand expression is appropriate. On constrained
 * surfaces (favicons, small UI chrome), prefer `iconPath`.
 */
export const wordmarkPath = join(assetsRoot, "wordmark-theory-cloud.svg");

/** Multi-resolution ICO bundle (16 / 32 / 48 px). */
export const faviconIcoPath = join(assetsRoot, "favicon.ico");

/** Directory containing the favicon PNG set. */
export const faviconDir = join(assetsRoot, "favicon");

/** Favicon PNGs by pixel size. */
export const faviconPngPaths = {
  16: join(faviconDir, "favicon-16.png"),
  32: join(faviconDir, "favicon-32.png"),
  48: join(faviconDir, "favicon-48.png"),
  192: join(faviconDir, "favicon-192.png"),
  512: join(faviconDir, "favicon-512.png"),
} as const;

/** Social / OG card master SVG. */
export const ogCardSvgPath = join(assetsRoot, "og-card.svg");

/** Social / OG card rendered PNG (1200 × 630). */
export const ogCardPngPath = join(assetsRoot, "og-card.png");

/**
 * Aggregated view of every asset path, for consumers that prefer a
 * single object import over named paths.
 */
export const theoryCloudAssets = {
  icon: iconPath,
  iconMonoLight: iconMonoLightPath,
  iconMonoDark: iconMonoDarkPath,
  wordmark: wordmarkPath,
  faviconIco: faviconIcoPath,
  faviconPngs: faviconPngPaths,
  ogCardSvg: ogCardSvgPath,
  ogCardPng: ogCardPngPath,
} as const;

export type TheoryCloudAssets = typeof theoryCloudAssets;
