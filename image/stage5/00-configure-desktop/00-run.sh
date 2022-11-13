#!/bin/bash

###
# Disable cursor and screen timeout
###

# Add `xserver-command=X -nocursor -s 0 dpms` to /etc/lightdm/lightdm.conf after
# the Seat:* line
#
# See
# * https://raspberrypi.stackexchange.com/a/53813
# * https://www.radishlogic.com/raspberry-pi/how-to-disable-screen-sleep-in-raspberry-pi/
# (Comment by @Eric)
on_chroot << EOF
    if ! grep -E "^xserver-command" /etc/lightdm/lightdm.conf > /dev/null; then
        echo "Disable cursor and sleep"
	    sed -E -i 's/(^\[Seat.*\])/\1\nxserver-command=X -nocursor -s 0 dpms/g' /etc/lightdm/lightdm.conf
    fi
EOF

###
# Disable taskbar
###

# Comment out `@lxpanel --profile LXDE-pi` in /etc/xdg/lxsession/LXDE-pi/autostart
#
# See https://unix.stackexchange.com/a/462739
on_chroot << EOF
    if ! grep "#@lxpanel" /etc/xdg/lxsession/LXDE-pi/autostart > /dev/null; then
        echo "Disable taskbar"
        sed -E -i 's/(@lxpanel.*)/#\1/g' /etc/xdg/lxsession/LXDE-pi/autostart
    fi
EOF
