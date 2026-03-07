import requests
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# --- Configuration ---
CLASH_CONTROLLER_HOST = "127.0.0.1"
CLASH_CONTROLLER_PORT = 9090
CLASH_API_BASE_URL = f"http://{CLASH_CONTROLLER_HOST}:{CLASH_CONTROLLER_PORT}"

# Top 10 popular websites (as of a general estimate, adjust as needed)
TOP_WEBSITE_LIST = [
    "https://www.google.com",
    "https://www.youtube.com",
    "https://www.twitter.com",
    "https://github.com",
    "https://www.reddit.com",
    "https://grok.com",
]

LATENCY_TEST_TIMEOUT_MS = 5000  # Increased timeout for slower tests
CONCURRENT_CONNECTIONS = 5  # Reduced concurrent connections for stability

EXCLUDE_PROXY_GROUPS = [
    "DIRECT",
    "REJECT",
    "GLOBAL",
    "🇨🇳国内网站或资源",
    "🌵其它规则外",
    "🎬Netflix等国外流媒体",
    "📦ChatGPT",
    "📹Youtube",
    "📺爱奇艺等国内流媒体",
    "🚧Proxy",
]

# --- Logging Setup ---
logging.basicConfig(
    filename="clash.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def get_all_proxy_names():
    try:
        response = requests.get(f"{CLASH_API_BASE_URL}/proxies", timeout=5)
        response.raise_for_status()
        proxies_data = response.json()
        all_names = proxies_data.get("proxies", {}).keys()
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


def test_proxy_latency(proxy_name, test_url):
    encoded_proxy_name = urllib.parse.quote(proxy_name)
    url = f"{CLASH_API_BASE_URL}/proxies/{encoded_proxy_name}/delay"
    params = {"url": test_url, "timeout": LATENCY_TEST_TIMEOUT_MS}
    try:
        response = requests.get(
            url, params=params, timeout=(LATENCY_TEST_TIMEOUT_MS / 1000) + 1
        )
        response.raise_for_status()
        latency_data = response.json()
        latency = latency_data.get("delay")
        logging.info(f"Proxy: {proxy_name} - Latency to {test_url}: {latency}ms")
        return proxy_name, test_url, latency
    except requests.exceptions.RequestException as e:
        logging.warning(f"Error testing '{proxy_name}' to {test_url}: {e}")
        return proxy_name, test_url, None


def get_average_latency(proxy_name):
    total_latency = 0
    successful_tests = 0
    for test_url in TOP_WEBSITE_LIST:
        proxy_name, test_url, latency = test_proxy_latency(proxy_name, test_url)
        if latency is not None:
            total_latency += latency
            successful_tests += 1
    if successful_tests > 0:
        return total_latency / successful_tests
    else:
        return None


def get_top_proxies(num_results=10):
    logging.info(
        "Starting Clash proxy speed test against top websites (concurrently)..."
    )
    logging.info(f"Testing against URLs: {TOP_WEBSITE_LIST}")
    logging.info(
        f"Running {CONCURRENT_CONNECTIONS} tests at a time. This might take a moment..."
    )

    proxy_names_to_test = get_all_proxy_names()
    if not proxy_names_to_test:
        logging.warning(
            "No testable proxies found or an error occurred during proxy name retrieval."
        )
        return []

    logging.info(f"Found {len(proxy_names_to_test)} individual proxies to test.")

    proxy_average_latencies = {}

    with ThreadPoolExecutor(max_workers=CONCURRENT_CONNECTIONS) as executor:
        future_to_proxy = {
            executor.submit(get_average_latency, name): name
            for name in proxy_names_to_test
        }

        for future in as_completed(future_to_proxy):
            proxy_name = future_to_proxy[future]
            try:
                average_latency = future.result()
                if average_latency is not None:
                    proxy_average_latencies[proxy_name] = average_latency
                else:
                    logging.info(
                        f"Proxy: {proxy_name} - Test Failed or Timed Out for all websites."
                    )
            except Exception as exc:
                logging.error(
                    f"Proxy {proxy_name} generated an unexpected exception during testing: {exc}"
                )

    sorted_proxies = sorted(
        [item for item in proxy_average_latencies.items() if item[1] is not None],
        key=lambda item: item[1],
    )

    top_proxies_list = []
    if not sorted_proxies:
        logging.warning("No successful individual proxy tests were completed.")
    else:
        logging.info(
            f"--- Top {num_results} Fastest Individual Proxies (Average Latency) ---"
        )
        for i, (name, latency) in enumerate(sorted_proxies[:num_results]):
            top_proxies_list.append({"name": name, "average_latency": latency})
            logging.info(f"  {i + 1}. {name}: {latency:.2f}ms")
        logging.info(f"Finished speed testing. Top {num_results} proxies identified.")

    return top_proxies_list


def generate_report(top_proxies):
    print("\n--- Clash Proxy Speed Test Report ---")
    if not top_proxies:
        print("No proxies were successfully tested.")
    else:
        print("Top Proxies (Fastest Average Latency):")
        for i, proxy in enumerate(top_proxies):
            print(f"  {i + 1}. {proxy['name']}: {proxy['average_latency']:.2f}ms")
    print("--- End of Report ---")


if __name__ == "__main__":
    top_proxies = get_top_proxies(num_results=10)
    generate_report(top_proxies)
