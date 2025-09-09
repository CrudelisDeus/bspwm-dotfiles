# script-snap-install.sh

set -e

sudo pacman -Sy --noconfirm

sudo pacman -S --needed --noconfirm go go-tools xfsprogs python-docutils autoconf-archive

if command -v paru >/dev/null 2>&1; then
  paru -S --noconfirm snapd
else
  cd ~
  if [ ! -d snapd ]; then
    git clone https://aur.archlinux.org/snapd.git
  fi
  cd snapd
  makepkg -si --noconfirm --noedit --noprogressbar
fi

sudo systemctl enable --now snapd.socket
if [ ! -e /snap ]; then
  sudo ln -s /var/lib/snapd/snap /snap
fi