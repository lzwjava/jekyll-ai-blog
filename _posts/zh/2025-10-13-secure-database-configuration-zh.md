---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 安全数据库配置策略
translated: true
type: note
---

### 处理 Python 项目中的敏感数据库配置

在 Python 项目中管理数据库密码和端口等敏感信息是常见挑战。目标是在保持部署简单的同时，避免将密钥提交到版本控制系统（如 Git）。下面我将比较您提到的两种方法：（1）使用模板 `config_example.ini` 配合 `.gitignore` 忽略真实文件，并在 UAT 等服务器上手动设置；（2）使用 GPG 加密将加密值存储在 `config.ini` 中，并在运行时解密。如果正确实施，这两种方法都很安全，但它们在简单性和自动化之间有所权衡。

#### 方法一：模板配置 + `.gitignore` + 手动服务器设置

这是一种直接的低技术方法。您为开发人员和 CI/CD 流水线创建示例配置文件，在 Git 中忽略真实文件，并在类生产环境（如 UAT 服务器）上手动处理实际配置。

**实施步骤：**

1. 创建带占位符的 `config_example.ini`：

   ```
   [database]
   host = localhost
   port = 5432  # 示例端口；替换为真实端口
   user = dbuser
   password = example_password  # 替换为真实密码
   database = mydb
   ```

2. 将真实的 `config.ini` 添加到 `.gitignore`：

   ```
   config.ini
   ```

3. 在 Python 代码中从 `config.ini` 加载（开发环境下若文件缺失则回退到示例文件）：

   ```python
   import configparser
   import os

   config = configparser.ConfigParser()
   config_file = 'config.ini' if os.path.exists('config.ini') else 'config_example.ini'
   config.read(config_file)

   db_host = config['database']['host']
   db_port = config['database']['port']
   db_user = config['database']['user']
   db_password = config['database']['password']
   db_name = config['database']['database']
   ```

4. 对于 UAT 服务器：在部署期间手动复制包含真实值的 `config.ini`（例如通过 SCP 或 Ansible）。开发人员可以复制 `config_example.ini` 为 `config.ini` 并在本地填写。

**优点：**

- 简单——无需额外库或密钥管理。
- 无运行时开销（解密）。
- 适合小团队；与手动部署配合良好。

**缺点：**

- 在每个服务器上手动设置会增加错误风险（例如忘记更新密码）。
- 不适合自动化 CI/CD；需要安全的密钥注入（例如通过流水线中的环境变量）。
- 如果有人误提交 `config.ini`，密钥会暴露。

这种方法非常适合早期项目或当加密显得过于复杂时。

#### 方法二：对配置值使用 GPG 加密

这种方法使用 GPG 加密敏感字段（例如密码），将加密后的数据块存储在 `config.ini` 中，并在代码运行时解密。只要您的私钥从未共享，加密文件可以安全地提交到 Git。

**实施步骤：**

1. 在系统上安装 GPG（Linux/Mac 上标准；Windows 使用 Gpg4win）。如果需要，生成密钥对：

   ```
   gpg --gen-key  # 按照提示操作生成密钥
   ```

2. 将敏感值（例如密码）加密到文件中：

   ```
   echo "real_password_here" | gpg --encrypt --recipient your-email@example.com -o encrypted_password.gpg
   ```

   - 这会创建 `encrypted_password.gpg`。您可以对其进行 base64 编码以便存储在 INI 中：

     ```bash
     base64 encrypted_password.gpg > encrypted_password.b64
     ```

3. 更新 `config.ini` 以包含加密（且 base64 编码）的值。提交此文件——它是安全的：

   ```
   [database]
   host = localhost
   port = 5432
   user = dbuser
   password_encrypted = <base64-encoded-encrypted-blob-here>  # 来自 encrypted_password.b64
   database = mydb
   ```

4. 在 Python 代码中，使用 `gnupg` 库解密（开发环境通过 `pip install python-gnupg` 安装，但需假设其可用）：

   ```python
   import configparser
   import gnupg
   import base64
   import tempfile
   import os

   config = configparser.ConfigParser()
   config.read('config.ini')  # 可以安全提交此文件

   # 解密密码
   gpg = gnupg.GPG()  # 假设 GPG 已安装且密钥可用
   encrypted_b64 = config['database']['password_encrypted']
   encrypted_data = base64.b64decode(encrypted_b64)

   with tempfile.NamedTemporaryFile(delete=False) as tmp:
       tmp.write(encrypted_data)
       tmp.flush()
       decrypted = gpg.decrypt_file(None, passphrase=None, extra_args=['--batch', '--yes'], output=tmp.name)
       if decrypted.ok:
           db_password = decrypted.data.decode('utf-8').strip()
       else:
           raise ValueError("解密失败")

   os.unlink(tmp.name)  # 清理

   db_host = config['database']['host']
   db_port = config['database']['port']
   db_user = config['database']['user']
   db_name = config['database']['database']

   # 现在使用 db_password...
   ```

5. 对于 UAT 服务器：按原样部署 `config.ini`（通过 Git 或复制）。确保 GPG 私钥安全地放置在服务器上（例如通过 Ansible vault 或手动安全复制）。代码将在启动时解密。

**优点：**

- 加密配置可以版本控制——无需为密钥使用 `.gitignore`。
- 自动化部署；与 CI/CD 配合良好（只需安全同步密钥）。
- 可审计：加密值的更改被跟踪。

**缺点：**

- 需要 GPG 设置和密钥管理（例如定期轮换密钥；绝不提交私钥）。
- 运行时依赖 GPG 和 `python-gnupg`；如果密钥缺失，解密会失败。
- 对初学者稍复杂；解密可能带来轻微性能开销（对密码可忽略）。

这种方法适用于具有自动化部署的团队或跨环境共享配置的情况。

#### 对比表格

| 方面               | 模板 + .gitignore + 手动 | GPG 加密 + 运行时解密 |
|--------------------|--------------------------|----------------------|
| **安全性**        | 如果手动步骤谨慎则高；存在人为错误风险。 | 高；密钥从不以明文形式存在。 |
| **设置简便性**    | 非常容易（无需工具）。   | 中等（GPG + 库）。   |
| **版本控制**      | 模板已提交；真实文件被忽略。 | 完整配置已提交（加密）。 |
| **部署**          | 每个服务器手动操作（例如 SCP）。 | 自动化（需要密钥同步）。 |
| **开销**          | 无。                     | 轻微（加载时解密）。  |
| **最适合**        | 小型/手动项目。          | 自动化/CI/CD 流水线。 |

#### 建议

- 如果项目简单或团队较小，从**方法一**开始——它久经考验。
- 为扩展规模切换到**方法二**（或演进到环境变量/密钥管理器，如 AWS SSM/HashiCorp Vault）。
- 始终结合环境变量进行覆盖（例如 `os.getenv('DB_PASSWORD', db_password)`）。
- 在 UAT 之前，在预发布环境中测试解密。

如果您分享更多细节（例如您的部署工具或完整配置），我可以优化代码！
