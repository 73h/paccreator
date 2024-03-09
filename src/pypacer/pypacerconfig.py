from dataclasses import dataclass, field

from pypacer.helpers import get_target_type, compute_netmask


class Target:
    def __init__(self, target: str):
        self.target = target
        self.rating = 0
        self.type = get_target_type(target)
        self.netmask = None
        if self.type == "NET_MASK":
            self.netmask = compute_netmask(self.target)
        elif self.type == "IP4":
            self.netmask = compute_netmask(f"{self.target}/32")

    def recognize_overlaps(self, targets: list):
        if self.type == "HOSTS":
            for target in targets:
                if target.type == "HOST" and target.target.endswith(self.target):
                    self.rating = target.rating + 2
        if self.type == "NET_MASK":
            self.rating = self.rating + 1


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
        self._recognize_overlaps()

    def _recognize_overlaps(self):
        for name, proxy in self.proxies.items():
            all_targets = [x for xs in [p.targets for n, p in self.proxies.items() if n != name] for x in xs]
            for target in proxy.targets:
                target.recognize_overlaps(all_targets)
