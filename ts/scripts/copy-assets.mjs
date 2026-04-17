#!/usr/bin/env node
/**
 * Stage the repo-root `assets/` tree into `ts/dist/assets/` so the
 * published package tarball carries the brand assets next to the
 * compiled `dist/assets.js` module.
 *
 * Runs as part of `npm run build` after `tsc` emits the compiled JS.
 */

import { cpSync, existsSync, mkdirSync, rmSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const tsDir = join(here, "..");
const repoRoot = join(tsDir, "..");

const src = join(repoRoot, "assets");
const dest = join(tsDir, "dist", "assets");

if (!existsSync(src)) {
  console.error(`copy-assets: source missing: ${src}`);
  process.exit(1);
}

mkdirSync(dirname(dest), { recursive: true });
rmSync(dest, { recursive: true, force: true });
cpSync(src, dest, { recursive: true });

console.log(`copy-assets: ${src} -> ${dest}`);
