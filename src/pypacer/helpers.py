import os
import re
from enum import Enum

location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class TargetType(Enum):
    IP_MASK = 1  # isInNet
    IP = 2
    HOST = 3  # for localHostOrDomainIs
    HOSTS = 4  # for dnsDomainIs


def get_target_type(target: str) -> TargetType:
    if re.fullmatch(r"[0-9.]+", target):
        return TargetType.IP
    elif re.fullmatch(r"[0-9./]+", target):
        return TargetType.IP_MASK
    elif target.startswith("."):
        return TargetType.HOSTS
    return TargetType.HOST
