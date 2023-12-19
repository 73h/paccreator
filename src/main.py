from pypacer import PyPacer

if __name__ == "__main__":
    p = PyPacer()
    yaml = """
    foo:
        bar: 1
        baz: 2
    """
    p.parse_from_yaml(yaml)
    print(p.output())
