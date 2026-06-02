---
audio: false
generated: true
image: false
lang: en
layout: post
title: Logging Proxy Requests in Express
translated: false
type: note
---

If you’re using [`http-proxy-middleware`](https://github.com/chimurai/http-proxy-middleware) in an Express app, you can hook into its `onProxyReq` and `onProxyRes` events to log request parameters and body.

Here’s a practical example:

```js
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();

// Parse JSON body before proxy
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use('/api', createProxyMiddleware({
  target: 'http://example.com',
  changeOrigin: true,

  // Log the request body & query params
  onProxyReq: (proxyReq, req, res) => {
    // Query params
    console.log('Query:', req.query);

    // Body (only if parsed before proxy)
    if (req.body && Object.keys(req.body).length) {
      console.log('Body:', req.body);

      // If you need to forward the body (for POST/PUT)
      const bodyData = JSON.stringify(req.body);
      proxyReq.setHeader('Content-Type', 'application/json');
      proxyReq.setHeader('Content-Length', Buffer.byteLength(bodyData));
      proxyReq.write(bodyData);
    }
  },

  // Log the response from target
  onProxyRes: (proxyRes, req, res) => {
    console.log(`Response from target: ${proxyRes.statusCode} for ${req.method} ${req.originalUrl}`);
  }
}));

app.listen(3000, () => {
  console.log('Proxy running on http://localhost:3000');
});
```

### Key Points

* **Parse body first**: Use `express.json()` or `express.urlencoded()` before the proxy, otherwise `req.body` will be empty.
* **Forwarding body**: By default, `http-proxy-middleware` doesn’t forward parsed bodies. If you log the body and also want it forwarded, you need to re-stringify and `write()` it to the proxied request.
* **Query params**: Available at `req.query`, no extra work needed.
* **Response logging**: Use `onProxyRes` for target server responses.

---

👉 Do you just need logging for debugging, or do you also want the proxy to forward the modified body after logging?
