import random, sys
sys.path.append("..")
from archgen_v1_knobs_spec import SYSTEM_KNOBS, NETWORK_KNOBS
from conf_file_tools import deserialize_cfgs

def random_cfg_generator(template_name, template_root):
    def _random_sample_set(set_):
        return random.choice(list(set_))
    
    def _sample_value(value_spec, list_sample_count=-1):
        if isinstance(value_spec, set):
            value = _random_sample_set(value_spec)
        elif isinstance(value_spec, tuple):
            assert isinstance(value_spec[0], type)
            if value_spec[0] == int:
                value = random.randint(value_spec[1], value_spec[2])
            elif value_spec[0] == float:
                value = random.random()
                value = value_spec[1] + (value_spec[2]-value_spec[1])*value
            else:
                # unsupported type
                assert False
        elif isinstance(value_spec, list):
            assert list_sample_count > 0
            value = list()
            for _ in range(list_sample_count):
                value.append(_sample_value(value_spec[0]))
        else:
            # unsupported value spec
            assert False
        return value
    
    system_f = open(os.path.join(template_root, 'system', template_name+".txt"), 'r')
    network_f = open(os.path.join(template_root, 'network', template_name+".json"), 'r')
    
    system, network = deserialize_cfgs(system_f, network_f)
    
    system_f.close()
    network_f.close()
    
    dimensions_count = network['dimensions-count']

    # system
    remain_system_keys = set(SYSTEM_KNOBS.keys())
    for key in system.keys():   # remove already have keys in template
        if key in remain_system_keys:
            remain_system_keys.remove(key)

    while len(remain_system_keys) > 0:
        keys_to_remove = set()
        for key in remain_system_keys:
            value_spec = SYSTEM_KNOBS[key]
            if isinstance(value_spec, list):
                # for list knobs, the number is decided by the network dimension
                # if the dimension is not decided, just skip
                if dimensions_count <= 0:
                    continue
                value = _sample_value(value_spec, list_sample_count=dimensions_count)
            else:
                value = _sample_value(value_spec)
            keys_to_remove.add(key)
            system[key] = value
        for key in keys_to_remove:
            remain_system_keys.remove(key)
        keys_to_remove.clear()

    return network, system


if __name__ == '__main__':
    import os
    from conf_file_tools import serialize_cfgs
    import shutil
    num_configs_each_template = 10
    template_dir = './templates'
    generated_dir = './generated/1'
    
    system_template_filenames = os.listdir(os.path.join(template_dir, "system"))
    template_names = list()
    for system_filename in system_template_filenames:
        if not system_filename.endswith('.txt'):
            continue
        template_name = system_filename[:-4]
        assert os.path.isfile(os.path.join(template_dir, "network", template_name+".json"))
        template_names.append(template_name)
    
    os.makedirs(os.path.join(generated_dir, 'system'), exist_ok=True)
    os.makedirs(os.path.join(generated_dir, 'network'), exist_ok=True)

    for template_name in template_names:
        # shutils.copy(os.path.join(template_dir, 'network', template_name+".json"), os.path.join(generated_dir, 'network', template_name+".json"))
        for i in range(num_configs_each_template):
            network, system = random_cfg_generator(template_name, template_dir)
            system_f = open(os.path.join(generated_dir, 'system', f"{template_name}_{i}.txt"), 'w')
            network_f = open(os.path.join(generated_dir, 'network', f"{template_name}_{i}.json"), 'w')

            serialize_cfgs(system, network, system_f, network_f)
            system_f.close()
            network_f.close()
