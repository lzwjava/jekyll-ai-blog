---
audio: false
generated: true
image: false
lang: en
layout: post
title: Debug Cloud Run Build Failures
translated: false
type: note
---

Question: The gcloud run deploy command failed with "Build failed; check build logs for details" and a traceback – how to find and fix the issue?

Answer: 

Your deployment failed during the **Cloud Build** phase (triggered automatically by `--source .`), which handles building the container image from your source code and `Dockerfile`.

The key message is: **"Build failed; check build logs for details"** — this means the actual error (e.g. Maven compile failure, missing dependency, wrong Dockerfile instruction, permission issue, or timeout) is in the **Cloud Build logs**, not in the short gcloud output.

### Step 1: Find the Build Logs (Quickest Ways)

1. **In the Google Cloud Console (easiest – recommended first)**:
   - Go to: https://console.cloud.google.com/cloud-build/builds?project=YOUR-PROJECT-ID
   - Look at the **Build history** list (sort by most recent).
   - Find the latest build for your service (`blog-server`); it usually shows as "FAILED" or has a red status.
   - Click on it → you'll see detailed step-by-step logs.
   - Scroll through steps (especially the Maven/build step or Dockerfile execution) to find red error lines (e.g. "Compilation failure", "Could not resolve dependencies", "COPY failed", etc.).
   - The console often shows a direct link like:  
     "Logs are available at https://console.cloud.google.com/cloud-build/builds/abc123-xyz?project=..."  
     (gcloud sometimes prints this before failing – check your terminal scrollback).

2. **Using gcloud CLI**:
   - List recent builds to get the BUILD_ID (the most recent failed one):
     ```bash
     gcloud builds list --limit=5 --filter="status=FAILURE"
     ```
     - Look for the ID (long hex string like `abcdef12-3456-...`) and trigger/source info matching your deploy.

   - View full logs for that build:
     ```bash
     gcloud builds log BUILD_ID_HERE
     ```
     - Add `--stream` if you want real-time (but since it's failed, normal is fine).
     - Or pipe to less/grep:  
       ```bash
       gcloud builds log BUILD_ID_HERE | less
       gcloud builds log BUILD_ID_HERE | grep -i error
       ```

### Step 2: Common Causes & Fixes for Java/Spring Boot + Dockerfile Projects

Once you see the logs, match against these frequent issues:

- **Maven build errors** (most common):
  - Dependency resolution failed → Check internet/proxy in build, or add Maven settings.xml if needed.
  - Tests failing → Skip tests in Dockerfile: add `mvn clean package -DskipTests`.
  - Out of memory → Increase build resources or add `--set-build-env-vars MAVEN_OPTS="-Xmx2g"`.

- **Dockerfile problems**:
  - Wrong base image (use `openjdk:17-jdk-slim` or `eclipse-temurin:17` for modern Java).
  - App not exposing/listening on `$PORT` (Cloud Run sets PORT=8080; your app must bind to `0.0.0.0:$PORT`).
  - CMD/ENTRYPOINT wrong → Ensure it runs the JAR correctly, e.g.:
    ```dockerfile
    CMD ["java", "-jar", "/app.jar", "--server.port=${PORT:-8080}"]
    ```
  - Multi-stage build failed in copy steps.

- **Permission/Quota Issues**:
  - Cloud Build service account missing roles → Ensure `PROJECT_NUMBER@cloudbuild.gserviceaccount.com` has `roles/run.builder` and `roles/artifactregistry.writer` (if using Artifact Registry).
  - Run: `gcloud projects add-iam-policy-binding YOUR-PROJECT-ID --member=serviceAccount:YOUR_PROJECT_NUMBER@cloudbuild.gserviceaccount.com --role=roles/run.builder`

- **Large upload / timeout**:
  - Add `.gcloudignore` to exclude `target/`, `.git/`, etc. (as mentioned earlier).

- **Buildpack fallback** (if no Dockerfile or misdetected):
  - Sometimes it uses buildpacks instead → force Dockerfile detection or specify builder.

### Step 3: Recommended Next Action (Faster & More Reliable)

Since source deploy is failing, switch to **manual build + deploy** (you control the build locally):

1. Build & test locally:
   ```bash
   docker build -t blog-server:test .
   docker run -p 8080:8080 -e PORT=8080 blog-server:test
   ```
   → Fix any errors here first.

2. Tag & push:
   ```bash
   IMAGE="asia-southeast1-docker.pkg.dev/YOUR-PROJECT-ID/my-repo/blog-server:latest"
   docker build -t $IMAGE .
   gcloud auth configure-docker asia-southeast1-docker.pkg.dev
   docker push $IMAGE
   ```

3. Deploy image directly:
   ```bash
   gcloud run deploy blog-server \
     --image $IMAGE \
     --region asia-southeast1 \
     --allow-unauthenticated \
     --port 8080 \
     --memory 1Gi
   ```

This skips the remote source upload/build entirely.

After checking logs, reply here with the **specific error message** from the build logs (e.g. the red part) — I can help pinpoint the exact fix.

References:  

- [Troubleshoot Cloud Run issues](https://cloud.google.com/run/docs/troubleshooting)
- [Troubleshooting build errors - Cloud Build](https://cloud.google.com/build/docs/troubleshooting)
- [Store and view build logs - Cloud Build](https://cloud.google.com/build/docs/securing-builds/store-manage-build-logs)
- [gcloud builds log reference](https://cloud.google.com/sdk/gcloud/reference/builds/log)
- [Deploy from source code - Cloud Run](https://cloud.google.com/run/docs/deploying-source-code)