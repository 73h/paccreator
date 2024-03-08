import os

from pypacer import PyPacer
from pypacer.helpers import location

if __name__ == "__main__":
    pac_file = open(os.path.join(location, "..", "examples", "unittests.yaml"), "r").read()
    p = PyPacer()
    p.load_config_from_yaml(pac_file)
    print(p.output())
