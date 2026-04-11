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


def gsettings_set(schema: str, key: str, value: str) -> None:
    subprocess.run(
        ["gsettings", "set", schema, key, value],
        check=True,
    )


def set_light() -> None:
    gsettings_set("org.gnome.desktop.interface", "gtk-theme", "Adwaita")
    gsettings_set("org.gnome.desktop.interface", "color-scheme", "default")


def set_dark() -> None:
    gsettings_set("org.gnome.desktop.interface", "gtk-theme", "Adwaita-dark")
    gsettings_set("org.gnome.desktop.interface", "color-scheme", "prefer-dark")


def main() -> None:
    try:
        current_theme = gsettings_get("org.gnome.desktop.interface", "gtk-theme")
        current_scheme = gsettings_get("org.gnome.desktop.interface", "color-scheme")

        print(f"Current gtk-theme: {current_theme}")
        print(f"Current color-scheme: {current_scheme}")

        if current_theme == "Adwaita-dark" or current_scheme == "prefer-dark":
            set_light()
            print("Switched to LIGHT")
        else:
            set_dark()
            print("Switched to DARK")

    except subprocess.CalledProcessError as exc:
        print("gsettings command failed")
        print(exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
