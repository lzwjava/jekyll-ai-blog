---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Ubuntu Proxy Bypass Hosts Configuration
translated: false
type: note
---

### Setting Multiple Hosts in Ubuntu's Manual Proxy Settings

In Ubuntu's manual proxy configuration (found under **Settings > Network > Network Proxy > Manual**), the "Ignore hosts" field allows you to specify a semicolon-separated list of hosts, domains, or IP ranges to bypass the proxy. This is commonly used for local traffic like localhost or internal networks. You can't set these as the *proxy server* address (which expects a single host:port), but they fit perfectly in "Ignore hosts."

#### Steps to Configure via GUI

1. Open **Settings** (search for it in the Activities overview).
2. Go to **Network** > **Network Proxy**.
3. Set the method to **Manual**.
4. In the **Ignore hosts** field, enter your list separated by semicolons (no spaces around them):

   ```
   localhost;127.0.0.1;192.168.1.1;192.168.2.1;::1
   ```

   - `localhost`: Resolves to loopback addresses.
   - `127.0.0.1`: IPv4 loopback.
   - `192.168.1.1` and `192.168.2.1`: Specific local IPs (add as many as needed).
   - `::1`: IPv6 loopback.

5. Click **Apply** to save. This applies system-wide (affects apps like browsers, apt, etc.).

#### Using Wildcards like `192.168.1.*`

- Direct wildcards (e.g., `192.168.1.*`) are **not supported** in the "Ignore hosts" field—it's designed for exact hosts, domain suffixes (e.g., `*.local`), or CIDR notation for IP ranges.
- Instead, use **CIDR notation** for ranges:
  - For `192.168.1.*` (all IPs in the 192.168.1.0/24 subnet), use `192.168.1.0/24`.
  - Example updated list:

    ```
    localhost;127.0.0.1;::1;192.168.1.0/24;192.168.2.1
    ```

  - For broader local networks, add `10.0.0.0/8;172.16.0.0/12;192.168.0.0/16` (common private ranges).

#### Command-Line Alternative (for Scripting or Precision)

If you prefer terminal (or need to automate), use `gsettings` (modern Ubuntu) or edit `/etc/environment` for system-wide:

- View current ignore list:

  ```
  gsettings get org.gnome.system.proxy ignore-hosts
  ```

- Set the list (replace with your values):

  ```
  gsettings set org.gnome.system.proxy ignore-hosts "['localhost', '127.0.0.1', '::1', '192.168.1.0/24', '192.168.2.1']"
  ```

- For permanent env var (affects some apps): Add to `/etc/environment`:

  ```
  no_proxy="localhost,127.0.0.1,::1,192.168.1.0/24,192.168.2.1"
  ```

  Then reboot or run `source /etc/environment`.

Test by pinging a listed host or checking proxy behavior in a browser. If issues arise (e.g., with specific apps), the env var method often covers more ground.

[Setting up proxy to ignore all local addresses](https://askubuntu.com/questions/11274/setting-up-proxy-to-ignore-all-local-addresses)
[How to Configure Proxy Settings on Ubuntu](https://phoenixnap.com/kb/ubuntu-proxy-settings)
[Set a network range in the no_proxy environment variable](https://unix.stackexchange.com/questions/23452/set-a-network-range-in-the-no-proxy-environment-variable)
