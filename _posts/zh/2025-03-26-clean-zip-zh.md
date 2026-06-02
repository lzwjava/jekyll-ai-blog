---
audio: false
generated: true
lang: zh
layout: post
title: 清理压缩文件
translated: true
type: note
---

1. **读取ZIP文件**：使用 `zipfile.ZipFile` 获取压缩包内所有文件的列表
2. **过滤无扩展名文件**：保留目录（以`/`结尾的条目）
3. **记录被移除文件**：向用户展示被排除的文件清单
4. **创建新ZIP文件**：仅保留有效文件（含扩展名的文件或目录）
5. **使用`argparse`接收ZIP文件路径**：通过命令行参数传入文件路径

该流程可确保仅保留规范文件，同时维持目录结构。🚀

```python
import zipfile
import os
import argparse

def clean_zip(zip_path):
    output_path = os.path.splitext(zip_path)[0] + "_output.zip"

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        file_names = zip_ref.namelist()

        # 分离有效文件与无扩展名文件（排除目录）
        valid_files = [f for f in file_names if os.path.splitext(os.path.basename(f))[1] or f.endswith('/')]
        removed_files = [f for f in file_names if not os.path.splitext(os.path.basename(f))[1] and not f.endswith('/')]

        if not valid_files:
            print("未找到带扩展名的有效文件，程序终止")
            return

        # 记录被移除文件
        if removed_files:
            print("正在移除以下文件（未检测到扩展名）：")
            for f in removed_files:
                print(f" - {f}")

        # 创建排除无效文件的新压缩包
        with zipfile.ZipFile(output_path, 'w') as clean_zip:
            for file in valid_files:
                with zip_ref.open(file) as source:
                    clean_zip.writestr(file, source.read())

    print(f"已生成清理后的ZIP文件：{output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="通过移除无扩展名文件来清理ZIP文件")
    parser.add_argument("zip_path", help="输入ZIP文件路径")
    args = parser.parse_args()
    clean_zip(args.zip_path)

```
