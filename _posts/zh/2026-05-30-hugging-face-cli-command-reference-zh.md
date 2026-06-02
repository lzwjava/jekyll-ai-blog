---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hugging Face CLI 命令参考
translated: true
type: note
---

以下是完整的 `hf` CLI 映射，按组组织。所有命令都位于 `hf` 入口点之下。

## 顶层命令（无子组）

```
hf download <repo_id> [filenames...]    # 从仓库下载文件
hf upload <repo_id> <local_path>        # 上传文件/文件夹到仓库
hf upload-large-folder <repo_id> <dir>  # 分块上传大文件夹
hf sync <bucket_id> <local_dir>         # 与存储桶同步
hf env                                  # 打印环境信息
hf update                               # 检查 huggingface_hub 更新
hf version                              # 打印版本
```

## `hf auth` — 身份认证

```
hf auth login              # 交互式登录（提示输入 token）
hf auth login --token $HF_TOKEN --add-to-git-credential
hf auth logout             # 从机器移除 token
hf auth whoami             # 显示当前用户/组织
hf auth token              # 打印原始 token（可管道至 curl 等）
hf auth list | ls          # 列出所有已存储的 token
hf auth switch <name>      # 切换激活的 token
```

## `hf repos`（别名 `hf repo`）— 仓库增删改查（CRUD）

```
hf repos list | ls         # 列出你的仓库（或 --namespace）
hf repos create            # 创建新仓库
hf repos delete            # 删除仓库
hf repos duplicate         # 复刻/复制仓库
hf repos move              # 重命名/移动仓库
hf repos settings          # 更新仓库设置
hf repos delete-files      # 从仓库删除特定文件

hf repos branch create     # 创建分支
hf repos branch delete     # 删除分支

hf repos tag create        # 创建标签
hf repos tag list | ls     # 列出标签
hf repos tag delete        # 删除标签
```

## `hf models` — 浏览模型

```
hf models list | ls        # 搜索/列出模型
hf models info             # 模型元数据
hf models card             # 显示模型卡片（README）
```

## `hf datasets` — 浏览数据集

```
hf datasets list | ls      # 搜索/列出数据集
hf datasets info           # 数据集元数据
hf datasets card           # 显示数据集卡片
hf datasets leaderboard    # 数据集排行榜
hf datasets parquet        # 显示 parquet 信息
hf datasets sql            # 使用 SQL 查询数据集
```

## `hf spaces` — Spaces（托管的 Gradio/Streamlit 应用）

```
hf spaces list | ls        # 列出 spaces
hf spaces info             # space 元数据/状态
hf spaces card             # 显示 space 卡片
hf spaces search           # 搜索 spaces
hf spaces ssh              # SSH 进入正在运行的 space
hf spaces pause            # 暂停 space
hf spaces restart          # 重启 space
hf spaces hardware         # 获取/设置硬件（CPU/GPU/TPU）
hf spaces settings         # 更新 space 设置
hf spaces logs             # 追踪 space 日志
hf spaces hot-reload       # 开发期间热重载

hf spaces volumes list | ls    # 列出持久卷
hf spaces volumes set          # 挂载卷
hf spaces volumes delete       # 卸载卷

hf spaces secrets list | ls    # 列出 space 密钥
hf spaces secrets add          # 添加密钥
hf spaces secrets delete       # 删除密钥

hf spaces variables list | ls  # 列出 space 变量
hf spaces variables add        # 添加变量
hf spaces variables delete     # 删除变量
```

## `hf jobs` — 训练任务（HF 推理/训练）

```
hf jobs run                # 启动训练任务
hf jobs uv run             # 通过 uv 启动（从 pyproject.toml 自动构建）
hf jobs logs               # 追踪任务日志
hf jobs stats              # 任务资源统计
hf jobs ps                 # 列出运行中的任务
hf jobs hardware           # 列出可用硬件
hf jobs inspect            # 检查任务
hf jobs cancel             # 取消任务
hf jobs labels             # 管理任务标签

hf jobs scheduled ...      # 定时/重复任务
  ps | inspect | delete | suspend | resume
hf jobs scheduled uv ...   # 定时 uv 任务
```

## `hf endpoints` — 推理端点

```
hf endpoints list | ls         # 列出端点
hf endpoints deploy            # 部署新端点
hf endpoints describe          # 端点详情
hf endpoints update            # 扩缩容/配置
hf endpoints delete            # 删除
hf endpoints pause             # 暂停
hf endpoints resume            # 恢复
hf endpoints scale-to-zero     # 缩到零（节省成本）
hf endpoints catalog           # 列出可用实例类型
```

## `hf buckets` — 存储桶（类似 S3）

```
hf buckets create          # 创建存储桶
hf buckets list | ls       # 列出存储桶
hf buckets info            # 存储桶详情
hf buckets delete          # 删除存储桶
hf buckets sync            # 同步本地目录 ↔ 存储桶
```

## `hf cache` — 本地缓存管理

```
hf cache list | ls         # 扫描并列出缓存的仓库
hf cache delete            # 删除特定缓存的仓库
hf cache prune             # 移除旧的/孤立的缓存条目
```

## `hf collections` — 精选集合

```
hf collections list | ls       # 列出集合
hf collections info            # 集合详情
hf collections create          # 创建集合
hf collections update          # 更新元数据
hf collections delete          # 删除
hf collections add-item        # 向集合中添加仓库
hf collections update-item     # 更新项目
hf collections delete-item     # 移除项目
```

## `hf discussions` — PR 与讨论

```
hf discussions list | ls       # 列出仓库的讨论/PR
hf discussions info            # 讨论详情
hf discussions create          # 开启讨论
hf discussions comment         # 添加评论
hf discussions close           # 关闭
hf discussions rename          # 重命名
hf discussions merge           # 合并 PR
```

## `hf webhooks` — Webhook 管理

```
hf webhooks list | ls      # 列出 webhooks
hf webhooks info           # webhook 详情
hf webhooks create         # 创建 webhook
hf webhooks update         # 更新
hf webhooks enable         # 启用
hf webhooks disable        # 禁用
hf webhooks delete         # 删除
```

## `hf papers` — 学术论文

```
hf papers list | ls        # 列出热门论文
hf papers search           # 搜索论文
hf papers info             # 论文详情
hf papers read             # 阅读论文内容
```

## `hf skills` — AI 代理技能市场

```
hf skills list | ls        # 列出已安装的技能
hf skills preview          # 预览技能
hf skills add              # 安装技能
hf skills update           # 更新已安装的技能
```

## `hf extensions`（别名 `hf ext`）— CLI 扩展

```
hf ext ...                 # 用户安装的 CLI 扩展
```

## Python API（HfApi 类）

CLI 是对 `hf_api.py`（约 11000 行）中 `HfApi` 的轻量封装。编程中常用的主要方法：

```python
from huggingface_hub import HfApi
api = HfApi()

# 认证
api.whoami()                           # 当前用户信息
api.get_token_permission()             # token 角色

# 仓库
api.list_repos()                       # 列出仓库
api.create_repo()                      # 创建
api.delete_repo()                      # 删除
api.duplicate_repo()                   # 复刻
api.rename_repo()                      # 移动

# 文件
api.upload_file()                      # 上传单个文件
api.upload_folder()                    # 上传文件夹
api.upload_large_folder()              # 分块上传大目录
api.hf_hub_download()                  # 下载单个文件
api.snapshot_download()                # 下载整个仓库
api.list_repo_files()                  # 列出仓库中的文件
api.delete_files()                     # 删除文件
api.repo_info()                        # 仓库元数据

# 分支/标签
api.create_branch() / api.delete_branch()
api.create_tag() / api.delete_tag() / api.list_repo_refs()

# 模型
api.list_models()                      # 搜索模型
api.model_info()                       # 模型元数据

# 数据集
api.list_datasets()                    # 搜索数据集
api.dataset_info()                     # 数据集元数据

# Spaces
api.list_spaces()                      # 搜索 spaces
api.space_info()                       # space 元数据
api.restart_space() / api.pause_space()
api.set_space_hardware()
api.add_space_secret() / api.delete_space_secret()

# 讨论/PR
api.get_repo_discussions()
api.create_discussion()

# 推理
api.list_inference_endpoints()
api.create_inference_endpoint()
api.get_inference_endpoint()

# 集合
api.list_collections() / api.get_collection()
api.create_collection() / api.delete_collection()

# 任务
api.list_jobs() / api.create_job()
```

模式始终是：**CLI 命令 → `hf_api.py` 方法 → HF REST API**。CLI 在此基础上添加了输出格式化（表格/JSON）、交互式提示和错误处理。
