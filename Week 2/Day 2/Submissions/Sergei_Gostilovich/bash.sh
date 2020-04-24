#!/bin/bash

set -x
set -e

SPLIT_SCRIPT= ./main.py

python3 ${SPLIT_SCRIPT}