---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复Git SSH拉取速度慢的问题
translated: true
type: note
---

以下是调查和修复的完整说明。

---

## 问题

通过 SSH (`git@github.com:QwenLM/Qwen2.5-Coder.git`) 拉取 `Qwen2.5-Coder` 仓库时，下载速度仅为 81 KiB/s，需要拉取 2976 个对象（约 30 MB）。

---

## 调查步骤

### 步骤 1：检查 git 远程和代理配置

```bash
git -C /Users/lzwjava/projects/Qwen2.5-Coder remote -v
# → git@github.com:QwenLM/Qwen2.5-Coder.git (SSH)

git config --global --list | grep -iE 'proxy|http'
# → http.proxy=127.0.0.1:7890
# → https.proxy=127.0.0.1:7890
```

git 配置了 HTTP 代理（7890），但远程仓库使用的是 SSH —— 因此 git 的 `http.proxy` 不适用。SSH 有自己独立的代理路径。

### 步骤 2：检查 SSH 配置

```bash
cat ~/.ssh/config
```

找到关键行：

```
Host !192.168.*.*
    ProxyCommand ncat --proxy localhost:7891 --proxy-type socks5 %h %p
```

这意味着**所有非本地 SSH 连接**（包括 GitHub）都通过 `ncat` → SOCKS5 代理（`localhost:7891`）进行。这是 SSH 的数据路径，与 git 的 HTTP 代理无关。

### 步骤 3：检查代理端口上运行的程序

```bash
lsof -i :7890 -sTCP:LISTEN
lsof -i :7891 -sTCP:LISTEN
```

两个端口均由 `mihomo-da`（PID 86998）提供服务 —— 即 mihomo（Clash Meta），你的本地代理。端口 7890 = HTTP 代理，端口 7891 = SOCKS5 代理。两者均正常运行。

### 步骤 4：直接测试代理速度

```bash
curl -x socks5h://localhost:7891 -o /dev/null -w "speed: %{speed_download}\n" https://github.com
# → ~1 MB/s — 代理速度快

curl -x http://127.0.0.1:7890 -o /dev/null -w "speed: %{speed_download}\n" https://github.com
# → ~980 KB/s — 同样很快
```

**结论：** 代理本身并非瓶颈。对于 HTTPS 流量，HTTP 和 SOCKS5 两条路径都很快。

### 步骤 5：测试 SSH 认证速度

```bash
time ssh -T git@github.com
# → 3.6 秒，认证成功
```

SSH 握手正常。慢的是认证后的**数据传输阶段**，而非连接建立阶段。

### 步骤 6：定位瓶颈

链路是：`git fetch` → SSH → `ncat` → SOCKS5 代理（7891）→ mihomo → 互联网。

`ncat`（来自 nmap 7.98）是薄弱环节。它被设计为网络工具，而非高吞吐量的 SSH 隧道代理。对于小数据包（认证、握手）表现尚可，但对于持续的大数据传输（git packfile），它会引入显著的开销 —— 这就是 81 KiB/s 与 1 MB/s 差异的原因。

对比：HTTPS 走的是：`git` → libcurl → HTTP 代理（7890）→ mihomo → 互联网。链路中没有 `ncat`。libcurl 针对批量传输进行了优化。

### 步骤 7：测试 HTTPS 拉取

```bash
GIT_TRACE=1 git -C /Users/lzwjava/projects/Qwen2.5-Coder fetch --depth=1
# → 413 个对象，约 77 秒，成功完成
```

从追踪信息看时间戳：
```
14:01:45.303  index-pack started (receiving data)
14:03:02.436  index-pack done
```

约 77 秒传输 413 个对象。原始 SSH 拉取需要获取 2976 个对象 —— 以 81 KiB/s 的速度，需要 10 分钟以上。

---

## 已执行的操作

将所有 5 个 Qwen 仓库从 SSH 切换为 HTTPS：

```
Qwen2-Audio:    git@github.com → https://github.com/QwenLM/Qwen2-Audio.git
Qwen2.5-Coder:  git@github.com → https://github.com/QwenLM/Qwen2.5-Coder.git
Qwen2.5-Math:   git@github.com → https://github.com/QwenLM/Qwen2.5-Math.git
Qwen2.5-VL:     git@github.com → https://github.com/QwenLM/Qwen2.5-VL.git
Qwen3:          已经是 HTTPS（无需更改）
```

使用的命令：
```bash
git -C /path/to/repo remote set-url origin https://github.com/QwenLM/RepoName.git
```

认证会自动工作，因为已配置 `git-credential-manager`。

---

## 关键要点

1. **git 中的 SSH 代理 ≠ HTTP 代理。** `http.proxy` 仅影响 HTTPS 远程仓库。SSH 远程仓库使用 `~/.ssh/config` 中的 ProxyCommand。
2. **`ncat` 在批量 SSH 隧道传输中速度慢。** 适合小数据交换，但对大型 packfile 传输表现很差。如果未来需要通过代理使用 SSH，`connect`（通过 `brew install connect` 安装）或 `nc -X 5 -x localhost:7891` 是更快的替代方案。
3. **对于大型仓库（模型权重、数据集），当拥有快速 HTTP 代理时，优先选择 HTTPS。** libcurl 路径针对批量数据进行了优化；通过 SOCKS5 的 SSH 会增加开销。
4. **需要记住的排查命令：**
   - `lsof -i :PORT -sTCP:LISTEN` —— 查看哪个进程在监听端口
   - `curl -x socks5h://localhost:PORT -o /dev/null -w "%{speed_download}" URL` —— 测试代理速度
   - `GIT_TRACE=1 git fetch` —— 查看 git 具体在哪个环节耗时
   - `git config --global --list | grep proxy` —— 检查代理配置