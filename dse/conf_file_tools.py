import os, json, yaml, copy
import graphviz
from chakra.third_party.utils.protolib import (
    openFileRd as open_file_rd,
    decodeMessage as decode_message,
    encodeMessage as encode_message
)
from chakra.et_def.et_def_pb2 import (
    GlobalMetadata,
    Node,
)


def workload_cfg_to_workload(workload: dict, output_et_file: str):
    if "prefilling" in workload and "decoding" in workload:
        assemble_inference_workload(workload, output_et_file)
        return
    elif "prefilling" in workload:
        workload["seq"] = workload['prefilling']
        workload['templates'] = 'prefilling'
        del workload['prefilling']
    elif "decoding" in workload:
        workload["seq"] = workload['decoding']
        workload['templates'] = 'decoding'
        del workload['decoding']
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
    cmd = f"PYTHONPATH={SYMBOLIC_GENERATOR_PATH} python {SYMBOLIC_GENERATOR_PATH}/main_adv.py --output_dir {output_dir} --output_name {output_file} --dp {dp} --mp {mp} --sp {sp} --pp {pp} --weight_sharded {weight_sharded} --comm_group_file {comm_file} --chakra_schema_version v0.0.4 --generate_io_info 1"
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
    if "templates" in workload:
        cmd += f" --templates {workload['templates']}"
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
             

def assemble_inference_workload(workload: dict, output_et_file: str):
    # not pass simulation
    raise NotImplementedError()
    workload = copy.deepcopy(workload)
    prefilling = workload['prefilling']
    decoding = workload['decoding']
    del workload['prefilling']
    del workload['decoding']
    output_dir, final_output_file = os.path.split(output_et_file)
    
    # generating prefilling
    prefilling_output_file = f"prefilling_{final_output_file}"
    workload['seq'] = prefilling
    workload['templates'] = 'prefilling'
    workload_cfg_to_workload(workload, os.path.join(output_dir, prefilling_output_file))
    
    # generating decoding
    decoding_output_files = list()
    workload['templates'] = 'decoding'
    period_cnt = 0
    for i in range(prefilling, prefilling+decoding):
        i += 1
        period_cnt += 1
        if period_cnt % (decoding//2) == 0 or i == prefilling+1:
            pass
        else:
            decoding_output_files.append(decoding_output_file)
            continue
        decoding_output_file = f"decoding_{i}_{final_output_file}"
        workload['seq'] = i
        decoding_output_files.append(decoding_output_file)
        workload_cfg_to_workload(workload, os.path.join(output_dir, decoding_output_file))

    def _load_chakra_et(_et_path):
        global_metadata = GlobalMetadata()
        node = Node()
        nodes = list()
        with open_file_rd(_et_path) as et:
            decode_message(et, global_metadata)
            while decode_message(et, node):
                nodes.append(copy.deepcopy(node))
        return copy.deepcopy(global_metadata), nodes
        
    files = os.listdir(output_dir)
    assert prefilling_output_file.endswith(".%d.et")
    prefilling_output_file_ = prefilling_output_file[:-6]
    num_ranks = -1
    for file in files:
        if prefilling_output_file_ in file:
            rank = int(file.split(".")[-2])
            num_ranks = max(num_ranks, rank)
    num_ranks += 1
    
    all_nodes_diff_ranks = dict()
    for rank in range(num_ranks):
        all_nodes = dict()
        
        global_metadata, nodes = _load_chakra_et(os.path.join(output_dir, prefilling_output_file % (rank,)))
        offset = len(all_nodes)
        for node in nodes:
            node.id = node.id+offset
            node.name = f"prefilling_{node.name}"
            data_deps = set(node.data_deps)
            ctrl_deps = set(node.ctrl_deps)
            updated_data_deps = set()
            updated_ctrl_deps = set()
            for data_dep in data_deps:
                updated_data_deps.add(data_dep+offset)
            for ctrl_dep in ctrl_deps:
                updated_ctrl_deps.add(ctrl_dep+offset)
            data_deps = updated_data_deps
            ctrl_deps = updated_ctrl_deps
            node.data_deps[:] = list(data_deps)
            node.ctrl_deps[:] = list(ctrl_deps)
            all_nodes[node.name] = node
        # os.system(f"rm {os.path.join(output_dir, prefilling_output_file % (rank,))}")
        
        for i, decoding_output_file in enumerate(decoding_output_files):
            global_metadata, nodes = _load_chakra_et(os.path.join(output_dir, decoding_output_file % (rank,)))
            offset = len(all_nodes)
            # offset = i*1000000
            for node in nodes:
                node.id = node.id+offset
                node.name = f"decoding_{i}_{node.name}"
                data_deps = set(node.data_deps)
                ctrl_deps = set(node.ctrl_deps)
                updated_data_deps = set()
                updated_ctrl_deps = set()
                for data_dep in data_deps:
                    updated_data_deps.add(data_dep+offset)
                for ctrl_dep in ctrl_deps:
                    updated_ctrl_deps.add(ctrl_dep+offset)
                data_deps = updated_data_deps
                ctrl_deps = updated_ctrl_deps
                if "mha_k@0_COMP" in node.name or "mha_v@0_COMP" in node.name:
                    last_kv = copy.deepcopy(node.name)
                    if i == 0:
                        last_kv = last_kv.replace(f"decoding_{i}_", "prefilling_")    
                    else:
                        last_kv = last_kv.replace(f"decoding_{i}_", f"decoding_{i-1}_")
                    print(last_kv, node.name)
                    last_kv = all_nodes[last_kv].id
                    data_deps.add(last_kv)
                node.data_deps[:] = list(data_deps)
                node.ctrl_deps[:] = list(ctrl_deps)
                all_nodes[node.name] = node
        for i, decoding_output_file in enumerate(set(decoding_output_files)):
            # os.system(f"rm {os.path.join(output_dir, decoding_output_file % (rank,))}")
            pass
        
        all_nodes_diff_ranks[rank] = (global_metadata, all_nodes)
        
    
    
    for rank in range(num_ranks):
        global_metadata, all_nodes = all_nodes_diff_ranks[rank]
        with open(os.path.join(output_dir, final_output_file % (rank,)), "wb") as f:
            encode_message(f, global_metadata)
            for node in all_nodes.values():
                encode_message(f, node)
        os.system(f"cp {os.path.join(output_dir, prefilling_output_file.replace(".%d.et", ".json"))} {os.path.join(output_dir, final_output_file.replace(".%d.et", ".json"))}")

