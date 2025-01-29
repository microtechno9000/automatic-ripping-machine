from netifaces import interfaces, ifaddresses, AF_INET


def detect_ip() -> str:
    """
    Autodetect the host's IP address, excluding the loopback address ('127.0.0.1').

    This function scans all network interfaces on the host machine and collects non-loopback IPv4 addresses.
    If multiple IP addresses are detected, the first one in the list is returned.

    Returns:
        ip (str): The detected IP address.
                    If no suitable IP is found, the default
                    loopback address ('127.0.0.1') is returned.

    Example:
        If the host machine has an IP address of '192.168.1.100', the function
        will return that address, provided it is not the loopback address.
    """
    arm_ip = '127.0.0.1'
    # autodetect host IP address
    ip_list = []
    for interface in interfaces():
        inet_links = ifaddresses(interface).get(AF_INET, [])
        for link in inet_links:
            ip = link['addr']
            if ip != '127.0.0.1':
                ip_list.append(ip)
    if len(ip_list) > 0:
        arm_ip = ip_list[0]

    return arm_ip
