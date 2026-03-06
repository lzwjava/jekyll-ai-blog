import os
import subprocess
import time
import shutil
import argparse
import logging
import threading
import yaml

# Assuming speed.py is in the same directory or accessible in PYTHONPATH
from speed import get_top_proxies

from clash_utils import (
    setup_logging,
    start_system_proxy,
    stop_system_proxy,
    switch_clash_proxy_group,
)


def main():
    """Main function to manage Clash config, restart, and select best proxy."""
    setup_logging()

    parser = argparse.ArgumentParser(
        description="Clash configuration and management script."
    )
    parser.add_argument(
        "--minutes", type=int, default=60, help="Minutes between updates (default: 60)"
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=1000,
        help="Number of iterations (default: 1000)",
    )
    parser.add_argument(
        "--clash-executable",
        type=str,
        default=os.getenv("CLASH_EXECUTABLE"),
        help="Path to the Clash executable. Defaults to CLASH_EXECUTABLE environment variable if set.",
    )
    parser.add_argument(
        "--type",
        type=str,
        default="zhs",
        choices=["zhs", "falemon"],
        help="Proxy provider type (default: zhs)",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="rule",
        choices=["rule", "global"],
        help="Mode: rule (standard groups) or global (GLOBAL group + DNS) (default: rule)",
    )
    parser.add_argument(
        "--not_stop_system_proxy",
        action="store_true",
        help="Do not stop existing system proxy settings at the beginning of each iteration",
    )
    parser.add_argument(
        "--config-file",
        type=str,
        help="Path to an existing config file. If provided, copies this file instead of downloading from URL",
    )
    args = parser.parse_args()

    if args.type == "zhs":
        env_var = "CLASH_DOWNLOAD_URL"
        temp_filename = "zhs4.yaml"
        target_proxy_group = "🚧Proxy"
    else:
        env_var = "CLASH_FALEMON_DOWNLOAD_URL"
        temp_filename = "falemon.yaml"
        target_proxy_group = "🚀 节点选择"

    if args.mode == "global":
        target_proxy_group = "GLOBAL"
    ITERATIONS = args.iterations
    SLEEP_SECONDS = args.minutes * 60
    config_download_url = os.getenv(env_var)
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

    # If config file is provided, validate it exists
    if args.config_file:
        if not os.path.exists(args.config_file):
            logging.critical(f"Error: Config file not found at: {args.config_file}")
            return

    for i in range(1, ITERATIONS + 1):
        logging.info(f"--- Starting Iteration {i} of {ITERATIONS} ---")

        # Step 1: Stop any existing system proxy settings (if not disabled)
        if not args.not_stop_system_proxy:
            stop_system_proxy()

        # Step 2: Download or copy Clash config
        try:
            if args.config_file:
                logging.info(f"Copying config from: {args.config_file}")
                os.makedirs(clash_config_dir, exist_ok=True)
                shutil.copy(args.config_file, clash_config_path)
            else:
                logging.info(f"Downloading new config from: {config_download_url}")
                subprocess.run(
                    ["wget", config_download_url, "-O", temp_filename],
                    check=True,
                    capture_output=True,
                )
                os.makedirs(clash_config_dir, exist_ok=True)
                shutil.move(temp_filename, clash_config_path)
            if args.mode == "global":
                with open(clash_config_path, "r") as f:
                    config = yaml.safe_load(f)
                config["mode"] = "Global"
                config["dns"] = {
                    "enable": True,
                    "ipv6": True,
                    "nameserver": [
                        "https://doh.pub/dns-query",
                        "https://dns.alidns.com/dns-query",
                    ],
                    "fallback": ["tls://223.5.5.5:853"],
                }
                with open(clash_config_path, "w") as f:
                    yaml.dump(config, f, default_flow_style=False, sort_keys=False)
                logging.info("Added DNS config for global mode.")
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
            # Set proxy name filter based on type
            if args.type == "zhs":
                name_filter = ["SG", "TW", "US", "UK", "JP"]
                filter_desc = "SG/TW/US/UK/JP"
            else:
                name_filter = [
                    "新加坡",
                    "台湾",
                    "日本",
                    "美国",
                    "印度",
                    "越南",
                    "加拿大",
                ]
                filter_desc = "SG/TW/JP/US/IN/VN/CA"

            logging.info("Testing proxy speeds to find the best one...")
            top_proxies = get_top_proxies(
                num_results=20, name_filter=name_filter
            )  # Get top 20 proxies matching filter
            if top_proxies:
                # All top_proxies already match the filter, take the fastest one
                best_proxy_name = top_proxies[0]["name"]
                logging.info(
                    f"Selected proxy '{best_proxy_name}' ({filter_desc}) with latency {top_proxies[0]['latency']}ms"
                )
            else:
                logging.warning(
                    f"No successful {filter_desc} proxy tests. Cannot select a best proxy for this iteration."
                )
        except Exception as e:
            logging.error(f"Error during proxy speed testing: {e}")

        # Step 5: Switch Clash's proxy group to the best proxy (if found)
        if best_proxy_name:
            # Before setting system proxy, ensure Clash is set up correctly.
            # Set the system-wide proxy to point to Clash's local HTTP proxy.
            # Clash typically runs its HTTP proxy on port 7890 (or similar, check your config).
            clash_local_proxy_address = "127.0.0.1:7890"  # Clash HTTP proxy port
            start_system_proxy(clash_local_proxy_address)

            if not switch_clash_proxy_group(target_proxy_group, best_proxy_name):
                logging.error(
                    f"Failed to switch Clash group '{target_proxy_group}' to '{best_proxy_name}'."
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
