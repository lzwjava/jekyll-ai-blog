---
audio: false
generated: true
lang: zh
layout: post
title: 优化Jekyll GitHub Pages上的gtag.js性能
translated: true
type: note
---

在使用Jekyll构建的GitHub Pages网站上使用`gtag.js`存在一些特殊限制，因为GitHub Pages的服务器端控制有限，无法直接访问缓存头或服务器端脚本。不过，您仍然可以通过客户端技术和Jekyll特定配置来优化`https://www.googletagmanager.com/gtag/js?id=UA-66656236-1`的加载速度。以下是针对此场景的性能优化策略：

---

### 1. **异步加载`gtag.js`**
确保`gtag.js`脚本异步加载以避免阻塞页面渲染。在Jekyll站点中：
- 将脚本添加到Jekyll布局或包含文件中（例如`_includes/analytics.html`或直接放入`default.html`布局）
- 使用`async`属性：
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-66656236-1"></script>
```
- 将此代码置于Jekyll模板的`<head>`或`</body>`前（如`_layouts/default.html`）：
```html
<head>
  <script async src="https://www.googletagmanager.com/gtag/js?id=UA-66656236-1"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'UA-66656236-1');
  </script>
</head>
```
- **优化原理**：`async`可确保脚本不阻塞HTML解析，降低感知加载时间

---

### 2. **添加Google域名的预连接**
通过为`googletagmanager.com`添加`preconnect`提示来减少DNS查询和连接延迟。在Jekyll布局中（`_layouts/default.html`或`_includes/head.html`）：
```html
<link rel="preconnect" href="https://www.googletagmanager.com" crossorigin>
```
- 将此代码置于`<head>`中`gtag.js`脚本之前
- **优化原理**：提前初始化DNS解析和TCP连接，加速`gtag.js`获取

---

### 3. **延迟加载`gtag.js`**
由于GitHub Pages是静态站点，可通过延迟加载优先处理关键内容。将以下JavaScript添加到Jekyll模板或独立JS文件（如`assets/js/analytics.js`）：
```javascript
window.addEventListener('load', () => {
  const script = document.createElement('script');
  script.src = 'https://www.googletagmanager.com/gtag/js?id=UA-66656236-1';
  script.async = true;
  document.head.appendChild(script);
  script.onload = () => {
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'UA-66656236-1');
  };
});
```
- 在Jekyll布局中包含此脚本：
{% raw %}
```html
<script src="{{ '/assets/js/analytics.js' | relative_url }}"></script>
```
{% endraw %}
- **优化原理**：延迟加载`gtag.js`直到页面关键资源（如HTML、CSS）加载完成，提升初始页面速度

---

### 4. **通过Cloudflare使用CDN代理**
GitHub Pages不支持自定义缓存头，但可通过Cloudflare等CDN代理将`gtag.js`缓存至用户附近：
1. **设置Cloudflare**：
   - 将GitHub Pages站点添加到Cloudflare（如`username.github.io`）
   - 为域名启用Cloudflare DNS和代理服务
2. **代理`gtag.js`**：
   - 在Cloudflare创建页面规则缓存该脚本，或在Jekyll站点的`_site`文件夹中托管本地副本（如`assets/js/gtag.js`）
   - 更新脚本标签：
{% raw %}
```html
<script async src="{{ '/assets/js/gtag.js' | relative_url }}"></script>
```
{% endraw %}
   - 定期同步本地副本与Google官方脚本（手动或通过CI/CD脚本）
3. **缓存设置**：
   - 在Cloudflare中为脚本设置缓存规则（如`Cache Everything`并配置1小时TTL）
- **优化原理**：Cloudflare边缘服务器通过就近提供服务降低延迟
- **注意**：代理Google脚本需谨慎，因其可能频繁更新。请充分测试确保跟踪功能正常

---

### 5. **优化Jekyll构建与交付**
确保Jekyll站点经过优化以最小化整体页面加载时间，间接提升`gtag.js`性能：
- **资源压缩**：
  - 使用`jekyll-compress`或`jekyll-minifier`等插件压缩HTML/CSS/JS
  - 在`_config.yml`中添加：
```yaml
plugins:
  - jekyll-compress
```
- **启用Gzip压缩**：
  - GitHub Pages自动为支持的文件启用Gzip，但需通过浏览器开发者工具检查`Content-Encoding`头确认CSS/JS文件已压缩
- **减少阻塞资源**：
  - 最小化在`gtag.js`之前加载的渲染阻塞CSS/JS文件数量
  - 使用`jekyll-assets`等工具优化资源交付：
```yaml
plugins:
  - jekyll-assets
```
- **内联关键CSS**：
  - 在`<head>`中内联关键CSS并延迟非关键CSS，减少渲染阻塞时间
- **图片优化**：
  - 使用`jekyll-picture-tag`等插件压缩图片，减轻页面负载

---

### 6. **切换至轻量级分析工具**
若`gtag.js`仍速度缓慢或分析功能非核心需求：
- 考虑改用Plausible或Fathom等轻量级方案（脚本体积约1KB，而`gtag.js`约50KB）
- Plausible示例：
```html
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/plausible.js"></script>
```
- 将此代码添加到Jekyll的`_includes/analytics.html`并在布局中包含
- **优化原理**：更小的脚本在GitHub Pages静态基础设施上加载更快

---

### 7. **测试与监控性能**
- **测量加载时间**：
  - 使用Chrome开发者工具（网络面板）检查`gtag.js`加载时间
  - 通过Lighthouse或WebPageTest评估整体页面性能
- **模拟用户位置**：
  - 使用Pingdom等工具从目标用户所在区域测试加载时间
- **监控真实用户指标**：
  - 通过Google Analytics的网站速度报告跟踪`gtag.js`影响
- **Jekyll特定调试**：
  - 运行`jekyll build --profile`识别可能间接影响性能的慢速构建组件

---

### 8. **GitHub Pages局限性**
- **无服务器端控制**：无法实现服务器端标记或自定义缓存头
- **不支持HTTP/3**：当前使用HTTP/2，Cloudflare等CDN可升级至HTTP/3
- **地理延迟**：服务器主要位于美国，远离美国的用户可能加载较慢

---

### Jekyll配置示例
以下是结合`preconnect`和`async`的`_includes/analytics.html`示例：
```html
<link rel="preconnect" href="https://www.googletagmanager.com" crossorigin>
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-66656236-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'UA-66656236-1');
</script>
```
在布局文件中引入（`_layouts/default.html`）：
```html
<head>
</head>
```

---

### 后续步骤
- **性能测试**：提供当前`gtag.js`加载时间（来自开发者工具）或站点URL以便深入分析
- **地域背景**：说明主要用户群体所在地（如美国、欧洲、亚洲）以便定制CDN方案
- **Cloudflare配置**：如需使用Cloudflare代理，可提供详细设置指南
- **替代方案**：如需切换分析工具，可推荐具体轻量级方案及其Jekyll集成方法

是否需要重点关注某个方面或执行特定分析（如测试站点性能或提供Cloudflare设置指南）？
