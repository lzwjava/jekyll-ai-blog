---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Rebuilding Fun Live on Google Cloud
translated: false
type: note
---

Question: If rebuilding Fun Live today using Google Cloud technologies, how should we architect it?

Answer:

To rebuild Fun Live—a knowledge-sharing live broadcast platform with real-time lectures (programming, design, etc.), paid sessions, lecturer rewards, real-time participation, playback (VOD), WeChat-like notifications, and WeChat Mini Program integration—using **Google Cloud** in 2025–2026, adopt a modern, scalable, serverless-first or managed-services-heavy architecture. This reduces operational burden compared to the original self-managed PHP/CodeIgniter + SRS + Alibaba Cloud stack.

### Core Principles for the New Architecture

- **Serverless & managed services** wherever possible → minimize DevOps work
- **Global low-latency delivery** for live + VOD
- **Scalability** to handle spikes (popular lectures)
- **Security & monetization** built-in (payments, access control)
- **Microservices** or modular monolith, but lean toward independent services
- Keep OBS compatibility for lecturers (most still use it)

### Recommended High-Level Architecture

1. **Frontend / Clients**
   - **Web app**: React / Next.js (or Vue 3 if you prefer continuity), hosted on **Cloudflare Pages** or **Firebase Hosting** + **Cloud Run** for SSR/edge needs
   - **WeChat Mini Program**: Still use WeChat SDK → call your backend APIs
   - **Mobile apps** (if expanded): Flutter or React Native, with Firebase SDKs

2. **Ingestion (Lecturer → Server)**
   - Lecturers push RTMP using **OBS** (unchanged — very common in 2025)
   - Ingest endpoint: **Live Stream API** (Cloud Live Stream) — Google's managed service that accepts RTMP/RTMPS, transcodes, and segments into HLS/DASH
   - Alternative (if you need more control): Cloud Run + own media server (e.g. Ant Media, OvenMediaEngine, or nginx-rtmp), but prefer managed

3. **Live Streaming Distribution**
   - Use **Media CDN** (Google's media-optimized CDN) for ultra-low latency delivery
     - Supports low-latency HLS (LL-HLS), WebRTC (via integration), CMAF
     - Edge caching, global anycast
   - Origin: Live Stream API output → Media CDN
   - Fallback/backup: Cloud Storage buckets for HLS segments

4. **Playback / VOD**
   - After live ends, Live Stream API archives to **Cloud Storage**
   - Transcode (if needed for adaptive bitrate) using **Transcoder API**
   - Serve VOD via **Media CDN** (same as live) or directly from Storage + signed URLs
   - Metadata (title, lecturer, duration, thumbnail) stored in **Firestore** or **Cloud SQL**

5. **Backend / Business Logic**
   - **Primary option (recommended)**: **Cloud Run** (containerized services) or **Cloud Functions (2nd gen)** for APIs
     - Node.js / Go / Python (faster cold starts than PHP)
     - Handle: user auth, payments, lecture scheduling, rewards, chat, Q&A
   - **Database**:
     - **Firestore** (NoSQL) for users, lectures, payments, real-time chat (real-time listeners great for live Q&A)
     - **Cloud SQL** (PostgreSQL) if you need strong relational consistency (e.g., financial transactions)
   - **Caching**: **Memorystore for Redis** (managed Redis)
   - **Authentication**: **Firebase Authentication** (easy social/WeChat login, phone, email)
   - **Payments & Rewards**: Integrate Stripe, WeChat Pay, or Alipay via Cloud Functions/Run (handle webhooks securely)

6. **Real-time Features (Chat, Q&A, Rewards during live)**
   - **Firestore** real-time listeners (sub-millisecond sync for chat)
   - Alternative: **Pub/Sub** + **Cloud Run** for higher scale, or **Firebase Realtime Database**
   - If very high concurrency: add **Memorystore**

7. **Notifications**
   - **Firebase Cloud Messaging (FCM)** → best for web push, Android, iOS
   - WeChat notifications: use WeChat Official Account / Mini Program template messages via their API (call from Cloud Functions)

8. **Infrastructure & DevOps**
   - **IaC**: Terraform or Google Cloud Deployment Manager
   - **Monitoring**: Cloud Monitoring + Cloud Logging + **Firebase Crashlytics** (if mobile)
   - **CI/CD**: Cloud Build
   - **Secret management**: **Secret Manager**
   - **Global scaling**: Use multi-region setups for Firestore, multi-region buckets

### Suggested Tech Stack Summary (Google Cloud focused)

| Layer              | Original (2016–2019)              | Modern Google Cloud Recommendation                  |
|--------------------|-----------------------------------|-----------------------------------------------------|
| Frontend           | Vue + HTML                        | React/Next.js or Vue 3 + Firebase Hosting           |
| Server             | PHP + CodeIgniter                 | Node.js/Go/Python on Cloud Run                     |
| Database           | MySQL + Redis                     | Firestore + Memorystore for Redis                   |
| Live Ingest        | SRS                               | Live Stream API (accepts RTMP from OBS)             |
| Streaming Delivery | SRS + Nginx                       | Media CDN + HLS/LL-HLS                              |
| VOD Storage        | Alibaba Cloud                     | Cloud Storage + Transcoder API                      |
| Notifications      | WeChat integration                | FCM + WeChat API calls                              |
| Auth               | Custom?                           | Firebase Authentication                             |
| Hosting/Compute    | Linux + Nginx                     | Cloud Run / Firebase                                |
| Design tool        | Sketch                            | Figma (modern replacement)                          |

### Migration / Rebuild Tips

- Start with MVP: Live Stream API + Media CDN + Firestore + Cloud Run APIs
- Keep OBS → RTMP unchanged for lecturer ease
- Open-source again on GitHub — consider monorepo or separate frontend/backend repos
- Estimate cost: Low traffic = very cheap (serverless); high traffic = Media CDN + egress dominate
- Latency target: Use Media CDN edge locations near China (Hong Kong/Singapore) if audience is mainly Chinese

This architecture would be far more scalable, lower maintenance, and globally distributed than the 2016–2019 version, while preserving the core experience.

References:

- [Google Cloud Live Stream API Best Practices](https://docs.cloud.google.com/livestream/docs/best-practices)
- [Media CDN for low-latency live streaming](https://discuss.google.dev/t/architecting-low-latency-live-streaming-a-developers-guide-to-media-cdn/296436)
- [Live Streaming with Media CDN and Live Stream API codelab](https://codelabs.developers.google.com/mediacdn-ls-codelab)
- [Google Cloud Video Streaming overview](https://www.vdocipher.com/blog/google-cloud-video-streaming)
