function FindProxyForURL(url, host) {
    host = host.toLowerCase();
    url = url.toLowerCase();
    if (
           isInNet(host, "93.184.0.0", "255.255.0.0")
        || localHostOrDomainIs(host, "example.net")
        || dnsResolve(host) === "192.0.0.170"
        || dnsResolve(host) === "127.0.0.1"
    ) { return "PROXY netmask.example.com"; }
    if (
           localHostOrDomainIs(host, "example.com")
        || localHostOrDomainIs(host, "foo.example.com")
        || localHostOrDomainIs(host, "bar.example.com")
    ) { return "PROXY company.example.com"; }
    if (
           dnsDomainIs(host, ".example.com")
    ) { return "DIRECT"; }
    return "PROXY default.example.com";
}