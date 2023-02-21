import subprocess
import netifaces
import datetime
import multiprocessing


def unix_time_to_str(timestamp):
    time_format = '%Y-%m-%d %H:%M:%S'
    time = datetime.datetime.fromtimestamp(timestamp)
    time = time.strftime(time_format)
    return time


def ip4_addresses():
    """
    :return: a dictionary containing interface names with a list of ip-addresses

    Example return: {'eth0':['192.168.0.101', '192.168.2.55'], 'lo':['127.0.0.1']}
    """

    result_ip = {}

    for interface in netifaces.interfaces():
        interface_ips = []

        for link in netifaces.ifaddresses(interface)[netifaces.AF_INET]: #AF_INET, AF_LINK, AF_INET6
            interface_ips.append(link['addr'])

        result_ip[interface] = interface_ips

    return result_ip


def ip_duplication(ip, interface):
    """
    Linux package required: 'iputils-arping'  (sudo apt-get install iputils-arping).
    The package is present in the repository of the Astra-Linux installation disk.

    :return:  True - there is a duplicate, False - there is not
    """

    command = f'sudo arping -D -w 5 -I {interface} {ip}' #python3.7+ format
    process = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE)
    bash_result = process.wait()

    if bash_result == 0:
        return False

    elif bash_result == 1:
        return True


def ip_duplicates():
    """
    Linux only

    Sequential ping of all addresses

    Linux package required: 'iputils-arping'  (sudo apt-get install iputils-arping).
    The package is present in the repository of the Astra-Linux installation disk.
    """

    interfaces = ip4_addresses()
    result = {}

    for interface in interfaces:
        ip_list = interfaces[interface]

        for ip in ip_list:
            result[ip] = ip_duplication(ip, interface)

    return result


def ip_duplicates_multiprocessing():
    """
    Linux only.

    Multiprocessing of the 'ip_duplicates' function.

    Linux package required: 'iputils-arping'  (sudo apt-get install iputils-arping).
    The package is present in the repository of the Astra-Linux installation disk.
    """

    interfaces = ip4_addresses()
    ips = []

    for interface in interfaces:
        ip_list = interfaces[interface]

        for ip in ip_list:
            ips.append([ip, interface])

    with multiprocessing.Pool() as p:
        result_pool = p.starmap(ip_duplication, ips)

    result = {}
    for _, (ip, adapter) in enumerate(ips):
        if adapter not in result:
            result[adapter] = {}
        result[adapter][ip] = result_pool[_]

    return result



if __name__ == '__main__':
    print(ip4_addresses())
    print(ip_duplicates_multiprocessing())
