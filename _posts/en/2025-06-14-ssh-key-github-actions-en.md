---
audio: false
generated: true
lang: en
layout: post
title: SSH Key Setup for GitHub Actions JAR Deployment
translated: false
type: note
---

To generate an SSH key for GitHub Actions to deploy a JAR file, follow these steps:

1. **Generate an SSH Key Pair**:
   - On your local machine or a secure environment, run:

     ```bash
     ssh-keygen -t ed25519 -C "your_email@example.com" -f github-actions-deploy
     ```

   - If your system doesn't support Ed25519, use:

     ```bash
     ssh-keygen -t rsa -b 4096 -C "your_email@example.com" -f github-actions-deploy
     ```

   - Press Enter to accept the default file location and optionally set a passphrase (recommended for security). This creates two files:
     - `github-actions-deploy` (private key)
     - `github-actions-deploy.pub` (public key)

2. **Add the Public Key to the Target Server**:
   - Copy the public key:

     ```bash
     cat github-actions-deploy.pub
     ```

   - Log in to the server where you'll deploy the JAR file.
   - Append the public key to `~/.ssh/authorized_keys` on the server:

     ```bash
     echo "your-public-key-content" >> ~/.ssh/authorized_keys
     ```

   - Ensure the `authorized_keys` file has the correct permissions:

     ```bash
     chmod 600 ~/.ssh/authorized_keys
     ```

3. **Store the Private Key in GitHub Secrets**:
   - Go to your GitHub repository: `Settings > Secrets and variables > Actions > Secrets`.
   - Click **New repository secret**.
   - Name the secret (e.g., `SSH_PRIVATE_KEY`).
   - Paste the contents of the private key (`github-actions-deploy`):

     ```bash
     cat github-actions-deploy
     ```

   - Save the secret.

4. **Configure the GitHub Actions Workflow**:
   - Create or edit a workflow file (e.g., `.github/workflows/deploy.yml`).
   - Add a step to use the SSH key for deploying the JAR. Below is an example workflow:

{% raw %}
     ```yaml
     name: Deploy JAR

     on:
       push:
         branches:
           - main

     jobs:
       deploy:
         runs-on: ubuntu-latest

         steps:
         - name: Checkout code
           uses: actions/checkout@v4

         - name: Set up Java
           uses: actions/setup-java@v4
           with:
             java-version: '17' # Adjust to your Java version
             distribution: 'temurin'

         - name: Build JAR
           run: mvn clean package # Adjust for your build tool (e.g., Gradle)

         - name: Install SSH Key
           uses: shimataro/ssh-key-action@v2
           with:
             key: ${{ secrets.SSH_PRIVATE_KEY }}
             known_hosts: 'optional-known-hosts' # See note below

         - name: Add Known Hosts
           run: |
             ssh-keyscan -H <server-ip-or-hostname> >> ~/.ssh/known_hosts
           # Replace <server-ip-or-hostname> with your server's IP or hostname

         - name: Deploy JAR to Server
           run: |
             scp target/your-app.jar user@<server-ip-or-hostname>:/path/to/deploy/
             ssh user@<server-ip-or-hostname> "sudo systemctl restart your-service" # Adjust for your deployment process
     ```
{% endraw %}

- **Notes**:
  - Replace `target/your-app.jar` with the path to your JAR file.
  - Replace `user@<server-ip-or-hostname>` with your server's SSH user and address.
  - Adjust the deployment command (e.g., `sudo systemctl restart your-service`) to match how you start or deploy the JAR on your server.
  - The `known_hosts` step is critical to avoid SSH host verification issues. If you know the server's host key, you can pre-populate it in the `shimataro/ssh-key-action` step, or use `ssh-keyscan` as shown.

5. **Secure the Workflow**:
   - Ensure the private key is never exposed in logs or outputs.
   - Restrict repository permissions to prevent unauthorized access to secrets.
   - If using a passphrase for the SSH key, add it as another secret and include it in the `shimataro/ssh-key-action` step:
{% raw %}

     ```yaml
     with:
       key: ${{ secrets.SSH_PRIVATE_KEY }}
       passphrase: ${{ secrets.SSH_KEY_PASSPHRASE }}
       known_hosts: 'optional-known-hosts'
     ```

{% endraw %}

6. **Test the Workflow**:
   - Push a change to the `main` branch (or the branch specified in the workflow).
   - Monitor the workflow in the **Actions** tab of your GitHub repository to ensure the JAR is built and deployed correctly.

7. **Troubleshooting**:
   - **Permission denied**: Verify the SSH key is correctly added to the server's `authorized_keys` and that the user has permission to access the target directory.
   - **Host verification failed**: Ensure the `known_hosts` step is correctly configured with the server's IP or hostname.
   - **Build issues**: Confirm the Java version and build commands match your project setup.

This setup securely integrates SSH-based deployment into your GitHub Actions workflow for deploying a JAR file. If you need specific adjustments (e.g., for a particular server setup or build tool), let me know!
