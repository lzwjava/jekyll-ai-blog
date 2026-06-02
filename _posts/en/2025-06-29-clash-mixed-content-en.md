---
audio: false
generated: true
lang: en
layout: post
title: Fix Clash VPN Mixed Content Errors
translated: false
type: note
---

The error messages you're encountering indicate a **mixed content** issue with the Clash VPN application, specifically when the page at `https://clash.razord.top/` tries to load resources from an insecure `http://127.0.0.1:9090/` endpoint (e.g., `http://127.0.0.1:9090/version`). Modern browsers block such requests because they violate security policies by attempting to load insecure HTTP content on a secure HTTPS page. Additionally, there are CORS (Cross-Origin Resource Sharing) errors due to access control restrictions. Below is a step-by-step guide to resolve this issue.

---

### Why This Happens

- **Mixed Content Error**: The webpage is served over HTTPS, but it’s attempting to fetch resources (like the version check) from `http://127.0.0.1:9090`, which is insecure. Browsers block these requests to prevent potential security vulnerabilities, such as man-in-the-middle attacks.
- **CORS Error**: The browser is blocking the request to `http://127.0.0.1:9090` due to CORS policy, which restricts cross-origin requests unless explicitly allowed by the server.
- **Clash Context**: Clash (or Clash for Windows) is a proxy application that likely uses a local server (`127.0.0.1:9090`) for its dashboard or API. If this local server doesn’t support HTTPS or isn’t configured correctly, it triggers these errors when accessed via an HTTPS webpage.

---

### Steps to Fix the Issue

#### 1. **Verify Clash Core Configuration**

- **Check if Clash Core is Running**: Ensure the Clash core (the backend service) is running on your machine and listening on `127.0.0.1:9090`. You can verify this by:
  - Opening a terminal or command prompt.
  - Running `curl http://127.0.0.1:9090/version` to check if the endpoint responds with the Clash version.
  - If it doesn’t respond, ensure the Clash service is active. Restart Clash for Windows or the Clash core process.
- **Enable HTTPS for Clash Core** (if possible):
  - Some versions of Clash (e.g., Clash Premium or Clash Meta) support HTTPS for the local API. Check the Clash documentation or configuration file (usually `config.yaml`) for an option to enable HTTPS for the external controller (the API endpoint).
  - Look for a setting like `external-controller` or `external-ui` in the configuration file. For example:

       ```yaml
       external-controller: 127.0.0.1:9090
       external-ui: <path-to-ui>
       ```

       If HTTPS is supported, you may need to configure a certificate for the local server. This is advanced and may require generating a self-signed certificate (see step 4 below).

#### 2. **Access the Dashboard via HTTP (Temporary Workaround)**

- If the Clash dashboard can be accessed via HTTP (e.g., `http://clash.razord.top/` instead of HTTPS), try loading it without HTTPS to avoid mixed content issues:
  - Open your browser and navigate to `http://clash.razord.top/`.
  - Note: This is not recommended for production use, as HTTP is insecure. Use this only for testing or if the dashboard is only accessed locally.
- If the dashboard requires HTTPS, proceed to the next steps to address the root cause.

#### 3. **Update URLs to HTTPS**

- The error suggests the Clash dashboard is trying to fetch resources from `http://127.0.0.1:9090`. If you have access to the Clash dashboard’s source code or configuration:
  - Check the frontend code (e.g., `index-5e90ca00.js` or `vendor-827b5617.js`) for hardcoded `http://127.0.0.1:9090` references.
  - Update these to `https://127.0.0.1:9090` if the Clash core supports HTTPS, or use a relative URL (e.g., `/version`) to let the browser use the same protocol as the page.
  - If you don’t have access to the source code, you may need to configure a reverse proxy (see step 4).

#### 4. **Set Up a Reverse Proxy with HTTPS**

- To resolve the mixed content issue, you can set up a reverse proxy (e.g., using Nginx or Caddy) to serve the Clash core API (`http://127.0.0.1:9090`) over HTTPS. This allows the dashboard to communicate with the core securely.
- **Steps for Nginx**:
     1. Install Nginx on your system (if not already installed).
     2. Generate a self-signed SSL certificate for `127.0.0.1`:

        ```bash
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout localhost.key -out localhost.crt -subj "/CN=localhost"
        ```

     3. Configure Nginx to proxy requests to `http://127.0.0.1:9090` over HTTPS. Create a configuration file (e.g., `/etc/nginx/sites-available/clash`):

        ```nginx
        server {
            listen 443 ssl;
            server_name localhost;

            ssl_certificate /path/to/localhost.crt;
            ssl_certificate_key /path/to/localhost.key;

            location / {
                proxy_pass http://127.0.0.1:9090;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
            }
        }
        ```

     4. Enable the configuration and restart Nginx:

        ```bash
        sudo ln -s /etc/nginx/sites-available/clash /etc/nginx/sites-enabled/
        sudo nginx -t
        sudo systemctl restart nginx
        ```

     5. Update the Clash dashboard to use `https://localhost:443` instead of `http://127.0.0.1:9090` for API requests.
     6. In your browser, accept the self-signed certificate when prompted.

- **Alternative with Caddy**: Caddy is simpler to configure and automatically handles HTTPS:
     1. Install Caddy.
     2. Create a `Caddyfile`:

        ```caddy
        localhost:443 {
            reverse_proxy http://127.0.0.1:9090
        }
        ```

     3. Run Caddy: `caddy run`.
     4. Update the Clash dashboard to use `https://localhost:443`.

#### 5. **Bypass CORS Restrictions (Advanced)**

- The CORS error (`XMLHttpRequest cannot load http://127.0.0.1:9090/version due to access control checks`) indicates the Clash core server isn’t sending the appropriate CORS headers. If you control the Clash core:
  - Modify the Clash core configuration to include CORS headers, such as:

       ```yaml
       external-controller: 127.0.0.1:9090
       allow-cors: true
       ```

       (Check the Clash documentation for the exact syntax, as this depends on the Clash version.)
  - Alternatively, the reverse proxy setup in step 4 can handle CORS by adding headers like:

       ```nginx
       add_header Access-Control-Allow-Origin "https://clash.razord.top";
       add_header Access-Control-Allow-Methods "GET, POST, OPTIONS";
       add_header Access-Control-Allow-Headers "*";
       ```

- If you don’t control the core, you can use a browser extension to temporarily bypass CORS (e.g., “CORS Unblock” for Chrome), but this is not recommended for security reasons.

#### 6. **Update Clash or Switch to a Compatible Version**

- Ensure you’re using the latest version of Clash for Windows or Clash Verge, as older versions may have bugs or lack HTTPS support for the external controller.
- Check the Clash GitHub repository (`github.com/Dreamacro/clash` or `github.com/Fndroid/clash_for_windows_pkg`) for updates or reported issues related to mixed content or CORS.
- Consider switching to **Clash Verge** or **Clash Meta**, which may have better support for HTTPS and modern browser security policies.[](https://clashverge.net/en/tutorial-en/)

#### 7. **Allow Insecure Content in Browser (Not Recommended)**

- As a last resort, you can allow insecure content in your browser for `https://clash.razord.top/`:
  - **Chrome**:
       1. Click the lock icon in the address bar.
       2. Go to “Site settings” > “Insecure content” > Set to “Allow.”
  - **Firefox**:
       1. Click the lock icon and go to “Connection settings.”
       2. Disable “Block dangerous and deceptive content” temporarily.
  - **Warning**: This bypasses security protections and should only be used for local testing on trusted networks.
- Alternatively, launch Chrome with the `--disable-web-security` flag (for development only):

     ```bash
     google-chrome --disable-web-security --user-data-dir="/tmp/chrome_dev"
     ```

#### 8. **Check for Conflicting Extensions or Firewall**

- Browser extensions (e.g., ad blockers, privacy tools) or firewall settings may interfere with Clash’s local server. Temporarily disable extensions or check your firewall to ensure `127.0.0.1:9090` is accessible.[](https://vpncentral.com/reddit-blocked-by-network-security/)
- On Windows, ensure the Clash app has firewall permissions:
  - Go to Settings > Network & Internet > Windows Firewall > Allow an app through firewall.
  - Add or enable Clash for Windows.

#### 9. **Contact Clash Support or Community**

- If the above steps don’t resolve the issue, report the problem on the Clash for Windows GitHub issues page (`github.com/Fndroid/clash_for_windows_pkg/issues`) or the Clash community forums. Provide details about your setup, including:
  - Clash version.
  - Operating system.
  - Configuration file (redact sensitive info).
  - Browser and version.
- Check for similar issues in the community, as this error may be specific to certain Clash versions or configurations.[](https://superuser.com/questions/1769163/could-not-switch-to-this-profile-proxy-0-filed-ws-opts-headershost-invalid-c)

---

### Recommended Approach

The most secure and robust solution is to **set up a reverse proxy with HTTPS** (step 4) to ensure all requests are served over HTTPS, resolving both the mixed content and CORS issues. If you’re unable to modify the Clash core or dashboard, using a newer version of Clash (e.g., Clash Verge) or accessing the dashboard via HTTP temporarily (step 2) may be quicker workarounds.

---

### Additional Notes

- If you’re using a custom Clash dashboard or a third-party service like `clash.razord.top`, verify that it’s compatible with your Clash core version.
- Always back up your Clash configuration (`config.yaml`) before making changes.
- If the issue persists, you can try switching to alternative proxy clients like v2rayN or OpenVPN, which may have better HTTPS support for local APIs.[](https://stackoverflow.com/questions/67822697/how-to-route-internet-traffic-via-clash-for-windows-ping-from-python-code-is)

Let me know if you need help with specific steps, such as setting up Nginx or debugging the Clash configuration!
