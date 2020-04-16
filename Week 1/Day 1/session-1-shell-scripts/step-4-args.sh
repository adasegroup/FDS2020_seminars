#!/bin/bash

set -x
set -e

usage() { echo "Usage: ${0} -i input_file -o output_file [-R offset_radius] [-r conv_radius] [-t threshold]" >&2; }

V_OFFSET_RADIUS=0.2
V_CONV_RADIUS=0.1
V_THRESHOLD=0.16
while getopts "i:o:R:r:t:" opt
do
    case ${opt} in 
        i) INPUT_HDF5_FILENAME=${OPTARG} ;;
        o) OUTPUT_HDF5_FILENAME=${OPTARG} ;;
        R) V_OFFSET_RADIUS=${OPTARG} ;;
        r) V_CONV_RADIUS=${OPTARG} ;;
        t) V_THRESHOLD=${OPTARG} ;;
        *) usage; exit 1 ;;
    esac
done

if [[ ! -f ${INPUT_HDF5_FILENAME} ]]
then 
    echo "input_file not set or empty"
    usage; exit 1
fi
# Shorthand:
# [[ -f ${INPUT_HDF5_FILENAME} ]] || (echo "input_file not set or empty" && usage && exit 1)

if [[ -z ${OUTPUT_HDF5_FILENAME} ]]
then
    echo "output_file not set or empty"
    usage; exit 1
fi


# INPUT_HDF5_FILENAME=/home/artonson/datasets/eccv_test/points/high_0.02/val/val_1024_0.hdf5
# OUTPUT_HDF5_BASENAME=$( basename ${INPUT_HDF5_FILENAME%.*} )
INPUT_XYZ_DIR=/home/artonson/tmp/voronoi_input

PY_SRC_DIR=../contrib/py/hdf5_utils
SPLIT_SCRIPT=${PY_SRC_DIR}/split_hdf5.py

python3 ${SPLIT_SCRIPT} \
    --label points \
    --output_dir ${INPUT_XYZ_DIR} \
    ${INPUT_HDF5_FILENAME}

OUTPUT_XYZ_DIR=/home/artonson/tmp/voronoi_output

BIN_DIR=../contrib/cxx
BINARY=${BIN_DIR}/voronoi_1

mkdir -p ${OUTPUT_XYZ_DIR}


#XYZ_FILES=$( find ${INPUT_XYZ_DIR} -type f -name "*.xyz" )

# Option 1: a simple for loop
# For the for loop to even start, the find must run to completion
#for XYZ_FILE in ${XYZ_FILES}
#do
#    ${BINARY} \
#        -f ${XYZ_FILE} \
#        -R ${V_OFFSET_RADIUS} \
#        -r ${V_CONV_RADIUS} \
#        -t ${V_THRESHOLD} \
#        -o ${OUTPUT_XYZ_DIR}
#done

# Option 2: pass filenames through pipe
#find ${INPUT_XYZ_DIR} -type f -name "*.xyz" -print0 | while IFS=' ' read -d $'\0' XYZ_FILE
#do
#   ${BINARY} \
#       -f ${XYZ_FILE} \
#       -R ${V_OFFSET_RADIUS} \
#       -r ${V_CONV_RADIUS} \
#       -t ${V_THRESHOLD} \
#       -o ${OUTPUT_XYZ_DIR}
#done

# Option 3: -exec invoked by find
# Syntax: -exec command {} \;
find ${INPUT_XYZ_DIR} -type f -name "*.xyz" -print0 \
    -exec ${BINARY} \
        -f {} \
        -R ${V_OFFSET_RADIUS} \
        -r ${V_CONV_RADIUS} \
        -t ${V_THRESHOLD} \
        -o ${OUTPUT_XYZ_DIR} \
    \;

# Tons of ways of looping thru files here 
# https://stackoverflow.com/questions/9612090/how-to-loop-through-file-names-returned-by-find


MERGE_SCRIPT=${PY_SRC_DIR}/merge_hdf5.py
# OUTPUT_HDF5_FILENAME=${OUTPUT_XYZ_DIR}/${OUTPUT_HDF5_BASENAME}

python3 ${MERGE_SCRIPT} \
    -i ${OUTPUT_XYZ_DIR} \
    -o ${OUTPUT_HDF5_FILENAME} \
    --input_format txt

