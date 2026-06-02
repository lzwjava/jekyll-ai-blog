---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 安装IBM DB2驱动程序DLLs
translated: true
type: note
---

问：在 Windows 中使用 IBM DB2 包时，我需要添加所有 DB2 驱动程序 DLL 吗？如何操作？

答：

用于连接 IBM DB2 的 Python 包名为 `ibm_db`（通常称为“ibm_db”或 IBM DB2 包）。它需要 IBM DB2 CLI/ODBC 驱动程序 (clidriver) 才能运行，因为它依赖于驱动程序的 DLL（例如 `db2cli.dll` 及其他文件）。

### 推荐的现代方法（适用于最新版本，最简单）

最新版本的 `ibm_db`（PyPI 上的 wheels）包含一个捆绑的轻量级 clidriver，其中包含所有必需的 DLL。

- 只需运行：
  `pip install ibm_db`

这会自动将驱动程序 DLL 安装到您的 Python site-packages 目录中（通常在 `site-packages\clidriver\bin` 下）。

通常不需要手动添加到 PATH，因为软件包会处理捆绑驱动程序的加载。如果遇到“DLL load failed”错误：

- 如果使用 64 位设置，请确保您的 Python 也是 64 位（通过 `python -c "import struct; print(struct.calcsize('P') * 8)"` 检查——应该输出 64）。
- 安装后重新启动您的 IDE 或命令提示符。

### 如果使用外部或单独的 DB2 驱动程序

如果您单独安装了 IBM Data Server Driver for ODBC and CLI（或需要特定版本）：

1. 从 IBM Fix Central 下载驱动程序 ZIP 文件（例如，适用于 64 位 Windows 的 `ntx64_odbc_cli.zip`）：
   搜索“IBM Data Server Driver for ODBC and CLI”（免费用于 DB2 LUW 连接）。

2. 将 ZIP 文件解压到一个文件夹，例如 `C:\Program Files\IBM\clidriver`。

3. 将 `bin` 文件夹添加到您的系统 PATH 环境变量中：
   - 右键单击“此电脑”>“属性”>“高级系统设置”>“环境变量”。
   - 在“系统变量”下，编辑 PATH 并添加：`C:\Program Files\IBM\clidriver\bin`（根据需要调整路径）。
   - 如果从源代码编译，还要添加 `lib` 文件夹。

4. （可选）在 ODBC 管理器中注册驱动程序：
   打开管理员命令提示符，导航到 `bin` 文件夹，然后运行：
   `db2cli install -setup`

5. 然后通过 pip 安装 `ibm_db`（如果 `IBM_DB_HOME` 设置为 clidriver 根目录，它将检测并使用外部驱动程序）。

这确保了所有必需的 DLL 都可以访问。

参考资料：

- [ibm_db PyPI 页面](https://pypi.org/project/ibm-db/)
- [IBM DB2 ODBC CLI Driver 下载和安装](https://www.ibm.com/support/pages/db2-odbc-cli-driver-download-and-installation-information)
- [如何安装和配置 DB2 ODBC 驱动程序](https://www.ryslander.com/how-to-install-and-configure-db2-odbc-driver/)
- [GitHub ibm_db 仓库 README](https://github.com/ibmdb/python-ibmdb/blob/master/README.md)
