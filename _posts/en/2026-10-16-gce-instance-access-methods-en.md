---
audio: false
generated: true
image: false
lang: en
layout: post
title: GCE Instance Access Methods
translated: false
type: note
---

There are several ways to access a Google Cloud (GCE) instance:

## 1. SSH via gcloud CLI (most common)

```bash
# SSH into a Linux instance by name
gcloud compute ssh INSTANCE_NAME --zone ZONE

# e.g.
gcloud compute ssh my-web-server --zone us-central1-a
```

On Windows, this uses your SSH keys; on first connect, OS Login or metadata SSH keys handle authentication automatically.

## 2. SSH from the Cloud Console (browser)

1. Go to **Compute Engine → VM instances** in the [console](https://console.cloud.google.com/compute/instances)
2. Click **SSH** next to your instance — opens a terminal in the browser
3. Useful when you don't have the gcloud CLI installed locally

## 3. Using your own SSH client

```bash
# Get the external IP first
gcloud compute instances describe INSTANCE_NAME --zone ZONE --format='get(networkInterfaces[0].accessConfigs[0].natIP)'

# Then connect directly
ssh username@EXTERNAL_IP
```

The username depends on the OS image:
- Debian/Ubuntu → `username` you configured (or your OS Login email)
- CentOS/RHEL → `your_username`
- Container-optimized OS → `username` from instance metadata

## 4. RDP (Windows instances)

```bash
gcloud compute start-iap-tunnel INSTANCE_NAME 3389 --local-host-port=localhost:3389 --zone ZONE
```

Then connect with an RDP client to `localhost:3389`. Or use the console's **Reset password** + browser RDP option.

## Prerequisites checklist

- `gcloud auth login` — authenticated
- `gcloud config set project PROJECT_ID` — correct project
- Firewall allows SSH: rule permitting TCP port **22** (default `default-allow-ssh` rule covers this)
- For IAP-based access (recommended, no external IP needed):
  ```bash
  gcloud compute ssh INSTANCE_NAME --zone ZONE --tunnel-through-iap
  ```

If you tell me your OS type and whether you have `gcloud` installed, I can give you the exact command.