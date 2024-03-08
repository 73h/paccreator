from dataclasses import dataclass, field


@dataclass
class Proxy:
    route: str
    description: str = ""


@dataclass
class Routing:
    proxy: str
    hosts: list[str] = field(default_factory=lambda: [])
    host: str = ""
    order: int = 0


@dataclass
class PyPacerConfig:
    proxies: dict
    default: str
    version: str = "1.0"
    description: str = "PAC File for my great company"
    routings: list = field(default_factory=lambda: [])

    def __post_init__(self):
        self.proxies = {k: Proxy(**v) for k, v in self.proxies.items()}
        self.routings = [Routing(**r) for r in self.routings]

    def validate(self):
        self._validate_proxies()

    def _validate_proxies(self):
        if self.default not in [p for p in self.proxies.keys()]:
            raise ValueError("default is not in proxies")
        for name, proxy in self.proxies.items():
            if not proxy.route:
                raise ValueError(f"proxy {name} has no route")
            # ToDo: Check proxy addresses

    def _validate_routings(self):

        for routing in self.routings:
            # test if the proxy exists
            if routing.proxy not in [p for p in self.proxies.keys()]:
                raise ValueError(f"proxy {routing.proxy} does not exist")
            # test whether at least one host exists
            if len(routing.hosts) == 0 and not routing.host:
                raise ValueError(f"a routing has no host")
