import os
from typing import Optional

import yaml
from jinja2 import Environment, FileSystemLoader

from .helpers import location, sort_by_rating
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
        template = environment.get_template("template.js.jinja")
        proxies = [p for p in self.config.proxies.values()]
        proxies.sort(key=sort_by_rating)
        return template.render(
            default=self._get_default_proxy_route(),
            proxies=proxies,
        )

    def output(self) -> str:
        output = self._get_javascript()
        open(os.path.join(location, "..", "examples", "unittests.pac"), "w").write(output)
        return output
