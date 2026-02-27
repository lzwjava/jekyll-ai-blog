import socket
import os
import argparse
import json
import requests
import time


def get_digitalocean_headers():
    api_key = os.environ.get("DO_API_KEY")
    if not api_key:
        print("Error: DO_API_KEY not found in environment variables.")
        return None
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def fetch_reserved_ips():
    headers = get_digitalocean_headers()
    if not headers:
        return None
    try:
        url = "https://api.digitalocean.com/v2/reserved_ips"
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        reserved_ips_data = resp.json().get("reserved_ips", [])
        with open("response.json", "w") as f:
            json.dump(reserved_ips_data, f, indent=4)
        return reserved_ips_data
    except Exception as e:
        print(f"Error getting reserved IP address: {e}")
        return None


def unassign_ip_from_droplet(ip_address, droplet_id, droplet_name):
    headers = get_digitalocean_headers()
    if not headers:
        return False

    try:
        url = f"https://api.digitalocean.com/v2/reserved_ips/{ip_address}"
        resp = requests.delete(url, headers=headers)
        resp.raise_for_status()
        print(f"Successfully deleted IP {ip_address} from droplet {droplet_name}")
        return True
    except Exception as e:
        print(f"Error deleting IP {ip_address} from droplet {droplet_name}: {e}")
        return False


def assign_ip_to_droplet(ip_address, droplet_id, droplet_name):
    headers = get_digitalocean_headers()
    if not headers:
        return False

    try:
        url = f"https://api.digitalocean.com/v2/reserved_ips/{ip_address}/actions"
        req = {"type": "assign", "droplet_id": droplet_id}
        resp = requests.post(url, headers=headers, json=req)
        resp.raise_for_status()
        print(f"Successfully assigned IP {ip_address} to droplet {droplet_name}")
        return True
    except Exception as e:
        print(f"Error assigning IP {ip_address} to droplet {droplet_name}: {e}")
        return False


def process_reserved_ips(reserved_ips, droplet_name, only_check=False):
    if not reserved_ips:
        print("No reserved IPs found in your account.")
        return None

    for reserved_ip in reserved_ips:
        ip_address = reserved_ip.get("ip")
        if not ip_address:
            print("No IP address found for a reserved IP.")
            continue

        if droplet_name:
            droplet = reserved_ip.get("droplet", None)
            if droplet:
                if droplet.get("name") == droplet_name:
                    print(
                        f"The reserved IP {ip_address} is assigned to droplet: {droplet_name}"
                    )
                    if only_check:
                        if check_port_80(ip_address):
                            print(
                                f"Port 80 is open on {ip_address} for droplet {droplet_name}"
                            )
                        else:
                            print(
                                f"Port 80 is closed on {ip_address} for droplet {droplet_name}"
                            )
                        return ip_address
                    droplet_id = droplet.get("id")
                    if droplet_id:
                        if unassign_ip_from_droplet(
                            ip_address, droplet_id, droplet_name
                        ):
                            # Attempt to assign a new IP after unassigning

                            new_ip = create_new_reserved_ip(droplet_id)
                            if new_ip:
                                print(
                                    "Sleeping for 10 seconds before assigning new IP..."
                                )
                                time.sleep(10)
                                if assign_ip_to_droplet(
                                    new_ip, droplet_id, droplet_name
                                ):
                                    print(
                                        f"Successfully assigned new IP {new_ip} to droplet {droplet_name}"
                                    )
                                else:
                                    print(
                                        f"Failed to reassign new IP {new_ip} to droplet {droplet_name}"
                                    )
                            else:
                                print("No available IP to assign")

                    else:
                        print(
                            f"Could not unassign IP {ip_address} because droplet ID was not found."
                        )
                    return None
                else:
                    print(
                        f"The reserved IP {ip_address} is not assigned to droplet: {droplet_name}"
                    )
            else:
                print(f"No droplets are assigned to the reserved IP: {ip_address}")
        else:
            return ip_address
    return None


def create_new_reserved_ip(droplet_id):
    headers = get_digitalocean_headers()
    if not headers:
        print("Failed to get DigitalOcean headers.")
        return False
    try:
        url = "https://api.digitalocean.com/v2/reserved_ips"
        req = {
            "region": "sgp1",
        }
        print(f"Attempting to create a new reserved IP for droplet ID: {droplet_id}")
        resp = requests.post(url, headers=headers, json=req)
        resp.raise_for_status()
        new_ip = resp.json().get("reserved_ip", {}).get("ip")
        print(f"Successfully created new reserved IP: {new_ip}")
        return new_ip
    except Exception as e:
        print(f"Error creating new reserved IP: {e}")
        return False


def check_port_80(ip_address):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((ip_address, 80))
            return True
    except Exception:
        return False


def get_reserved_ip(droplet_name=None, only_check=False):
    reserved_ips = fetch_reserved_ips()
    if reserved_ips is None:
        return None
    return process_reserved_ips(reserved_ips, droplet_name, only_check)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get DigitalOcean reserved IP address."
    )
    parser.add_argument(
        "--droplet-name",
        required=True,
        help="Name of the droplet to check if the reserved IP is assigned to.",
    )
    parser.add_argument(
        "--only-check",
        action="store_true",
        help="Only check if the IP is assigned to the droplet, do not reassign.",
    )
    args = parser.parse_args()

    reserved_ip = get_reserved_ip(args.droplet_name, args.only_check)
    if reserved_ip:
        print(f"The reserved IP address is: {reserved_ip}")
