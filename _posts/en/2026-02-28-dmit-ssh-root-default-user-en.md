---
audio: false
generated: true
image: false
lang: en
layout: post
title: DMIT SSH Default Username Root
translated: false
type: note
---

Question: For dmit.io, when using the command `ssh -i id_rsa.pem xxx`, what is the username to access the server?

Answer:

For **dmit.io** VPS instances, the default SSH username is **`root`**.

This is consistently shown in their official connection guides (even though some knowledge base pages now return 404 errors, archived/cached versions and multiple references confirm it).

### Correct command format

```bash
ssh -i id_rsa.pem root@your-vps-ip-address
```

Replace `your-vps-ip-address` with the actual public IP of your DMIT VPS (you can find it in your client area on dmit.io).

### Real examples

```bash
# Basic connection
ssh -i id_rsa.pem root@123.45.67.89

# With verbose output for debugging
ssh -i id_rsa.pem -v root@your-server-ip

# If your key has a passphrase
ssh -i id_rsa.pem root@your-server-ip
```

### Important notes

- DMIT provides or lets you download a private key (often named something like `id_rsa.pem` or similar) when you enable SSH key access or during provisioning.
- Make sure the private key file permissions are secure:

  ```bash
  chmod 400 id_rsa.pem
  ```

- If you get **Permission denied (publickey)**:
  - Confirm you're using `root` (not `admin`, `user`, `ubuntu`, etc.)
  - Verify the correct private key file is specified with `-i`
  - Check that port 22 is open in your VPS firewall/security settings
  - Ensure the public key is properly installed in `/root/.ssh/authorized_keys` on the server
- DMIT uses **root** login by default for most (or all) of their KVM-based VPS plans — this is common among many Hong Kong / Asia-focused low-end VPS providers.

If your instance was custom-installed with a different OS template that changes the default user (rare), check your welcome email or client area for specific credentials. But in standard DMIT setups, it's **root**.

References:

- [https://www.dmit.io/index.php?rp=/knowledgebase/56/How-to-connect-DMIT-VPS-via-SSH-Key-using-PuTTY.html](https://www.dmit.io/index.php?rp=/knowledgebase/56/How-to-connect-DMIT-VPS-via-SSH-Key-using-PuTTY.html) (mentions typing "root" in Auto-login username)
- [https://www.dmit.io/index.php?rp=/knowledgebase/64/How-to-connect-DMIT-VPS-via-SSH-Key-using-Termius.html](https://www.dmit.io/index.php?rp=/knowledgebase/64/How-to-connect-DMIT-VPS-via-SSH-Key-using-Termius.html) (type "root" to the "Username")
- [https://www.dmit.io/index.php?rp=/knowledgebase/58/How-to-connect-DMIT-VPS-via-SSH-Key-using-XShell.html](https://www.dmit.io/index.php?rp=/knowledgebase/58/How-to-connect-DMIT-VPS-via-SSH-Key-using-XShell.html) (type "root" to the "User Name")
