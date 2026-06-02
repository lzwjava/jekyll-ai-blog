---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 排查 Openclaw systemd 服务失败
translated: true
type: note
---

**问题：** 如何找出 `openclaw-gateway.service` systemd 用户服务失败的原因？

**回答：**

服务显示 `status=1/FAILURE`，但日志被截断了。以下是深入排查的方法：

## 1. 检查完整的 Journal 日志（最有用）

```bash
journalctl --user -u openclaw-gateway.service -n 100 --no-pager
```

或实时跟踪重启过程：
```bash
journalctl --user -u openclaw-gateway.service -f
```

## 2. 检查自上次启动以来的日志

```bash
journalctl --user -u openclaw-gateway.service -b
```

## 3. 使用详细输出查看完整错误

```bash
journalctl --user -u openclaw-gateway.service -n 50 --no-pager -o verbose
```

## 4. 直接运行二进制文件查看原始错误

由于它是 Node.js 进程，手动运行以捕获 stderr：

```bash
/usr/bin/node /home/lzw/.npm-global/lib/node_modules/openclaw/dist/index.js gateway --host 0.0.0.0 2>&1
```

这将把确切错误打印到您的终端，而不会被 systemd 吞没。

## 5. 检查 Node 或模块是否存在问题

```bash
# 检查 node 是否正常工作
node --version

# 检查模块是否存在
ls /home/lzw/.npm-global/lib/node_modules/openclaw/dist/index.js

# 检查缺失的依赖
cd /home/lzw/.npm-global/lib/node_modules/openclaw && npm ls 2>&1 | grep "missing\|UNMET"
```

## 快速诊断总结

| Symptom | Likely Cause |
|---|---|
| `MODULE_NOT_FOUND` | Missing npm dependency |
| `EADDRINUSE` | Port already in use |
| `EACCES` | Permission denied on port/file |
| `SyntaxError` | Node.js version incompatible |
| `ENOENT` | Config file or path not found |

**从 `journalctl --user -u openclaw-gateway.service -n 100 --no-pager` 开始** — 这几乎总是会显示 Node.js 的确切错误消息。
