from typing import Optional

import yaml
from jinja2 import Environment, FileSystemLoader

from .helpers import location
from .pypacerconfig import PyPacerConfig


class PyPacer:
    def __init__(self):
        self.config: Optional[PyPacerConfig] = None

    def load_config_from_yaml(self, stream: str):
        y = yaml.safe_load(stream)
        self.config = PyPacerConfig(**y)
        self.config.validate()

    def _get_default_proxy_route(self) -> str:
        return self.config.proxies[self.config.default].route

    def _get_javascript(self) -> str:
        environment = Environment(loader=FileSystemLoader(location))
        template = environment.get_template("template.js")
        return template.render(
            default=self._get_default_proxy_route()
        )

    def output(self) -> str:
        return self._get_javascript()
