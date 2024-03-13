import copy
import pathlib
from typing import Optional

import yaml
from jinja2 import Environment, FileSystemLoader

from .helpers import sort_by_rating
from .pypacerconfig import PyPacerConfig


class PyPacer:
    def __init__(self):
        self.config: Optional[PyPacerConfig] = None

    def load_from_dict(self, d: dict):
        self.config = PyPacerConfig(**d)
        self.config.validate()

    def load_from_yaml(self, stream: str):
        y = yaml.safe_load(stream)
        self.load_from_dict(y)

    def output(self) -> str:
        if self.config is None:
            raise Exception("No config loaded, use load_from_yaml or load_from_dict first.")
        config = copy.deepcopy(self.config)
        default = config.get_default_proxy()
        config.reorganize_proxies()
        config.recognize_overlaps()
        environment = Environment(loader=FileSystemLoader(pathlib.Path(__file__).parent.resolve()))
        template = environment.get_template("template.js.jinja")
        proxies = [p for p in config.proxies.values() if len(p.targets) > 0]
        proxies.sort(key=sort_by_rating)
        return template.render(
            default=default,
            proxies=proxies,
            description=config.description,
            version=config.version
        )
