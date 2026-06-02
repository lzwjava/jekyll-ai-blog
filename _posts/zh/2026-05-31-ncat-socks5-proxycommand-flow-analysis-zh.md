---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ncat SOCKS5代理命令流程分析
translated: true
type: note
---

现在我看清了 nmap 源码树的整体情况。下面是在你的 SSH ProxyCommand 配置中 ncat 的工作原理：

```
ncat --proxy localhost:7891 --proxy-type socks5 %h %p
```

完整流程（来自源码）：

1. **选项解析** (ncat_main.c:441-448)
   `--proxy`       → `o.proxyaddr = "localhost:7891"`
   `--proxy-type`  → `o.proxytype = "socks5"`
   `%h %p`         → `o.target = hostname`，`o.portno = port`（SSH 默认 22）

2. **代理地址解析** (ncat_main.c:753)
   `parseproxy("localhost:7891", ...)` 解析代理本身
   `targetaddrs` 现在指向 `localhost:7891`（SOCKS 代理，**不是**最终的 SSH 目标）
   真正的目标（`o.target`）被保留，用于 SOCKS5 CONNECT 请求

3. **调度** (ncat_connect.c:1064)

   ```c
   if (strcmp(o.proxytype, "socks5") == 0)
       connect_socket = do_proxy_socks5();
   ```

4. **TCP 连接到代理** (ncat_connect.c:639, util.c:489-517)

   ```c
   sd = do_connect(SOCK_STREAM)
   ```

   创建原始 TCP 套接字，连接到 `targetaddrs`（= `localhost:7891`）
   这是 ncat 建立的**唯一**直接网络连接

5. **SOCKS5 握手 — 阶段 1：认证协商** (ncat_connect.c:650-671)
   发送：`[0x05, 0x01, 0x00]` = SOCKS5，1 种方法，无认证
   接收：`[0x05, 0x00]`       = SOCKS5，无认证被接受
   （如果指定了 `--proxy-auth`，还会提供 0x02 用户密码方法）

6. **SOCKS5 握手 — 阶段 2：CONNECT 请求** (ncat_connect.c:773-828)
   发送 `socks5_request` 结构体：
   - `ver`  = `0x05`（SOCKS5）
   - `cmd`  = `0x01`（CONNECT）
   - `rsv`  = `0x00`
   - `atyp` = `0x03`（域名）或 `0x01`（IPv4）或 `0x04`（IPv6）
   - `dst`  = 主机名字节 + 端口（2 字节，网络字节序）

   以 `github.com:22` 为例：

   ```
   [0x05, 0x01, 0x00, 0x03, 0x0A]
   + "github.com"
   + [0x00, 0x16]  # 端口 22
   ```

7. **SOCKS5 响应** (ncat_connect.c:830-920)
   接收 4 字节头部，检查回复码 `0x00` = 成功
   读取绑定地址（长度取决于 `atyp`）
   返回套接字文件描述符

8. **数据中继** (ncat_connect.c:1074-1097)
   代理协商成功后：

   ```c
   cs.sock_nsi = nsock_iod_new2(mypool, connect_socket, NULL);
   ```

   Nsock（nmap 的异步 I/O 库）接管原始套接字
   `nsock_loop(mypool, -1)` 运行事件循环
   数据流：`SSH <-> ncat stdin/stdout <-> SOCKS 代理 <-> 互联网`

**为什么大块传输时速度慢：**

瓶颈在第 8 步。Nsock 的事件循环通过用户空间缓冲区复制数据，缓冲区大小为 `DEFAULT_BUF_LEN`（TCP 为 8KB）。每个数据块：

```
read(socket) -> buffer -> write(stdout)   # 代理 -> SSH
read(stdin)  -> buffer -> write(socket)   # SSH -> 代理
```

每个方向每个满缓冲区需要两次额外的 `copy()` 系统调用。对于一个假设为 50MB 的 git packfile：

```
50MB / 8KB = ~6,400 次事件循环往返
每次 2 次系统调用 = ~12,800 次额外系统调用
```

此外，nsock 在每次迭代中还有自己的 `select()`/`poll()` 开销。

**替代方案及其更快的原因：**

- **`connect`**（通过 `brew install connect` 安装）：
  尽可能使用 `splice()`/`sendfile()`
  直接 fd 到 fd 中继，没有事件循环抽象层
  `ProxyCommand: connect -H localhost:7891 %h %p`

- **`nc -X 5 -x localhost:7891`**：
  使用原始 `read()`/`write()` 和更大的缓冲区
  没有 nsock 事件循环开销
  `ProxyCommand: nc -X 5 -x localhost:7891 %h %p`

两者都跳过了 nsock 的间接层，采用更简单的 I/O 循环，并可能使用更大的缓冲区（64KB+ 而非 8KB）。

对于你的模型仓库——在通过代理传输大 packfile 时，优先使用 HTTPS 远程仓库而非 SSH，你的判断是正确的。SOCKS5 握手本身（步骤 4-7）很快（约 2ms），问题出在持续吞吐量上。
