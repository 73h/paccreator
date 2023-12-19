from pypacer import PyPacer

if __name__ == "__main__":
    p = PyPacer()
    yaml = """
    description: PAC File for TEST
    proxies:
        - name: proxy-1
          proxy: PROXY proxy1.example.com:8080; DIRECT
          description: proxy-1
        - name: proxy-2
          proxy: DIRECT
          description: proxy-2
    default_proxy: proxy-1
    """
    p.parse_from_yaml(yaml)
    print(p.output())
