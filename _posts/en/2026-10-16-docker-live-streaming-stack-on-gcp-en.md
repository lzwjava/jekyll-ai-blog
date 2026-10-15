---
audio: false
generated: true
image: false
lang: en
layout: post
title: Docker Live Streaming Stack on GCP
translated: false
type: note
---

This project is a Docker-based stack (PHP-FPM + nginx + MySQL 5.7 + Redis, plus SRS for RTMP streaming). On Google Cloud you have three realistic options:

## Option 1: Compute Engine VM + Docker Compose (recommended, simplest)

This mirrors your `docker-compose.yml` exactly and supports RTMP streaming (Cloud Run/Knative can't do TCP 1935).

```bash
# 1. Create a VM (e.g. e2-standard-4, Ubuntu 22.04) in your project
gcloud compute instances create live-server \
  --project=YOUR_PROJECT_ID \
  --zone=asia-east1 \
  --machine-type=e2-standard-4 \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=50GB \
  --tags=live-server

# 2. Open firewall ports (HTTP, HTTPS, RTMP, SRS HTTP-FLV)
gcloud compute firewall-rules create allow-live \
  --allow=tcp:80,tcp:443,tcp:1935,tcp:8080,udp:8000 \
  --target-tags=live-server

# 3. SSH in and deploy
gcloud compute ssh live-server --zone=asia-east1
```

Then on the VM:

```bash
sudo apt-get update && sudo apt-get install -y docker.io docker-compose-plugin git
sudo usermod -aG docker $USER && newgrp docker

git clone https://github.com/lzwjava/live-server.git
cd live-server

cp .env.example .env
# Edit .env: WeChat keys, Qiniu keys, Supabase keys, DB creds

# Set production env + real DB password in docker-compose.yml
docker compose up -d --build
```

Point your domain at the VM's external IP (or put Cloud Load Balancing in front).

## Option 2: Cloud Run + Cloud SQL (serverless, HTTP only)

Good for the API/web part, but **won't work for SRS/RTMP streaming** — you'd need to run SRS elsewhere (a small GCE VM or a streaming service).

1. **Create Cloud SQL (MySQL 5.7 or 8.0):**

   ```bash
   gcloud sql instances create live-mysql \
     --database-version=MYSQL_5_7 \
     --tier=db-f1-micro \
     --region=asia-east1 \
     --root-password=YOUR_PASSWORD
   gcloud sql databases create qulive --instance=live-mysql
   gcloud sql import sql live-mysql gs://YOUR_BUCKET/db-dump.sql
   ```

2. **Adjust the image for Cloud Run:** your current Dockerfile runs `php-fpm` on port 9000, but Cloud Run needs a single HTTP server on `$PORT`. Change the CMD to run nginx + php-fpm together (e.g. use `nginx -g 'daemon off;'` with php-fpm started via supervisord, and point `fastcgi_pass` to `127.0.0.1:9000` instead of `app:9000`).
3. **Deploy:**

   ```bash
   gcloud run deploy live-server \
     --image gcr.io/YOUR_PROJECT_ID/live-server \
     --region=asia-east1 \
     --allow-unauthenticated \
     --add-cloudsql-instances=YOUR_PROJECT_ID:asia-east1:live-mysql \
     --set-env-vars="CI_ENVIRONMENT=production,DB_HOST=/cloudsql/... connection name,DB_NAME=qulive,DB_USER=root,DB_PASS=..."
   ```

4. **Redis:** use Memorystore (needs VPC connector with Cloud Run) or a Redis-compatible service.

## Option 3: GKE (Kubernetes)

Only worth it if you expect to scale heavily. You'd write Deployments/Services for app + nginx + SRS, use StatefulSets or Cloud SQL for MySQL, and Memorystore for Redis. Significant extra complexity for a single-server app.

## Practical notes

- **Streaming:** SRS needs port 1935 (RTMP), 8080 (HTTP-FLV), and possibly UDP 8000 (WebRTC) — only Option 1 (or GKE with a LoadBalancer) handles this cleanly. Update `RTMP_URL_PREFIX` in `.env` to your VM's domain/IP.
- **WeChat callbacks** (pay notify, OAuth) require a public HTTPS endpoint — put Cloud CDN/Letsencrypt (e.g. certbot or Caddy) in front of the VM.
- **Secrets:** don't commit real keys; use GCE's Secret Manager or `gcloud secrets` and mount/inject them, since `.env.example` currently contains real-looking credentials.
- **MySQL 5.7 is EOL** — consider migrating to MySQL 8.0 or Cloud SQL's supported version.
- **Storage:** recordings/videos currently use local paths (`/home/videos/`) and Qiniu; on GCP you'd likely swap Qiniu for Google Cloud Storage, and use a persistent disk for the VM's media dirs.

**TL;DR:** For quickest working deployment, use **Option 1** (one GCE VM, `docker compose up -d`, open ports 80/443/1935/8080). Move to Cloud Run + Cloud SQL later once you separate streaming from the API.
