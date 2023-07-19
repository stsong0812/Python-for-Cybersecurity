from scapy.all import *

# Ports to scan for the public DNS host (Cloudflare's public DNS)
ports = [53, 80, 443]

def SynScan(host):
    """
    Replicates a simple port scan by sending SYN packets to our host machine looking for open port connections from our ports list.
    Loops over our sent and recieved packets in our answered ports and verifies if we are got a response from the ports we sent
    the packets to.
    """
        
    # Sending SYN packets to the specified host and port list
    ans, unans = sr(IP(dst=host) / TCP(sport=5555, dport=ports, flags="S"), timeout=2, verbose=0)

    # Printing the open ports that received a response
    print("Open ports at %s:" % host)
    for (s, r,) in ans:
        if s[TCP].dport == r[TCP].sport:
            print(s[TCP].dport)

def DNSScan(host):
    """
    Replicates a DNS query to the specified host's DNS server and checks if it gets a response within the timeout period.
    If a response is received, it indicates that the host is running a DNS server.
    """

    # Sending a DNS query packet to the specified host's DNS server on port 53
    ans, unans = sr(IP(dst=host) / UDP(sport=5555, dport=53) / DNS(rd=1, qd=DNSQR(qname="cloudflare.com")), timeout=2, verbose=0)

    # If a response is received, the host is running a DNS server
    if ans:
        print("DNS Server at %s" % host)

# Cloudflare's public DNS IP address
host = "1.1.1.1"

# Perform a SYN scan on the specified host
SynScan(host)

# Perform a DNS scan on the specified host
DNSScan(host)
