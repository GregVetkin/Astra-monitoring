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


def cpu_times(eachcore=True):
    result = psutil.cpu_times(percpu=eachcore)

    if eachcore:
        dict_result = {}
        for core_number, core_times in enumerate(result):
            dict_result[f'Core {core_number}'] = dict(core_times._asdict())

    else:
        dict_result = dict(result._asdict())

    return dict_result


def cpu_percent(eachcore=True, interval=None):
    result = psutil.cpu_percent(interval=interval, percpu=eachcore)

    if eachcore:
        dict_result = {}
        for core_number, core_percent in enumerate(result):
            dict_result[f'Core {core_number}'] = core_percent
        return dict_result

    else:
        return result


def cpu_count():
    phys_cores = psutil.cpu_count(logical=False)
    logic_cores = psutil.cpu_count(logical=True)
    dict_result = {'physical': phys_cores, 'logical': logic_cores}

    return dict_result


def cpu_stats():
    result = psutil.cpu_stats()
    dict_result = dict(result._asdict())

    return dict_result


def cpu_freq(eachcore=True):
    result = psutil.cpu_freq(percpu=eachcore)

    if eachcore:
        dict_result = {}

        for core_number, core_freq in enumerate(result):
            dict_result[f'Core {core_number}'] = dict(core_freq._asdict())

    else:
        dict_result = dict(result._asdict())

    return dict_result


def disks_info():
    dict_result = {}
    disks = psutil.disk_partitions(all=False)
    disks_io_counters = psutil.disk_io_counters(perdisk=True, nowrap=True)

    for disk_io in disks_io_counters:
        if 'sda' in disk_io:
            print(disks_io_counters[disk_io])

    for disk_number, disk in enumerate(disks):
        dict_result[f'Disk {disk_number}'] = {}
        dict_result[f'Disk {disk_number}']['device'] = disk.device
        dict_result[f'Disk {disk_number}']['mountpoint'] = disk.mountpoint
        dict_result[f'Disk {disk_number}']['fstype'] = disk.fstype
        dict_result[f'Disk {disk_number}']['opts'] = disk.opts
        dict_result[f'Disk {disk_number}']['maxfile'] = disk.maxfile
        dict_result[f'Disk {disk_number}']['maxpath'] = disk.maxpath

        if 'rw' in disk.opts:
            disk_usage = psutil.disk_usage(disk.mountpoint)
            dict_result[f'Disk {disk_number}']['total'] = disk_usage.total
            dict_result[f'Disk {disk_number}']['used'] = disk_usage.used
            dict_result[f'Disk {disk_number}']['free'] = disk_usage.free
            dict_result[f'Disk {disk_number}']['percent'] = disk_usage.percent

        else:
            dict_result[f'Disk {disk_number}']['total'] = None
            dict_result[f'Disk {disk_number}']['used'] = None
            dict_result[f'Disk {disk_number}']['free'] = None
            dict_result[f'Disk {disk_number}']['percent'] = None

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
    #print(vm_detect())
    #print(virtual_memory())
    #print(swap_memory())
    #print(cpu_times())
    #print(cpu_percent())
    #print(cpu_count())
    #print(cpu_stats())
    #print(cpu_freq())
    #print(disks_info())
    #print(net_io_counters())
    proc = processes_info()
    import json
    with open('procs.json', 'w') as file:
        json.dump(proc, file, indent=6)
    #print(processes_info())