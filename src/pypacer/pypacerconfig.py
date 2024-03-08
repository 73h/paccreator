from dataclasses import dataclass, field


@dataclass
class Proxy:
    route: str
    description: str = ""


@dataclass
class PyPacerConfig:
    proxies: dict
    default: str
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
