---
audio: false
generated: true
lang: zh
layout: post
title: 分析Maven项目对象模型
translated: true
type: note
---

针对您的需求，我将提供一个解决方案，通过递归查找目录中的所有 `pom.xml` 文件并分析它们的依赖关系，生成 DOT 格式的依赖图。该方案不假定固定的 Maven 多模块项目结构（如示例中的 `project/module1/pom.xml` 等），而是先收集所有 `pom.xml` 文件，然后分析模块依赖关系并输出图表。

---

## 解决方案概述

该脚本将执行以下步骤：
1. **递归收集 `pom.xml` 文件**：遍历指定的根目录，查找所有 `pom.xml` 文件，无论其位置或结构如何。
2. **解析模块信息**：从每个 `pom.xml` 中提取 `groupId`、`artifactId` 和依赖项。
3. **处理 `groupId` 继承**：如果 `pom.xml` 未指定 `groupId`，则从 `<parent>` 声明中继承（如果存在）。
4. **识别项目内依赖**：根据 `groupId` 和 `artifactId` 将依赖项与项目内的模块进行匹配。
5. **生成 DOT 输出**：创建模块间依赖关系的有向图。

该方法不依赖于预定义的目录层次结构，也不假定父 `pom.xml` 文件位于父目录中。

---

## Python 脚本

以下是符合您需求的 Python 脚本：

```python
import os
import sys
import xml.etree.ElementTree as ET

# 定义 Maven POM 命名空间
NS = "{http://maven.apache.org/POM/4.0.0}"

# 缓存 groupId 以避免重复解析
group_id_cache = {}

def get_group_id(pom_path, pom_map):
    """
    从 pom.xml 文件中提取 groupId，考虑从父 POM 继承的情况。

    参数:
        pom_path (str): pom.xml 文件的路径。
        pom_map (dict): pom.xml 路径到其解析数据的映射。

    返回:
        str: 模块的 groupId。
    """
    if pom_path in group_id_cache:
        return group_id_cache[pom_path]

    tree = ET.parse(pom_path)
    root = tree.getroot()
    group_id_elem = root.find(NS + 'groupId')

    if group_id_elem is not None:
        group_id = group_id_elem.text.strip()
    else:
        # 检查父声明
        parent = root.find(NS + 'parent')
        if parent is not None:
            parent_group_id = parent.find(NS + 'groupId').text.strip()
            parent_artifact_id = parent.find(NS + 'artifactId').text.strip()
            parent_relative_path = parent.find(NS + 'relativePath')
            if parent_relative_path is not None and parent_relative_path.text:
                parent_pom_path = os.path.normpath(
                    os.path.join(os.path.dirname(pom_path), parent_relative_path.text)
                )
            else:
                # 如果省略 relativePath，默认为父目录
                parent_pom_path = os.path.join(os.path.dirname(pom_path), '..', 'pom.xml')
                parent_pom_path = os.path.normpath(parent_pom_path)

            if parent_pom_path in pom_map:
                group_id = get_group_id(parent_pom_path, pom_map)
            else:
                raise ValueError(f"未找到 {pom_path} 的父 POM: {parent_pom_path}")
        else:
            raise ValueError(f"{pom_path} 中未指定 groupId 或 parent")

    group_id_cache[pom_path] = group_id
    return group_id

def get_artifact_id(pom_path):
    """
    从 pom.xml 文件中提取 artifactId。

    参数:
        pom_path (str): pom.xml 文件的路径。

    返回:
        str: 模块的 artifactId。
    """
    tree = ET.parse(pom_path)
    root = tree.getroot()
    artifact_id_elem = root.find(NS + 'artifactId')

    if artifact_id_elem is None:
        raise ValueError(f"pom.xml 必须指定 artifactId: {pom_path}")

    return artifact_id_elem.text.strip()

def get_dependencies(pom_path):
    """
    从 pom.xml 文件中提取依赖列表。

    参数:
        pom_path (str): pom.xml 文件的路径。

    返回:
        list: 每个依赖项的 (groupId, artifactId) 元组列表。
    """
    tree = ET.parse(pom_path)
    root = tree.getroot()
    dependencies = []

    for dep in root.findall(NS + 'dependencies/' + NS + 'dependency'):
        dep_group_id_elem = dep.find(NS + 'groupId')
        dep_artifact_id_elem = dep.find(NS + 'artifactId')
        if dep_group_id_elem is not None and dep_artifact_id_elem is not None:
            dep_group_id = dep_group_id_elem.text.strip()
            dep_artifact_id = dep_artifact_id_elem.text.strip()
            dependencies.append((dep_group_id, dep_artifact_id))

    return dependencies

if __name__ == '__main__':
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("用法: python script.py <根目录>")
        sys.exit(1)

    root_dir = sys.argv[1]
    if not os.path.isdir(root_dir):
        print(f"错误: {root_dir} 不是目录")
        sys.exit(1)

    # 步骤 1: 递归查找所有 pom.xml 文件
    pom_files = [
        os.path.join(root, file)
        for root, _, files in os.walk(root_dir)
        for file in files if file == 'pom.xml'
    ]

    if not pom_files:
        print(f"在 {root_dir} 中未找到 pom.xml 文件")
        sys.exit(1)

    # 步骤 2: 构建所有 POM 的字典用于父查找
    pom_map = {pom_file: None for pom_file in pom_files}

    # 步骤 3: 提取模块信息
    modules = {}  # (groupId, artifactId) -> pom_path
    for pom_file in pom_files:
        try:
            group_id = get_group_id(pom_file, pom_map)
            artifact_id = get_artifact_id(pom_file)
            modules[(group_id, artifact_id)] = pom_file
        except ValueError as e:
            print(f"警告: 由于错误跳过 {pom_file}: {e}")
            continue

    # 步骤 4: 分析依赖关系
    dependencies = set()
    for pom_file in pom_files:
        try:
            importer_group_id = get_group_id(pom_file, pom_map)
            importer_artifact_id = get_artifact_id(pom_file)
            importer_key = (importer_group_id, importer_artifact_id)
            deps = get_dependencies(pom_file)
            for dep_group_id, dep_artifact_id in deps:
                dep_key = (dep_group_id, dep_artifact_id)
                if dep_key in modules and dep_key != importer_key:
                    # 添加依赖关系为 (导入者, 被导入者) 元组，为简化使用 artifactId
                    dependencies.add((importer_artifact_id, dep_artifact_id))
        except ValueError as e:
            print(f"警告: 处理 {pom_file} 中的依赖关系时出错: {e}")
            continue

    # 步骤 5: 以 DOT 格式输出
    print('digraph G {')
    for from_module, to_module in sorted(dependencies):
        print(f'  "{from_module}" -> "{to_module}";')
    print('}')
```

---

## 工作原理

### 1. **命令行输入**
- 接受单个参数：`<根目录>`，作为递归搜索的起点。
- 验证其是否为目录。

### 2. **查找 `pom.xml` 文件**
- 使用 `os.walk` 递归遍历目录树，将所有 `pom.xml` 文件收集到列表中。

### 3. **解析模块信息**
- **Group ID (`groupId`)**：
  - 从每个 `pom.xml` 中提取。
  - 如果不存在，则查找 `<parent>` 部分，并通过 `relativePath`（如果省略则默认为父目录）从引用的父 POM 解析 `groupId`。
  - 缓存结果以避免重复解析。
- **Artifact ID (`artifactId`)**：必须存在于每个 `pom.xml` 中。
- **依赖项**：从 `<dependencies>` 部分提取 `(groupId, artifactId)` 对。

### 4. **依赖分析**
- 构建所有模块的 `(groupId, artifactId)` 到 `pom_path` 的映射。
- 对于每个 `pom.xml`，检查其依赖项与模块映射的匹配情况，以找到项目内依赖。
- 排除自依赖（模块依赖自身的情况）。
- 将依赖关系记录为 `(导入者_artifactId, 被导入者_artifactId)` 对。

### 5. **DOT 输出**
- 以 DOT 格式输出有向图，为简化使用 `artifactId` 作为节点标签。

---

## 使用示例

假设您的目录结构不规则：

```
myproject/
├── app/pom.xml (groupId="com.myapp", artifactId="app", 依赖 "core")
├── libs/core/pom.xml (groupId="com.myapp", artifactId="core")
├── tools/util/pom.xml (groupId="com.myapp", artifactId="util", 依赖 "core")
```

运行脚本：

```bash
python script.py myproject
```

**输出：**

```
digraph G {
  "app" -> "core";
  "util" -> "core";
}
```

这表明 `app` 和 `util` 都依赖 `core`。

---

## 注意事项与限制

- **无目录分组**：与思考轨迹中的原始脚本不同，此版本不按目录结构对模块进行分组，因为您未要求此功能。它直接在图中使用 `artifactId`。
- **父解析**：依赖 `<parent>` 部分中的 `relativePath`，如果省略则假定父 POM 位于父目录中。如果父 POM 不在收集的集合中，则会引发错误。
- **简单匹配**：仅通过 `groupId` 和 `artifactId` 匹配依赖项，忽略版本。
- **无属性替换**：不处理 Maven 属性如 `${project.groupId}`。
- **错误处理**：跳过有问题的 `pom.xml` 文件并发出警告，而不是完全失败。

该脚本满足您"先递归迭代获取所有 POM，然后分析"的需求，且不假定固定的文件结构。如需调整，请告知！
