#!/bin/bash
set -x

ML_PKG="beautifulsoup4 requests pandas numpy matplotlib.pyplot argparse sklearn"

for pkg in $ML_PKG; do
    if pip -q list installed "$ML_PKG" > /dev/null 2>&1; then
        echo -e "$pkg is already installed"
    else
        pip install $ML_PLG -y
        echo "Successfully installed $pkg"
    fi
done

python3 ./task.py  --input_dir ./ --output_dir ./

