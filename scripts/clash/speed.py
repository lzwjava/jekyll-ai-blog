import requests
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging  # Import the logging module

# --- Configuration ---
CLASH_CONTROLLER_HOST = (
    "127.0.0.1"  # Use 127.0.0.1 as the controller is on the same machine
)
CLASH_CONTROLLER_PORT = 9090
CLASH_API_BASE_URL = f"http://{CLASH_CONTROLLER_HOST}:{CLASH_CONTROLLER_PORT}"
LATENCY_TEST_URL = "https://www.youtube.com"  # Updated test URL
LATENCY_TEST_TIMEOUT_MS = 2000  # Milliseconds
CONCURRENT_CONNECTIONS = 5  # Number of concurrent tests

# List of known group proxy names to exclude from speed testing
# These are typically not individual nodes but rather policy groups or special proxies.
EXCLUDE_PROXY_GROUPS = [
    "DIRECT",
    "REJECT",
    "GLOBAL",  # Already excluded by default in the API
    "🇨🇳国内网站或资源",
    "🌵其它规则外",
    "🎬Netflix等国外流媒体",
    "📦ChatGPT",
    "📹Youtube",
    "📺爱奇艺等国内流媒体",
    "🚧Proxy",
    # Add any other group names you want to exclude here
]

# --- Logging Setup for speed.py ---
# Configure logging for this specific script
# This ensures that when speed.py is imported and its functions are called,
# its output goes to speed.log, separate from clash_manager.log.
logging.basicConfig(
    filename="clash.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
# Optionally, if you also want to see output in the console, add a StreamHandler:
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# console_handler.setFormatter(formatter)
# logging.getLogger().addHandler(console_handler)

# --- Script Logic ---


def get_all_proxy_names():
    """Fetches all proxy names from the Clash API, excluding known groups."""
    try:
        response = requests.get(f"{CLASH_API_BASE_URL}/proxies", timeout=5)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        proxies_data = response.json()

        all_names = proxies_data.get("proxies", {}).keys()

        # Filter out the group names
        filtered_names = [
            name for name in all_names if name not in EXCLUDE_PROXY_GROUPS
        ]

        logging.info(
            f"Successfully fetched {len(filtered_names)} testable proxy names."
        )
        return filtered_names
    except requests.exceptions.ConnectionError:
        logging.error(
            f"Could not connect to Clash API at {CLASH_API_BASE_URL}. Ensure Clash is running."
        )
        return []
    except requests.exceptions.Timeout:
        logging.error("Connection to Clash API timed out after 5 seconds.")
        return []
    except requests.exceptions.RequestException as e:
        logging.error(f"An unexpected error occurred while fetching proxy names: {e}")
        return []


def test_proxy_latency(proxy_name):
    """Tests the latency of a single proxy using the Clash API.
    Returns a tuple (proxy_name, latency) or (proxy_name, None) on failure.
    """
    encoded_proxy_name = urllib.parse.quote(proxy_name)
    url = f"{CLASH_API_BASE_URL}/proxies/{encoded_proxy_name}/delay"
    params = {"url": LATENCY_TEST_URL, "timeout": LATENCY_TEST_TIMEOUT_MS}
    try:
        # requests timeout is in seconds, convert milliseconds
        response = requests.get(
            url, params=params, timeout=(LATENCY_TEST_TIMEOUT_MS / 1000) + 1
        )
        response.raise_for_status()
        latency_data = response.json()
        latency = latency_data.get("delay")
        logging.info(f"Proxy: {proxy_name} - Latency: {latency}ms")
        return proxy_name, latency
    except requests.exceptions.RequestException as e:
        logging.warning(f"Error testing '{proxy_name}': {e}")
        return proxy_name, None


def get_top_proxies(num_results=5, name_filter=None):
    """
    Tests Clash proxy speeds concurrently and returns the top N fastest individual proxies.

    Args:
        num_results (int): Number of top proxies to return (default: 5)
        name_filter (list): List of strings to filter proxy names. Only proxies containing
                           any of these strings in their name will be tested.

    Returns:
        list: A list of dictionaries, each containing 'name' and 'latency' for the top proxies.
              Returns an empty list if no testable proxies are found or an error occurs.
    """
    logging.info(
        "Starting Clash proxy speed test via External Controller API (concurrently)..."
    )
    logging.info(f"Using test URL: {LATENCY_TEST_URL}")
    logging.info(
        f"Running {CONCURRENT_CONNECTIONS} tests at a time. This might take a moment..."
    )

    proxy_names_to_test = get_all_proxy_names()
    if not proxy_names_to_test:
        logging.warning(
            "No testable proxies found or an error occurred during proxy name retrieval."
        )
        return []

    # Filter proxies by name if name_filter is provided
    if name_filter:
        filtered_names = [
            name
            for name in proxy_names_to_test
            if any(keyword in name for keyword in name_filter)
        ]
        logging.info(f"Filtering for proxies containing: {name_filter}")
        logging.info(
            f"Before filtering: {len(proxy_names_to_test)} proxies, after filtering: {len(filtered_names)} proxies"
        )
        proxy_names_to_test = filtered_names
        if not proxy_names_to_test:
            logging.warning(
                f"No proxies found matching the filter criteria: {name_filter}"
            )
            return []

    logging.info(f"Found {len(proxy_names_to_test)} individual proxies to test.")

    proxy_latencies = {}

    with ThreadPoolExecutor(max_workers=CONCURRENT_CONNECTIONS) as executor:
        future_to_proxy = {
            executor.submit(test_proxy_latency, name): name
            for name in proxy_names_to_test
        }

        for future in as_completed(future_to_proxy):
            proxy_name = future_to_proxy[future]
            try:
                name, latency = future.result()
                if latency is not None:
                    proxy_latencies[name] = latency
                else:
                    logging.info(
                        f"Proxy: {name} - Test Failed or Timed Out (details in warning logs)"
                    )
            except Exception as exc:
                logging.error(
                    f"Proxy {proxy_name} generated an unexpected exception during testing: {exc}"
                )

    sorted_proxies = sorted(
        [item for item in proxy_latencies.items() if item[1] is not None],
        key=lambda item: item[1],
    )

    top_proxies_list = []
    if not sorted_proxies:
        logging.warning("No successful individual proxy tests were completed.")
    else:
        logging.info(f"--- Top {num_results} Fastest Individual Proxies ---")
        for i, (name, latency) in enumerate(sorted_proxies[:num_results]):
            top_proxies_list.append({"name": name, "latency": latency})
            logging.info(f"  {i + 1}. {name}: {latency}ms")
        logging.info(f"Finished speed testing. Top {num_results} proxies identified.")

    return top_proxies_list


if __name__ == "__main__":
    # When speed.py is run directly, it will still output to speed.log
    # and print to console (if console_handler is uncommented).
    top_5_proxies = get_top_proxies(num_results=5)
    print("\nTop 5 proxies returned by function:", top_5_proxies)
