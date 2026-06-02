---
audio: false
generated: true
image: false
lang: en
layout: post
title: Debug Gcloud Run Deploy Hangs
translated: false
type: note
---

Question: The gcloud run deploy command is stuck / hanging, does gcloud have a verbose option?

Answer:

Yes, **gcloud** supports a `--verbosity` flag to get more detailed output, which is very useful for debugging when a deployment hangs or takes unusually long.

### How to add verbosity

Run your command with one of these (higher = more output):

```bash
gcloud run deploy blog-server \
  --source . \
  --region asia-northeast1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --verbosity=debug
```

Common levels (from most to least verbose):

- `--verbosity=debug`   → shows detailed steps, API calls, retries, etc. (recommended for troubleshooting hangs)
- `--verbosity=info`    → more than default, but cleaner
- `--verbosity=warning` → default-ish
- `--verbosity=error`   → minimal

You can also set it globally (affects all gcloud commands):

```bash
gcloud config set core/verbosity debug
```

(Reset later with `gcloud config set core/verbosity warning` or just omit `--verbosity`.)

### Why it might be stuck / hanging on `--source .`

The `--source .` flag triggers:

1. Source upload to Cloud Build
2. Automatic container build (using your `Dockerfile` or Cloud Buildpacks if no Dockerfile)
3. Deploy to Cloud Run

Common reasons for long hangs (especially "Uploading sources..." or "Building and deploying..."):

- **Large project / many files** — Maven downloads dependencies during build, large `target/` folder, git history, node_modules, etc. → upload takes forever.
  - **Fix idea**: Add a `.gcloudignore` file (like `.gitignore`) to exclude unnecessary files/folders (e.g. `target/`, `.git/`, `node_modules/`, `logs/`). Example minimal `.gcloudignore`:

    ```
    .git
    target/
    *.log
    node_modules/
    .mvn/
    ```

- **Slow internet / large upload** — Especially if you're on a slow connection or VPN.
- **Build is slow** — If using Maven, it might be resolving dependencies, compiling, tests, etc. (even if you have `Dockerfile`, Cloud Build still runs it).
- **Known occasional Cloud Build / Cloud Run backend delays** — Sometimes it hangs 10–30+ minutes then fails with "deadline exceeded" or succeeds late.
- **Permissions / quota issues** — Missing roles for Cloud Build or Artifact Registry.

### Quick workarounds / faster alternatives

1. **Build & push image manually** (avoids source upload slowness):

   ```bash
   docker build -t gcr.io/$(gcloud config get-value project)/blog-server:latest .
   docker push gcr.io/$(gcloud config get-value project)/blog-server:latest

   gcloud run deploy blog-server \
     --image gcr.io/$(gcloud config get-value project)/blog-server:latest \
     --region asia-northeast1 \
     --allow-unauthenticated \
     --port 8080 \
     --memory 1Gi
   ```

   This is usually much faster for repeated deploys.

2. **Use Artifact Registry** instead of gcr.io (modern recommendation):
   Create repo: `gcloud artifacts repositories create my-repo --repository-format=docker --location=asia-northeast1`
   Then tag/push: `asia-northeast1-docker.pkg.dev/YOUR-PROJECT/my-repo/blog-server:latest`

3. **Check Cloud Build logs** (even if CLI hangs):
   - Go to <https://console.cloud.google.com/cloud-build/builds>
   - Find the latest build triggered by your deploy → see detailed steps / errors.

4. **Add `--async`** to make CLI return immediately:

   ```bash
   gcloud run deploy ... --async
   ```

   Then monitor in console or with `gcloud run services describe blog-server --region asia-northeast1`

Run with `--verbosity=debug` first — it will show exactly where it's spending time (e.g., uploading X MB, waiting for build step Y). If it still hangs forever (>20–30 min), cancel (Ctrl+C), clean up unnecessary files with `.gcloudignore`, or switch to manual image push.

References:

- [gcloud CLI overview – verbosity flag](https://docs.cloud.google.com/sdk/gcloud)
- [Deploy services from source code | Cloud Run](https://docs.cloud.google.com/run/docs/deploying-source-code)
- [gcloud run deploy reference](https://docs.cloud.google.com/sdk/gcloud/reference/run/deploy)
- [Troubleshoot Cloud Run issues](https://docs.cloud.google.com/run/docs/troubleshooting)
