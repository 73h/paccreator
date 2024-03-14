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
    description: str = "use this proxy"
    targets: list = field(default_factory=lambda: [])
    tags: list[str] = field(default_factory=lambda: [])

    def __post_init__(self):
        self.targets = [Target(t) for t in self.targets]
        if "catch-plain-hostnames" in self.tags:
            target = Target("")
            target.type = "PLAIN_HOSTNAME"
            self.targets.append(target)


@dataclass
class PyPacerConfig:
    proxies: list
    version: str = "0.1"
    description: str = "pac file for my company"

    def __post_init__(self):
        self.proxies = [Proxy(**p) for p in self.proxies]

    def validate(self):
        for proxy in self.proxies:
            if not proxy.route:
                raise ValueError(f"one proxy has no route")
            # ToDo: Check proxy addresses

    def reorganize_proxies(self):
        # dns queries should be at the end. to get this done, proxies with mixed destinations need to be split
        i = 0
        for index, proxy in enumerate(self.proxies):
            i += 1
            targets = [t for t in proxy.targets]
            nw = ["IP", "NETWORK"]
            if any([t.type in nw for t in targets]) and any([t.type not in nw for t in targets]):
                new_proxy = Proxy(route=proxy.route, description=proxy.description)
                new_proxy.targets = [t for t in targets if t.type in nw]
                self.proxies.append(new_proxy)
                proxy.targets = [t for t in targets if t.type not in nw]

    def recognize_overlaps(self):
        for index, proxy in enumerate(self.proxies):
            all_targets = [x for xs in [p.targets for i, p in enumerate(self.proxies) if i != index] for x in xs]
            for target in proxy.targets:
                target.recognize_overlaps(all_targets)

    def get_default_proxy(self) -> Proxy:
        defaults = [p for p in self.proxies if "default" in p.tags]
        return defaults[0] if len(defaults) > 0 else [p for p in self.proxies][0]
