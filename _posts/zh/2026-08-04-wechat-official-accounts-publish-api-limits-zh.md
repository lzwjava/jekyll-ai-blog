---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 微信公众号发布API限制
translated: true
type: note
---

问题：微信公众号不支持通过 API 发布文章，对吗？

回答：**基本正确——微信公众号并未提供通用的公开 API，允许普通账号直接向公众平台发布文章。** 不过，确实存在一些有限的发布 API。

具体情况如下：

### 1. 普通公众号

对于大多数账号：

* ✅ 支持通过 API 进行：
  * 上传图片/素材
  * 管理菜单
  * 获取粉丝列表
  * 发送模板消息/客服消息（有频率限制）
  * 管理草稿（较新的 API）
* ❌ 没有无限制的“立即发布此文章”API

长期以来，工作流程是：

```
你的 CMS
    |
    v
微信 API
    |
    v
草稿文章
    |
    v
人工在微信后台点击“发布”
```

最后的发布步骤通常需要手动确认。

---

### 2. 微信 API 提供了草稿 + 发布接口

腾讯针对某些场景引入了内容发布 API。

典型流程：

```
POST /cgi-bin/material/add_news
        |
        v
创建草稿
        |
        v
POST /cgi-bin/freepublish/submit
        |
        v
发布
```

接口地址：

```
https://api.weixin.qq.com/cgi-bin/freepublish/submit
```

允许提交草稿进行发布。

但需满足以下条件：

* 账号必须拥有相应权限
* 账号类型有要求
* 部分功能需经过认证
* 有频率限制

许多小型个人公众号无法使用此功能。

---

### 3. 微信为何限制此功能

微信的生态与博客/Twitter 不同：

如果任何人都能执行：

```python
wechat.publish(
    title="xxx",
    content="spam"
)
```

那么数百万机器人就能大量发布：

* 垃圾文章
* 虚假新闻
* SEO 农场内容
* 钓鱼页面

因此，腾讯将发布功能置于账号权限和审核机制之后。

---

### 4. 常见的自动化架构

大型发布方通常构建：

```
Markdown
   |
   v
CMS
   |
   +--> Jekyll / Hugo 博客
   |
   +--> 微信排版工具
           |
           v
       草稿 API
           |
           v
       微信后台审批
```

常用工具如：

* Markdown → 微信排版
* mdnice
* OpenWrite
* 自建 CMS

通常自动化的是**格式排版 + 草稿创建**，而非完全无人值守的发布。

---

### 5. 针对你的 AI 博客 / 社区场景

鉴于你已在运行 `lzwjava.github.io` 并涉及 AI 内容：

一个实用的流程是：

```
GitHub Markdown
       |
       v
GitHub Actions
       |
       +--> Jekyll 网站
       |
       +--> 生成微信 HTML
                    |
                    v
             上传草稿到公众号
                    |
                    v
             一键发布
```

你可以自动化 95% 的流程，但除非你的公众号拥有必要的 API 权限，否则建议保留最终发布的手动操作。

参考资料：

* 微信公众号 API 文档：[https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html](https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html)
* 微信发布接口：[https://developers.weixin.qq.com/doc/offiaccount/Publish/Publish.html](https://developers.weixin.qq.com/doc/offiaccount/Publish/Publish.html)