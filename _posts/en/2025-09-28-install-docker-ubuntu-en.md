---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-sonnet-4
title: Installing Docker on Ubuntu Guide
translated: false
type: note
---

Based on your Ubuntu system output, you have several options to install Docker. Here's the recommended approach:

## Option 1: Install Docker Engine (Recommended)

The most common and recommended way is to install Docker Engine from Docker's official repository:

```bash
# Update package index
sudo apt update

# Install prerequisites
sudo apt install apt-transport-https ca-certificates curl software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package index again
sudo apt update

# Install Docker Engine
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## Option 2: Quick Install via APT (Simpler)

From the options shown in your terminal, you can use:

```bash
sudo apt install docker.io
```

## Post-Installation Setup

After installation, you'll want to:

1. **Start and enable Docker service:**

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

2. **Add your user to the docker group** (to run Docker without sudo):

```bash
sudo usermod -aG docker $USER
```

Then log out and log back in, or run:

```bash
newgrp docker
```

3. **Verify installation:**

```bash
docker --version
docker run hello-world
```

## Which Option to Choose?

- **Option 1** gives you the latest Docker version directly from Docker Inc.
- **Option 2** is simpler but may have a slightly older version from Ubuntu's repositories

For most users, Option 2 (`sudo apt install docker.io`) is perfectly fine and much simpler. The version difference is usually minimal for regular use.

Would you like me to explain any of these steps in more detail?
