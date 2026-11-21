"""Entrypoint: render the Talmara passport spread to entry.png.

Writes a single deterministic 1024x1024 PNG (the make.fun entry image)
into $MAKEFUN_OUTPUT_DIR (default /output). Stdlib + PIL only, no network.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate import build

OUTPUT_FILENAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"
EXPECTED_SIZE = (1024, 1024)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    if not out_dir:
        raise SystemExit("MAKEFUN_OUTPUT_DIR is set but empty")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_FILENAME)
    build(path)
    from PIL import Image

    with Image.open(path) as im:
        if im.size != EXPECTED_SIZE or im.format != "PNG":
            raise SystemExit(f"bad output: {im.format} {im.size}")
    print("wrote", path)


if __name__ == "__main__":
    main()
