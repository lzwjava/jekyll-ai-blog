---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 支付SDK移植完成且已验证
translated: true
type: note
---

支付 SDK 移植已完成，已提交，已推送，并且两个 checkout 已验证完全一致。

## ✅ 我所做的（#1 — 恢复真实支付）

**根本问题：** CI3→CI4 迁移过程悄悄地将支付层替换成了安全失败桩代码，导致在商业化平台上没有任何支付能够工作。

已将真实 SDK（5,769 行）从 `application_ci3/libraries/{alipay,wx}` 移植到 `app/Libraries/`，以及商户密钥和证书。

修复了旧版 SDK 中的 PHP 8.5 阻塞问题（已在容器内验证）：
- `each()` → `foreach`（在 PHP 8 中已移除）
- `get_magic_quotes_gpc()` → 删除（该函数在 PHP 8 中已移除）
- `substr(count($arg)-2)` → `substr(...,-1)`（对字符串使用 count() 会抛出 TypeError）
- `implode(array, glue)` 参数顺序颠倒 → `implode(glue, array)`
- `strftime()` → `date()`；删除已弃用的 `openssl_free_key()`；`final private` → `private`；`APPPATH` 证书路径 → `__DIR__` 相对路径；所有 `require_once` → `__DIR__` 绝对路径

重写了 3 个包装类，其公共 API 与 CI3 完全一致：`Alipay.php`（RSA 订单签名）、`WxPay.php`（7 个方法：统一订单/退款/转账/红包）、`WxPayCallback.php`（继承 SDK 的 `WxPayNotify`）。为商户配置创建了 `Config\Alipay`。

修复了移植过程中暴露的 3 个潜在 bug：
- `guard()` 包装器，使 SDK 传输异常变成 `[false, msg]` 元组，而不是 500 错误
- `unifiedOrder` 现在检查 `result_code`（业务）而不只是 `return_code`（传输）——CI3 只检查传输层，因此业务失败时读取缺失的键（在 PHP 7 中静默，在 CI4 中返回 500）
- `PayNotifyDao` 在读取属性前进行空值检查（CI3 先解引用 → 在未知 orderNo 时返回 500，可从回调触发）

## ✅ 端到端验证（真实 API 调用）

| 渠道 | 结果 |
|---|---|
| `alipay_app` | **真实的 RSA 签名订单字符串** ✓ |
| `wechat_qrcode` | **可到达微信**，呈现真实的商户状态消息 ✓ |
| `wechat_h5` / `wechat_app` | `must_bind_wechat`（正确的业务验证） ✓ |
| `apple_iap` | 充值记录已持久化到数据库 ✓ |

96/96 个 GET 路由仍然通过，没有 500 错误，所有文件 lint 检查通过，测试数据已清理。

## 📦 Git

- 提交 `e24302e` 已推送到 `origin/master`
- **两个 checkout 已验证完全一致**：相同 HEAD，干净工作树，源码逐字节一致，两个 checkout 中都存在所有支付文件，过时的桩代码已从两者中移除

## ⚠️ 两个外部阻塞项（不是代码问题 — 需要你处理）

1. **微信商户证书已于 2026-09-11 过期**，并且使用 MD5（被 OpenSSL 3.x 拒绝）。请从微信商户平台重新下载。
2. **微信商户账户当前被限制** — 微信官方回应：*“此商家的收款功能已被限制”*。请检查商户控制台。
3. 另外还有此前的待办：**LeanCloud 应用已归档**（阻止创建 live 实例）。

代码已就绪 — 一旦这些凭据/账户问题得到解决，支付将无需进一步修改即可正常工作。