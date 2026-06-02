---
audio: false
generated: true
lang: zh
layout: post
title: 李智维：从美钛技术服务到趣直播，一位创业者的转型之路
translated: true
type: note
---

### 检测用户国家或语言偏好

由于您的 Jekyll 博客是静态的（生成的 HTML/JS），在没有集成支持此功能的主机平台（例如 Netlify 函数或功能受限的 GitHub Pages）的情况下，很难轻松实现服务器端检测。最佳方法是在页面加载时进行客户端 JavaScript 检测。您有两个主要选择：

1. **浏览器语言偏好**（推荐用于您的用例）：通过 `navigator.language` 或 `navigator.languages` 检测用户浏览器设置中的首选语言。这种方法快速、无需外部 API、尊重用户隐私（不共享 IP），并且直接与语言而非国家/地区关联。国家/地区通常使用多种语言（例如印度广泛使用英语和印地语），因此对于自动设置下拉菜单而言更为准确。

2. **基于 IP 的国家检测**：使用免费的地理定位 API 从用户 IP 地址获取国家/地区，然后将其映射到语言。如果您特别需要国家/地区信息（例如用于分析），这很有用，但它需要外部获取、可能涉及隐私问题且并不总是精确（VPN、代理）。将国家/地区映射到语言是近似方法。

您的目标似乎是自动选择 `<select id="sort-select">` 下拉菜单中的语言（例如，英语为 'date-desc|en'）。我将提供两种方法的代码，您可以将其添加到 `<script>` 标签内，紧接在 `const sortSelect = document.getElementById('sort-select');` 之后。

优先检查 `localStorage`（正如您的代码已经做的），如果没有保存的偏好，则回退到检测。

#### 选项 1：使用浏览器语言（更简单且首选）

添加此代码片段。它检查 `navigator.language` 中的主要语言代码（例如 'en-US' -> 'en'，'zh-CN' -> 'zh'）并将其映射到您的下拉菜单值。如果不匹配，则默认为英语。

```javascript
// 在 window.addEventListener('load', function () { ... }); 内部

// 在 const sortSelect = ...; 之后

// 如果 localStorage 中有保存的值，则恢复
const savedSort = localStorage.getItem('sortOption');
if (savedSort) {
  sortSelect.value = savedSort;
} else {
  // 如果没有保存的偏好，则检测浏览器语言
  let lang = navigator.language.toLowerCase().split('-')[0]; // 例如 'en-US' -> 'en'

  // 对中文变体进行特殊处理（繁体中文为 zh-Hant）
  if (lang === 'zh') {
    const fullLang = navigator.language.toLowerCase();
    if (fullLang.includes('tw') || fullLang.includes('hk') || fullLang.includes('hant')) {
      lang = 'hant';
    } else {
      lang = 'zh'; // 简体中文
    }
  }

  // 映射到您的下拉选项（根据需要添加更多）
  const langMap = {
    'en': 'date-desc|en',
    'zh': 'date-desc|zh',
    'ja': 'date-desc|ja',
    'es': 'date-desc|es',
    'hi': 'date-desc|hi',
    'fr': 'date-desc|fr',
    'de': 'date-desc|de',
    'ar': 'date-desc|ar',
    'hant': 'date-desc|hant'
  };

  sortSelect.value = langMap[lang] || 'date-desc|en'; // 默认为英语
}

updatePosts();
```

这在加载时同步运行，因此没有延迟。通过更改浏览器语言设置（例如在 Chrome 中：设置 > 语言）进行测试。

#### 选项 2：使用基于 IP 的国家检测

这需要异步获取免费 API。我推荐 `country.is`，因为它简单且仅返回国家代码（例如 {country: 'US'}）。它是免费的，无需 API 密钥，并且是开源的。

添加此代码。注意：它是异步的，因此我们使用 `await` 并将其包装在异步函数中以避免阻塞 UI。如果获取失败（例如被广告拦截器阻止），则默认为英语。

```javascript
// 在 window.addEventListener('load', async function () { ... }); 内部 // 使 load 处理程序异步

// 在 const sortSelect = ...; 之后

// 如果 localStorage 中有保存的值，则恢复
const savedSort = localStorage.getItem('sortOption');
if (savedSort) {
  sortSelect.value = savedSort;
  updatePosts();
} else {
  try {
    // 获取国家代码
    const response = await fetch('https://country.is/');
    const data = await response.json();
    const country = data.country.toUpperCase(); // 例如 'US'

    // 将国家代码映射到您的语言（ISO 3166-1 alpha-2 代码）
    // 这是近似映射；根据需要扩展（例如，每种语言对应多个国家）
    const countryLangMap = {
      'US': 'date-desc|en',  // 美国 -> 英语
      'GB': 'date-desc|en',  // 英国 -> 英语
      'CN': 'date-desc|zh',  // 中国 -> 简体中文
      'TW': 'date-desc|hant', // 台湾 -> 繁体中文
      'HK': 'date-desc|hant', // 香港 -> 繁体中文
      'JP': 'date-desc|ja',  // 日本 -> 日语
      'ES': 'date-desc|es',  // 西班牙 -> 西班牙语
      'MX': 'date-desc|es',  // 墨西哥 -> 西班牙语（拉丁美洲示例）
      'IN': 'date-desc|hi',  // 印度 -> 印地语
      'FR': 'date-desc|fr',  // 法国 -> 法语
      'DE': 'date-desc|de',  // 德国 -> 德语
      'SA': 'date-desc|ar',  // 沙特阿拉伯 -> 阿拉伯语
      'AE': 'date-desc|ar'   // 阿联酋 -> 阿拉伯语
    };

    sortSelect.value = countryLangMap[country] || 'date-desc|en'; // 默认为英语
  } catch (error) {
    console.warn('国家检测失败:', error);
    sortSelect.value = 'date-desc|en'; // 回退
  }

  updatePosts();
}
```

- **注意事项**：
  - 如图所示，将 `window.addEventListener` 更新为 `async function ()`。
  - 关于隐私：如果需要（例如欧盟的 GDPR），请告知用户。某些浏览器/API 可能会阻止跨域请求；请彻底测试。
  - 如果您更喜欢其他 API，替代方案包括 `https://ip-api.com/json/`（返回更多数据，如 `{ "countryCode": "US" }`）或 `https://ipgeolocation.io/ip_location/`（注册免费套餐）。
  - 速率限制：对于个人博客来说这些 API 很慷慨，但如果流量增长，请监控。

#### 其他考虑因素

- **回退和用户覆盖**：用户可以随时更改下拉菜单，并且它会保存到 localStorage。如果自动检测并不总是需要，您可以添加一个“检测语言”按钮。
- **测试**：使用 VPN 模拟不同国家/地区，或使用浏览器扩展伪装语言。
- **隐私**：浏览器语言风险较低。对于基于 IP 的方法，如果您的受众敏感，请考虑添加同意提示。
- **结合两者**：首先使用浏览器语言，如果与您支持的语言不匹配，则使用 IP（但保持简单）。
- **Jekyll 特定**：无需更改 Jekyll 配置。如果您在 Netlify/Vercel 上托管，可以使用边缘函数进行服务器端检测，但这对于当前需求来说过于复杂。

如果这不起作用或者您可以分享错误信息，请提供更多详细信息！

[Country.is API](https://country.is/)
[IP-API 地理定位](https://ip-api.com/)
[ipgeolocation.io](https://ipgeolocation.io/)
