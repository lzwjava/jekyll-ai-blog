import socket
import argparse
import threading

MAX_THREADS = 50  # Maximum number of threads to use


def is_port_open(host, port):
    """
    Checks if a port is open on the given host.
    Returns True if the port is open, False otherwise.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            return True
        else:
            return False
    except socket.error as e:
        return False
    finally:
        sock.close()


def scan_port(host, port, open_ports):
    """
    Scans a single port and records if it's open.
    """
    if is_port_open(host, port):
        print(f"Port {port} is open")
        open_ports.append(port)
    else:
        print(f"Port {port} is closed")


def scan_ports(host, start_port, end_port):
    """
    Scans a range of ports on the given host using threads.
    """
    print(f"Scanning ports {start_port}-{end_port} on {host}")
    threads = []
    semaphore = threading.Semaphore(MAX_THREADS)
    open_ports = []

    def scan_port_with_semaphore(port):
        semaphore.acquire()
        try:
            scan_port(host, port, open_ports)
        finally:
            semaphore.release()

    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port_with_semaphore, args=(port,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return open_ports


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan ports on a host.")
    parser.add_argument("host", help="The IP address or hostname to scan")
    parser.add_argument(
        "port_range",
        nargs="?",
        default="1-10000",
        help="The port range to scan (e.g., 1-1024, default: 1-10000)",
    )
    args = parser.parse_args()

    try:
        start_port, end_port = map(int, args.port_range.split("-"))
        if start_port > end_port or start_port < 1 or end_port > 65535:
            print("Invalid port range. Ports must be between 1-65535 and start <= end.")
            exit(1)
    except ValueError:
        print("Invalid port range format. Use format: start-end (e.g., 1-1024)")
        exit(1)

    open_ports = scan_ports(args.host, start_port, end_port)

    print("\nOpen ports:")
    if open_ports:
        for port in sorted(open_ports):
            print(port)
    else:
        print("None found")
