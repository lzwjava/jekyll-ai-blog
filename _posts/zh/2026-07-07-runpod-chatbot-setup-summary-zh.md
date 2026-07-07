---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RunPod聊天机器人设置摘要
translated: true
type: note
---

以下是本次会话的完整操作总结。

---

## RunPod LibreChat + SGLang 设置 — 完整总结

### 服务器
- **主机：** `213.173.110.200:23634`（密钥：`~/.ssh/id_ed25519`）
- **聊天机器人 URL：** `http://213.173.110.200:8888`（LibreChat 界面）

### 运行中的服务

| 服务 | 内部端口 | 状态 | 详情 |
|---------|-------------|--------|---------|
| **SGLang** | 30000 | ✅ | Qwen 2.5 14B AWQ，已通过 CUDA 图预热 |
| **MongoDB** | 27017 | ✅ | 数据位于 `/workspace/mongodb` |
| **LibreChat** | 8889 | ✅ | 通过 nginx 代理在 8888 端口提供服务 |
| **nginx** | 8888 | ✅ | 代理 8888 → 8889，超时时间 300 秒 |

### 已完成的操作

1. **检查服务器** — 发现 SGLang 在 30000 端口运行，搭载 Qwen 14B AWQ 模型。LibreChat 克隆在 `/workspace/LibreChat`，`.env` 和 `librechat.yaml` 已配置好指向 SGLang。

2. **释放 8888 端口** — 终止了占用该端口的 Jupyter Lab。

3. **启动 MongoDB** — `mongod --dbpath /workspace/mongodb --logpath /workspace/mongodb/mongod.log --fork`（之前未运行）。

4. **修复空的 `actions.ts`** — 由于浅层 git 克隆，`packages/data-provider/src/actions.ts` 文件大小为 0 字节。通过 `git checkout` 恢复。这引发了连锁反应：客户端 Vite 构建因缺少导出（`validateAndParseOpenAPISpec`、`openapiToFunction`）而失败。

5. **重建 Node 原生模块** — MongoDB 驱动 v6.20.0 的原生 BSON 附加组件与 Node v22.23.1 不兼容。`npm rebuild mongodb` 修复了 ABI 不匹配问题。

6. **构建客户端** — 依次执行 `npm run build:packages` 和 `vite build`，均成功。客户端构建产物位于 `/workspace/LibreChat/client/dist/`。

7. **更改端口** — `.env`：`PORT=8888` → `PORT=8889`。在 8888 端口添加 nginx 反向代理（`/etc/nginx/conf.d/librechat.conf`），转发至 8889 端口。这样确保了：
   - 外部请求访问 nginx 的 8888 端口
   - nginx 添加正确的代理头并设置 300 秒超时
   - LibreChat 后端在内部 8889 端口运行

8. **启动 LibreChat** — 在 8889 端口运行，通过 nginx 在 8888 端口对外提供服务。

### 保存到 `runpod/` 的文件

| 文件 | 用途 |
|------|---------|
| `start_services.sh` | 一键重启：MongoDB → 检查 SGLang → 重建原生模块 → 启动 LibreChat → 验证 |
| `build_librechat.sh` | 完整重建：恢复 git 文件 → 构建包 → Vite 客户端构建 |
| `start_librechat.md` | 运行手册，包含当前状态、服务表格、验证命令 |
| `setup_librechat.sh` | *(预先存在的)* 旧脚本，基于 3080 端口，仅供参考 |

### 遇到的关键问题

1. **浅层 git 克隆** → 空的 `actions.ts` → 客户端构建因缺少 OpenAPI 导出而失败
2. **Node v22 与 mongodb v6** → 原生附加组件 ABI 不匹配 → `require("mongodb")` 时进程静默挂起，无错误信息
3. **SSH 断开会终止子进程** → 通过 SSH 执行的 `nohup`/`&` 在断开连接后无法存活，必须使用 `setsid` + 后台终端
4. **LibreChat 的 DOMAIN_SERVER = 0.0.0.0** → 对外访问不正确，已切换为 `127.0.0.1` 作为 nginx 后端

### 访问方式

在浏览器中打开 `http://213.173.110.200:8888`。注册一个账户，然后在模型选择器中选择 **Qwen 2.5 14B AWQ** 即可开始聊天。