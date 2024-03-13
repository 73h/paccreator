import ipaddress
from dataclasses import dataclass, field

from pypacer.helpers import get_target_type


class Target:
    def __init__(self, target: str):
        self.target = str(target)
        self.rating = 0
        self.type = get_target_type(self.target)
        self.netmask = None
        if self.type == "NETWORK":
            self.netmask = ipaddress.ip_network(self.target).with_netmask.split("/")

    def recognize_overlaps(self, targets: list):
        if self.type == "HOSTS":
            for target in targets:
                if target.type == "HOST" and target.target.endswith(self.target):
                    target.rating = target.rating - 1
        if self.type == "IP":
            self.rating = 1
        if self.type == "NETWORK":
            self.rating = 2


@dataclass
class Proxy:
    route: str
    description: str = ""
    targets: list = field(default_factory=lambda: [])

    def __post_init__(self):
        self.targets = [Target(t) for t in self.targets]


@dataclass
class PyPacerConfig:
    proxies: dict
    default: str
    version: str = "1.0"
    description: str = "PAC File for my great company"
    routings: list = field(default_factory=lambda: [])

    def __post_init__(self):
        self.proxies = {k: Proxy(**v) for k, v in self.proxies.items()}

    def validate(self):
        if self.default not in [p for p in self.proxies.keys()]:
            raise ValueError("default is not in proxies")
        for name, proxy in self.proxies.items():
            if not proxy.route:
                raise ValueError(f"proxy {name} has no route")
            # ToDo: Check proxy addresses

    def reorganize_proxies(self):
        # dns queries should be at the end. to get this done, proxies with mixed destinations need to be split
        proxies = {}
        i = 0
        for name, proxy in self.proxies.items():
            i += 1
            targets = [t for t in proxy.targets]
            nw = ["IP", "NETWORK"]
            if any([t.type in nw for t in targets]) and any([t.type not in nw for t in targets]):
                new_proxy = Proxy(route=proxy.route, description=proxy.description)
                new_proxy.targets = [t for t in targets if t.type in nw]
                proxies[f"{name}_{str(i)}"] = new_proxy
                proxy.targets = [t for t in targets if t.type not in nw]
        self.proxies.update(proxies)

    def recognize_overlaps(self):
        for name, proxy in self.proxies.items():
            all_targets = [x for xs in [p.targets for n, p in self.proxies.items() if n != name] for x in xs]
            for target in proxy.targets:
                target.recognize_overlaps(all_targets)

    def get_default_proxy_route(self) -> str:
        return self.proxies[self.default].route
