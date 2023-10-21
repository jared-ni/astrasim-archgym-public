import os, json

def serialize_cfgs(system: dict, network: dict, system_file, network_file):
    # assert these dp satisfy the constraint
    json.dump(network, network_file, indent=4)

    for key in system.keys():
        value = system[key]
        if isinstance(value, str):
            print(f"{key}: {value}", file=system_file)
        elif isinstance(value, int):
            print(f"{key}: {value}", file=system_file)
        elif isinstance(value, list):
            print(f"{key}: ", end="", file=system_file)
            for i, value_element in enumerate(value):
                print(value_element, end="", file=system_file)
                if i < len(value)-1:
                    print("_", end="", file=system_file)
            print("", file=system_file)
        else:
            # unsupported value format
            assert False
    return


def deserialize_cfgs(system_file, network_file):
    network = json.load(network_file)
    system = dict()

    lines = system_file.readlines()
    for line in lines:
        line = line.strip()
        line_split = line.split(':')
        assert len(line_split)==2
        key = line_split[0]
        value = line_split[1]
        try:
            value = int(value)
            system[key] = value
            continue    # int type finished
        except ValueError:
            pass
        if '_' in value:
            value_split = value.split('_')
            system[key] = value_split
            continue    # list[str] type finished
        system[key] = value   # str type finished
    return system, network
        