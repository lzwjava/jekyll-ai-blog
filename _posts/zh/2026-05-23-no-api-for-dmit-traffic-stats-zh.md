---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DMIT流量统计无API
translated: true
type: note
---

**问题：** DMIT.io 是否提供 API，用于以编程方式查询服务器流量/带宽使用情况（针对 CN2 VPN 服务器）？

**答案：**

简短回答：**没有公开/官方 API。** DMIT 并未向用户暴露用于查询流量统计的文档化客户 API。以下是完整说明及可行的变通方案：

---

## DMIT 底层实际使用的技术

DMIT 运行基于 **WHMCS** 并结合 **SolusVM** 进行 VPS 控制的自定义管理面板。这两者均具备 API，但 DMIT 并未将其公开给客户。

- **WHMCS** 在 `/includes/api.php` 处有 API，但这是仅限管理员使用的 API —— 客户无法获取凭据。
- **SolusVM** 提供了客户端 API，但同样受限 —— 你需要 DMIT 为你的账户启用该功能。

---

## 你的实际选项

### 选项 1：爬取 DMIT 客户区域（最快的 hack 方法）

登录 `https://www.dmit.io/clientarea.php`，查看你的 VPS 服务页面 —— 它会显示已使用/剩余带宽。你可以使用 `requests` + `BeautifulSoup` 自动化爬取：

```python
import requests
from bs4 import BeautifulSoup

SESSION_COOKIE = "YOUR_WHMCS_SESSION_COOKIE"

s = requests.Session()
s.cookies.set("WHMCSUser", SESSION_COOKIE, domain="www.dmit.io")

r = s.get("https://www.dmit.io/clientarea.php?action=productdetails&id=YOUR_SERVICE_ID")
soup = BeautifulSoup(r.text, "html.parser")

# 检查 HTML 以找到带宽元素 —— 通常类似于：
bw = soup.find("div", {"class": "traffic-usage"})  # 调整选择器
print(bw.text if bw else "Selector needs adjustment")
```

要获取你的会话 cookie：打开 DevTools → Network → 对 dmit.io 的任意请求 → 复制 `Cookie` 头部。在客户区域点击你的服务时，从 URL 中获取 `id=`。

---

### 选项 2：直接在 VPS 上监控流量（最可靠）

既然你控制着 VPS，只需从服务器端进行测量即可。无需 API。

```bash
# 安装 vnstat 以实现持久化的月度追踪
apt install vnstat
vnstat -i eth0 --json   # 输出包含日/月统计的 JSON
```

或者一行命令获取本月用量：

```bash
vnstat -m --json | python3 -c "
import json,sys
d=json.load(sys.stdin)
m=d['interfaces'][0]['traffic']['month']
print(f\"RX: {m[-1]['rx']/1e9:.2f} GB, TX: {m[-1]['tx']/1e9:.2f} GB\")
"
```

设置 cron 任务并推送到 webhook/Telegram 机器人，以便在接近配额时收到警报。

---

### 选项 3：SolusVM 客户端 API（如果 DMIT 为你启用）

SolusVM 提供了面向客户的 API。向 DMIT 支持发邮件，询问他们是否为你的 VPS 暴露了 SolusVM API 密钥。如果他们提供了：

```python
import requests

# SolusVM 客户端 API 端点（DMIT 的 SolusVM 主机 —— 向对方询问）
SOLUSVM_URL = "https://vpsmanage.dmit.io/api.php"
KEY = "your_api_key"
HASH = "your_api_hash"

params = {
    "key": KEY,
    "hash": HASH,
    "action": "info",
    "status": "true",
    "bw": "true",      # 带宽信息
    "ipaddr": "true",
}
r = requests.get(SOLUSVM_URL, params=params)
print(r.text)  # 包含 <bw> 字段的 XML 响应
```

SolusVM API 响应中的 `bw` 字段提供了已使用/剩余/总带宽。如果对方授予了访问权限，这是最简洁的解决方案。

---

### 选项 4：直接联系 DMIT 支持

他们的支持响应迅速且对中文用户友好。直接询问：*“我能为我的 VPS 获取 SolusVM API 凭据吗？”* 某些 DMIT 套餐会暴露，某些则不会。

---

## 快速总结

| 方法 | 可靠性 | 工作量 |
|------|--------|--------|
| VPS 上的 `vnstat` | ✅ 最佳 | 5 分钟 |
| 爬取客户区域 | ⚠️ 脆弱 | 30 分钟 |
| SolusVM API（如已启用） | ✅ 干净 | 联系支持 |
| 官方 DMIT API | ❌ 不存在 | — |

对于你的用例（监控 CN2 VPN 流量配额），**在服务器上使用 `vnstat` + 设置 cron 任务推送到 Telegram** 是最可靠的路径，只需 10 分钟即可完成配置。
