---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 使用自定义主目录的GPG
translated: true
type: note
---

### 使用 GPG 的 `--homedir` 选项

`--homedir` 标志（注意：是 `--homedir` 而非 `--home-dir`——GPG 使用单个单词）指示 GPG 使用自定义目录作为其“主目录”，用于存储配置文件、密钥环、信任数据库和其他数据。默认情况下，GPG 使用 `~/.gnupg`（例如在 Windows 的 Git Bash 中为 `/c/Users/YourName/.gnupg`）。此选项适用于以下场景：
- 隔离多个 GPG 设置（例如，一个用于个人密钥，另一个用于工作密钥）。
- 测试或避免与系统级 GPG 配置冲突。
- 在便携或自定义环境中运行 GPG。

#### 基础语法
```
gpg --homedir /path/to/custom/dir [其他 gpg 命令]
```
- 将 `/path/to/custom/dir` 替换为您的目标目录路径。
- 在 Windows 的 Git Bash 中，**请始终使用正斜杠 (`/`)** 作为路径分隔符，即使是 Windows 驱动器路径（例如 `/c/Users/YourName/my-gpg-dir`）。
- 目录必须已存在；GPG 不会自动创建该目录。请先使用 `mkdir -p /path/to/custom/dir` 创建目录。

#### 示例：设置并使用自定义主目录
1. **创建自定义目录**（在 Git Bash 中）：
   ```
   mkdir -p /c/Users/YourName/my-custom-gpg
   ```

2. **使用自定义 homedir 生成密钥对**：
   ```
   gpg --homedir /c/Users/YourName/my-custom-gpg --full-generate-key
   ```
   - 这会将您的密钥和配置存储在 `my-custom-gpg` 中，而非默认目录。

3. **列出该目录中的密钥**：
   ```
   gpg --homedir /c/Users/YourName/my-custom-gpg --list-secret-keys --keyid-format LONG
   ```

4. **使用自定义目录中的密钥加密文件**：
   ```
   gpg --homedir /c/Users/YourName/my-custom-gpg --encrypt --recipient RECIPIENT_EMAIL secret.txt
   ```

5. **解密文件**：
   ```
   gpg --homedir /c/Users/YourName/my-custom-gpg --output decrypted.txt --decrypt secret.txt.gpg
   ```

#### Git Bash on Windows 使用技巧
- **路径规范：** 坚持使用 `/`——避免使用 `\` 或混合斜杠，因为它们可能导致命令执行失败。
- **权限设置：** 确保自定义目录具有读写权限（建议使用 `chmod 700 /path/to/custom/dir` 设置安全权限，与默认 `.gnupg` 目录保持一致）。
- **环境变量替代方案：** 无需每次使用 `--homedir`，可在 `.bashrc` 中设置 `export GNUPGHOME=/c/Users/YourName/my-custom-gpg`（编辑后运行 `source ~/.bashrc`）。之后 GPG 将自动使用该路径。
- **Git 集成：** 若用于 Git 签名，可通过以下命令配置：
  ```
  git config --global gpg.program "gpg --homedir /c/Users/YourName/my-custom-gpg"
  ```
- **常见问题：** 若 GPG 提示缺少文件，可能需要先执行初始化——运行 `gpg --homedir /path --gen-key`。在 Windows 系统中，除非使用引号包裹，否则请避免包含空格的路径。

完整说明请参阅 GPG 手册：[GnuPG Documentation](https://www.gnupg.org/documentation/manuals/gnupg/)
