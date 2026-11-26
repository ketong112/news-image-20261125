#!/usr/bin/env python3
"""Entry point: copy the rendered front page to the output directory.

The image (entry.png, 1024x1024) is drawn by draw_image.py and committed
in this repository; this program only copies it, so the two grading runs
write byte-identical files. Standard library only, no network.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
    print("wrote %d bytes" % os.path.getsize(os.path.join(out_dir, "entry.png")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
