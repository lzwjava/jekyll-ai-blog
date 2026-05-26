---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Windows上通过pip包装器安装protobuf
translated: true
type: note
---

**问题：** 在 Warp dev（代理开发）中涉及 protobuf。在 Windows 上，由于无法直接从 GitHub 发布版安装 protobuf 且需要从源码构建，我们该如何使用 `pip install` 来安装 protobuf 并封装 `protoc` 编译器命令？

**答案：**

在 Windows 上最简洁的方法是使用 `grpc-tools` 或 `protoc-wheel-0` pip 包，它们内置了预编译的 `protoc` 二进制文件，无需源码编译。

## 选项 1：`grpcio-tools`（推荐——包含 `protoc`）

```bash
pip install grpcio-tools
```

该包将 `protoc` 捆绑在 Python 包中，使用方法如下：

```bash
python -m grpc_tools.protoc \
  -I./protos \
  --python_out=./generated \
  --grpc_python_out=./generated \
  ./protos/your_service.proto
```

如果只需要 `protoc`（不包含 gRPC），直接进行纯代码生成：

```bash
python -m grpc_tools.protoc \
  -I./protos \
  --python_out=./generated \
  ./protos/your_message.proto
```

## 选项 2：`protoc-wheel-0`（更轻量，仅包含 protoc 二进制文件）

```bash
pip install protoc-wheel-0
```

然后封装使用：

```bash
python -c "import protoc; protoc.main()" -- --version
```

或者直接使用安装后的脚本：

```bash
protoc --version
```

## 选项 3：编写 `protoc` 封装脚本（适用于构建系统 / Warp 代理管道）

创建一个 `compile_proto.py` 封装脚本，供代理或构建步骤调用：

```python
#!/usr/bin/env python3
"""
使用 grpcio-tools 的 protoc 封装。
用法：python compile_proto.py <proto_file> [--out=./generated]
"""
import sys
import os
from grpc_tools import protoc

def compile_proto(proto_file: str, proto_path: str = ".", out_dir: str = "./generated"):
    os.makedirs(out_dir, exist_ok=True)
    result = protoc.main([
        "grpc_tools.protoc",
        f"-I{proto_path}",
        f"--python_out={out_dir}",
        f"--grpc_python_out={out_dir}",
        proto_file,
    ])
    if result != 0:
        print(f"protoc failed with code {result}", file=sys.stderr)
        sys.exit(result)
    print(f"Compiled {proto_file} → {out_dir}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("proto_file")
    parser.add_argument("--proto-path", default=".")
    parser.add_argument("--out", default="./generated")
    args = parser.parse_args()
    compile_proto(args.proto_file, args.proto_path, args.out)
```

运行：

```bash
python compile_proto.py protos/agent.proto --proto-path=protos --out=generated
```

## 针对 Warp 代理开发

如果 Warp 的构建系统以原生二进制形式调用 `protoc`（例如通过 `subprocess` 或 `Makefile`），你可以通过将 `protoc.bat` 放在 PATH 中来为其创建一个垫片（shim）：

```bat
@echo off
:: protoc.bat — 在 Windows 上为 grpcio-tools protoc 提供的垫片
python -m grpc_tools.protoc %*
```

将此文件保存为 `protoc.bat`，并放在 PATH 中的某个目录（例如 `C:\tools\` 或仓库根目录）。之后，脚本或构建工具对 `protoc` 的所有调用都会透明地使用 pip 安装的版本。

## 要固定的版本（截至 2026 年中稳定版本）

```txt
# requirements-dev.txt
grpcio-tools==1.64.1
protobuf==5.27.1
```

```bash
pip install grpcio-tools==1.64.1 protobuf==5.27.1
```

`protobuf` Python 运行时和 `grpcio-tools` 的版本需要兼容——同时固定这两个版本可避免 Windows 上常见的 `google.protobuf` 版本不匹配错误。