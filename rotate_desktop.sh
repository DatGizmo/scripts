#!/bin/bash
#
# rotate_desktop.sh
#
# Rotates modern Linux desktop screen and input devices to match. Handy for
# convertible notebooks. Call this script from panel launchers, keyboard
# shortcuts, or touch gesture bindings (xSwipe, touchegg, etc.).
#
# Using transformation matrix bits taken from:
#   https://wiki.ubuntu.com/X/InputCoordinateTransformation
#

# Configure these to match your hardware (names taken from `xinput` output).
TOUCHSCREEN='DATA MODUL easyTOUCH'

if [ -z "$1" ]; then
  echo "Missing orientation."
  echo "Usage: $0 [normal|inverted|left|right] [revert_seconds]"
  echo
  exit 1
fi

function do_rotate
{
  #xrandr --output $1 --rotate $2
  xrandr -o $1

  TRANSFORM='Coordinate Transformation Matrix'

  case "$1" in
    normal)
      [ ! -z "$TOUCHSCREEN" ] && xinput set-prop "$TOUCHSCREEN" "$TRANSFORM" 1 0 0 0 1 0 0 0 1
      ;;
    inverted)
      [ ! -z "$TOUCHSCREEN" ] && xinput set-prop "$TOUCHSCREEN" "$TRANSFORM" -1 0 1 0 -1 1 0 0 1
      ;;
    left)
      [ ! -z "$TOUCHSCREEN" ] && xinput set-prop "$TOUCHSCREEN" "$TRANSFORM" 0 -1 1 1 0 0 0 0 1
      ;;
    right)
      [ ! -z "$TOUCHSCREEN" ] && xinput set-prop "$TOUCHSCREEN" "$TRANSFORM" 0 1 0 -1 0 1 0 0 1
      ;;
  esac
}

#XDISPLAY=`xrandr --current | grep primary | sed -e 's/ .*//g'`
XROT=`xrandr --current --verbose | grep primary | egrep -o ' (normal|left|inverted|right) '`

#do_rotate $XDISPLAY $1
do_rotate $1

if [ ! -z "$2" ]; then
  sleep $2
  do_rotate $XROT
  exit 0
fi

