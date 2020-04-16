#!/bin/bash

set -x
set -e

INPUT_HDF5_FILENAME=/home/artonson/datasets/eccv_test/points/high_0.02/val/val_1024_0.hdf5
INPUT_XYZ_DIR=/home/artonson/tmp/voronoi_input

PY_SRC_DIR=../contrib/py/hdf5_utils
SPLIT_SCRIPT=${PY_SRC_DIR}/split_hdf5.py

python3 ${SPLIT_SCRIPT} \
    --label points \
    --output_dir ${INPUT_XYZ_DIR} \
    ${INPUT_HDF5_FILENAME}

V_OFFSET_RADIUS=0.2
V_CONV_RADIUS=0.1
V_THRESHOLD=0.16
OUTPUT_XYZ_DIR=/home/artonson/tmp/voronoi_output

BIN_DIR=../contrib/cxx
BINARY=${BIN_DIR}/voronoi_1

mkdir -p ${OUTPUT_XYZ_DIR}

${BINARY} \
    -f ${INPUT_XYZ_DIR}/val_1024_0_points_0.xyz \
    -R ${V_OFFSET_RADIUS} \
    -r ${V_CONV_RADIUS} \
    -t ${V_THRESHOLD} \
    -o ${OUTPUT_XYZ_DIR}

MERGE_SCRIPT=${PY_SRC_DIR}/merge_hdf5.py

python3 ${MERGE_SCRIPT} \
    -i ${OUTPUT_XYZ_DIR} \
    -o ${OUTPUT_XYZ_DIR}/test.hdf5 \
    --input_format txt

