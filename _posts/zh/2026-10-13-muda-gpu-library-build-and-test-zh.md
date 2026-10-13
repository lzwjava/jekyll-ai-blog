---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Muda GPU 库构建与测试
translated: true
type: note
---

所有测试均通过。从任意位置复制粘贴：

```sh
cd ~/projects/muda

# 1. 构建所有
make clean && make

# 2. 运行测试套件（35 项检查）
make test

# 3. 查看设备 / 驱动 / PCI 信息
./build/mudainfo

# 4. 运行示例
./build/vector_add    # 1M 元素向量加法
./build/saxpy         # 4M 元素 SAXPY，使用 streams 和事件计时
./build/matmul        # 256x256 分块 matmul（共享内存 + __syncthreads）
```

可选环境变量：

```sh
MUDA_DRIVER=opencl ./build/test_muda    # 选择后端（目前仅支持 opencl）
MUDA_VERBOSE=1 ./build/matmul          # 输出生成的 OpenCL 构建日志
```

预期结果（在 M40 上）：

```
35 passed, 0 failed
vector_add of 1048576 elements: OK (~0.19 ms, ~66 GB/s)
saxpy of 4194304 elements: OK (~0.24 ms, ~210 GB/s)
matmul 256x256: OK (~0.09 ms, ~390 GFLOP/s)
```

要在你自己的 C 程序中使用 `muda`，请链接静态库或共享库：

```sh
cc -Iinclude myprog.c build/libmuda.a -ldl -lpthread -o myprog
# 或者： cc -Iinclude myprog.c -Lbuild -lmuda -Wl,-rpath,$PWD/build -ldl -lpthread -o myprog
```

一个完整的参考程序是 `examples/vector_add.c`。
