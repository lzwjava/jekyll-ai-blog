---
audio: false
generated: true
lang: zh
layout: post
title: 缺少psycopg2所需的libpq-fe.h头文件
translated: true
type: note
---

在尝试安装 Python 包 `psycopg2` 时，您遇到了一个错误，提示无法成功构建 wheel。错误信息的关键部分是：

```
In file included from psycopg/adapter_asis.c:28:
./psycopg/psycopg.h:36:10: fatal error: libpq-fe.h: No such file or directory
   36 | #include <libpq-fe.h>
      |          ^~~~~~~~~~~~
compilation terminated.
```

出现此错误是因为系统中缺少 PostgreSQL 客户端库的头文件 `libpq-fe.h`。`psycopg2` 包需要此文件才能从源代码构建，因为它提供了 Python 连接到 PostgreSQL 数据库的接口。下面，我将解释为什么会发生这种情况，并提供逐步解决方案来修复它。

---

### 错误原因
`psycopg2` 包是 Python 的 PostgreSQL 适配器，当您使用 `pip` 安装它时，它会尝试编译其 C 扩展。这些扩展依赖于 PostgreSQL 客户端库，特别是开发头文件，如 `libpq-fe.h`。错误信息证实了这一点：

```
It appears you are missing some prerequisite to build the package from source.
```

您的系统（根据使用的 `x86_64-linux-gnu-gcc` 判断，似乎是基于 Debian 的 Linux 发行版）缺少必要的 PostgreSQL 开发文件。没有这些文件，编译就会失败，导致无法为 `psycopg2` 构建 wheel。

错误还建议了两个选项：
1. 通过 PyPI 安装预构建的二进制包 `psycopg2-binary`。
2. 安装缺少的必备组件并从源代码构建 `psycopg2`。

由于您的项目在 requirements 文件中指定了 `psycopg2`（而不是 `psycopg2-binary`），并且为了兼容性或自定义可能需要从源代码构建，我们将重点放在修复构建过程上。不过，我稍后也会提到二进制选项以供参考。

---

### 如何修复错误
要解决此问题，您需要安装 PostgreSQL 客户端开发包，它提供了 `libpq-fe.h` 和其他必要的文件。具体操作如下：

#### 步骤 1：识别您的系统
您的构建输出中包含 `x86_64-linux-gnu-gcc`，表明您可能使用的是基于 Debian 的系统，如 Ubuntu。解决方案将针对此系统定制，但我会在后面注明其他发行版的替代方案。

#### 步骤 2：安装 PostgreSQL 开发包
在基于 Debian 的系统（例如 Ubuntu）上，包 `libpq-dev` 包含 PostgreSQL 客户端库的头文件，包括 `libpq-fe.h`。使用以下命令安装它：

```bash
sudo apt-get update
sudo apt-get install libpq-dev
```

- **`sudo apt-get update`**：确保您的软件包列表是最新的。
- **`sudo apt-get install libpq-dev`**：安装 PostgreSQL 客户端库的开发文件。

此包将 `libpq-fe.h` 放置在标准位置（通常是 `/usr/include/postgresql`），构建过程会搜索该位置（如您的包含路径所示：`-I/usr/include/postgresql`）。

#### 步骤 3：重试安装
安装 `libpq-dev` 后，重试安装您的 requirements：

```bash
pip install -r scripts/requirements/requirements.local.txt
```

现在这应该会成功，因为缺少的 `libpq-fe.h` 文件已可用，允许 `psycopg2` 构建其 wheel。

---

### 验证修复
如果安装仍然失败，请检查 PostgreSQL 头文件是否正确安装：
- 运行 `pg_config --includedir` 查看头文件的位置（例如 `/usr/include/postgresql`）。
- 确保这与构建命令中的包含路径（`-I/usr/include/postgresql`）匹配。

您的构建输出显示 `-DPG_VERSION_NUM=140018`，表明它针对的是 PostgreSQL 14。`libpq-dev` 包是版本无关的，应该适用于 PostgreSQL 14 头文件。

---

### 替代方案：使用二进制包
如果您不需要从源代码构建 `psycopg2`（例如，为了特定的优化或兼容性），可以安装预构建的 `psycopg2-binary`：

```bash
pip install psycopg2-binary
```

要在您的项目中使用此包，请将 `scripts/requirements/requirements.local.txt` 中的 `psycopg2` 替换为 `psycopg2-binary`。但请注意，`psycopg2-binary` 可能存在限制（例如，与某些 PostgreSQL 版本的潜在兼容性问题），因此如果您的项目需要，从源代码构建是首选。

---

### 其他发行版
如果您不在基于 Debian 的系统上，请安装等效的包：
- **Red Hat/CentOS/Fedora**：`sudo yum install postgresql-devel` 或 `sudo dnf install postgresql-devel`
- **Arch Linux**：`sudo pacman -S postgresql-libs`
- **macOS（使用 Homebrew）**：`brew install libpq`

然后，重试 `pip install` 命令。

---

### 总结
错误的发生是因为缺少 `libpq-fe.h`，该文件是 PostgreSQL 客户端开发文件的一部分。对于您的基于 Debian 的系统，使用 `sudo apt-get install libpq-dev` 安装 `libpq-dev` 应该可以解决问题。之后，重新运行您的 `pip install` 命令，`psycopg2` 应该能成功构建。如果您希望更快地修复并且不需要源代码编译，请改用 `psycopg2-binary`。
