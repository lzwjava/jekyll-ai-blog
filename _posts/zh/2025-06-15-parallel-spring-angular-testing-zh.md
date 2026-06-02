---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 并行弹簧角度浏览器测试
translated: true
type: note
---

明白了——你需要一种实用的方法，在 **Edge 和 Chrome 中并行测试** 你的 Spring (Java) + Angular 站点，主要是 **手动测试**（在有帮助的地方辅以轻量自动化）。以下是一个经过实践检验的工作流程，可以避免宽表格问题。

---

# 1) 设置干净、可比较的浏览器

* **安装最新的稳定版** Chrome 和 Edge。记录下版本号。
* 为每个浏览器创建 **独立的干净配置文件** 用于测试：

  * Chrome: `chrome --user-data-dir=/tmp/chrome-qa --no-first-run`
  * Edge: `msedge --user-data-dir=/tmp/edge-qa --no-first-run`
* 匹配 **缩放比例 (100%)**、**设备像素比 (DPR)**、**语言**、**操作系统主题**、**字体包**，并关闭扩展程序。
* 将两个浏览器并排固定（如果可能，使用两个显示器）。使用相同的 **视口**（例如，1440×900）。

---

# 2) 准备稳定的后端 + 真实数据

* 在 **预发布模式** 下启动你的 Spring 后端，并使用确定性的种子数据。
* 优先使用 **不可变的测试账户** 和 **已知数据集**（例如，使用 Testcontainers 进行数据库快照，或使用 Flyway/Liquibase 种子脚本）。
* 对于不稳定的依赖项，使用 **WireMock** 桩（HTTP）以使 UI 行为可重复。

---

# 3) 跨浏览器镜像交互（手动，但同步）

为了进行真正的并行手动测试，将一个浏览器的点击、滚动、输入操作镜像到另一个浏览器：

* 使用 **Browsersync** 作为本地代理来 **同步交互**：

    ```bash
    npm i -g browser-sync
    browser-sync start --proxy "http://localhost:4200" --files "dist/**/*" --open "external"
    ```

    在 **Chrome** 和 **Edge** 中打开代理后的 URL；滚动、点击和表单输入将被镜像。
    （对于布局差异、悬停/焦点检查以及快速流程非常有用。）

> 如果无法使用代理（由于认证限制、公司网络），则运行两个浏览器窗口，并保持一个严格的 **步骤列表**（见下文），外加一个分屏屏幕录制器。

---

# 4) 跨浏览器检查清单（同时运行）

**并行** 处理此清单——在两个浏览器中完成相同步骤后再进行下一步。

* **引导与字体：** 无样式内容闪烁 (FOUC)、图标字体、回退字体。
* **布局：** Flex/Grid 间隙、粘性头部/底部、溢出/省略、RTL/本地化文本换行。
* **表单：** 自动填充、占位符、验证消息、数字/日期输入、IME/中文输入、复制/粘贴。
* **焦点/键盘：** Tab 键顺序、焦点环可见性、`:focus-visible` 与 `:focus`、Enter/Esc 行为、快捷键。
* **悬停/激活：** 菜单、工具提示、涟漪效果、Angular Material 状态类。
* **文件与下载：** 文件输入接受过滤器、拖放、下载提示。
* **认证/会话：** Cookie、SameSite、跨标签页的存储隔离、会话超时和刷新令牌流程。
* **路由：** 深层链接、在嵌套路由上硬刷新、404 回退。
* **缓存：** Service Worker 更新周期、陈旧资源清除、离线页面行为。
* **媒体与 API：** getUserMedia/剪贴板、通知权限。
* **可访问性快速检查：** 地标/角色、颜色对比度（开发者工具）、仅键盘导航。
* **性能检查：** 开发者工具性能面板，检查长任务，并在 **两个** 浏览器中运行 Lighthouse。

提示：在 **两个浏览器中都打开开发者工具** (F12)，停靠在底部，并比较 **控制台** 警告（框架、CSP 和弃用消息）。

---

# 5) Angular 特有的常见差异点

* **变更检测与异步：** 微任务时序可能导致竞态条件在不同浏览器中表现不同；注意观察加载指示器和“保存”按钮的双击问题。
* **Zone.js 错误：** 未处理的 Promise 拒绝可能在一个浏览器中出现，而在另一个中没有——检查控制台。
* **Angular Material 主题：** 验证深色/浅色主题令牌、高对比度模式和焦点轮廓（Edge 的焦点渲染通常略有不同）。
* **i18n 管道与日期格式：** 在 Chromium 变体中，`DatePipe` 和 `Intl` 的区域设置差异。

---

# 6) Spring 后端需要注意的问题

* **CORS 与重定向：** 规则相同，但 **Edge 有时在开发阶段更早暴露 CORS 预检请求问题**；验证 `OPTIONS` 响应和头部。
* **Content-Type 与压缩：** 检查 `application/json;charset=UTF-8` 与 `application/json`；验证 gzip/br——不匹配可能导致一个浏览器首先显示“加载失败”。
* **安全头部：** CSP、HSTS、X-Frame-Options——更严格的策略可能以不同方式阻止内联脚本/样式。

---

# 7) 通过薄自动化层使“手动”测试可重复

即使你不想做完整的 E2E 测试，也可以设置一个 **简短、快速** 的浏览器测试工具，让 CI 在每个 PR 上同时运行 Chrome 和 Edge。这样可以更早地发现回归问题，并减轻手动测试的负担。

### 选项 A: Playwright（我对 Angular 应用的首选）

* 一个测试运行器，启动 **Chrome Stable** 和 **Microsoft Edge** 渠道，**并行运行**。
* `npm i -D @playwright/test`
* `npx playwright install chromium`
* `playwright.config.ts` 示例：

    ```ts
    import { defineConfig, devices } from '@playwright/test';

    export default defineConfig({
      testDir: './e2e',
      workers: 4, // 并行度
      use: {
        baseURL: 'http://localhost:4200',
        trace: 'retain-on-failure',
      },
      projects: [
        {
          name: 'Chrome Stable',
          use: { ...devices['Desktop Chrome'], channel: 'chrome' },
        },
        {
          name: 'Microsoft Edge',
          use: { ...devices['Desktop Edge'], channel: 'msedge' },
        },
      ],
    });
    ```

    最小化的冒烟测试用例 (`e2e/smoke.spec.ts`)：

    ```ts
    import { test, expect } from '@playwright/test';

    test('home loads and login works', async ({ page }) => {
      await page.goto('/');
      await expect(page.getByRole('heading', { name: 'Welcome' })).toBeVisible();
      await page.getByLabel('Email').fill('user@example.com');
      await page.getByLabel('Password').fill('Password123!');
      await page.getByRole('button', { name: 'Sign in' }).click();
      await expect(page.getByText('Dashboard')).toBeVisible();
    });
    ```

    运行：`npx playwright test`

### 选项 B: Cypress（Chromium 系列，可运行 Chrome 和 Edge）

* 通过 CI 矩阵（或 Cypress Dashboard）实现并行化。
* 在 CI 中运行：

  * `cypress run --browser chrome`
  * `cypress run --browser edge`
* 保持测试用例短小（仅冒烟测试），以维持“手动为主”的原则。

### 选项 C: Selenium Grid（如果你已在使用 Selenium）

* Docker 化的 Grid **并发运行 chromium/edge 节点**。

    ```yaml
    # docker-compose.yml
    services:
      selenium-hub:
        image: selenium/hub:4
        ports: ["4444:4444"]
      chrome:
        image: selenium/node-chrome:4
        shm_size: 2gb
        depends_on: [selenium-hub]
        environment: [SE_EVENT_BUS_HOST=selenium-hub]
      edge:
        image: selenium/node-edge:4
        shm_size: 2gb
        depends_on: [selenium-hub]
        environment: [SE_EVENT_BUS_HOST=selenium-hub]
    ```

    将你的 WebDriver 测试指向 `http://localhost:4444/wd/hub` 并并行运行测试套件。

---

# 8) CI“默认并行”

* 使用 **矩阵** 任务（Chrome/Edge）并并行运行你的 Playwright/Cypress 冒烟测试。
* 快速失败以节省时间；为失败的浏览器附加 **追踪记录/视频**。
* 每晚运行一组稍广的测试，并在两个浏览器上运行 **Lighthouse** 检查。

---

# 9) 出现差异时的快速排查

* 从每个浏览器获取 **HAR** 文件，对比响应（状态码、头部、缓存）。
* 对比故障元素的 **计算样式**（开发者工具 → 样式 → 计算样式）。
* 切换 **减弱动画效果** 和 **强制颜色** 以发现可访问性 CSS 问题。
* 清除 **站点数据**（应用面板）并重新测试，以排除过时的 Service Worker/缓存。

---

# 10) 需保留的最少工件

* 一份 **共享的检查清单** (markdown)，记录你的跨浏览器检查项。
* 一个 **版本记录**：应用提交哈希、Chrome/Edge 版本、操作系统、重要标志。
* 为你接受为“不予修复”的任何视觉差异附上 **截图**（相同视口）。

---

如果你需要，我可以为你的 Angular 应用生成一个可立即运行的 **Playwright 骨架项目**（包含 `npm scripts`、CI 矩阵和两个冒烟测试用例），或者一个针对你的开发服务器环境定制的 **Browsersync 脚本**。
