import psutil
import subprocess


def vm_detect():
    command = 'sudo systemd-detect-virt'
    process = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE).wait()

    if process == 0:
        return True

    else:
        return False


def virtual_memory():
    result = psutil.virtual_memory()
    dict_result = dict(result._asdict())

    return dict_result


def swap_memory():
    result = psutil.swap_memory()
    dict_result = dict(result._asdict())

    return dict_result


def cpu_times():
    dict_result = {}
    result = psutil.cpu_times(percpu=True)

    for core_number, core_times in enumerate(result):
        dict_result[f'Core {core_number}'] = dict(core_times._asdict())

    return dict_result


def cpu_percent():
    dict_result = {}
    result = psutil.cpu_percent(interval=None, percpu=True)

    for core_number, core_percent in enumerate(result):
        dict_result[f'Core {core_number}'] = core_percent

    return dict_result


def cpu_count():
    phys_cores = psutil.cpu_count(logical=False)
    logic_cores = psutil.cpu_count(logical=True)
    dict_result = {'physical': phys_cores, 'logical': logic_cores}

    return dict_result


def cpu_stats():
    result = psutil.cpu_stats()
    dict_result = dict(result._asdict())

    return dict_result


def cpu_freq():
    dict_result = {}
    result = psutil.cpu_freq(percpu=True)

    for core_number, core_freq in enumerate(result):
        dict_result[f'Core {core_number}'] = dict(core_freq._asdict())

    return dict_result


def disks_info():
    dict_result = {}
    disks = psutil.disk_partitions(all=False)

    for disk_number, disk in enumerate(disks):
        dict_result[f'Disk {disk_number}'] = dict(disk._asdict())

        if 'rw' in disk.opts:
            disk_usage = psutil.disk_usage(disk.mountpoint)
            dict_result[f'Disk {disk_number}']['total'] = disk_usage.total
            dict_result[f'Disk {disk_number}']['used'] = disk_usage.used
            dict_result[f'Disk {disk_number}']['free'] = disk_usage.free
            dict_result[f'Disk {disk_number}']['percent'] = disk_usage.percent

        else:
            dict_result[f'Disk {disk_number}']['total'] = 0
            dict_result[f'Disk {disk_number}']['used'] = 0
            dict_result[f'Disk {disk_number}']['free'] = 0
            dict_result[f'Disk {disk_number}']['percent'] = 0

    return dict_result


def disks_io():
    dict_result = {}
    partitions_io = psutil.disk_io_counters(perdisk=True, nowrap=True)

    for disk in partitions_io:
        dict_result[disk] = dict(partitions_io[disk]._asdict())

    return dict_result


def net_io_counters():
    result = psutil.net_io_counters(pernic=True, nowrap=True)
    dict_result = {}
    for interface in result:
        dict_result[interface] = {}
        dict_result[interface]['bytes_sent'] = result[interface].bytes_sent
        dict_result[interface]['bytes_recv'] = result[interface].bytes_recv
        dict_result[interface]['packets_sent'] = result[interface].packets_sent
        dict_result[interface]['packets_recv'] = result[interface].packets_recv
        dict_result[interface]['errin'] = result[interface].errin
        dict_result[interface]['errout'] = result[interface].errout
        dict_result[interface]['dropin'] = result[interface].dropin
        dict_result[interface]['dropout'] = result[interface].dropout

    return dict_result


def processes_info():
    result_dict = {}

    for process in psutil.process_iter():
        try:
            process_data = {}
            with process.oneshot():
                pid = process.pid
                process_data['name'] = process.name()
                process_data['username'] = process.username()
                process_data['status'] = process.status()
                process_data['memory_info'] = dict(process.memory_info()._asdict())
                process_data['cpu_times'] = dict(process.cpu_times()._asdict())
                process_data['cpu_percent'] = process.cpu_percent(interval=0)
                process_data['connections'] = {}

                connections = process.connections(kind='all')
                for connection_number, connection in enumerate(connections):
                    process_data['connections'][connection_number] = {}
                    process_data['connections'][connection_number]['fd'] = connection.fd
                    process_data['connections'][connection_number]['family'] = connection.family
                    process_data['connections'][connection_number]['type'] = connection.type
                    process_data['connections'][connection_number]['laddr'] = ''
                    process_data['connections'][connection_number]['raddr'] = ''
                    process_data['connections'][connection_number]['status'] = connection.status

                    if connection.laddr:
                        process_data['connections'][connection_number]['laddr'] = connection.laddr

                    if connection.raddr:
                        process_data['connections'][connection_number]['raddr'] = connection.raddr

            result_dict[pid] = process_data

        except psutil.NoSuchProcess:
            pass

        except psutil.AccessDenied:
            pass

    return result_dict


if __name__ == '__main__':
    all_data = {}
    all_data['vm_detect'] = vm_detect()
    all_data['virtual_memory'] = virtual_memory()
    all_data['swap_memory'] = swap_memory()
    all_data['cpu_times'] = cpu_times()
    all_data['cpu_percent'] = cpu_percent()
    all_data['cpu_count'] = cpu_count()
    all_data['cpu_stats'] = cpu_stats()
    all_data['cpu_freq'] = cpu_freq()
    all_data['disks_info'] = disks_info()
    all_data['disks_io'] = disks_io()
    all_data['net_io_counters'] = net_io_counters()
    all_data['processes_info'] = processes_info()

    import json
    with open('all.json', 'w') as file:
        json.dump(all_data, file, indent=6)
