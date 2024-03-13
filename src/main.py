from pypacer import PyPacer

if __name__ == "__main__":
    p = PyPacer()
    simple_proxy = """
    description: "Simple proxy"
    proxies:
      DIRECT:
        route: "DIRECT"
        targets:
          - "10.0.0.0/8"
          - ".my-company.com"
      MYPROXY:
        route: "PROXY proxy.my-company.com:80"
        targets:
          - "www.my-company.com"
          - "contact.my-company.com"
      SPECIAL_PROXY:
        description: "Special proxy"
        route: "PROXY proxy.my-company.com:8080"
        targets:
          - "datacenter.my-company.com"
    default: MYPROXY
    """
    p.load_from_yaml(str(simple_proxy))
    print(p.output())
