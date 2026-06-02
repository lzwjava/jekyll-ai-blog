---
audio: false
generated: true
lang: en
layout: post
title: Building and Deploying a Docker Image
translated: false
type: note
---

Here’s a step-by-step guide to building a Spring Boot application into a Docker image and deploying it on a server:

### Prerequisites

1. **Java** (e.g., JDK 17 or compatible version) installed locally.
2. **Maven** or **Gradle** (depending on your Spring Boot project setup).
3. **Docker** installed on your local machine and the server.
4. **A Spring Boot project** ready to containerize.
5. **Server access** (e.g., via SSH) with Docker installed.

---

### Step 1: Prepare Your Spring Boot Application

Ensure your Spring Boot application is working locally. Test it with:

```bash
mvn spring-boot:run  # If using Maven
# OR
gradle bootRun       # If using Gradle
```

Make sure the application builds successfully:

```bash
mvn clean package    # Maven
# OR
gradle build         # Gradle
```

This generates a `.jar` file (e.g., `target/myapp-1.0.0.jar`).

---

### Step 2: Create a Dockerfile

In your project’s root directory (where the `.jar` file is located), create a file named `Dockerfile` with the following content:

```dockerfile
# Use an official OpenJDK runtime as the base image
FROM openjdk:17-jdk-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the Spring Boot JAR file into the container
COPY target/myapp-1.0.0.jar app.jar

# Expose the port your Spring Boot app runs on (default is 8080)
EXPOSE 8080

# Run the JAR file
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**Notes:**

- Replace `myapp-1.0.0.jar` with the actual name of your JAR file.
- Adjust the Java version (`openjdk:17-jdk-slim`) if your app uses a different version.

---

### Step 3: Build the Docker Image

From the directory containing the `Dockerfile`, run:

```bash
docker build -t myapp:latest .
```

- `-t myapp:latest` tags the image as `myapp` with the `latest` version.
- The `.` tells Docker to use the current directory for the build context.

Verify the image was created:

```bash
docker images
```

---

### Step 4: Test the Docker Image Locally

Run the container locally to ensure it works:

```bash
docker run -p 8080:8080 myapp:latest
```

- `-p 8080:8080` maps port 8080 on your machine to port 8080 in the container.
- Open a browser or use `curl` to test (e.g., `curl http://localhost:8080`).

Stop the container with `Ctrl+C` or find its ID with `docker ps` and stop it:

```bash
docker stop <container-id>
```

---

### Step 5: Push the Image to a Docker Registry (Optional)

To deploy to a server, you’ll need to push the image to a registry like Docker Hub (or a private registry). If you skip this, you’ll transfer the image manually.

1. Log in to Docker Hub:

   ```bash
   docker login
   ```

2. Tag your image:

   ```bash
   docker tag myapp:latest yourusername/myapp:latest
   ```

3. Push the image:

   ```bash
   docker push yourusername/myapp:latest
   ```

---

### Step 6: Deploy to the Server

#### Option 1: Using a Registry

1. SSH into your server:

   ```bash
   ssh user@server-ip
   ```

2. Pull the image:

   ```bash
   docker pull yourusername/myapp:latest
   ```

3. Run the container:

   ```bash
   docker run -d -p 8080:8080 yourusername/myapp:latest
   ```

   - `-d` runs the container in detached mode (background).

#### Option 2: Manual Transfer

If you didn’t use a registry:

1. Save the image locally as a `.tar` file:

   ```bash
   docker save -o myapp.tar myapp:latest
   ```

2. Transfer it to the server (e.g., via SCP):

   ```bash
   scp myapp.tar user@server-ip:/path/to/destination
   ```

3. SSH into the server:

   ```bash
   ssh user@server-ip
   ```

4. Load the image:

   ```bash
   docker load -i myapp.tar
   ```

5. Run the container:

   ```bash
   docker run -d -p 8080:8080 myapp:latest
   ```

---

### Step 7: Verify Deployment

Check if the container is running:

```bash
docker ps
```

Test the app from the server or externally:

- If on the server: `curl http://localhost:8080`
- If external: Use the server’s IP (e.g., `http://server-ip:8080`), ensuring the port is open in the server’s firewall.

---

### Optional: Enhancements

- **Environment Variables**: Pass configs to your app:

  ```bash
  docker run -d -p 8080:8080 -e "SPRING_PROFILES_ACTIVE=prod" myapp:latest
  ```

- **Docker Compose**: For multi-container setups, use a `docker-compose.yml` file.
- **Restart Policy**: Add `--restart unless-stopped` to ensure the container restarts on server reboot.

Let me know if you need help with any specific part!

---

From the error output you provided, there are a few issues preventing your `docker build` command from succeeding. Let’s break them down and resolve them step-by-step.

---

### Issues Identified

1. **Missing `docker-buildx` Plugin**
   Error: `fork/exec /Users/lzwjava/.docker/cli-plugins/docker-buildx: no such file or directory`
   This suggests that Docker is trying to use the `buildx` plugin (a modern build tool), but it’s not installed or configured correctly.

2. **Legacy Builder Deprecation Warning**
   Warning: `DEPRECATED: The legacy builder is deprecated...`
   Docker recommends switching to BuildKit (`buildx`), but it’s falling back to the legacy builder, which is failing.

3. **Docker Daemon Not Running**
   Error: `Cannot connect to the Docker daemon at unix:///Users/lzwjava/.docker/run/docker.sock. Is the docker daemon running?`
   The Docker daemon (the background service that manages containers) isn’t running on your system.

4. **File Access Errors**
   Errors: `Can't add file ... to tar: io: read/write on closed pipe` and `Can't close tar writer...`
   These are secondary issues caused by the build process failing due to the daemon not running.

5. **Proxy Settings Detected**
   Your system is using proxies (`HTTP_PROXY` and `HTTPS_PROXY`). This might interfere with Docker if not configured properly.

---

### Step-by-Step Fix

#### 1. Verify Docker Daemon is Running

The core issue is that the Docker daemon isn’t running. Here’s how to fix it:

- **On macOS** (assuming you’re using Docker Desktop):
  1. Open Docker Desktop from your Applications folder or Spotlight.
  2. Ensure it’s running (you’ll see the Docker whale icon in the menu bar turn green).
  3. If it’s not starting:
     - Quit Docker Desktop and restart it.
     - Check for updates: Docker Desktop > Check for Updates.
     - If it still fails, reinstall Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop/).

- **Check via Terminal**:
  Run:

  ```bash
  docker info
  ```

  If the daemon is running, you’ll see system info. If not, you’ll get the same "Cannot connect" error.

- **Restart Daemon Manually** (if needed):

  ```bash
  sudo launchctl stop com.docker.docker
  sudo launchctl start com.docker.docker
  ```

Once the daemon is running, proceed to the next steps.

---

#### 2. Install `buildx` Plugin (Optional but Recommended)

Since the legacy builder is deprecated, let’s set up `buildx`:

1. **Install `buildx`**:
   - Download the binary manually or use Docker’s instructions:

     ```bash
     mkdir -p ~/.docker/cli-plugins
     curl -SL https://github.com/docker/buildx/releases/download/v0.13.0/buildx-v0.13.0.darwin-amd64 -o ~/.docker/cli-plugins/docker-buildx
     chmod +x ~/.docker/cli-plugins/docker-buildx
     ```

     (Check the [latest release](https://github.com/docker/buildx/releases) for your OS/architecture, e.g., `darwin-arm64` for M1/M2 Macs.)

2. **Verify Installation**:

   ```bash
   docker buildx version
   ```

3. **Set BuildKit as Default** (optional):
   Add this to `~/.docker/config.json`:

   ```json
   {
     "features": { "buildkit": true }
   }
   ```

Alternatively, you can skip this and use the legacy builder for now (see Step 4).

---

#### 3. Handle Proxy Settings

Your proxy settings (`http://127.0.0.1:7890`) might interfere with Docker’s ability to fetch images. Configure Docker to use them:

1. **Via Docker Desktop**:
   - Open Docker Desktop > Settings > Resources > Proxies.
   - Enable "Manual proxy configuration" and enter:
     - HTTP Proxy: `http://127.0.0.1:7890`
     - HTTPS Proxy: `http://127.0.0.1:7890`
   - Apply & Restart.

2. **Via CLI** (if not using Desktop):
   Create or edit `~/.docker/config.json`:

   ```json
   {
     "proxies": {
       "default": {
         "httpProxy": "http://127.0.0.1:7890",
         "httpsProxy": "http://127.0.0.1:7890"
       }
     }
   }
   ```

   Restart Docker after editing.

---

#### 4. Retry the Build

Now that the daemon is running and proxies are configured, try building again:

```bash
docker build -t myapp:latest .
```

- If you installed `buildx`, it will use BuildKit by default.
- If you skipped `buildx`, add `--progress=plain` to force the legacy builder:

  ```bash
  docker build --progress=plain -t myapp:latest .
  ```

---

#### 5. Troubleshoot `.git/hooks` Error (If Persists)

The `.git/hooks/pre-rebase.sample` error suggests Docker is trying to include unnecessary files in the build context. Exclude them with a `.dockerignore` file:

1. Create `.dockerignore` in the same directory as your `Dockerfile`:

   ```
   .git
   .gitignore
   *.md
   target/*
   !target/*.jar
   ```

2. This tells Docker to ignore the `.git` folder and everything in `target/` except your JAR file.

3. Retry the build:

   ```bash
   docker build -t myapp:latest .
   ```

---

### Final Verification

- Check the image:

  ```bash
  docker images
  ```

- Run it locally:

  ```bash
  docker run -p 8080:8080 myapp:latest
  ```

- Test with `curl http://localhost:8080`.

---

### Next Steps

Once the image builds successfully, follow the deployment steps from my previous response (e.g., push to a registry or transfer to a server). Let me know if you hit any more issues!
