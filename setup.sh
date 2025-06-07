#!/usr/bin/bash

FLAG="${1}"

function err() {
    echo "Error: corrupted at ${1} requirements.txt";
    echo "Check that pip3 is installed at your machine and try again";
    exit 1;
}

function setup() {
    if ! [ -f requirements.txt ]; then
        if ! pip3 freeze > requirements.txt; then
            err "creation";
        fi
    fi
    if [ "${FLAG}" == "--break-system-packages" ]; then
        if ! pip3 install -r requirements.txt --break-system-packages; then
            err "installation";
        fi
    else
        if ! pip3 install -r requirements.txt; then
            err "installation";
        fi
    fi
}

echo "Setup Filelink..."
setup;

# shellcheck disable=SC1091
source /etc/os-release

if ! python3 -c "import flask" > /dev/null 2>&1 && [ "${ID}" == "ubuntu" ]; then
    apt update;
    apt install python3 pip3 python3-flask -y;
    setup;
fi

echo "Installation was successful"
exit 0