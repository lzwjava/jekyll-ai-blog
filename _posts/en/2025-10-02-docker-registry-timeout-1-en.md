---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast:free
title: Docker Registry Connection Timeout Troubleshooting
translated: false
type: note
---

The error you're encountering, `Error response from daemon: Get "https://registry-1.docker.io/v2/": net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)`, indicates that the Docker client failed to connect to the Docker Hub registry due to a timeout. This could be caused by network issues, authentication problems, or configuration errors. Since you're attempting a web-based login, let's troubleshoot and resolve the issue step-by-step.

### Steps to Resolve the Issue

1. **Verify Network Connectivity**
   - Ensure your internet connection is stable.
   - Test connectivity to Docker Hub by running:
     ```bash:disable-run
     ping registry-1.docker.io
     ```
     or
     ```bash
     curl -v https://registry-1.docker.io/v2/
     ```
     If these fail, you may have a network issue (e.g., firewall, proxy, or DNS problems).

2. **Check Web-Based Authentication**
   - The message indicates you're using a one-time device confirmation code (`LVFK-KCQX`). Ensure you:
     - Pressed `ENTER` to open the browser or manually visited `https://login.docker.com/activate`.
     - Entered the code correctly in the browser.
     - Completed the authentication process in the browser within the timeout period.
   - If the browser didn't open automatically, manually visit the URL and input the code.
   - If authentication fails or times out, try restarting the process:
     ```bash
     docker login
     ```

3. **Handle Timeout Issues**
   - The timeout error suggests the Docker client couldn't connect to the registry. Increase the timeout by setting the `DOCKER_CLIENT_TIMEOUT` environment variable:
     ```bash
     export DOCKER_CLIENT_TIMEOUT=120
     export COMPOSE_HTTP_TIMEOUT=120
     docker login
     ```
     This extends the timeout to 120 seconds.

4. **Check for Proxy or Firewall Issues**
   - If you're behind a proxy, configure Docker to use it. Edit or create `~/.docker/config.json` and add:
     ```json
     {
       "proxies": {
         "default": {
           "httpProxy": "http://<proxy-host>:<proxy-port>",
           "httpsProxy": "https://<proxy-host>:<proxy-port>",
           "noProxy": "localhost,127.0.0.1"
         }
       }
     }
     ```
     Replace `<proxy-host>` and `<proxy-port>` with your proxy details.
   - If a firewall is blocking access, ensure `registry-1.docker.io` and `login.docker.com` are allowed.

5. **Use Credential Helper (Optional but Recommended)**
   - The warning about unencrypted credentials in `~/.docker/config.json` suggests setting up a credential helper. Install a credential helper like `docker-credential-pass` or `docker-credential-secretservice`:
     - For Linux with `pass`:
       ```bash
       sudo apt-get install pass
       curl -fsSL https://github.com/docker/docker-credential-helpers/releases/download/v0.7.0/docker-credential-pass-v0.7.0-amd64.tar.gz | tar -xz
       sudo mv docker-credential-pass /usr/local/bin/
       ```
       Initialize `pass`:
       ```bash
       gpg2 --gen-key
       pass init <your-gpg-key-id>
       ```
       Update `~/.docker/config.json` to use the helper:
       ```json
       {
         "credsStore": "pass"
       }
       ```
     - Retry the login after configuring the credential helper.

6. **Fallback to Command-Line Login**
   - If web-based login continues to fail, try the command-line login with your Docker Hub username and password:
     ```bash
     docker login -u <your-username>
     ```
     Enter your password or a Personal Access Token (PAT) when prompted. You can generate a PAT from your Docker Hub account settings.

7. **Check Docker Daemon Status**
   - Ensure the Docker daemon is running:
     ```bash
     sudo systemctl status docker
     ```
     If it's not running, start it:
     ```bash
     sudo systemctl start docker
     ```

8. **Clear Docker Configuration (Last Resort)**
   - If the issue persists, clear the Docker configuration file and retry:
     ```bash
     mv ~/.docker/config.json ~/.docker/config.json.bak
     docker login
     ```

### Additional Notes
- **Docker Hub Status**: Check if Docker Hub is experiencing outages by visiting `https://status.docker.com/`.
- **DNS Issues**: If `registry-1.docker.io` doesn't resolve, try using a public DNS like Google (`8.8.8.8`) or Cloudflare (`1.1.1.1`) in your network settings.
- **Docker Version**: Ensure your Docker client is up-to-date:
  ```bash
  docker --version
  ```
  Update Docker if needed, following the instructions for your OS.

### References
- [Docker Credential Store Documentation](https://docs.docker.com/go/credential-store/)
- [Docker Login Documentation](https://docs.docker.com/engine/reference/commandline/login/)
- [Docker Hub Status](https://status.docker.com/)
```
