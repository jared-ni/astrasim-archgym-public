import os, json, yaml


def serialize_cfgs(system: dict, network: dict, system_file, network_file):
    json.dump(system, system_file, indent=4)
    yaml.dump(network, network_file)
    return


def deserialize_cfgs(system_file, network_file):
    network = yaml.load(network_file, Loader=yaml.FullLoader)
    system = json.load(system_file)
    return system, network
