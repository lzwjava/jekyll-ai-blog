---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 内联依赖确保可靠性
translated: true
type: note
---

搜索代码库中的"写一篇关于此的博客教程"，找到22条结果

以下是一篇博客教程草稿：

---

## 内联你的依赖项：一则代理配置的启示

我最近通过移除外部规则提供者并直接内联规则，简化了Clash代理配置。这虽然是个小改动，却揭示了一个远超出代理配置范围的原则。

### 改造前：外部依赖

```yaml
rule-providers:
  AIRule:
    type: http
    behavior: classical
    path: ./Rules/AI.yaml
    url: https://raw.githubusercontent.com/lzwjava/blog-source/.../AI.yaml
    interval: 1440
```

这种写法看起来很简洁。`rules`部分只需一行代码——`RULE-SET,AIRule,Proxy`——就能处理所有AI相关流量。但这份优雅背后隐藏着多个假设：

- GitHub在启动时可访问
- 该URL仍然存在且未移动位置
- 远程文件未发生非预期变更
- `./Rules/AI.yaml`的本地缓存足够新鲜

以上任何一点都可能静默失效。代理规则将出现故障，而你未必能察觉错误——流量只会被错误路由。

### 改造后：自包含配置

```yaml
rules:
  - DOMAIN-SUFFIX,claude.ai,Proxy
  - DOMAIN-SUFFIX,openai.com,Proxy
  - DOMAIN-SUFFIX,anthropic.com,Proxy
  - DOMAIN-SUFFIX,gemini.google.com,Proxy
  # ... 等等
```

冗长吗？确实。但现在配置本身就是唯一真相源。它在离线状态、首次启动、Docker容器、新机器上——任何场景，始终可用。

### 通用原则

外部依赖是用**未来脆弱性**交换**当下便利性**。这种现象随处可见：

| 场景 | 外部依赖 | 自包含方案 |
|---|---|---|
| 代理配置 | 远程规则文件 | 内联规则 |
| CI流水线 | 从URL下载脚本 | 本地化脚本 |
| 前端开发 | CDN托管库 | 打包入库 |
| Docker镜像 | 运行时`apt install` | 预置入镜像 |
| 配置文件 | 远程获取环境变量 | 本地.env文件 |

模式始终如一：在运行时获取外部资源会引入不可控的故障点。

### 何时值得使用外部依赖

内联并非永远正确。外部依赖在以下情况仍具意义：

- 规则集**体量巨大**（数百个IP网段）且频繁变更
- 需要在多台机器间**集中更新**
- 依赖项具有**稳定、版本化的受控URL**

在当前案例中，AI域名列表简短（约15条）、极少变更，且源文件本就归我所有——因此保留外部依赖并无实质益处。

### 核心启示

在添加外部依赖前，请思考：*若此依赖不可用，会发生什么？* 如果答案是"系统将静默崩溃"，请考虑是否能够将其内联。自包含系统虽显平淡，却具有最佳特质——它们始终如一地稳定运行。