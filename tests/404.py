import requests
from bs4 import BeautifulSoup
import logging
import concurrent.futures
from urllib.parse import urljoin
import argparse

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

BASE_URL = "http://127.0.0.1:4000"
VISITED_URLS = set()
MAX_THREADS = 10  # You can adjust the number of threads
IGNORE_HASH_TAG = False


def is_local_url(url):
    return url.startswith(BASE_URL) or url.startswith("/")


def is_hashtag_link(url):
    return "#" in url


def get_all_local_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        links = []
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            absolute_url = urljoin(url, href)
            if is_local_url(absolute_url) and (
                not IGNORE_HASH_TAG or not is_hashtag_link(absolute_url)
            ):
                links.append(absolute_url)
        return links
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return []


def check_404(url):
    if url in VISITED_URLS:
        return
    VISITED_URLS.add(url)
    try:
        response = requests.get(url)
        if response.status_code == 404:
            logging.warning(f"404 detected at: {url}")
        elif response.status_code >= 400:
            logging.error(f"Error {response.status_code} at: {url}")
        else:
            logging.info(f"OK {response.status_code} at: {url}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error accessing {url}: {e}")


def crawl(url):
    links = get_all_local_links(url)
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(process_link, links)


def process_link(link):
    if link not in VISITED_URLS:
        check_404(link)
        crawl(link)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check for 404 errors on a website.")
    parser.add_argument(
        "--ignore-hash-tag", action="store_true", help="Ignore links with hash tags."
    )
    args = parser.parse_args()
    IGNORE_HASH_TAG = args.ignore_hash_tag

    logging.info(f"Starting crawl at {BASE_URL}")
    check_404(BASE_URL)
    crawl(BASE_URL)
    logging.info("Finished crawling.")
