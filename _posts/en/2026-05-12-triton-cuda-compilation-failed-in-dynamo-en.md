---
audio: false
generated: true
image: false
lang: en
layout: post
title: Triton CUDA Compilation Failed in Dynamo
translated: false
type: note
---

File "/home/lzw/.local/lib/python3.11/site-packages/torch/utils/_triton.py", line 103, in triton_backend
    target = driver.active.get_current_target()
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lzw/.local/lib/python3.11/site-packages/triton/runtime/driver.py", line 23, in __getattr__
    self._initialize_obj()
  File "/home/lzw/.local/lib/python3.11/site-packages/triton/runtime/driver.py", line 20, in _initialize_obj
    self._obj = self._init_fn()
                ^^^^^^^^^^^^^^^
  File "/home/lzw/.local/lib/python3.11/site-packages/triton/runtime/driver.py", line 9, in _create_driver
    return actives[0]()
           ^^^^^^^^^^^^
  File "/home/lzw/.local/lib/python3.11/site-packages/triton/backends/nvidia/driver.py", line 450, in __init__
    self.utils = CudaUtils()  # TODO: make static
                 ^^^^^^^^^^^
  File "/home/lzw/.local/lib/python3.11/site-packages/triton/backends/nvidia/driver.py", line 80, in __init__
    mod = compile_module_from_src(Path(os.path.join(dirname, "driver.c")).read_text(), "cuda_utils")
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lzw/.local/lib/python3.11/site-packages/triton/backends/nvidia/driver.py", line 57, in compile_module_from_src
    so = _build(name, src_path, tmpdir, library_dirs(), include_dir, libraries)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lzw/.local/lib/python3.11/site-packages/triton/runtime/build.py", line 50, in _build
    ret = subprocess.check_call(cc_cmd)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/subprocess.py", line 413, in check_call
    raise CalledProcessError(retcode, cmd)
torch._dynamo.exc.BackendCompilerFailed: backend='inductor' raised:
CalledProcessError: Command '['/usr/bin/gcc', '/tmp/tmpt2wndipb/main.c', '-O3', '-shared', '-fPIC', '-Wno-psabi', '-o', '/tmp/tmpt2wndipb/cuda_utils.cpython-311-x86_64-linux-gnu.so', '-lcuda', '-L/home/lzw/.local/lib/python3.11/site-packages/triton/backends/nvidia/lib', '-L/lib/x86_64-linux-gnu', '-L/lib/i386-linux-gnu', '-I/home/lzw/.local/lib/python3.11/site-packages/triton/backends/nvidia/include', '-I/tmp/tmpt2wndipb', '-I/usr/include/python3.11']' returned non-zero exit status 1.

Set TORCH_LOGS="+dynamo" and TORCHDYNAMO_VERBOSE=1 for more information


You can suppress this exception and fall back to eager by setting:
    import torch._dynamo
    torch._dynamo.config.suppress_errors = True
