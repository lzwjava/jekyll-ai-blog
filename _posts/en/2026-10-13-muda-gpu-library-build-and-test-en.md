---
audio: false
generated: true
image: false
lang: en
layout: post
title: Muda GPU Library Build and Test
translated: false
type: note
---

Everything passes. Copy‑paste from anywhere:

```sh
cd ~/projects/muda

# 1. build everything
make clean && make

# 2. run the test suite (35 checks)
make test

# 3. inspect the device / driver / PCI info
./build/mudainfo

# 4. run the examples
./build/vector_add    # 1M-element vector add
./build/saxpy         # 4M-element SAXPY, uses streams + event timing
./build/matmul        # 256x256 tiled matmul (shared mem + __syncthreads)
```

Optional environment variables:

```sh
MUDA_DRIVER=opencl ./build/test_muda    # pick the backend (only opencl today)
MUDA_VERBOSE=1 ./build/matmul          # dump the generated OpenCL build log
```

Expected result (on your M40):

```
35 passed, 0 failed
vector_add of 1048576 elements: OK (~0.19 ms, ~66 GB/s)
saxpy of 4194304 elements: OK (~0.24 ms, ~210 GB/s)
matmul 256x256: OK (~0.09 ms, ~390 GFLOP/s)
```

To use `muda` from your own C program, link the static or shared library:

```sh
cc -Iinclude myprog.c build/libmuda.a -ldl -lpthread -o myprog
# or: cc -Iinclude myprog.c -Lbuild -lmuda -Wl,-rpath,$PWD/build -ldl -lpthread -o myprog
```

A complete reference program is `examples/vector_add.c`.