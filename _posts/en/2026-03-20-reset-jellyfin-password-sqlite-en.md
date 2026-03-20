---
audio: false
generated: true
image: false
lang: en
layout: post
title: Resetting Jellyfin Password via SQLite
translated: false
type: note
---

Sure. Here's what I did:

### How the Reset Worked

**1. Stop the service** — can't modify the database while Jellyfin is running:
```bash
sudo systemctl stop jellyfin
```

**2. Backup the database** — just in case:
```bash
sudo cp /var/lib/jellyfin/data/jellyfin.db /var/lib/jellyfin/data/jellyfin.db.bak
```

**3. Inspect the schema** — found the `Users` table and saw the password is stored as a PBKDF2-SHA512 hash in the `Password` column.

**4. Clear the password and force a reset:**
```sql
UPDATE Users SET Password='', MustUpdatePassword=1 WHERE Username='jellyfin';
```
- `Password=''` — removes the hash, so no password is needed to log in
- `MustUpdatePassword=1` — forces Jellyfin to prompt for a new password on next login

**5. Start the service back up:**
```bash
sudo systemctl start jellyfin
```

That's it. No Jellyfin CLI needed — just a direct SQLite edit on the local database.