---
audio: false
generated: true
image: false
lang: en
layout: post
title: GitHub Webhooks Setup Guide
translated: false
type: note
---

**Question:** How to use webhooks for a GitHub repository?

**Answer:**

GitHub **webhooks** allow your external server, service, or application to receive real-time HTTP POST requests whenever specific events happen in your repository (push, pull request created, issue opened, etc.).

Here is the standard way to set up a repository webhook using the GitHub web interface (most common method):

### Step-by-step guide to create a repository webhook

1. Go to your repository on GitHub
   Open https://github.com and navigate to the repository you want to add a webhook to.

2. Open Settings
   Click **Settings** (you need to be owner or have admin permissions on the repo).

3. Go to Webhooks section
   In the left sidebar, click **Webhooks** → then click **Add webhook** (or **Create webhook**).

4. Fill in the webhook configuration

   - **Payload URL**
     The most important field. Enter the HTTPS URL of your server/endpoint that will receive the webhook events.
     Example: `https://your-app.com/webhook/github` or `https://hooks.zapier.com/hooks/catch/123456/abcde/`

   - **Content type**
     Choose:
     - `application/json` (most common and recommended)
     - or `application/x-www-form-urlencoded`

   - **Secret** (strongly recommended)
     Enter a random, secure string (at least 30+ characters).
     GitHub will use this to create an HMAC signature that you can verify on your server to make sure the request really came from GitHub.
     Generate one easily: `openssl rand -hex 20` or use an online secure random generator.

   - **SSL verification**
     Keep it enabled (default) unless you're testing with a self-signed certificate (not recommended for production).

   - **Which events would you like to trigger this webhook?**
     - Select **Let me select individual events** (recommended)
     - Choose the events you care about, for example:
       - Pushes (code is pushed)
       - Pull requests (opened, closed, merged, etc.)
       - Issues (opened, edited, closed)
       - Releases
       - Commits comments
       - … (see full list in GitHub docs)

     Or simply choose **Send me everything** for testing (not recommended long-term — creates unnecessary traffic).

5. Click **Add webhook** at the bottom.

6. Test it (optional but recommended)
   After creation, GitHub shows a **Recent Deliveries** section.
   Click **Edit** → **Redeliver** on any event, or trigger a real event (git push, open PR, etc.) and check if your server received it.

### What your server needs to do

Your endpoint must:

- Accept **POST** requests
- Return HTTP **2xx** status quickly (GitHub retries failed deliveries)
- (Recommended) Verify the signature using the secret:

```python
# Python example (Flask + hmac)
import hmac
import hashlib

def verify_signature(payload, secret, signature):
    expected = "sha256=" + hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

GitHub sends header: `X-Hub-Signature-256: sha256=abc123...`

### Common use cases

- Continuous deployment (push → deploy to server/Vercel/Netlify)
- Notify Discord/Slack/Teams on push/PR
- Auto-label issues or run CI checks
- Sync repo events to external database
- Trigger Jenkins/GitLab CI

### Important security & best practices

- Always use **HTTPS** for Payload URL
- Always set a **secret** and verify signatures
- Return 2xx fast — don't do heavy work in the webhook handler (queue it)
- Use **individual events** instead of "everything"
- Monitor **Recent Deliveries** for failed requests

For full details and all possible events → see the official documentation.

**References:**

- [Creating webhooks - GitHub Docs](https://docs.github.com/en/webhooks/using-webhooks/creating-webhooks)
- [About webhooks - GitHub Docs](https://docs.github.com/en/webhooks/about-webhooks)
- [Webhook events and payloads - GitHub Docs](https://docs.github.com/en/webhooks/webhook-events-and-payloads)
- [Best practices for using webhooks - GitHub Docs](https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks)
