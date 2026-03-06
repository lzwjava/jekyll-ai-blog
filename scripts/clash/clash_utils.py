import os
import logging
import requests
import json
import urllib.parse

CLASH_CONTROLLER_HOST = "127.0.0.1"
CLASH_CONTROLLER_PORT = 9090
CLASH_API_BASE_URL = f"http://{CLASH_CONTROLLER_HOST}:{CLASH_CONTROLLER_PORT}"


def setup_logging():
    """Configures basic logging for the script. Clears previous log."""
    if os.path.exists("clash.log"):
        with open("clash.log", "w"):  # clears the log file
            pass
    logging.basicConfig(
        filename="clash.log",
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def start_system_proxy(global_proxy_address):
    """Sets system-wide proxy environment variables."""
    os.environ["GLOBAL_PROXY"] = (
        global_proxy_address  # Set for consistency if needed elsewhere
    )
    os.environ["HTTP_PROXY"] = f"http://{global_proxy_address}"
    os.environ["HTTPS_PROXY"] = f"http://{global_proxy_address}"
    os.environ["http_proxy"] = f"http://{global_proxy_address}"
    os.environ["https_proxy"] = f"http://{global_proxy_address}"
    # These typically don't need to be explicitly set to "false" with modern tools,
    # but keeping for compatibility with your original script's intent.
    os.environ["HTTP_PROXY_REQUEST_FULLURI"] = "false"
    os.environ["HTTPS_PROXY_REQUEST_FULLURI"] = "false"
    os.environ["ALL_PROXY"] = os.environ["http_proxy"]
    logging.info(f"System-wide proxy set to: {global_proxy_address}")


def stop_system_proxy():
    """Clears system-wide proxy environment variables."""
    os.environ["http_proxy"] = ""
    os.environ["HTTP_PROXY"] = ""
    os.environ["https_proxy"] = ""
    os.environ["HTTPS_PROXY"] = ""
    os.environ["HTTP_PROXY_REQUEST_FULLURI"] = "true"  # Revert to default
    os.environ["HTTPS_PROXY_REQUEST_FULLURI"] = "true"
    os.environ["ALL_PROXY"] = ""
    logging.info("System-wide proxy stopped (environment variables cleared).")


def switch_clash_proxy_group(group_name, proxy_name):
    """
    Switches the active proxy in a specified Clash proxy group to a new proxy.
    """
    encoded_group_name = urllib.parse.quote(group_name)
    url = f"{CLASH_API_BASE_URL}/proxies/{encoded_group_name}"
    headers = {"Content-Type": "application/json"}
    payload = {"name": proxy_name}

    try:
        response = requests.put(
            url, headers=headers, data=json.dumps(payload), timeout=5
        )
        response.raise_for_status()
        logging.info(f"Successfully switched '{group_name}' to '{proxy_name}'.")
        return True
    except requests.exceptions.ConnectionError:
        logging.error(
            f"Error: Could not connect to Clash API at {CLASH_API_BASE_URL} to switch proxy."
        )
        logging.error(
            "Ensure Clash is running and its external-controller is configured."
        )
        return False
    except requests.exceptions.Timeout:
        logging.error(
            f"Error: Connection to Clash API timed out while switching proxy for '{group_name}'."
        )
        return False
    except requests.exceptions.RequestException as e:
        logging.error(
            f"An unexpected error occurred while switching proxy for '{group_name}': {e}"
        )
        return False
