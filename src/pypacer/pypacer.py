from typing import Optional

import yaml

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
        return """
        function FindProxyForURL(url, host) {{
            host = host.toLowerCase();
            // at this point they are placed exclusions
            return "{0}";
        }}
        """.format(self._get_default_proxy_route())

    def output(self) -> str:
        # IDEA: implement output with jinja
        return self._get_javascript()
