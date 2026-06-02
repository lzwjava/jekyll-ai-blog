---
audio: false
generated: true
lang: zh
layout: post
title: 分析Java依赖关系
translated: true
type: note
---

针对您的查询，我将修改提供的Python脚本，使其能够生成基于指定包层次"级别"分组的Java类依赖关系图。例如，若`level=1`，则按顶级包分组（如"org"）；若`level=2`，则按第二级包分组（如"org.springframework"）。这意味着在分析依赖关系之前，我们会根据包名前`level`个部分将类归组，最终图表将展示这些组之间的依赖关系，而非单个类之间的依赖。

以下是修改后的脚本，随后是变更说明及如何满足需求的解释。

### 修改后的脚本

```python
import os
import sys
import re
from collections import defaultdict

def get_package(file_path):
    """
    从.java文件中提取包名。

    参数:
        file_path (str): .java文件路径。

    返回:
        str: 包名，未找到则返回None。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.search(r'^\s*package\s+([\w.]+);', line)
                if match:
                    return match.group(1)
    except Exception as e:
        print(f"警告：无法读取 {file_path}：{e}")
    return None

def get_specific_imports(file_path):
    """
    从.java文件中提取具体的类导入（排除通配符导入）。

    参数:
        file_path (str): .java文件路径。

    返回:
        list: 完全限定导入类名列表。
    """
    imports = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.search(r'^\s*import\s+([\w.]+);', line)
                if match:
                    imp = match.group(1)
                    # 排除通配符导入（如import java.util.*;）
                    if not imp.endswith('.*'):
                        imports.append(imp)
    except Exception as e:
        print(f"警告：无法读取 {file_path}：{e}")
    return imports

def get_package_group(full_class_name, level):
    """
    根据包名前'level'个部分获取包分组。

    参数:
        full_class_name (str): 完全限定类名（如"org.springframework.boot.App"）。
        level (int): 包含的包层级数（如1表示"org"，2表示"org.springframework"）。

    返回:
        str: 包分组（如"org"或"org.springframework"）。
    """
    package = '.'.join(full_class_name.split('.')[:-1])  # 提取包名（排除类名）
    parts = package.split('.')
    if len(parts) <= level:
        return package  # 若包名部分数小于等于level，则返回完整包名
    else:
        return '.'.join(parts[:level])  # 返回前'level'个部分

if __name__ == '__main__':
    # 检查命令行参数：root_directory和level
    if len(sys.argv) != 3:
        print("用法：python script.py <根目录> <层级>")
        sys.exit(1)

    root_dir = sys.argv[1]
    try:
        level = int(sys.argv[2])
        if level < 1:
            raise ValueError
    except ValueError:
        print("错误：层级必须为正整数")
        sys.exit(1)

    all_classes = set()

    # 第一轮遍历：收集项目中所有完全限定类名
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                package = get_package(file_path)
                if package:
                    class_name = file.replace('.java', '')
                    full_class_name = f"{package}.{class_name}"
                    all_classes.add(full_class_name)

    # 存储包分组间的依赖关系
    group_dependencies = set()

    # 第二轮遍历：基于包分组分析依赖关系
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                package = get_package(file_path)
                if package:
                    class_name = file.replace('.java', '')
                    full_class_name = f"{package}.{class_name}"
                    importer_group = get_package_group(full_class_name, level)
                    imports = get_specific_imports(file_path)
                    for imp in imports:
                        # 仅包含项目内部的依赖关系
                        # 排除自依赖
                        if imp in all_classes and imp != full_class_name:
                            imported_group = get_package_group(imp, level)
                            if imported_group != importer_group:
                                group_dependencies.add((importer_group, imported_group))

    # 以DOT格式输出依赖图
    print('digraph G {')
    for from_group, to_group in sorted(group_dependencies):
        print(f'  "{from_group}" -> "{to_group}";')
    print('}')
```

### 变更说明

1. **命令行参数**：
   - **原版**：`python script.py <根目录>`
   - **修改版**：`python script.py <根目录> <层级>`
   - 新增对第二个参数`level`的支持，用于指定包层次级别。脚本会检查是否提供了两个参数，并确保`level`为正整数。

2. **新增函数：`get_package_group`**：
   - 新增用于根据指定`level`计算类所属包分组的函数。
   - 对于完全限定类名（如"org.springframework.boot.App"），提取包名（"org.springframework.boot"），分割为部分（"org"、"springframework"、"boot"），并取前`level`个部分：
     - 若`level=1`：返回"org"。
     - 若`level=2`：返回"org.springframework"。
     - 若包名部分数少于`level`（如"com.example"且`level=3`），则返回完整包名（"com.example"）。

3. **依赖分组**：
   - **原版**：使用`defaultdict(set)`存储单个类间的依赖关系。
   - **修改版**：使用集合`group_dependencies`存储包分组间的有向边，以元组`(from_group, to_group)`形式记录。
   - 对每个类：
     - 使用`get_package_group`计算其包分组（`importer_group`）。
     - 对每个项目内的具体导入（`imp in all_classes`）且非自身类（`imp != full_class_name`）：
       - 计算被导入类的包分组（`imported_group`）。
       - 若分组不同（`imported_group != importer_group`），则向`group_dependencies`添加边。
   - 集合确保唯一性，因此相同分组间的多个依赖仅生成单一边。

4. **DOT输出**：
   - **原版**：打印单个类间的边（如"org.springframework.boot.App" -> "org.apache.commons.IOUtils"）。
   - **修改版**：打印包分组间的边（如`level=2`时"org.springframework" -> "org.apache"）。
   - 边经过排序以确保输出一致性。

### 如何满足需求

- **支持层级**：脚本现接受`level`参数，在分析依赖前对包进行分组。
- **层级=1**：所有类按顶级包分组（如"org"）。例如，"org.springframework.boot.App"和"org.apache.commons.IOUtils"同属"org"组，因此它们之间的导入不会显示为边。
- **层级=2**：类按前两级包分组（如"org.springframework"）。例如，从"org.springframework.boot.App"导入"org.apache.commons.IOUtils"会创建从"org.springframework"到"org.apache"的边。
- **依赖分析前累积包**：脚本在分析导入前根据`level`确定每个类的包分组，确保依赖关系在组间而非单个类间建立。
- **示例兼容性**：对于您的示例边：
  - 原版：`"org.springframework.boot.web.servlet.server.Session" -> "org.springframework.boot.convert.DurationUnit"`
  - `level=2`：两类别同属"org.springframework"，故不添加边（同组）。
  - `level=3`："org.springframework.boot.web" -> "org.springframework.boot.convert"，在这些不同分组间添加边。

### 使用示例

- **命令**：`python script.py /项目路径 1`
  - 分组："org"、"com"等。
  - 输出可能包含：若"org"包中的类导入"com"包中的类，则输出`"org" -> "com"`。

- **命令**：`python script.py /项目路径 2`
  - 分组："org.springframework"、"org.apache"等。
  - 输出可能包含：`"org.springframework" -> "org.apache"`。

### 注意事项

- 脚本保持原有行为，仅包含项目内依赖（`all_classes`中的导入），排除通配符导入和自依赖。
- 无包声明的类会被跳过，与原脚本一致。
- 输出为DOT格式的有向图，可通过Graphviz等工具查看。

此修改后的脚本应完全满足您按包层级分组依赖关系的需求。
