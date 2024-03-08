function FindProxyForURL(url, host) {
    var host = host.toLowerCase();
    if (
           dnsDomainIs(host, "99.77.128.0/18")
        || dnsDomainIs(host, "127.0.0.0/24")
    ) { return "PROXY localhost:8080"; }
    if (
           localHostOrDomainIs(host, "example.com")
        || localHostOrDomainIs(host, "foo.example.com")
        || localHostOrDomainIs(host, "bar.example.com")
    ) { return "PROXY localhost:8081"; }
    if (
           dnsDomainIs(host, ".example.com")
    ) { return "DIRECT"; }
    return "PROXY localhost:8080";
}