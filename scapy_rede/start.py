from scapy.all import ARP, Ether, srp
import ipaddress
import csv

def scan_network(ip_range):
    arp = ARP(pdst=str(ip_range))
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices

def find_free_ips(all_ips, used_ips):
    free_ips = []
    for ip in all_ips:
        if ip not in used_ips:
            free_ips.append(ip)
    return free_ips

def save_to_csv(free_ips, filename='free_ips.csv'):
    with open(filename, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(["IP Address"])
        for ip in free_ips:
            csv_writer.writerow([ip])

def main():
    # Solicitar informações da rede
    subnet_mask = input("Digite a máscara de sub-rede (ex: 255.255.255.0): ")
    gateway = input("Digite o gateway")
