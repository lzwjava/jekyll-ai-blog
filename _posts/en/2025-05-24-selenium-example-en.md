---
audio: false
generated: true
lang: en
layout: post
title: Selenium Script
translated: false
type: note
---

Below is a sophisticated example of a Selenium script in Python that demonstrates advanced features, including the Page Object Model (POM), explicit FacetGrid for responsive layouts, explicit waits, handling dynamic content, and error handling. The script automates a complex scenario: scraping product data from an e-commerce website, navigating through multiple pages, and generating a summary report. The example assumes a hypothetical e-commerce website for demonstration purposes, but the concepts can be adapted to real websites.

This example showcases:
- **Page Object Model (POM)** for organized and maintainable code.
- **Explicit waits** for handling dynamic content.
- **FacetGrid** for responsive table handling.
- **Headless browser** for efficient execution.
- **Data processing** to generate a JSON report.
- **Error handling** for robustness.

```python
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import Select
import time

# Page Object for Product Listing Page
class ProductListingPage:
    def __init__(self, driver):
        self.driver = driver
        self.product_cards = (By.CLASS_NAME, "product-card")
        self.product_name = (By.CLASS_NAME, "product-name")
        self.product_price = (By.CLASS_NAME, "product-price")
        self.next_page_button = (By.ID, "next-page")
        self.sort_dropdown = (By.ID, "sort-options")

    def sort_by_price(self):
        try:
            sort_select = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.sort_dropdown)
            )
            select = Select(sort_select)
            select.select_by_value("price-asc")
            time.sleep(2)  # Allow sorting to apply
        except TimeoutException:
            print("Sort dropdown not found or timed out")

    def get_products(self):
        try:
            cards = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(self.product_cards)
            )
            products = []
            for card in cards:
                name = card.find_element(*self.product_name).text
                price = card.find_element(*self.product_price).text
                products.append({"name": name, "price": price})
            return products
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error retrieving products: {e}")
            return []

    def go_to_next_page(self):
        try:
            next_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.next_page_button)
            )
            next_button.click()
            time.sleep(2)  # Wait for page load
            return True
        except TimeoutException:
            print("No next page button found or timed out")
            return False

# Page Object for Search Page
class SearchPage:
    def __init__(self, driver):
        self.driver = driver
        self.search_input = (By.ID, "search-bar")
        self.search_button = (By.ID, "search-submit")

    def search(self, query):
        try:
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.search_input)
            )
            search_box.clear()
            search_box.send_keys(query)
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.search_button)
            ).click()
            time.sleep(2)  # Wait for search results
        except TimeoutException as e:
            print(f"Search failed: {e}")

# Main script
def scrape_ecommerce_site():
    # Set up headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    all_products = []

    try:
        # Navigate to the website
        driver.get("https://example.com")

        # Initialize page objects
        search_page = SearchPage(driver)
        product_page = ProductListingPage(driver)

        # Perform search
        search_page.search("laptop")

        # Sort by price
        product_page.sort_by_price()

        # Scrape multiple pages
        page_count = 0
        max_pages = 3  # Limit for demo

        while page_count < max_pages:
            products = product_page.get_products()
            all_products.extend(products)
            print(f"Scraped page {page_count + 1}: {len(products)} products")

            if not product_page.go_to_next_page():
                break
            page_count += 1

        # Generate summary
        summary = {
            "total_products": len(all_products),
            "average_price": calculate_average_price(all_products),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Save results to JSON
        with open("product_data.json", "w") as f:
            json.dump({"products": all_products, "summary": summary}, f, indent=2)
        print("Results saved to product_data.json")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

def calculate_average_price(products):
    if not products:
        return 0
    prices = []
    for product in products:
        try:
            price_str = product["price"].replace("$", "").replace(",", "")
            prices.append(float(price_str))
        except (ValueError, AttributeError):
            continue
    return sum(prices) / len(prices) if prices else 0

if __name__ == "__main__":
    scrape_ecommerce_site()
```

### Explanation of the Example
1. **Page Object Model (POM)**:
   - The script uses two page object classes (`SearchPage` and `ProductListingPage`) to encapsulate page-specific logic, making the code modular and maintainable.
   - Each class contains locators and methods for interacting with specific page elements.

2. **Headless Browser**:
   - The script runs Chrome in headless mode for efficiency, suitable for CI/CD pipelines or servers.

3. **Explicit Waits**:
   - `WebDriverWait` and `expected_conditions` are used to handle dynamic content, ensuring elements are present or clickable before interaction.

4. **Responsive Table Handling**:
   - The script uses FacetGrid-like logic to scrape a product listing table, extracting product names and prices from each card.
   - It handles pagination by navigating through multiple pages (up to a maximum of 3 for this example).

5. **Error Handling**:
   - The script catches `TimeoutException` and `NoSuchElementException` to handle missing elements or timeouts gracefully.
   - A `try-finally` block ensures the browser is closed even if an error occurs.

6. **Data Processing**:
   - Scraped data is stored in a list of dictionaries and summarized (e.g., total products, average price).
   - Results are saved to a JSON file (`product_data.json`) for further use.

7. **Dynamic Sorting**:
   - The script interacts with a dropdown to sort products by price, simulating real user behavior.

### Output
The script produces a JSON file (`product_data.json`) with the following structure:
```json
{
  "products": [
    {"name": "Laptop Model A", "price": "$999.99"},
    {"name": "Laptop Model B", "price": "$1299.99"},
    ...
  ],
  "summary": {
    "total_products": 30,
    "average_price": 1099.45,
    "timestamp": "2025-05-24 21:33:00"
  }
}
```

### Notes
- **Website Adaptation**: The locators (`By.ID`, `By.CLASS_NAME`) and URL (`https://example.com`) are placeholders. Replace them with actual values from the target website’s HTML structure, which you can inspect using browser developer tools.
- **Dependencies**: Ensure you have `selenium` installed (`pip install selenium`) and the appropriate browser driver (e.g., ChromeDriver) in your PATH.
- **Improvements**:
  - Add logging for better debugging.
  - Implement retry logic for flaky network requests.
  - Use a configuration file for locators and settings.
  - Extend to handle more complex scenarios like authentication or CAPTCHA.

### Running the Script
1. Install dependencies: `pip install selenium`.
2. Download and configure ChromeDriver.
3. Replace the URL and locators with those of a real e-commerce site (e.g., Amazon, eBay).
4. Run the script: `python advanced_selenium_ecommerce_scraper.py`.

This example demonstrates a production-ready Selenium script with best practices. Let me know if you need help adapting it to a specific website or adding features like authentication or parallel execution with Selenium Grid!
