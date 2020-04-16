#!/bin/bash

set -x

mkdir -p /home/artonson/tmp/voronoi_output /home/artonson/tmp/voronoi_input

python3 ../contrib/py/hdf5_utils/split_hdf5.py --label points --output_dir /home/artonson/tmp/voronoi_input /home/artonson/datasets/eccv_test/points/high_0.02/val/val_1024_0.hdf5

../contrib/cxx/voronoi_1 -f /home/artonson/tmp/voronoi_input/val_1024_0_points_0.xyz -R 0.2 -r 0.1 -t 0.16 -o /home/artonson/tmp/voronoi_output

python3 ../contrib/py/hdf5_utils/merge_hdf5.py -i /home/artonson/tmp/voronoi_output -o /home/artonson/tmp/voronoi_output/test.hdf5 --input_format txt

