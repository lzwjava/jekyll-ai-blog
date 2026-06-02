---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Selenium网页爬虫代码解析
translated: true
type: note
---

### 代码中 Selenium API 使用说明

这段 Python 脚本使用 **Selenium WebDriver** 库来自动化网页浏览器（特别是 Chrome），以便与网站（很可能是位于 `https://xxdata.com/index.aspx` 的数据/贸易门户网站）进行交互。其目标似乎是网络爬取：登录、搜索贸易/订单数据（使用如 '8449' 的 HS 编码）、浏览分页结果、点击查看详情、从 HTML 表格中提取结构化数据，并将其存储到 SQLite 数据库 (`data.db`) 中。

这里使用 Selenium 是为了**浏览器自动化**，使脚本能够模拟人类的交互行为，如输入、点击、滚动和等待页面加载——这对于简单的 HTTP 请求（例如，由于 JavaScript 繁重的页面、iframe 或动态内容）来说是困难或不可能实现的。它能处理动态网页元素、会话和多窗口/iframe 切换，这些在现代网络应用中很常见。

我将**逐节**进行分解，重点介绍关键的 Selenium API、它们的用途以及它们是如何被使用的。注意：代码中的某些方法（例如 `find_element_by_css_selector`）来自旧版 Selenium（4.0 之前），并且已弃用。在现代 Selenium（4+）中，您应使用 `find_element(By.CSS_SELECTOR, ...)`，但其功能是相同的。该脚本还导入了用于等待、异常处理和元素操作的必要模块。

#### 1. **导入和设置（Selenium 初始化）**
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
   - **目的**：这些导入核心的 Selenium 组件：
     - `webdriver`：控制浏览器的主模块。
     - `WebDriver`：浏览器实例的类型提示（确保类型安全）。
     - `Keys`：用于模拟键盘输入（例如，Page Up）。
     - 异常：处理常见错误，如超时或元素过时（页面刷新后元素发生变化）。
     - `WebDriverWait` 和 `EC`（预期条件）：用于显式等待——轮询直到元素满足某个条件（例如，在页面上存在）。
     - `By`：定位策略（例如，CSS 选择器、ID、标签名）用于查找元素。
     - `WebElement`：表示用于交互的 HTML 元素。

   在 `run()` 函数中：
   ```python
   options = webdriver.ChromeOptions()
   options.add_argument("--start-maximized")  # 以全屏模式打开浏览器。
   options.add_argument('--log-level=3')      # 抑制控制台日志输出，使输出更清晰。
   browser: WebDriver = webdriver.Chrome(executable_path="./chromedriver", options=options)
   ```
   - **使用的 Selenium API**：`webdriver.Chrome(options=...)`
     - 使用本地的 `chromedriver` 可执行文件（必须在脚本目录中）初始化 Chrome 浏览器实例。
     - `ChromeOptions`：自定义浏览器会话（例如，可以添加 `options.add_argument("--headless")` 以在后台运行的无头模式）。
     - 这会创建一个实时的、可控制的浏览器窗口。Selenium 充当 Python 和浏览器开发者工具协议之间的桥梁。

   ```python
   browser.get('https://xxdata.com/index.aspx')
   ```
   - **使用的 Selenium API**：`WebDriver.get(url)`
     - 导航到起始 URL，像用户在地址栏中输入一样加载页面。

#### 2. **登录过程**
   ```python
   input_username = browser.find_element_by_css_selector('input[name=username]')
   input_username.send_keys('name')
   input_password = browser.find_element_by_css_selector('input[name=password]')
   input_password.send_keys('password')
   btn_login = browser.find_element_by_css_selector('div.login-check')
   btn_login.click()
   ```
   - **使用的 Selenium API**：
     - `WebDriver.find_element_by_css_selector(css)`（已弃用；现代写法：`find_element(By.CSS_SELECTOR, css)`）：使用 CSS 选择器（例如，通过属性如 `name="username"`）定位单个 HTML 元素。返回一个 `WebElement`。
     - `WebElement.send_keys(text)`：模拟在输入字段中键入内容（例如，用户名/密码）。
     - `WebElement.click()`：模拟在按钮或链接上的鼠标点击。
   - **Selenium 的使用方式**：自动化表单提交。如果没有 Selenium，您需要反向工程 POST 请求，但这可以无缝处理 JavaScript 验证或动态表单。凭证是硬编码的（在生产环境中不安全——请使用环境变量）。

   登录后：
   ```python
   wait_element(browser, 'div.dsh_01')
   ```
   - 调用自定义的 `wait_element` 函数（如下所述）暂停，直到仪表板加载完成。

#### 3. **导航和搜索**
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
   - **使用的 Selenium API**：
     - `find_element_by_css_selector`：定位导航元素（例如，仪表板 div、图标链接）。
     - `WebElement.click()`：点击进行导航（例如，到"贸易"部分）。
     - `WebElement.get_attribute('id')`：检索 HTML 属性（此处为 iframe 的 ID）。
     - `WebDriver.switch_to.frame(frame_id)`：将驱动程序的上下文切换到 `<iframe>`（在应用中嵌入内容很常见）。没有这个，iframe 内部的元素将无法访问。
   - **Selenium 的使用方式**：处理多步导航和嵌入内容。Iframe 隔离了 DOM，因此切换对于爬取内部页面至关重要。

   搜索过程：
   ```python
   input_search = browser.find_element_by_id('_easyui_textbox_input7')  # 使用 ID 定位器。
   input_search.send_keys('8449')
   time.sleep(10)
   enter = browser.find_element_by_css_selector('a#btnOk > div.enter-bt')
   enter.click()
   ```
   - **使用的 Selenium API**：
     - `find_element_by_id(id)`（已弃用；现代写法：`find_element(By.ID, id)`）：通过 HTML `id` 属性定位。
     - `send_keys`：输入搜索查询（产品的 HS 编码）。
     - `time.sleep(10)`：隐式等待（粗糙；最好使用显式等待）。
     - `click()`：提交搜索。
   - **Selenium 的使用方式**：模拟用户搜索。`time.sleep` 暂停以等待 AJAX/JavaScript 加载结果。

#### 4. **分页和结果处理**
   ```python
   result_count_span = browser.find_element_by_css_selector('span#ResultCount')
   page = math.ceil(int(result_count_span.text) / 20)  # 计算总页数（每页 20 条结果）。
   skip = 0
   page = page - skip

   for p in range(page):
       input_page = browser.find_element_by_css_selector('input.laypage_skip')
       input_page.send_keys(str(p + skip + 1))
       btn_confirm = browser.find_element_by_css_selector('button.laypage_btn')
       btn_confirm.click()
       time.sleep(2)

       locates = browser.find_elements_by_css_selector('div.rownumber-bt')  # 多个元素。
       print('page ' + str(p) + ' size: ' + str(len(locates)))
       for locate in locates:
           browser.execute_script("arguments[0].scrollIntoView();", locate)  # JavaScript 滚动。
           time.sleep(1)
           browser.find_element_by_tag_name('html').send_keys(Keys.PAGE_UP)  # 键盘滚动。
           time.sleep(1)
           try:
               locate.click()
           except ElementClickInterceptedException:
               print('ElementClickInterceptedException')
               continue
           except StaleElementReferenceException:
               print('StaleElementReferenceException')
               continue
           # ... (后续更多代码)
   ```
   - **使用的 Selenium API**：
     - `find_element_by_css_selector`：从 span 中获取结果计数。
     - `WebElement.text`：从元素中提取可见文本（例如，像 "100" 这样的计数）。
     - `find_elements_by_css_selector`（复数；已弃用：`find_elements(By.CSS_SELECTOR, ...)`）：查找多个元素（例如，页面上的行链接）。返回一个 `WebElement` 列表。
     - `WebDriver.execute_script(js_code, *args)`：在浏览器中运行自定义 JavaScript（此处，将元素滚动到视图中以避免点击问题）。
     - `WebDriver.find_element_by_tag_name('html').send_keys(Keys.PAGE_UP)`：模拟键盘滚动（使用 `Keys` 枚举）。
     - 异常：捕获点击失败（例如，覆盖层阻挡点击）或过时元素（DOM 已刷新，使引用无效——在动态 UI 中很常见）。
   - **Selenium 的使用方式**：通过输入页码并点击"前往"来自动化分页。对于每个结果行 (`div.rownumber-bt`)，它会滚动以确保可见性，然后点击以在新窗口中打开详情。这处理了懒加载或类似无限滚动的行为。

#### 5. **窗口/Iframe 切换和数据提取**
   从循环继续：
   ```python
   time.sleep(1)
   browser.switch_to.window(browser.window_handles[1])  # 切换到新标签页/窗口。
   wait_element(browser, 'div#content')
   try:
       save_page(browser)
   except IndexError:
       print('IndexError')
       continue
   browser.close()  # 关闭详情窗口。
   browser.switch_to.window(browser.window_handles[0])  # 返回主窗口。
   browser.switch_to.frame(iframe_id)  # 返回 iframe 上下文。
   ```
   - **使用的 Selenium API**：
     - `WebDriver.window_handles`：打开的窗口/标签页 ID 列表。
     - `WebDriver.switch_to.window(handle)`：将焦点切换到特定窗口（索引 0 = 主窗口，1 = 点击打开的新标签页）。
     - `WebDriver.close()`：关闭当前窗口。
   - **Selenium 的使用方式**：点击在新标签页中打开详情，因此它会切换上下文来爬取它们，然后返回。这对于多标签页应用至关重要。

#### 6. **在 `save_page(browser: WebDriver)` 函数中的数据提取**
   这是核心的爬取逻辑：
   ```python
   ts = browser.find_elements_by_css_selector('table')  # 页面上的所有表格。
   t0 = ts[0]
   tds0 = t0.find_elements_by_tag_name('td')  # 第一个表格中的 TD 单元格。
   order_number = tds0[2].text  # 从特定单元格提取文本。
   # ... (对其他表格 t1, t2 等类似操作)
   ```
   - **使用的 Selenium API**：
     - `find_elements_by_css_selector('table')` / `find_elements_by_tag_name('td')`（已弃用：使用 `By.TAG_NAME`）：查找所有 `<table>` 及其 `<td>` 单元格。
     - `WebElement.text`：从单元格中提取文本内容（例如，订单号、进口商名称）。
     - 自定义 `tds_to_text(tds: list[WebElement])`：连接成对的 `<td>` 中的文本（例如，标签 + 值）。
   - **Selenium 的使用方式**：解析页面的 DOM 结构（包含订单/进口商/出口商详情的表格）。它处理可变的表格数量（例如，如果 `len(ts) == 8`，则存在额外的表格）。然后数据被插入到 SQLite 中（非 Selenium 部分）。

   条件逻辑根据表格索引提取字段，如 `order_number`、`importer`、`exporter` 等——假设布局是固定的。

#### 7. **等待和错误处理（`wait_element` 函数）**
   ```python
   def wait_element(browser, css):
       timeout = 30
       try:
           element_present = EC.presence_of_element_located((By.CSS_SELECTOR, css))
           WebDriverWait(browser, timeout).until(element_present)
       except TimeoutException:
           print('Timed out waiting for page to load')
   ```
   - **使用的 Selenium API**：
     - `expected_conditions.presence_of_element_located(locator)`：等待元素在 DOM 中存在（不一定可见）。
     - `WebDriverWait(driver, timeout).until(condition)`：在超时时间（30秒）内每隔 0.5 秒轮询一次条件。
     - `TimeoutException`：如果等待失败则抛出。
   - **Selenium 的使用方式**：防止竞态条件（例如，在页面加载完成前点击）。比 `time.sleep` 更好，因为它是元素特定的且效率更高。

#### 8. **清理**
   ```python
   time.sleep(1000)  # 长暂停（用于调试？）。
   browser.quit()    # 关闭浏览器并结束会话。
   ```
   - **使用的 Selenium API**：`WebDriver.quit()`：终止驱动程序，关闭所有窗口并释放资源。

#### Selenium 的整体作用
- **自动化流程**：Selenium 启动一个真实的浏览器，加载页面，通过 DOM 查询（如 CSS/ID 定位器）进行交互，并处理动态行为（JS 执行、等待、切换）。它对于 SPA 或具有会话/Cookie 的受保护站点来说是理想选择。
- **在此处的优势**：处理登录状态、iframe、新标签页和滚动——仅使用 BeautifulSoup/Requests 等爬取工具无法单独做到这一点。
- **代码中的限制/问题**：
  - 已弃用的定位器：更新为使用 `By` 以面向未来。
  - 硬编码的睡眠：用更多的等待替换以加速运行/减少不稳定性。
  - 异常：处理得很好，但可以在 StaleElement 上重试。
  - 道德/合法性：爬取可能违反条款；添加用户代理头或代理以模拟人类行为。
  - 性能：以有头模式运行（可见浏览器）；在生产环境中改为无头模式。
- **运行它**：需要 ChromeDriver（从 Selenium 网站下载，与 Chrome 版本匹配）。通过 `pip install selenium` 安装 Selenium。

如果您对特定部分、代码现代化或调试有疑问，请告诉我！
