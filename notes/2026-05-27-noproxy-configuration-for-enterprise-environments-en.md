---
audio: false
generated: true
image: false
lang: en
layout: post
title: NO_PROXY Configuration for Enterprise Environments
translated: false
type: note
---

**Question:** How to configure `NO_PROXY` in enterprise environments (e.g., SCB bank), specifically for internal services like Nexus?

---

**Answer:**

## `NO_PROXY` Mechanics — First Principles

`NO_PROXY` tells HTTP clients which hosts to bypass the corporate proxy for. Without it, traffic to internal Nexus, Harbor, GitLab, etc. gets routed through the corporate proxy and fails with connection refused or auth errors.

---

## The Variable

```bash
# Both forms matter — many tools check one or the other
export HTTP_PROXY=http://proxy.scb.com:8080
export HTTPS_PROXY=http://proxy.scb.com:8080
export http_proxy=http://proxy.scb.com:8080
export https_proxy=http://proxy.scb.com:8080

# Bypass list
export NO_PROXY="localhost,127.0.0.1,::1,.scb.com,nexus.internal.scb.com,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"
export no_proxy="$NO_PROXY"   # lowercase alias — curl, wget, python use this
```

---

## What to Put in `NO_PROXY`

```
# Pattern                      # What it matches
localhost                       127.0.0.1 loopback
127.0.0.1                       IPv4 loopback explicit
::1                             IPv6 loopback
.scb.com                        ALL subdomains of scb.com (leading dot = wildcard)
nexus.internal.scb.com          explicit Nexus hostname
harbor.scb.com                  container registry
gitlab.scb.com                  internal GitLab
10.0.0.0/8                      entire 10.x.x.x block (CIDR — works in Python/curl, NOT in Java)
172.16.0.0/12                   private range
192.168.0.0/16                  LAN range
```

> **Important:** Java (`HttpURLConnection`, Maven, Gradle) does **NOT** understand CIDR notation in `NO_PROXY`. Use explicit IPs or domain suffixes instead.

---

## Tool-Specific Config

### curl / wget

```bash
# Reads no_proxy (lowercase) automatically
export no_proxy="localhost,127.0.0.1,.scb.com,10.10.0.0/8"
curl https://nexus.internal.scb.com/repository/maven-public/
```

### Python (requests, pip)

```bash
export NO_PROXY="localhost,.scb.com,10.0.0.0/8"
# requests library reads both NO_PROXY and no_proxy
pip install --index-url https://nexus.internal.scb.com/repository/pypi/simple/ somepackage
```

Or in `~/.pip/pip.conf`:

```ini
[global]
index-url = https://nexus.internal.scb.com/repository/pypi/simple/
trusted-host = nexus.internal.scb.com
```

### Maven (`~/.m2/settings.xml`)

```xml
<settings>
  <proxies>
    <proxy>
      <id>scb-proxy</id>
      <active>true</active>
      <protocol>http</protocol>
      <host>proxy.scb.com</host>
      <port>8080</port>
      <!-- No CIDR here — Java doesn't support it -->
      <nonProxyHosts>localhost|127.0.0.1|*.scb.com|nexus.internal.scb.com</nonProxyHosts>
    </proxy>
  </proxies>
  <mirrors>
    <mirror>
      <id>nexus</id>
      <url>https://nexus.internal.scb.com/repository/maven-public/</url>
      <mirrorOf>central</mirrorOf>
    </mirror>
  </mirrors>
</settings>
```

> Maven uses `|` as separator in `nonProxyHosts`, not `,`.

### Gradle (`~/.gradle/gradle.properties`)

```properties
systemProp.http.proxyHost=proxy.scb.com
systemProp.http.proxyPort=8080
systemProp.https.proxyHost=proxy.scb.com
systemProp.https.proxyPort=8080
# Pipe-separated, supports wildcards
systemProp.http.nonProxyHosts=localhost|127.0.0.1|*.scb.com|nexus.internal.scb.com
systemProp.https.nonProxyHosts=localhost|127.0.0.1|*.scb.com|nexus.internal.scb.com
```

### npm

```bash
npm config set proxy http://proxy.scb.com:8080
npm config set https-proxy http://proxy.scb.com:8080
npm config set noproxy "localhost,127.0.0.1,.scb.com,nexus.internal.scb.com"
# Or point registry directly to Nexus (bypasses proxy entirely)
npm config set registry https://nexus.internal.scb.com/repository/npm-public/
```

### Docker daemon (`/etc/docker/daemon.json`)

```json
{
  "proxies": {
    "http-proxy": "http://proxy.scb.com:8080",
    "https-proxy": "http://proxy.scb.com:8080",
    "no-proxy": "localhost,127.0.0.1,.scb.com,harbor.scb.com"
  }
}
```

For Docker build (pass as build args):

```bash
docker build \
  --build-arg HTTP_PROXY=http://proxy.scb.com:8080 \
  --build-arg NO_PROXY=localhost,.scb.com \
  .
```

### Git

```bash
git config --global http.proxy http://proxy.scb.com:8080
git config --global https.proxy http://proxy.scb.com:8080
# Bypass for internal GitLab
git config --global http.noProxy "gitlab.internal.scb.com,.scb.com"
```

---

## Shell Profile — Put This in `~/.bashrc` or `~/.zshrc`

```bash
# === SCB Proxy Config ===
SCB_PROXY="http://proxy.scb.com:8080"
SCB_NO_PROXY="localhost,127.0.0.1,::1,.scb.com,nexus.internal.scb.com,harbor.scb.com,gitlab.internal.scb.com,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"

export HTTP_PROXY="$SCB_PROXY"
export HTTPS_PROXY="$SCB_PROXY"
export http_proxy="$SCB_PROXY"
export https_proxy="$SCB_PROXY"
export NO_PROXY="$SCB_NO_PROXY"
export no_proxy="$SCB_NO_PROXY"

# Quick toggles
proxy_off() {
  unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy NO_PROXY no_proxy
  echo "Proxy disabled"
}
proxy_on() {
  export HTTP_PROXY="$SCB_PROXY" HTTPS_PROXY="$SCB_PROXY"
  export http_proxy="$SCB_PROXY" https_proxy="$SCB_PROXY"
  export NO_PROXY="$SCB_NO_PROXY" no_proxy="$SCB_NO_PROXY"
  echo "Proxy enabled"
}
```

---

## Debugging Proxy Issues

```bash
# Check what env vars are set
env | grep -i proxy

# Test with explicit bypass
curl -v --noproxy "nexus.internal.scb.com" https://nexus.internal.scb.com/

# Trace where connection goes
curl -v https://nexus.internal.scb.com/ 2>&1 | grep -E "proxy|connect|Could"

# Python — see what requests resolves
python3 -c "
import requests
s = requests.Session()
print('proxies:', s.merge_environment_settings('https://nexus.internal.scb.com', {}, True, None, None))
"

# Check if it's a cert issue (common with MITM corp proxies)
curl -k https://nexus.internal.scb.com/   # -k skips TLS verify
# If that works, you need to add the corporate CA cert
```

### Corporate MITM Certificate (very common at banks)

```bash
# Add the corp CA to system trust (Ubuntu)
sudo cp scb-root-ca.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates

# Python — point to cert bundle
export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

# pip
pip config set global.cert /etc/ssl/certs/ca-certificates.crt
```

---

## Key Gotchas at Banks

| Gotcha | Fix |
|--------|-----|
| Java doesn't support CIDR in `nonProxyHosts` | Use `*.scb.com` wildcard instead |
| Maven uses `\|` not `,` as separator | `localhost\|*.scb.com` |
| Corporate proxy does TLS inspection (MITM) | Install corp CA cert system-wide |
| Docker daemon vs Docker client proxy config | Both need separate config |
| `NO_PROXY` vs `no_proxy` — some tools only read one | Export both always |
| Nexus needs auth — proxy strips headers | Use `.netrc` or `~/.m2/settings.xml` credentials |
