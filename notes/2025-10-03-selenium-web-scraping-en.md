---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Selenium Web Scraping Code Explanation
translated: false
type: note
---

### Explanation of Selenium API Usage in the Provided Code

This Python script uses the **Selenium WebDriver** library to automate a web browser (specifically Chrome) for interacting with a website (likely a data/trade portal at `https://xxdata.com/index.aspx`). The goal appears to be web scraping: logging in, searching for trade/order data (using a HS code like '8449'), navigating through paginated results, clicking on details, extracting structured data from HTML tables, and storing it in a SQLite database (`data.db`).

Selenium is used here for **browser automation**, allowing the script to mimic human interactions like typing, clicking, scrolling, and waiting for page loads—something that's hard or impossible with simple HTTP requests (e.g., due to JavaScript-heavy pages, iframes, or dynamic content). It handles dynamic web elements, sessions, and multi-window/iframe switching, which are common in modern web apps.

I'll break it down **section by section**, highlighting key Selenium APIs, their purpose, and how they're used. Note: Some methods in the code (e.g., `find_element_by_css_selector`) are from older Selenium versions (pre-4.0) and are deprecated. In modern Selenium (4+), you'd use `find_element(By.CSS_SELECTOR, ...)` instead, but the functionality is the same. The script also imports necessary modules for waits, exceptions, and element handling.

#### 1. **Imports and Setup (Selenium Initialization)**
   ```python
   from selenium import webdriver
   from selenium.webdriver.chrome.webdriver import WebDriver
   from selenium.webdriver.common.keys import Keys
   from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
   from selenium.webdriver.support.ui import WebDriverWait
   from selenium.webdriver.support import expected_conditions as EC
   from selenium.webdriver.common.by import By
   from selenium.webdriver.remote.webelement import WebElement
   ```
   - **Purpose**: These import core Selenium components:
     - `webdriver`: Main module for controlling the browser.
     - `WebDriver`: Type hint for the browser instance (ensures type safety).
     - `Keys`: For simulating keyboard inputs (e.g., Page Up).
     - Exceptions: Handle common errors like timeouts or stale elements (elements that change after a page refresh).
     - `WebDriverWait` and `EC` (Expected Conditions): For explicit waits—polling until an element meets a condition (e.g., present on page).
     - `By`: Locator strategies (e.g., CSS selector, ID, tag name) to find elements.
     - `WebElement`: Represents HTML elements for interaction.

   In `run()` function:
   ```python
   options = webdriver.ChromeOptions()
   options.add_argument("--start-maximized")  # Opens browser in full screen.
   options.add_argument('--log-level=3')      # Suppresses console logs for cleaner output.
   browser: WebDriver = webdriver.Chrome(executable_path="./chromedriver", options=options)
   ```
   - **Selenium API Used**: `webdriver.Chrome(options=...)`
     - Initializes a Chrome browser instance using a local `chromedriver` executable (must be in the script's directory).
     - `ChromeOptions`: Customizes the browser session (e.g., headless mode could be added with `options.add_argument("--headless")` for background running).
     - This creates a live, controllable browser window. Selenium acts as a bridge between Python and the browser's DevTools protocol.

   ```python
   browser.get('https://xxdata.com/index.aspx')
   ```
   - **Selenium API Used**: `WebDriver.get(url)`
     - Navigates to the starting URL, loading the page like a user typing it in the address bar.

#### 2. **Login Process**
   ```python
   input_username = browser.find_element_by_css_selector('input[name=username]')
   input_username.send_keys('name')
   input_password = browser.find_element_by_css_selector('input[name=password]')
   input_password.send_keys('password')
   btn_login = browser.find_element_by_css_selector('div.login-check')
   btn_login.click()
   ```
   - **Selenium APIs Used**:
     - `WebDriver.find_element_by_css_selector(css)` (deprecated; modern: `find_element(By.CSS_SELECTOR, css)`): Locates a single HTML element using a CSS selector (e.g., by attribute like `name="username"`). Returns a `WebElement`.
     - `WebElement.send_keys(text)`: Simulates typing into an input field (e.g., username/password).
     - `WebElement.click()`: Simulates a mouse click on a button or link.
   - **How Selenium is Used**: Automates form submission. Without Selenium, you'd need to reverse-engineer POST requests, but this handles JavaScript validation or dynamic forms seamlessly. Credentials are hardcoded (insecure in production—use env vars).

   After login:
   ```python
   wait_element(browser, 'div.dsh_01')
   ```
   - Calls a custom `wait_element` function (explained below) to pause until the dashboard loads.

#### 3. **Navigation and Search**
   ```python
   trade_div = browser.find_element_by_css_selector('div.dsh_01')
   trade_div.click()
   wait_element(browser, 'a.teq_icon')
   teq = browser.find_element_by_css_selector('a.teq_icon')
   teq.click()
   wait_element(browser, 'div.panel-body')
   iframe = browser.find_element_by_css_selector('div.panel-body > iframe')
   iframe_id = iframe.get_attribute('id')
   browser.switch_to.frame(iframe_id)
   ```
   - **Selenium APIs Used**:
     - `find_element_by_css_selector`: Locates navigation elements (e.g., dashboard div, icon link).
     - `WebElement.click()`: Clicks to navigate (e.g., to a "trade" section).
     - `WebElement.get_attribute('id')`: Retrieves an HTML attribute (here, iframe's ID).
     - `WebDriver.switch_to.frame(frame_id)`: Switches the driver context to an `<iframe>` (common in apps for embedding content). Without this, elements inside the iframe are inaccessible.
   - **How Selenium is Used**: Handles multi-step navigation and embedded content. Iframes isolate DOMs, so switching is essential for scraping inner pages.

   Search process:
   ```python
   input_search = browser.find_element_by_id('_easyui_textbox_input7')  # Uses ID locator.
   input_search.send_keys('8449')
   time.sleep(10)
   enter = browser.find_element_by_css_selector('a#btnOk > div.enter-bt')
   enter.click()
   ```
   - **Selenium APIs Used**:
     - `find_element_by_id(id)` (deprecated; modern: `find_element(By.ID, id)`): Locates by HTML `id` attribute.
     - `send_keys`: Types the search query (HS code for products).
     - `time.sleep(10)`: Implicit wait (crude; better to use explicit waits).
     - `click()`: Submits the search.
   - **How Selenium is Used**: Simulates user search. The `time.sleep` pauses for AJAX/JavaScript to load results.

#### 4. **Pagination and Result Processing**
   ```python
   result_count_span = browser.find_element_by_css_selector('span#ResultCount')
   page = math.ceil(int(result_count_span.text) / 20)  # Calculates total pages (20 results/page).
   skip = 0
   page = page - skip

   for p in range(page):
       input_page = browser.find_element_by_css_selector('input.laypage_skip')
       input_page.send_keys(str(p + skip + 1))
       btn_confirm = browser.find_element_by_css_selector('button.laypage_btn')
       btn_confirm.click()
       time.sleep(2)

       locates = browser.find_elements_by_css_selector('div.rownumber-bt')  # Multiple elements.
       print('page ' + str(p) + ' size: ' + str(len(locates)))
       for locate in locates:
           browser.execute_script("arguments[0].scrollIntoView();", locate)  # JavaScript scroll.
           time.sleep(1)
           browser.find_element_by_tag_name('html').send_keys(Keys.PAGE_UP)  # Keyboard scroll.
           time.sleep(1)
           try:
               locate.click()
           except ElementClickInterceptedException:
               print('ElementClickInterceptedException')
               continue
           except StaleElementReferenceException:
               print('StaleElementReferenceException')
               continue
           # ... (more below)
   ```
   - **Selenium APIs Used**:
     - `find_element_by_css_selector`: Gets result count from a span.
     - `WebElement.text`: Extracts visible text from an element (e.g., count like "100").
     - `find_elements_by_css_selector` (plural; deprecated: `find_elements(By.CSS_SELECTOR, ...)`): Finds multiple elements (e.g., row links on a page). Returns a list of `WebElement`s.
     - `WebDriver.execute_script(js_code, *args)`: Runs custom JavaScript in the browser (here, scrolls an element into view to avoid click issues).
     - `WebDriver.find_element_by_tag_name('html').send_keys(Keys.PAGE_UP)`: Simulates keyboard scrolling (using `Keys` enum).
     - Exceptions: Catches click failures (e.g., overlay blocks click) or stale elements (DOM refreshed, invalidating references—common in dynamic UIs).
   - **How Selenium is Used**: Automates pagination by typing page numbers and clicking "go." For each result row (`div.rownumber-bt`), it scrolls to ensure visibility, then clicks to open details in a new window. This handles lazy-loaded or infinite-scroll-like behavior.

#### 5. **Window/Iframe Switching and Data Extraction**
   Continuing from the loop:
   ```python
   time.sleep(1)
   browser.switch_to.window(browser.window_handles[1])  # Switch to new tab/window.
   wait_element(browser, 'div#content')
   try:
       save_page(browser)
   except IndexError:
       print('IndexError')
       continue
   browser.close()  # Closes the detail window.
   browser.switch_to.window(browser.window_handles[0])  # Back to main window.
   browser.switch_to.frame(iframe_id)  # Back to iframe context.
   ```
   - **Selenium APIs Used**:
     - `WebDriver.window_handles`: List of open window/tab IDs.
     - `WebDriver.switch_to.window(handle)`: Switches focus to a specific window (index 0 = main, 1 = new tab opened by click).
     - `WebDriver.close()`: Closes the current window.
   - **How Selenium is Used**: Clicks open details in new tabs, so it switches contexts to scrape them, then returns. This is crucial for multi-tab apps.

#### 6. **Data Extraction in `save_page(browser: WebDriver)` Function**
   This is the core scraping logic:
   ```python
   ts = browser.find_elements_by_css_selector('table')  # All tables on the page.
   t0 = ts[0]
   tds0 = t0.find_elements_by_tag_name('td')  # TD cells in first table.
   order_number = tds0[2].text  # Extracts text from specific cells.
   # ... (similar for other tables: t1, t2, etc.)
   ```
   - **Selenium APIs Used**:
     - `find_elements_by_css_selector('table')` / `find_elements_by_tag_name('td')` (deprecated: use `By.TAG_NAME`): Finds all `<table>`s and their `<td>` cells.
     - `WebElement.text`: Pulls text content from cells (e.g., order number, importer name).
     - Custom `tds_to_text(tds: list[WebElement])`: Concatenates text from paired `<td>`s (e.g., label + value).
   - **How Selenium is Used**: Parses the page's DOM structure (tables with order/importer/exporter details). It handles variable table counts (e.g., if `len(ts) == 8`, extra tables exist). Data is then inserted into SQLite (non-Selenium part).

   Conditional logic extracts fields like `order_number`, `importer`, `exporter`, etc., based on table indices—assuming a fixed layout.

#### 7. **Waits and Error Handling (`wait_element` Function)**
   ```python
   def wait_element(browser, css):
       timeout = 30
       try:
           element_present = EC.presence_of_element_located((By.CSS_SELECTOR, css))
           WebDriverWait(browser, timeout).until(element_present)
       except TimeoutException:
           print('Timed out waiting for page to load')
   ```
   - **Selenium APIs Used**:
     - `expected_conditions.presence_of_element_located(locator)`: Waits for an element to exist in the DOM (not necessarily visible).
     - `WebDriverWait(driver, timeout).until(condition)`: Polls every 0.5s up to 30s for the condition.
     - `TimeoutException`: Raised if wait fails.
   - **How Selenium is Used**: Prevents race conditions (e.g., clicking before page loads). Better than `time.sleep` as it's element-specific and efficient.

#### 8. **Cleanup**
   ```python
   time.sleep(1000)  # Long pause (debugging?).
   browser.quit()    # Closes browser and ends session.
   ```
   - **Selenium API Used**: `WebDriver.quit()`: Terminates the driver, closes all windows, and releases resources.

#### Overall How Selenium Fits In
- **Automation Flow**: Selenium launches a real browser, loads pages, interacts via DOM queries (locators like CSS/ID), and handles dynamic behaviors (JS execution, waits, switches). It's ideal for SPAs or protected sites with sessions/cookies.
- **Strengths Here**: Handles login state, iframes, new tabs, and scrolling—scraping tools like BeautifulSoup/Requests couldn't do this alone.
- **Limitations/Issues in Code**:
  - Deprecated locators: Update to `By` for future-proofing.
  - Hardcoded sleeps: Replace more with waits to speed up/reduce flakiness.
  - Exceptions: Good handling, but could retry on StaleElement.
  - Ethics/Legality: Scraping may violate terms; add user-agent headers or proxies to mimic humans.
  - Performance: Runs headful (visible browser); make headless for production.
- **Running It**: Requires ChromeDriver (download from Selenium site, match Chrome version). Install Selenium via `pip install selenium`.

If you have questions about specific parts, modernizing the code, or debugging, let me know!
