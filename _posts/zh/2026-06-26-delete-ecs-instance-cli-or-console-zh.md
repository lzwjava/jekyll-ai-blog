---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 删除ECS实例：CLI还是控制台？
translated: true
type: note
---

阿里云CLI已安装但未配置——缺少凭证。您有两个选择：

**选项1：配置CLI（需要您的AccessKey）**

```
aliyun configure
# 输入：AccessKey ID、AccessKey Secret、地域：cn-hongkong
# 然后：aliyun ecs DeleteInstance --InstanceId i-j6civepr8vf1085n7x0u --Force true
```

**选项2：网页控制台（更快捷）**
访问 <https://ecs.console.aliyun.com> → 在香港区域找到实例 `i-j6civepr8vf1085n7x0u` → 删除

您想配置CLI，还是直接从网页控制台删除？
