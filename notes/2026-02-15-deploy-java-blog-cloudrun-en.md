---
audio: false
generated: true
image: false
lang: en
layout: post
title: Deploy Java Blog to Cloud Run
translated: false
type: note
---

Question: How to use a Docker container to deploy the blog-server application in Google Cloud?

Answer:

Here are the most common and recommended ways in 2026 to deploy your **Dockerized Java/Spring Boot** application (from the directory with `Dockerfile` and `pom.xml`) to **Google Cloud**. The easiest and most popular option today is **Cloud Run** (serverless containers).

### Recommended Option: Deploy to Cloud Run (serverless, pay-per-request)

#### Option A – Simplest: Build & deploy automatically from source (recommended for most developers)

You don't even need to build the Docker image locally.

1. Make sure you have the Google Cloud SDK installed and authenticated:

   ```bash
   gcloud auth login
   gcloud config set project YOUR-PROJECT-ID
   ```

2. Enable necessary APIs (run once):

   ```bash
   gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com
   ```

3. From the project root (where `pom.xml` and `Dockerfile` are), run:

   ```bash
   gcloud run deploy blog-server \
     --source . \
     --region asia-northeast1 \          # or us-central1, europe-west1, etc.
     --allow-unauthenticated \          # remove if you want private service
     --port 8080 \                      # change if your app listens on different port
     --memory 1Gi                       # optional – adjust based on needs
   ```

   - Cloud Run automatically detects it's a Maven/Spring Boot project, builds a container using Cloud Build, and deploys it.
   - First deployment takes ~3–5 minutes; later ones are much faster.

#### Option B – Build Docker image yourself and push it

Useful when you want more control or already have CI/CD.

1. Build and tag the image locally:

   ```bash
   docker build -t gcr.io/YOUR-PROJECT-ID/blog-server:latest .
   # or use Artifact Registry (newer & recommended):
   # docker build -t asia-northeast1-docker.pkg.dev/YOUR-PROJECT-ID/my-repo/blog-server:latest .
   ```

2. Push the image:

   ```bash
   gcloud auth configure-docker
   docker push gcr.io/YOUR-PROJECT-ID/blog-server:latest
   # or for Artifact Registry:
   # gcloud auth configure-docker asia-northeast1-docker.pkg.dev
   # docker push asia-northeast1-docker.pkg.dev/YOUR-PROJECT-ID/my-repo/blog-server:latest
   ```

3. Deploy to Cloud Run:

   ```bash
   gcloud run deploy blog-server \
     --image gcr.io/YOUR-PROJECT-ID/blog-server:latest \
     --region asia-northeast1 \
     --allow-unauthenticated \
     --port 8080
   ```

   Or using Artifact Registry image:

   ```bash
   --image asia-northeast1-docker.pkg.dev/YOUR-PROJECT-ID/my-repo/blog-server:latest
   ```

#### Quick checklist before deploying

- Your **Dockerfile** should expose the correct port (usually `EXPOSE 8080`)
- App should listen on `0.0.0.0` (not `localhost`)
- For production add:

  ```bash
  --cpu 1 --memory 512Mi --concurrency 80 --max-instances 10
  ```

- If you use environment variables / secrets:

  ```bash
  --set-env-vars "SPRING_PROFILES_ACTIVE=prod,DATABASE_URL=..."
  ```

#### Other popular Google Cloud options (when Cloud Run is not suitable)

- **Cloud Run jobs** → for batch / one-off tasks
- **Google Kubernetes Engine (GKE)** → when you need advanced networking, stateful apps, or very high customization
- **Compute Engine** → classic VM + Docker (more manual)

Cloud Run is usually the best balance of price, simplicity, and scaling for a blog server.

After deployment you will get a URL like:

<https://blog-server-abc123-uc.a.run.app>

Good luck!

References:

- [Deploying container images to Cloud Run](https://docs.cloud.google.com/run/docs/deploying)
- [Quickstart: Build and deploy a Java Spring Boot web app to Cloud Run](https://docs.cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-java-service)
- [Deploy services from source code | Cloud Run](https://docs.cloud.google.com/run/docs/deploying-source-code)
