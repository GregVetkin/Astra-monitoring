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


if __name__ == '__main__':
    #print(vm_detect())
    #print(virtual_memory())
    #print(swap_memory())
    #print(cpu_times())
    #print(cpu_percent())
    print(cpu_count())