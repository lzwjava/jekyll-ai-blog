---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 中国下载速度缓慢问题
translated: true
type: note
---

问题：为什么在中国使用“npx camoufox-js fetch”下载Camoufox极其缓慢，长达1523秒后仍显示0%？

回答：

下载速度极慢的原因是**Camoufox**（一款基于Firefox定制、用于自动化及反检测的浏览器）需要从**境外服务器**（可能托管在AWS、GitHub、Fastly CDN或类似的海外基础设施）拉取一个大型二进制文件（约300-400 MB）。

### 在中国下载缓慢的主要原因：
- **中国防火墙（GFW）**：所有进出中国大陆的流量必须经过少数国际网关。防火墙实施**深度包检测（DPI）**，会故意对连接境外服务器的流量施加**数据包丢失**、限流和额外延迟，导致大文件下载速度降至正常速度的极小部分。
- **跨境带宽拥堵**：中国出境的国际链路负载重且常出现拥堵，尤其从热门西方CDN下载时更为明显。
- **缺乏中国优化CDN**：与大型企业（例如部分公司使用阿里云或腾讯云CDN部署国内镜像）不同，Camoufox的下载源未在中国大陆设立高速镜像。进度条在25分钟以上（1523秒≈25分钟）保持0%是此类被阻断/限流下载的典型现象。

这也是为什么在中国从GitHub/AWS下载Playwright、Puppeteer、Chrome/Firefox二进制文件或任何大文件时，速度 notoriously 缓慢或不稳定的原因。

### 解决方案（建议按此顺序尝试）：

1. **使用优质VPN**（最有效）
   - 连接至**高质量VPN**，优先选择针对中国优化的服务器（例如采用混淆协议或设有中国专线节点的服务）。
   - 常用于大文件下载且效果较好的选项：Astrill、ExpressVPN或已知能绕过GFW限流的付费服务。
   - **在VPN连接状态下**运行fetch命令。
   - 注意：免费VPN通常会使情况更糟。

2. **强制重新尝试（清理缓存）**
   ```bash
   npx camoufox-js remove   # 或使用Python版本时运行 camoufox remove
   npx camoufox-js fetch
   ```
   部分下载可能损坏，导致速度进一步下降。

3. **优化本地网络**
   - 切换不同运营商（例如尝试中国移动、中国电信、中国联通——某些运营商的国际路由略优）。
   - 使用有线网络替代Wi-Fi。
   - 关闭其他高带宽占用应用。

4. **手动下载（高级备用方案）**
   - 尽可能开启详细日志模式运行命令，以查看确切下载URL。
   - 获取URL后，使用下载管理器、开启VPN的浏览器或支持断点续传的工具（如`aria2c`/`wget`）手动下载文件。
   - 将文件放置于Camoufox的缓存目录中（具体路径请查阅工具文档）。

5. **等待并择时重试**
   - 国际线路在非高峰时段（例如中国当地深夜或凌晨）可能有所改善。

目前Camoufox尚未提供官方中国镜像，因此使用VPN是中国大陆用户最可靠的解决方案。

若开启VPN后下载仍失败或持续显示0%，请分享完整输出信息（包括最终失败时的错误提示），以便进一步协助。

参考链接：
- https://www.mlytics.com/blog/why-your-website-is-slow-in-china-and-how-to-fix-it-2024-total-guide-for-better-web-app-performance-in-china/
- https://www.thoughtworks.com/insights/blog/user-experience/foreign-websites-slower-China
- https://github.com/platformio/platformio-core/issues/4656
- Camoufox文档提及约300-400MB下载量及低速连接说明
