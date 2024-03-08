function FindProxyForURL(url, host) {
    host = host.toLowerCase();
    // at this point they are placed exclusions
    return "{{ default }}";
}
