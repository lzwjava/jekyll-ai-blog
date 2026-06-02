---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 电报的安全开源策略
translated: true
type: note
---

以下是 Telegram 安全开源其代码的完整解析：

---

## 1. API 密钥 — 有意提交至仓库

Telegram API ID 和哈希值**故意设为公开**，直接保存在仓库中：

```json
// build-system/appstore-configuration.json
{
    "bundle_id": "ph.telegra.Telegraph",
    "api_id": "8",
    "api_hash": "7245de8e747a0d6fbe11f7cc14fcc0bb",
    "team_id": "C67CF9S4VU",
    "appstore_id": "686449807"
}
```

同样也存在于示例 Bazel 配置中：

```python
// build-system/example-configuration/variables.bzl
telegram_api_id = "8"
telegram_api_hash = "7245de8e747a0d6fbe11f7cc14fcc0bb"
```

**为何安全：** Telegram 的 API 采用挑战-响应协议（MTProto）。`api_id` 和 `api_hash` 是公共标识符——它们向 Telegram 服务器标识你的应用，类似于客户端 ID，并非用于身份验证。身份验证通过手机号 + 短信验证码 + MTProto 密钥交换完成。所有第三方 Telegram 客户端（Pyrogram、Telethon 等）都使用相同的值。甚至有一个其他客户端的 [公开密钥列表](https://github.com/nicegram/nicegram-ios/blob/main/Nicegram/Nicegram-API-Keys.plist)。

第三方开发者的模板使用占位符：

```json
// build-system/template_minimal_development_configuration.json
{
    "api_id": "{! 请前往 https://my.telegram.org/apps 获取 !}",
    "api_hash": "{! 请前往 https://my.telegram.org/apps 获取 !}",
    "team_id": "{! 请查阅 README.md !}"
}
```

---

## 2. 代码签名 — 加密 Git 仓库 + 环境密码

这是真正的密钥管理机制。配置文件描述文件和证书存储在一个**独立的私有 Git 仓库**（即 "fastlane match" 仓库）中，并使用 AES-256 加密。

构建系统在构建时获取并解密它们：

```python
# build-system/Make/Make.py 第 422 行
password = os.getenv('TELEGRAM_CODESIGNING_GIT_PASSWORD')
if password is None:
    print('TELEGRAM_CODESIGNING_GIT_PASSWORD 环境变量未设置')
    sys.exit(1)

private_key = os.getenv('TELEGRAM_CODESIGNING_PRIVATE_KEY')

profile_source = GitCodesigningSource(
    repo_url=arguments.gitCodesigningRepository,  # 例如 git@gitlab.com:peter-iakovlev/fastlanematch.git
    private_key=private_key,
    team_id=build_configuration.team_id,
    bundle_id=build_configuration.bundle_id,
    codesigning_type=arguments.gitCodesigningType,  # development, adhoc, appstore, enterprise
    password=password,
    always_fetch=not arguments.gitCodesigningUseCurrent
)
```

加密仓库被克隆后，每个 `.mobileprovision`、`.cer` 和 `.p12` 文件都会被解密：

```python
# build-system/Make/BuildConfiguration.py
def decrypt_codesigning_directory_recursively(source_base_path, destination_base_path, password):
    for file_name in os.listdir(source_base_path):
        source_path = source_base_path + '/' + file_name
        destination_path = destination_base_path + '/' + file_name
        allowed_file_extensions = ['.mobileprovision', '.cer', '.p12']
        if os.path.isfile(source_path) and any(source_path.endswith(ext) for ext in allowed_file_extensions):
            decrypt_match_data(source_path, destination_path, password)
        elif os.path.isdir(source_path):
            os.makedirs(destination_path, exist_ok=True)
            decrypt_codesigning_directory_recursively(source_path, destination_path, password)
```

---

## 3. 自定义 AES-256-GCM 解密（无 OpenSSL 依赖）

他们用纯 Python 编写了自己的 AES-256 实现来解密代码签名数据——同时支持 V1（AES-CBC，OpenSSL 遗留格式）和 V2（AES-GCM，fastlane match 现代格式）：

```python
# build-system/Make/DecryptMatch.py
_V1_PREFIX = b"Salted__"
_V2_PREFIX = b"match_encrypted_v2__"

def _decrypt_stored(stored_data, password):
    if stored_data.startswith(_V2_PREFIX):
        salt = stored_data[20:28]
        auth_tag = stored_data[28:44]
        ciphertext = stored_data[44:]
        material = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            10_000,                    # 10k PBKDF2 迭代次数
            dklen=32 + 12 + 24,       # 256位密钥 + 96位IV + 192位AAD
        )
        key = material[0:32]
        iv = material[32:44]
        aad = material[44:68]
        return _aes_gcm_decrypt(ciphertext, key, iv, aad, auth_tag)

    if stored_data.startswith(_V1_PREFIX):
        salt = stored_data[8:16]
        ciphertext = stored_data[16:]
        key, iv = _evp_bytes_to_key(password, salt, 'md5', 32, 16)
        return _aes_cbc_decrypt(ciphertext, key, iv)
```

V2 使用 PBKDF2-HMAC-SHA256 进行密钥派生（迭代次数 10,000 次），然后使用 AES-256-GCM 进行认证加密。GCM 认证标签可防止篡改。

---

## 4. 构建变量注入 — 构建时生成的 Bazel `variables.bzl`

配置 JSON 由 `BuildConfiguration.py` 解析并写入 Bazel `.bzl` 文件，该文件**在构建时生成，不提交到仓库**：

```python
# build-system/Make/BuildConfiguration.py
def write_to_variables_file(self, bazel_path, use_xcode_managed_codesigning, aps_environment, path):
    string = ''
    string += 'telegram_api_id = "{}"\n'.format(self.api_id)
    string += 'telegram_api_hash = "{}"\n'.format(self.api_hash)
    string += 'telegram_team_id = "{}"\n'.format(self.team_id)
    string += 'telegram_is_internal_build = "{}"\n'.format(self.is_internal_build)
    # ... 写入 Bazel 导入的文件
```

然后 BUILD 文件将这些值作为**编译器标志**（而非运行时值）注入：

```python
# submodules/BuildConfig/BUILD
load("@build_configuration//:variables.bzl", "telegram_api_id", "telegram_api_hash", ...)

objc_library(
    name = "BuildConfig",
    copts = [
        "-DAPP_CONFIG_API_ID={}".format(telegram_api_id),
        "-DAPP_CONFIG_API_HASH=\\\"{}\\\"".format(telegram_api_hash),
        "-DAPP_CONFIG_IS_INTERNAL_BUILD={}".format(telegram_is_internal_build),
        "-DAPP_CONFIG_IS_APPSTORE_BUILD={}".format(telegram_is_appstore_build),
    ],
)
```

API 哈希值在编译时以 C 字符串字面量的形式嵌入到二进制文件中——运行时不会从文件读取。

---

## 5. 三种代码签名来源 — 任选路径

构建系统支持三种方式提供签名身份：

```python
# build-system/Make/Make.py
if arguments.gitCodesigningRepository is not None:
    # 路径 A：加密的 Git 仓库（Telegram 内部 CI）
    profile_source = GitCodesigningSource(...)
elif arguments.codesigningInformationPath is not None:
    # 路径 B：本地目录（开发者自己的证书）
    profile_source = DirectoryCodesigningSource(...)
elif arguments.xcodeManagedCodesigning:
    # 路径 C：Xcode 自动签名（最简单，适合模拟器/开发）
    profile_source = XcodeManagedCodesigningSource()
```

路径 A 是 Telegram 内部使用的方式——即加密的 `fastlanematch` 仓库。路径 B 适用于拥有自己 Apple Developer 证书的开发者。路径 C 适用于仅模拟器构建（无需签名）。

对于仅模拟器构建，可以完全跳过代码签名：

```sh
python3 build-system/Make/Make.py --overrideXcodeVersion \
    generateProject \
    --configurationPath=build-system/template_minimal_development_configuration.json \
    --disableProvisioningProfiles    # <-- 此标志
```

---

## 6. 环境变量 — 实际的机密信息

唯一真正的机密信息是：

| 机密信息 | 存放位置 | 保护对象 |
|---------|---------|---------|
| `TELEGRAM_CODESIGNING_GIT_PASSWORD` | `~/.zshrc`（开发者机器） | 解密代码签名仓库 |
| `TELEGRAM_CODESIGNING_PRIVATE_KEY` | 环境变量（CI） | 代码签名仓库的 SSH 密钥 |
| Apple Developer 证书（`.p12`） | 加密存储在代码签名仓库中 | 代码签名身份 |
| 配置文件描述文件（`.mobileprovision`） | 加密存储在代码签名仓库中 | 应用分发授权 |

这些信息均不在开源仓库中。`.gitignore` 甚至无需列出它们，因为它们位于完全独立的仓库中。

---

## 7. `build-input/` 目录 — 生成而非提交

`build-input/` 目录被列入 `.gitignore`：

```
build-input/*
```

这是构建系统写入以下内容的目录：

- `build-input/data/variables.bzl` — 从配置 JSON 生成
- `build-input/configuration-repository-workdir/` — 克隆并解密的代码签名仓库

该目录是临时性的——每次构建时全新生成，从不提交。

---

## 总结：安全模型

```
┌─────────────────────────────────────────────────────────┐
│  开源仓库（Telegram-iOS）                                │
│                                                         │
│  ✅ api_id, api_hash — 公开，有意为之                    │
│  ✅ 所有源代码 — 开源                                    │
│  ✅ 构建系统（Bazel, Make.py）— 开源                    │
│  ✅ AES 解密代码 — 开源                                  │
│  ✅ 带占位符的模板配置                                    │
│  ❌ 无签名证书，无配置文件描述文件                        │
│  ❌ 无密码，无 SSH 密钥                                  │
│  ❌ 无 build-input/ 目录                                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  私有仓库（fastlanematch）                               │
│                                                         │
│  🔒 加密的 .mobileprovision 文件（AES-256-GCM）          │
│  🔒 加密的 .p12 证书                                     │
│  🔒 加密的 .cer 文件                                      │
│  🔒 仅通过 TELEGRAM_CODESIGNING_GIT_PWD 解密            │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  开发者机器 / CI                                         │
│                                                         │
│  🔑 ~/.zshrc 中的 TELEGRAM_CODESIGNING_GIT_PASSWORD      │
│  🔑 TELEGRAM_CODESIGNING_PRIVATE_KEY（SSH 密钥）          │
│  🔑 Apple Developer 账号                                 │
└─────────────────────────────────────────────────────────┘
```

核心要点：**代码可以安全开源，因为机密信息不在代码中**。API 密钥按协议设计为公开。签名证书位于独立的加密仓库中。解密密码保存在开发者的 shell 环境中。构建系统在构建时协调这一切，生成永不提交的临时文件。
