---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 升级CodeIgniter框架
translated: true
type: note
---

老大，这活儿可不小。从 CI3 升级到 CI4 完全是 **一次彻底重写** —— 目录结构、核心类、配置格式、路由以及几乎所有代码模式都变了。这绝不是一项轻松的任务。

让我完整介绍一下需要做的改动：

**核心变动：**

- `application/` → `app/`，`system/`目录移除（现为 Composer 包）
- `Controllers` 继承 `BaseController` 而非 `CI_Controller`
- `Models` 继承 `Model` 而非 `CI_Model`
- 配置文件：`config/` → `app/Config/`，采用新的 PHP 命名空间
- 路由：`config/routes.php` 采用新格式
- 环境文件 `.env` 取代大部分 `config/config.php` 设置
- 辅助函数/类库需重写（不再有 `get_instance()`）
- HMVC 架构需要第三方包支持
- 数据库：`application/config/database.php` → `app/Config/Database.php`
- 必须使用 Composer（不再支持手动复制类库）

**导致 PHP 8.5 无法运行的真正问题：**

- CI3 设计时基于 PHP 5.6-7.x 环境，许多 mysql 函数在 8.x 版本中已被移除
- 多处 `mysql_*` 函数需替换为 `mysqli_*`
- 众多过时特性需要修正

**我的建议：** 这是一个需要分阶段完成的重构项目。建议您启动一个 coding agent 来系统处理 —— 读取现有 CI3 代码，逐步映射至 CI4 模式，并进行系统化的重写工作。

需要我现在就开始吗？我可以在后台运行这个任务并定期汇报进度。这肯定不是五分钟就能完成的 —— 更可能需要数小时甚至更长时间，涉及大量文件的修改。🦞
