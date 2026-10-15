---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Docker在GCP上的直播推流架构
translated: true
type: note
---

本项目是一个基于 Docker 的技術栈（PHP-FPM + nginx + MySQL 5.7 + Redis，外加 SRS 用于 RTMP 推流）。在 Google Cloud 上，你有三个比较现实的选择：

## 方案 1：Compute Engine 虚拟机 + Docker Compose（推荐，最简单）

这种方式与你的 `docker-compose.yml` 完全一致，并且支持 RTMP 推流（Cloud Run/Knative 无法处理 TCP 1935 端口）。

```bash
# 1. 在你的项目中创建一台虚拟机（例如 e2-standard-4，Ubuntu 22.04）
gcloud compute instances create live-server \
  --project=YOUR_PROJECT_ID \
  --zone=asia-east1 \
  --machine-type=e2-standard-4 \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=50GB \
  --tags=live-server

# 2. 开放防火墙端口（HTTP、HTTPS、RTMP、SRS HTTP-FLV）
gcloud compute firewall-rules create allow-live \
  --allow=tcp:80,tcp:443,tcp:1935,tcp:8080,udp:8000 \
  --target-tags=live-server

# 3. SSH 登录并部署
gcloud compute ssh live-server --zone=asia-east1
```

然后在虚拟机上：

```bash
sudo apt-get update && sudo apt-get install -y docker.io docker-compose-plugin git
sudo usermod -aG docker $USER && newgrp docker

git clone https://github.com/lzwjava/live-server.git
cd live-server

cp .env.example .env
# 编辑 .env：微信密钥、七牛密钥、Supabase 密钥、数据库凭据

# 在 docker-compose.yml 中设置生产环境变量和真实数据库密码
docker compose up -d --build
```

将你的域名解析到虚拟机的公网 IP（或者在前方配置 Cloud Load Balancing）。

## 方案 2：Cloud Run + Cloud SQL（无服务器，仅支持 HTTP）

适合 API/Web 部分，但**不能用于 SRS/RTMP 推流**——你需要将 SRS 部署在其他地方（一台小型 GCE 虚拟机或使用推流服务）。

1. **创建 Cloud SQL（MySQL 5.7 或 8.0）：**
   ```bash
   gcloud sql instances create live-mysql \
     --database-version=MYSQL_5_7 \
     --tier=db-f1-micro \
     --region=asia-east1 \
     --root-password=YOUR_PASSWORD
   gcloud sql databases create qulive --instance=live-mysql
   gcloud sql import sql live-mysql gs://YOUR_BUCKET/db-dump.sql
   ```
2. **为 Cloud Run 调整镜像：** 你当前的 Dockerfile 在 9000 端口运行 `php-fpm`，但 Cloud Run 需要在 `$PORT` 上运行单一的 HTTP 服务器。修改 CMD，让 nginx 和 php-fpm 一起运行（例如通过 supervisord 启动 `nginx -g 'daemon off;'` 和 php-fpm，并将 `fastcgi_pass` 指向 `127.0.0.1:9000` 而不是 `app:9000`）。
3. **部署：**
   ```bash
   gcloud run deploy live-server \
     --image gcr.io/YOUR_PROJECT_ID/live-server \
     --region=asia-east1 \
     --allow-unauthenticated \
     --add-cloudsql-instances=YOUR_PROJECT_ID:asia-east1:live-mysql \
     --set-env-vars="CI_ENVIRONMENT=production,DB_HOST=/cloudsql/... connection name,DB_NAME=qulive,DB_USER=root,DB_PASS=..."
   ```
4. **Redis：** 使用 Memorystore（需要为 Cloud Run 配置 VPC connector）或使用兼容 Redis 的服务。

## 方案 3：GKE（Kubernetes）

只有当你预期需要大规模扩展时，才值得考虑。你需要为应用 + nginx + SRS 编写 Deployment/Service，使用 StatefulSet 或 Cloud SQL 作为 MySQL，使用 Memorystore 作为 Redis。对于单服务器应用来说，这会带来显著的额外复杂度。

## 实用说明

- **推流：** SRS 需要 1935 端口（RTMP）、8080 端口（HTTP-FLV），可能还需要 UDP 8000 端口（WebRTC）——只有方案 1（或带 LoadBalancer 的 GKE）能干净利落地处理这些。将 `.env` 中的 `RTMP_URL_PREFIX` 更新为你虚拟机的域名或 IP。
- **微信回调**（支付通知、OAuth）需要一个公网 HTTPS 端点——在虚拟机前面配置 Cloud CDN/Letsencrypt（例如 certbot 或 Caddy）。
- **密钥：** 不要提交真实密钥；使用 GCE 的 Secret Manager 或 `gcloud secrets` 来挂载或注入，因为 `.env.example` 中目前包含看起来像真实凭据的内容。
- **MySQL 5.7 已停止维护（EOL）** ——考虑迁移到 MySQL 8.0 或 Cloud SQL 支持的版本。
- **存储：** 录制文件和视频目前使用本地路径（`/home/videos/`）和七牛；在 GCP 上，你很可能需要将七牛替换为 Google Cloud Storage，并为虚拟机的媒体目录使用持久化磁盘。

**总结：** 要实现最快且可用的部署，请使用**方案 1**（一台 GCE 虚拟机，`docker compose up -d`，开放 80/443/1935/8080 端口）。等将来将推流与 API 分离后，再迁移到 Cloud Run + Cloud SQL。