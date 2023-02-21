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


if __name__ == '__main__':
    #print(vm_detect())
    print(virtual_memory())
