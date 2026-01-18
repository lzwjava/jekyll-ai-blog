import os
import subprocess
import time
import shutil
import argparse
import logging
import requests
import threading
import json
import urllib.parse

# Assuming speed.py is in the same directory or accessible in PYTHONPATH
from speed import get_top_proxies

# --- Configuration ---
CLASH_CONTROLLER_HOST = "127.0.0.1"
CLASH_CONTROLLER_PORT = 9090
CLASH_API_BASE_URL = f"http://{CLASH_CONTROLLER_HOST}:{CLASH_CONTROLLER_PORT}"
# The group proxy name to which the best individual proxy will be assigned.
# Make sure this group exists in your Clash configuration.
TARGET_PROXY_GROUP = "🚧Proxy"


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


def main():
    """Main function to manage Clash config, restart, and select best proxy."""
    setup_logging()

    parser = argparse.ArgumentParser(
        description="Clash configuration and management script."
    )
    parser.add_argument(
        "--minutes", type=int, default=20, help="Minutes between updates (default: 20)"
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=1000,
        help="Number of iterations (default: 1000)",
    )
    parser.add_argument(
        "--config-url",
        type=str,
        default=os.getenv("CLASH_DOWNLOAD_URL"),
        help="URL to download Clash configuration from. Defaults to CLASH_DOWNLOAD_URL environment variable if set, otherwise a hardcoded URL.",
    )
    parser.add_argument(
        "--clash-executable",
        type=str,
        default=os.getenv("CLASH_EXECUTABLE"),
        help="Path to the Clash executable. Defaults to CLASH_EXECUTABLE environment variable if set.",
    )
    args = parser.parse_args()

    ITERATIONS = args.iterations
    SLEEP_SECONDS = args.minutes * 60
    config_download_url = args.config_url
    clash_executable_path = args.clash_executable

    if not config_download_url:
        logging.critical(
            "Error: No configuration download URL provided. Please set CLASH_DOWNLOAD_URL environment variable or use --config-url argument."
        )
        return  # Exit if no URL is available

    if not clash_executable_path:
        logging.critical(
            "Error: No Clash executable path provided. Please set CLASH_EXECUTABLE environment variable or use --clash-executable argument."
        )
        return  # Exit if no executable path is available

    clash_config_dir = os.path.expanduser("~/.config/clash")
    clash_config_path = os.path.join(clash_config_dir, "config.yaml")

    for i in range(1, ITERATIONS + 1):
        logging.info(f"--- Starting Iteration {i} of {ITERATIONS} ---")

        # Step 1: Stop any existing system proxy settings
        stop_system_proxy()

        # Step 2: Download and update Clash config
        try:
            logging.info(f"Downloading new config from: {config_download_url}")
            subprocess.run(
                ["wget", config_download_url, "-O", "zhs4.yaml"],
                check=True,
                capture_output=True,
            )
            os.makedirs(clash_config_dir, exist_ok=True)
            shutil.move("zhs4.yaml", clash_config_path)
            logging.info("Clash config updated successfully!")
        except subprocess.CalledProcessError as e:
            logging.error(
                f"Failed to download or move config file: {e.stderr.decode().strip()}"
            )
            logging.error("Skipping to next iteration.")
            time.sleep(10)  # Wait a bit before retrying
            continue
        except Exception as e:
            logging.error(f"An unexpected error occurred during config update: {e}")
            logging.error("Skipping to next iteration.")
            time.sleep(10)
            continue

        # Step 3: Start Clash in the background
        clash_process = None
        try:
            # Start Clash and redirect its output to a logging function instead of a file
            def log_clash_output(pipe, level=logging.INFO):
                for line in iter(pipe.readline, b""):
                    logging.log(
                        level, f"[Clash] {line.decode(errors='replace').rstrip()}"
                    )
                pipe.close()

            clash_process = subprocess.Popen(
                [clash_executable_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            logging.info(f"Clash started with PID {clash_process.pid}")

            # Start threads to capture and log stdout and stderr
            threading.Thread(
                target=log_clash_output,
                args=(clash_process.stdout, logging.INFO),
                daemon=True,
            ).start()
            threading.Thread(
                target=log_clash_output,
                args=(clash_process.stderr, logging.ERROR),
                daemon=True,
            ).start()

            # Give Clash a moment to fully initialize and open its API port
            time.sleep(5)
        except FileNotFoundError:
            logging.critical(f"Clash executable not found at: {clash_executable_path}")
            logging.critical(
                "Please ensure the path is correct and Clash is installed."
            )
            return  # Critical error, exit script
        except Exception as e:
            logging.error(f"Failed to start Clash: {e}")
            logging.error("Skipping to next iteration.")
            if clash_process:
                clash_process.terminate()
            time.sleep(10)
            continue

        # Step 4: Test proxy speeds and select the best one
        best_proxy_name = None
        try:
            # Only select SG and TW proxies
            name_filter = ["SG", "TW"]
            filter_desc = "SG/TW"

            logging.info("Testing proxy speeds to find the best one...")
            top_proxies = get_top_proxies(num_results=20, name_filter=name_filter)  # Get top 20 proxies matching filter
            if top_proxies:
                # All top_proxies already match the filter, take the fastest one
                best_proxy_name = top_proxies[0]["name"]
                logging.info(
                    f"Selected proxy '{best_proxy_name}' (contains {filter_desc}) with latency {top_proxies[0]['latency']}ms"
                )
            else:
                logging.warning(
                    f"No successful proxy tests for {filter_desc} proxies. Cannot select a best proxy for this iteration."
                )
        except Exception as e:
            logging.error(f"Error during proxy speed testing: {e}")

        # Step 5: Switch Clash's proxy group to the best proxy (if found)
        if best_proxy_name:
            # Before setting system proxy, ensure Clash is set up correctly.
            # Set the system-wide proxy to point to Clash's local HTTP proxy.
            # Clash typically runs its HTTP proxy on port 7890 (or similar, check your config).
            clash_local_proxy_address = f"{CLASH_CONTROLLER_HOST}:7890"  # Adjust if your Clash HTTP port is different
            start_system_proxy(clash_local_proxy_address)

            if not switch_clash_proxy_group(TARGET_PROXY_GROUP, best_proxy_name):
                logging.error(
                    f"Failed to switch Clash group '{TARGET_PROXY_GROUP}' to '{best_proxy_name}'."
                )
        else:
            logging.warning(
                "No best proxy found, skipping proxy group switch and system proxy setup for this iteration."
            )

        # Step 6: Wait for the specified duration
        logging.info(
            f"Waiting for {SLEEP_SECONDS / 60} minutes before next iteration..."
        )
        time.sleep(SLEEP_SECONDS)

        # Step 7: Stop Clash process
        if clash_process:
            logging.info("Terminating Clash process...")
            clash_process.terminate()
            try:
                clash_process.wait(
                    timeout=10
                )  # Give Clash a bit more time to shut down gracefully
                logging.info("Clash stopped successfully.")
            except subprocess.TimeoutExpired:
                logging.warning("Clash did not terminate gracefully, killing process.")
                clash_process.kill()
                clash_process.wait()  # Ensure process is fully killed
            except Exception as e:
                logging.error(f"Error while waiting for Clash to stop: {e}")

        logging.info(f"--- Iteration {i} completed ---")

    logging.info(f"Completed {ITERATIONS} iterations. Script finished.")


if __name__ == "__main__":
    main()
