import subprocess 

# pkg 
std_pkg = [
    # python
    "python",
    
    # fonts
    "ttf-dejavu",
    "ttf-font-awesome",
    "ttf-nerd-fonts-symbols",
    "ttf-jetbrains-mono-nerd",
    "noto-fonts",

    # dbus
    "dbus",
    "dunst",
    "libcanberra",
    "xdg-desktop-portal",
    "xdg-desktop-portal-gtk",

    # xorg
    "xorg-xinit",
    "xorg",

    # bspwm
    "bspwm",
    "sxhkd",

]

# function

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
        except Exception as e:
            result = 1

        if result != 0:
            print(f'pkg FAILED: {pkg}')
        else:
            print(f'pkg OK: {pkg}')

# start
def main():
    install_pkg(std_pkg)

if __name__ == '__main__':
    main()
