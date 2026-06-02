---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Configuring Docker Daemon Proxy Settings
translated: false
type: note
---

### Configuring Docker Daemon for Proxy Settings

The Docker daemon can be configured to use an HTTP/HTTPS proxy for operations like pulling images or building containers from behind a corporate firewall. This is done by editing (or creating) the `/etc/docker/daemon.json` file. Note that this configuration applies to the daemon itself (e.g., for `docker pull` or `docker build`), not to individual containers (which would use environment variables or Docker build args).

#### Prerequisites
- You need root or sudo access on a Linux system (this is the primary OS for Docker daemon configuration; on Windows/Mac with Docker Desktop, use the GUI settings instead).
- Docker installed and running.
- Know your proxy server details (e.g., `http://proxy.company.com:8080` for HTTP/HTTPS proxy, and any no-proxy exceptions).

#### Step-by-Step Configuration

1. **Locate or Create the Daemon Configuration File**:
   - Open a terminal and navigate to `/etc/docker/` (create the directory if it doesn't exist: `sudo mkdir -p /etc/docker`).
   - Edit the file `daemon.json` using a text editor (e.g., `sudo nano /etc/docker/daemon.json` or `sudo vim /etc/docker/daemon.json`).
   - If the file doesn't exist, create it. Start with an empty JSON object `{}` if it's new.

2. **Add Proxy Configuration**:
   - Add a `"proxies"` section to the JSON file. Here's a basic example:

     ```json
     {
       "proxies": {
         "http-proxy": "http://proxy.company.com:8080",
         "https-proxy": "http://proxy.company.com:8080",
         "no-proxy": "localhost,127.0.0.1,*.company.com,10.0.0.0/8"
       }
     }
     ```

     - **Explanations**:
       - `"http-proxy"`: The URL for HTTP proxy (required for non-HTTPS requests).
       - `"https-proxy"`: The URL for HTTPS proxy (often the same as HTTP proxy).
       - `"no-proxy"`: A comma-separated list of hosts/domains/IP ranges that should bypass the proxy (e.g., local addresses or internal domains). This prevents infinite loops.
       - If authentication is needed, use the format `http://username:password@proxy.company.com:8080`.
       - For SOCKS proxies, use `"http-proxy": "socks5://proxy.company.com:1080"`.

     - If `daemon.json` already has existing content (e.g., other settings like `"log-driver": "json-file"`), merge the `"proxies"` section into it without duplicating keys. Ensure valid JSON syntax (use a tool like `jsonlint` to validate if needed).

3. **Save and Restart the Docker Daemon**:
   - Save the file.
   - Restart the Docker service to apply changes:
     ```
     sudo systemctl restart docker
     ```
     - On older systems or non-systemd setups, use `sudo service docker restart`.
   - Verify the daemon is running:
     ```
     sudo systemctl status docker
     ```
     - Check logs if there are issues: `sudo journalctl -u docker.service`.

4. **Verify the Configuration**:
   - Test by pulling an image (which should now route through your proxy):
     ```
     docker pull hello-world
     ```
   - Check if the proxy settings are applied by inspecting the daemon config:
     ```
     docker info | grep -i proxy
     ```
     - You should see output like:
       ```
       HTTP Proxy: http://proxy.company.com:8080
       HTTPS Proxy: http://proxy.company.com:8080
       No Proxy: localhost,127.0.0.1,*.company.com,10.0.0.0/8
       ```
   - If you're using Docker in a build context, test with:
     ```
     docker build -t test-proxy .
     ```
     (Assuming a simple Dockerfile that pulls a base image.)

#### Additional Notes
- **Security**: Avoid hardcoding credentials in `daemon.json` on shared systems. Use environment variables if possible, or tools like `docker config` for more advanced setups.
- **Common Issues**:
  - **Syntax Errors**: Invalid JSON will prevent the daemon from starting. Double-check with `cat /etc/docker/daemon.json` and a JSON validator.
  - **Firewall/SELinux**: Ensure your proxy is reachable and no security modules block it.
  - **Docker Version**: This works on Docker 20.10+ (earlier versions used different env vars like `HTTP_PROXY`). Check your version with `docker --version` and upgrade if needed.
  - **Registry-Specific Proxies**: For private registries, you might need additional config under `"registry-mirrors"` or insecure registries in `daemon.json`.
- **For Containers**: If you need proxy settings *inside* running containers (not the daemon), set environment variables in the Dockerfile (e.g., `ENV http_proxy=http://proxy.company.com:8080`) or via `docker run -e http_proxy=...`.
- **Docker Desktop (Windows/Mac)**: Go to Settings > Resources > Proxies, and enable/configure there—no JSON editing needed.

For more details, refer to the official Docker docs: [Configure the Docker daemon](https://docs.docker.com/engine/reference/commandline/dockerd/#daemon-configuration-file). If you encounter errors, share the exact output for troubleshooting!
