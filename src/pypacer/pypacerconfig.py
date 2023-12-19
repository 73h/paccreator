from dataclasses import dataclass, field


def d(x) -> dict:
    # facepalm
    return x


@dataclass
class Proxy:
    name: str
    proxy: str
    description: str = ""
    targets: list[str] = field(default_factory=list)


@dataclass
class PyPacerConfig:
    proxies: list[Proxy]
    default_proxy: str
    description: str = "PAC File for my great company"

    def __post_init__(self):
        proxies = []
        for proxy in self.proxies:
            proxies.append(Proxy(**dict(d(proxy))))
        self.proxies = proxies

    def check(self):
        if self.default_proxy not in [p.name for p in self.proxies]:
            raise ValueError("default_proxy is not in proxies")
