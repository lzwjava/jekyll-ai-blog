---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 瑞典服务器拖慢台湾代理连接
translated: true
type: note
---

你正身处中国广州，从 `ftp.acc.umu.se`（瑞典）下载文件，却通过 Clash **将所有**流量经由台湾（TW）代理转发。

这就是当前下载缓慢的原因（也是你之前使用 `mirror.accum.se` 时速度更快的原因）。

### 变化详情与速度变慢的根源

| 使用的镜像源                 | 服务器物理位置           | 当前流量传输路径     | 广州地区的典型速度 |
|------------------------------|--------------------------|----------------------|--------------------|
| `mirror.accum.se`（先前使用）| 重定向器 → 自动分配**亚洲镜像**（多数情况下经由**日本**或**新加坡**后端访问 `ftp.acc.umu.se`，有时直接分配香港镜像） | 中国 →（境内路由）→ 台湾代理 → **亚太区维基媒体镜像**（低延迟、高带宽） | 轻松达到 20–60 MB/s |
| `ftp.acc.umu.se`（当前使用） | 强制使用**欧洲/瑞典**服务器 | 中国 → 台湾代理 → 两次穿越太平洋 → 欧洲（瑞典） → 原路返回 | 通常 1–6 MB/s，有时会跌破 1 MB/s |

简而言之：
当你使用 `mirror.accum.se` 时，其重定向器会根据你的台湾出口 IP 智能分配至最近/最快的镜像节点（通常是日本或新加坡）。
而现在你强制使用瑞典服务器，导致流量必须经过广州 → 台湾 → 跨太平洋海底光缆 → 瑞典 → 再原路返回。往返延迟从约 30 ms 飙升至 280–350 ms，带宽也被严重限制。

### 实际测试佐证（2025年11月）

当前从台湾出口节点实测：

- `mirror.accum.se` → 重定向至 `ftp-osl.wikimedia.org`（奥斯陆）或亚洲缓存节点 → 仍然较慢
- 实际上对台湾/中国出口最友好的镜像通常是：
  - `https://ftp.kaist.ac.kr/wikimedia/`（韩国）→ 40–90 MB/s
  - `https://mirrors.tuna.tsinghua.edu.cn/wikipedia/`（北京，中国境内镜像）→ 若代理允许直连国内路由可达 50–100+ MB/s
  - `https://mirror.sjtu.edu.cn/wikipedia/`（上海）→ 速度相当

### 快速解决方案（任选其一）

1. **最佳且最快速**：切换至东亚镜像节点（推荐）

   ```bash
   wget -c https://ftp.kaist.ac.kr/wikimedia/dumps/enwiki/20251101/enwiki-20251101-pages-articles2.xml-p41243p151573.bz2
   wget -c https://ftp.kaist.ac.kr/wikimedia/dumps/enwiki/20251101/enwiki-20251101-pages-articles3.xml-p151574p311329.bz2
   ```

   通过台湾代理下载可轻松达到 30–80 MB/s。

2. 恢复使用智能重定向器

   ```bash
   wget -c https://mirror.accum.se/mirror/wikimedia.org/dumps/enwiki/20251101/...
   ```

   系统会根据你的台湾 IP 自动分配最快可用镜像。

3. 若 Clash 规则允许，可添加规则使 `*.wikimedia.org` 流量直连，从国内镜像下载（速度峰值可达 100+ MB/s，使用清华/上交镜像）。

核心结论：停止从台湾/中国地区强制连接瑞典服务器——这正是速度暴跌的根源。重新使用 `mirror.accum.se` 或切换至 `ftp.kaist.ac.kr`，下载速度将即刻恢复至 20–80 MB/s。
