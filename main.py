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
        for core_number, core_info in enumerate(result):
            dict_result[f'Core {core_number}'] = dict(core_info._asdict())

    else:
        dict_result = dict(result._asdict())

    return dict_result


if __name__ == '__main__':
    #print(vm_detect())
    #print(virtual_memory())
    #print(swap_memory())
    print(cpu_times())