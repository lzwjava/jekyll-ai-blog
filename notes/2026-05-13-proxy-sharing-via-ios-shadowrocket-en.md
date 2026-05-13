---
audio: false
generated: true
image: false
lang: en
layout: post
title: Proxy Sharing via iOS Shadowrocket
translated: false
type: note
---

Question: Can using the proxy sharing feature in iOS Shadowrocket make it convenient for a computer or another phone to use the same connection?

Answer:

Yes, using Shadowrocket’s proxy sharing feature on iOS can allow other devices—like a computer or another phone—to use the same proxy connection, effectively routing their internet traffic through your iPhone’s proxy setup. Here’s how it works and what to consider:

1. **Functionality:**

   * Shadowrocket can create a local HTTP/SOCKS proxy on your iPhone.
   * Other devices on the same Wi-Fi network can connect to your iPhone’s proxy, allowing them to access the internet as if they were using your iPhone’s configured proxy.

2. **Setup Basics:**

   * Enable “Proxy Sharing” or “Local HTTP Proxy” in Shadowrocket settings.
   * Note the IP address of your iPhone on the Wi-Fi network and the port used by Shadowrocket.
   * On the other device, configure its network settings to use that IP and port as a proxy.

3. **Advantages:**

   * Convenient for devices that can’t directly run Shadowrocket.
   * Centralized control: You can manage which sites or traffic get routed through the proxy via your iPhone.

4. **Limitations & Considerations:**

   * Both devices usually need to be on the same local network, unless you set up additional port forwarding for remote access.
   * Performance depends on your iPhone’s network speed; heavy traffic may slow down your iPhone or connected devices.
   * Security: Be cautious if sharing with untrusted devices, as all traffic goes through your iPhone.

So yes, it can be convenient, but it’s best for smaller setups or temporary use rather than high-bandwidth or permanent sharing.

References:

* [Shadowrocket User Guide (iOS Proxy Sharing Overview)](https://shadowrocket.app/)
* [Proxy Setup for Multiple Devices via iPhone](https://medium.com/@proxyguide/using-iphone-as-proxy-server-2f0f1b2a1e1b)