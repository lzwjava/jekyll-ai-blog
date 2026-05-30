---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Codex 2026年第二季度开发总结
translated: true
type: note
---

以下是过去约3个月（2026年3月至5月）Codex更新的全面总结，基于146次提交：

---

## 1. 扩展系统（`codex-rs/ext/`）

最大的架构变化——Codex现已拥有正式的扩展框架，包含6个扩展：

```
ext/
├── extension-api/    # 贡献者/注册系统
├── goal/             # 目标导向、记账、使用限制
├── guardian/         # 带提示缓存的安全审查
├── image-generation/ # 通过原生流水线的独立图像生成
├── memories/         # 专用SQLite记忆存储
└── web-search/       # 独立的web.run搜索工具
```

关键提交：
- **独立网络搜索扩展**（a22706d）——新的`web.run`工具直接调用`codex-api`搜索客户端，启用独立模式时隐藏托管版`web_search`
- **独立图像生成**（ecb41fc, 10b0399）——通过原生图像补全流水线的功能门控扩展路由
- **目标扩展**——通过`inject_if_running`进行导向、使用限制（bc00502）、遥测同等性、线程资格门控
- **守护者**——9次提交稳定了提示缓存键处理、审查指标以及跨会话的缓存复用

---

## 2. 线程/生命周期模型

线程和会话工作方式的重大重构：

- **线程空闲生命周期钩子**（d2ebb8d）——新的`thread-idle`贡献者
- **将任务完成接入线程空闲**（462deb0）
- **持久化会话接口**（c9dc0f6）——代码模式引入持久化
- **带对话轮次的线程恢复**（2a1158b）——应用服务器在恢复时包含对话轮次历史
- **分叉线程谱系**（1911021）——`forked_from_thread_id`元数据
- **子代理谱系元数据**（fc9cf62）——在Responses API中追踪代理祖先
- **每个线程存储的权限配置文件**（a1ecf0c）
- **从恢复的消息中提取提示历史**（56958f2）

---

## 3. Python SDK（Beta版）

Python SDK进入Beta阶段（`python-v0.1.0b1`，`python-v0.1.0b2`）：

- 独立的Beta版本发布流水线（4d0c4cd）
- 沙箱预设（b1cbf62）——用户友好的默认值
- 重命名`AppServerConfig`为`CodexConfig`（0db49a7）
- 文档和元数据清理
- `codex app-server --stdio`别名（b90ec46）供SDK使用者使用

---

## 4. TUI改进

- **Markdown表格渲染**——应用风格表格（6b4b15a）+ 紧凑表格作为键值记录（26c9502）
- **OSC 8网页链接**（7a26497）——终端中可点击的超链接
- **Vim文本对象**（8d398d3）——`iw`、`aw`等
- **可配置的对话轮次中断按键绑定**（2d1ad37）
- **统一提及**（6c1215d）——优化的@提及渲染
- **命名权限配置文件选择器**（f6fd753）
- **多行钩子输出**（251b241）
- **`/archive`斜杠命令**（36cd366）

---

## 5. Windows沙箱

Windows沙箱支持的活跃开发：

- 配置设置命令（cb9178e）
- 传递工作区根目录给运行器（986c604）
- 网络拒绝取消修复（3cf737e）
- 捕获取消测试根目录（bcf2b55）
- 移除旧的SandboxPolicy管道（0a6bc4e）

---

## 6. 清理/退役

- **debug-client完全移除**——8次提交删除了整个CLI、JSONL助手、事件读取器、清单、README及管道
- 从目录中移除Bedrock OSS模型（0a8c835）
- 移除冗余的SQLite动态工具存储（24819）
- 将记忆移至专用SQLite数据库（aad59a0）
- Rust工具链升级至1.95.0（cca1e0b）
- SQLx升级以支持更新的捆绑SQLite（379511d）

---

## 7. 安全与沙箱化

- 为安全命令保留拒绝读取的沙箱化（6e10142）
- Unix套接字权限设置为拒绝（bf72be5）
- WebSocket Origin头部拒绝（a027135）
- 阻止`/diff`执行仓库配置的代码（2e0c4f4）
- `exec-server` CoreFoundation环境保留（a717e4e）

---

## 8. 应用服务器协议

- 远程控制迁移至服务器令牌（912d7d4）
- 模型工具模式选择器（5577a9e）
- 工具UI可见性元数据（577ec03）
- 启动基准测试包（bd2a732，后回退）
- 用于工具调用的扩展TurnItemEmitter（2066874）

---

**总结**：最大的变化是**扩展系统**（目标、守护者、图像生成、网络搜索、记忆）——Codex正从单体核心转向插件架构。**Python SDK Beta版**正在发布。**线程生命周期模型**通过空闲钩子、恢复语义和分叉谱系进行了重大重构。TUI获得了显著的UX打磨。Windows沙箱正在积极建设中。旧的debug-client已完全退役。