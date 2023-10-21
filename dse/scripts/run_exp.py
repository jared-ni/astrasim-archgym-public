import os, sys, multiprocessing


results_dir = '../results/archgen_v1_1'
astrasim_bin = '../../astra-sim/build/astra_analytical/build/AnalyticalAstra/bin/AnalyticalAstra'
workload_dir = '../workload/realworld_workloads'
system_dir = '../archgen_v1_knobs/generated/1/system'
network_dir = '../archgen_v1_knobs/generated/1/network'


def run_task(workload, system, network, run_name_prefix=''):
    config_name = os.path.split(network)[-1][:-5]
    workload_name = os.path.split(workload)[-1][:-4]
    run_dir = os.path.join(results_dir, config_name, workload_name)+"/"
    log_path = os.path.join(run_dir, 'std.out')
    os.makedirs(run_dir, exist_ok=True)
    run_name = f"{run_name_prefix}{config_name}_{workload_name}"
    cmd = f"{astrasim_bin} --workload-configuration={workload} --system-configuration={system} --network-configuration={network} --path={run_dir} --run-name={run_name} > {log_path} 2>&1"
    print(cmd)
    os.system(cmd)
    return True


def get_experiment_space(workload_dir_, system_dir_, network_dir_):
    workloads = os.listdir(workload_dir_)
    systems = os.listdir(system_dir_)
    networks = os.listdir(network_dir_)
    rets = list()
    for workload in workloads:
        if not workload.endswith('.txt'):
            continue

        for network in networks:
            if not network.endswith('.json'):
                continue
            network_name = network[:-5]

            for system in systems:
                if not system.startswith(network_name):
                    continue
                if not system.endswith('.txt'):
                    continue
                print(workload_dir_, system_dir_, network_dir_)
                workload_fullpath = os.path.join(workload_dir_, workload)
                system_fullpath = os.path.join(system_dir_, system)
                network_fullpath = os.path.join(network_dir_, network)
                rets.append((workload_fullpath, system_fullpath, network_fullpath))
    return rets


def run_experiments(num_workers=-1):
    if num_workers == -1:
        num_workers = int(multiprocessing.cpu_count()*0.5)
    pool = multiprocessing.Pool(num_workers)
    experiment_space = get_experiment_space(workload_dir, system_dir, network_dir)
    rets = list()
    for experiment_point in experiment_space:
        pool.apply_async(run_task, experiment_point)
    pool.close()
    pool.join()
    for ret in rets:
        ret.get()
    return


if __name__ == '__main__':
    run_experiments()

