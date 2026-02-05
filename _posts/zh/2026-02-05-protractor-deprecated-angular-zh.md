---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Protractor 已弃用的 Angular 测试框架
translated: true
type: note
---

啊，**Protractor**！现在明白了。

## Protractor 是什么：

**Protractor** 是一个专门为测试 **Angular 和 AngularJS applications** 设计的 **end-to-end (E2E) testing framework**。它是构建在 WebDriverJS (Node.js 版的 Selenium WebDriver) 之上的。

### 主要特性：
- 自动化浏览器测试 (Chrome, Firefox, Safari 等)
- 专为 Angular apps 设计，内置对 Angular-specific locators 的支持
- 允许你编写测试来模拟用户交互 (clicking, typing, navigating)
- 能够自动等待 Angular 完成 rendering 后再继续执行测试

## 重要提示：Protractor 已 **deprecated** ⚠️

Angular 团队在 **2021 年 4 月** 正式宣布弃用 Protractor，并在 2023 年停止了支持。他们建议迁移到现代的替代方案。

### 为什么它需要 requesting libraries 和 form-data：

Protractor 需要这些是因为：

1. **WebDriver communication** - 它必须向 WebDriver server (Selenium) 发送 HTTP requests 来控制浏览器
2. **测试中的 File uploads** - 在测试文件上传功能时，它需要 `form-data` 来构建 multipart requests
3. **API testing** - 有时 E2E tests 需要在浏览器自动化的同时进行直接的 API calls
4. **Screenshot/file handling** - 管理测试产物，如 screenshots 和 reports

## 推荐使用的现代替代方案：

- **Cypress** - 非常流行，具有极佳的 developer experience
- **Playwright** - Microsoft 的解决方案，支持多种浏览器
- **WebdriverIO** - 现代的基于 WebDriver 的 framework
- **TestCafe** - 无需 WebDriver

你是在进行从 Protractor 迁出的工作，还是为了维护 legacy tests 而在学习它？