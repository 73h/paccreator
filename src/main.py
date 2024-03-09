import os

from pypacer import PyPacer
from pypacer.helpers import location

if __name__ == "__main__":
    p = PyPacer()
    with open(os.path.join(location, "..", "examples", "unittests.yaml"), "r") as f:
        p.load_from_yaml(f.read())
        print(p.output())

    simple_proxy = """
    proxies:
        DIRECT:
            route: DIRECT
    default: DIRECT
    """
    p.load_from_yaml(str(simple_proxy))
    print(p.output())
