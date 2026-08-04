---
audio: false
generated: true
image: false
lang: en
layout: post
title: WechatRealFriends QR Login Broken
translated: false
type: note
---

Question: Why does `WechatRealFriends` QR login fail with “need iPad to confirm login”? Does this project no longer work?

Answer:

Yes, your observation is basically correct: **for most normal WeChat accounts today, this type of project is effectively broken or unreliable**.

`WechatRealFriends` is based on automating WeChat Web login. The original flow was:

```
Browser/Web API
      |
      | generate QR code
      v
User scans QR with WeChat phone
      |
      v
WeChat confirms login
      |
      v
Web session cookie/token
      |
      v
Scan contacts
```

But WeChat has changed its security model. Many accounts now see:

```
Scan QR
   |
   v
"Need iPad to confirm login"
```

because WeChat treats this as a **new web/device login risk**.

The project issue you mentioned is also a symptom of this kind of breakage: the reported issue is "检测登录状态失败，手机已经登录，网页一直显示状态失败" (login status detection failed, phone already logged in, webpage keeps showing failure).

The reasons:

1. **WeChat Web login is not a stable public API**

Projects like this depend on reverse engineering internal protocols. WeChat can change:

* QR login flow
* device fingerprint checks
* risk control rules
* session tokens
* protobuf/API endpoints

without notice.

2. **Account risk level matters**

Some accounts can still login:

```
old account
+ trusted device
+ same network
+ previously used web login
```

may work.

Newer accounts often get:

```
QR scan
 -> security verification
 -> iPad confirmation
 -> impossible without extra device
```

3. **iPad confirmation is intentional**

WeChat historically allowed:

* Windows client login
* Web login
* iPad login

but iPad has a stronger trust relationship than browser automation.

So WeChat is basically saying:

> "This login looks like an iPad client. Confirm from a trusted iPad."

The project cannot bypass this legitimately.

---

If your goal is **find who deleted you from WeChat**, these projects are now difficult.

More practical options:

### Option 1: Use WeChat client automation (hard)

Run a real Android device:

```
Android phone
    |
uiautomator / accessibility
    |
WeChat app
    |
scan contacts
```

This is closer to how commercial tools work.

### Option 2: Export contacts and compare

If you can get:

```
friends_today.json
friends_old.json
```

then:

```python
old = set(open("old.txt").read().splitlines())
new = set(open("new.txt").read().splitlines())

print(old - new)
```

The hard part is extraction, not comparison.

### Option 3: Use WeChat PC client

Some automation projects use:

```
Windows WeChat
      |
memory/API hooks
      |
contacts
```

but these are fragile and can risk account bans.

---

For an engineering project perspective, this repo is interesting historically, but I would not spend much time making it work. The real technical challenge is no longer QR scanning; it is **reverse engineering WeChat's device trust and risk-control system**.

References:

* `WechatRealFriends` GitHub issue #116:
