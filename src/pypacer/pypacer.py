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

    def output(self) -> str:
        return str(self.config)
