---
audio: false
generated: true
lang: en
layout: post
title: Log User-Agent in Clash Proxy
translated: false
type: note
---

It seems you're referring to **Clash**, a rule-based proxy utility, and want to configure it to print or log the **User-Agent** of its HTTP requests. Based on available information, Clash (or its core, often referred to as `clash-core`) doesn't have a built-in feature to directly print the User-Agent of outgoing requests in a straightforward way. However, you can achieve this by leveraging Clash's configuration options, external tools, or debugging methods. Below is a step-by-step guide to help you log or inspect the User-Agent of requests made through Clash.

---

### Understanding the Context
- **Clash** is a proxy utility that routes traffic based on rules and supports protocols like HTTP, SOCKS5, Shadowsocks, V2Ray, and more. It operates at the network and application layers.
- The **User-Agent** is an HTTP header typically set by the client application (e.g., a browser or a tool like `curl`) making the request, not by Clash itself. Clash, as a proxy, forwards these requests and may not inherently log or modify the User-Agent unless explicitly configured to do so.
- To print the User-Agent, you need to either:
  1. Configure Clash to log HTTP headers (including User-Agent) for debugging.
  2. Use an external tool (e.g., a proxy debugger or network sniffer) to inspect the requests.
  3. Modify the Clash configuration to add custom headers or use a script to log them.

Since Clash itself does not have a direct configuration to log User-Agent headers, you may need to combine Clash with other tools or use specific configurations. Below are the methods to achieve this.

---

### Method 1: Enable Detailed Logging in Clash and Inspect Logs
Clash can log requests at various levels, but it doesn't natively log HTTP headers like User-Agent unless explicitly configured or used with a tool that can inspect the traffic. You can enable detailed logging and use a tool to capture the User-Agent.

#### Steps:
1. **Set Clash Log Level to Debug**:
   - Edit your Clash configuration file (`config.yaml`, typically located at `~/.config/clash/config.yaml` or a custom directory specified with the `-d` flag).
   - Set the `log-level` to `debug` to capture detailed information about requests:
     ```yaml
     log-level: debug
     ```
   - Save the configuration and restart Clash:
     ```bash
     clash -d ~/.config/clash
     ```
   - Clash will now log more detailed information to `STDOUT` or a specified log file. However, this may not include the User-Agent header directly, as Clash focuses on routing and connection details.

2. **Inspect Logs**:
   - Check the logs output in the terminal or the log file (if configured). Look for HTTP request details, but note that Clash's default logging may not include full HTTP headers like User-Agent.
   - If you don't see User-Agent information, proceed to use a debugging proxy (see Method 2) or network sniffer (Method 3).

3. **Optional: Use Clash Dashboard**:
   - Clash provides a web-based dashboard (e.g., YACD at `https://yacd.haishan.me/` or the official dashboard at `https://clash.razord.top/`) to monitor connections and logs.
   - Configure the `external-controller` and `external-ui` in your `config.yaml` to enable the dashboard:
     ```yaml
     external-controller: 127.0.0.1:9090
     external-ui: folder
     ```
   - Access the dashboard via `http://127.0.0.1:9090/ui` and check the "Logs" or "Connections" tab. This may show connection details but is unlikely to display the User-Agent directly.

#### Limitations:
- Clash's debug logs focus on routing and proxy decisions, not full HTTP headers. To capture the User-Agent, you need to intercept the HTTP traffic, which requires additional tools.

---

### Method 2: Use a Debugging Proxy to Capture User-Agent
Since Clash itself doesn't directly log HTTP headers like User-Agent, you can route Clash's traffic through a debugging proxy like **mitmproxy**, **Charles Proxy**, or **Fiddler**. These tools can intercept and display the full HTTP request, including the User-Agent.

#### Steps:
1. **Install mitmproxy**:
   - Install `mitmproxy`, a popular open-source tool for intercepting HTTP/HTTPS traffic:
     ```bash
     sudo apt install mitmproxy  # On Debian/Ubuntu
     brew install mitmproxy      # On macOS
     ```
   - Alternatively, use another proxy tool like Charles or Fiddler.

2. **Configure Clash to Route Traffic Through mitmproxy**:
   - By default, Clash acts as an HTTP/SOCKS5 proxy. You can chain it to `mitmproxy` by setting `mitmproxy` as the upstream proxy.
   - Edit your Clash `config.yaml` to include an HTTP proxy that points to `mitmproxy`:
     ```yaml
     proxies:
       - name: mitmproxy
         type: http
         server: 127.0.0.1
         port: 8080  # Default mitmproxy port
     proxy-groups:
       - name: Proxy
         type: select
         proxies:
           - mitmproxy
     ```
   - Save the configuration and restart Clash.

3. **Start mitmproxy**:
   - Run `mitmproxy` to listen on port 8080:
     ```bash
     mitmproxy
     ```
   - `mitmproxy` will display all HTTP requests passing through it, including the User-Agent header.

4. **Send a Test Request**:
   - Use a client (e.g., `curl`, a browser, or another tool) configured to use Clash as a proxy.
   - Example with `curl`:
     ```bash
     curl --proxy http://127.0.0.1:7890 http://example.com
     ```
   - In `mitmproxy`, you’ll see the full HTTP request, including the User-Agent (e.g., `curl/8.0.1` or the browser’s User-Agent).

5. **Inspect User-Agent**:
   - In the `mitmproxy` interface, navigate through the captured requests. The User-Agent header will be visible in the request details.
   - You can also save the logs to a file for further analysis:
     ```bash
     mitmproxy -w mitmproxy.log
     ```

#### Notes:
- If you’re using HTTPS, you need to install and trust the `mitmproxy` CA certificate on your client device to decrypt HTTPS traffic. Follow the instructions at `http://mitm.clash/cert.crt` or `mitmproxy`’s documentation.
- This method requires chaining proxies (Client → Clash → mitmproxy → Destination), which may slightly increase latency but allows full inspection of headers.

---

### Method 3: Use a Network Sniffer to Capture User-Agent
If you prefer not to chain proxies, you can use a network sniffer like **Wireshark** to capture and inspect the HTTP traffic passing through Clash.

#### Steps:
1. **Install Wireshark**:
   - Download and install Wireshark from [wireshark.org](https://www.wireshark.org/).
   - On Linux:
     ```bash
     sudo apt install wireshark
     ```
   - On macOS:
     ```bash
     brew install wireshark
     ```

2. **Start Clash**:
   - Ensure Clash is running with your desired configuration (e.g., HTTP proxy on port 7890):
     ```bash
     clash -d ~/.config/clash
     ```

3. **Capture Traffic in Wireshark**:
   - Open Wireshark and select the network interface that Clash is using (e.g., `eth0`, `wlan0`, or `lo` for localhost traffic).
   - Apply a filter to capture HTTP traffic:
     ```
     http
     ```
   - Alternatively, filter by the Clash HTTP proxy port (e.g., 7890):
     ```
     tcp.port == 7890
     ```

4. **Send a Test Request**:
   - Use a client configured to use Clash as a proxy:
     ```bash
     curl --proxy http://127.0.0.1:7890 http://example.com
     ```

5. **Inspect User-Agent**:
   - In Wireshark, look for HTTP requests (e.g., `GET / HTTP/1.1`). Double-click a packet to view its details.
   - Expand the “Hypertext Transfer Protocol” section to find the `User-Agent` header (e.g., `User-Agent: curl/8.0.1`).

#### Notes:
- For HTTPS traffic, Wireshark cannot decrypt the User-Agent unless you have the server’s private key or use a tool like `mitmproxy` to decrypt the traffic.
- This method is more complex and requires familiarity with network packet analysis.

---

### Method 4: Modify Clash Configuration to Inject or Log Custom Headers
Clash supports custom HTTP headers in its configuration for certain proxy types (e.g., HTTP or VMess). You can configure Clash to inject a specific User-Agent or use a script to log headers. However, this is less direct for logging the User-Agent of all requests.

#### Steps:
1. **Add Custom User-Agent Header**:
   - If you want to force a specific User-Agent for testing, modify the `proxies` section in `config.yaml` to include a custom header:
     ```yaml
     proxies:
       - name: my-http-proxy
         type: http
         server: proxy.example.com
         port: 8080
         header:
           User-Agent:
             - "MyCustomUserAgent/1.0"
     ```
   - This sets a custom User-Agent for requests sent through this proxy. However, it overrides the client’s original User-Agent, which may not be what you want if you’re trying to log the client’s User-Agent.

2. **Use Script Rules to Log Headers**:
   - Clash supports script-based rules using engines like `expr` or `starlark` (). You can write a script to log or process headers, including User-Agent.[](https://pkg.go.dev/github.com/yaling888/clash)
   - Example configuration:
     ```yaml
     script:
       engine: starlark
       code: |
         def match(req):
           print("User-Agent:", req.headers["User-Agent"])
           return "Proxy"  # Route to a proxy group
     ```
   - This requires writing a custom script, which is advanced and may not be fully supported in all Clash versions. Check the Clash documentation for script support.

3. **Verify with mitmproxy or Wireshark**:
   - After injecting a custom User-Agent, use Method 2 or Method 3 to confirm that the User-Agent is being sent as expected.

#### Limitations:
- Injecting a custom User-Agent overrides the client’s User-Agent, so this is only useful for testing specific User-Agents.
- Script-based logging is experimental and may not be available in all Clash versions.

---

### Method 5: Use Clash’s MITM Proxy to Log Headers
Clash supports a **Man-in-the-Middle (MITM)** proxy mode that can intercept and log HTTPS traffic, including headers like User-Agent.

#### Steps:
1. **Enable MITM in Clash**:
   - Edit `config.yaml` to enable the MITM proxy:
     ```yaml
     mitm-port: 7894
     mitm:
       hosts:
         - "*.example.com"
     ```
   - This configures Clash to intercept HTTPS traffic for specified domains.

2. **Install Clash’s CA Certificate**:
   - Clash generates a CA certificate for MITM. Access `http://mitm.clash/cert.crt` in a browser to download and install it.
   - Trust the certificate on your client device to allow Clash to decrypt HTTPS traffic.

3. **Inspect Logs**:
   - With MITM enabled, Clash may log more detailed request information, including headers. Check the logs in the terminal or dashboard.
   - If headers are not logged, use `mitmproxy` (Method 2) to capture the decrypted traffic.

#### Notes:
- MITM mode requires trusting the CA certificate on all client devices, which may not be practical for all use cases.
- This method is best for HTTPS traffic but requires additional setup.

---

### Recommendations
- **Preferred Method**: Use **Method 2 (mitmproxy)** for the easiest and most reliable way to capture and log the User-Agent of requests. It’s open-source, widely supported, and designed for HTTP debugging.
- **Alternative**: Use **Method 3 (Wireshark)** if you’re comfortable with network packet analysis and don’t want to chain proxies.
- **For Advanced Users**: Experiment with **Method 4 (Custom Headers or Scripts)** if you need to programmatically manipulate or log headers within Clash.

---

### Additional Notes
- **Clash Documentation**: Refer to the official Clash documentation (,) for configuration details. The GitHub repository (`https://github.com/Dreamacro/clash`) and wiki (`https://en.clash.wiki`) provide detailed guidance.[](https://en.clash.wiki/)[](https://en.clash.wiki/configuration/getting-started.html)
- **Client-Side User-Agent**: The User-Agent is set by the client (e.g., browser, `curl`, or application), not Clash. Ensure your client is sending the expected User-Agent. For example:
  - `curl` uses `curl/<version>` by default.
  - Browsers use their own User-Agent strings (e.g., `Mozilla/5.0 ...`).
- **Testing**: Always test with a simple HTTP request (e.g., `curl --proxy http://127.0.0.1:7890 http://example.com`) to verify the setup.
- **Security**: When using MITM or debugging proxies, ensure you trust the CA certificates and tools to avoid security risks.

If you need further clarification or assistance with specific configurations, please provide more details about your setup (e.g., Clash version, operating system, or specific proxy type), and I can tailor the instructions further!
