function FindProxyForURL(url, host) {
    /*
        Description: For the unittests, hopefully no real script should look like this. ;)
        Version: 1.0
    */
    host = host.toLowerCase();
    if (
           localHostOrDomainIs(host, "example.com")
        || localHostOrDomainIs(host, "foo.example.com")
        || localHostOrDomainIs(host, "foo.example.net")
    ) {
        /* here domains overlap with the default route */
        return "PROXY domain-overlaps.example.com";
    }
    if (
           localHostOrDomainIs(host, "example.net")
        || localHostOrDomainIs(host, "bar.example.com")
        || localHostOrDomainIs(host, "bar.example.net")
    ) {
        /* a proxy for mixed matches, this should be split up */
        return "PROXY mixed.example.com";
    }
    if (
           dnsDomainIs(host, ".example.com")
    ) {
        /* take the direct route */
        return "DIRECT";
    }
    if (
           isPlainHostName(host)
    ) {
        /* a proxy for plain hostnames */
        return "PROXY plain-hostname.example.com";
    }
    if (
           host.substring(0, 3) === "10."
        || host.substring(host.length - 8) === ".102.123"
        || host === "10"
    ) {
        /* a proxy for string matches */
        return "PROXY string.example.com";
    }
    if (
           isInNet(host, "93.184.0.0", "255.255.0.0")
    ) {
        /* a proxy for netmask */
        return "PROXY netmask.example.com";
    }
    if (
           dnsResolve(host) === "192.0.0.170"
        || dnsResolve(host) === "192.0.0.171"
        || dnsResolve(host) === "127.0.0.1"
    ) {
        /* a proxy for IPs */
        return "PROXY ip.example.com";
    }
    if (
           isInNet(host, "20.10.10.0", "255.255.255.0")
        || dnsResolve(host) === "130.131.132.133"
    ) {
        /* a proxy for mixed matches, this should be split up */
        return "PROXY mixed.example.com";
    }
    /* Default: take the default proxy route */
    return "PROXY default.example.com";
}