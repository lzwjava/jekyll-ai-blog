---
audio: false
generated: true
image: false
lang: en
layout: post
title: Healthy Live Server with Dead Port
translated: false
type: note
---

It's already up — and healthy. Here's the state:

## Status

| Service | Container | Status |
| --- | --- | --- |
| PHP 8.5-FPM app | `live-server-app-1` | up 45h |
| nginx | `live-server-web-1` | up 2d |
| MySQL 5.7 (`qulive`) | `live-server-database-1` | up 2d — 23 tables, 2 users |
| Redis 7 | `live-server-redis-1` | up 2d |

## Smoke tests (all passing)

```
GET  /            -> 200  {"app":"live-server","status":"migrated from CI3"}
GET  /home        -> 200
GET  /users/1     -> 200  {"status":"object_not_exists", ...}   (DB round-trip OK)
POST /users/list  -> 200
POST /login       -> 200
GET  /lives/count -> 200  {"count":"0"}
GET  /static/     -> 200  (frontend dist volume mounted)
```

**Entry point: `http://localhost:8088`** (nginx → `app:9000` fastcgi).

## One real issue found

`docker-compose.yml:21` maps `"8082:80"` to the `app` service, but that image is `php:8.5-fpm` with **no nginx** — nothing listens on port 80 in the container (only `:9000`). So `http://localhost:8082` accepts the connection and immediately resets:

```
> GET / HTTP/1.1
* Recv failure: Connection reset by peer
```

Nothing else in the repo references 8082, so it's a dead mapping. Two options:

1. **Remove the mapping** — 8088 is the only entry point (cleanest).
2. **Remap to FPM** — `"9000:9000"` if you ever want to point a host-side nginx at it directly.

Want me to drop the dead `8082:80` line? I'd leave the containers untouched otherwise since everything is serving.
