---
audio: false
generated: true
lang: en
layout: post
title: Why Git Operations Fail on Chinese Mobile Networks
translated: false
type: note
---

This is a common issue when using certain mobile networks in China, especially with services like Git that rely on specific ports and protocols. Here's a breakdown of why it happens and how to fix it:

**Why Git Operations Fail on Chinese Mobile Networks:**

* **Port Blocking/Throttling:**
    * Mobile network operators in China sometimes implement traffic shaping or port blocking, particularly for non-standard ports used by Git (like SSH port 22). This is often done to manage network bandwidth or for security reasons.
    * Even if port 22 is not completely blocked, it might be heavily throttled, leading to extremely slow connections or timeouts, which appear as "stuck" Git operations.
* **DNS Issues:**
    * While you can access websites like GitHub and Google, Git operations rely on resolving specific hostnames (e.g., `github.com`) through DNS. If the DNS resolution is slow or unreliable, it can cause Git to hang.
* **Packet Loss/Latency:**
    * Mobile networks, especially when used as hotspots, can have higher latency and packet loss compared to wired connections. This can disrupt the SSH connection used by Git, leading to failures.
* **Firewall Interference:**
    * China's "Great Firewall" may interfere with SSH connections, even if they are not explicitly blocked. The firewall's deep packet inspection can sometimes cause connection instability.
* **MTU Issues:**
    * Maximum Transmission Unit (MTU) problems can cause issues with data transfer, and mobile networks sometimes have smaller MTU values than wired networks.

**How to Fix Git Push/Pull Issues on Chinese Mobile Networks:**

1.  **Use HTTPS Instead of SSH:**
    * Git over HTTPS uses port 443, which is typically open for web traffic. This is the most reliable workaround.
    * To change your Git remote to HTTPS:
        * Open your terminal.
        * Navigate to your Git repository.
        * Run the following command, replacing `your_username` and `your_repository` with your GitHub details:
            ```bash
            git remote set-url origin https://github.com/your_username/your_repository.git
            ```
    * If you need to provide username and password, you can use git credential helper, or use personal access token.
2.  **Use a VPN:**
    * A reliable VPN can bypass network restrictions and provide a more stable connection.
    * Connect to a VPN server outside of China before attempting Git operations.
    * Be aware that VPNs can also experience instability and speed issues.
3.  **Configure SSH Port (If SSH is Necessary):**
    * If you must use SSH, try configuring Git to use a different port (e.g., 443) that might be less likely to be blocked.
    * Edit your `~/.ssh/config` file:
        ```
        Host github.com
            Hostname ssh.github.com
            Port 443
            User git
        ```
    * Then, change your git remote url to use ssh.github.com:
        ```bash
        git remote set-url origin git@ssh.github.com:your_username/your_repository.git
        ```
4.  **Check MTU Settings:**
    * If you suspect MTU issues, try reducing your MTU size.
    * On macOS, you can use the `networksetup` command to adjust MTU.
    * However, changing MTU is generally a more advanced troubleshooting step and should be done with caution.
5.  **Check DNS Settings:**
    * Try using a public DNS server, like Google DNS (8.8.8.8 and 8.8.4.4) or Cloudflare DNS (1.1.1.1 and 1.0.0.1).
    * You can configure DNS settings in your macOS network preferences.
6.  **Use a Git Proxy:**
    * If you have access to a proxy server, you can configure Git to use it.
    * Set the `http.proxy` and `https.proxy` Git configuration variables:
        ```bash
        git config --global http.proxy http://proxy_address:proxy_port
        git config --global https.proxy https://proxy_address:proxy_port
        ```
    * If the proxy needs authentication, you can include the username and password in the proxy URL.
7.  **Try using SSH over Websockets:**
    * Some tools and services allow you to tunnel SSH traffic over websockets, which can be helpful if standard SSH ports are blocked.
    * This is a more advanced technique and requires setting up a server that supports SSH over websockets.

**Important Considerations:**

* Mobile network conditions can vary significantly, so what works in one location or at one time might not work in another.
* Be aware of the terms of service of your mobile network provider and any potential restrictions on using VPNs or other workarounds.
* HTTPS is generally the best solution for most users.
