---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 迁移代码已完成但未经核实
translated: true
type: note
---

## 项目：live-server (趣直播 知识直播平台后端)

### 简介
知识直播平台的 PHP 后端（约 80 场讲座，历史累计 30k+ 用户），在 `test/` 中有 Go 集成测试，Docker 部署，以及 SRS/RTMP 直播配置，微信/支付宝/七牛集成。

### 主要工作流：CodeIgniter 3 → CodeIgniter 4 迁移
根据 `MIGRATION_SUMMARY.md` / `README_MIGRATION.md`，迁移被声明为 **“已完成”**，完成度约 85%：

| 模块 | 状态 |
|---|---|
| 配置（`app/Config/` 中 25+ 个文件，145 条路由，448 个常量） | ✅ 100% |
| 控制器（26 个，包括新的 `Home`） | ✅ 100% |
| 模型/DAO（33 个） | ✅ 100% |
| CI3 兼容层（`CI3Compat.php`、支付存根、用于 JSSDK/WeChat/Pay/Sms/LeanCloud 的 CI4 库） | ✅ |
| Docker（php:8.5-fpm + MySQL 5.7 + Redis 7 + nginx + 可选的 Vite 前端构建） | ✅ |
| 框架安装 / composer | ✅ 已在工作区副本中完成 |
| **集成测试** | ⬜ **待处理** — MIGRATION_SUMMARY 中的检查清单仍有 9/10 项未勾选（认证、直播、数据库查询、微信、支付、上传、Redis、路由、会话） |

### Git 状态
- 10 个提交，全部来自 **2026 年 4 月 5 日至 7 日**，均已推送；`master` 干净且与 `origin/master` 同步（HEAD `4ce0cba`）。
- 最后 3 个提交是打磨：docker-compose 中的前端构建阶段、`NODE_ENV` 修复、`VITE_BASE_URL` + 应用端口重新映射 **8081 → 8082**（8081 被 llama-server 占用）。
- **自 2026 年 4 月以来没有提交**（今天是 2026 年 10 月 13 日）—— 项目已闲置约 6 个月。

### 当前运行状态：⚠️ 全部已停止
- 所有 5 个 compose 容器（`app`、`database`、`redis`、`web`、`frontend`）**大约 5 个月前退出** —— 8082/8088/3005 端口上没有服务在监听。
- `/home/lzw/projects/live-server` 的工作树缺少运行时文件：**没有 `.env`、没有 `vendor/`、没有 `writable/`、没有 `composer.lock`**（全部被 git 忽略）。
- 真正可运行的副本位于 `/home/lzw/.openclaw/workspace/live-server` —— 同一提交，但包含 `.env`（微信/七牛/支付宝密钥）、`vendor/`（root 所有）、`writable/`、`composer.lock`。旧的 `app` 容器绑定挂载的是那个路径，而不是 `projects/live-server`。
- 还缺少：`frontend` 构建服务所期望的兄弟仓库 `../live-mobile-web`。
- Go 测试（`test/*.go`，26 个文件）目标是 `http://localhost:3005/` —— 一个过时的端口（当前设置使用 8088 nginx / 8082 app），所以它们按现状运行会失败。

### 总结
**迁移代码已完成（约 85%），但功能上尚未验证。** 技术栈已停止运行，两个仓库副本已发生漂移（密钥/vendor 只在 openclaw 路径中），测试套件指向一个失效的端口。最有价值的下一步：

1. `docker compose up -d`（从工作区副本）并对 `GET /` + 认证 + `/lives/attended` 端点进行冒烟测试
2. 协调两个检出副本 —— 复制 `.env`、`vendor/`、`writable/`，或者使 `projects/` 成为规范目录
3. 将 `test/client.go` 指向实际端口，并针对实际端点运行 Go 测试套件

要我启动整个技术栈并开始运行验证清单吗？