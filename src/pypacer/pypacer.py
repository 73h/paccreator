import yaml


class PyPacer(object):
    def __init__(self, *args, **kwargs):
        self.temp = "Hello World!"

    def parse_from_yaml(self, stream: str, *args, **kwargs):
        self.temp = yaml.safe_load(stream)

    def output(self, *args, **kwargs) -> str:
        return self.temp
