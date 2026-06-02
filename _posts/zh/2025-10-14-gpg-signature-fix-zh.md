---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 修复GPG签名验证错误
translated: true
type: note
---

### 理解错误原因

出现该错误是因为 `gpg --verify` 命令通常需要两个参数：首先是**签名文件**（如 `zhs.tw.yaml.sig` 或 `zhs.tw.yaml.asc`），其次是要验证的**实际文件**（如 `zhs.tw.yaml`）。

在您使用的命令中：
```
gpg --verify zhs.tw.yaml
```
GPG 试图将 `zhs.tw.yaml` 同时解释为签名文件和数据文件，但该文件并不包含有效的 OpenPGP 签名数据（YAML 文件本身不是签名文件），因此会出现“未找到有效 OpenPGP 数据”的提示。

### 解决方案

1. **定位签名文件**：需要找到与 YAML 文件匹配的独立签名文件，通常命名格式为：
   - `zhs.tw.yaml.sig`（二进制格式）
   - `zhs.tw.yaml.asc`（ASCII 编码格式）

   如果尚未获取该文件，需从下载 `zhs.tw.yaml` 的源头（如项目仓库或网站）同步下载。

2. **执行正确命令**：获得签名文件后使用以下格式：
   ```
   gpg --verify zhs.tw.yaml.sig zhs.tw.yaml
   ```
   - 若签名文件为 `.asc` 格式请相应替换
   - 参数顺序至关重要：签名文件在前，被验证文件在后

3. **验证成功时的预期输出**：
   当签名有效且已信任对应密钥时，将显示：
   ```
   gpg: 于 [日期] 使用 [密钥类型] 创建签名
   gpg: 来自“[签名者名称/邮箱]”的完好签名
   ```
   若签名无效或未信任密钥，则会显示警告/错误信息

### 补充建议

- **导入公钥**：若 GPG 提示未知密钥，请获取并导入签名者的公钥：
  ```
  gpg --keyserver keyserver.ubuntu.com --recv-keys [密钥ID]
  ```
  （将 `[密钥ID]` 替换为错误输出或项目文档中的实际密钥指纹）

- **脚本批处理模式**：自动化验证时可添加 `--batch` 参数禁用提示：
  ```
  gpg --batch --verify zhs.tw.yaml.sig zhs.tw.yaml
  ```

- **内联签名**：若签名直接嵌入 YAML 文件（对于 `.yaml` 文件较罕见），需确保文件以 `-----END PGP SIGNATURE-----` 结尾，然后直接执行 `gpg --verify zhs.tw.yaml`。但根据错误提示，当前应为独立签名模式。

若问题仍未解决，提供更多背景信息（如文件来源）可获得更精准的指导！

[GNU Privacy Guard 手册](https://www.gnupg.org/documentation/manpage.html)
