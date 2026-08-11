#!/usr/bin/env python3
"""Build a deterministic walkthrough GIF from real live-demo screenshots.

The source PNG files were captured from the real deployed AiFriends application.
This script does not invent UI content; it only normalizes those screenshots into
an animated gallery for bilingual documentation.
"""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "docs" / "assets" / "live-demo"
SOURCES = [
    ASSET_DIR / "homepage.png",
    ASSET_DIR / "login.png",
    ASSET_DIR / "register.png",
    ASSET_DIR / "public-profile.png",
]
OUTPUT = ASSET_DIR / "walkthrough.gif"
CANVAS = (1200, 800)
FRAME_DURATION_MS = 2200


def build(output: Path) -> None:
    missing = [path for path in SOURCES if not path.exists()]
    if missing:
        raise SystemExit("Missing live-demo screenshots: " + ", ".join(map(str, missing)))

    frames: list[Image.Image] = []
    for source in SOURCES:
        with Image.open(source) as image:
            rgb = image.convert("RGB")
            contained = ImageOps.contain(rgb, CANVAS, method=Image.Resampling.LANCZOS)
            canvas = Image.new("RGB", CANVAS, "white")
            x = (CANVAS[0] - contained.width) // 2
            y = (CANVAS[1] - contained.height) // 2
            canvas.paste(contained, (x, y))
            palette_frame = canvas.convert(
                "P",
                palette=Image.Palette.ADAPTIVE,
                colors=160,
                dither=Image.Dither.NONE,
            )
            frames.append(palette_frame)

    output.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        output,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION_MS,
        loop=0,
        optimize=False,
        disposal=2,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail when the committed walkthrough.gif is missing or stale.",
    )
    args = parser.parse_args()

    if not args.check:
        build(OUTPUT)
        print(f"Built {OUTPUT.relative_to(ROOT)}")
        return 0

    if not OUTPUT.exists():
        raise SystemExit("walkthrough.gif is missing; run python scripts/build_demo_gif.py")

    with tempfile.TemporaryDirectory() as tmpdir:
        candidate = Path(tmpdir) / "walkthrough.gif"
        build(candidate)
        if candidate.read_bytes() != OUTPUT.read_bytes():
            raise SystemExit(
                "walkthrough.gif is stale; run python scripts/build_demo_gif.py and commit it"
            )

    print("Live-demo GIF is up to date")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
