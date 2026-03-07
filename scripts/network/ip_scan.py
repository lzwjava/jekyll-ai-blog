import subprocess
import ipaddress
import threading
import socket
import argparse

MAX_THREADS = 50  # Maximum number of threads to use


def is_host_up(host, port=None):
    """
    Checks if a host is up using ping or telnet.
    If port is specified, uses telnet to check if the port is open.
    Otherwise, uses ping.
    Returns True if the host is up, False otherwise.
    """
    if port:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            if result == 0:
                return True
            else:
                return False
        except socket.error:
            return False
        finally:
            sock.close()
    else:
        try:
            # -c 1: Send only 1 packet
            # -W 1: Wait 1 second for a response
            subprocess.check_output(["ping", "-c", "1", "-W", "1", host], timeout=1)
            return True
        except subprocess.CalledProcessError:
            return False
        except subprocess.TimeoutExpired:
            return False


def scan_ip(ip_str, up_ips, port=None):
    """
    Scans a single IP address and prints its status.
    """
    if is_host_up(ip_str, port):
        print(f"{ip_str} is up")
        up_ips.append(ip_str)
    else:
        print(f"{ip_str} is down")


def scan_network(network, port=None):
    """
    Scans a network for live hosts using threads, limiting the number of concurrent threads.
    """
    print(f"Scanning network: {network}")
    threads = []
    semaphore = threading.Semaphore(
        MAX_THREADS
    )  # Limit the number of concurrent threads
    up_ips = []

    def scan_ip_with_semaphore(ip_str):
        semaphore.acquire()
        try:
            scan_ip(ip_str, up_ips, port)
        finally:
            semaphore.release()

    for ip in ipaddress.IPv4Network(network):
        ip_str = str(ip)
        thread = threading.Thread(target=scan_ip_with_semaphore, args=(ip_str,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return up_ips


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan a network for live hosts.")
    parser.add_argument(
        "network",
        nargs="?",
        default="192.168.1.0/24",
        help="The network to scan (e.g., 192.168.1.0/24)",
    )
    parser.add_argument("-p", "--port", type=int, help="The port to check (optional)")
    args = parser.parse_args()

    network_to_scan = args.network
    port_to_scan = args.port

    up_ips = scan_network(network_to_scan, port_to_scan)
    print("\nLive IPs:")
    for ip in up_ips:
        print(ip)
