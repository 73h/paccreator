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
           isInNet(host, "93.184.0.0", "255.255.0.0")
        || localHostOrDomainIs(host, "example.net")
        || isInNet(host, "192.0.0.170", "255.255.255.255")
        || isInNet(host, "127.0.0.1", "255.255.255.255")
    ) { return "PROXY netmask.example.com"; }
    return "PROXY default.example.com";
}