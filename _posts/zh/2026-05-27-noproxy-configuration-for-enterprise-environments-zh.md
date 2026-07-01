---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 企业环境中的NO_PROXY配置
translated: true
type: note
---

**问题：** 如何在企业环境（如SCB银行）中配置 `NO_PROXY`，特别是针对Nexus等内部服务？

---

**答案：**

## `NO_PROXY` 机制——基本原理

`NO_PROXY` 告知HTTP客户端哪些主机应绕过企业代理。若不设置，发往内部Nexus、Harbor、GitLab等的流量将通过企业代理转发，导致连接被拒绝或身份验证错误。

---

## 变量设置

```bash
# 两种形式都很重要——许多工具会检查其中之一
export HTTP_PROXY=http://proxy.scb.com:8080
export HTTPS_PROXY=http://proxy.scb.com:8080
export http_proxy=http://proxy.scb.com:8080
export https_proxy=http://proxy.scb.com:8080

# 绕过列表
export NO_PROXY="localhost,127.0.0.1,::1,.scb.com,nexus.internal.scb.com,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"
export no_proxy="$NO_PROXY"   # 小写别名——curl、wget、python会使用这个
```

---

## `NO_PROXY` 中应包含的内容

```
# 模式                          # 匹配内容
localhost                       127.0.0.1 回环地址
127.0.0.1                       显式IPv4回环地址
::1                             IPv6回环地址
.scb.com                        scb.com的所有子域名（前导点表示通配）
nexus.internal.scb.com          显式的Nexus主机名
harbor.scb.com                  容器仓库
gitlab.scb.com                  内部GitLab
10.0.0.0/8                      整个10.x.x.x地址段（CIDR——适用于Python/curl，不适用于Java）
172.16.0.0/12                   私有地址范围
192.168.0.0/16                  LAN地址范围
```

> **重要提示：** Java（`HttpURLConnection`、Maven、Gradle）**不**支持 `NO_PROXY` 中的CIDR表示法。请改用显式IP或域名后缀。

---

## 各工具特定配置

### curl / wget

```bash
# 自动读取 no_proxy（小写）
export no_proxy="localhost,127.0.0.1,.scb.com,10.10.0.0/8"
curl https://nexus.internal.scb.com/repository/maven-public/
```

### Python（requests、pip）

```bash
export NO_PROXY="localhost,.scb.com,10.0.0.0/8"
# requests 库同时读取 NO_PROXY 和 no_proxy
pip install --index-url https://nexus.internal.scb.com/repository/pypi/simple/ somepackage
```

或者在 `~/.pip/pip.conf` 中：

```ini
[global]
index-url = https://nexus.internal.scb.com/repository/pypi/simple/
trusted-host = nexus.internal.scb.com
```

### Maven（`~/.m2/settings.xml`）

```xml
<settings>
  <proxies>
    <proxy>
      <id>scb-proxy</id>
      <active>true</active>
      <protocol>http</protocol>
      <host>proxy.scb.com</host>
      <port>8080</port>
      <!-- 此处不能使用CIDR——Java不支持 -->
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

> Maven 在 `nonProxyHosts` 中使用 `|` 作为分隔符，而非 `,`。

### Gradle（`~/.gradle/gradle.properties`）

```properties
systemProp.http.proxyHost=proxy.scb.com
systemProp.http.proxyPort=8080
systemProp.https.proxyHost=proxy.scb.com
systemProp.https.proxyPort=8080
# 管道分隔，支持通配符
systemProp.http.nonProxyHosts=localhost|127.0.0.1|*.scb.com|nexus.internal.scb.com
systemProp.https.nonProxyHosts=localhost|127.0.0.1|*.scb.com|nexus.internal.scb.com
```

### npm

```bash
npm config set proxy http://proxy.scb.com:8080
npm config set https-proxy http://proxy.scb.com:8080
npm config set noproxy "localhost,127.0.0.1,.scb.com,nexus.internal.scb.com"
# 或者直接将仓库指向Nexus（完全绕过代理）
npm config set registry https://nexus.internal.scb.com/repository/npm-public/
```

### Docker 守护进程（`/etc/docker/daemon.json`）

```json
{
  "proxies": {
    "http-proxy": "http://proxy.scb.com:8080",
    "https-proxy": "http://proxy.scb.com:8080",
    "no-proxy": "localhost,127.0.0.1,.scb.com,harbor.scb.com"
  }
}
```

对于 Docker 构建（作为构建参数传递）：

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
# 绕过内部GitLab
git config --global http.noProxy "gitlab.internal.scb.com,.scb.com"
```

---

## Shell 配置文件——将此内容放入 `~/.bashrc` 或 `~/.zshrc`

```bash
# === SCB 代理配置 ===
SCB_PROXY="http://proxy.scb.com:8080"
SCB_NO_PROXY="localhost,127.0.0.1,::1,.scb.com,nexus.internal.scb.com,harbor.scb.com,gitlab.internal.scb.com,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"

export HTTP_PROXY="$SCB_PROXY"
export HTTPS_PROXY="$SCB_PROXY"
export http_proxy="$SCB_PROXY"
export https_proxy="$SCB_PROXY"
export NO_PROXY="$SCB_NO_PROXY"
export no_proxy="$SCB_NO_PROXY"

# 快速切换
proxy_off() {
  unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy NO_PROXY no_proxy
  echo "已禁用代理"
}
proxy_on() {
  export HTTP_PROXY="$SCB_PROXY" HTTPS_PROXY="$SCB_PROXY"
  export http_proxy="$SCB_PROXY" https_proxy="$SCB_PROXY"
  export NO_PROXY="$SCB_NO_PROXY" no_proxy="$SCB_NO_PROXY"
  echo "已启用代理"
}
```

---

## 代理问题调试

```bash
# 检查已设置的环境变量
env | grep -i proxy

# 使用显式绕过进行测试
curl -v --noproxy "nexus.internal.scb.com" https://nexus.internal.scb.com/

# 追踪连接去向
curl -v https://nexus.internal.scb.com/ 2>&1 | grep -E "proxy|connect|Could"

# Python——查看 requests 解析结果
python3 -c "
import requests
s = requests.Session()
print('proxies:', s.merge_environment_settings('https://nexus.internal.scb.com', {}, True, None, None))
"

# 检查是否为证书问题（企业 MITM 代理常见）
curl -k https://nexus.internal.scb.com/   # -k 跳过TLS验证
# 如果这样能工作，则需要添加企业CA证书
```

### 企业 MITM 证书（银行中非常常见）

```bash
# 将企业CA添加到系统信任（Ubuntu）
sudo cp scb-root-ca.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates

# Python——指向证书包
export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

# pip
pip config set global.cert /etc/ssl/certs/ca-certificates.crt
```

---

## 银行环境中常见陷阱

| 陷阱 | 解决方案 |
| ------ | ---------- |
| Java 不支持 `nonProxyHosts` 中的CIDR | 改用 `*.scb.com` 通配符 |
| Maven 使用 `\|` 而非 `,` 作为分隔符 | `localhost\|*.scb.com` |
| 企业代理进行TLS检测（MITM） | 在系统中安装企业CA证书 |
| Docker 守护进程与客户端代理配置不同 | 两者需分别配置 |
| `NO_PROXY` 与 `no_proxy`——有些工具只读取其中之一 | 始终同时导出两者 |
| Nexus 需要认证——代理可能会剥离认证头 | 使用 `.netrc` 或 `~/.m2/settings.xml` 中的凭据 |
