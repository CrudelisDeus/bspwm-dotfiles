#!/usr/bin/env python3

import os
import shutil
import subprocess
from pathlib import Path
from datetime import datetime


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

    # usb
    "udisks2",
    "udiskie",
    "ntfs-3g",
    "exfatprogs",
    "gvfs",
    "gvfs-mtp",

    # network
    "networkmanager",
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

def enable_networkmanager() -> bool:
    try:
        subprocess.run(
            ["sudo", "systemctl", "enable", "--now", "NetworkManager"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("NetworkManager: OK")
        return True
    except subprocess.CalledProcessError as e:
        print("NetworkManager: FAILED")
        if e.stderr:
            print(e.stderr.strip())
        return False

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

def logo() -> None:
    logo = r"""       _ /\      /\ _
      / X  \.--./  X \
     /_/ \/`    `\/ \_\
    /|(`-/\_/)(\_/\-`)|\
   ( |` (_(.oOOo.)_) `| )
   ` |  `//\(  )/\\`  | `
     (  // ()\/() \\  )
      ` (   \   /   ) `
         \         /
          `       `"""
    print(logo)

def log_step(ok: bool, action: str, src: str, dst: str = "") -> None:
    status = "OK" if ok else "FAILED"
    if dst:
        print(f"{status} -> {action}: {src} -> {dst}")
    else:
        print(f"{status} -> {action}: {src}")

def setup_user_files() -> bool:
    BASE_DIR = Path(__file__).resolve().parent

    SRC_CONFIG = BASE_DIR / "config"
    SRC_HOME = BASE_DIR / "home"

    HOME_DIR = Path.home()
    HOME_CONFIG = HOME_DIR / ".config"

    ALLOWED_CONFIGS = {
        "bspwm",
        "dunst",
        "fastfetch",
        "kitty",
        "nvim",
        "picom",
        "polybar",
        "rofi",
        "speech-dispatcher",
        "sxhkd",
        "yazi",
    }

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    BACKUP_ROOT = Path("/tmp") / f"backup_dotfiles_{timestamp}"

    try:
        if not SRC_CONFIG.exists():
            log_step(False, "source", str(SRC_CONFIG))
            return False

        if not SRC_HOME.exists():
            log_step(False, "source", str(SRC_HOME))
            return False

        BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
        log_step(True, "create dir", str(BACKUP_ROOT))

        def backup_path(dst: Path) -> Path:
            return BACKUP_ROOT / dst.relative_to(HOME_DIR)

        def backup_and_remove(dst: Path) -> None:
            bkp = backup_path(dst)
            bkp.parent.mkdir(parents=True, exist_ok=True)

            if dst.is_symlink() or dst.is_file():
                shutil.copy2(dst, bkp)
                log_step(True, "backup", str(dst), str(bkp))
                dst.unlink()
                log_step(True, "remove", str(dst))

            elif dst.is_dir():
                shutil.copytree(dst, bkp, dirs_exist_ok=True)
                log_step(True, "backup", str(dst), str(bkp))
                shutil.rmtree(dst)
                log_step(True, "remove", str(dst))

        HOME_CONFIG.mkdir(parents=True, exist_ok=True)
        log_step(True, "create dir", str(HOME_CONFIG))

        for item in SRC_CONFIG.iterdir():
            if item.name not in ALLOWED_CONFIGS:
                print(f"SKIP config: {item.name}")
                continue

            dst = HOME_CONFIG / item.name

            if dst.exists() or dst.is_symlink():
                backup_and_remove(dst)

            if item.is_dir():
                shutil.copytree(item, dst)
            else:
                shutil.copy2(item, dst)

            log_step(True, "copy", str(item), str(dst))

        for item in SRC_HOME.iterdir():
            dst = HOME_DIR / item.name

            if dst.exists() or dst.is_symlink():
                backup_and_remove(dst)

            if item.is_dir():
                shutil.copytree(item, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dst)

            log_step(True, "copy", str(item), str(dst))

        log_step(True, "install", "user files")
        return True

    except Exception as e:
        log_step(False, "install", "user files")
        print(str(e))
        return False

def handle_nvim_config() -> bool:
    nvim_dir = Path.home() / ".config" / "nvim"

    try:
        if not nvim_dir.exists():
            print("nvim config: SKIPPED (not found)")
            return True

        if ask_yes_no("Do you want to keep nvim config? (y/n): "):
            print("nvim config: KEEP")
            return True

        shutil.rmtree(nvim_dir)
        print("nvim config: REMOVED")
        return True

    except Exception as e:
        print("nvim config: FAILED")
        print(str(e))
        return False

def main() -> None:
    os.system("clear")

    logo()

    if not ask_yes_no("\nDo you want to install karakurtOS? (y/n): "):
        return

    run_step("Install std packages", lambda: install_pkg(std_pkg))
    run_step("Install yay", install_yay)
    run_step("Install yay packages", lambda: install_yay_pkg(yay_list_pkg))
    run_step("Create standard dirs", create_std_dir)
    run_step("Enable NetworkManager", enable_networkmanager)
    run_step("Setup user files", setup_user_files)
    input("\nPress Enter...")

    os.system("clear")
    logo()
    run_step("Handle nvim config", handle_nvim_config)
    input("\nPress Enter...")

    os.system("clear")
    logo()
    if ask_yes_no("\nDo you want to install work and home packages? (y/n): "):
        run_step("Install work and home packages", lambda: install_pkg(work_and_home_pkg))
        input("\nPress Enter...")

    os.system("clear")
    logo()
    if ask_yes_no("\nDo you want to install NVIDIA drivers? (y/n): "):
        run_step("Install NVIDIA", lambda: install_pkg(nvidia_pkg))
        input("\nPress Enter...")

    os.system("clear")
    logo()
    if ask_yes_no("\nDo you want to set up the firewall? (y/n): "):
        run_step("Setup firewall", setup_firewall)
        input("\nPress Enter...")

    os.system('clear')

if __name__ == "__main__":
    main()
