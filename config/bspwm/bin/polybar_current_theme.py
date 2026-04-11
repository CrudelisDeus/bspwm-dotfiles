#!/usr/bin/env python3

import subprocess
import sys


def gsettings_get(schema: str, key: str) -> str:
    result = subprocess.run(
        ["gsettings", "get", schema, key],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip().strip("'")


def main() -> None:
    try:
        theme = gsettings_get("org.gnome.desktop.interface", "gtk-theme")
        scheme = gsettings_get("org.gnome.desktop.interface", "color-scheme")

        if theme == "Adwaita-dark" or scheme == "prefer-dark":
            print("󰽧")
        else:
            print("󰖙")
    except Exception:
        print("?")


if __name__ == "__main__":
    main()
