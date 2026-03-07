from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time
import os
from urllib.parse import urlencode


def scrape_weibo(url, end_time=None):
    try:
        all_weibo_data = []
        page = 1
        cookies = {}
        script_dir = os.path.dirname(os.path.abspath(__file__))
        cookies_file_path = os.path.join(script_dir, "weibo_cookies.txt")
        print(f"Checking for cookies file at: {cookies_file_path}")
        if os.path.exists(cookies_file_path):
            print("Cookies file found. Loading cookies...")
            with open(cookies_file_path, "r") as f:
                cookies_text = f.read()
                try:
                    cookies = json.loads(cookies_text)
                    print("Cookies loaded from JSON.")
                except json.JSONDecodeError:
                    print("Failed to load cookies from JSON. Parsing as string.")
                    cookies = {}
                    for item in cookies_text.strip().split(";"):
                        if "=" in item:
                            key, value = item.split("=", 1)
                            cookies[key.strip()] = value.strip()
        else:
            print("Cookies file not found.")
        print(f"Cookies: {cookies}")

        chrome_options = Options()
        # Stealth settings
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        chrome_options.add_argument(f"user-agent={user_agent}")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        if os.environ.get("HTTP_PROXY"):
            proxy = os.environ.get("HTTP_PROXY")
            chrome_options.add_argument(f"--proxy-server={proxy}")
            print(f"Using HTTP Proxy: {proxy}")
        if os.environ.get("HTTPS_PROXY"):
            proxy = os.environ.get("HTTPS_PROXY")
            chrome_options.add_argument(f"--proxy-server={proxy}")
            print(f"Using HTTPS Proxy: {proxy}")

        driver = webdriver.Chrome(options=chrome_options)

        if end_time:
            params = {
                "tabtype": "feed",
                "is_ori": 1,
                "is_text": 1,
                "is_pic": 1,
                "is_video": 1,
                "is_music": 1,
                "is_forward": 1,
                "end_time": end_time,
            }
            url = f"{url}?{urlencode(params)}"

        print(f"Navigating to: {url}")
        driver.get(url)

        # Debug: Save initial page
        with open("initial_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        # Add cookies with domain
        driver.get(url)  # Ensure we're on the domain before adding cookies
        for name, value in cookies.items():
            driver.add_cookie(
                {
                    "name": name,
                    "value": value,
                    "domain": ".weibo.com",  # Critical for cross-subdomain cookies
                    "path": "/",
                    "secure": False,
                }
            )
        print("Cookies added. Reloading page...")
        driver.refresh()  # Reload to apply cookies

        # Debug: Check post-login page
        with open("post_login_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        # Verify login success by checking page title or specific element
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div[class*="ProfileHeader_avatar"]')
                )
            )
            print("Login verified. Profile detected.")
        except Exception:
            print("Failed to confirm login. Proceeding with caution.")

        while True:
            print(f"Scraping page {page}...")

            try:
                # Wait longer for content
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div"))
                )
                print("Posts container loaded.")
            except Exception as e:
                print(f"Timeout waiting for posts: {e}")
                break

            html_content = driver.page_source
            print(html_content)
            soup = BeautifulSoup(html_content, "html.parser")

            posts = soup.find_all(
                "div", class_="card-wrap", attrs={"data-card": "mblog"}
            )

            if not posts:
                print("No posts found. Exiting.")
                break

            weibo_data = []
            for post in posts:
                text_content_div = post.find("div", class_="weibo-text")
                text_content = (
                    text_content_div.get_text(strip=True)
                    if text_content_div
                    else "No text"
                )

                images = [
                    img["src"]
                    for img in post.select("img.weibo-image")
                    if img.get("src")
                ]
                video = (
                    post.select_one("video source")["src"]
                    if post.select_one("video source")
                    else None
                )

                timestamp = (
                    post.find("a", class_="from").get_text(strip=True)
                    if post.find("a", class_="from")
                    else "Unknown time"
                )

                weibo_data.append(
                    {
                        "text": text_content,
                        "images": images,
                        "video": video,
                        "timestamp": timestamp,
                    }
                )

            all_weibo_data.extend(weibo_data)
            print(f"Page {page}: Captured {len(weibo_data)} posts")

            # Find next page button
            next_buttons = driver.find_elements(
                By.XPATH, "//a[contains(., '下一页') or contains(., 'Next')]"
            )
            if not next_buttons:
                print("No more pages.")
                break

            try:
                next_buttons[0].click()
                print("Navigating to next page...")
                time.sleep(3)  # Allow time for AJAX load
                # Wait for new content
                WebDriverWait(driver, 15).until(
                    EC.staleness_of(posts[0])  # Wait until old posts are removed
                )
            except Exception as e:
                print(f"Error navigating: {e}")
                break

            page += 1

        driver.quit()
        return all_weibo_data

    except Exception as e:
        print(f"Critical error: {str(e)}")
        if "driver" in locals():
            driver.quit()
        return None


def main():
    weibo_url = "https://weibo.com/u/6347862377"
    end_time = 1737561600
    data = scrape_weibo(weibo_url, end_time)

    if data:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print("Scraping failed.")


if __name__ == "__main__":
    main()
