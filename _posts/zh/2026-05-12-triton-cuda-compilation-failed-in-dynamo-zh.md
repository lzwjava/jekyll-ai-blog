---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Dynamo 中 Triton CUDA 编译失败
translated: true
type: note
---

文件 "/home/lzw/.local/lib/python3.11/site-packages/torch/utils/_triton.py"，第103行，在 triton_backend 中
    target = driver.active.get_current_target()
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
文件 "/home/lzw/.local/lib/python3.11/site-packages/triton/runtime/driver.py"，第23行，在 __getattr__ 中
    self._initialize_obj()
文件 "/home/lzw/.local/lib/python3.11/site-packages/triton/runtime/driver.py"，第20行，在 _initialize_obj 中
    self._obj = self._init_fn()
                ^^^^^^^^^^^^^^^
文件 "/home/lzw/.local/lib/python3.11/site-packages/triton/runtime/driver.py"，第9行，在 _create_driver 中
    return actives[0]()
           ^^^^^^^^^^^^
文件 "/home/lzw/.local/lib/python3.11/site-packages/triton/backends/nvidia/driver.py"，第450行，在 __init__ 中
    self.utils = CudaUtils()  # TODO: 改为静态
                 ^^^^^^^^^^^
文件 "/home/lzw/.local/lib/python3.11/site-packages/triton/backends/nvidia/driver.py"，第80行，在 __init__ 中
    mod = compile_module_from_src(Path(os.path.join(dirname, "driver.c")).read_text(), "cuda_utils")
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
文件 "/home/lzw/.local/lib/python3.11/site-packages/triton/backends/nvidia/driver.py"，第57行，在 compile_module_from_src 中
    so = _build(name, src_path, tmpdir, library_dirs(), include_dir, libraries)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
文件 "/home/lzw/.local/lib/python3.11/site-packages/triton/runtime/build.py"，第50行，在 _build 中
    ret = subprocess.check_call(cc_cmd)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
文件 "/usr/lib/python3.11/subprocess.py"，第413行，在 check_call 中
    raise CalledProcessError(retcode, cmd)
torch._dynamo.exc.BackendCompilerFailed: backend='inductor' 引发:
CalledProcessError: 命令 '['/usr/bin/gcc', '/tmp/tmpt2wndipb/main.c', '-O3', '-shared', '-fPIC', '-Wno-psabi', '-o', '/tmp/tmpt2wndipb/cuda_utils.cpython-311-x86_64-linux-gnu.so', '-lcuda', '-L/home/lzw/.local/lib/python3.11/site-packages/triton/backends/nvidia/lib', '-L/lib/x86_64-linux-gnu', '-L/lib/i386-linux-gnu', '-I/home/lzw/.local/lib/python3.11/site-packages/triton/backends/nvidia/include', '-I/tmp/tmpt2wndipb', '-I/usr/include/python3.11']' 返回非零退出状态 1。

设置 TORCH_LOGS="+dynamo" 和 TORCHDYNAMO_VERBOSE=1 以获取更多信息


你可以通过以下设置抑制此异常并回退到 eager 模式：
    import torch._dynamo
    torch._dynamo.config.suppress_errors = True
