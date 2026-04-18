#!/usr/bin/python

# Simple font manager for kitty and polybar
# Uses global font size if set, otherwise applies individual values
# Cleans duplicates and ensures correct config formatting

#!/usr/bin/python

from pathlib import Path
import re
import subprocess

# GLOBAL FONT SIZE
# <==============================
FONT_SIZE_GLOBAL = ''
FONT_SIZE_KITTY = '10.5'
FONT_SIZE_POLYBAR = '10;2'
# <==============================


def ensure_font_config_file() -> Path:
    conf_dir = Path.home() / ".config" / "bspwm" / "conf"
    conf_dir.mkdir(parents=True, exist_ok=True)

    font_file = conf_dir / "font.txt"
    if not font_file.exists():
        font_file.touch()

    return font_file


def write_font_values_to_file() -> bool:
    try:
        font_file = ensure_font_config_file()

        content = (
            f"FONT_SIZE_GLOBAL={FONT_SIZE_GLOBAL}\n"
            f"FONT_SIZE_KITTY={FONT_SIZE_KITTY}\n"
            f"FONT_SIZE_POLYBAR={FONT_SIZE_POLYBAR}\n"
        )

        font_file.write_text(content)
        return True

    except Exception as e:
        print(f"font file error: {e}")
        return False


def reload_polybar():
    subprocess.run(["killall", "-q", "polybar"], stderr=subprocess.DEVNULL)
    subprocess.run(
        ["sh", "-c", "while pgrep -x polybar >/dev/null; do sleep 0.5; done; polybar main &"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def change_kitty_font() -> bool:
    try:
        path = Path.home() / ".config" / "kitty" / "kitty.conf"
        text = path.read_text()

        font_size = FONT_SIZE_GLOBAL if FONT_SIZE_GLOBAL else FONT_SIZE_KITTY
        if not font_size:
            return False

        lines = text.splitlines()

        cleaned_lines = []
        for line in lines:
            stripped = line.strip()

            if stripped in {"P", "H.5"}:
                continue

            if re.match(r'^\s*font_size\s+', line):
                continue

            cleaned_lines.append(line)

        new_lines = []
        inserted = False

        for line in cleaned_lines:
            new_lines.append(line)

            if re.match(r'^\s*font_family\s+', line) and not inserted:
                new_lines.append(f"font_size {font_size}")
                inserted = True

        if not inserted:
            new_lines.insert(0, f"font_size {font_size}")

        path.write_text("\n".join(new_lines) + "\n")
        return True

    except Exception as e:
        print(f"kitty error: {e}")
        return False


def change_polybar_font() -> bool:
    try:
        path = Path.home() / ".config" / "polybar" / "config.ini"
        text = path.read_text()

        font_size = FONT_SIZE_GLOBAL if FONT_SIZE_GLOBAL else FONT_SIZE_POLYBAR
        if not font_size:
            return False

        pattern = r'(?m)^(\s*font-\d+\s*=\s*"[^"\n]*:size=)([^"\n]+)(")$'
        new_text, count = re.subn(pattern, rf'\g<1>{font_size}\g<3>', text)

        if count == 0:
            return False

        path.write_text(new_text)
        return True

    except Exception as e:
        print(f"polybar error: {e}")
        return False


def main():
    if write_font_values_to_file():
        print("OK: font.txt updated")
    else:
        print("FAILED: font.txt updated")

    if change_kitty_font():
        print("OK: kitty font_size changed")
    else:
        print("FAILED: kitty font_size changed")

    if change_polybar_font():
        print("OK: polybar font size changed")
    else:
        print("FAILED: polybar font size changed")

    reload_polybar()


if __name__ == '__main__':
    main()
