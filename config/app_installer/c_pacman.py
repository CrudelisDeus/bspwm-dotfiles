def enable_multilib(path='/etc/pacman.conf'):
    """ Enable multilib repository in pacman.conf """
    import fileinput
    import sys

    in_multilib = False
    try:
        for line in fileinput.input(path, inplace=True):
            if line.lstrip().startswith('#[multilib]'):
                in_multilib = True
                sys.stdout.write('[multilib]\n')
            elif in_multilib and line.lstrip().startswith('#Include'):
                sys.stdout.write('Include = /etc/pacman.d/mirrorlist\n')
                in_multilib = False
            else:
                sys.stdout.write(line)
        print('Multilib enabled: Success')
    except Exception as e:
        print(f'Multilib enabled: Failed - {e}')


if __name__ == "__main__":
    enable_multilib()
