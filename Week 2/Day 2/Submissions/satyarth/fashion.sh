#!/bin/bash

SCRIPT_PATH="fashion.py"


FREQUENCY_THRESH="${1:-3}"
python3 $SCRIPT_PATH --thresh $FREQUENCY_THRESH 