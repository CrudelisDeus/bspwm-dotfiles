#!/bin/sh
# LightDM greeter-setup: pick a random wallpaper from current rice and set greeter background

set -eu

# Determine real user home (not lightdm/root)
USER_HOME="/home/$USER"
if [ "${USER:-}" = "lightdm" ] || [ "${USER:-}" = "root" ] || [ ! -d "$USER_HOME" ]; then
    REAL_USER=$(getent passwd | awk -F: '$3>=1000 && $3<65534 {print $1; exit}')
    USER_HOME="/home/${REAL_USER:-$USER}"
fi

RICE_FILE="$USER_HOME/.config/bspwm/.rice"
GREETER_BG="/var/cache/lightdm/greeter-wallpaper.webp"

# Ensure cache dir exists
install -d -m 0755 "$(dirname "$GREETER_BG")"

pick_random_wall() {
    rice_name="default"
    [ -f "$RICE_FILE" ] && rice_name=$(head -n1 "$RICE_FILE")

    rice_dir1="$USER_HOME/.config/bspwm/rices/$rice_name"
    rice_dir2="$USER_HOME/bspwm/rices/$rice_name"
    # Prefer walls subdir if exists
    if [ -d "$rice_dir1/walls" ]; then
        search_dir="$rice_dir1/walls"
    elif [ -d "$rice_dir2/walls" ]; then
        search_dir="$rice_dir2/walls"
    elif [ -d "$rice_dir1" ]; then
        search_dir="$rice_dir1"
    else
        search_dir="$rice_dir2"
    fi

    # Find .webp files and pick one randomly
    set +e
    mapfile -t files <<EOF
$(find "$search_dir" -maxdepth 2 -type f -name "*.webp" 2>/dev/null)
EOF
    set -e
    if [ "${#files[@]}" -gt 0 ]; then
        idx=$((RANDOM % ${#files[@]}))
        printf '%s\n' "${files[$idx]}"
        return 0
    fi
    return 1
}

if wall=$(pick_random_wall); then
    # Convert to a friendly size/format if needed; copy as webp
    if command -v dwebp >/dev/null 2>&1 && command -v cwebp >/dev/null 2>&1; then
        tmp_png="/tmp/ldm_wall_${RANDOM}.png"
        dwebp "$wall" -o "$tmp_png" >/dev/null 2>&1 || cp -f "$wall" "$GREETER_BG"
        cwebp -q 90 "$tmp_png" -o "$GREETER_BG" >/dev/null 2>&1 || cp -f "$wall" "$GREETER_BG"
        rm -f "$tmp_png" 2>/dev/null || true
    else
        # Direct copy; greeter reads webp via webp-pixbuf-loader
        cp -f "$wall" "$GREETER_BG"
    fi
fi

# Relax permissions so greeter can read
chmod 0644 "$GREETER_BG" 2>/dev/null || true

exit 0


