import time
import logging
import random
from urllib.parse import urljoin, urlparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException,
    NoSuchElementException,
    InvalidArgumentException,
)
from selenium.webdriver.common.by import By

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# List of User-Agents to rotate (if needed)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/115.0.0.0 Safari/537.36",
    # Add more User-Agent strings as needed
]


class SeleniumCrawler:
    def __init__(self, base_url, max_depth=3, delay=1.0, driver_path=None):
        self.base_url = self.normalize_url(base_url)
        self.domain = urlparse(self.base_url).netloc
        self.visited = set()
        self.broken_links = set()
        self.max_depth = max_depth
        self.delay = delay  # Base delay between requests in seconds

        # Initialize Selenium WebDriver with headless Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Rotate User-Agent if desired
        # Uncomment the following lines to rotate User-Agent
        # user_agent = random.choice(USER_AGENTS)
        # chrome_options.add_argument(f'user-agent={user_agent}')

        try:
            if driver_path:
                self.driver = webdriver.Chrome(
                    options=chrome_options, executable_path=driver_path
                )
            else:
                # Assumes chromedriver is in PATH
                self.driver = webdriver.Chrome(options=chrome_options)
        except WebDriverException as e:
            logging.error(f"Failed to initialize WebDriver: {e}")
            raise e

        # Set implicit wait
        self.driver.implicitly_wait(10)

    def normalize_url(self, url):
        """
        Normalize the URL by ensuring it has a scheme and removing fragments.
        """
        parsed = urlparse(url)
        if not parsed.scheme:
            url = "http://" + url
            parsed = urlparse(url)
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        return normalized.rstrip("/")

    def is_valid(self, url):
        """
        Check if the URL is valid and belongs to the same domain.
        """
        parsed = urlparse(url)
        return (parsed.scheme in ["http", "https"]) and (parsed.netloc == self.domain)

    def get_links(self, url):
        """
        Use Selenium to fetch the page and extract all internal links.
        """
        try:
            logging.info(f"Accessing: {url}")
            self.driver.get(url)
            # Randomized delay
            time.sleep(random.uniform(self.delay, self.delay + 1))

            # Extract all <a> elements with href attribute
            links = set()
            anchor_elements = self.driver.find_elements(By.TAG_NAME, "a")
            for element in anchor_elements:
                href = element.get_attribute("href")
                if href:
                    href = href.strip()
                    if (
                        href.startswith("mailto:")
                        or href.startswith("tel:")
                        or href.startswith("javascript:")
                    ):
                        continue  # Skip non-HTTP links
                    absolute_url = urljoin(url, href)
                    absolute_url = absolute_url.split("#")[0]  # Remove URL fragments
                    absolute_url = absolute_url.rstrip("/")
                    if self.is_valid(absolute_url):
                        links.add(absolute_url)
            return list(links)
        except (WebDriverException, TimeoutException, InvalidArgumentException) as e:
            logging.error(f"Error accessing {url}: {e}")
            return []

    def check_link(self, url):
        """
        Check if the link is broken by attempting to access it.
        """
        try:
            logging.info(f"Checking link: {url}")
            self.driver.get(url)
            # Randomized delay
            time.sleep(random.uniform(self.delay, self.delay + 1))

            # Simple check: look for "404" in the title or body
            page_title = self.driver.title.lower()
            page_body = self.driver.find_element(By.TAG_NAME, "body").text.lower()

            if "404" in page_title or "not found" in page_body:
                logging.warning(f"[404] Broken link found: {url}")
                self.broken_links.add(url)
        except (WebDriverException, TimeoutException, NoSuchElementException) as e:
            logging.error(f"Error checking link {url}: {e}")
            self.broken_links.add(url)

    def crawl(self, url, depth=0):
        """
        Recursively crawl the website up to a specified depth.
        """
        if depth > self.max_depth:
            return
        if url in self.visited:
            return
        self.visited.add(url)
        logging.info(f"Crawling: {url} (Depth: {depth})")
        links = self.get_links(url)
        for link in links:
            if link in self.visited:
                continue
            self.check_link(link)
            self.crawl(link, depth + 1)

    def start_crawl(self):
        try:
            self.crawl(self.base_url, depth=0)
        finally:
            self.driver.quit()
