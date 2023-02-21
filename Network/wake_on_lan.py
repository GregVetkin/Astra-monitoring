import socket


def wake_on_lan(mac_address: str, broadcast='255.255.255.255', port=9):
    """
    Example:
    mac_address: 'AA:BB:CC:DD:EE:FF'
    """

    res_mac_address = mac_address.replace(':', '')
    mac_address_byte = bytes.fromhex(res_mac_address)

    packet_head = b'\xFF' * 6
    packet_body = mac_address_byte * 16
    packet_password = b'\x00' * 6

    magick_packet = packet_head + packet_body + packet_password

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(magick_packet, (broadcast, port))
    sock.close()


if __name__ == '__main__':
    wake_on_lan('50:EB:F6:28:8B:5A')  # 192.168.0.237
    wake_on_lan('30:85:a9:90:9e:1f')  # 192.168.0.247

