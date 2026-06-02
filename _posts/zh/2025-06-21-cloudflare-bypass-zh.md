---
audio: false
generated: true
lang: zh
layout: post
title: 云盾绕过Selenium脚本
translated: true
type: note
---

您的 Selenium 脚本设计用于通过 Firefox 和特定配置文件与 "https://grok.com" 交互，但遇到了 Cloudflare 的机器人检测挑战，特别是"请验证您是人类"的复选框。即使点击了复选框，脚本似乎仍难以通过验证，从而无法访问主要内容（例如文本区域）。Cloudflare 采用了复杂的方法来检测自动化浏览器，例如 HTTP 头分析、TLS 指纹识别和行为检查，这使得仅使用 Selenium 绕过此挑战变得棘手。不过，您可以尝试一些策略来通过 Cloudflare 测试，同时保持在当前基于 Firefox 的设置范围内。以下是两种针对您脚本的实用方法，如果这些方法不够，后面还提供了其他考虑事项。

---

### **方法一：使用配置文件重复使用手动完成的挑战**
由于您的脚本使用了特定的 Firefox 配置文件 (`/home/lzw/.mozilla/firefox/wzfodx6v.default`)，您可以利用此配置文件在手动通过 Cloudflare 挑战后存储会话数据。具体操作如下：

1. **手动使用配置文件打开 Firefox**：
   - 使用脚本中指定的相同配置文件启动 Firefox。您可以通过命令行执行此操作：
     ```bash
     firefox --profile "/home/lzw/.mozilla/firefox/wzfodx6v.default"
     ```
   - 或者，使用 Firefox 的配置文件管理器 (`firefox --ProfileManager`) 选择 `wzfodx6v.default`。

2. **导航并通过挑战**：
   - 在浏览器中访问 "https://grok.com"。
   - 当出现 Cloudflare 的"请验证您是人类"复选框提示时，点击它，如果出现任何额外的验证步骤，也请完成。
   - 等待直到进入主页面（例如，可以看到带有 `aria-label="向 Grok 提问任何内容"` 的文本区域）。

3. **关闭浏览器**：
   - 退出 Firefox，以确保配置文件保存会话 Cookie，包括任何 Cloudflare 的验证令牌（如 `cf_clearance`）。

4. **运行您的 Selenium 脚本**：
   - 按原样执行您的脚本。由于它使用相同的配置文件，它应该继承存储的 Cookie 和会话数据，从而可能允许它绕过挑战。

**此方法可能有效的原因**：Cloudflare 通常依赖 Cookie 来记住浏览器已通过其测试。通过手动预先验证配置文件，您的自动化会话可能看起来像是已验证访问的延续。

**局限性**：如果 Cloudflare 在每次页面加载时执行额外检查（例如，检测 Selenium 的自动化指纹），此方法可能会失败。如果发生这种情况，请尝试下一个方法。

---

### **方法二：在脚本中提取并设置 Cookie**
如果重复使用配置文件无效，您可以在通过挑战后手动提取 Cookie，并将其注入到您的 Selenium 驱动程序中。以下是分步过程：

1. **手动通过挑战**：
   - 按照方法一中的步骤 1 和 2 操作，以到达 "https://grok.com" 的主页面。

2. **提取 Cookie**：
   - 打开 Firefox 的开发者工具（按 F12 或右键单击 > 检查）。
   - 转到 **存储** 选项卡（或 **网络** 选项卡，然后重新加载页面以检查 Cookie）。
   - 查找与 `.grok.com` 关联的 Cookie，特别是 `cf_clearance`（Cloudflare 的验证 Cookie）。
   - 记下每个相关 Cookie 的 `name`、`value` 和 `domain`。例如：
     - 名称：`cf_clearance`，值：`abc123...`，域：`.grok.com`
     - 可能还存在其他 Cookie，如 `__cfduid` 或特定于会话的 Cookie。

3. **修改您的脚本**：
   - 在导航到 URL 之前，将 Cookie 添加到您的 Selenium 驱动程序中。像这样更新您的代码：
     ```python
     # ...（现有的导入和设置保持不变）

     # 设置 geckodriver 服务
     service = Service(executable_path="/home/lzw/bin/geckodriver")
     driver = webdriver.Firefox(service=service, options=firefox_options)

     # 首先打开一个空白页面来设置 Cookie（只能在页面加载后设置 Cookie）
     driver.get("about:blank")

     # 添加您提取的 Cookie
     cookies = [
         {"name": "cf_clearance", "value": "abc123...", "domain": ".grok.com"},
         # 根据需要添加其他 Cookie，例如：
         # {"name": "__cfduid", "value": "xyz789...", "domain": ".grok.com"},
     ]
     for cookie in cookies:
         driver.add_cookie(cookie)

     # 现在导航到目标 URL
     driver.get("https://grok.com")

     # 打印页面标题
     print("页面标题:", driver.title)

     # ...（脚本的其余部分保持不变）
     ```

4. **测试脚本**：
   - 运行修改后的脚本。预设的 Cookie 应向 Cloudflare 发出信号，表明浏览器已经通过了挑战。

**此方法可能有效的原因**：显式设置 `cf_clearance` Cookie 模拟了一个已验证的会话，可能绕过了与复选框交互的需要。

**局限性**：Cookie 可能与浏览器指纹（例如，用户代理、IP 或 TLS 设置）绑定。如果 Selenium 的指纹与手动会话的指纹不同，Cloudflare 可能会拒绝 Cookie 或重新发起挑战。

---

### **额外的调试和增强功能**
如果这两种方法都不能完全解决问题，请考虑对您的脚本进行以下调整，以确保它能正确与 Cloudflare 挑战交互：

- **检查是否存在 Iframe**："请验证您是人类"的复选框可能位于 iframe 内。修改您点击复选框的代码，首先切换到 iframe：
  ```python
  try:
      wait = WebDriverWait(driver, 20)
      iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'cloudflare')]")))
      driver.switch_to.frame(iframe)
      label = wait.until(EC.presence_of_element_located((By.XPATH, "//label[@class='cb-lb']")))
      checkbox = label.find_element(By.TAG_NAME, "input")
      print("找到复选框:", checkbox.is_displayed())
      checkbox.click()
      driver.switch_to.default_content()  # 切换回主内容
      print("复选框已点击。")
  except Exception as e:
      print("未找到复选框或无法点击:", e)
  ```

- **改进等待逻辑**：点击复选框后，等待挑战已通过的明确迹象（例如，验证页面消失）：
  ```python
  try:
      wait.until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Verify you are human')]")))
      print("挑战已通过。")
  except Exception as e:
      print("挑战未通过:", e)
  ```

- **掩盖自动化痕迹**：添加 JavaScript 以隐藏 Selenium 的自动化痕迹：
  ```python
  driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
  ```

---

### **如果所有方法都失败：替代方案**
如果 Cloudflare 的检测持续存在，可能是因为高级指纹识别是您当前设置无法规避的。以下是升级选项，尽管它们偏离了您对 Firefox 的偏好：

- **切换到使用 Undetected ChromeDriver 的 Chrome**：
  - 安装：`pip install undetected-chromedriver`
  - 修改设置：
    ```python
    import undetected_chromedriver as uc
    driver = uc.Chrome()
    driver.get("https://grok.com")
    ```
  - 此库对 Chrome 进行补丁，以避免常见的检测方法。

- **使用代理或 CAPTCHA 解决服务**：像 2Captcha 或住宅代理这样的服务可以处理挑战，但它们会增加复杂性和成本。

---

### **推荐的后续步骤**
从**方法一**（重复使用配置文件）开始，因为它最简单且与您的脚本设置一致。如果失败，请尝试**方法二**（注入 Cookie）并添加 iframe 检查。这些方法最大限度地利用了您现有的 Firefox 配置，无需新工具。测试每种方法并监控输出（例如 `driver.title` 和异常消息）以确认挑战是否被绕过。如果您仍然遇到问题，请根据项目的灵活性考虑替代方案。

如果您需要帮助实施或排查这些解决方案，请告诉我！
