#!/usr/bin/env bash

set -e

__usage="
Usage: $0 [-v]

  -v: if set, verbose mode is activated (more output from the script generally)

Example: ./run.sh -v
"

usage() { echo "$__usage" >&2; }

# Get all the required options and set the necessary variables
VERBOSE=false
while getopts "v" opt
do
    case ${opt} in
        v) VERBOSE=true;;
        *) usage; exit 1 ;;
    esac
done

if [ "${VERBOSE}" = true ]; then
    set -x
    VERBOSE_ARG="--verbose"
fi

python main.py ${VERBOSE_ARG}