---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Ubuntu代理绕过主机配置
translated: true
type: note
---

### 在 Ubuntu 手动代理设置中配置多个主机

在 Ubuntu 的手动代理配置中（通过**设置 > 网络 > 网络代理 > 手动**进入），"忽略主机"字段允许您指定以分号分隔的主机、域名或 IP 范围列表，使其绕过代理。这通常用于本地流量，如本地主机或内部网络。虽然不能将这些地址设置为*代理服务器*地址（该字段需要单个主机:端口），但它们非常适合填入"忽略主机"字段。

#### 通过图形界面配置步骤：
1. 打开**设置**（在活动概览中搜索）。
2. 进入**网络 > 网络代理**。
3. 将方法设置为**手动**。
4. 在**忽略主机**字段中，输入以分号分隔的列表（分号前后不要加空格）：
   ```
   localhost;127.0.0.1;192.168.1.1;192.168.2.1;::1
   ```
   - `localhost`：解析为回环地址
   - `127.0.0.1`：IPv4 回环地址
   - `192.168.1.1` 和 `192.168.2.1`：特定本地 IP（可根据需要添加多个）
   - `::1`：IPv6 回环地址

5. 点击**应用**保存。此设置将系统级生效（影响浏览器、apt 等应用程序）。

#### 关于使用通配符（如 `192.168.1.*`）：
- "忽略主机"字段**不支持**直接使用通配符（如 `192.168.1.*`）——该字段设计用于精确主机、域名后缀（如 `*.local`）或 IP 范围的 CIDR 表示法。
- 建议使用**CIDR 表示法**定义范围：
  - 对于 `192.168.1.*`（192.168.1.0/24 子网中的所有 IP），请使用 `192.168.1.0/24`
  - 更新后的示例列表：
    ```
    localhost;127.0.0.1;::1;192.168.1.0/24;192.168.2.1
    ```
  - 对于更广泛的本地网络，可添加 `10.0.0.0/8;172.16.0.0/12;192.168.0.0/16`（常见私有地址范围）

#### 命令行替代方案（适用于脚本编写或精确配置）：
如果更喜欢使用终端（或需要自动化），可通过 `gsettings`（现代 Ubuntu）或编辑 `/etc/environment` 进行系统级配置：
- 查看当前忽略列表：
  ```
  gsettings get org.gnome.system.proxy ignore-hosts
  ```
- 设置列表（替换为您的值）：
  ```
  gsettings set org.gnome.system.proxy ignore-hosts "['localhost', '127.0.0.1', '::1', '192.168.1.0/24', '192.168.2.1']"
  ```
- 配置永久环境变量（影响部分应用程序）：在 `/etc/environment` 中添加：
  ```
  no_proxy="localhost,127.0.0.1,::1,192.168.1.0/24,192.168.2.1"
  ```
  然后重启系统或运行 `source /etc/environment`

可通过 ping 列表中的主机或检查浏览器代理行为来测试。如果出现问题（例如特定应用程序异常），环境变量方法通常能覆盖更多场景。

[设置代理忽略所有本地地址](https://askubuntu.com/questions/11274/setting-up-proxy-to-ignore-all-local-addresses)
[如何在 Ubuntu 上配置代理设置](https://phoenixnap.com/kb/ubuntu-proxy-settings)
[在 no_proxy 环境变量中设置网络范围](https://unix.stackexchange.com/questions/23452/set-a-network-range-in-the-no-proxy-environment-variable)
