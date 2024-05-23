import copy
import pathlib
from contextlib import contextmanager
from typing import Optional

import yaml
from jinja2 import Environment, FileSystemLoader

from .helpers import sort_by_rating
from .paccreatorconfig import PacCreatorConfig


class PacCreator:
    def __init__(self):
        self.config: Optional[PacCreatorConfig] = None

    def load_from_dict(self, config: dict):
        self.config = PacCreatorConfig(**config)
        self.config.validate()

    def load_from_yaml(self, config: str):
        y = yaml.safe_load(config)
        self.load_from_dict(y)

    def output(self, excludes: list[str] = None, includes: list[str] = None) -> str:
        """Returns the finished ProxyScript as a string

        Parameters
        ----------
        excludes : list[str], optional
            A list of tags. Proxies that have this tag are excluded.

        includes : list[str], optional
            A list of tags. Proxies that have this tag are included. Other proxies are not included.

        """
        if self.config is None:
            raise Exception("No config loaded, use load_from_yaml or load_from_dict first.")
        config = copy.deepcopy(self.config)

        # handle includes
        if includes:
            proxies = []
            for proxy in config.proxies:
                include = False
                for tag in proxy.tags:
                    if tag in includes:
                        include = True
                if include:
                    proxies.append(proxy)
            config.proxies = proxies

        # handle excludes
        if excludes:
            proxies = []
            for proxy in config.proxies:
                exclude = False
                for tag in proxy.tags:
                    if tag in excludes:
                        exclude = True
                if not exclude:
                    proxies.append(proxy)
            config.proxies = proxies

        default = config.get_default_proxy()
        config.reorganize_proxies()
        config.recognize_overlaps()
        environment = Environment(loader=FileSystemLoader(pathlib.Path(__file__).parent.resolve()))
        template = environment.get_template("template.js.jinja")
        proxies = [p for p in config.proxies if len(p.targets) > 0]
        proxies.sort(key=sort_by_rating)
        return template.render(
            default=default,
            proxies=proxies,
            description=config.description,
            version=config.version
        )


@contextmanager
def load_from_yaml(config: str) -> PacCreator():
    p = PacCreator()
    p.load_from_yaml(config)
    yield p


@contextmanager
def load_from_dict(config: dict) -> PacCreator():
    p = PacCreator()
    p.load_from_dict(config)
    yield p
