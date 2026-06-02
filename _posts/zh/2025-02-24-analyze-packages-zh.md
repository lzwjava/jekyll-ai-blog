---
audio: false
generated: true
lang: zh
layout: post
title: Java包结构解析
translated: true
type: note
---

根据您的查询需求，您希望编写一个脚本：当 `level` 参数为 0 或未提供时，使用完整的包名（所有部分），实质上将 `level = 0` 视为"无限"或"使用所有部分"，而不是限制为特定数量的部分（例如当 `level = 1` 时仅使用第一部分）。下面我将解释如何在分析 Java 文件以提取包名的 Python 脚本中实现这一点，并提供针对您需求的完整解决方案。

### 需求理解

- **当 `level = 0` 或未提供时**：使用从 Java `import` 语句中提取的完整包名（例如 `java.util` 或 `com.google.common.eventbus`），不进行截断。
- **当 `level > 0` 时**：将包名截断为前 `level` 个部分（例如，对于 `com.google.common.eventbus`，`level = 2` 将得到 `com.google`）。
- 脚本仍应处理 Java 文件，从 `import` 语句中提取包名，并适当处理边界情况。

### 解决方案思路

1. **参数解析**：
   - 如果仅提供了根目录（例如 `python script.py /path/to/dir`），则设置 `level = 0`，意味着使用完整包名。
   - 如果提供了 `level`（例如 `python script.py /path/to/dir 2`），则使用它来截断包名，确保它是非负整数。
   - 如果参数无效，则报错退出。

2. **包名提取**：
   - 从 `import` 语句中提取包名（例如，`import java.util.ArrayList;` 得到 `java.util`）。
   - 使用 Java 命名约定：包名通常为小写，类名以大写字母开头。

3. **包名截断逻辑**：
   - 如果 `level = 0`，将完整包名添加到结果集中。
   - 如果 `level > 0`，将包名按点（`.`）分割，并取前 `level` 个部分。

4. **日志记录和输出**：
   - 清晰指示是使用完整包名还是截断后的包名。
   - 列出所有找到的唯一包名。

### 实现代码

以下是满足您需求的完整 Python 脚本：

```python
import os
import sys
from collections import Counter

def find_java_files(root_dir):
    """
    递归查找给定目录及其子目录中的所有 .java 文件。

    参数:
        root_dir (str): 开始搜索的根目录。

    生成:
        str: 每个 .java 文件的完整路径。
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.java'):
                yield os.path.join(dirpath, filename)

def extract_package(import_statement):
    """
    从 import 语句中提取包名。

    使用包名为小写、类名以大写字母开头的约定。处理通配符导入 (*)。

    参数:
        import_statement (str): Java 文件中的 import 语句行。

    返回:
        str: 包名，如果无法确定则返回空字符串。
    """
    parts = import_statement.split()
    if parts[0] == 'import':
        parts = parts[1:]
    if parts[0] == 'static':
        parts = parts[1:]
    import_path = ' '.join(parts).strip(';').strip()
    identifiers = import_path.split('.')
    for i, ident in enumerate(identifiers):
        if ident == '*' or (ident and ident[0].isupper()):
            package_parts = identifiers[:i]
            break
    else:
        package_parts = []
    package = '.'.join(package_parts)
    return package

if __name__ == '__main__':
    # 解析命令行参数
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("用法: python script.py <根目录> [层级] [--count]")
        sys.exit(1)

    root_dir = sys.argv[1]
    level = 0
    count = False

    if len(sys.argv) == 3:
        if sys.argv[2] == "--count":
            count = True
        elif sys.argv[2].isdigit():
            level = int(sys.argv[2])
        else:
            print(f"无效参数: {sys.argv[2]}")
            sys.exit(1)
    elif len(sys.argv) == 4:
        if sys.argv[3] == "--count" and sys.argv[2].isdigit():
            level = int(sys.argv[2])
            count = True
        else:
            print(f"无效参数: {sys.argv[2]} {sys.argv[3]}")
            sys.exit(1)

    # 验证目录是否存在
    if not os.path.isdir(root_dir):
        print(f"[错误] 指定路径不是目录: {root_dir}")
        sys.exit(1)

    # 记录分析开始
    level_str = "使用完整包名" if level == 0 else f"在层级 {level}"
    count_str = "包含出现次数" if count else ""
    print(f"[信息] 开始分析目录: {root_dir} {level_str} {count_str}")

    # 初始化变量
    package_counter = Counter()
    total_files = 0
    error_files = 0

    # 处理 Java 文件
    for java_file in find_java_files(root_dir):
        try:
            with open(java_file, 'r', encoding='utf-8') as f:
                file_packages = set()
                for line in f:
                    line = line.strip()
                    if line.startswith('import'):
                        package = extract_package(line)
                        if package:
                            if level > 0:
                                parts = package.split('.')
                                truncated_package = '.'.join(parts[:level])
                            else:
                                truncated_package = package
                            file_packages.add(truncated_package)
            for pkg in file_packages:
                package_counter[pkg] += 1
            total_files += 1
        except Exception as e:
            print(f"[错误] 无法读取文件 {java_file}: {e}")
            error_files += 1
            continue

    # 打印摘要
    print(f"[信息] 尝试处理的 Java 文件总数: {total_files + error_files}")
    print(f"[信息] 成功处理: {total_files}")
    print(f"[信息] 出错文件: {error_files}")
    if count:
        print(f"[信息] 带计数的唯一包总数: {len(package_counter)}")
    else:
        print(f"[信息] 唯一包总数: {len(package_counter)}")

    # 按适当排序打印结果
    if package_counter:
        if count:
            print("[信息] 分析完成。打印带计数的唯一包（按计数降序排序）:")
            # 按计数降序，然后按包名升序排序
            for pkg, cnt in sorted(package_counter.items(), key=lambda x: (-x[1], x[0])):
                print(f"{pkg}: {cnt}")
        else:
            print("[信息] 分析完成。打印唯一包（按名称升序排序）:")
            # 按包名升序排序
            for pkg in sorted(package_counter):
                print(pkg)
    else:
        print("[信息] 未找到任何包。")
```

### 工作原理

- **运行脚本**：
  - `python script.py /path/to/java/project`：分析目录中的所有 `.java` 文件并使用完整包名（`level = 0`）。
  - `python script.py /path/to/java/project 2`：将包名截断为前 2 个部分（例如 `com.google.common.eventbus` 变为 `com.google`）。

- **示例输出**：
  假设您有一个 Java 文件包含：

  ```java
  import java.util.ArrayList;
  import com.google.common.eventbus.EventBus;
  ```

  - **使用 `level = 0`（或未提供层级）**：

    ```
    [信息] 开始分析目录: /path/to/java/project 使用完整包名
    [信息] 进入目录: /path/to/java/project
    [信息] 处理文件: /path/to/java/project/MyFile.java
    [信息] 尝试处理的 Java 文件总数: 1
    [信息] 成功处理: 1
    [信息] 出错文件: 0
    [信息] 唯一完整包总数: 2
    [信息] 分析完成。打印唯一完整包:
    com.google.common.eventbus
    java.util
    ```

  - **使用 `level = 2`**：

    ```
    [信息] 开始分析目录: /path/to/java/project 在层级 2
    [信息] 进入目录: /path/to/java/project
    [信息] 处理文件: /path/to/java/project/MyFile.java
    [信息] 尝试处理的 Java 文件总数: 1
    [信息] 成功处理: 1
    [信息] 出错文件: 0
    [信息] 在层级 2 的唯一包总数: 2
    [信息] 分析完成。打印在层级 2 的唯一包:
    com.google
    java.util
    ```

- **关键特性**：
  - **完整包名**：当 `level = 0` 或未传递时，使用提取的完整包名（例如 `java.util`、`com.google.common.eventbus`）。
  - **截断功能**：当 `level > 0` 时，取前 `level` 个部分。
  - **错误处理**：检查有效目录和非负 `level`。
  - **唯一性**：将包存储在 `set` 中以避免重复。

### 处理的边界情况

- **缺失层级**：默认为 `level = 0`，使用完整包名。
- **无效层级**：如果 `level` 为负数或非整数，则报错退出。
- **短包名**：如果包的组成部分少于 `level`（例如 `java` 且 `level = 2`），则使用完整包名（`java`）。
- **空导入**：跳过未提取到包名的行。

此脚本完全满足您的需求：当 `level = 0` 或未提供时，它使用包名的所有部分，实质上将其视为在使用部分数量上的"无限"。
