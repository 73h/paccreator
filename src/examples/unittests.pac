function FindProxyForURL(url, host) {
    host = host.toLowerCase();
    if (
           localHostOrDomainIs(host, "example.com")
        || localHostOrDomainIs(host, "foo.example.com")
        || localHostOrDomainIs(host, "foo.example.net")
    ) { return "PROXY domain-overlaps.example.com"; }
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
           localHostOrDomainIs(host, "example.net")
        || localHostOrDomainIs(host, "bar.example.com")
        || localHostOrDomainIs(host, "bar.example.net")
        || isInNet(host, "20.10.10.0", "255.255.255.0")
        || dnsResolve(host) === "130.131.132.133"
    ) { return "PROXY mixed.example.com"; }
    if (
           isInNet(host, "93.184.0.0", "255.255.0.0")
        || isInNet(host, "2001:db8:85a3:8d3::", "ffff:ffff:ffff:ffff::")
    ) { return "PROXY netmask.example.com"; }
    return "PROXY default.example.com";
}