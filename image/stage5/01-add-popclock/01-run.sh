#!/bin/bash

# Copy population clock files over
cp -r files/popclock "${ROOTFS_DIR}/opt/"
chown -R 1000:1000 "${ROOTFS_DIR}/opt/"

# Add startup script to run the population clock
#
# See https://www.makeuseof.com/how-to-run-a-raspberry-pi-program-script-at-startup/
install -m 755 files/popclock.desktop "${ROOTFS_DIR}/etc/xdg/autostart/"

# Install everything except Pyside2 (and requirements) - Pyside2
# is installed with apt during 00-packages
on_chroot << EOF
	cat /opt/popclock/requirements.txt | sed -E 's/(PySide2|shiboken2).*//g' | xargs python3 -m pip install
EOF
