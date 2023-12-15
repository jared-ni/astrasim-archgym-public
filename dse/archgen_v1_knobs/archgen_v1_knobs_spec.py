## knob spec format:
##      set: the knob value should be any of them in the set.
##      list: the knob value should be a list, and its elements should satisfy the spec inside the list
##      tuple: the knob value should be in the defined type and range
##              the tuple always follow format of (type_fn, min, max, default_value), is no range/default_value defined, use None

## TODO: For some reason, the themis-related knobs get lost in new astrasim.
##       Will ask if there is particular reason to remove those and add these back.
SYSTEM_KNOBS = {
    "scheduling-policy": {"FIFO", "LIFO"},
    "active-chunks-per-dimension": (
        int,
        1,
        32,
        1,
    ),  # int type, range [1, 32], default value=1
    "preferred-dataset-splits": (
        int,
        16,
        1024,
        64,
    ),  # int type, range [16, 1024], default value=64
    "collective-optimization": {"localBWAware", "baseline"},
    # "intra-dimension-scheduling": {"FIFO", "SCF"},
    # "inter-dimension-scheduling": {"baseline", "themis"}
}


NETWORK_KNOBS = {}


WORKLOAD_KNOBS = {
    "dp": {1, 2, 4, 8, 16, 32, 64, 128, 256},
    "num_npus": {256},
    "weight_sharded": {0, 1},
}
