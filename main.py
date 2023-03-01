import psutil
import subprocess


class Virtual:

    @staticmethod
    def vm_detect():
        command = 'sudo systemd-detect-virt'
        process = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE).wait()
        if process == 0:
            return True
        else:
            return False


class Memory:

    @staticmethod
    def virtual_memory():
        return dict(psutil.virtual_memory()._asdict())

    @staticmethod
    def swap_memory():
        return dict(psutil.swap_memory()._asdict())


class Processor:

    @staticmethod
    def cpu_times():
        dict_result = {}
        result = psutil.cpu_times(percpu=True)
        for core_number, core_times in enumerate(result):
            dict_result[f'Core {core_number}'] = dict(core_times._asdict())
        return dict_result

    @staticmethod
    def cpu_percent():
        dict_result = {}
        result = psutil.cpu_percent(interval=None, percpu=True)
        for core_number, core_percent in enumerate(result):
            dict_result[f'Core {core_number}'] = core_percent
        return dict_result

    @staticmethod
    def cpu_count():
        phys_cores = psutil.cpu_count(logical=False)
        logic_cores = psutil.cpu_count(logical=True)
        dict_result = {'physical': phys_cores, 'logical': logic_cores}
        return dict_result

    @staticmethod
    def cpu_stats():
        return dict(psutil.cpu_stats()._asdict())

    @staticmethod
    def cpu_freq():
        dict_result = {}
        result = psutil.cpu_freq(percpu=True)
        for core_number, core_freq in enumerate(result):
            dict_result[f'Core {core_number}'] = dict(core_freq._asdict())
        return dict_result


class Disk:

    @staticmethod
    def disks_info():
        dict_result = {}
        disks = psutil.disk_partitions(all=False)

        for disk_number, disk in enumerate(disks):
            dict_result[f'Disk {disk_number}'] = dict(disk._asdict())

            if 'rw' in disk.opts:
                dict_result[f'Disk {disk_number}'].update(dict(psutil.disk_usage(disk.mountpoint)._asdict()))
            else:
                dict_result[f'Disk {disk_number}'].update({'total': 0, 'used': 0, 'free': 0, 'percent': 0})

        return dict_result

    @staticmethod
    def disks_io():
        dict_result = {}
        partitions_io = psutil.disk_io_counters(perdisk=True, nowrap=True)
        for disk in partitions_io:
            dict_result[disk] = dict(partitions_io[disk]._asdict())
        return dict_result


class Network:

    @staticmethod
    def net_io_counters():
        result = psutil.net_io_counters(pernic=True, nowrap=True)
        dict_result = {}
        for interface in result:
            dict_result[interface] = dict(result[interface]._asdict())
        return dict_result


class Processes:

    @staticmethod
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
    all_data['vm_detect'] = Virtual.vm_detect()
    all_data['virtual_memory'] = Memory.virtual_memory()
    all_data['swap_memory'] = Memory.swap_memory()
    all_data['cpu_times'] = Processor.cpu_times()
    all_data['cpu_percent'] = Processor.cpu_percent()
    all_data['cpu_count'] = Processor.cpu_count()
    all_data['cpu_stats'] = Processor.cpu_stats()
    all_data['cpu_freq'] = Processor.cpu_freq()
    all_data['disks_info'] = Disk.disks_info()
    all_data['disks_io'] = Disk.disks_io()
    all_data['net_io_counters'] = Network.net_io_counters()
    all_data['processes_info'] = Processes.processes_info()

    import json
    with open('all.json', 'w') as file:
        json.dump(all_data, file, indent=6)
