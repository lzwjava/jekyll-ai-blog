---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 用于下载 Nexus NPM 包的 Python 脚本
translated: true
type: note
---

这是一个用于从你的内部 Nexus registry 下载 npm package 的 Python 脚本：

```python
import os
import requests
import sys
import json

def download_npm_package(registry_url, package_name, version=None, output_dir="."):
    """
    从内部 Nexus registry 下载 npm package。

    Args:
        registry_url: Nexus npm registry 的基础 URL (例如：https://company.com/npm/group)
        package_name: package 名称 (例如：'lodash' 或 '@scope/package-name')
        version: 指定下载的版本 (可选，默认为 latest)
        output_dir: 保存下载 package 的目录
    """

    # 从环境变量获取 auth token
    auth_token = os.getenv('NPM_AUTH_TOKEN')
    if not auth_token:
        print("Error: NPM_AUTH_TOKEN environment variable not set")
        sys.exit(1)

    # 设置带有 authentication 的 headers
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Accept': 'application/json'
    }

    # 构建 package metadata URL
    # 处理 scoped packages (例如：@scope/package-name)
    encoded_package_name = package_name.replace('/', '%2F')
    metadata_url = f"{registry_url.rstrip('/')}/{encoded_package_name}"

    try:
        # 获取 package metadata
        print(f"Fetching package metadata for {package_name}...")
        response = requests.get(metadata_url, headers=headers)
        response.raise_for_status()

        metadata = response.json()

        # 确定下载哪个版本
        if version is None:
            version = metadata.get('dist-tags', {}).get('latest')
            if not version:
                print("Error: Could not determine latest version")
                sys.exit(1)
            print(f"Latest version: {version}")

        # 获取指定版本的 tarball URL
        if version not in metadata.get('versions', {}):
            print(f"Error: Version {version} not found")
            print(f"Available versions: {list(metadata.get('versions', {}).keys())}")
            sys.exit(1)

        tarball_url = metadata['versions'][version]['dist']['tarball']

        # 下载 tarball
        print(f"Downloading {package_name}@{version}...")
        tarball_response = requests.get(tarball_url, headers=headers, stream=True)
        tarball_response.raise_for_status()

        # 保存 tarball
        os.makedirs(output_dir, exist_ok=True)
        safe_package_name = package_name.replace('@', '').replace('/', '-')
        output_file = os.path.join(output_dir, f"{safe_package_name}-{version}.tgz")

        with open(output_file, 'wb') as f:
            for chunk in tarball_response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Successfully downloaded to {output_file}")
        return output_file

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {e.response.text}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # 示例用法
    REGISTRY_URL = "https://company.com/npm/group"

    # 示例：下载指定 package
    # download_npm_package(REGISTRY_URL, "lodash", version="4.17.21")

    # 示例：下载最新版本
    # download_npm_package(REGISTRY_URL, "express")

    # 示例：下载 scoped package
    # download_npm_package(REGISTRY_URL, "@babel/core", version="7.23.0")

    # 交互模式
    if len(sys.argv) < 2:
        print("Usage: python script.py <package-name> [version]")
        print("Example: python script.py lodash 4.17.21")
        print("Example: python script.py @babel/core")
        sys.exit(1)

    package = sys.argv[1]
    ver = sys.argv[2] if len(sys.argv) > 2 else None

    download_npm_package(REGISTRY_URL, package, version=ver)
```

**用法：**

1. **设置你的 auth token：**

   ```bash
   export NPM_AUTH_TOKEN="your-token-here"
   ```

2. **运行脚本：**

   ```bash
   # 下载最新版本
   python script.py lodash

   # 下载指定版本
   python script.py lodash 4.17.21

   # 下载 scoped package
   python script.py @babel/core 7.23.0
   ```

**主要特性：**

- 使用 `NPM_AUTH_TOKEN` 环境变量进行 authentication
- 支持普通 package 和 scoped packages
- 默认下载最新版本，或根据提供的值下载指定版本
- 使用清晰的文件名保存 `.tgz` 文件
- 包含错误处理和进度提示消息
- 高效地以流式方式 (stream) 下载大文件

**注意：** 某些 Nexus 配置可能使用 `_auth` (base64) 而不是 bearer tokens。如果你的环境使用 basic auth，请将 headers 修改为：

```python
headers = {
    'Authorization': f'Basic {auth_token}',  # token 应该是 base64 编码的
    'Accept': 'application/json'
}
```
