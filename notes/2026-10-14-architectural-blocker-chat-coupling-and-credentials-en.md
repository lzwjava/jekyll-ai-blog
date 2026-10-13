---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Architectural Blocker: Chat Coupling and Credentials"
translated: false
type: note
---

I've completed the investigation, and I need to surface a **critical architectural finding** before writing code — because it changes the scope substantially and there's a hard blocker.

## What LeanCloud actually does here (3 features)

| Feature | Backend location | Replaceable backend-only? |
|---|---|---|
| **SMS verification codes** (`requestSmsCode`/`verifySmsCode`) | `Users.php` | ✅ Yes — Supabase Auth phone OTP |
| **IM conversations** (`createConversation`) | `LiveDao.php` → stores `conversationId` on the live | ⚠️ **No — see below** |
| **Template SMS notifications** (`sendTemplateSms`: LiveStart/VideoReady/Invite) | `Sms.php` (cron) | ⚠️ Gap — no Supabase equivalent |

## 🚨 The blocker: chat is coupled client-side, in 2 other repos

The backend's `createConversation` returns a **LeanCloud conversation ID**, and both frontends consume it directly with the `leancloud-realtime` npm SDK:

```
live-web/src/views/LiveView.vue:108    import { Realtime, ... } from 'leancloud-realtime'
live-mobile-web/src/views/LiveView.vue:75   import { Realtime, ... } from 'leancloud-realtime'
   appId: 's83aTX5nigX1KYu9fjaBTxIa-gzGzoHsz'   ← hardcoded LeanCloud app
   client.getConversation(live.conversationId)   ← connects to LeanCloud's servers
```

So the frontends **bypass the backend entirely** for chat and talk to LeanCloud's realtime infrastructure. If I swap only the backend's `createConversation` to return a Supabase ID, chat **breaks in a new way** — the frontends would get an ID that `leancloud-realtime` can't use. A full chat migration means rewriting chat in **both Vue apps** to use `supabase-js` Realtime + a `messages` table (Supabase has no built-in message history like LeanCloud conversations).

Also: **template SMS has no Supabase equivalent** — that needs Twilio/another provider wired via an Edge Function.

## 🚫 Hard blocker: no Supabase credentials
No project ref, anon key, or service role key exists anywhere in the repo or env. I can't wire this up or verify it end-to-end without them.

## My recommendation
Migrate in two phases, backend-first, so each piece is verifiable:
1. **SMS verification** → Supabase Auth phone OTP (unambiguous, backend-only, unblocks login once SMS codes are down from the archived app)
2. **Conversation storage** → Supabase `conversations` table, and **flag the frontend chat rewrite** as required follow-up in `live-web` + `live-mobile-web`

But before I build, two questions genuinely change what I write:

1. **Scope of chat** — (a) backend-only now (chat stays broken until frontends migrate), or (b) full migration including rewriting chat in both Vue apps?
2. **Credentials** — can you give me the Supabase **project URL + anon key + service role key**? (And whether SMS should go through Supabase's phone provider, or you'll attach Twilio.)

If you just say **"backend-only, SMS first, here are the creds"**, I'll start immediately and leave the chat frontend rewrite as a clearly-documented follow-up. Which way do you want to go?