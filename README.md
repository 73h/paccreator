# Generate auto proxy config files (PAC) from a declaration

[![Tests](https://github.com/73h/pypacer/actions/workflows/tests.yml/badge.svg)](https://github.com/73h/pypacer/actions/workflows/tests.yml)

---

This package aims to make it possible to create simple proxy scripts declaratively. It will never cover all the
subtleties. If you have unusual requirements, it is better to write the proxy script directly in JavaScript

## Usage

ToDo: Build package and publish on pypi

You can also load the script directly with pip:
```
pip install git+https://github.com/73h/pypacer.git@main#egg=pypacer
```

Create a file called myproxy.yaml and define your proxy rules in it like this:
```yaml
description: "(optional) A description of the proxy script"
version: "(optional) The version of the proxy script"
default: direct # The default proxy to use
proxies:
  direct:
    route: "DIRECT"
    description: "(optional) A description of the proxy"
    targets:
      - "example.com"
      - "foo.example.com"
      - ".example.net"
      # You can also use a network mask, ip-addresses, hosts or strings
  proxy1:
    route: "PROXY proxy1.example.com:80; DIRECT"
    targets:
      - "10.0.0.0/8"
```

Run this in python:
```python
import os
from pypacer import PyPacer

p = PyPacer()
with open(os.path.join("myproxy.yaml"), "r") as f:
    p.load_from_yaml(f.read())
    print(p.output())
```

## Examples

### A simple Example for a random company

yaml:  
```yaml
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
    route: "PROXY proxy.my-company.com:8080"
    targets:
      - "datacenter.my-company.com"
default: MYPROXY
```

As a result, you can see that it has resolved the overlap between ``.my-company.com`` and,
for example, ``contact.my-company.com`` by first evaluating the exact subdomains.
The network mask ``10.0.0.0/8`` was placed at the end to avoid DNS queries when they are not necessary.  
```javascript
function FindProxyForURL(url, host) {
    host = host.toLowerCase();
    if (
         localHostOrDomainIs(host, "www.my-company.com")
      || localHostOrDomainIs(host, "contact.my-company.com")
    ) { return "PROXY proxy.my-company.com:80"; }
    if (
         localHostOrDomainIs(host, "datacenter.my-company.com")
    ) { return "PROXY proxy.my-company.com:8080"; }
    if (
         dnsDomainIs(host, ".my-company.com")
    ) { return "DIRECT"; }
    if (
         isInNet(host, "10.0.0.0", "255.0.0.0")
    ) { return "DIRECT"; }
    return "PROXY proxy.my-company.com:80";
}
```

### Unit Tests Example

You can see all the options supported so far in the test examples.

unittests.yaml:
```yaml
description: For the unittests, hopefully no real script should look like this. ;)
version: 1.0
default: PROXY_DEFAULT
proxies:
  DIRECT:
    description: take the direct route
    route: "DIRECT"
    targets:
      - ".example.com"
  PROXY_DOMAIN_OVERLAPS:
    description: here domains overlap with the default route
    route: "PROXY domain-overlaps.example.com"
    targets:
      - "example.com"
      - "foo.example.com"
      - "foo.example.net"
  PROXY_NETMASK:
    description: a proxy for netmask
    route: "PROXY netmask.example.com"
    targets:
      - "93.184.0.0/16"
      - "2001:0db8:85a3:08d3::/64"
  PROXY_IP:
    description: a proxy for IPs
    route: "PROXY ip.example.com"
    targets:
      - "192.0.0.170"
      - "127.0.0.1"
  PROXY_STRING:
    description: a proxy for string matches
    route: "PROXY string.example.com"
    targets:
      - "10."
      - ".102.123"
      - "10"
  PROXY_MIXED:
    description: a proxy for mixed matches, this should be split up
    route: "PROXY mixed.example.com"
    targets:
      - "example.net"
      - "bar.example.com"
      - "bar.example.net"
      - "20.10.10.0/24"
      - "130.131.132.133"
  PROXY_DEFAULT:
    description: take the default proxy route
    route: "PROXY default.example.com"
    targets: []
```

unittests.pac:
```javascript
function FindProxyForURL(url, host) {
    host = host.toLowerCase();
    if (
        localHostOrDomainIs(host, "example.com")
        || localHostOrDomainIs(host, "foo.example.com")
        || localHostOrDomainIs(host, "foo.example.net")
    ) { return "PROXY domain-overlaps.example.com"; }
    if (
        localHostOrDomainIs(host, "example.net")
        || localHostOrDomainIs(host, "bar.example.com")
        || localHostOrDomainIs(host, "bar.example.net")
    ) { return "PROXY mixed.example.com"; }
    if (
        dnsDomainIs(host, ".example.com")
    ) { return "DIRECT"; }
    if (
        host.substring(0, 3) === "10."
        || host.substring(host.length - 8) === ".102.123"
        || host === "10"
    ) { return "PROXY string.example.com"; }
    if (
        dnsResolve(host) === "192.0.0.170"
        || dnsResolve(host) === "127.0.0.1"
    ) { return "PROXY ip.example.com"; }
    if (
        isInNet(host, "20.10.10.0", "255.255.255.0")
        || dnsResolve(host) === "130.131.132.133"
    ) { return "PROXY mixed.example.com"; }
    if (
        isInNet(host, "93.184.0.0", "255.255.0.0")
        || isInNet(host, "2001:db8:85a3:8d3::", "ffff:ffff:ffff:ffff::")
    ) { return "PROXY netmask.example.com"; }
    return "PROXY default.example.com";
}
```