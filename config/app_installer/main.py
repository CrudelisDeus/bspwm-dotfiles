from c_pacman import enable_multilib
from i_pkg import install_package
from i_gpu import install_gpu


def main():
    enable_multilib()
    install_gpu()
    install_package()


if __name__ == "__main__":
    main()
