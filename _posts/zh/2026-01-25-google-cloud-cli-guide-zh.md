---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Google Cloud CLI 完整指南
translated: true
type: note
---

Question: Give a comprehensive introduction to Google Cloud CLI

Answer: 

**Google Cloud CLI**（通常被称为 **gcloud CLI**）是与 Google Cloud Platform (GCP) 交互的官方命令行界面。它是开发者、DevOps 工程师和管理员直接从终端创建、管理、配置和自动化几乎所有 Google Cloud 资源的主要工具。

### What is included in the Google Cloud CLI?

现代 Google Cloud CLI 是一个包含多个重要工具的单一捆绑发行版：

- **gcloud** – 用于大多数 Google Cloud 服务的主命令（authentication、configuration、Compute Engine、GKE、Cloud Run、Cloud Functions、IAM、billing 等）。
- **gsutil** – 用于 Google Cloud Storage 操作的强大工具（upload、download、rsync、ACLs、lifecycle management 等）。
- **bq** – BigQuery 的命令行工具（query、load data、manage datasets/tables、show schema 等）。
- **kubectl** – 通常包含在内（Google Kubernetes Engine 友好版本）。
- 额外组件（根据需求安装）：`app-engine-go`、`cloud-build-local`、emulators、`anthos-auth` 等。

### Key Features and Concepts

- **分层命令结构**  
  命令遵循以下模式：  
  `gcloud [GROUP] [COMMAND] [SUB-COMMAND] [FLAGS] [ARGUMENTS]`

  示例：
  - `gcloud compute instances list`
  - `gcloud container clusters get-credentials my-cluster`
  - `gcloud functions deploy my-func --gen2 --trigger-http --runtime nodejs20`
  - `gcloud alpha services identity create ...`（early access 特性）

- **Release tracks / 命令稳定性级别**
  - **GA** (General Availability) – 稳定，production-ready。
  - **beta** – 相当稳定，被许多团队在 production 中使用。
  - **alpha** – 实验性，可能在不通知的情况下更改或消失。

  运行方式如下：
  ```bash
  gcloud beta run services list
  gcloud alpha network-security security-profiles list
  ```

- **Configuration & Contexts**
  gcloud 维护着命名配置（类似于 kubectl contexts）：
  ```bash
  gcloud config configurations create prod
  gcloud config configurations activate dev
  gcloud config set project my-prod-project-123
  gcloud config set compute/zone us-central1-c
  ```

- **Authentication & Authorization**
  常见流程：
  - `gcloud init` → 交互式设置（建议首次使用时运行）。
  - `gcloud auth login` → 用户凭据。
  - `gcloud auth application-default login` → 为 SDKs 和本地开发提供的 ADC (Application Default Credentials)。
  - Service account 密钥文件：`gcloud auth activate-service-account --key-file=sa.json`。

- **输出格式**  
  对脚本非常友好：
  ```bash
  gcloud compute instances list --format="value(name,zone,status)"
  gcloud projects list --format="table(projectId, name, state)"
  gcloud asset search-all-resources --format="yaml"
  ```

- **用于本地开发的 Emulators**
  ```bash
  gcloud beta emulators firestore start
  gcloud beta emulators pubsub start
  gcloud beta emulators bigtable start
  ```

### Typical Use Cases

| Task                              | Example Command(s)                                      |
|:----------------------------------|:--------------------------------------------------------|
| Create / manage VM                | `gcloud compute instances create ...`                   |
| Deploy Cloud Run service          | `gcloud run deploy ...`                                 |
| Deploy 2nd-gen Cloud Function     | `gcloud functions deploy ... --gen2`                    |
| Manage GKE cluster                | `gcloud container clusters create-auto ...`             |
| Upload/download files to GCS      | `gsutil cp -r ./data gs://my-bucket/`                   |
| Run BigQuery query                | `bq query --nouse_legacy_sql 'SELECT ...'`              |
| Impersonate service account       | `gcloud auth configure-docker --impersonate-service-account=...` |
| Enable service                    | `gcloud services enable artifactregistry.googleapis.com` |
| List enabled APIs                 | `gcloud services list --enabled`                        |

### Best Practices (2025–2026 era)

- 始终使用最新的 gcloud 版本 (`gcloud components update`)。
- 优先使用 **impersonation**，而不是长期有效的 service account keys。
- 在脚本中显式使用 **--project**、**--region**、**--zone** 参数，而不是依赖本地 config。
- 为自动化任务使用 **--quiet** + **--format**。
- 对于新工作负载，优先为 Cloud Functions 使用 **--gen2**，并优先选择 **Cloud Run**。
- 仅在需要时学习 `gcloud alpha` / `gcloud beta`（预览版特性变化很快）。

### Quick Start (2025)

```bash
# macOS / Linux (推荐方法)
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init

# 或通过包管理器
brew install --cask google-cloud-sdk          # macOS
winget install Google.CloudSDK                # Windows
sudo snap install google-cloud-cli --classic  # Ubuntu
```

在 2026 年，gcloud CLI 仍然是与 Google Cloud 交互的最强大且使用最广泛的方式之一（与 **terraform**、**pulumi** 和 **Google Cloud Console** 并列）。

References:  

- [gcloud CLI overview](https://docs.cloud.google.com/sdk/gcloud)
- [Google Cloud CLI main page](https://cloud.google.com/cli)
- [Google Cloud SDK installation](https://docs.cloud.google.com/sdk/docs/install-sdk)
- [gcloud CLI cheat sheet](https://docs.cloud.google.com/sdk/docs/cheatsheet)