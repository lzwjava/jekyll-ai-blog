---
audio: false
generated: true
lang: zh
layout: post
title: 使用Google Analytics
translated: true
type: note
---

要使用 Google Analytics，请将其集成到您的前端项目中，并通过应用和网站查看数据。请按照以下步骤操作。本指南假设您的前端项目是网站或移动应用，并使用 **Google Analytics 4 (GA4)**——这是 2023 年的现行标准，因为 Universal Analytics 已不再支持新数据收集。

---

### 1. 设置 Google Analytics

在将 Google Analytics 集成到项目之前，您需要创建一个账户并进行配置：

- **创建账户**：访问 [analytics.google.com](https://analytics.google.com)，如果没有 Google 账户，请先注册。
- **创建 GA4 媒体资源**：
  - 点击左下角的“管理”。
  - 在“媒体资源”下，点击“创建媒体资源”，填写项目详细信息，并选择 **Google Analytics 4**。
- **添加数据流**：根据您的前端项目类型：
  - **对于网站**：选择“网站”，输入网站 URL，并为数据流命名（例如“我的网站”）。
  - **对于移动应用**：选择“应用”，选择 iOS 或 Android，并提供应用详细信息（例如包名）。

设置数据流后，您将获得一个 **衡量 ID**（例如 `G-XXXXXXXXXX`），用于集成。

---

### 2. 将 Google Analytics 集成到您的前端项目

集成过程取决于您的前端项目是网站还是移动应用。

#### 对于网站

- **添加 Google 代码**：
  - 在 GA4 媒体资源中，转到“数据流”，选择您的网站数据流，找到“代码设置说明”。
  - 复制提供的 **Google 代码**脚本，如下所示：

    ```html
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_MEASUREMENT_ID"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'YOUR_MEASUREMENT_ID');
    </script>
    ```

  - 将此代码粘贴到网站 HTML 的 `<head>` 部分，将 `YOUR_MEASUREMENT_ID` 替换为您的实际衡量 ID。
- **对于单页应用 (SPA)**（例如 React、Angular、Vue）：
  - 默认脚本仅跟踪初始页面加载。对于 SPA（页面在路由更改时不重新加载），请使用库来跟踪导航。例如，在 **React** 中：
    1. 安装 `react-ga4` 库：

       ```bash
       npm install react-ga4
       ```

    2. 在应用中初始化（例如在 `index.js` 或 `App.js` 中）：

       ```javascript
       import ReactGA from 'react-ga4';
       ReactGA.initialize('YOUR_MEASUREMENT_ID');
       ```

    3. 在路由更改时跟踪页面浏览（例如使用 React Router）：

       ```javascript
       ReactGA.send({ hitType: "pageview", page: window.location.pathname });
       ```

       在路由更改时调用此代码，例如在绑定到路由器位置的 `useEffect` 钩子中。
  - 其他框架也有类似的库（例如 Angular 的 `ngx-analytics`、Vue 的 `vue-ga`——请检查 GA4 兼容性）。
- **可选**：使用 **Google 跟踪代码管理器 (GTM)** 代替硬编码代码，以便更轻松地管理跟踪脚本。

#### 对于移动应用

- **使用 Firebase（推荐）**：
  - 如果您的应用使用 Firebase，请启用 **Google Analytics for Firebase**：
    1. 在 [console.firebase.google.com](https://console.firebase.google.com) 创建一个 Firebase 项目。
    2. 将您的应用添加到项目（iOS 或 Android）。
    3. 按照提示下载配置文件（例如 iOS 的 `GoogleService-Info.plist`、Android 的 `google-services.json`）并将其添加到您的应用。
    4. 安装 Firebase SDK：
       - **iOS**：使用 CocoaPods（`pod 'Firebase/Analytics'`）并在 `AppDelegate` 中初始化。
       - **Android**：在 `build.gradle` 中添加依赖项并在应用中初始化。
    5. Firebase 会自动链接到您的 GA4 媒体资源并开始收集数据。
- **不使用 Firebase**：
  - 使用独立的 **Google Analytics SDK**（适用于 iOS 或 Android）（现在较少使用，因为 GA4 已与 Firebase 集成）。请参阅官方文档进行设置，因为设置因平台而异。

---

### 3. 验证集成

- **对于网站**：添加跟踪代码后：
  - 访问您的网站并在 Google Analytics 中打开 **实时** 报告（位于“报告”>“实时”）。
  - 如果您看到您的访问记录，则集成正常工作。
  - 或者，使用浏览器工具（如 **GA Checker** 或 Chrome DevTools 控制台）确认 `gtag` 调用。
- **对于应用**：在安装 SDK 后启动应用，检查 Firebase 控制台或 GA4 实时报告。数据可能需要几分钟才能显示。

---

### 4. 通过应用和网站查看数据

Google Analytics 开始收集数据后，您可以通过两种方式查看：

- **Google Analytics 网页界面**：
  - 登录 [analytics.google.com](https://analytics.google.com)。
  - 选择您的 GA4 媒体资源。
  - 浏览报告，例如：
    - **实时**：查看实时用户活动。
    - **受众群体**：了解用户人口统计信息。
    - **获客**：跟踪用户来源。
    - **行为**：分析用户互动（例如页面浏览、事件）。
- **Google Analytics 移动应用**：
  - 从 App Store（iOS）或 Google Play Store（Android）下载官方 **Google Analytics 应用**。
  - 使用您的 Google 账户登录并选择您的媒体资源。
  - 随时查看部分报告（例如实时、受众群体）。

---

### 补充说明

- **如果您的项目同时包含网站和应用**：您可以在同一 GA4 媒体资源下添加多个数据流（例如一个用于网站，一个用于应用）。这允许您在同一界面中查看合并或分开的分析数据。
- **跟踪事件**：除了页面浏览，还可以使用 `gtag('event', ...)`（对于网站）或 Firebase 的 `logEvent`（对于应用）跟踪自定义事件（例如按钮点击）。网站示例：

  ```javascript
  gtag('event', 'click', {
    'event_category': 'Button',
    'event_label': 'Submit'
  });
  ```

- **GA4 与 Universal Analytics**：对于新项目，请使用 GA4，因为 Universal Analytics 已于 2023 年 7 月 1 日停止处理数据。

通过遵循这些步骤，您将成功将 Google Analytics 集成到您的前端项目中，并能够使用 Google Analytics 网站和移动应用监控用户数据。如果您的项目类型（网站或应用）需要具体说明，请相应调整集成步骤！
