---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing OAuth Testing Mode Error
translated: false
type: note
---

Question: Why does YouTube Data API OAuth show `ZhiweiTextToSpeech has not completed the Google verification process` and `Error 403: access_denied`?

Answer:

This is **not a YouTube Data API problem**. It is a **Google OAuth consent screen configuration problem**.

Your OAuth app (`ZhiweiTextToSpeech`) is currently in **Testing mode**, and the Google account you used (`lzwjava@gmail.com`) is not listed as a test user.

---

## Why this happens

When you create OAuth credentials, Google creates an OAuth application:

```
Google Cloud Project
        |
        |
OAuth Consent Screen
        |
        |
ZhiweiTextToSpeech
        |
        |
YouTube Data API scope:
youtube.upload
```

Because you request sensitive scopes like:

```
https://www.googleapis.com/auth/youtube.upload
```

Google requires OAuth verification **for public apps**.

But for personal/private tools, you usually don't need verification.

You can use **Testing mode**.

---

## Fix: add yourself as Test User

Go to:

[Google Cloud Console](https://console.cloud.google.com/?utm_source=chatgpt.com)

Then:

```
APIs & Services
    |
    OAuth consent screen
    |
    Audience
```

You should see:

```
Publishing status:
Testing
```

Find:

```
Test users
```

Add:

```
lzwjava@gmail.com
```

Save.

Then wait a few minutes.

Retry:

```bash
python upload.py
```

---

## If you already authorized before

Delete cached OAuth token.

Your script probably created:

```
token.json
```

or:

```
token.pickle
```

Remove it:

```bash
rm token.json
rm token.pickle
```

Run again:

```bash
python upload.py
```

Browser login again.

---

## Alternative: make app Internal

Only available if using Google Workspace:

```
OAuth consent screen

User Type:
    Internal
```

Then no verification.

For normal Gmail accounts:

```
External + Testing
```

is correct.

---

## Why Google says "verification"

The confusing part:

> "has not completed the Google verification process"

sounds like you need to submit an app review.

You **do not** need that if:

* only you use it
* only a few testers use it
* it is your own CLI tool

Google allows up to 100 test users in Testing mode.

---

## For your AI video uploader

I would keep it:

```
OAuth Consent Screen:
    External

Publishing status:
    Testing

Test users:
    your Gmail

Scopes:
    youtube.upload
```

Then your agent can use:

```
video_agent
    |
    +-- generate_video()
    |
    +-- generate_thumbnail()
    |
    +-- youtube_upload()
          |
          +-- refresh_token.json
```

No verification needed.

The refresh token will keep working until you revoke access or change the OAuth configuration.
