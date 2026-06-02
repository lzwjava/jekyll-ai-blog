---
audio: false
generated: true
lang: en
layout: post
title: Optimizing gtag.js Performance on Jekyll GitHub Pages
translated: false
type: note
---

Using `gtag.js` on a GitHub Pages site built with Jekyll presents some unique constraints, as GitHub Pages has limited server-side control and no direct access to caching headers or server-side scripting. However, you can still optimize the fetch speed of `https://www.googletagmanager.com/gtag/js?id=UA-66656236-1` using client-side techniques and Jekyll-specific configurations. Below are targeted strategies to improve its performance in this context:

---

### 1. **Load `gtag.js` Asynchronously**

Ensure the `gtag.js` script is loaded asynchronously to avoid blocking page rendering. In your Jekyll site:

- Add the script to your Jekyll layout or include file (e.g., `_includes/analytics.html` or directly in your `default.html` layout).
- Use the `async` attribute:

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-66656236-1"></script>
```

- Place this in the `<head>` or just before `</body>` in your Jekyll template (e.g., `_layouts/default.html`):

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

- **Why it helps**: `async` ensures the script doesn’t block HTML parsing, reducing perceived load time.

---

### 2. **Add Preconnect for Google’s Domain**

Reduce DNS lookup and connection latency by adding a `preconnect` hint for `googletagmanager.com`. In your Jekyll layout (`_layouts/default.html` or `_includes/head.html`):

```html
<link rel="preconnect" href="https://www.googletagmanager.com" crossorigin>
```

- Place this in the `<head>` before the `gtag.js` script.
- **Why it helps**: Initiates DNS resolution and TCP connection early, speeding up the fetch of `gtag.js`.

---

### 3. **Lazy-Load `gtag.js`**

Since GitHub Pages is static, you can lazy-load `gtag.js` to prioritize critical content. Add the following JavaScript to your Jekyll template or a separate JS file (e.g., `assets/js/analytics.js`):

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

- Include this script in your Jekyll layout:
{% raw %}

```html
<script src="{{ '/assets/js/analytics.js' | relative_url }}"></script>
```

{% endraw %}

- **Why it helps**: Delays `gtag.js` loading until after the page’s critical resources (e.g., HTML, CSS) are loaded, improving initial page speed.

---

### 4. **Use a CDN Proxy via Cloudflare**

GitHub Pages doesn’t allow custom caching headers, but you can proxy `gtag.js` through a CDN like Cloudflare to cache it closer to your users:

1. **Set up Cloudflare**:
   - Add your GitHub Pages site to Cloudflare (e.g., `username.github.io`).
   - Enable Cloudflare’s DNS and proxying for your domain.
2. **Proxy `gtag.js`**:
   - Create a Page Rule in Cloudflare to cache the `gtag.js` script or host a local copy in your Jekyll site’s `_site` folder (e.g., `assets/js/gtag.js`).
   - Update your script tag:
{% raw %}

```html
<script async src="{{ '/assets/js/gtag.js' | relative_url }}"></script>
```

{% endraw %}

- Sync the local copy with Google’s `gtag.js` periodically to ensure it’s up-to-date (manual process or via a CI/CD script).

3. **Cache Settings**:
   - In Cloudflare, set a cache rule for the script (e.g., `Cache Everything` with a TTL of 1 hour).

- **Why it helps**: Cloudflare’s edge servers reduce latency by serving the script from a location closer to your users.
- **Note**: Be cautious with proxying Google’s scripts, as they may update frequently. Test thoroughly to ensure tracking works.

---

### 5. **Optimize Jekyll Build and Delivery**

Ensure your Jekyll site is optimized to minimize overall page load time, which indirectly helps `gtag.js` performance:

- **Minify Assets**:
  - Use a Jekyll plugin like `jekyll-compress` or `jekyll-minifier` to minify HTML, CSS, and JS.
  - Add to your `_config.yml`:

```yaml
plugins:
  - jekyll-compress
```

- **Enable Gzip Compression**:
  - GitHub Pages automatically enables Gzip for supported files, but confirm your CSS/JS files are compressed by checking the `Content-Encoding` header in browser dev tools.
- **Reduce Blocking Resources**:
  - Minimize the number of render-blocking CSS/JS files loaded before `gtag.js`.
  - Use `jekyll-assets` or similar to optimize asset delivery:

```yaml
plugins:
  - jekyll-assets
```

- **Inline Critical CSS**:
  - Inline critical CSS in the `<head>` and defer non-critical CSS to reduce render-blocking time, which can make `gtag.js` appear to load faster.
- **Image Optimization**:
  - Compress images using `jekyll-picture-tag` or a similar plugin to reduce overall page weight, freeing up bandwidth for `gtag.js`.

---

### 6. **Switch to Minimal Analytics**

If `gtag.js` remains slow or analytics isn’t critical:

- Consider lightweight alternatives like Plausible or Fathom, which use smaller scripts (~1 KB vs. ~50 KB for `gtag.js`).
- Example for Plausible:

```html
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/plausible.js"></script>
```

- Add this to your Jekyll `_includes/analytics.html` and include it in your layout.
- **Why it helps**: Smaller scripts load faster, especially on GitHub Pages’ static infrastructure.

---

### 7. **Test and Monitor Performance**

- **Measure Fetch Time**:
  - Use Chrome DevTools (Network tab) to check `gtag.js` load time.
  - Test with tools like Lighthouse or WebPageTest to assess overall page performance.
- **Simulate User Locations**:
  - Use a tool like Pingdom to test load times from regions where your audience is located, as GitHub Pages and Google’s CDN performance vary geographically.
- **Monitor Real User Metrics**:
  - If using Google Analytics, check the Site Speed report to track `gtag.js` impact.
- **Jekyll-Specific Debugging**:
  - Run `jekyll build --profile` to identify slow-building components in your site that might indirectly affect performance.

---

### 8. **Limitations with GitHub Pages**

- **No Server-Side Control**: GitHub Pages is a static host, so you can’t implement server-side tagging or custom cache headers for `gtag.js`.
- **No HTTP/3**: GitHub Pages uses HTTP/2, which is fast but not as optimized as HTTP/3. A CDN like Cloudflare can upgrade to HTTP/3.
- **Geographic Latency**: GitHub Pages servers are primarily US-based, so users far from the US may experience slower loads. A CDN mitigates this.

---

### Example Jekyll Setup

Here’s a sample `_includes/analytics.html` for your Jekyll site combining `preconnect` and `async`:

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

Include it in your layout (`_layouts/default.html`):

```html
<head>
</head>
```

---

### Next Steps

- **Test Current Performance**: Share the current fetch time for `gtag.js` (from browser dev tools) or your site’s URL, and I can analyze it further.
- **Geographic Context**: Let me know your audience’s primary location (e.g., US, Europe, Asia) to tailor CDN or proxy recommendations.
- **Cloudflare Setup**: If you’re open to using Cloudflare, I can provide detailed steps to proxy `gtag.js`.
- **Alternative Analytics**: If you’re open to switching from Google Analytics, I can recommend specific lightweight tools and their Jekyll integration.

Would you like me to focus on any of these aspects or perform a specific analysis (e.g., test your site’s performance or provide a Cloudflare setup guide)?
