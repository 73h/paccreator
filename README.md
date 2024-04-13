# Generate auto proxy config files (PAC) from a declaration

[![Tests](https://github.com/73h/pypacer/actions/workflows/tests.yml/badge.svg)](https://github.com/73h/pypacer/actions/workflows/tests.yml)

---

This package aims to make it possible to create simple proxy scripts declaratively. It will never cover all the
subtleties. If you have unusual requirements, it is better to write the proxy script directly in JavaScript

## I would still like to implement this

- [x] ~~automatic sorting for overlapping host names~~
- [x] ~~implementation of inclusion and exclusion filters for output~~
- [x] ~~sort automatically if ip address in network mask~~
- [ ] publish on pypi
- [ ] Add annotation to automatically add local networks to the proxy


## Usage

You can also load the script directly with pip:
```
pip install git+https://github.com/73h/pypacer.git@main#egg=pypacer
```

Create a file called myproxy.yaml and define your proxy rules in it like this:
```yaml
description: A description of proxy script # (optional, default=pac file for my company)
version: The version of proxy script # (optional, default=0.1)
proxies:
  - route: DIRECT
    description: A description of proxy # (optional, default=use this proxy)
    tags: # (optional) Here you can add any comments you like, which you can use to filter later. However, there are also standard annotations.
      - default # (optional) This marks the proxy as default if no other condition applies. if no default proxy is available, the first one is used.
      - catch-plain-hostnames # (optional) This proxy applies if there is no domain name in the hostname (no dots). You should not annotate this on several proxies.
    targets:
      - example.com
      - foo.example.com
      - .example.net
      # You can also use a network mask, ip-addresses, hosts or strings
  - route: PROXY proxy1.example.com:80; DIRECT
    targets:
      - 10.0.0.0/8
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
```

As a result, you can see that it has resolved the overlap between ``.my-company.com`` and,
for example, ``contact.my-company.com`` by first evaluating the exact subdomains.
The network mask ``10.0.0.0/8`` was placed at the end to avoid DNS queries when they are not necessary.  
```javascript
function FindProxyForURL(url, host) {
    /*
        Description: Simple proxy
        Version: 0.1
    */
    host = host.toLowerCase();
    if (
        localHostOrDomainIs(host, "www.my-company.com")
        || localHostOrDomainIs(host, "contact.my-company.com")
    ) {
        /* use my proxy */
        return "PROXY proxy.my-company.com:80";
    }
    if (
        localHostOrDomainIs(host, "datacenter.my-company.com")
    ) {
        /* use the special proxy */
        return "PROXY proxy.my-company.com:8080";
    }
    if (
        dnsDomainIs(host, ".my-company.com")
    ) {
        /* use direct connection */
        return "DIRECT";
    }
    if (
        isInNet(host, "10.0.0.0", "255.0.0.0")
    ) {
        /* use direct connection */
        return "DIRECT";
    }
    /* Default: use my proxy */
    return "PROXY proxy.my-company.com:80";
}
```

### Unit Tests Example

You can see all the options supported so far in the test examples.

- [unittests.yaml](src/examples/unittests.yaml)
- [unittests.pac](src/examples/unittests.pac)
