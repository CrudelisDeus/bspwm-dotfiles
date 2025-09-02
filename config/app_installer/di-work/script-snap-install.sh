cd ~
git clone https://aur.archlinux.org/snapd.git
cd snapd
# Build and install without any interactive prompts
makepkg -si --noconfirm --noedit --noprogressbar