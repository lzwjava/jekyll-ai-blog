---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复OAuth测试模式错误
translated: true
type: note
---

问题：为什么 YouTube Data API OAuth 显示 `ZhiweiTextToSpeech has not completed the Google verification process` 和 `Error 403: access_denied`？

答案：

这**不是 YouTube Data API 的问题**，而是 **Google OAuth 同意屏幕配置问题**。

你的 OAuth 应用（`ZhiweiTextToSpeech`）当前处于**测试模式**，而你使用的 Google 账户（`lzwjava@gmail.com`）未被列为测试用户。

---

## 为什么会发生

当你创建 OAuth 凭据时，Google 会创建一个 OAuth 应用：

```
Google Cloud 项目
        |
        |
OAuth 同意屏幕
        |
        |
ZhiweiTextToSpeech
        |
        |
YouTube Data API 范围：
youtube.upload
```

因为你请求了敏感范围，例如：

```
https://www.googleapis.com/auth/youtube.upload
```

对于**公开应用**，Google 要求 OAuth 验证。

但对于个人/私有工具，通常不需要验证。

你可以使用**测试模式**。

---

## 修复：将你自己添加为测试用户

前往：

[Google Cloud Console](https://console.cloud.google.com/?utm_source=chatgpt.com)

然后：

```
API 和服务
    |
    OAuth 同意屏幕
    |
    受众群体
```

你应该看到：

```
发布状态：
测试
```

找到：

```
测试用户
```

添加：

```
lzwjava@gmail.com
```

保存。

然后等待几分钟。

重试：

```bash
python upload.py
```

---

## 如果你之前已经授权过

删除缓存的 OAuth 令牌。

你的脚本可能创建了：

```
token.json
```

或：

```
token.pickle
```

删除它：

```bash
rm token.json
rm token.pickle
```

再次运行：

```bash
python upload.py
```

重新在浏览器中登录。

---

## 替代方案：将应用设为内部

仅当使用 Google Workspace 时才可用：

```
OAuth 同意屏幕

用户类型：
    内部
```

这样就不需要验证。

对于普通 Gmail 账户：

```
外部 + 测试
```

是正确的。

---

## 为什么 Google 说“验证”

令人困惑的部分：

> "has not completed the Google verification process"

听起来像是你需要提交应用审核。

如果满足以下条件，则**不需要**：

* 只有你使用
* 只有少数测试者使用
* 是你自己的 CLI 工具

Google 允许在测试模式下最多 100 个测试用户。

---

## 对于你的 AI 视频上传器

我会保持这样：

```
OAuth 同意屏幕：
    外部

发布状态：
    测试

测试用户：
    你的 Gmail

范围：
    youtube.upload
```

然后你的 agent 可以使用：

```
video_agent
    |
    +-- generate_video()
    |
    +-- generate_thumbnail()
    |
    +-- youtube_upload()
          |
          +-- refresh_token.json
```

无需验证。

刷新令牌将持续有效，直到你撤销访问权限或更改 OAuth 配置。