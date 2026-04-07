---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 强制 npm 使用新注册表
translated: true
type: note
---

问题：`npm --cache <dir> --prefer-online` 如何工作？如果 `package-lock.json` 中有指向旧注册表的陈旧 `resolved` 网址，如何强制 npm 使用新注册表？为什么指定 `--registry` 有时无效，npm 仍会使用旧注册表？

回答：

这是团队切换私有注册表（Artifactory、Nexus、Verdaccio 等）时常遇到的痛点。我们来全面拆解一下。

---

## 1. `--cache <dir>` 的工作原理

`--cache <dir>` 标志会覆盖 npm 存储本地内容寻址缓存的位置（默认值：Unix 系统为 `~/.npm`，Windows 系统为 `%AppData%\npm-cache`）。

```bash
npm install --cache /tmp/my-cache
```

npm 缓存存储以下内容：
- **包压缩包**（`.tgz` 文件），以内容哈希（SHA-512）作为键
- **包元数据**（版本信息、依赖树）

缓存采用**内容寻址**机制，这意味着文件是以其完整性哈希作为键值，而非 URL 或注册表名称。这一点很重要：如果同一个包在新旧注册表中具有相同的哈希值，npm 可能会直接从缓存提供该包，而不会联系新注册表。

---

## 2. `--prefer-online` 的工作原理

`--prefer-online` 会强制 npm 重新验证缓存数据（使用 HTTP 304 检查），忽略任何陈旧性检查，并用重新验证后的最新数据刷新缓存。

相比之下：
- `--prefer-offline` 让 npm 跳过对陈旧缓存数据的条件请求（304 检查），仅当缓存中缺少某些内容时才访问网络。
- `--offline` 强制 npm 仅使用缓存，如果缓存中缺少任何内容，则会报错 `ENOTCACHED` 并退出。

因此，`--prefer-online` 是最“新鲜”的模式——即使数据已缓存，它也始终会访问网络进行验证。

当使用 `--prefer-online` 且没有 `package-lock.json` 并连接公共注册表时，可能会产生大量 HTTP 请求（典型项目约为 2,800 个），因为 npm 会同时获取最新的元数据和包内容。

**组合使用示例：**
```bash
npm install --cache /my/cache/dir --prefer-online
```
这会使用自定义缓存目录，但仍在线重新验证所有内容。在 CI 流水线中非常有用，因为你希望共享缓存目录，同时又始终保持最新的依赖解析。

---

## 3. 为什么 `--registry` 无效——`resolved` 字段问题

这是核心问题。当你运行 `npm install` 时，**npm 会先读取 `package-lock.json`**，其中每个包条目都包含一个固化的 `resolved` 字段：

```json
{
  "lodash": {
    "version": "4.17.21",
    "resolved": "https://old-registry.company.com/lodash/-/lodash-4.17.21.tgz",
    "integrity": "sha512-xxxx"
  }
}
```

即使指定了 `--registry <URL>`，现有的锁文件仍可能覆盖此设置，npm 会使用 `resolved` 路径作为包的来源。具体行为取决于 npm 客户端的版本。

这在 npm 文档中有明确说明：“如果包存在 `package-lock`、`npm-shrinkwrap` 文件或 yarn lock 文件，依赖项的安装将由这些文件驱动。”

因此，**命令行中的 `--registry` 会输给 `package-lock.json` 中的 `resolved` 网址**。锁文件的优先级更高。

---

## 4. 如何强制 npm 使用新注册表

### 方案 A — 删除并重新生成锁文件（推荐）

用户在使用新注册表时，应删除现有锁文件并生成新锁文件。记得将新的和更新后的锁文件提交到项目仓库。

```bash
# 设置新注册表
npm config set registry https://new-registry.company.com

# 删除旧锁文件
rm package-lock.json

# 重新安装——新锁文件将使用新注册表
npm install
```

**缺点：** 这可能会改变传递依赖的版本，因为 npm 会从头开始重新解析所有依赖。

### 方案 B — 在 `package-lock.json` 中查找并替换

如果你想保持版本锁定，仅切换注册表网址：

```bash
# 在 Linux/Mac 上
sed -i 's|https://old-registry.company.com|https://new-registry.company.com|g' package-lock.json

# 然后安装
npm install
```

当需要更改注册表而不改变版本或完整性哈希时，查找并替换可能是最安全、最一致的解决方案——版本和完整性字段保持完全一致，仅 `resolved` 字段被更改。

### 方案 C — 使用 `.npmrc` 进行持久性注册表配置

在项目根目录创建或更新 `.npmrc`：

```ini
registry=https://new-registry.company.com
# 对于作用域包：
@myorg:registry=https://new-registry.company.com
```

对于不同的包使用不同的注册表，可使用作用域特定的注册表设置：`npm config set @myscope:registry=https://myownregist.ry/packages/`

### 方案 D — npm 5+ 自动切换（有限）

从 npm 5 开始，如果你的 `package-lock.json` 是针对注册表 A 生成的，而你将注册表切换到 B，npm 会尝试从注册表 B 安装包——但这仅适用于*非作用域*包，并且不再支持为非作用域包设置不同的注册表。

---

## 5. 总结：优先级顺序（优先级高的胜出）

| 优先级（高→低） | 来源 |
|----------|--------|
| 1（最高） | `package-lock.json` 中的 `resolved` 网址 |
| 2 | 项目目录中的 `.npmrc` |
| 3 | `--registry` 命令行标志 |
| 4 | `~/.npmrc` 用户配置 |
| 5（最低） | npm 全局配置 |

---

## 6. 常见故障排除清单

```bash
# 检查 npm 当前识别的注册表
npm config get registry

# 检查所有配置来源及其应用情况
npm config list

# 完全清除 npm 缓存（强制重新下载）
npm cache clean --force

# 然后使用显式注册表和 prefer-online 重新安装
npm install --registry https://new-registry.company.com --prefer-online

# 如果问题依旧：删除锁文件和 node_modules
rm -rf node_modules package-lock.json
npm install --registry https://new-registry.company.com
```

---

## 关键要点

`--registry` 似乎被“忽略”的最常见原因是：**`package-lock.json` 中硬编码的 `resolved` 网址在运行时覆盖了你的注册表标志**。锁文件是关于包来源的权威来源。要真正切换注册表，你必须要么重新生成锁文件，要么对其中的 `resolved` 字段值进行批量查找并替换。

参考资料：

- [npm v5.0.0 发布博客 — prefer-online、prefer-offline、offline 标志详解](https://blog.npmjs.org/post/161081169345/v500)
- [Bytesafe 文档 — 缺失包 / lockfile resolved 字段覆盖注册表](https://docs.bytesafe.dev/troubleshooting/missing-packages/)
- [npm/npm GitHub Issue #19578 — 更改注册表后 package-lock.json resolved 字段未更新](https://github.com/npm/npm/issues/19578)
- [npm 官方文档 — 包锁](https://docs.npmjs.com/cli/v6/configuring-npm/package-locks/)
- [npm 官方文档 — 配置参考（prefer-online、prefer-offline、cache）](https://docs.npmjs.com/cli/v6/using-npm/config/)
- [DEV 社区 — 解密 npm 包安装（prefer-online 深度解析）](https://dev.to/pavel-zeman/demystifying-npm-package-installation-insights-analysis-and-optimization-tips-4nmj)