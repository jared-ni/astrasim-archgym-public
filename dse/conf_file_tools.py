import os, json, yaml


def workload_cfg_to_workload(workload: dict, output_et_file: str):
    SYMBOLIC_GENERATOR_PATH = os.path.join(os.path.split(os.path.abspath(__file__))[0], "../symbolic_tensor_network")
    dp = workload["dp"]
    sp = workload["sp"]
    pp = workload["pp"]
    mp = workload["num_npus"] // (dp*sp*pp)
    weight_sharded = workload["weight_sharded"]
    output_dir, output_file = os.path.split(output_et_file)
    if not "%d" in output_file:
        output_file = f"{output_file}.%d.et"
    comm_file = output_file.replace(".%d.et", ".json")
    cmd = f"PYTHONPATH={SYMBOLIC_GENERATOR_PATH} python {SYMBOLIC_GENERATOR_PATH}/main.py --output_dir {output_dir} --output_name {output_file} --dp {dp} --mp {mp} --sp {sp} --pp {pp} --weight_sharded {weight_sharded} --comm_group_file {comm_file} --chakra_schema_version v0.0.4"
    if "din" in workload:
        cmd += f" --din {workload['din']}"
    if "dout" in workload:
        cmd += f" --dout {workload['dout']}"
    if "dmodel" in workload:
        cmd += f" --dmodel {workload['dmodel']}"
    if "dff" in workload:
        cmd += f" --dff {workload['dff']}"
    if "batch" in workload:
        cmd += f" --batch {workload['batch']}"
    if "seq" in workload:
        cmd += f" --seq {workload['seq']}"
    if "head" in workload:
        cmd += f" --head {workload['head']}"
    if "num_stacks" in workload:
        cmd += f" --num_stacks {workload['num_stacks']}"
    os.system(cmd)


def serialize_cfgs(
    system=None,
    network=None,
    workload=None,
    system_file=None,
    network_file=None,
    workload_cfg_file=None,
    workload_et_file=None,
):
    if not system is None:
        assert system_file is not None
        json.dump(system, system_file, indent=4)
    if not network is None:
        assert network_file is not None
        yaml.dump(network, network_file)
    if not workload is None:
        assert workload_cfg_file is not None
        assert workload_et_file is not None
        json.dump(workload, workload_cfg_file)
        workload_cfg_to_workload(workload, workload_et_file)
    return


def deserialize_cfgs(system_file=None, network_file=None, workload_cfg_file=None):
    if not network_file is None:
        network = yaml.load(network_file, Loader=yaml.FullLoader)
    else:
        network = None
    if not system_file is None:
        system = json.load(system_file)
    else:
        system = None
    if not workload_cfg_file is None:
        workload = json.load(workload_cfg_file)
    else:
        workload = None
    return system, network, workload
