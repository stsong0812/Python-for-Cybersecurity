import dns
import dns.resolver
import socket


def ReverseDNS(ip):
    """
    Perform reverse DNS lookup for an IP address and return associated hostnames.
    """
    try:
        result = socket.gethostbyaddr(ip)
        return [result[0]] + result[1]
    except socket.herror:
        return None


def DNSRequest(domain):
    """
    Resolve the DNS records for a given domain and print the results.
    """
    ips = []
    try:
        result = dns.resolver.resolve(domain)
        if result:
            print("Domain:", domain)
            for answer in result:
                print("Record Type:", dns.rdatatype.to_text(answer.rdtype))
                print("Record Value:", answer.to_text())
                ips.append(answer.to_text())
                print("Domain Names: %s" % ReverseDNS(answer.to_text()))
    except (dns.resolver.NXDOMAIN, dns.exception.Timeout):
        return []
    return ips


def SubdomainSearch(domain, dictionary, nums):
    """
    Search for subdomains of a given domain using a list of dictionary words and numeric suffixes.
    """
    successes = []
    for word in dictionary:
        subdomain = word + "." + domain
        # Perform DNS request for the subdomain
        ips = DNSRequest(subdomain)
        # Collect the IP addresses found for successful subdomains
        successes.extend(ips)
        if nums:
            for i in range(0, 10):
                s = word + str(i) + "." + domain
                # Perform DNS request for the subdomain with numeric suffix
                ips = DNSRequest(s)
                # Collect the IP addresses found for successful subdomains
                successes.extend(ips)


# Main block
domain = "google.com"
d = "subdomains.txt"
dictionary = []
with open(d, "r") as f:
    dictionary = f.read().splitlines()

SubdomainSearch(domain, dictionary, True)
