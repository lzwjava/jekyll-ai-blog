---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast:free
title: Installing LibreChat on Ubuntu
translated: false
type: note
---

### Installing LibreChat on Ubuntu 24.04 LTS

LibreChat is an open-source AI chat platform that supports multiple AI models (e.g., OpenAI, Gemini, Ollama) through a web interface. The recommended installation method is using Docker Compose, as it's simple, handles dependencies like MongoDB and MeiliSearch automatically, and works reliably on Ubuntu. Your system (Ubuntu 24.04.2 LTS with Python 3.13.4) meets the requirements, but you'll need to install Docker and Git first.

#### Prerequisites

1. **Update your system**:

   ```
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install Git** (if not already installed):

   ```
   sudo apt install git -y
   ```

3. **Install Docker and Docker Compose**:
   - Install Docker:

     ```
     sudo apt install docker.io -y
     sudo systemctl start docker
     sudo systemctl enable docker
     sudo usermod -aG docker $USER
     ```

     Log out and back in (or run `newgrp docker`) for group changes to take effect.
   - Install Docker Compose (latest version):

     ```
     sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
     sudo chmod +x /usr/local/bin/docker-compose
     ```

     Verify with `docker-compose --version`.

#### Installation Steps

1. **Clone the LibreChat repository**:

   ```
   cd ~/projects  # Or your preferred directory
   git clone https://github.com/danny-avila/LibreChat.git
   cd LibreChat
   ```

2. **Copy and configure the environment file**:
   - Copy the example file:

     ```
     cp .env.example .env
     ```

   - Edit `.env` with a text editor (e.g., `nano .env`). Key settings to update:
     - Set a MongoDB master key: Generate a strong password and set `MONGODB_URI=mongodb://mongodb:27017/LibreChat?authSource=admin` and `MONGODB_MASTER_KEY=your_generated_key_here`.
     - For MeiliSearch: Set `MEILI_MASTER_KEY=your_generated_key_here` (generate a strong key).
     - Add AI API keys if needed (e.g., `OPENAI_API_KEY=your_openai_key`). For local models like Ollama, no key is required initially.
     - Save and exit. For full config options, refer to the docs.

3. **Start LibreChat with Docker Compose**:

   ```
   docker-compose up -d
   ```

   - This pulls images, starts services (LibreChat app, MongoDB, MeiliSearch), and runs in detached mode.
   - Wait for it to fully start (check with `docker-compose logs -f`).

4. **Access LibreChat**:
   - Open your browser and go to `http://localhost:3080`.
   - Create an account on the login page.
   - Select an AI model (configure endpoints in settings) and start chatting.

#### Post-Installation Tips

- **Stopping/Updating**: Run `docker-compose down` to stop, then `git pull` and `docker-compose up -d --build` to update.
- **Data Persistence**: Volumes are created automatically for MongoDB data (in `./data/mongodb`).
- **Troubleshooting**:
  - If ports conflict, edit `docker-compose.yml` to change `3080:3080`.
  - For headless/server access, use your server's IP (e.g., `http://your-server-ip:3080`) and ensure firewall allows port 3080 (`sudo ufw allow 3080`).
  - If using local LLMs, install Ollama separately and add it as an endpoint in `.env`.
- **Alternative: NPM Method** (without Docker): If you prefer, install Node.js 18+, Yarn, MongoDB, and MeiliSearch manually, then run `yarn install` and `yarn run frontend` + `yarn run backend`. But Docker is strongly recommended for simplicity.

This should get you up and running quickly. If you encounter errors, share the output for more help!

[LibreChat Official Docs](https://docs.librechat.ai/install/installation/docker_compose.html)
[Ubuntu Docker Guide](https://docs.librechat.ai/install/installation/docker_ubuntu.html)
[It's FOSS Tutorial](https://itsfoss.com/librechat-linux/)
