from pypacer import PyPacer

if __name__ == "__main__":
    p = PyPacer()
    simple_proxy = """
    description: Simple proxy
    proxies:
      direct:
        description: use direct connection
        route: DIRECT
        targets:
          - 10.0.0.0/8
          - .my-company.com
      myproxy:
        description: use my proxy
        route: PROXY proxy.my-company.com:80
        default: true
        targets:
          - www.my-company.com
          - contact.my-company.com
      special_proxy:
        description: use the special proxy
        route: PROXY proxy.my-company.com:8080
        targets:
          - datacenter.my-company.com
    """
    p.load_from_yaml(str(simple_proxy))
    print(p.output())
