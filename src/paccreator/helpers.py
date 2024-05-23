import ipaddress
import re
from enum import Enum


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


class TargetType(Enum):
    PLAIN_HOSTNAME = 0
    HOST = 2
    HOSTS = 4
    STRING = 6
    STRING_L = 8
    STRING_R = 10
    IP = 12
    NETWORK = 14


def get_target_type(target: str) -> TargetType:
    if is_ipaddress(target):
        return TargetType.IP
    elif is_network(target):
        return TargetType.NETWORK
    elif is_hostname(target):
        if target.startswith("."):
            return TargetType.HOSTS
        return TargetType.HOST
    else:
        if target.startswith("."):
            return TargetType.STRING_R
        if target.endswith("."):
            return TargetType.STRING_L
        return TargetType.STRING


def sort_by_rating(proxy):
    return min([t.rating for t in proxy.targets])
