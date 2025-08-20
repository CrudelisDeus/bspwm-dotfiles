#!/usr/bin/env bash
# set-1080p.sh — force 1920x1080@60 on all connected outputs via xrandr

set -euo pipefail

W=1920
H=1080
R=60
MODE_NAME="${W}x${H}_${R}.00"
# запасной Modeline на случай отсутствия `cvt`
FALLBACK_MODELINE='1920x1080_60.00 173.00 1920 2048 2248 2576 1080 1083 1088 1120 -hsync +vsync'

have_mode_global() { xrandr --query | grep -q "\"$MODE_NAME\""; }
add_mode_global() {
  if command -v cvt >/dev/null 2>&1; then
    # берём всё после слова Modeline
    read -r _ name rest < <(cvt "$W" "$H" "$R" | awk '/Modeline/{print $1, $2, substr($0, index($0,$3))}')
    # name == "$MODE_NAME"
    xrandr --newmode "$name" $rest
  else
    # без cvt — используем заранее известный modeline
    xrandr --newmode $FALLBACK_MODELINE
  fi
}

# 1) глобально объявляем режим, если его ещё нет
if ! have_mode_global; then
  echo "[i] Adding global mode $MODE_NAME"
  add_mode_global || { echo "[!] Failed to add global mode"; exit 1; }
fi

# 2) обрабатываем все подключённые выходы
outputs=$(xrandr | awk '/ connected/{print $1}')
if [[ -z "$outputs" ]]; then
  echo "[!] No connected outputs found"; exit 2
fi

for out in $outputs; do
  echo "[i] Processing $out"
  # прикрепляем режим к выходу, если отсутствует
  if ! xrandr --verbose | awk -v o="$out" '
    $1==o && /connected/ {seen=1}
    seen && $1=="   " && $2 ~ /^'"$W"'x'"$H"'$/ {found=1}
    END{exit found?0:1}' ; then
    echo "    + attaching mode to $out"
    xrandr --addmode "$out" "$MODE_NAME" || true
  fi

  # применяем режим
  echo "    + setting $MODE_NAME on $out"
  if ! xrandr --output "$out" --mode "$MODE_NAME"; then
    echo "    ! failed to set $MODE_NAME on $out — trying --preferred"
    xrandr --output "$out" --preferred || true
  fi
done

echo "[✓] Done."
