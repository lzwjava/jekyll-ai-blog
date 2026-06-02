---
audio: false
generated: true
lang: zh
layout: post
title: Selenium脚本
translated: true
type: note
---

以下是Python中一个复杂的Selenium脚本示例，展示了高级功能，包括页面对象模型（POM）、用于响应式布局的显式FacetGrid、显式等待、处理动态内容和错误处理。该脚本自动化了一个复杂场景：从电商网站抓取产品数据，浏览多个页面，并生成摘要报告。该示例假设了一个用于演示的虚拟电商网站，但这些概念可以适用于实际网站。

此示例展示了：
- **页面对象模型（POM）**，用于组织代码并提高可维护性。
- **显式等待**，用于处理动态内容。
- **FacetGrid**，用于响应式表格处理。
- **无头浏览器**，以提高执行效率。
- **数据处理**，生成JSON报告。
- **错误处理**，增强鲁棒性。

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

# 产品列表页的页面对象
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
            time.sleep(2)  # 等待排序生效
        except TimeoutException:
            print("排序下拉框未找到或超时")

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
            print(f"获取产品时出错: {e}")
            return []

    def go_to_next_page(self):
        try:
            next_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.next_page_button)
            )
            next_button.click()
            time.sleep(2)  # 等待页面加载
            return True
        except TimeoutException:
            print("未找到下一页按钮或超时")
            return False

# 搜索页的页面对象
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
            time.sleep(2)  # 等待搜索结果
        except TimeoutException as e:
            print(f"搜索失败: {e}")

# 主脚本
def scrape_ecommerce_site():
    # 设置无头Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    all_products = []

    try:
        # 导航到网站
        driver.get("https://example.com")

        # 初始化页面对象
        search_page = SearchPage(driver)
        product_page = ProductListingPage(driver)

        # 执行搜索
        search_page.search("laptop")

        # 按价格排序
        product_page.sort_by_price()

        # 抓取多个页面
        page_count = 0
        max_pages = 3  # 演示限制

        while page_count < max_pages:
            products = product_page.get_products()
            all_products.extend(products)
            print(f"已抓取第 {page_count + 1} 页: {len(products)} 个产品")

            if not product_page.go_to_next_page():
                break
            page_count += 1

        # 生成摘要
        summary = {
            "total_products": len(all_products),
            "average_price": calculate_average_price(all_products),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # 保存结果到JSON
        with open("product_data.json", "w") as f:
            json.dump({"products": all_products, "summary": summary}, f, indent=2)
        print("结果已保存到 product_data.json")

    except Exception as e:
        print(f"发生错误: {e}")

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

### 示例说明
1. **页面对象模型（POM）**：
   - 脚本使用两个页面对象类（`SearchPage` 和 `ProductListingPage`）来封装特定页面的逻辑，使代码模块化且易于维护。
   - 每个类包含定位符和与特定页面元素交互的方法。

2. **无头浏览器**：
   - 脚本在无头模式下运行Chrome以提高效率，适用于CI/CD流水线或服务器。

3. **显式等待**：
   - 使用 `WebDriverWait` 和 `expected_conditions` 处理动态内容，确保在交互之前元素存在或可点击。

4. **响应式表格处理**：
   - 脚本使用类似FacetGrid的逻辑抓取产品列表表格，从每个卡片中提取产品名称和价格。
   - 通过浏览多个页面（此示例最多3页）处理分页。

5. **错误处理**：
   - 脚本捕获 `TimeoutException` 和 `NoSuchElementException` 以优雅地处理缺失元素或超时。
   - `try-finally` 块确保即使发生错误也会关闭浏览器。

6. **数据处理**：
   - 抓取的数据存储在字典列表中并进行摘要（例如，产品总数、平均价格）。
   - 结果保存到JSON文件（`product_data.json`）以供进一步使用。

7. **动态排序**：
   - 脚本与下拉菜单交互以按价格排序产品，模拟真实用户行为。

### 输出
脚本生成一个JSON文件（`product_data.json`），结构如下：
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

### 注意事项
- **网站适配**：定位符（`By.ID`、`By.CLASS_NAME`）和URL（`https://example.com`）是占位符。请用目标网站HTML结构中的实际值替换它们，您可以使用浏览器开发者工具检查这些值。
- **依赖项**：确保已安装 `selenium`（`pip install selenium`）并且适当的浏览器驱动程序（例如ChromeDriver）在您的PATH中。
- **改进建议**：
  - 添加日志记录以便更好地调试。
  - 为不稳定的网络请求实现重试逻辑。
  - 使用配置文件管理定位符和设置。
  - 扩展以处理更复杂的场景，如身份验证或CAPTCHA。

### 运行脚本
1. 安装依赖项：`pip install selenium`。
2. 下载并配置ChromeDriver。
3. 将URL和定位符替换为真实电商网站（例如Amazon、eBay）的值。
4. 运行脚本：`python advanced_selenium_ecommerce_scraper.py`。

此示例展示了具有最佳实践的生产就绪Selenium脚本。如果您需要帮助将其适配到特定网站或添加如身份验证或使用Selenium Grid进行并行执行等功能，请告诉我！
