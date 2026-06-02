---
audio: false
generated: true
lang: en
layout: post
title: Fix llama.cpp Model Loading Error
translated: false
type: note
---

Based on the error `gguf_init_from_file_impl: failed to read key-value pairs`, your model file is either **corrupted**, **incomplete**, or **incompatible** with your llama.cpp version. Here's how to fix it:

### 1. **Verify & Redownload the Model**

   ```bash
   # Check current file size (Q6_K quant should be ~6.1GB for 8B model):
   ls -lh /home/lzw/Projects/llama.cpp/models/DeepSeek-R1-0528-Qwen3-8B-UD-Q6_K_XL.gguf

   # Expected output:
   # -rw-r--r-- 1 lzw lzw 6.1G Jun  2 10:00 ...Q6_K_XL.gguf
   ```

- If size < 6GB, **redownload the model**:

     ```bash
     rm /home/lzw/Projects/llama.cpp/models/DeepSeek-R1-0528-Qwen3-8B-UD-Q6_K_XL.gguf
     # Re-download from the original source (e.g., HuggingFace)
     ```

### 2. **Update llama.cpp**

Your build (commit `7675c555`) might be outdated:

```bash
cd ~/Projects/llama.cpp
git pull origin master          # Update code
rm -rf build && mkdir build     # Clean build
cd build
cmake .. -DLLAMA_CUBLAS=ON      # Enable CUDA
make -j                         # Recompile
```

### 3. **Validate Model Integrity**

Test the model with a simple inference:

```bash
~/Projects/llama.cpp/build/bin/main \
  -m /home/lzw/Projects/llama.cpp/models/DeepSeek-R1-0528-Qwen3-8B-UD-Q6_K_XL.gguf \
  -p "Hello" -n 10
```

- If this fails, the model file is definitely corrupted.

### 4. **Try a Different Model (Sanity Check)**

Test with a known-working model (e.g., [TinyLlama](https://huggingface.co/TheBloke/TinyLlama-1.1B-1T-OpenOrca-GGUF)):

```bash
~/Projects/llama.cpp/build/bin/llama-server \
  -m /path/to/tinyllama.Q8_0.gguf \
  --port 8000
```

- If this works, your original model file is the issue.

### 5. **Re-convert the Model (Advanced)**

If redownloading fails:

1. Get the original Hugging Face model:

   ```bash
   huggingface-cli download deepseek-ai/DeepSeek-R1-0528-Qwen3-8B --local-dir ./deepseek-original
   ```

2. Reconvert to GGUF:

   ```bash
   python3 ~/Projects/llama.cpp/convert-hf-to-gguf.py \
     ./deepseek-original \
     --outtype q6_k  # Match your quantization
   ```

### Common Fixes Summary

| Issue | Solution |
|-------|----------|
| **Corrupted download** | Redownload model |
| **Outdated llama.cpp** | `git pull` + recompile |
| **Incompatible GGUF** | Use latest `convert-hf-to-gguf.py` |
| **File permissions** | `chmod +r /path/to/model.gguf` |

> 💡 **Note:** The DeepSeek-R1 model is new (released May 28, 2024). Ensure your llama.cpp is **updated within the last week** for compatibility.

Start by redownloading the model and updating llama.cpp – this resolves 90% of such issues. Let me know if you need further help!
