#!/usr/bin/env python

import subprocess
import os
from pathlib import Path

IMAGE_PATH = Path.home() / ".config" / "bspwm" / "wallpaper" / "rofi" / "custom_script_checks.png"

process_list = [
    'bspwm',
    'sxhkd',
    'dunst',
    'picom',
    'polybar',
    'greenclip',
    'pipewire',
    'pipewire-pulse',
    'wireplumber'
]

env_list = [
    {
        "name": "dbus",
        "var": "DBUS_SESSION_BUS_ADDRESS"
    }
]

def print_image(path: Path) -> None:
    if not path.exists():
        print(f"[image not found: {path}]")
        return

    try:
        subprocess.run(
            [
                "chafa",
                str(path),
                "--size=40x20",
            ],
            check=True
        )
    except Exception:
        print("[failed to render image]")

def check_firewall() -> None:
    result = subprocess.run(
        ["sudo", "ufw", "status"],
        capture_output=True,
        text=True
    )

    if "Status: active" in result.stdout:
        print("firewall OK: ufw")
    else:
        print("firewall FAIL: ufw")

def check_process(process: str) -> bool:
    result = subprocess.run(
        ['pgrep', '-x', process],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0

def check_env(var: str) -> bool:
    return bool(os.environ.get(var))

def check_process_list() -> None:
    for p in process_list:
        status = f"OK" if check_process(p) else f"FAIL"
        print(f'process {status}: {p}')

def check_env_list() -> None:
    for e in env_list:
        status = "OK" if check_env(e["var"]) else "FAIL"
        print(f'env {status}: {e["name"]}')

def main() -> None:
    print_image(IMAGE_PATH)
    print()
    check_process_list()
    check_env_list()
    #check_firewall()

    input("\nPress Enter to exit...")

if __name__ == '__main__':
    main()
