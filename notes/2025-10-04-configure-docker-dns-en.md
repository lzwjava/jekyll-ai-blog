---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Configure Docker Daemon DNS Servers
translated: false
type: note
---

To configure DNS servers for the Docker daemon (which will be used by containers unless overridden at the container level), you can edit the `/etc/docker/daemon.json` file. This file allows you to customize Docker's runtime behavior.

### Steps to Configure DNS

1. **Edit the daemon.json file**:
   - If the file doesn't exist, create it with root privileges (e.g., using `sudo nano /etc/docker/daemon.json` or your preferred editor).
   - Add or update the `dns` key as an array of IP addresses for the DNS servers. For example, to use Google's public DNS (8.8.8.8 and 8.8.4.4):

     ```json
     {
       "dns": ["8.8.8.8", "8.8.4.4"]
     }
     ```

     - You can add more servers if needed (e.g., Cloudflare's 1.1.1.1).
     - This setting applies to all containers created with the default network unless specified otherwise.

2. **Validate the JSON**:
   - Ensure the file is valid JSON. You can use a tool like `jq` to check: `jq . /etc/docker/daemon.json`. If it errors, fix the syntax.

3. **Restart the Docker service**:
   - Apply the changes by restarting Docker:

     ```
     sudo systemctl restart docker
     ```

     - On non-systemd systems (e.g., older Linux distros), use `sudo service docker restart`.
   - Verify the status: `sudo systemctl status docker`.

4. **Test the configuration**:
   - Run a test container and check its DNS resolution:

     ```
     docker run --rm busybox nslookup google.com
     ```

     - It should resolve using your configured DNS servers.

### Notes

- **Scope**: This configures DNS for the Docker daemon on the host, affecting outbound name resolution for containers. It doesn't change the host's system DNS.
- **Overrides**: If a container needs different DNS (e.g., via `--dns` flag in `docker run`), it will override this daemon-level setting.
- **Security**: Using public DNS like 8.8.8.8 is fine for most cases, but consider internal DNS for enterprise environments.
- **Documentation**: For more options (e.g., DNS search domains), see the [official Docker docs on daemon.json](https://docs.docker.com/engine/reference/commandline/dockerd/#daemon-configuration-file).

If you encounter errors (e.g., permission issues or JSON parsing), share the details for further troubleshooting.
