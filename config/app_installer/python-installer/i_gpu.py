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
        exit(1)
    elif result.returncode == 0:
        print("System update: Success")


def install_nvidia_driver():
    """ Install NVIDIA driver """
    pkg = ["nvidia", "nvidia-utils", "nvidia-settings", "lib32-nvidia-utils"]
    import subprocess
    for p in pkg:
        result = subprocess.run(
            ["sudo", "pacman", "-S", p, "--noconfirm"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if result.returncode != 0:
            print(f"Pkg {p}: Failed")
            exit(1)
        elif result.returncode == 0:
            print(f"Pkg {p}: Success")


def install_gpu():
    """ Install GPU driver """
    while True:
        user_input = input("Select type of GPU (nvidia/skip): ")
        if user_input.lower() == 'nvidia':
            update_system()
            install_nvidia_driver()
            break
        elif user_input.lower() == 'skip':
            break
        else:
            print("Invalid input. Please enter 'nvidia' or 'skip'.")


install_gpu()
