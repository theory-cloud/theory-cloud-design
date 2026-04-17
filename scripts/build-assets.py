#!/usr/bin/env python3
"""Render Theory Cloud raster assets from the canonical SVG sources.

Usage: python3 scripts/build-assets.py

Inputs (SVG is the authoring format — §stewardship asset discipline):
  assets/icon.svg          — primary icon master
  assets/og-card.svg       — 1200x630 social/OG card master

Outputs:
  assets/favicon/favicon-16.png
  assets/favicon/favicon-32.png
  assets/favicon/favicon-48.png
  assets/favicon/favicon-192.png
  assets/favicon/favicon-512.png
  assets/favicon.ico       — multi-resolution ICO (16, 32, 48)
  assets/og-card.png       — 1200x630 rendered card

Idempotent: reruns regenerate all outputs from scratch.
"""

from __future__ import annotations

from pathlib import Path

import cairosvg
from PIL import Image


REPO_ROOT = Path(__file__).resolve().parent.parent
ASSETS = REPO_ROOT / "assets"
FAVICON_DIR = ASSETS / "favicon"

FAVICON_SIZES = [16, 32, 48, 192, 512]
ICO_SIZES = [16, 32, 48]


def render_png(svg_path: Path, png_path: Path, width: int, height: int) -> None:
    """Render an SVG to a PNG at the given pixel dimensions."""
    png_path.parent.mkdir(parents=True, exist_ok=True)
    cairosvg.svg2png(
        url=str(svg_path),
        write_to=str(png_path),
        output_width=width,
        output_height=height,
    )
    print(f"  rendered {png_path.relative_to(REPO_ROOT)} ({width}x{height})")


def build_favicons() -> None:
    """Render the favicon PNG set and assemble the multi-resolution ICO."""
    icon_svg = ASSETS / "icon.svg"
    print(f"favicons from {icon_svg.relative_to(REPO_ROOT)}:")
    for size in FAVICON_SIZES:
        render_png(
            icon_svg,
            FAVICON_DIR / f"favicon-{size}.png",
            size,
            size,
        )

    ico_path = ASSETS / "favicon.ico"
    print(f"assembling {ico_path.relative_to(REPO_ROOT)}:")
    ico_frames = [
        Image.open(FAVICON_DIR / f"favicon-{size}.png") for size in ICO_SIZES
    ]
    ico_frames[0].save(
        ico_path,
        format="ICO",
        sizes=[(size, size) for size in ICO_SIZES],
        append_images=ico_frames[1:],
    )
    print(f"  packed {len(ICO_SIZES)} resolutions: {ICO_SIZES}")


def build_og_card() -> None:
    """Render the 1200x630 social/OG card PNG."""
    og_svg = ASSETS / "og-card.svg"
    og_png = ASSETS / "og-card.png"
    print(f"og card from {og_svg.relative_to(REPO_ROOT)}:")
    render_png(og_svg, og_png, 1200, 630)


def main() -> None:
    build_favicons()
    build_og_card()
    print("done.")


if __name__ == "__main__":
    main()
