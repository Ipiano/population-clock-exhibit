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
echo "Disable cursor and sleep"
on_chroot << EOF
    XSERVER_CMD="xserver-command=X -nocursor -s 0 dpms"
	sed -E -i 's/(\[Seat.*\])/\1\n${XSERVER_CMD}/g' /etc/lightdm/lightdm.conf
EOF

###
# Disable taskbar
###

# Comment out `@lxpanel --profile LXDE-pi` in /etc/xdg/lxsession/LXDE-pi/autostart
#
# See https://unix.stackexchange.com/a/462739
echo "Disable taskbar"
on_chroot << EOF
    sed -E -i 's/(@lxpanel.*)/#\1/g' /etc/xdg/lxsession/LXDE-pi/autostart
EOF
