#!/bin/bash

set -o pipefail
set -o errexit

# Check docker is installed
if ! which docker > /dev/null; then
    echo "docker is not set up; please first install docker!"
    exit 1
fi

# Figure out if docker can run without root
DOCKER="docker"

if ! ${DOCKER} ps >/dev/null 2>&1; then
	DOCKER="sudo docker"
fi
if ! ${DOCKER} ps >/dev/null; then
	echo "error connecting to docker:"
	${DOCKER} ps
	exit 1
fi

# Find location of this script
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

pushd $SCRIPT_DIR

print_usage() {
    echo "build-image.sh [-u {username}] [-p {password}] [--wpa-ssid {ssid}] [--wpa-pass {password}] [--clean] [--save-work] [-h|--help]"
    echo ""
    echo "  Build a Ras-Pi image that runs the population clock project on startup by default."
    echo "  The first time this runs (or when --clean is specified), a username and password must be specified."
    echo "  Once a configuration file is generated, options can be used to append settings; but previously"
    echo "  specified options will persist."
    echo ""
    echo "  -h/--help               Show this text and exit"
    echo ""
    echo "  -u {username}           Username of the default account"
    echo "  -p {password}           Password of the default account"
    echo ""
    echo "  --wpa-ssid {ssid}       Wi-fi SSID to connect to by default"
    echo "  --wpa-pass {password}   Wi-fi password to connect to by default"
    echo ""
    echo "  --clean                 Delete old configuration and/or partial image builds"
    echo "  --save-work             Preserve the docker container that was used to build the image so it can be re-used for later builds"
}

# Load up CLI args
USER=""
PASS=""
WPA_SSID=""
WPA_PASS=""
CLEAN=0

while [ ! -z "$1" ]; do
    arg="$1"
    shift
    case "${arg}" in
        "-u")
            USER="$1"
            shift
        ;;
        "-p")
            PASS="$1"
            shift
        ;;
        "--wpa-ssid")
            WPA_SSID="$1"
            shift
        ;;
        "--wpa-pass")
            WPA_PASS="$1"
            shift
        ;;
        "--clean")
            CLEAN=1
        ;;
        "-h|--help")
            print_usage
            exit 0
        ;;
        "--save-work")
            export PRESERVE_CONTAINER=1
        ;;
        -?*)
            echo "Unknown arg: $0"
            print_usage
            exit 1
        ;;
        *)
            break
        ;;
    esac
done

if [ "$CLEAN" == "1" ]; then
    export CONTINUE=0
    rm -f ./config
    ${DOCKER} rm -v pigen_work || true
else
    export CONTINUE=1
fi

# Build the config script
if [ ! -f ./config ]; then
    if [[ -z "$USER" || -z "$PASS" ]]; then
        echo "-u or -p not specified"
        echo ""
        print_usage
        exit 1
    fi

    cp ./config.in ./config

    echo "PIGEN_DOCKER_OPTS=\"--platform linux/386\"" >> ./config
fi

if [ ! -z "$USER" ]; then
    echo "FIRST_USER_NAME=\"$USER\"" >> ./config
fi

if [ ! -z "$PASS" ]; then
    echo "FIRST_USER_PASS=\"$PASS\"" >> ./config
fi

if [ ! -z "$WPA_SSID" ]; then
    echo "WPA_ESSID=\"$WPA_SSID\"" >> ./config
fi

if [ ! -z "$WPA_PASS" ]; then
    echo "WPA_PASSWORD=\"$WPA_PASS\"" >> ./config
fi


echo "====Build Configuration===="
cat ./config
echo "==========================="

# Set up ARM emulation
EMU_PKGS="qemu binfmt-support qemu-user-static"

echo "====Setting up binfmt/qemu===="
if ! dpkg --list ${EMU_PKGS} > /dev/null; then
    sudo apt-get install --yes --quiet --no-install-recommends $EMU_PKGS
fi

${DOCKER} run --rm --privileged multiarch/qemu-user-static --reset -p yes > /dev/null

echo "====Building Pi Image===="
# Configure pi-gen
if [ ! -d ./pi-gen ]; then
    git clone --depth 1 https://github.com/RPI-Distro/pi-gen.git
fi

# Build up to stage 4, and don't produce the stage 2 or 4 images
#
# We need a basic desktop-enabled image. Could probably set up to go to stage 3,
# but stage 4 sets up a couple nice things w.r.t auto-login and VNC
touch pi-gen/stage2/SKIP_IMAGES
touch pi-gen/stage4/SKIP_IMAGES

# Insert custom stage 5 into the build
rm -rf pi-gen/stage5
cp -r ./stage5 ./pi-gen

# Insert the population clock code into new stage 5
cp -r ../app ./pi-gen/stage5/01-add-popclock/files/popclock

# Do the build
./pi-gen/build-docker.sh -c $PWD/config

popd
