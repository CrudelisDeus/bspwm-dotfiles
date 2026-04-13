#!/usr/bin/env python3

import os
import shutil
import subprocess
from pathlib import Path


# pkg
std_pkg = [
    # python
    "python",

    # openssh
    "openssh",

    # fonts
    "ttf-dejavu",
    "ttf-font-awesome",
    "ttf-nerd-fonts-symbols",
    "ttf-jetbrains-mono-nerd",
    "noto-fonts",

    # notify
    "dunst",
    "libnotify",

    # dbus
    "dbus",
    "libcanberra",
    "xdg-desktop-portal",
    "xdg-desktop-portal-gtk",

    # xorg
    "xorg-xinit",
    "xorg",

    # bspwm
    "bspwm",
    "sxhkd",

    # shell output
    "bat",
    "eza",
    "btop",
    "fastfetch",
    "less",

    # code editor
    "vim",
    "neovim",
    "nodejs",
    "npm",
    "git",
    "base-devel",

    # terminal
    "kitty",

    # wallpaper
    "feh",
    "xorg-xrandr",
    "mpv",

    # compositor
    "picom",

    # bar
    "polybar",

    # clipboard
    "xclip",
    "xsel",

    # launcher
    "rofi",

    # browser
    "firefox",

    # file manager
    "yazi",
    "ffmpegthumbnailer",
    "poppler",
    "fd",
    "ripgrep",
    "fzf",
    "zoxide",
    "chafa",
    "resvg",
    "7zip",

    # audio
    "pipewire",
    "pipewire-audio",
    "pipewire-alsa",
    "pipewire-pulse",
    "wireplumber",
    "alsa-utils",

    # screenshot
    "flameshot",

    # lockscreen
    "imagemagick",
    "scrot",

    # color selector
    "xcolor",

    # update mirror
    "reflector",
    "pacman-contrib",

    # theme
    "dconf",
    "gsettings-desktop-schemas",

    "udisks2",
    "udiskie",
]

yay_pkg = [
    "base-devel",
    "git",
]

yay_list_pkg = [
    "greenclip",
    "i3lock-color",
    "xwinwrap-git",
]

work_and_home_pkg = [
    "telegram-desktop",
    "discord",
    "anki",
    "obsidian",
    "obs-studio",
    "speech-dispatcher",
    "espeak-ng",
]

nvidia_pkg = [
    "nvidia-dkms",
    "nvidia-utils",
    "nvidia-settings",
    "linux-headers",
]

firewall_pkg = [
    "ufw",
]


def ask_yes_no(prompt: str) -> bool:
    answer = input(prompt).strip().lower()
    return answer in ("y", "yes")


def install_pkg(pkgs: list[str]) -> bool:
    for pkg in pkgs:
        try:
            subprocess.run(
                ["sudo", "pacman", "-S", pkg, "--noconfirm", "--needed"],
                check=True,
                capture_output=True,
                text=True,
            )
            print(f"pkg OK: {pkg}")
        except subprocess.CalledProcessError as e:
            print(f"pkg FAILED: {pkg}")
            if e.stderr:
                print(e.stderr.strip())
            return False

    return True


def clone_yay() -> bool:
    yay_dir = Path("/tmp/yay")

    try:
        if yay_dir.exists():
            shutil.rmtree(yay_dir)

        subprocess.run(
            [
                "git",
                "clone",
                "https://aur.archlinux.org/yay.git",
                str(yay_dir),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        print("yay OK: clone")
        return True
    except subprocess.CalledProcessError as e:
        print("yay FAILED: clone")
        if e.stderr:
            print(e.stderr.strip())
        return False


def configure_yay() -> bool:
    try:
        subprocess.run(
            ["makepkg", "-si", "--noconfirm"],
            check=True,
            cwd="/tmp/yay",
            capture_output=True,
            text=True,
        )
        print("yay OK: configure")
        return True
    except subprocess.CalledProcessError as e:
        print("yay FAILED: configure")
        if e.stderr:
            print(e.stderr.strip())
        return False


def install_yay_pkg(pkgs: list[str]) -> bool:
    for pkg in pkgs:
        try:
            subprocess.run(
                ["yay", "-S", pkg, "--noconfirm", "--needed"],
                check=True,
                capture_output=True,
                text=True,
            )
            print(f"yay pkg OK: {pkg}")
        except subprocess.CalledProcessError as e:
            print(f"yay pkg FAILED: {pkg}")
            if e.stderr:
                print(e.stderr.strip())
            return False

    return True


def install_yay() -> bool:
    if shutil.which("yay"):
        print("yay OK: already installed")
        return True

    if not install_pkg(yay_pkg):
        return False

    if not clone_yay():
        return False

    if not configure_yay():
        return False

    return True


def create_std_dir() -> bool:
    std_dir = [
        "Downloads",
        "Pictures",
        "Videos",
        "projects",
    ]
    home = Path.home()

    try:
        for name in std_dir:
            (home / name).mkdir(exist_ok=True)

        print("std dir: OK")
        return True
    except Exception as e:
        print("std dir: FAILED")
        print(str(e))
        return False


def enable_firewall() -> bool:
    try:
        subprocess.run(
            ["sudo", "ufw", "--force", "enable"],
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            ["sudo", "systemctl", "enable", "ufw"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("ufw start: OK")
        return True
    except subprocess.CalledProcessError as e:
        print("ufw start: FAILED")
        if e.stderr:
            print(e.stderr.strip())
        return False


def create_std_rule_firewall() -> bool:
    try:
        subprocess.run(
            ["sudo", "ufw", "default", "deny", "incoming"],
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            ["sudo", "ufw", "default", "allow", "outgoing"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("ufw rule: OK")
        return True
    except subprocess.CalledProcessError as e:
        print("ufw rule: FAILED")
        if e.stderr:
            print(e.stderr.strip())
        return False


def setup_firewall() -> bool:
    if not install_pkg(firewall_pkg):
        return False

    if not create_std_rule_firewall():
        return False

    if not enable_firewall():
        return False

    return True


def run_step(name: str, func) -> None:
    while True:
        print(f"\n== {name} ==")

        if func():
            return

        if not ask_yes_no("Failed. Retry? (y/n): "):
            return


def main() -> None:
    os.system("clear")

    if not ask_yes_no("Do you want to install DeusOS? (y/n)\n"):
        return

    run_step("Install std packages", lambda: install_pkg(std_pkg))
    run_step("Install yay", install_yay)
    run_step("Install yay packages", lambda: install_yay_pkg(yay_list_pkg))
    run_step("Create standard dirs", create_std_dir)
    input("\nPress Enter...")

    os.system("clear")
    if ask_yes_no("Do you want to install work and home packages? (y/n)\n"):
        run_step("Install work and home packages", lambda: install_pkg(work_and_home_pkg))
        input("\nPress Enter...")

    os.system("clear")
    if ask_yes_no("Do you want to install NVIDIA drivers? (y/n)\n"):
        run_step("Install NVIDIA", lambda: install_pkg(nvidia_pkg))
        input("\nPress Enter...")

    os.system("clear")
    if ask_yes_no("Do you want to set up the firewall? (y/n)\n"):
        run_step("Setup firewall", setup_firewall)
        input("\nPress Enter...")

    os.system('clear')

if __name__ == "__main__":
    main()
