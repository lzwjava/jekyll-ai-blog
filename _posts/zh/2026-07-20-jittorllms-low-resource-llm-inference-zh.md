---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 计图大模型推理库：低资源大模型推理
translated: true
type: note
---

问题：什么是 Jittor/JittorLLMs？

答：这是一个基于 **Jittor**（清华大学/飞腾开发的深度学习框架，可作为 PyTorch 的中国替代方案——采用 JIT 元算子编译而非即时/图执行）构建的大语言模型推理库。核心理念：在没有 GPU、仅 2GB 内存的笔记本上运行大模型。

关键机制：
- **模型支持**：ChatGLM-6B、LLaMA/LLaMA2、ChatRWKV、PanGu-α、Atom-7B（计划支持 MOSS）
- **内存技巧**：在 GPU↔CPU↔磁盘之间动态张量交换——他们声称是首个实现自动动态图变量交换的框架（相比之下，其他方法使用静态图交换技术）
- **可移植性**：`JTorch`——一个由 Jittor 驱动的 `torch` 即插即用替代品，因此现有 HF Transformers/Megatron 代码无需修改即可运行
- **宣称**：相比同类框架，硬件需求降低 80%，加载速度提升 40%（零拷贝），计算速度提升 20% 以上（未经验证，除营销宣传外无公开基准测试）

实际使用以命令行为主，适合你的工作流：

```bash
git clone https://github.com/Jittor/JittorLLMs.git --depth 1
cd JittorLLMs
pip install -r requirements.txt -i https://pypi.jittor.org/simple -I

python cli_demo.py chatglm    # 或：pangualpha|llama|chatrwkv|llama2|atom7b
```

通过环境变量限制内存（在受限机器上测试时有用）：
```bash
export JT_SAVE_MEM=1
export cpu_mem_limit=16000000000   # 16G
export device_mem_limit=8000000000  # 8G
```

后端服务器模式：
```bash
python api.py chatglm
# 然后：requests.post("http://0.0.0.0:8000", json.dumps({'prompt': '...'}))
```

**现实审视**：2.4k 星标、187 个分支、无发布版本，最近活跃开发似乎停留在 2023 年的 ChatGLM/LLaMA2 时代模型——无更新（无 Qwen3、DeepSeek-V3/R1、Llama 3+）。对于你的 GPU 集群工作（MI300X、每月 2B tokens），这更像是一个“笔记本演示玩具”而非生产基础设施——llama.cpp/vLLM/SGLang 覆盖了相同领域，且维护更活跃、硬件支持更广泛。主要作为 Jittor 生态系统的一个有趣点值得了解（如果你在开发自定义硬件后端，JTorch 的即插即用兼容层是更有技术含量的部分）。

参考：
- [Jittor/JittorLLMs](https://github.com/Jittor/JittorLLMs)
- [Jittor 文档](https://cg.cs.tsinghua.edu.cn/jittor/assets/docs/index.html)