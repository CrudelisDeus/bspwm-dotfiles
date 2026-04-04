echo "=== PROCESSES ==="
pgrep -a bspwm
pgrep -a sxhkd
pgrep -a dunst
pgrep -a dbus-daemon

echo "=== DBUS ==="
echo $DBUS_SESSION_BUS_ADDRESS
