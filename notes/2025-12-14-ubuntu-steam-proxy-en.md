---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Setting Steam Proxy on Ubuntu
translated: false
type: note
---

Question: How to set a proxy for Steam on Ubuntu?

Answer:

Steam on Ubuntu does not have built-in proxy settings in its UI. It partially supports HTTP/HTTPS proxies via environment variables for client updates, logins, and downloads, but much of Steam's traffic (including content servers and multiplayer gaming) uses UDP, which standard HTTP proxies do not support. This means full functionality (especially online gaming) may not work behind a typical proxy.

### Basic Method: Use Environment Variables (for HTTP/HTTPS Proxy)

This works for initial updates, login, and some downloads if the proxy allows the necessary connections.

1. Open a terminal.
2. Set the proxy variables (replace with your proxy details; include username:password if authenticated):

   ```
   export http_proxy="http://username:password@proxy-server:port/"
   export https_proxy="http://username:password@proxy-server:port/"
   export HTTP_PROXY=$http_proxy
   export HTTPS_PROXY=$https_proxy
   ```

   (Lowercase and uppercase are both often needed.)

3. Launch Steam from the same terminal:

   ```
   steam
   ```

If launching from the menu/GUI, the variables may not be inherited—always launch from the terminal after setting them.

For convenience, add the exports to `~/.bashrc` or `~/.profile` for persistence, but launch Steam via terminal or create a custom launcher.

### Advanced Method: Use Proxychains (for SOCKS or More Complex Proxies)

If your proxy is SOCKS5 (better for UDP in some cases) or the above doesn't suffice:

1. Install proxychains:

   ```
   sudo apt update
   sudo apt install proxychains
   ```

2. Edit the config file:

   ```
   sudo nano /etc/proxychains.conf
   ```

   Comment out the default and add your proxy (e.g., for SOCKS5):

   ```
   socks5  proxy-server  port  username  password
   ```

   (Or http if supported.)

3. Launch Steam through proxychains:

   ```
   proxychains steam
   ```

This forces more traffic through the proxy but may be slower or unstable for gaming.

### Additional Tips

- Add the `-tcp` launch option to force TCP connections (may help compatibility):

  ```
  steam -tcp
  ```

- System-wide proxy settings in Ubuntu (Settings > Network > Proxy) do not affect Steam reliably.
- If behind an institutional proxy, login/update Steam on unrestricted network first, then switch (downloads may still need proxy).
- Note: Using proxies (especially for region changes) may violate Steam's terms of service.

References:

- [https://askubuntu.com/questions/227064/steam-linux-behind-a-proxy-server](https://askubuntu.com/questions/227064/steam-linux-behind-a-proxy-server)
- [https://blog.navinda.xyz/using-steam-with-proxy/](https://blog.navinda.xyz/using-steam-with-proxy/)
- [https://medium.com/@limeproxiesserver/how-to-use-steam-on-a-proxy-network-step-by-step-guide-6cfdd74c5b6](https://medium.com/@limeproxiesserver/how-to-use-steam-on-a-proxy-network-step-by-step-guide-6cfdd74c5b6)
- [https://superuser.com/questions/387856/getting-steam-exe-to-run-through-a-http-proxy](https://superuser.com/questions/387856/getting-steam-exe-to-run-through-a-http-proxy)
