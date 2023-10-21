## knob spec format:
##      set: the knob value should be any of them in the set.
##      list: the knob value should be a list, and its elements should satisfy the spec inside the list
##      tuple: the knob value should be in the defined type and range
##              the tuple always follow format of (type_fn, min, max, default_value), is no range/default_value defined, use None

SYSTEM_KNOBS = {
    "scheduling-policy": {"FIFO", "LIFO"},
    "collective-optimization": {"localBWAware", "baseline"},
    "intra-dimension-scheduling": {"FIFO", "SCF"},
    "inter-dimension-scheduling": {"baseline", "themis"}
}


NETWORK_KNOBS = {

}
