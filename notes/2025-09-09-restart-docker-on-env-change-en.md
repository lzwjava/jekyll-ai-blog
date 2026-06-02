---
audio: false
date: 2025-09-09
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Restart Docker Containers After Env Change
translated: false
type: note
---

When you change `.env`, Docker won’t automatically reload those environment variables. You need to restart the containers so they pick up the new values. For your LibreChat setup, you can do it like this:

1. Make sure you’re in the same directory as your `docker-compose.yml` file.
2. Run:

```bash
docker compose down
docker compose up -d
```

That will stop and remove the running containers, then recreate them with the new `.env` values.

---

### Alternative: restart only

If you don’t want to fully tear everything down, you can force containers to pick up the new env by rebuilding:

```bash
docker compose up -d --force-recreate
```

Or if you’ve also changed Dockerfiles or dependencies, add `--build`:

```bash
docker compose up -d --build
```

---

✅ In short:

* After editing `.env`, always **recreate** containers (`down` + `up` or `up --force-recreate`).
* A simple `docker compose restart` won’t reload new env values, it just restarts with the old ones.

Do you also want me to show you how to **verify** your LibreChat containers are using the new env values (e.g. with `docker inspect` or `docker exec env`)?
