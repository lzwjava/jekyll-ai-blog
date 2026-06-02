---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nginx Config on macOS Homebrew
translated: false
type: note
---

For Nginx installed via Homebrew on macOS (as indicated by the binary path `/opt/homebrew/bin/nginx`), the main configuration file is typically located at:

```
/opt/homebrew/etc/nginx/nginx.conf
```

This directory also contains other related files, such as server blocks in a `servers/` subdirectory (e.g., `/opt/homebrew/etc/nginx/servers/`).

To confirm the exact config file path used by your Nginx instance, run the following command in your terminal:

```
nginx -t
```

This will test the configuration and output the path to the `nginx.conf` file it's using. Alternatively, use `nginx -V` to see compile-time details, including the config path prefix.

If you're on an older Intel-based Mac where Homebrew installs to `/usr/local` instead, the path would be `/usr/local/etc/nginx/nginx.conf`, but your provided binary path confirms the `/opt/homebrew` location.

**References**
[Locate the nginx.conf file my nginx is actually using - Stack Overflow](https://stackoverflow.com/questions/19910042/locate-the-nginx-conf-file-my-nginx-is-actually-using)
[Installing nginx in macOS using homebrew | by Ram - Medium](https://medium.com/@rprprasath05/installing-nginx-in-macos-ventura-using-homebrew-12b87a900a03)
[Simple Configuration of NGINX on Mac - DEV Community](https://dev.to/arjavdave/simple-configuration-of-nginx-on-mac-3cg3)
