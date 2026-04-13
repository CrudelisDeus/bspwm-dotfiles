#!/usr/bin/env python3

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
    "mpv",

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

    # change default theme (dark or light)
    "gsettings",
    "dconf",
    "gsettings-desktop-schemas",
]

yay_pkg = [
    'base-devel',
    'git',
]

yay_list_pkg = [
    # clip hisrory
    'greenclip',

    # lockscreen
    'i3lock-color',

#    # launcher
#    'eww',
    # wallpaper
    "xwinwrap-git",
]

work_and_home_pkg = [
    "telegram-desktop",
    "discord",
    "anki",
    "obsidian",
    "obs-studio",
    # for anki TTS
    "speech-dispatcher",
    "espeak-ng"
]

nvidia_pkg = [
    'nvidia-dkms',
    'nvidia-utils',
    'nvidia-settings',
    'linux-headers',
]

firewall_pkg = [
    'ufw',
]

def install_pkg(pkgs: list) -> None:
    for pkg in pkgs:
        try:
            subprocess.run(
                ['sudo', 'pacman', '-S', pkg, '--noconfirm'],
                check=True,
                capture_output=True,
                text=True
            )
            result = 0
        except Exception:
            result = 1

        if result != 0:
            print(f'pkg FAILED: {pkg}')
        else:
            print(f'pkg OK: {pkg}')

# yay install
def clone_yay():
    try:
        subprocess.run(
            [
                'git',
                'clone',
                'https://aur.archlinux.org/yay.git',
                '/tmp/yay'
            ],
            check=True,
            capture_output=True,
            text=True
        )
        result = 0
    except Exception:
        result = 1

    if result != 0:
        print(f'yay FAILED: clone')
    else:
        print(f'yay OK: clone')

def configure_yay():
    try:
        subprocess.run(
            ['makepkg', '-si', '--noconfirm'],
            check=True,
            text=True,
            cwd='/tmp/yay',
            capture_output=True,
        )
        result = 0
    except Exception:
        result = 1

    if result != 0:
        print(f'yay FAILED: configure')
    else:
        print(f'yay OK: configure')

def install_yay_pkg(pkgs: list) -> None:
    for pkg in pkgs:
        try:
            subprocess.run(
                ['yay', '-S', pkg, '--noconfirm', '--needed'],
                check=True,
                capture_output=True,
                text=True
            )
            result = 0
        except Exception:
            result = 1

        if result != 0:
            print(f'yay pkg FAILED: {pkg}')
        else:
            print(f'yay pkg OK: {pkg}')

def install_yay():
    install_pkg(yay_pkg)
    clone_yay()
    configure_yay()

def create_std_dir():
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
        result = 0
    except Exception:
        result = 1
    if result != 0:
        print(f'std dir: FAILED')
    else:
        print(f'std dir: OK')

def enable_firewall():
    try:
        subprocess.run(
            ["sudo", "ufw", "--force", "enable"],
            check=True,
            capture_output=True,
            text=True
        )
        subprocess.run(
            ["sudo", "systemctl", "enable", "ufw"],
            check=True,
            capture_output=True,
            text=True
        )
        result = 0
    except Exception:
        result = 1

    if result != 0:
        print("ufw start: FAILED")
    else:
        print("ufw start: OK")

def create_std_rule_firewall():
    try:
        subprocess.run(
            ["sudo", "ufw", "default", "deny", "incoming"],
            check=True,
            capture_output=True,
            text=True
        )
        subprocess.run(
            ["sudo", "ufw", "default", "allow", "outgoing"],
            check=True,
            capture_output=True,
            text=True
        )
        result = 0
    except Exception:
        result = 1

    if result != 0:
        print(f'ufw rule: FAILED')
    else:
        print(f'ufw rule: OK')

def setup_firewall():
    install_pkg(firewall_pkg)
    create_std_rule_firewall()
    enable_firewall()

# start programm
def main():
    install_pkg(std_pkg)
    install_pkg(work_and_home_pkg)

    install_yay()
    install_yay_pkg(yay_list_pkg)

    #install_pkg(nvidia_pkg)

    create_std_dir()

    setup_firewall()

if __name__ == '__main__':
    main()
