import scapy.all as scapy
import subprocess

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def get_network_ips(network):
    ips = []
    try:
        output = subprocess.check_output(["arping", "-c", "1", "-I", network, "-D"])
        output = output.decode("utf-8")
        lines = output.split("\n")
        for line in lines:
            if "reply from" in line:
                ip = line.split(" ")[4]
                ips.append(ip)
    except Exception as e:
        print("Erro ao obter IPs:", e)
    return ips

def main():
    network = "192.168.1.0/24"  # Substitua pela sua rede
    ips_available = get_network_ips(network)
    print("IPs disponíveis na rede:")
    for ip in ips_available:
        print(ip)

    print("\nVerificando IPs ocupados:")
    for ip in ips_available:
        client_list = scan(ip)
        if client_list:
            for client in client_list:
                print("IP:", client["ip"], " MAC:", client["mac"])

if __name__ == "__main__":
    main()
