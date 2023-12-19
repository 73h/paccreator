from typing import Optional

import yaml

from .pypacerconfig import PyPacerConfig


class PyPacer:
    def __init__(self):
        self.config: Optional[PyPacerConfig] = None

    def parse_from_yaml(self, stream: str):
        y = yaml.safe_load(stream)
        self.config = PyPacerConfig(**y)
        self.config.check()

    def _get_javascript(self) -> str:
        default_proxy = [p for p in self.config.proxies if p.name == self.config.default_proxy][0].proxy
        return """
        function FindProxyForURL(url, host) {{
            host = host.toLowerCase();
            // at this point they are placed exclusions
            return "{0}";
        }}
        """.format(default_proxy)

    def output(self) -> str:
        # IDEA: implement output with jinja
        return self._get_javascript()
