---
audio: false
generated: true
image: false
lang: en
layout: post
title: Google OAuth token expiry and renewal
translated: false
type: note
---

Question: What is the expiry date of the Google OAuth authorization used by `ww gen-video upload`, and can it be extended?

Answer:

From this log:

```
scope=https://www.googleapis.com/auth/youtube
access_type=offline
```

you are using **Google OAuth 2.0 with offline access**.

There are two different expirations:

1. **Access token**

   * Usually expires after about **1 hour**.
   * If your upload succeeded and then you wait half an hour, it is still valid.
   * You normally do **not extend this** manually.

2. **Refresh token**

   * This is what `access_type=offline` gives you.
   * It can live for a long time (often months/years) and is used to obtain new access tokens automatically.
   * It does not have a fixed "30 minutes" expiry.

So if your question is:

> "After half an hour, can I continue uploading?"

Yes. Half an hour is nothing; the access token is likely still valid.

If your question is:

> "Can I make the token last longer than 1 hour?"

No, not for the access token. The correct design is:

```
refresh_token
      |
      v
Google OAuth token endpoint
      |
      v
new access_token (1 hour)
      |
      v
YouTube Data API upload
```

Your CLI should store the refresh token securely and automatically refresh:

```python
creds = Credentials(
    token=access_token,
    refresh_token=refresh_token,
    token_uri="https://oauth2.googleapis.com/token",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    scopes=["https://www.googleapis.com/auth/youtube"],
)

if creds.expired:
    creds.refresh(Request())
```

For a personal CLI tool like `ww`, the normal workflow is:

```
first run:
    browser OAuth login
    save refresh token

future runs:
    no browser
    refresh automatically
    upload video
```

One more thing: if you see the earlier error:

```
Access blocked: ZhiweiTextToSpeech has not completed the Google verification process
```

that is unrelated to token lifetime. That was an **OAuth consent screen / testing user issue**. For a personal YouTube uploader, keep the app in **Testing** mode and add your Google account as a test user, or publish the OAuth app if you need other users to authorize.
