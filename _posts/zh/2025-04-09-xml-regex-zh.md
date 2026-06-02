---
audio: false
generated: true
lang: zh
layout: post
title: XML正则表达式脚本
translated: true
type: note
---

我将修改脚本，使用 `argparse` 来处理命令行参数。这将允许您在运行脚本时直接传递文件路径：

```python
import xml.etree.ElementTree as ET
import re
import argparse

def extract_look_tags(xml_file):
    # 读取 XML 文件内容
    with open(xml_file, 'r') as file:
        xml_content = file.read()

    # 使用正则表达式查找所有 <c:look> 标签
    pattern = r'<c:look>(\d+)</c:look>'
    matches = re.findall(pattern, xml_content)

    # 打印数字
    for number in matches:
        print(number)

def main():
    # 设置参数解析器
    parser = argparse.ArgumentParser(description='从 XML 文件的 <c:look> 标签中提取数字')
    parser.add_argument('file_path', help='XML 文件路径')

    # 解析参数
    args = parser.parse_args()

    # 处理文件
    extract_look_tags(args.file_path)

if __name__ == "__main__":
    main()
```

现在您可以从命令行这样运行脚本：

```
python 脚本名称.py 路径/到/您的/xml文件.xml
```

该脚本将：
1. 使用 `argparse` 处理文件路径的命令行参数
2. 解析 XML 文件以查找所有 `<c:look>` 标签
3. 提取并打印这些标签内的数字

这种方法使脚本更加用户友好，适用于脚本或批处理操作。
