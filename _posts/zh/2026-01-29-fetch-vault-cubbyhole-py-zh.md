---
audio: false
generated: true
image: false
lang: zh
layout: post
model: google/gemini-3-flash-preview
title: 使用 Python 获取 Vault Cubbyhole 密钥
translated: true
type: note
---

问题：如何使用 Python 通过带有证书和特定 namespace 的 HTTPS 从 HashiCorp Vault cubbyhole 获取 secrets？

回答：在 Python 中与 HashiCorp Vault 交互，标准的库选择是 `hvac`。**cubbyhole** 后端非常独特，因为它的作用域仅限于特定的 token；存储在那里的 secrets 仅对创建它们的 token 可见，并在该 token 过期时被删除。

### Prerequisites

如果您尚未安装 `hvac` 库，则需要进行安装：

```bash
pip install hvac
```

### Python Implementation

以下示例演示了如何使用 SSL 验证初始化 client，设置自定义 namespace，并从 cubbyhole 读取 secret。

```python
import hvac

# Configuration Details
vault_url = 'https://your-vault-cluster:8200'
vault_token = 'your-vault-token'
vault_namespace = 'admin/my-project'  # Specify your namespace
cert_path = '/path/to/ca_bundle.crt'   # Path to your CA certificate

def fetch_cubbyhole_secret(path):
    # 1. Initialize the client
    # verify=cert_path 确保 HTTPS 使用您指定的 certificate
    # namespace 允许您定位隔离的 Vault 环境
    client = hvac.Client(
        url=vault_url,
        token=vault_token,
        namespace=vault_namespace,
        verify=cert_path
    )

    # 2. Check if the client is authenticated
    if not client.is_authenticated():
        raise Exception("Vault authentication failed.")

    # 3. Read from the cubbyhole
    # cubbyhole 始终位于 'cubbyhole/' 挂载点
    read_response = client.secrets.cubbyhole.read_secret(path=path)

    # 4. Extract data
    secret_data = read_response['data']
    return secret_data

# Example Usage
try:
    # 这将获取 'https://.../v1/cubbyhole/my-app-secrets'
    secrets = fetch_cubbyhole_secret(path='my-app-secrets')
    print("Fetched Secrets:", secrets)
except Exception as e:
    print(f"Error: {e}")
```

---

### Key Considerations

* **Namespace:** 在 Vault Enterprise 中，namespaces 是层级结构的。请确保提供完整路径（例如 `parent/child`）。
* **SSL Verification:** 设置 `verify=cert_path` 是处理自签名或内部 CA certificates 的安全方式。在测试时可以设置 `verify=False`，但在生产环境中极不推荐，因为它会禁用 SSL 加密检查。
* **Cubbyhole Lifetime:** 请记住，cubbyhole secrets 是与 **token** 绑定的。如果您运行此脚本时使用的 token 与写入 secret 时使用的 token 不同，则无法找到该 secret。

您是否需要我向您展示如何先使用相同的配置向 cubbyhole 写入 secret？

References:

* [hvac Documentation - Cubbyhole](https://www.google.com/search?q=https://hvac.readthedocs.io/en/stable/usage/secrets_engines/cubbyhole.html)
* [HashiCorp Vault - Cubbyhole Secrets Engine](https://developer.hashicorp.com/vault/docs/secrets/cubbyhole)
