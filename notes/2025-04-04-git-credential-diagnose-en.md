---
audio: false
generated: true
lang: en
layout: post
title: Git Credential Manager Diagnose
translated: false
type: note
---

The output of `git credential-manager diagnose` now clearly indicates a **networking failure**, in addition to the TLS certificate verification warning. Let's break down the error and how to fix it:

**Key Findings:**

* **Networking Failure:**
  * The diagnostic test failed with the error: `System.Net.Http.HttpRequestException: nodename nor servname provided, or not known (example.com:443)`.
  * This error means that the Git Credential Manager could not resolve the hostname `example.com` to an IP address, or it could not connect to port 443 on that host.
  * The diagnostic log shows that the HEAD request to `https://example.com` failed.
* **Proxy Interference (Likely Cause):**
  * The presence of `HTTP_PROXY: http://127.0.0.1:7890` and `HTTPS_PROXY: http://127.0.0.1:7890` strongly suggests that the proxy is the root cause of the networking failure.
  * The fact that the diagnostic can access [http://httpforever.com](http://httpforever.com), but not [https://example.com](https://example.com), indicates the proxy is having issues with https requests.
* **TLS Certificate Verification Disabled (Security Risk):**
  * As before, the TLS certificate verification is disabled, which is a major security concern.

**Troubleshooting Steps:**

1. **Proxy Verification:**
    * **Test the Proxy:** Open a web browser and try to access `https://example.com` directly. If you encounter a "cannot connect" or "hostname not found" error, your proxy is likely misconfigured.
    * **Proxy Software Issues:**
        * Restart your proxy software (Shadowsocks, Clash, etc.).
        * Check the proxy software's logs for error messages.
        * Ensure that the proxy is configured to handle HTTPS traffic correctly.
        * Ensure the proxy software is running.
    * **Proxy Configuration:**
        * Double-check your proxy settings in your operating system's network preferences and in any Git configuration files.
        * Verify that the proxy address (`127.0.0.1`) and port (`7890`) are correct.
        * Temporarily disable the proxy in your operating system network settings, and retry the git credential manager diagnose.
2. **DNS Resolution:**
    * Although the error message suggests a hostname resolution problem, the proxy is the most likely culprit. However, it's still worth checking your DNS settings.
    * Try using a public DNS server (e.g., 8.8.8.8, 1.1.1.1).
3. **TLS Certificate Verification:**
    * **Re-enable Certificate Verification:** This is crucial for security. Follow the instructions provided in the `https://aka.ms/gcm/tlsverify` link.
    * If your proxy software is designed to intercept HTTPS traffic, make sure to install the proxies root certificate into your operating systems trusted root certificate store. This is the secure way to allow the proxy to work.
4. **Git Configuration:**
    * Run `git config --global --list` to examine your Git configuration.
    * Temporarily remove the proxy settings from Git to isolate the issue:

        ```bash
        git config --global --unset http.proxy
        git config --global --unset https.proxy
        ```

    * After removing the proxy settings, re-run the `git credential-manager diagnose` command.
5. **Firewall:**
    * Temporarily disable any firewalls on your computer, to rule out any firewall interferences.
6. **Network Connection:**
    * Test your network connection using other network applications, to ensure that the network itself is stable.
    * If using a mobile hotspot, move to a location with better signal strength.

**Key Takeaway:** The proxy is almost certainly causing the networking failures. Correctly configuring the proxy and re-enabling TLS certificate verification are the most important steps.
