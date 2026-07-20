---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 刷新逻辑正确且完整
translated: true
type: note
---

是的，刷新逻辑已经就位。**`_get_credentials()`** 在第124–125行：

```python
# 刷新或获取新凭据
if credentials and credentials.expired and credentials.refresh_token:
    credentials.refresh(Request())
```

完整流程按回答中的描述运行：

1. **加载** 来自 `~/.google/youtube_upload_token.json` 的缓存令牌
2. 如果过期且存在 `refresh_token`，则**自动刷新**
3. 如果没有有效令牌，则**回退**到浏览器 OAuth
4. 每次认证周期后**保存**（可能已刷新的）令牌回磁盘（第145–146行）

无需更改——刷新逻辑正确且完整。