import subprocess
import argparse


def get_connected_network_interfaces():
    try:
        result = subprocess.run(
            ["networksetup", "-listallnetworkservices"],
            capture_output=True,
            text=True,
            check=True,
        )
        services = result.stdout.splitlines()
        connected_interfaces = []
        for service in services:
            service = service.strip()
            if service and ("Wi-Fi" in service or "USB 10/100 LAN" in service):
                # Verify if the interface is active
                status = subprocess.run(
                    ["networksetup", "-getinfo", service],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                lines = status.stdout.splitlines()
                ip_address = None
                for line in lines:
                    if line.startswith("IP address:"):
                        ip_address = line.split(":", 1)[1].strip().lower()
                        break
                if (
                    ip_address
                    and ip_address != "none"
                    and ip_address != "0.0.0.0"
                    and ip_address != ""
                ):
                    connected_interfaces.append(service)
        return connected_interfaces
    except subprocess.CalledProcessError as e:
        print(f"Error getting network interfaces: {e}")
        return []


def set_proxy(interface, proxy_host, proxy_port):
    try:
        subprocess.run(
            ["networksetup", "-setwebproxy", interface, proxy_host, str(proxy_port)],
            check=True,
        )
        subprocess.run(
            [
                "networksetup",
                "-setsecurewebproxy",
                interface,
                proxy_host,
                str(proxy_port),
            ],
            check=True,
        )
        subprocess.run(
            [
                "networksetup",
                "-setsocksfirewallproxy",
                interface,
                proxy_host,
                str(proxy_port + 1),  # SOCKS proxy port is typically 7891 (7890 + 1)
            ],
            check=True,
        )
        print(
            f"Successfully set HTTP, HTTPS, and SOCKS proxies to {proxy_host}:{proxy_port} and {proxy_host}:{proxy_port + 1} for {interface}"
        )
    except subprocess.CalledProcessError as e:
        print(f"Error setting proxy for {interface}: {e}")


def unset_proxy(interface):
    try:
        subprocess.run(
            ["networksetup", "-setwebproxystate", interface, "off"], check=True
        )
        subprocess.run(
            ["networksetup", "-setsecurewebproxystate", interface, "off"], check=True
        )
        subprocess.run(
            ["networksetup", "-setsocksfirewallproxystate", interface, "off"],
            check=True,
        )
        print(f"Successfully unset HTTP, HTTPS, and SOCKS proxies for {interface}")
    except subprocess.CalledProcessError as e:
        print(f"Error unsetting proxy for {interface}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Manage HTTP and HTTPS proxy settings for Wi-Fi or USB Ethernet on macOS"
    )
    parser.add_argument(
        "action", choices=["set", "unset"], help="Action to perform: set or unset proxy"
    )
    args = parser.parse_args()

    proxy_host = "127.0.0.1"
    proxy_port = 7890

    connected_interfaces = get_connected_network_interfaces()

    if not connected_interfaces:
        print(
            "No active Wi-Fi or USB Ethernet interface found. Please ensure a network is connected."
        )
        return

    for interface in connected_interfaces:
        print(f"Processing active network interface: {interface}")
        if args.action == "set":
            set_proxy(interface, proxy_host, proxy_port)
        else:
            unset_proxy(interface)


if __name__ == "__main__":
    main()
