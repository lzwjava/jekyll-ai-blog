---
audio: false
generated: true
lang: zh
layout: post
title: Spring Boot项目分析
translated: true
type: note
---

要分析一个Spring Boot项目（可能包含多个模块）并提取所有使用`@GetMapping`或`@PostMapping`注解定义的API，我们需要遍历项目目录，识别控制器类，提取API路径，并按指定格式打印。以下是一个完整的Python脚本，受提供代码结构的启发，但根据新需求进行了调整。输出将列出每个控制器及其关联的GET和POST路径，格式为"XXController: get path post path"。

### 方法思路

1. **遍历目录**：递归查找项目目录及其子目录中的所有`.java`文件。
2. **识别控制器**：检查每个Java文件是否包含`@Controller`或`@RestController`注解以确认其为控制器类。
3. **提取类级别路径**：查找类级别的`@RequestMapping`注解以确定基础路径。
4. **提取方法级别API**：查找带有`@GetMapping`或`@PostMapping`注解的方法，提取其路径，并与基础路径（如果存在）组合。
5. **组织并打印**：收集每个控制器的GET和POST路径，并按指定格式打印。

### Python脚本

```python
import os
import sys
import re
from collections import defaultdict

def find_java_files(root_dir):
    """
    递归查找给定目录及其子目录中的所有.java文件。

    Args:
        root_dir (str): 开始搜索的根目录。

    Yields:
        str: 每个.java文件的完整路径。
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.java'):
                yield os.path.join(dirpath, filename)

def extract_paths(line, annotation_type):
    """
    从Spring注解（@GetMapping、@PostMapping或@RequestMapping）中提取路径值。

    Args:
        line (str): 包含注解的行。
        annotation_type (str): 注解类型（'GetMapping'、'PostMapping'或'RequestMapping'）。

    Returns:
        list: 从注解中提取的路径字符串列表。
    """
    if annotation_type in ['GetMapping', 'PostMapping']:
        match = re.search(rf'@{annotation_type}\\((.*)\\)', line)
        if match:
            content = match.group(1)
            # 提取引号内的所有字符串字面量
            paths = re.findall(r'"([^"]*)"', content)
            return paths
        return []
    elif annotation_type == 'RequestMapping':
        match = re.search(r'@RequestMapping\\((.*)\\)', line)
        if match:
            content = match.group(1)
            # 查找'value'或'path'属性
            value_match = re.search(r'(value|path)\s*=\s*({[^}]*}|"[^"]*")', content)
            if value_match:
                value = value_match.group(2)
                if value.startswith('{'):
                    paths = re.findall(r'"([^"]*)"', value)
                else:
                    paths = [value.strip('"')]
                return paths
            # 如果没有'value'或'path'，假设直接指定路径
            paths = re.findall(r'"([^"]*)"', content)
            return paths
        return []

if __name__ == '__main__':
    # 解析命令行参数
    if len(sys.argv) != 2:
        print("Usage: python script.py <root_directory>")
        sys.exit(1)

    root_dir = sys.argv[1]
    if not os.path.isdir(root_dir):
        print(f"[ERROR] The specified path is not a directory: {root_dir}")
        sys.exit(1)

    print(f"[INFO] Starting analysis of directory: {root_dir}")

    # 初始化字典以存储控制器映射
    controllers = defaultdict(lambda: {'GET': [], 'POST': []})
    total_files = 0
    error_files = 0

    # 处理所有Java文件
    for java_file in find_java_files(root_dir):
        try:
            with open(java_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # 检查文件是否为控制器
            if any('@Controller' in line or '@RestController' in line for line in lines):
                controller_name = os.path.basename(java_file).replace('.java', '')

                # 查找类声明行以分离类级别和方法级别注解
                class_line_index = None
                for i, line in enumerate(lines):
                    if re.search(r'public\s+(class|abstract\s+class|interface)\s+\w+', line):
                        class_line_index = i
                        break
                if class_line_index is None:
                    continue

                # 提取类级别的@RequestMapping作为基础路径
                base_paths = []
                for line in lines[:class_line_index]:
                    if re.search(r'\s*@RequestMapping', line):
                        base_paths = extract_paths(line, 'RequestMapping')
                        break
                if not base_paths:
                    base_paths = ['']

                # 提取方法级别的@GetMapping和@PostMapping
                get_paths = []
                post_paths = []
                for line in lines[class_line_index:]:
                    if re.search(r'\s*@GetMapping', line):
                        paths = extract_paths(line, 'GetMapping')
                        for base in base_paths:
                            for path in paths:
                                full_path = base + path
                                get_paths.append(full_path)
                    elif re.search(r'\s*@PostMapping', line):
                        paths = extract_paths(line, 'PostMapping')
                        for base in base_paths:
                            for path in paths:
                                full_path = base + path
                                post_paths.append(full_path)

                # 存储唯一路径
                get_paths = sorted(list(set(get_paths)))
                post_paths = sorted(list(set(post_paths)))

                if get_paths or post_paths:
                    controllers[controller_name]['GET'] = get_paths
                    controllers[controller_name]['POST'] = post_paths

            total_files += 1
        except Exception as e:
            print(f"[ERROR] Could not read file {java_file}: {e}")
            error_files += 1

    # 打印摘要
    print(f"[INFO] Total Java files attempted: {total_files + error_files}")
    print(f"[INFO] Successfully processed: {total_files}")
    print(f"[INFO] Files with errors: {error_files}")
    print(f"[INFO] Total controllers found: {len(controllers)}")

    # 按指定格式打印结果
    for controller, mappings in sorted(controllers.items()):
        print(f"{controller}:")
        for path in mappings['GET']:
            print(f"get {path}")
        for path in mappings['POST']:
            print(f"post {path}")
```

### 代码解释

- **导入模块**：使用`os`进行目录遍历，`sys`处理命令行参数，`re`进行正则表达式匹配，`defaultdict`组织控制器数据。
- **`find_java_files`**：该函数递归生成项目目录中的所有`.java`文件，通过`os.walk`自然处理多个模块。
- **`extract_paths`**：该函数解析`@GetMapping`、`@PostMapping`或`@RequestMapping`注解以提取路径值。它处理：
  - 单一路径（例如`@GetMapping("/path")`）。
  - 多个路径（例如`@GetMapping({"/path1", "/path2"})`）。
  - 命名属性（例如`@RequestMapping(value = "/path")`）。
- **主逻辑**：
  - **命令行处理**：接受根目录作为输入，类似于提供的脚本。
  - **控制器检测**：检查文件内容中是否存在`@Controller`或`@RestController`。
  - **基础路径**：在类声明之前提取类级别的`@RequestMapping`路径。
  - **API提取**：处理类声明之后的行，查找`@GetMapping`和`@PostMapping`，将路径与基础路径组合。
  - **输出**：打印每个控制器及其GET和POST路径，每行一个，前缀为"get"或"post"。
- **错误处理**：捕获文件读取期间的异常并报告，与提供代码的健壮性保持一致。

### 示例输出

对于一个包含`UserController.java`文件的Spring Boot项目：

```java
@RestController
@RequestMapping("/users")
public class UserController {
    @GetMapping("/all")
    public ResponseEntity<?> getAllUsers() { ... }

    @PostMapping("/create")
    public ResponseEntity<?> createUser() { ... }
}
```

运行`python script.py /path/to/project`可能产生：

```
[INFO] Starting analysis of directory: /path/to/project
[INFO] Total Java files attempted: 10
[INFO] Successfully processed: 10
[INFO] Files with errors: 0
[INFO] Total controllers found: 1
UserController:
get /users/all
post /users/create
```

### 注意事项

- **简化处理**：该脚本假设注解位于单行，且路径为字符串字面量，不包含复杂表达式。对于生产环境使用，Java解析器可能更健壮。
- **仅GET和POST**：根据要求，它专注于`@GetMapping`和`@PostMapping`，忽略其他方法如PUT或DELETE（尽管思考轨迹考虑了带方法的`@RequestMapping`）。
- **路径拼接**：直接组合类级别和方法级别路径（例如`/users` + `/all` = `/users/all`）。Spring会规范化多个斜杠，因此这对于显示目的已经足够。

该脚本满足查询要求，同时保持了与提供代码相似的结构，确保了熟悉性和可靠性。
