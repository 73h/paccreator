function FindProxyForURL(url, host) {
    host = host.toLowerCase();
    if (
           localHostOrDomainIs(host, "example.com")
        || localHostOrDomainIs(host, "foo.example.com")
        || localHostOrDomainIs(host, "bar.example.com")
    ) { return "PROXY company.example.com"; }
    if (
           dnsDomainIs(host, ".example.com")
    ) { return "DIRECT"; }
    if (
           isInNet(host, "99.77.128.0", "255.255.192.0")
        || isInNet(host, "140.82.121.0", "255.255.255.0")
        || isInNet(host, "10.0.0.0", "255.0.0.0")
        || host === "127.0.0.1"
    ) { return "PROXY netmask.example.com"; }
    return "PROXY default.example.com";
}