from scapy.all import ARP, Ether, srp

def scan_network(ip):
    arp = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=False)[0]

    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    return devices

def main():
    ip = "10.85.14.170"  # Defina o IP a ser verificado
    print(f"Scanning network for IP: {ip}")
    devices = scan_network(ip)
    if devices:
        print("IPs in use:")
        for device in devices:
            print(f"IP: {device['ip']}, MAC: {device['mac']}")
    else:
        print("No devices found in the network.")

if __name__ == "__main__":
    main()
