---
audio: false
generated: true
image: false
lang: en
layout: post
title: Detecting Deleted WeChat Contacts
translated: false
type: note
---

Question: Any tool to scan WeChat contacts and find who deleted me?

Answer:

Yes, there are tools/scripts that claim to detect who has deleted you on WeChat, but **be careful**: WeChat does not provide an official API for this. Most "friend checkers" work by trying to send messages, create group chats, or batch-check contact status, which can:

* violate WeChat's Terms of Service
* trigger account risk controls
* leak your contacts/session data
* get your account temporarily restricted

### How these tools usually work

There are several techniques:

#### 1. Group chat detection (common)

The script creates a temporary group with selected contacts.

If someone deleted you:

* WeChat may show "you are not friends" when adding them
* The person may receive no notification if the group is immediately deleted (behavior has changed over versions)

Problem:

* Adding hundreds of people can trigger anti-spam protection.

#### 2. Transfer / payment check

Some scripts try:

```
Friend -> send small payment request -> observe error
```

Example:

```
"Please enter payment password"
vs
"You're not friends, please send friend request"
```

Problem:

* Risky.
* Could annoy contacts.
* Not reliable.

#### 3. Export + compare contacts

Some Android tools extract the WeChat database:

Typical location:

```
/data/data/com.tencent.mm/
```

Database:

```
EnMicroMsg.db
```

Then analyze:

```
Contact table
    username
    nickname
    alias
    type
```

Problem:

* Requires root access.
* WeChat encrypts data.
* Modern Android versions make this difficult.

---

### Open-source projects

Historically:

* `wechaty`

[Wechaty GitHub](https://github.com/wechaty/wechaty?utm_source=chatgpt.com)

Wechaty is a WeChat bot framework. It used to support personal WeChat automation, but personal account support has become limited because WeChat tightened restrictions.

Older scripts:

* `wxpy`

[wxpy GitHub](https://github.com/youfou/wxpy?utm_source=chatgpt.com)

Also mostly unusable for modern personal accounts.

---

### Safer manual method

If you only need to check a small number of people:

1. Open contact profile.
2. Tap "Send Message".
3. Look for:

   * normal chat → probably still friends
   * "You are not friends yet..." → deleted/removed

Or:

```
Contacts → Search → name → profile
```

---

### My recommendation

For an important WeChat account:

* Do **not** install random "WeChat friend scanner APKs".
* Do **not** give your WeChat QR login/session to websites.
* If you have thousands of contacts and need cleanup, use a controlled script only on a secondary account.

A safer engineering approach would be:

```
Android emulator
        |
        v
uiautomator/Appium
        |
        v
WeChat UI automation
        |
        v
slow verification
```

with rate limits:

```
check 20-50 contacts/day
random delays
no group creation
no messaging
```

but even this can still risk the account.

There is currently no official, reliable "scan all deleted me" API.