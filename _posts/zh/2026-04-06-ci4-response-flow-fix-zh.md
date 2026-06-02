---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CI4响应流修复
translated: true
type: note
---

完成。以下是修复内容：

**核心问题在于CI3→CI4的响应流程不匹配。** 在CI3中，`succeed()`/`failure()`会直接输出JSON并由框架捕获。在CI4中，`gatherOutput()`会用自己的输出缓冲区覆盖响应体——因此调用`$this->response->setJSON()`却未实际向缓冲区写入内容，导致**每次响应都返回零字节**。

**已应用的修复：**

1. **`BaseController::responseResult()` 与 `responseJSON()`** —— 添加了`echo $response->getBody()`使JSON能够进入CI4的输出缓冲区。这是务实的修复方案，因为数百个控制器调用点都在没有`return`的情况下使用`succeed()`/`failure()`。

2. **`Lives::attended()`** —— 添加了空会话守卫。当不存在认证会话时，原本会在`$curUser->userId`处崩溃。

3. **缺失的`KEY_IS_SCANNED`常量** —— 已添加至Constants.php。

**30/30路由 → HTTP 200状态码并返回正确JSON响应体** ✅

提交记录：`74783ee`，已推送至GitHub。

待处理事项：真实登录会话测试、支付桩模块、数据库迁移。接下来需要我处理其中任何一项吗？
