import os
import re

location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_target_type(target: str) -> str:
    if re.fullmatch(r"[0-9.]+", target):
        return "IP"
    elif re.fullmatch(r"[0-9./]+", target):
        return "IP_MASK"
    elif target.startswith("."):
        return "HOSTS"
    return "HOST"


def sort_by_rating(proxy):
    rating = 0
    for target in proxy.targets:
        rating += target.rating
    return rating
