from paccreator import load_from_yaml

if __name__ == "__main__":
    simple_proxy = """
    description: Simple proxy
    proxies:
      - description: use direct connection
        route: DIRECT
        targets:
          - 10.0.0.0/8
          - .my-company.com
      - description: use my proxy
        route: PROXY proxy.my-company.com:80
        tags:
          - default
        targets:
          - www.my-company.com
          - contact.my-company.com
      - description: use the special proxy
        route: PROXY proxy.my-company.com:8080
        targets:
          - datacenter.my-company.com
    """

    with load_from_yaml(str(simple_proxy)) as p:
        print(p.output(excludes=["default"]))
