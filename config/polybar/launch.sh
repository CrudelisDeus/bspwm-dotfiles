#!/bin/sh
killall -q polybar

echo "---" | tee -a /tmp/polybar.log
polybar example >> /tmp/polybar.log 2>&1 &
