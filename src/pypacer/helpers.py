import ipaddress
import re


def is_ipaddress(ip) -> bool:
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def is_network(ip) -> bool:
    try:
        ipaddress.ip_network(ip)
        return True
    except ValueError:
        return False


def is_hostname(hostname):
    if len(hostname) > 255 or not hostname:
        return False
    hostname = hostname.rstrip(".") if hostname.endswith(".") else hostname
    hostname = hostname.lstrip(".") if hostname.startswith(".") else hostname
    regex = r"^((?!-)[\w-]" + "{1,63}(?<!-)\\.)" + "+[A-Za-z]{2,6}"
    p = re.compile(regex)
    if re.search(p, hostname):
        return True
    return False


def get_target_type(target: str) -> str:
    if is_ipaddress(target):
        return "IP"
    elif is_network(target):
        return "NETWORK"
    elif is_hostname(target):
        if target.startswith("."):
            return "HOSTS"
        return "HOST"
    else:
        if target.startswith("."):
            return "STRING_R"
        if target.endswith("."):
            return "STRING_L"
        return "STRING"


def sort_by_rating(proxy):
    rating = 0
    for target in proxy.targets:
        rating += target.rating
    return rating
