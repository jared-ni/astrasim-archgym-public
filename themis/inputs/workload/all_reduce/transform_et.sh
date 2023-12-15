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

WORKLOAD_NAME="allreduce_0.10"
python -m et_converter.et_converter \
    --input_type Text \
    --input_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME}.txt\
    --output_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME} \
    --num_dims ${NUM_DIM} \
    --num_npus ${NUM_NPU} \
    --num_passes ${NUM_PASSES}

WORKLOAD_NAME="allreduce_0.15"
python -m et_converter.et_converter \
    --input_type Text \
    --input_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME}.txt\
    --output_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME} \
    --num_dims ${NUM_DIM} \
    --num_npus ${NUM_NPU} \
    --num_passes ${NUM_PASSES}

WORKLOAD_NAME="allreduce_0.20"
python -m et_converter.et_converter \
    --input_type Text \
    --input_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME}.txt\
    --output_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME} \
    --num_dims ${NUM_DIM} \
    --num_npus ${NUM_NPU} \
    --num_passes ${NUM_PASSES}

WORKLOAD_NAME="allreduce_0.25"
python -m et_converter.et_converter \
    --input_type Text \
    --input_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME}.txt\
    --output_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME} \
    --num_dims ${NUM_DIM} \
    --num_npus ${NUM_NPU} \
    --num_passes ${NUM_PASSES}

WORKLOAD_NAME="allreduce_0.30"
python -m et_converter.et_converter \
    --input_type Text \
    --input_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME}.txt\
    --output_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME} \
    --num_dims ${NUM_DIM} \
    --num_npus ${NUM_NPU} \
    --num_passes ${NUM_PASSES}

WORKLOAD_NAME="allreduce_0.35"
python -m et_converter.et_converter \
    --input_type Text \
    --input_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME}.txt\
    --output_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME} \
    --num_dims ${NUM_DIM} \
    --num_npus ${NUM_NPU} \
    --num_passes ${NUM_PASSES}

WORKLOAD_NAME="allreduce_0.40"
python -m et_converter.et_converter \
    --input_type Text \
    --input_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME}.txt\
    --output_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME} \
    --num_dims ${NUM_DIM} \
    --num_npus ${NUM_NPU} \
    --num_passes ${NUM_PASSES}

WORKLOAD_NAME="allreduce_0.45"
python -m et_converter.et_converter \
    --input_type Text \
    --input_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME}.txt\
    --output_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME} \
    --num_dims ${NUM_DIM} \
    --num_npus ${NUM_NPU} \
    --num_passes ${NUM_PASSES}

WORKLOAD_NAME="allreduce_0.50"
python -m et_converter.et_converter \
    --input_type Text \
    --input_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME}.txt\
    --output_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME} \
    --num_dims ${NUM_DIM} \
    --num_npus ${NUM_NPU} \
    --num_passes ${NUM_PASSES}

WORKLOAD_NAME="allreduce_0.55"
python -m et_converter.et_converter \
    --input_type Text \
    --input_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME}.txt\
    --output_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME} \
    --num_dims ${NUM_DIM} \
    --num_npus ${NUM_NPU} \
    --num_passes ${NUM_PASSES}

WORKLOAD_NAME="allreduce_0.60"
python -m et_converter.et_converter \
    --input_type Text \
    --input_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME}.txt\
    --output_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME} \
    --num_dims ${NUM_DIM} \
    --num_npus ${NUM_NPU} \
    --num_passes ${NUM_PASSES}

WORKLOAD_NAME="allreduce_0.65"
python -m et_converter.et_converter \
    --input_type Text \
    --input_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME}.txt\
    --output_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME} \
    --num_dims ${NUM_DIM} \
    --num_npus ${NUM_NPU} \
    --num_passes ${NUM_PASSES}

WORKLOAD_NAME="allreduce_0.70"
python -m et_converter.et_converter \
    --input_type Text \
    --input_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME}.txt\
    --output_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME} \
    --num_dims ${NUM_DIM} \
    --num_npus ${NUM_NPU} \
    --num_passes ${NUM_PASSES}

WORKLOAD_NAME="allreduce_0.75"
python -m et_converter.et_converter \
    --input_type Text \
    --input_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME}.txt\
    --output_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME} \
    --num_dims ${NUM_DIM} \
    --num_npus ${NUM_NPU} \
    --num_passes ${NUM_PASSES}

WORKLOAD_NAME="allreduce_0.80"
python -m et_converter.et_converter \
    --input_type Text \
    --input_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME}.txt\
    --output_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME} \
    --num_dims ${NUM_DIM} \
    --num_npus ${NUM_NPU} \
    --num_passes ${NUM_PASSES}

WORKLOAD_NAME="allreduce_0.85"
python -m et_converter.et_converter \
    --input_type Text \
    --input_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME}.txt\
    --output_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME} \
    --num_dims ${NUM_DIM} \
    --num_npus ${NUM_NPU} \
    --num_passes ${NUM_PASSES}

WORKLOAD_NAME="allreduce_0.90"
python -m et_converter.et_converter \
    --input_type Text \
    --input_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME}.txt\
    --output_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME} \
    --num_dims ${NUM_DIM} \
    --num_npus ${NUM_NPU} \
    --num_passes ${NUM_PASSES}

WORKLOAD_NAME="allreduce_0.95"
python -m et_converter.et_converter \
    --input_type Text \
    --input_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME}.txt\
    --output_filename  ${SCRIPT_DIR}/${WORKLOAD_NAME} \
    --num_dims ${NUM_DIM} \
    --num_npus ${NUM_NPU} \
    --num_passes ${NUM_PASSES}
