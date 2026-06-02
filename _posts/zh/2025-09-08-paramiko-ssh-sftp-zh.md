---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: Paramiko SSH与SFTP使用指南
translated: true
type: note
---

### 安装
Paramiko 是一个用于 SSH 和 SFTP 的 Python 库。通过 pip 安装：

```bash
pip install paramiko
```

### 基础用法
Paramiko 允许您连接 SSH 服务器、执行命令和传输文件。请始终安全处理私钥并使用强密码——Paramiko 支持基于密钥和密码的身份验证。

核心概念：
- **客户端**：使用 `paramiko.SSHClient()` 建立连接
- **传输层**：需要底层控制时使用 `paramiko.Transport()`
- 通过 `client.connect()` 进行身份验证，需提供主机名、用户名及密码或密钥（例如通过 `paramiko.RSAKey.from_private_key_file()`）

### 示例：连接并执行命令
以下是通过 SSH 连接服务器、执行命令并输出结果的完整脚本。请将占位符替换为实际信息。

```python
import paramiko

# 创建 SSH 客户端
client = paramiko.SSHClient()

# 自动添加主机密钥（生产环境需谨慎；应加载已知主机密钥）
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # 建立连接（使用密码或密钥文件）
    client.connect(
        hostname='your.server.com',
        port=22,  # 默认 SSH 端口
        username='your_username',
        password='your_password',  # 或使用 key_filename='path/to/private_key.pem'
    )

    # 执行命令
    stdin, stdout, stderr = client.exec_command('echo "Hello from SSH!"')

    # 读取输出
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')

    print("输出:", output)
    print("错误:", error)

except paramiko.SSHException as e:
    print(f"SSH 错误: {e}")
finally:
    client.close()
```

### 进阶示例：使用密钥认证与文件传输
如需使用密钥认证，请先生成密钥对（例如使用 `ssh-keygen`），将公钥添加到服务器的 `~/.ssh/authorized_keys`，然后使用：

```python
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # 基于密钥的连接
    client.connect(
        hostname='your.server.com',
        username='your_username',
        key_filename='~/.ssh/id_rsa',  # 私钥路径
    )

    # 执行命令
    stdin, stdout, stderr = client.exec_command('ls -la')
    print(stdout.read().decode('utf-8'))

    # SFTP 示例：传输文件
    sftp = client.open_sftp()
    sftp.put('local_file.txt', 'remote_file.txt')  # 上传
    sftp.get('remote_file.txt', 'local_copy.txt')  # 下载
    sftp.close()

except Exception as e:
    print(f"错误: {e}")
finally:
    client.close()
```

### 技巧与最佳实践
- **安全性**：优先使用密钥认证而非密码。生产环境中应禁用 `AutoAddPolicy`，并通过 `client.load_host_keys()` 验证主机密钥
- **错误处理**：始终捕获 `paramiko.SSHException`，并使用 `exit_status = stdout.channel.recv_exit_status()` 检查退出码
- **线程安全**：Paramiko 默认非线程安全，必要时请使用锁机制
- **文档**：详见[官方 Paramiko 文档](https://docs.paramiko.org/)。可使用 OpenSSH 的 `sshd` 或本地虚拟机进行测试

以上内容可帮助您快速入门，请根据实际需求进行调整！
