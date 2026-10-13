---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 关键付款存根需要修复
translated: true
type: note
---

现在情况已经很清楚了。以下是我发现的问题和按优先级排序的建议。

## 🔴 严重问题：支付是 stub——这是一个变现平台

CI3→CI4 迁移**悄悄地将你真实的支付 SDK 替换成了 safe-fail stubs**：

| | CI3（真实） | CI4（当前） |
| --- | --- | --- |
| `Alipay.php` | 85 行，真实的 RSA 签名 + 配置加载 | 56 行 **stub** → 返回 *"Alipay not configured"* |
| `WxPay.php` | 167 行，真实 API 集成 | 87 行 **stub** → 返回 *"WxPay not configured"* |
| `WxPayCallback.php` | 真实回调处理 | **stub** |
| `Pay.php` facade | 调用真实 SDK | 调用这些 stub |

真实的 CI3 代码仍然存在于 `application_ci3/libraries/{alipay,wx}/` 中，因此可以恢复——但**目前没有任何支付功能可用**。Go 测试确实覆盖了 `charges`/`attendances`/`wxpayNotify`，所以这是一个已确认的功能回归。

## 建议的后续步骤（按优先级排序）

**1. 恢复真实支付**（最高价值）——将 CI3 的 `alipay/` 和 `wx/` SDK 移植到 `app/Libraries/`，通过现有的 `Pay.php` facade（已正确迁移）接入。这些 stub 可以防止控制器崩溃，因此这是一个干净的替换。

**2. 重建 Docker 镜像**——我已修复 `Dockerfile` 以安装 GD，但*正在运行的容器*还没有安装它（`/lives/:id/card` 邀请卡片功能降级）。运行 `docker compose up -d --build app`。这能快速见效。

**3. 修复生产环境调试配置**——`app/Config/Boot/production.php` 中设置了 `display_errors=1` 和 `CI_DEBUG=true`。这会在生产环境中向客户端泄露堆栈跟踪信息。应改为 `CI_DEBUG=false`、`display_errors=0`。

**4. 全面排查 40 条 POST 路由**——我已手动验证了全部 96 条 GET 路由，但 POST 路由只验证了约 4 条。写入路径（charges、packets、withdraws、attendances）正是迁移 bug 的藏身之处。

**5. 让 Go 测试套件可运行**——它是你的回归防线，但目前无法运行：缺少 `test/go.mod`，目标端口 `3005` 已失效（应为 `8088`），数据库凭据 `lzw:@/qulive` 与 Docker MySQL（`root`/`WeImg4096`）不匹配。修复后，你就能获得迁移成功的自动化证明。

**6. 更新 `crontab.conf`**——它指向 `/home/project/live-server` 和 `/usr/local/php/bin/php`（旧服务器），而不是 Docker 环境。这些处理器（`Jobs::alive`、`Withdraws::withdrawAnchor/NonAnchor`）在 CI4 中都存在，所以只是路径/调用方式的修正。

**7. LeanCloud**——外部服务，但会阻止直播创建。请在 LeanCloud 控制台中恢复已归档的应用。

## 我的建议

从 **#1（支付）** 开始，因为它是核心业务功能，也是唯一一个真正的回归问题，而非配置问题。**#2 和 #3** 是 5 分钟就能完成的快速修复，我可以立即一并处理。

需要我怎么做：

- **(A)** 现在就开始移植 CI3 支付 SDK（大工程）？
- **(B)** 先做快速修复——重建镜像 + 修复生产环境调试配置（#2、#3）？
- **(C)** 两者并行？

你希望我往哪个方向推进？
