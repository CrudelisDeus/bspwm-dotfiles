#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess


def which_first(*names: str) -> str:
    for n in names:
        p = shutil.which(n)
        if p:
            return p
    return ""


def main() -> int:
    # If no path provided, quickly capture a full-screen shot ourselves
    if len(sys.argv) < 2:
        pictures = os.popen('xdg-user-dir PICTURES').read().strip() or os.path.expanduser('~/Pictures')
        os.makedirs(os.path.join(pictures, 'ScreenShots'), exist_ok=True)
        from datetime import datetime
        filename = f"Shot-{datetime.now().strftime('%Y-%m-%d-%H%M%S')}.png"
        path = os.path.join(pictures, 'ScreenShots', filename)
        maim = which_first("maim")
        if not maim:
            print("maim is required to create screenshot.", file=sys.stderr)
            return 1
        # fast full-screen capture
        r = subprocess.run([maim, "-u", "-d", "0", path])
        if r.returncode != 0:
            return r.returncode
    else:
        path = sys.argv[1]

    # Optional: Respect user-defined IMAGE_EDITOR
    editor = os.environ.get("IMAGE_EDITOR")
    if editor and shutil.which(editor):
        os.execvp(editor, [editor, path])
        return 0

    slop = which_first("slop")
    magick = which_first("magick", "convert")

    if not slop or not magick:
        print("Missing tools for crop. Required: slop and imagemagick (magick/convert)", file=sys.stderr)
        return 1

    # Fast path: don't show overlay viewer; just select region on screen
    # Output from slop: x y w h in global coordinates
    p = subprocess.run([slop, "-f", "%x %y %w %h"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    selection = p.stdout.strip()

    if not selection:
        # User cancelled selection
        return 1

    try:
        x, y, w, h = (int(v) for v in selection.split())
    except Exception:
        print(f"Invalid selection: {selection}", file=sys.stderr)
        return 1

    # If caller passed monitor geometry, offset crop to local coords
    # argv[2] format: WxH+X+Y
    if len(sys.argv) >= 3 and "+" in sys.argv[2]:
        try:
            geo = sys.argv[2]
            size, offx, offy = geo.split("+")
            base_x = int(offx)
            base_y = int(offy)
            x -= base_x
            y -= base_y
        except Exception:
            pass

    geometry = f"{w}x{h}+{x}+{y}"
    # Crop in-place
    cmd = [magick, path, "-crop", geometry, "+repage", path]
    if os.path.basename(magick) == "convert":
        # Older imagemagick 'convert' syntax is the same
        cmd = [magick, path, "-crop", geometry, "+repage", path]

    r = subprocess.run(cmd)
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())



