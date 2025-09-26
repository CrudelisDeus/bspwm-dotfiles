import subprocess

default_pkg = [
    "obsidian", "git-crypt", "openssh",
    "telegram-desktop", "discord", "rsync",
    "curl", "pavucontrol", "cronie",
    "wget", "obs-studio", "krita",
    "hunspell", "hunspell-en_US",
    "hunspell-ru", "hunspell-uk"
]

work_pkg = ["signal-desktop", "thunderbird"]


def install_pkg(user_imput=None):
    """ Install packages for work environment """
    if user_imput == 'work':
        pkg = default_pkg + work_pkg
    elif user_imput == 'home':
        pkg = default_pkg
    else:
        pkg = []

    for p in pkg:
        if p:
            result = subprocess.run(
                ["sudo", "pacman", "-S", p, "--noconfirm"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            if result.returncode != 0:
                print(f"Pkg {p}: Failed")
            elif result.returncode == 0:
                print(f"Pkg {p}: Success")
        else:
            pass


def update_system():
    """ Update system packages """
    import subprocess
    result = subprocess.run(
        ["sudo", "pacman", "-Syu", "--noconfirm"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    if result.returncode != 0:
        print("System update: Failed")
    elif result.returncode == 0:
        print("System update: Success")


def install_package():
    """ Environment Installation """
    while True:
        user_input = input("Choose your environment (work/home/skip): ")
        if user_input.lower() == 'work':
            update_system()
            install_pkg(user_input.lower())
            break
        elif user_input.lower() == 'home':
            update_system()
            install_pkg(user_input.lower())
            break
        elif user_input.lower() == 'skip':
            break
        else:
            print("Invalid input. Please enter 'work' or 'home' or 'skip'.")


if __name__ == "__main__":
    install_package()
