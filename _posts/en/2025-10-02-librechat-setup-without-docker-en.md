---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast:free
title: LibreChat Setup Without Docker Compose
translated: false
type: note
---

Yes, you can set up LibreChat without Docker Compose by using individual `docker run` commands or even a non-Docker method (manual installation with Node.js, Yarn, MongoDB, and MeiliSearch). This avoids downloading the `docker-compose` binary itself (which is small, ~20-30MB, but I assume you're referring to the overall image pulls totaling ~70MB+ for LibreChat's services). However, the core Docker images (e.g., for the app, MongoDB, MeiliSearch) are still around 500MB-1GB total when pulled—Docker Compose is just an orchestration tool on top of Docker, not the main bandwidth user. Pulling images over slow 4G/5G will still be the bottleneck, but you can mitigate it.

I'll outline options below, prioritizing bandwidth-saving tips first. If mobile data is very limited, consider tethering to a WiFi network temporarily or using a pre-downloaded setup on another machine (e.g., export/import images via `docker save`/`docker load`).

### Bandwidth-Saving Tips for Any Docker-Based Setup

- **Pre-pull images on a faster connection**: On another device with better internet, run `docker pull node:20-alpine` (for the app), `docker pull mongo:7` (database), and `docker pull getmeili/meilisearch:v1.10` (search). Then save them to files:

  ```
  docker save -o librechat-app.tar node:20-alpine
  docker save -o mongo.tar mongo:7
  docker save -o meili.tar getmeili/meilisearch:v1.10
  ```

  Transfer the .tar files via USB/drive (total ~500-800MB compressed), then on your Ubuntu machine: `docker load -i librechat-app.tar` etc. No online pulling needed.
- **Use lighter alternatives**: For testing, skip MeiliSearch initially (it's optional for search; disable in config). MongoDB image is ~400MB—use a local MongoDB install instead (see non-Docker section below) to save ~400MB.
- **Monitor usage**: Use `docker pull --quiet` or tools like `watch docker images` to track.
- **Proxy or cache**: If you have a Docker Hub mirror or proxy, configure it in `/etc/docker/daemon.json` to speed up pulls.

### Option 1: Pure Docker (No Compose) – Equivalent to Compose Setup

You can replicate the `docker-compose.yml` behavior with `docker run` and `docker network`. This downloads the same images but lets you control each step. Total download still ~700MB+ (app build + DBs).

1. **Create a Docker network** (isolates services):

   ```
   docker network create librechat-network
   ```

2. **Run MongoDB** (replace `your_mongo_key` with a strong password):

   ```
   docker run -d --name mongodb --network librechat-network \
     -e MONGO_INITDB_ROOT_USERNAME=librechat \
     -e MONGO_INITDB_ROOT_PASSWORD=your_mongo_key \
     -v $(pwd)/data/mongodb:/data/db \
     mongo:7
   ```

   - Creates `./data/mongodb` for persistence.

3. **Run MeiliSearch** (replace `your_meili_key`):

   ```
   docker run -d --name meilisearch --network librechat-network \
     -e MEILI_MASTER_KEY=your_meili_key \
     -p 7700:7700 \
     -v $(pwd)/data/meili:/meili_data \
     getmeili/meilisearch:v1.10
   ```

   - Skip if bandwidth is tight; disable in app config later.

4. **Clone and Build/Run the LibreChat App**:
   - Clone repo if not done: `git clone https://github.com/danny-avila/LibreChat.git && cd LibreChat` (~50MB download for repo).
   - Build the image (this pulls Node.js base ~200MB and builds app layers):

     ```
     docker build -t librechat-app .
     ```

   - Run it (links to DB, uses env vars—create a `.env` file as in my previous response):

     ```
     docker run -d --name librechat --network librechat-network -p 3080:3080 \
       --env-file .env \
       -v $(pwd):/app \
       librechat-app
     ```

     - In `.env`, set `MONGODB_URI=mongodb://librechat:your_mongo_key@mongodb:27017/LibreChat` and `MEILI_HOST=http://meilisearch:7700` etc.

5. **Access**: `http://localhost:3080`. Logs: `docker logs -f librechat`.

- **Stop/Cleanup**: `docker stop mongodb meilisearch librechat && docker rm them`.
- **Pros/Cons**: Same as Compose, but more manual. Still heavy on data for image pulls/build.

### Option 2: Non-Docker Installation (Manual, No Image Pulls) – Recommended for Low Bandwidth

Install dependencies natively on Ubuntu. This avoids all Docker overhead (~0MB for containers; just package downloads via apt/yarn, totaling ~200-300MB). Uses your system's Python/Node setups indirectly.

#### Prerequisites (Install Once)

```
sudo apt update
sudo apt install nodejs npm mongodb-org redis meilisearch git curl build-essential python3-pip -y  # MongoDB official pkg; MeiliSearch ~50MB binary
sudo systemctl start mongod redis meilisearch
sudo systemctl enable mongod redis meilisearch
```

- Node.js: If not v20+, install via nvm: `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash`, then `nvm install 20`.
- Yarn: `npm install -g yarn`.
- MongoDB config: Edit `/etc/mongod.conf` to bind to localhost, restart.

#### Installation Steps

1. **Clone Repo**:

   ```
   cd ~/projects
   git clone https://github.com/danny-avila/LibreChat.git
   cd LibreChat
   ```

2. **Install Dependencies**:

   ```
   yarn install  # ~100-200MB downloads for packages
   ```

3. **Configure `.env`** (copy from `.env.example`):
   - `cp .env.example .env && nano .env`
   - Key changes:
     - Mongo: `MONGODB_URI=mongodb://localhost:27017/LibreChat` (create DB user if needed via `mongo` shell).
     - Meili: `MEILI_HOST=http://localhost:7700` and `MEILI_MASTER_KEY=your_key`.
     - Disable search if skipping Meili: `SEARCH=false`.
     - Add AI keys as needed.

4. **Build and Run**:
   - In one terminal: `yarn run backend` (starts API on port 3090).
   - In another: `yarn run frontend` (starts UI on port 3080).
   - Or use PM2 for production: `yarn global add pm2 && pm2 start yarn --name backend -- run backend` etc.

5. **Access**: `http://localhost:3080`. Create account and configure.

- **Data**: MongoDB stores in `/var/lib/mongodb`, Meili in `/var/lib/meilisearch`.
- **Troubleshooting**:
  - Mongo auth: Run `mongo` and create user: `use LibreChat; db.createUser({user: 'librechat', pwd: 'yourpass', roles: ['readWrite']})`.
  - Ports/Firewall: `sudo ufw allow 3080,3090,7700`.
  - Updates: `git pull && yarn install && restart services`.
- **Pros**: Lighter on bandwidth (no containers), uses system resources directly. Cons: More setup fiddling, potential dependency conflicts (e.g., with your Python 3.13, but Node is separate).

If mobile data is extremely limited, the non-Docker method is best—do it in stages, monitoring with `du -sh` on directories. For errors, share logs (e.g., from `yarn run backend`). Official non-Docker guide: <https://docs.librechat.ai/install/installation/manual_install.html>. If you need Ollama integration for local AI (saves API costs), install it separately via their script (~100MB). Let me know for tweaks!
