---
audio: false
generated: true
image: false
lang: en
layout: post
title: Windows protobuf installation via pip wrappers
translated: false
type: note
---

**Question:** In Warp dev (agent development), there's protobuf involved. On Windows, how can we use `pip install` for protobuf and wrap the `protoc` compiler command, since we can't install protobuf directly from GitHub releases and need to build from source?

**Answer:**

The cleanest approach on Windows is to use the `grpc-tools` or `protoc-wheel-0` pip packages, which ship a bundled `protoc` binary. No source compilation needed.

## Option 1: `grpcio-tools` (recommended — includes `protoc`)

```bash
pip install grpcio-tools
```

This bundles `protoc` inside the Python package. Use it like:

```bash
python -m grpc_tools.protoc \
  -I./protos \
  --python_out=./generated \
  --grpc_python_out=./generated \
  ./protos/your_service.proto
```

If you only need `protoc` (no gRPC), just do plain codegen:

```bash
python -m grpc_tools.protoc \
  -I./protos \
  --python_out=./generated \
  ./protos/your_message.proto
```

## Option 2: `protoc-wheel-0` (lighter, just protoc binary)

```bash
pip install protoc-wheel-0
```

Then wrap it:

```bash
python -c "import protoc; protoc.main()" -- --version
```

Or use the installed script directly:

```bash
protoc --version
```

## Option 3: Write a `protoc` wrapper script (for build systems / Warp agent pipelines)

Create a `compile_proto.py` wrapper that your agent or build step calls:

```python
#!/usr/bin/env python3
"""
protoc wrapper using grpcio-tools.
Usage: python compile_proto.py <proto_file> [--out=./generated]
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

Run:

```bash
python compile_proto.py protos/agent.proto --proto-path=protos --out=generated
```

## For Warp agent dev specifically

If Warp's build system calls `protoc` as a raw binary (e.g. via `subprocess` or a `Makefile`), you can shim it by putting a `protoc.bat` on your PATH:

```bat
@echo off
:: protoc.bat — shim for grpcio-tools protoc on Windows
python -m grpc_tools.protoc %*
```

Save this as `protoc.bat` somewhere in your `PATH` (e.g. `C:\tools\` or the repo root). Now any call to `protoc` from scripts or build tools transparently uses the pip-installed version.

## Versions to pin (stable as of mid-2026)

```txt
# requirements-dev.txt
grpcio-tools==1.64.1
protobuf==5.27.1
```

```bash
pip install grpcio-tools==1.64.1 protobuf==5.27.1
```

The `protobuf` Python runtime and `grpcio-tools` versions need to be compatible — pinning both avoids the common `google.protobuf` version mismatch error on Windows.