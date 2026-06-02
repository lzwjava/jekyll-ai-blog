---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Express日志代理请求记录
translated: true
type: note
---

若你在 Express 应用中使用 [`http-proxy-middleware`](https://github.com/chimurai/http-proxy-middleware)，可通过其 `onProxyReq` 和 `onProxyRes` 事件钩子记录请求参数与请求体。

以下是一个实用示例：

```js
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();

// 在代理前解析 JSON 请求体
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use('/api', createProxyMiddleware({
  target: 'http://example.com',
  changeOrigin: true,

  // 记录请求体与查询参数
  onProxyReq: (proxyReq, req, res) => {
    // 查询参数
    console.log('Query:', req.query);

    // 请求体（仅当在代理前完成解析时）
    if (req.body && Object.keys(req.body).length) {
      console.log('Body:', req.body);

      // 如需转发请求体（针对 POST/PUT 请求）
      const bodyData = JSON.stringify(req.body);
      proxyReq.setHeader('Content-Type', 'application/json');
      proxyReq.setHeader('Content-Length', Buffer.byteLength(bodyData));
      proxyReq.write(bodyData);
    }
  },

  // 记录目标服务器响应
  onProxyRes: (proxyRes, req, res) => {
    console.log(`目标服务器响应：${proxyRes.statusCode} - ${req.method} ${req.originalUrl}`);
  }
}));

app.listen(3000, () => {
  console.log('代理服务运行于 http://localhost:3000');
});
```

### 关键要点

* **优先解析请求体**：在代理中间件前使用 `express.json()` 或 `express.urlencoded()`，否则 `req.body` 将为空
* **请求体转发**：默认情况下 `http-proxy-middleware` 不会转发已解析的请求体。若需在记录后转发，需要重新序列化并通过 `write()` 写入代理请求
* **查询参数**：直接通过 `req.query` 获取，无需额外处理
* **响应记录**：通过 `onProxyRes` 获取目标服务器响应信息

---

👉 你仅需记录日志用于调试，还是希望代理在记录后转发修改后的请求体？
