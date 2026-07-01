---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-sonnet-4
title: Playwright端到端测试指南
translated: true
type: note
---

## 什么是 Playwright？

Playwright 是由微软开发的现代端到端测试框架，支持跨多种浏览器（Chromium、Firefox 和 WebKit）对 Web 应用程序进行可靠测试。它提供了统一的 API 用于自动化网页操作，专为处理现代 Web 应用挑战而设计，如单页应用、动态内容和复杂的用户交互。

## 主要特性

- **跨浏览器测试**：支持 Chromium、Firefox 和 WebKit
- **快速执行**：默认并行运行测试
- **自动等待**：自动等待元素准备就绪
- **网络拦截**：模拟 API 并捕获网络请求
- **移动端测试**：通过设备仿真测试移动 Web 应用
- **截图和视频**：内置可视化测试能力
- **调试工具**：配备追踪查看器的全面调试功能

## 安装与设置

### 基础安装

```bash
# 安装 Playwright
npm init playwright@latest

# 或添加到现有项目
npm install -D @playwright/test

# 安装浏览器
npx playwright install
```

### 项目结构

```
tests/
  example.spec.js
playwright.config.js
package.json
```

### 配置 (playwright.config.js)

```javascript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],

  webServer: {
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

## 编写第一个测试

### 基础测试结构

```javascript
import { test, expect } from '@playwright/test';

test('基础测试示例', async ({ page }) => {
  // 导航到页面
  await page.goto('https://example.com');

  // 与元素交互
  await page.click('button');
  await page.fill('input[name="username"]', 'testuser');

  // 断言
  await expect(page.locator('h1')).toHaveText('Welcome');
  await expect(page).toHaveURL(/dashboard/);
});
```

### 常用操作

#### 导航

```javascript
await page.goto('https://example.com');
await page.goBack();
await page.goForward();
await page.reload();
```

#### 元素交互

```javascript
// 点击元素
await page.click('button');
await page.click('text=Submit');
await page.click('#login-btn');

// 填写表单
await page.fill('input[name="email"]', 'user@example.com');
await page.type('textarea', 'Hello world');
await page.selectOption('select', 'option-value');

// 勾选/取消勾选
await page.check('input[type="checkbox"]');
await page.uncheck('input[type="checkbox"]');
```

#### 等待与超时

```javascript
// 等待元素
await page.waitForSelector('.loading-spinner', { state: 'hidden' });
await page.waitForURL('**/dashboard');
await page.waitForResponse('**/api/users');

// 等待自定义条件
await page.waitForFunction(() => window.myApp.isReady);
```

## 高级测试模式

### 页面对象模型

```javascript
// pages/LoginPage.js
export class LoginPage {
  constructor(page) {
    this.page = page;
    this.emailInput = page.locator('input[name="email"]');
    this.passwordInput = page.locator('input[name="password"]');
    this.loginButton = page.locator('button[type="submit"]');
  }

  async login(email, password) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }
}

// tests/login.spec.js
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test('用户可登录', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await page.goto('/login');
  await loginPage.login('user@example.com', 'password123');
  await expect(page).toHaveURL('/dashboard');
});
```

### API 测试

```javascript
test('API 测试', async ({ request }) => {
  // POST 请求
  const response = await request.post('/api/users', {
    data: {
      name: 'John Doe',
      email: 'john@example.com'
    }
  });

  expect(response.ok()).toBeTruthy();
  const userData = await response.json();
  expect(userData.name).toBe('John Doe');
});
```

### 网络模拟

```javascript
test('模拟 API 响应', async ({ page }) => {
  // 模拟 API 响应
  await page.route('**/api/users', async route => {
    const json = [{ id: 1, name: 'Mock User' }];
    await route.fulfill({ json });
  });

  await page.goto('/users');
  await expect(page.locator('.user-name')).toHaveText('Mock User');
});
```

### 可视化测试

```javascript
test('可视化对比', async ({ page }) => {
  await page.goto('/dashboard');

  // 全页面截图
  await expect(page).toHaveScreenshot('dashboard.png');

  // 元素截图
  await expect(page.locator('.header')).toHaveScreenshot('header.png');
});
```

## 测试组织与最佳实践

### 测试钩子

```javascript
import { test, expect } from '@playwright/test';

test.describe('用户管理', () => {
  test.beforeEach(async ({ page }) => {
    // 每个测试前运行
    await page.goto('/login');
    await page.fill('[name="email"]', 'admin@example.com');
    await page.fill('[name="password"]', 'password');
    await page.click('button[type="submit"]');
  });

  test.afterEach(async ({ page }) => {
    // 每个测试后清理
    await page.evaluate(() => localStorage.clear());
  });

  test('应创建新用户', async ({ page }) => {
    // 测试实现
  });
});
```

### 夹具与测试上下文

```javascript
// fixtures/auth.js
import { test as base } from '@playwright/test';

export const test = base.extend({
  authenticatedPage: async ({ page }, use) => {
    // 测试前登录
    await page.goto('/login');
    await page.fill('[name="email"]', 'user@example.com');
    await page.fill('[name="password"]', 'password');
    await page.click('button[type="submit"]');
    await page.waitForURL('/dashboard');

    await use(page);

    // 测试后清理
    await page.goto('/logout');
  },
});

// 在测试文件中
import { test, expect } from '../fixtures/auth';

test('认证用户操作', async ({ authenticatedPage }) => {
  await expect(authenticatedPage.locator('.welcome')).toBeVisible();
});
```

## 运行测试

### 命令行选项

```bash
# 运行所有测试
npx playwright test

# 运行特定测试文件
npx playwright test tests/login.spec.js

# 在 headed 模式下运行测试
npx playwright test --headed

# 在特定浏览器中运行测试
npx playwright test --project=firefox

# 在调试模式下运行测试
npx playwright test --debug

# 并行运行测试
npx playwright test --workers=4
```

### 测试报告

```bash
# 生成 HTML 报告
npx playwright show-report

# 查看追踪文件
npx playwright show-trace trace.zip
```

## Playwright vs Selenium

### 架构差异

| 特性 | Playwright | Selenium |
| --------- | ------------ | ---------- |
| **架构** | 直接浏览器通信 | WebDriver 协议 |
| **浏览器支持** | Chromium、Firefox、WebKit | Chrome、Firefox、Safari、Edge、IE |
| **安装** | 单一包包含浏览器 | 需单独下载驱动程序 |
| **语言支持** | JavaScript、Python、Java、C# | 大多数编程语言 |

### 性能对比

**Playwright 优势：**

- **执行更快**：直接浏览器 API 通信消除了 WebDriver 开销
- **默认并行**：内置并行测试执行
- **自动等待**：智能等待无需显式等待
- **网络控制**：内置请求/响应拦截

**Selenium 优势：**

- **成熟生态**：广泛的社区和第三方工具
- **语言灵活性**：支持更多编程语言
- **浏览器覆盖**：支持旧版浏览器如 Internet Explorer
- **行业标准**：广泛采用且文档丰富

### 特性对比

#### 测试可靠性

```javascript
// Playwright - 内置自动等待
await page.click('button'); // 等待元素可点击

// Selenium - 需要手动等待
await driver.wait(until.elementIsVisible(button));
await driver.wait(until.elementToBeClickable(button));
await button.click();
```

#### 移动端测试

```javascript
// Playwright - 内置移动端模拟
const context = await browser.newContext({
  ...devices['iPhone 13']
});

// Selenium - 需要额外设置
const options = new chrome.Options();
options.addArguments('--user-agent=iPhone...');
```

#### 网络处理

```javascript
// Playwright - 原生网络拦截
await page.route('**/api/**', route => route.abort());

// Selenium - 需要代理设置
const proxy = new Proxy();
proxy.setHttpProxy('localhost:8080');
```

### 迁移考量

**选择 Playwright 的情况：**

- 新项目或全新应用
- 具有 SPA 架构的现代 Web 应用
- 需要快速、可靠的测试执行
- 团队主要使用 JavaScript/TypeScript
- 需要内置的可视化测试

**坚持使用 Selenium 的情况：**

- 大型现有测试套件
- 需要特定的浏览器/操作系统组合
- 团队擅长非 JavaScript 语言
- 与现有 CI/CD 流水线集成
- 测试遗留应用程序

### 代码对比示例

```javascript
// Playwright
import { test, expect } from '@playwright/test';

test('登录流程', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="email"]', 'user@example.com');
  await page.fill('[name="password"]', 'password');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('/dashboard');
});

// Selenium (JavaScript)
const { Builder, By, until } = require('selenium-webdriver');

describe('登录流程', () => {
  let driver;

  beforeEach(async () => {
    driver = await new Builder().forBrowser('chrome').build();
  });

  afterEach(async () => {
    await driver.quit();
  });

  it('应成功登录', async () => {
    await driver.get('http://localhost:3000/login');
    await driver.findElement(By.name('email')).sendKeys('user@example.com');
    await driver.findElement(By.name('password')).sendKeys('password');
    await driver.findElement(By.css('button[type="submit"]')).click();
    await driver.wait(until.urlContains('/dashboard'));
  });
});
```

## 结论

Playwright 代表了端到端测试的现代方法，在速度、可靠性和开发者体验方面具有显著优势。虽然 Selenium 对于已建立的项目和特定用例仍然是可靠选择，但 Playwright 的架构和特性集使其特别适合测试现代 Web 应用程序。两者之间的选择应基于具体的项目需求、现有基础设施和团队专业知识。
