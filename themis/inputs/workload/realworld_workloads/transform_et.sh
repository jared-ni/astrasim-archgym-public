#!/bin/bash

SCRIPT_DIR=$(dirname "$(realpath $0)")
CHAKRA_DIR=${SCRIPT_DIR}"/../../../../astra-sim/extern/graph_frontend/chakra/"
NUM_NPU=1024
NUM_DIM=1
NUM_PASSES=1

# if not install chakra package, uncomment following
# cd ${CHAKRA_DIR}
# python -m pip install . --user

cd ${CHAKRA_DIR}

WORKLOAD_NAME="gnmt_fp16_fused"
python -m et_converter.et_converter \
    --input_type Text \
    --input_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME}.txt\
    --output_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME} \
    --num_dims ${NUM_DIM} \
    --num_npus ${NUM_NPU} \
    --num_passes ${NUM_PASSES}

WORKLOAD_NAME="large_DLRM_fused"
python -m et_converter.et_converter \
    --input_type Text \
    --input_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME}.txt\
    --output_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME} \
    --num_dims ${NUM_DIM} \
    --num_npus ${NUM_NPU} \
    --num_passes ${NUM_PASSES}

WORKLOAD_NAME="medium_DLRM_fused"
python -m et_converter.et_converter \
    --input_type Text \
    --input_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME}.txt\
    --output_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME} \
    --num_dims ${NUM_DIM} \
    --num_npus ${NUM_NPU} \
    --num_passes ${NUM_PASSES}

WORKLOAD_NAME="microAllReduce"
python -m et_converter.et_converter \
    --input_type Text \
    --input_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME}.txt\
    --output_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME} \
    --num_dims ${NUM_DIM} \
    --num_npus ${NUM_NPU} \
    --num_passes ${NUM_PASSES}

WORKLOAD_NAME="Resnet50_DataParallel_fused"
python -m et_converter.et_converter \
    --input_type Text \
    --input_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME}.txt\
    --output_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME} \
    --num_dims ${NUM_DIM} \
    --num_npus ${NUM_NPU} \
    --num_passes ${NUM_PASSES}
