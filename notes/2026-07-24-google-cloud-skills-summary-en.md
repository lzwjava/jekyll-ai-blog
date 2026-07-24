---
audio: false
generated: true
image: false
lang: en
layout: post
title: Google Cloud Skills Summary
translated: false
type: note
---

Based on all the notes I've read, here's a comprehensive summary of your Google Cloud knowledge:

---

## ☁️ Google Cloud — What You Know & Have Used

### 🛠️ Actually Built & Deployed (Hands-on)

| Module/Feature | How You Used It |
|---|---|
| **Speech-to-Text v2 API** | Built into your `ww` CLI tool — `ww gcp-speech transcribe <audio>` — uploads audio to GCS, runs Chirp/long/short models, saves transcripts as `.md`. You know Chirp, Chirp_2, Chirp_3, long, short models in detail. |
| **Cloud Storage (GCS)** | The `test2x` bucket for audio uploads. GCS lifecycle rules (delete old files, move to Nearline/Coldline/Archive). `gsutil` CLI. |
| **Cloud Run** | Deployed a Java/Spring Boot `blog-server` container. You know `gcloud run deploy --source .`, Artifact Registry, Cloud Build, `.gcloudignore`, `--verbosity=debug` for debugging hangs. Deployed to `asia-northeast1` region. |
| **YouTube Data API v3** | Built `ww gen-video upload` — OAuth 2.0 desktop flow, video upload with resumable MediaFileUpload. Stored `client_secret.json` at `~/.google/`. |
| **OAuth 2.0** | Fixed redirect_uri issues, ran `flow.run_local_server(port=8080)`, handled token caching at `~/.google/youtube_token.json`. |
| **Compute Engine** | Created E2 micro VM in Taipei (`asia-east1`) as a VPN server (around $13/month). Knows shared-core, preemptible/spot VMs, custom machine types. |
| **gcloud CLI** | Updated from 507.0.0 → 532.0.0. Uses `gcloud auth login`, `gcloud config set project`, `gcloud services enable`, `gcloud components update`. |
| **Google AdSense** | Added to your Jekyll blog — `ads.txt`, Auto Ads script, manual in-article ad units. Applied for approval, dealt with rejection/fixes. Understands ad revenue dynamics. |

### 📚 Studied & Know Deeply (Exam/Cert Level)

| Module | What You Know |
|---|---|
| **BigQuery** | Serverless columnar warehouse. Dremel/Colossus/Borg architecture. Partitioning & clustering for cost optimization. `bq` CLI, Python client (`google.cloud.bigquery`), `--dry_run`. BigQuery ML, vector search, JSON embeddings storage for RAG. |
| **IAM & Security** | Identity-Aware Proxy (IAP) — Zero Trust, context-aware access. `roles/compute.instanceAdmin` vs `roles/editor` vs `roles/owner`. Service accounts vs user accounts. |
| **GKE (Kubernetes Engine)** | Knows GKE cluster creation, HPA/VPA scaling, Nginx Ingress, secure access patterns. |
| **Cloud SQL / Spanner / Firestore** | Spanner — globally distributed, strong consistency, ACID. Firestore — NoSQL document DB, real-time sync, offline support, security rules. Cloud SQL — traditional relational. |
| **Vertex AI** | Imagen 4 image generation on Vertex AI, safety filters, `google-gen-ai-image-config`. Google AI Studio vs Vertex AI metrics. |
| **Cloud Load Balancing** | Introduction to GCP Cloud Load Balancing, Cloud NAT, Cloud Armor (WAF). |
| **Networking** | Cloud NAT vs home router, multi-region design, VPC, private service connect. |
| **Certifications** | Studied GCP ACE (Associate Cloud Engineer), Professional Cloud Developer, Cloud Digital Leader, Professional ML Engineer. Did practice questions. |

### 💰 Pricing & Cost Knowledge

| Topic | Details |
|---|---|
| **Compute Engine pricing** | E2 micro = $0.0084/hr in Taipei. Sustained use discounts, committed use discounts (30-70% off). Spot VMs (60-91% off). |
| **Network egress** | $0.12/GiB from Asia (first 1TB). Ingress is free. |
| **GCS storage classes** | Standard → Nearline → Coldline → Archive. Lifecycle rules. |
| **BigQuery pricing** | $6.25/TB scanned (on-demand). Partitioning/clustering to reduce. |
| **GPU costs** | 8× H100 on GCP = ~$57k/month. GCP GPU quota denials experienced. |
| **Cloud Run** | Free tier: 2M requests/month. Pay-per-request. |

### ⚡ Summary of Your GCP Profile

You're not just studying theory — you've **built real integrations**:
- **`ww gcp-speech transcribe`** — speech-to-text pipeline with GCS + Chirp models
- **`ww gen-video upload`** — YouTube Data API with OAuth
- **AdSense monetization** on your Jekyll blog
- **Cloud Run deployment** of a Java backend
- **Compute Engine VPN** in Taipei

You know the **developer/platform** side of GCP well (Cloud Run, GCS, Speech API, YouTube API, gcloud CLI, BigQuery), plus **certification-level knowledge** across many services. Your weakest areas (based on note volume) seem to be **GKE** (more theory than hands-on) and **Vertex AI** (studied Imagen but less hands-on), while your strongest is **GCP Speech-to-Text** + **Cloud Run** + **GCS** + **OAuth/YouTube integration**.
