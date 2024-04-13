function FindProxyForURL(url, host) {
    /*
        Description: For the unittests, hopefully no real script should look like this. ;)
        Version: 1.0
    */
    host = host.toLowerCase();
    if (
           isPlainHostName(host)// rating: 0
    ) {
        /* a proxy for plain hostnames */
        return "PROXY plain-hostname.example.com";
    }
    if (
           localHostOrDomainIs(host, "example.com")// rating: 2
        || localHostOrDomainIs(host, "foo.example.com")// rating: 1
        || localHostOrDomainIs(host, "foo.example.net")// rating: 2
    ) {
        /* here domains overlap with the default route */
        return "PROXY domain-overlaps.example.com";
    }
    if (
           localHostOrDomainIs(host, "example.net")// rating: 2
        || localHostOrDomainIs(host, "bar.example.com")// rating: 1
        || localHostOrDomainIs(host, "bar.example.net")// rating: 2
    ) {
        /* a proxy for mixed matches, this should be split up */
        return "PROXY mixed.example.com";
    }
    if (
           dnsDomainIs(host, ".example.com")// rating: 4
    ) {
        /* take the direct route */
        return "DIRECT";
    }
    if (
           host === "10"// rating: 6
        || host.substring(0, 3) === "10."// rating: 8
        || host.substring(host.length - 8) === ".102.123"// rating: 10
    ) {
        /* a proxy for string matches */
        return "PROXY string.example.com";
    }
    if (
           dnsResolve(host) === "240.100.50.3"// rating: 11
    ) {
        /* the ip is within the netmask */
        return "PROXY ip-within-netmask-2.example.com";
    }
    if (
           dnsResolve(host) === "192.0.0.170"// rating: 12
        || dnsResolve(host) === "192.0.0.171"// rating: 12
        || dnsResolve(host) === "127.0.0.1"// rating: 12
    ) {
        /* a proxy for IPs */
        return "PROXY ip.example.com";
    }
    if (
           dnsResolve(host) === "130.131.132.133"// rating: 12
    ) {
        /* a proxy for mixed matches, this should be split up */
        return "PROXY mixed.example.com";
    }
    if (
           isInNet(host, "240.100.50.0", "255.255.255.0")// rating: 14
    ) {
        /* the ip is within the netmask */
        return "PROXY ip-within-netmask-1.example.com";
    }
    if (
           isInNet(host, "93.184.0.0", "255.255.0.0")// rating: 14
    ) {
        /* a proxy for netmask */
        return "PROXY netmask.example.com";
    }
    if (
           isInNet(host, "240.100.51.0", "255.255.255.0")// rating: 14
    ) {
        /* the ip is within the netmask */
        return "PROXY ip-within-netmask-2.example.com";
    }
    if (
           isInNet(host, "20.10.10.0", "255.255.255.0")// rating: 14
    ) {
        /* a proxy for mixed matches, this should be split up */
        return "PROXY mixed.example.com";
    }
    /* Default: take the default proxy route */
    return "PROXY default.example.com";
}