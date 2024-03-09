# Generate auto proxy config files (PAC) from a declaration

[![Tests](https://github.com/73h/pypacer/actions/workflows/tests.yml/badge.svg)](https://github.com/73h/pypacer/actions/workflows/tests.yml)

---

This package aims to make it possible to create simple proxy scripts declaratively. It will never cover all the
subtleties. If you have unusual requirements, it is better to write the proxy script directly in JavaScript

## Usage

ToDo: Build package and publish on pypi

### Example

example.yaml:

```yaml
description: A normal proxy script
version: 1.0
default: PROXY_DEFAULT
proxies:
  DIRECT:
    description: take the direct route
    route: "DIRECT"
    targets:
      - ".example.com"
  PROXY_NET_MASKS:
    description: take the proxy A route
    route: "PROXY netmask.example.com"
    targets:
      - "93.184.0.0/16"
      - "example.net"
      - "192.0.0.170"
      - "127.0.0.1"
  PROXY_COMPANY:
    description: take the proxy B route
    route: "PROXY company.example.com"
    targets:
      - "example.com"
      - "foo.example.com"
      - "bar.example.com"
  PROXY_DEFAULT:
    description: take the default proxy route
    route: "PROXY default.example.com"
    targets: []

```

run this in python:

```python
import os
from pypacer import PyPacer

p = PyPacer()
with open(os.path.join("examples.yaml"), "r") as f:
    p.load_from_yaml(f.read())
    print(p.output())
```

and you get this:

```javascript
function FindProxyForURL(url, host) {
    host = host.toLowerCase();
    if (
        localHostOrDomainIs(host, "example.com")
        || localHostOrDomainIs(host, "foo.example.com")
        || localHostOrDomainIs(host, "bar.example.com")
    ) {
        return "PROXY company.example.com";
    }
    if (
        dnsDomainIs(host, ".example.com")
    ) {
        return "DIRECT";
    }
    if (
        isInNet(host, "93.184.0.0", "255.255.0.0")
        || localHostOrDomainIs(host, "example.net")
        || isInNet(host, "192.0.0.170", "255.255.255.255")
        || isInNet(host, "127.0.0.1", "255.255.255.255")
    ) {
        return "PROXY netmask.example.com";
    }
    return "PROXY default.example.com";
}
```
