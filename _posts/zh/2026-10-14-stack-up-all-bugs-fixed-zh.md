---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 堆叠更新，所有错误已修复
translated: true
type: note
---

完成。技术栈已启动、验证通过，所有修复已提交。以下是整体情况。

## 我做了什么

**1. 启动了技术栈**（从 Docker 挂载的可运行工作区副本 `~/.openclaw/workspace/live-server` 启动）：
- 全部 4 个容器均健康：`app`（PHP 8.5-FPM）、`database`（MySQL 5.7）、`redis`、`web`（nginx on :8088）。

**2. 全面检查了每个端点** — 所有 96 个 GET 路由 + 认证/直播写入流程。发现 **10 个端点故障 + 7 个潜在 bug**，全部可追溯到 CI3→CI4 的语义差异。

## 发现并修复的 bug

**数据库层**
- `BaseDao` 字段前缀有一个尾部点（`'users.'`），而 `mergeFields()` 会添加自己的点 → 生成无效 SQL `SELECT users..userId`。导致 `/users/:id` 被破坏。
- 关联数组绑定：CI3 的 `compile_binds()` 内部调用了 `array_values()`，因此关联数组绑定按位置工作；CI4 将字符串键名的绑定视为*命名*绑定（`:name`），因此 `WHERE x=?` 没有被替换 → 语法错误。已在 `RewardDao`、`CouponDao`、`WithdrawDao` 中修复。
- 控制器上缺少 `$this->db`；CI3 的 `trans_begin`/`affected_rows` → CI4 的 `transBegin`/`affectedRows`（16 处）。

**库 / 配置**
- `JSSDK`：`env('WECHAT_API_BASE'/'CGIBIN')` 是 **null**（它们是常量，不是环境变量）→ 所有 WeChat URL 都变成了相对路径。这就是 WeChat 此前报 `curl error'd` 的原因。
- `JSSDK`：缺少 `addNews`/`uploadImg`/`sendMassMsg`；`code` 参数可空（缺少 `?code=` 会导致 TypeError）。
- `WeChatClient::httpPost` 静默地**丢弃了 POST 请求体**，并且没有追加查询字符串。
- `LeanCloud` 读取了空的 `env('LC_PROD_APP_ID')`，而不是真正的 `LC_APP_ID` 常量 → 导致短信和直播创建失败。
- 启动时抑制了 `E_DEPRECATED`，因此 Qiniu SDK 在 PHP 8.4 下的弃用警告不再给每个 JSON 响应添加前缀。
- `Dockerfile` 配置了 GD，但从未安装它。

**控制器**
- `logout`（PHP 原生 `session_unset` 无法被覆盖）、`notifyLiveStartRecommend`（空值保护让 null 传到了 SQL）、`invitationCard`（未定义的 `phpInfo`）、`login` 和 `uploadImg`（空值解引用 → 500）。

## 验证通过

- **96/96 的 GET 路由**返回 200，且 JSON 干净。
- 完整的 **register → login → self → logout** 会话生命周期，cookie 和 token 认证均已验证。
- **Qiniu** uptoken、**Redis**（`PONG`）、**DB** 查询、**事务**（`topics/init` 生成了 13 个主题）、**WeChat JSSDK** 现在返回真实的签名和真实的 API 响应。

## 备注

- **直播创建唯一受阻于一个外部问题**：上游 LeanCloud 应用已归档（`504: The app is archived, please restore in console`）。代码是正确的——它现在发送真实的凭证（得到已认证的响应），而之前发送的是空的 `X-LC-Id`。只需要在 LeanCloud 控制台中恢复该应用即可。
- **两个工作副本现在完全一致**：主 git 仓库 `/home/lzw/projects/live-server`（2 个新提交，干净）和实际运行的工作区副本。我创建的测试用户已清理干净。

**提交**（在 `master` 分支上，未推送）：
- `41c879c` — CI4 迁移的主要 bug 修复（24 个文件）
- `3383cdb` — login 和 uploadImg 中的空值解引用保护

需要我推送这些提交，还是留在本地供你审查？