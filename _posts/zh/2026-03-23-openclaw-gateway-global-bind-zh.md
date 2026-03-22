---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为 OpenClaw 网关启用全局绑定
translated: true
type: note
---

问题：如何将 OpenClaw gateway 配置从 "loopback" (127.0.0.1) 修改为全局绑定 (0.0.0.0)，以便通过 192.168.1.36:18789 进行访问？

回答：

## 修改配置文件

只需在 config 中修改 **两个字段**：

```json
"gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "loopback",
    "auth": {
        "mode": "token",
        "token": "86c230696f27eada444097a03167fca718b3321b3d52c117"
    }
}
```

**修改为：**

```json
"gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "all",
    "auth": {
        "mode": "token",
        "token": "86c230696f27eada444097a03167fca718b3321b3d52c117"
    }
}
```

---

## 变更说明

| 字段 | 修改前 | 修改后 | 含义 |
|---|---|---|---|
| `bind` | `"loopback"` | `"all"` | 监听 `0.0.0.0` 而非 `127.0.0.1` |

> 典型值为 `loopback` → 仅绑定到 `127.0.0.1`，以及 `all` → 绑定到 `0.0.0.0`（所有接口）。
> 部分配置可能使用 `global` 而非 `all` —— 如果 `all` 不起作用，请检查 OpenClaw 的官方文档。

---

## 修改后的操作

1. **保存** 配置文件
2. **重启** OpenClaw 服务：
```bash
systemctl restart openclaw
# 或
pkill openclaw && openclaw &
```

3. **验证** 是否已在所有接口上监听：
```bash
ss -tlnp | grep 18789
# 应当显示: 0.0.0.0:18789 (而不是 127.0.0.1:18789)
```

4. 如有需要，**允许防火墙** 通行：
```bash
sudo ufw allow 18789
```

5. 通过浏览器访问：
```
http://192.168.1.36:18789
```

---

## 安全提示

⚠️ 由于你的配置已经启用了 **token auth** (`"mode": "token"`)，你的访问是受保护的 —— 任何请求都必须包含 token。这对于局域网（LAN）使用是安全的，但在没有额外防火墙规则的情况下，**请勿将 18789 端口暴露在公网（public internet）上**。