import tkinter as tk
from tkinter import simpledialog
from scapy.all import ARP, Ether, srp

def scan_network(ip_range):
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=False)[0]

    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    return devices

def get_ip_range():
    root = tk.Tk()
    root.withdraw()
    ip_range = simpledialog.askstring("IP Range", "Enter IP range to scan (e.g., 10.85.14.1 - 10.85.14.255):")
    return ip_range

def main():
    ip_range = get_ip_range()
    if ip_range:
        print(f"Scanning network for IP range: {ip_range}")
        devices = scan_network(ip_range)
        print("Network scan complete.\n")
        if devices:
            used_ips = set(device['ip'] for device in devices)
            all_ips = [f"{ip_range.split('.')[0]}.{ip_range.split('.')[1]}.{ip_range.split('.')[2]}.{i}" for i in range(1, 256)]
            free_ips = set(all_ips) - used_ips
            print("IPs in use:")
            for device in devices:
                print(f"IP: {device['ip']}, MAC: {device['mac']}")
            print("\nFree IPs:")
            for ip in free_ips:
                print(f"IP: {ip}")
        else:
            print("No devices found in the network.")
    else:
        print("Invalid IP range.")

if __name__ == "__main__":
    main()
