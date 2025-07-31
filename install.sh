# ---------------- # 
# Dmytro Shvydenko #
# -----2025------- #
# ---------------- # 
# 1. global update #
# 2. create dir    #

# ---------------- #

# var

std_config=(
    bspwm sxhkd polybar
)

# function

global_update() {
    sudo pacman -Syu --noconfirm
}

create_dir_config() {
    mkdir ~/.config
    
    # copy config
    for i in "${std_config[@]}"; do 
        mkdir -p ~/.config/$i
        cp -r ./config/$i/* ~/.config/$i/
        chmod +x ~/.config/$i/*
    done
    
    # copy x conf
    cp ./config/x/.xinitrc ~/.xinitrc
}

install_pkg() {
    # Xserver
    sudo pacman -S xorg-server xorg-xinit --noconfirm

    # Videodriver (test)
    sudo pacman -S xf86-video-vesa --noconfirm

    # BSPWM and related packages
    sudo pacman -S bspwm sxhkd polybar --noconfirm

    # Terminal
    sudo pacman -S kitty --noconfirm
}

# run

global_update
create_dir_config
install_pkg