---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过代理修复缓慢的Git拉取操作
translated: true
type: note
---

问题：在 DMIT.io 洛杉矶节点的代理上，Git pull 速度仅为 38.00 KiB/s，这个数据是否正确，是否算慢？

答案：

是的，从你的 `git pull` 输出中显示的速度（3.49 MiB 以 **38.00 KiB/s** 接收）对于现代 VPS 连接来说 **非常慢**，尤其是在 DMIT 洛杉矶节点上。在良好的连接条件下，GitHub 的正常下载速度应达到几 MB/s（兆字节每秒），而不是千字节每秒。38 KiB/s 大致相当于拨号上网时代的性能水平，表明存在瓶颈。

### 为什么在这种情况下会这么慢？
你的设置使用了本地 **HTTP/HTTPS 代理**（地址为 `http://127.0.0.1:7890`，常见于 Clash、V2Ray 或类似代理工具）。输出显示：

- Git 通过 SSH 公钥成功验证并连接 GitHub。
- 随后，它通过看起来是 **HTTPS 路径** 的方式接收数据对象，且该路径似乎经由代理路由。

在 DMIT 洛杉矶节点上使用代理导致速度缓慢的常见原因：

- **代理开销与路由**：代理（运行在你的本地机器或 VPS 上）可能存在带宽限制、高延迟或到 GitHub CDN 服务器（通常解析到洛杉矶地区的 IP）的路由不佳。即使 VPS 位于洛杉矶，代理也可能引入额外的跳转、丢包或限流。
- **Git 协议不匹配**：SSH 认证已成功，但数据传输很可能通过代理使用 HTTPS 进行，而 HTTPS 在大文件传输上通常比原生 SSH 慢。
- **已知的 GitHub 下载问题**：由于 CDN 路由、拥塞或临时问题，GitHub 的克隆/拉取操作可能会变慢。许多用户报告在特定区域或通过代理/VPN 使用时，速度会降至 50-100 KiB/s。
- **DMIT 特有因素**：虽然 DMIT 洛杉矶节点通常提供良好的性能（尤其是面向亚洲具有高带宽的 Premium/CN2 GIA 套餐），但如果代理本身是薄弱环节，使用代理可能会抵消这一优势。

### 快速检查与尝试的修复方法
1. **测试无代理连接**：
   - 暂时取消 shell 中的代理设置：
     ```
     unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy
     ```
   - 然后再次运行 `git pull` 并比较速度。

2. **强制 Git 完全使用 SSH**（通常更快）：
   - 如果尚未使用，将你的远程仓库地址改为 SSH：
     ```
     git remote set-url origin git@github.com:username/repo.git
     ```
   - 确保你的 SSH 密钥设置正确。

3. **增大 Git 缓冲区大小**（有助于改善慢速或不稳定连接）：
   ```
   git config --global http.postBuffer 524288000
   ```

4. **如果需要完整历史记录，可以使用浅克隆拉取**：
   ```
   git pull --depth=1
   ```

5. **检查代理性能**：
   - 测试通过代理的一般下载速度（例如，使用 `curl -x http://127.0.0.1:7890 -I https://github.com` 或进行速度测试）。
   - 尝试不同的代理端点或暂时禁用代理。
   - 如果代理用于绕过限制（例如来自中国），请测试直接连接或不同的代理位置。

6. **其他诊断方法**：
   - 从 VPS 上运行 `ping github.com` 和 `traceroute github.com`（或 `mtr github.com`）以检查延迟/丢包。
   - 查看 GitHub 当前状态页面，确认是否存在任何正在进行的问题。

总结：**不，这个速度不正常** — 它异常缓慢，值得进行故障排查。DMIT 洛杉矶节点本身应支持更高的吞吐量；代理或 Git 配置很可能是此问题的根源。尝试以上步骤，看看速度是否能提升到 MB/s 范围。

参考：  
- 关于 GitHub 下载缓慢的社区讨论（有多份报告称通过代理或路由不佳时速度低于 100 KiB/s）  
- Stack Overflow 上关于 GitHub 克隆缓慢和代理影响的帖子  
- 关于 Git HTTPS 与 SSH 速度差异的普遍报告