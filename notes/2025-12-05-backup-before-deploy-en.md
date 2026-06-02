---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Back Up Before Deploying Code
translated: false
type: note
---

Question: When deploying new code or packages to production servers, is it a good practice to back up the old files/packages before replacing them?

Answer:

Yes, it is almost always considered a best practice to preserve the old version during deployment so you can roll back quickly and safely if something goes wrong.

Common safe deployment strategies that include keeping/backing up the old version:

- **Blue-green deployments** – You keep the old (blue) environment fully intact while bringing up the new (green) one, then switch traffic. Instant rollback by switching back.
- **Rolling deployments with versioned directories** – Deploy new code to `/app/v2025.12.05-01`, update symlink `/app/current` → new version. Old directory remains on disk until you delete it manually after verification.
- **Immutable artifacts + atomic switches** – Build a new container image or package, deploy it alongside the old one, then update the load balancer or service manager to point to the new one. Old image/version stays available.
- **Simple backup before overwrite** – Even in basic setups (scp/ftp/rsync), copy the current application directory to `.bak` or a timestamped folder first:

  ```bash
  cp -r /var/www/myapp /var/www/myapp.bak.$(date +%Y%m%d-%H%M%S)
  ```

  or

  ```bash
  tar czf /backups/myapp-$(date +%Y%m%d-%H%M%S).tgz /var/www/myapp
  ```

Why you should almost never deploy by blindly overwriting without a rollback path:

- A single syntax error or missing dependency can take the entire service down.
- Configuration mistakes or incompatible database migrations are common.
- Zero-downtime rollbacks are only possible if the old code is still present and runnable.
- Compliance/audit requirements in many organizations explicitly require proven rollback capability.

Exceptions where you might skip an explicit backup (but still have rollback):

- You are using Kubernetes with proper Deployment rollback (`kubectl rollout undo`).
- You are on platforms like Heroku, Vercel, Netlify, or Cloud Run that keep previous releases automatically.
- Git-based deployments (e.g., GitHub Actions deploying via `git pull` on the server) where you can simply `git checkout` the previous commit.

Even in those cases, most mature teams still keep at least a few previous artifacts/images for a few days.

Bottom line: Never deploy by permanently deleting or overwriting the currently running version without having a fast, tested way to get back to it. Keeping a backup or old version directory is cheap insurance.

References:

- [The Twelve-Factor App – Deploy](https://12factor.net/)
- [Martin Fowler – BlueGreenDeployment](https://martinfowler.com/bliki/BlueGreenDeployment.html)
- [Google SRE Book – Reliable Deployments (Chapter 27)](https://sre.google/sre-book/)
