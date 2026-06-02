---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Paramiko SSH and SFTP Guide
translated: false
type: note
---

### Installation
Paramiko is a Python library for SSH and SFTP. Install it via pip:

```bash
pip install paramiko
```

### Basic Usage
Paramiko allows you to connect to SSH servers, run commands, and transfer files. Always handle private keys securely and use strong passwords—Paramiko supports key-based and password authentication.

Key concepts:
- **Client**: Use `paramiko.SSHClient()` to set up a connection.
- **Transport**: For lower-level control, use `paramiko.Transport()`.
- Authenticate via `client.connect()` with hostname, username, and either password or key (e.g., via `paramiko.RSAKey.from_private_key_file()`).

### Example: Connecting and Running a Command
Here's a complete script to connect to an SSH server, run a command, and print the output. Replace placeholders with your details.

```python
import paramiko

# Create SSH client
client = paramiko.SSHClient()

# Auto-add host key (be cautious in production; load known_hosts instead)
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Connect (use password or key file)
    client.connect(
        hostname='your.server.com',
        port=22,  # Default SSH port
        username='your_username',
        password='your_password',  # Or key_filename='path/to/private_key.pem'
    )

    # Run a command
    stdin, stdout, stderr = client.exec_command('echo "Hello from SSH!"')

    # Read output
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')

    print("Output:", output)
    print("Error:", error)

except paramiko.SSHException as e:
    print(f"SSH error: {e}")
finally:
    client.close()
```

### Advanced Example: Using Key-Based Authentication and File Transfer
For key auth, generate a key pair if needed (e.g., `ssh-keygen`), add the public key to `~/.ssh/authorized_keys` on the server, then use:

```python
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Key-based connect
    client.connect(
        hostname='your.server.com',
        username='your_username',
        key_filename='~/.ssh/id_rsa',  # Path to private key
    )

    # Run command
    stdin, stdout, stderr = client.exec_command('ls -la')
    print(stdout.read().decode('utf-8'))

    # SFTP example: transfer file
    sftp = client.open_sftp()
    sftp.put('local_file.txt', 'remote_file.txt')  # Upload
    sftp.get('remote_file.txt', 'local_copy.txt')  # Download
    sftp.close()

except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
```

### Tips and Best Practices
- **Security**: Prefer key-based auth over passwords. Disable `AutoAddPolicy` in production and verify host keys via `client.load_host_keys()`.
- **Error Handling**: Always catch `paramiko.SSHException` and check exit codes with `exit_status = stdout.channel.recv_exit_status()`.
- **Threads**: Paramiko isn't thread-safe by default; use locks if needed.
- **Documentation**: For more, see the [official Paramiko docs](https://docs.paramiko.org/). Test with tools like OpenSSH's `sshd` or local VMs.

This should get you started; adapt to your needs!
