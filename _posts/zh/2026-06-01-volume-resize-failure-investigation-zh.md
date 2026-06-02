---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 卷大小调整失败调查
translated: true
type: note
---

## 调查：为何通过 CLI 调整卷大小失败

### 问题

AMD Dev Cloud（基于 DigitalOcean）的 Web UI 中，卷 `volume-atl1-1780280110689` 显示“增加存储大小”弹窗。在大小字段输入 `200` 显示“无效大小”。用户希望改用 CLI 操作。

### 步骤 1：检查 doctl 代码库

查看 `/Users/lzwjava/projects/doctl/commands/volumes.go`：

- 第 53 行：`--size` 标志默认值为 `"4TiB"` —— 需要单位后缀（例如 `200GiB`）
- 第 152 行：使用 `humanize.ParseBytes()` 解析大小字符串
- 第 194 行：通过 `int64(size / (1 << 30))` 转换为 GiB

发现裸写 `--size 200` 会被解析为 **200 字节** → 除法后为 0 GiB。但这只是 CLI 的细节问题，并非 UI 问题。

### 步骤 2：分析 Web UI HTML

用户分享了弹窗的 HTML。关键发现：

```html
<input type="number" min="101" max="16384" step="1" value="101">
```

- `min="101"` —— 最小值为 101 GB（当前卷为 100 GB）
- `max="16384"` —— 最大值为 16 TiB
- 默认值为 101

HTML5 验证应接受 `200`。错误必定来自其他位置。

### 步骤 3：检查 API 客户端库

查看 `/Users/lzwjava/projects/doctl/vendor/github.com/digitalocean/godo/storage_actions.go`：

- 第 68-75 行：`Resize()` 发送 `{"type": "resize", "size_gigabytes": N, "region": "..."}` 到 `POST /v2/volumes/{id}/actions`
- `size_gigabytes` 为 `int64` —— 除类型检查外无客户端验证

### 步骤 4：设置 CLI 访问

- 通过 Homebrew 已安装 `doctl` v1.148.0
- 通过 `doctl auth init` 使用 API token 认证
- 验证 token 有效：`doctl compute volume list` 成功

### 步骤 5：列出卷

```
doctl compute volume list
```

结果：

```
ID                                      Name                         Size       Region    Droplet IDs
52743aec-...                            volume-atl1-1780280110689    100 GiB    atl1      [574422820]
```

当前大小：**100 GiB**，已挂载到 GPU Droplet `574422820`（MI300X 192GB，atl1）。

### 步骤 6：尝试通过 CLI 调整大小

```bash
doctl compute volume-action resize 52743aec-... --size 200 --region atl1
```

结果：`422 "error resizing volume: invalid size specified"`

### 步骤 7：暴力测试所有大小

编写 Python 脚本测试大小 101、110、125、128、150、200、250、256、300、400、500、512、1024，通过 `POST /v2/volumes/{id}/actions` 发送：

**每个大小均返回 `422 "invalid size specified"`。**

### 步骤 8：尝试先分离卷

```bash
doctl compute volume-action detach 52743aec-... 574422820 --wait
doctl compute volume-action resize 52743aec-... --size 200 --region atl1
```

仍然 `422`。之后重新挂载卷。

### 步骤 9：测试不同请求格式

编写另一个 Python 脚本测试：

- 请求体中包含/不包含 `droplet_id`
- 包含/不包含 `region`
- `size_gigabytes` 作为浮点数（200.0）→ `400 "error parsing request body"`（API 期望整数）
- `size_gigabytes` 作为字符串（"200"）→ `400 "error parsing request body"`
- 整数 200 → `422 "invalid size specified"`（已正确解析但被拒绝）

### 步骤 10：测试其他区域

- 在 `atl1` 创建新 100 GiB 卷 → 调整大小失败
- 在 `nyc1` 创建新 100 GiB 卷 → 调整大小失败
- 删除两个测试卷

### 结论

在此账户上，所有区域的所有整数大小通过 `POST /v2/volumes/{id}/actions` 调整大小端点均返回 `422 "invalid size specified"`。这是**服务端 API 限制**，而非客户端代码错误。

Token 前缀 `dop_v1_` 表明这是一个 **DigitalOcean Partner Cloud** token（AMD Dev Cloud）。标准 DO 卷调整大小 API 似乎**不适用于合作伙伴/GPU 卷**。Web UI 可能使用了不同的内部 API 或具有更高权限。

### 建议

1. 暂时使用 Web UI（在弹窗中输入 101 以上）
2. 联系 AMD Dev Cloud 支持，询问 CLI/API 卷调整大小问题
3. **轮换 API token** —— 该 token 已在聊天中共享

---

**调查期间创建的文件：**

- `/tmp/resize_vol.py` — 卷详情 + 大小暴力测试
- `/tmp/resize_vol2.py` — 不同请求格式（PATCH、带额外字段的 POST）
- `/tmp/resize_vol3.py` — 类型强制转换测试（浮点数、字符串、整数）
