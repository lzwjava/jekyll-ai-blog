---
audio: false
generated: true
image: false
lang: en
layout: post
title: Access Instance With Server SSH Key
translated: false
type: note
---

Question: How to use a server-generated SSH key's permissions to access the instance?

Answer: 

If a server (such as AWS EC2, Oracle Cloud, Azure, or similar cloud provider) **generated an SSH key pair** for you during instance creation, this almost always means:

- The **public key** was automatically placed on the instance (usually in `~/.ssh/authorized_keys`).
- The **private key** was provided to you as a downloadable file (most commonly a `.pem` file in AWS).

You use the **private key file** (not the public key or "perm") to authenticate when connecting via SSH.

### Step-by-step guide to access the instance

1. **Locate the private key file**
   - Find the `.pem` file (AWS) or other private key file you downloaded when launching the instance.
   - Example names: `my-key-pair.pem`, `id_rsa`, etc.
   - Make sure you know its full path (e.g., `~/Downloads/my-key.pem` or `C:\keys\my-key.pem`).

2. **Set correct file permissions (very important – SSH refuses keys with loose permissions)**
   On Linux/macOS:
   ```bash
   chmod 400 /path/to/your-key.pem
   ```
   On Windows (if using OpenSSH or Git Bash):
   ```bash
   icacls "C:\path\to\your-key.pem" /inheritance:r
   icacls "C:\path\to\your-key.pem" /grant:r "%username%:F"
   ```
   This ensures only you can read the file.

3. **Find your instance connection details**
   - Public IP address or Public DNS name (from cloud console)
   - Username (common defaults):
     - AWS EC2 Amazon Linux / Fedora → `ec2-user`
     - AWS Ubuntu → `ubuntu`
     - CentOS / RHEL → `centos` or `ec2-user`
     - Oracle Cloud → `opc`
     - Debian → `admin` or `debian`
     - Google Cloud → usually your Google username

4. **Connect using SSH**
   Basic command (Linux/macOS or Windows with OpenSSH):
   ```bash
   ssh -i /path/to/your-key.pem username@public-ip-or-dns
   ```
   Real examples:

   ```bash
   # AWS Amazon Linux example
   ssh -i ~/my-key.pem ec2-user@ec2-54-123-45-67.compute-1.amazonaws.com

   # Ubuntu example
   ssh -i ~/my-key.pem ubuntu@34.89.12.34

   # Very verbose mode (useful for debugging)
   ssh -i ~/my-key.pem -v username@public-ip
   ```

5. **Common fixes for "Permission denied (publickey)" error**
   - Wrong private key file → double-check you're using the correct one
   - Wrong username → check cloud provider documentation
   - Key permissions too open → run `chmod 400` again
   - Instance security group doesn't allow SSH (port 22) from your IP
   - Instance is in private subnet (needs bastion/jump host or VPN)
   - Key was replaced/removed on the instance after launch

The phrase "its perm" most likely refers to the private key file permissions (which must be restrictive), not the public key.

If you never received/downloaded any private key file, then the instance probably doesn't have key-based login enabled — in that case you may need to:
- Use cloud console "Connect" feature (EC2 Instance Connect, Serial Console, etc.)
- Reset access by mounting the volume elsewhere
- Or create and add a new key pair

References:  

- [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect-linux-inst-ssh.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect-linux-inst-ssh.html)
- [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html)