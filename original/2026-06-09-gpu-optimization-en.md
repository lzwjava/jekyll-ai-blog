---
audio: false
generated: false
image: false
lang: en
layout: post
title: "Discussion of CUDA Graph Optimization and Inference Acceleration"
translated: false
---

Two participants: [aztice](https://github.com/aztice) and [lzwjava](https://github.com/lzwjava).

Aztice — Hong Kong secondary school student, lead developer of Axono (a lightweight AI inference library). Participated in the 2024 6th IKCEST "Belt and Road" International Big Data Competition and the 10th Baidu & Xi'an Jiaotong University Big Data Competition, ranking 17th out of 1,700+ team members. Multiple years of experience in AI Infrastructure. GitHub: [@aztice](https://github.com/aztice) , WeChat@awalightice.

The following conversation was transcribed using Whisper on an RTX 4070, then refined and organized with the help of AI tools. The original conversation was in Chinese.

Note: Because both transcription and refinement were AI-assisted, some details may be inaccurate or paraphrased. Please verify any important information independently before relying on it.

---

# Discussion of CUDA Graph Optimization, Inference Acceleration, and the Broader GPU Software Ecosystem

This meeting covered a broad exploration of GPU programming and inference optimization, centered around the participant's work on CUDA Graph technology and its application in improving model inference speed. The discussion moved from a specific review of competition results and the mechanics of CUDA Graph to a deeper examination of the broader GPU software stack, including memory bandwidth bottlenecks, KV Cache optimization, the roles of TensorRT and CUDNN, the Triton language, and the relationship between distributed inference frameworks like vLLM and SGLang versus handwritten optimizations. The conversation also touched on model selection, the culture of AI competitions, and the pursuit of extreme performance through low-level optimization.

## Competition Status and Preliminary Discussion

The meeting began with a check on the outcome of a recent competition. The participant confirmed that the competition — a Baidu-sponsored event (referred to as Baidu CTI) — has not yet ended, and currently no rankings are being displayed. Although the participant had previously mentioned being in first place, the competition's final results have not been released, and no conclusion has been reached.

## Deep Dive into CUDA Graph: Concept and Mechanics

A major portion of the discussion focused on the participant's deepening understanding of **CUDA Graph**, a technique for optimizing GPU kernel launches.

### What CUDA Graph Does

The participant explained that CUDA Graph works by "recording" the sequence of kernel launches that the CPU would normally issue to the GPU. In a typical execution flow, the CPU must dispatch each individual kernel command to the GPU — a process that involves significant overhead and blocking. With CUDA Graph, the CPU records the entire sequence of operations that the GPU needs to perform. Once recorded, this sequence becomes a fixed graph that the GPU can execute autonomously, without requiring the CPU to issue each command individually.

In the participant's words, the CPU "kicks out the kernel commands" directly to the GPU for execution, saving the launch time, graph building time, and eliminating the need for the CPU to remain involved in the scheduling loop. The GPU effectively "executes what it has already been told to do," following the recorded graph.

### Recording and Non-Blocking Execution

When asked about the timing of the recording — whether it happens at fixed intervals (e.g., every second or millisecond) or when a certain number of instructions accumulate — the participant clarified that there is no interval-based triggering. The recording is performed in a **non-blocking** (non-blocking) manner.

To explain the blocking vs. non-blocking distinction: in a normal execution, when the CPU dispatches a kernel, it often blocks itself while waiting for the GPU to complete or for the next instruction. However, after recording a CUDA Graph, the GPU no longer needs to wait for the CPU to issue new commands; it simply replays the recorded graph. This eliminates the CPU bottleneck, allowing the GPU to execute more efficiently.

### How the GPU Communicates Results Back to the CPU

A follow-up question was raised: after the GPU finishes executing the recorded graph, how does it notify the CPU? The participant explained that the GPU returns the results directly to the CPU — it delivers the graph's output, enabling the CPU to handle post-execution tasks. There is still some coordination between the two, but the heavy lifting of command dispatching is offloaded.

### Why CUDA Graph Is Associated with Optimization

The participant emphasized that the core reason CUDA Graph accelerates performance is that the CPU is often blocked for too long during kernel launches. By moving the command dispatch responsibility to the GPU, the system avoids prolonged CPU stalls. Recording the graph generally yields speed improvements, as the CPU only needs to instruct the GPU once ("follow the usual habit") rather than repeatedly telling it what to do.

### Comparison with PyTorch's Approach

A key clarification was made regarding the difference between simply moving data to the GPU (e.g., using `tensor.to(device)` in PyTorch) and using CUDA Graph. Moving data to the GPU places the data in GPU memory, but the CPU still must issue every execution command. In a large model, the CPU might need to communicate with the GPU tens of thousands of times per inference run. CUDA Graph reduces this to a single recording step: "just tell the GPU once, and it remembers what to do."

## Memory Bandwidth, HBM, and Inference Bottlenecks

The conversation shifted to the broader challenge of memory bandwidth in inference, particularly the role of **High Bandwidth Memory (HBM)**.

### The Shift from Compute to Memory Bottlenecks

The participant noted that the industry has shifted its focus: the bottleneck in inference is no longer compute but rather memory — specifically, the bandwidth of HBM. When executing operators or moving data (especially model weights), the system requires high bandwidth. Weights, as opposed to general parameters, are the main consumers of memory during inference. (The participant distinguished between the two: parameters are typically handled by the CPU, while weights reside in GPU memory for inference.)

### Why Weights Consume So Much Space

Weights occupy large amounts of memory because large models have many layers (layers). The bandwidth of HBM — often rates like hundreds of GB per second or even TB per second — is still a limiting factor. The participant cited HBM3 as an example, offering up to 192 GB of VRAM, and noted that while TB-level bandwidth is theoretically reasonable for some very large models, GB-level bandwidth is generally sufficient for most current use cases. Training, however, tends to require greater bandwidth and is given higher priority.

## Inference Optimization Approaches: From Competition to Practical Techniques

When asked how the participant achieved a first-place finish in an earlier Baidu Xi'an competition (several years ago), they declined to provide specific details, citing the competition's non-disclosure rules: "It hasn't ended yet, so I can't make it public."

### Estimating Model Capacity on a Given GPU

The discussion then moved to a practical question: given a specific GPU (e.g., H100, H200, RTX 4090, RTX 3090), how do you estimate what size model can be run locally for inference? The participant explained that the primary factor is the available VRAM. For example, with 12 GB of VRAM, you are generally limited to running small or quantized models (e.g., GGUF format models of 5–6 GB or 7–8 GB). The context size (上下文字长度) is also critical: a model with a context of 100,000 tokens versus one with 10,000 tokens makes a huge difference. The quantization type (e.g., 4-bit vs. 8-bit) further affects the model's memory footprint. In practice, for a 12 GB card, the context size might be limited to around 2,048 tokens or up to 10,000, and anything beyond that requires optimization work — which the participant described as their specialty: "making it run on smaller devices."

### Distributed Inference Frameworks: vLLM and SGLang

The conversation turned to popular inference optimization frameworks. The participant described **vLLM** and **SGLang** (likely referring to SGLang or a similar project) as tools that perform distributed processing optimizations. They explained that these frameworks handle the isolation of user contexts — each user's prompt is kept separate — and perform basic batching at a low level. However, the participant noted that these frameworks are primarily designed for ease of deployment and are more suitable for "lazy" users who want out-of-the-box functionality. In contrast, handwritten optimizations (like those the participant performs) can be faster but are kept private by companies rather than open-sourced.

The participant also drew a contrast between single-user solutions like **llama.cpp** and multi-user server solutions like vLLM and SGLang. While llama.cpp is more common for individual use, server-facing deployments favor the latter two for their convenience.

### Understanding KV Cache

A detailed explanation of **KV Cache** was provided. The participant explained that "K" and "V" refer to the key and value components of the attention mechanism, which represent the context (context). Without KV Cache, when generating a new token, the model would need to re-examine all previous tokens from scratch. KV Cache stores the key and value states of previous tokens after they are computed, so that for each new token, the model only needs to compute attention based on the current token (or the last token) and the cached context. This eliminates the need to recompute the entire attention for every previous token with each new step.

The participant clarified that, while the high-level concept is straightforward — "the last token already knows the context" — the actual performance optimization details are more nuanced.

### Role of Flash Attention and Software Optimization

The group discussed **Flash Attention**, which the participant described as a technique that moves attention computation from general memory into **SRAM** (static random-access memory) and uses a tiled (block-based) approach. By processing attention in smaller blocks within SRAM, Flash Attention reduces memory consumption and maintains near-perfect precision. The participant explained that SRAM's key advantage is that it does not involve dynamic address creation — it provides stable memory access, which is highly beneficial for running CUDA Graphs.

When asked why Flash Attention uses tiling instead of simply moving everything to SRAM, the participant responded that SRAM is limited in capacity, so splitting the computation into smaller blocks is more efficient. The CPU is also better at handling block-based operations.

## The GPU Software Stack: TensorRT, cuDNN, cuBLAS, and Triton

The conversation then explored the broader GPU software ecosystem, from high-level frameworks down to extremely low-level libraries.

### TensorRT and cuDNN

**TensorRT** was described as a dedicated acceleration engine that integrates closely with CUDA Graph. It is faster than PyTorch's built-in acceleration because it is purpose-built for optimization. However, the participant noted that TensorRT is very difficult to use — "a very hard platform to work with, quite troublesome." In contrast, **cuDNN** is a library of accelerated operators (算子库), similar to **cuBLAS**, both of which accelerate linear algebra and matrix operations for AI workloads.

### cuBLAS and Low-Level Acceleration

The participant explained that cuBLAS is a matrix acceleration library, but its name is somewhat misleading — it is extremely fine-grained and accelerated specifically for NVIDIA cards. It can be significantly faster than standard CUDA programs written without it, because it operates at a very low level. There is also **cuBLAS LT** (currently in the experimental stage within PyTorch), which can be even faster than cuBLAS, though it is not yet stable.

### NVIDIA's Moat: Software, Not Hardware

A point was made that NVIDIA's competitive advantage lies not in hardware (which is already excellent) but in its software ecosystem. The participant agreed, noting that the software layer, including CUDA drivers and toolkits, is a major differentiator. The **CUDA driver** and the **CUDA toolkit** serve different purposes: the toolkit is used for development (writing code), while the driver is the underlying runtime that makes the toolkit's output executable.

### Triton (OpenAI's Triton)

When asked what comes to mind when thinking of CUDA, the participant mentioned "operator acceleration" and "operator fusion." They highlighted **Triton** (likely referring to OpenAI's Triton language) as a representative project. Triton is described as a language for writing GPU operators that is easier to use than standard CUDA. It allows developers to write code quickly and achieve 85% to 95% of the performance of hand-tuned CUDA, which would otherwise require days of debugging.

The participant noted that they use Triton more than raw CUDA, only resorting to CUDA when extreme optimization is required. Triton is now considered the industry's most standard operator fusion library — "currently the best and most widely used." It is ubiquitous in frameworks like SGLang.

## Personal Optimization Work: Philosophy, Scale, and Competitors

The participant shared insights into their own optimization work and the competitive landscape.

### Philosophy of Pursuing Extreme Speed

When asked why their optimizations are not simply available online (e.g., from projects like NanoGPT or NanoChat), the participant explained that while some code exists, it is rare. They prefer writing custom code for two reasons: it is faster than standard implementations, and they are driven by a philosophy of "pursuing extreme speed" (追求极致的速度). However, they emphasized that reducing layer depth (层级) is not the goal — reducing layers can harm precision. Instead, they aim for acceleration while maintaining high precision, often through techniques like pre-computation, fusing matrix operations, or moving CPU tasks to the GPU.

### The Role of `torch.compile`

The discussion touched on PyTorch's `torch.compile`. According to the participant, many mainstream model developers will tell you that `torch.compile` is the fastest way to accelerate PyTorch models. However, the participant disagreed, arguing that hand-written code is always faster because it is more targeted. `torch.compile` must handle many general cases and check for various conditions, which introduces overhead. The participant acknowledged that `torch.compile` is a powerful tool — it "does a lot of things" — but it lacks the customization needed for extreme optimization.

### Code Scale and Language

The participant's optimization code typically ranges from **500 to 2,000 lines**, all written in **Python** (not C++). If they were to use pure CUDA, the codebase would exceed 2,000 lines. The code is largely composed of Triton-based operator fusion for inference optimization.

### Competitive Landscape: Who Else Does This?

When asked whether they encounter other people with comparable levels of expertise in deep optimization, the participant responded: "Very few." Most competitors and engineers prefer using out-of-the-box solutions like vLLM, which is automated. The participant expressed skepticism about the trend of using AI tools (e.g., Cursor Copilot) to write code for competitions: "They use cloud code, they use AI to write — many people can produce results, but they don't understand the principles. That defeats the purpose of the competition." They noted that competition organizers sometimes review participants' resumes and code to verify authenticity; if a person with a weak resume suddenly gets first place, they may be scrutinized.

## Model Usage: Qwen Series and Gemini

The participant uses **Qwen (千问)** 2B for their optimization work, as a small model is sufficient for testing — "if it works for a small model, it works for a large one." They described Qwen as a series they admire for its open-source philosophy, including not only weights but also training and inference scripts.

For daily personal use, the participant uses **Gemini** (the closed-source Google model), which they find excellent even though they cannot download its weights for optimization.

## Action Items

- **Action item:** The participant will send the refined meeting notes back to the other party for review, as confirmed at the end of the conversation.
