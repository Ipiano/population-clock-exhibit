#!/bin/bash

set -o pipefail
set -o errexit

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

pushd $SCRIPT_DIR

print_usage() {
    echo "build-image.sh [-u {username}] [-p {password}] [--wpa-ssid {ssid}] [--wpa-pass {password}] [--clean]"
    echo ""
    echo "  Build a Ras-Pi image that runs the population clock project on startup by default."
    echo "  The first time this runs (or when --clean is specified), a username and password must be specified."
    echo "  Once a configuration file is generated, options can be used to append settings; but previously"
    echo "  specified options will persist."
    echo ""
    echo "  -u {username}           Username of the default account"
    echo "  -p {password}           Password of the default account"
    echo ""
    echo "  --wpa-ssid {ssid}       Wi-fi SSID to connect to by default"
    echo "  --wpa-pass {password}   Wi-fi password to connect to by default"
    echo ""
    echo "  --clean                 Delete old configuration and/or partial image builds"
}

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
        -?*)
            print_usage
            exit 1
        ;;
        *)
            break
        ;;
    esac
done

if [ ! -f ./config ]; then
    if [[ -z "$USER" || -z "$PASS" ]]; then
        echo "-u or -p not specified"
        echo ""
        print_usage
        exit 1
    fi

    cp ./config.in ./config

    echo "WORK_DIR=$PWD/build" >> ./config
    echo "DEPLOY_DIR=$PWD/deploy" >> ./config

    echo "PIGEN_DOCKER_OPTS=\"--mount type=bind,src=$PWD,dst=$PWD\""
fi

mkdir -p "$PWD/build"
mkdir -p "$PWD/deploy"

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

if [ ! -d ./pi-gen ]; then
    git clone --depth 1 https://github.com/RPI-Distro/pi-gen.git
fi

echo "====Building Pi Image===="
touch pi-gen/stage3/SKIP
touch pi-gen/stage4/SKIP
touch pi-gen/stage5/SKIP

touch pi-gen/stage4/SKIP_IMAGES
touch pi-gen/stage5/SKIP_IMAGES

# sudo apt-get install qemu binfmt-support qemu-user-static
# docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

CONTINUE=1 ./pi-gen/build-docker.sh -c $PWD/config

popd
