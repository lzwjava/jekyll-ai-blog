---
audio: false
generated: false
image: false
lang: en
layout: post
title: "A Conversation on GPU Optimization for LLM Inference"
translated: false
---

Two participants: [aztice](https://github.com/aztice) and [lzwjava](https://github.com/lzwjava).

Aztice — Hong Kong secondary school student, lead developer of Axono (a lightweight AI inference library). Participated in the 2024 6th IKCEST "Belt and Road" International Big Data Competition and the 10th Baidu & Xi'an Jiaotong University Big Data Competition, ranking 17th out of 1,700+ team members. Multiple years of experience in AI Infrastructure. GitHub: [@aztice](https://github.com/aztice) , WeChat@awalightice.

The following conversation was transcribed using Whisper on an RTX 4070, then refined and organized with the help of AI tools. The original conversation was in Chinese.

Note: Because both transcription and refinement were AI-assisted, some details may be inaccurate or paraphrased. Please verify any important information independently before relying on it.

---

# Summary: CUDA Graph Inference Optimization and Model Acceleration Discussion

This meeting covered an in-depth discussion on CUDA Graph principles, inference optimization techniques, model acceleration toolchains, and related competition progress. The main topics included: CUDA Graph recording and execution mechanisms, memory bandwidth bottlenecks in inference optimization, KVCache working principles, comparisons of acceleration tools like TensorRT and Triton, Flash Attention's tiling strategy, as well as personal practical experience and optimization philosophy from model optimization competitions. The meeting also touched on commonly used models (such as the Qwen series) and daily AI tools (such as Gemini).

## Competition Progress and Background

At the beginning of the meeting, recent competition participation was discussed. It was previously mentioned that someone ranked first in a competition, but that competition had not yet concluded. The full name of the competition is "Baidu CTI," which is still ongoing, and the organizers no longer display rankings. The competition involves inference optimization tasks, where participants must submit code and a self-introduction. The organizers review participants' qualifications, including whether the code was AI-generated and their technical level. If the submitted results do not match the resume's level, further review may be conducted.

## CUDA Graph Principles and Understanding

### Core Concept: Recording and Execution

The core idea of CUDA Graph is to record the kernel instructions that the CPU launches to the GPU, forming a "graph," after which the GPU can directly execute this graph without the CPU repeatedly issuing instructions. Specifically, during normal model execution, the CPU needs to notify the GPU multiple times to perform various operations (such as floating-point computations), each time waiting for the CPU to issue instructions, which causes CPU blocking. CUDA Graph, through recording, completely captures what the CPU tells the GPU to do, after which the GPU can automatically execute following the "habit," and the CPU no longer needs to participate in the instruction issuance process.

### Recording Mechanism and Blocking Issues

The recording process is non-blocking, with no fixed time interval or instruction count threshold. After recording is complete, the GPU no longer needs to wait for the CPU to issue instructions during execution, but directly executes the previously recorded instruction sequence. During the recording phase, the CPU receives an ID or completion marker, rather than actual execution results. After the GPU finishes executing the graph, it directly reports the results back to the CPU, completing the collaboration.

### Applicable Scenarios and Optimization Value

CUDA Graph is not applicable to all CPU instructions, but mainly targets matrix operations and floating-point computations that GPUs excel at. Its optimization value lies in: during normal model execution, the CPU may need to communicate with the GPU tens of thousands of times (each time telling the GPU what to do), but after recording a CUDA Graph, the CPU only needs to tell the GPU once to "follow previous habits," thereby significantly reducing CPU blocking time and achieving acceleration. This acceleration effect is generally observable after recording is complete.

### Relationship with PyTorch

PyTorch provides automated compilation tools like `torch.compile`, but CUDA Graph is a more fundamental optimization approach. PyTorch's compilation is automated, while CUDA Graph requires manual recording and customization. Although PyTorch's compilation is powerful, it lacks specificity and has limited customization. Manually written optimization code is generally faster than PyTorch's automatic compilation because it can make the most direct optimizations for specific scenarios, whereas PyTorch needs to check and handle multiple cases.

## Memory Bandwidth Bottlenecks in Inference Optimization

### Weight Movement and Bandwidth Requirements

The bottleneck in inference optimization has shifted from computational capability to memory bandwidth, particularly the bandwidth limitations of High Bandwidth Memory (HBM). When executing operators, weight movement requires substantial bandwidth. Large model weights occupy significant space because models have many layers, requiring HBM to provide hundreds of GB/s or even TB/s of bandwidth. HBM3 provides 192 GB of VRAM, and TB-level bandwidth is reasonable for very large models, but GB-level is usually sufficient for general use. Training scenarios have greater bandwidth requirements and higher priority.

### Inference Model Scale Analysis

The size of a model that can run for inference mainly depends on VRAM. For example, 12 GB of VRAM is generally only for inference (not training), and can load GGUF quantized models of 5–6 GB or 7–8 GB. However, context size is also critical: there is a significant difference in VRAM usage between 100K tokens and 10K tokens of context length. Quantization type (4-bit vs. 8-bit) also affects model size. Typically, with 12 GB of VRAM, context length may only support 2048 or under 10,000 tokens. One of the tasks of optimization engineers is to enable models to run on smaller devices.

## KVCache Working Principles

KVCache is a key optimization technique in large model inference. During normal inference, to generate the next token, all previous tokens need to be re-inferred. With KVCache, only the previous token needs to be inferred, without all tokens participating in computation. Because the previous token already has various context information bound to it (through K and V caches), the cached results can be directly utilized, saving the overhead of recalculating all preceding tokens. However, at the detailed level of performance optimization, the actual mechanism differs from this simplified understanding, though the concept is similar.

## Inference Optimization Toolchain

### TensorRT and cuDNN

TensorRT is an acceleration engine tied to CUDA Graph, offering better acceleration than PyTorch because it provides targeted optimization. However, TensorRT is very difficult to use and cumbersome to operate. cuDNN is an operator library, similar to cuBLAS, specifically designed to accelerate linear computation and other operations for big data and AI scenarios.

### cuBLAS and cuBLAS LT

cuBLAS is a matrix acceleration library specifically designed for NVIDIA GPUs, much faster than ordinary CUDA programs because it may utilize very low-level instructions. cuBLAS LT is an experimental product, still in experimental stages in PyTorch, but can be faster than cuBLAS.

### Triton Language

Triton is a simplified version of CUDA, an operator fusion language that can also run on AMD devices. It is easier to use than native CUDA — write and debug immediately, typically achieving 85%–95% of native performance. Triton is currently the industry's most standard operator fusion library, ubiquitous in open-source frameworks like SGLang and vLLM. Daily work primarily uses Triton, only resorting to direct CUDA when extreme optimization is needed.

### vLLM and SGLang

vLLM and SGLang are similar inference optimization frameworks, primarily focused on distributed processing optimization. They can help pre-process across multiple devices, achieving distributed optimization. vLLM is suitable for multi-user scenarios, convenient for deployment, and ready to use out of the box. However, manually optimized code is typically faster than vLLM, though it won't be publicly documented — generally kept private within companies. LLaMA.cpp is more suitable for single-user scenarios.

## Flash Attention's Tiling Strategy

Flash Attention optimizes attention's linear matrix computation from quadratic complexity by placing data in SRAM (static memory) and using a tiling approach, keeping memory usage from increasing too much while maintaining near-perfect precision. The reason for tiling is that SRAM space is limited and cannot hold all data at once, and CPUs excel at breaking tasks into chunks. SRAM is static memory where addresses do not change dynamically, which is also helpful for running CUDA Graph.

## Personal Optimization Practice and Philosophy

### Optimization Methods and Code Scale

Optimization work is primarily written in Python, typically between 500 and 2,000 lines of code. If written directly in CUDA, the code exceeds 2,000 lines. Optimization pursues extreme speed while ensuring high precision. Acceleration methods include: fusing matrix operations, moving CPU work to the GPU, pre-computing some content, and using CUDA Graph to record graphs and hand them to the GPU for execution. During optimization, layers are reduced as much as possible, but not arbitrarily to avoid affecting precision.

### Commonly Used Models and Tools

Gemini is used daily (not open-source, used directly online). Optimized models include the Qwen series (2B, 8B, 27B, 128B, etc.) and some sequence models. The Qwen series has open-sourced weights, training scripts, and inference scripts, and is highly regarded. Optimization typically uses small models (e.g., 2B), because if a small model can be optimized well, large models certainly can be.

### Views on Automation Tools

Many participants currently prefer using automation tools (such as Claude Code, AI-written code), but this is believed to miss the true spirit of competition — lacking the spirit of understanding underlying principles. The organizers review participants' qualifications, including whether code is AI-generated and personal backgrounds. If someone with an ordinary resume wins first place, they may be questioned, but the first-place achievement itself should be respected.

### Industry Seniority

In the field of inference optimization, it is rare to encounter someone more senior, because most people prefer using ready-made tools like vLLM rather than optimizing themselves. It is difficult to judge their true level, as very few people work on low-level optimization themselves.

## NVIDIA's Moat and Hardware Ecosystem

NVIDIA's moat lies not only in hardware but more so in the software ecosystem. Hardware is already excellent, and software takes it to another level. CUDA has two layers: driver and toolkit — the toolkit is for developers, and the driver is the underlying runtime environment for the toolkit. PyTorch is just a wrapper calling CUDA, a higher-level differentiable framework. NVIDIA's software products (such as CUDA, cuDNN, TensorRT) are very convenient to use. With proper optimization, NVIDIA's general-purpose chips can achieve inference speeds of 500 tokens/s or even higher, rivaling custom chips like Groq, though custom chips (such as FPGAs) are generally faster.

## Action Items

**Action item:** [Meeting note-taker] to send the organized meeting notes to participants.

---

# Detailed Description

They discussed the recent competition and the participant's performance. One participant asked the other to briefly show their recent results and how the competition was going, specifically the one where they had claimed to be ranked first but the results hadn't been released yet. It was clarified that the competition was not over and currently did not display rankings. Someone asked if it was the Baidu competition, and the other confirmed it was. They asked for the full English name of the competition, and it was identified as Baidu CTI, noting that it didn't have an English name.

The conversation turned to CUDA Graph. One participant mentioned that they had been further understanding CUDA Graph, specifically how it works. They discussed how CUDA Graph works: it records the kernels that the CPU would normally launch to the GPU, allowing the GPU to execute them directly without CPU involvement. One participant asked whether the graph was a real data structure or just a concept, and the other explained that it is a recording of CPU calls to the GPU, which are then fixed into a graph. When the GPU runs next, it no longer needs the CPU to issue instructions; the CPU can step away, and the GPU handles everything. There was a question about how the recording interval is specified—whether it's every second, every millisecond, or based on a certain number of instructions. The response was that there is no interval; it executes in a non-blocking manner.

One participant admitted they didn't understand blocking versus non-blocking, and the other explained that normally, running a graph would cause blocking because the CPU has to wait to issue instructions, but after recording a CUDA graph, the GPU no longer needs to wait for the CPU and can directly execute previously recorded instructions. One participant asked how the GPU notifies the CPU after execution, and it was explained that the graph results are directly handed back to the CPU, which then proceeds with subsequent tasks. It was noted that not all CPU instructions are recorded into the CUDA graph—only certain ones, particularly those involving matrix and floating-point operations that the GPU handles well. One participant asked why CUDA graph is often associated with optimization, and the other explained that it accelerates performance because CPU blocking takes too long; after recording, it generally speeds things up. There was a discussion about why one would need to deal with such a low-level concept as CUDA graph instead of simply moving data to the GPU via PyTorch. The response was that even after moving data to the GPU, the CPU still has to issue commands thousands of times when running a model, but with CUDA graph, the CPU only needs to tell the GPU once, and the GPU records and repeats the operations automatically.

They then discussed the concept of weight and parameters in large models. One participant asked about the difference between weight and parameters, and it was clarified that parameters are generally handled by the CPU, while weights are the GPU's concern. Weights occupy a large amount of space due to many layers and require high-bandwidth memory (HBM), with speeds in the hundreds of GB/s or even TB/s. It was noted that HBM3 provides 192 GB of VRAM, and while TB-level speeds are reasonable for very large models, GB-level speeds are usually sufficient for inference, though training requires higher priority.

The conversation moved to the participant's previous competition win, where they optimized inference. When asked what techniques allowed them to rank first, they replied that the competition was not yet over and the details could not be disclosed. One participant then asked how to analyze what size of local model a given GPU (e.g., H100, H200, 4090, 3090) can handle for inference. The response was that it mainly depends on the available VRAM. For example, with 12 GB of VRAM, one can only run small models or quantized models, and the context length is also critical—10,000 tokens versus 100,000 tokens makes a big difference, as does the quantization type (e.g., 4-bit vs. 8-bit). Models around 5–8 GB can be loaded via GGUF, but larger models won't fit, and context size may be limited to 2048 or under 10,000. Optimizing for smaller devices is part of their work, using techniques like Flash Attention.

They discussed vLLM and SGLang. One participant asked about the principles behind SGLang and why it can significantly reduce KV cache usage. The other explained that SGLang is similar to vLLM and provides distributed processing optimization, handling multiple devices by pre-processing and isolating each user's memory. It was noted that such frameworks are generally tied to math companies and don't require special attention, as batch processing and user isolation are handled by the underlying framework. One participant asked why vLLM and SGLang are used for public-facing servers while Llama.cpp is more single-user, and the response was that vLLM and SGLang are more convenient for deployment, though custom optimizations can be faster but are usually kept private by companies.

They then discussed KV cache. One participant asked what K and V refer to and how much optimization is possible. The other explained that KV cache refers to the context; without it, to infer a new token, you need to re-process all previous tokens, but with KV cache, you only need the previous token's cached information, saving that step. One participant clarified that the previous token already contains bound context information, so you only need to look it up to generate the next token. The other agreed that this is conceptually similar, though performance optimization reveals differences.

The conversation turned to Flash Attention. One participant mentioned that the author of Flash Attention claimed that software optimization on general-purpose NVIDIA hardware can achieve 500 tokens per second for models like DeepSeek V4, rivaling custom chips like Groq's. The other agreed that custom chips like FPGAs are generally faster, but NVIDIA hardware with proper optimization can be very competitive. They briefly mentioned that Groq's company may have been acquired by NVIDIA, but the participant was not sure. One participant asked if NVIDIA chips with suitable optimization can indeed reach 500 tokens per second or even higher, and the other affirmed that NVIDIA's technology is good, aside from being expensive.

They discussed TensorRT and cuDNN. One participant asked what these tools do, and the other explained that TensorRT is an acceleration engine that is also tied to CUDA graph, and it is faster than PyTorch because it is specifically optimized for acceleration, though it is very difficult to use. cuDNN is a library of accelerated operators, similar to cuBLAS, designed for linear algebra and AI acceleration. One participant noted that cuBLAS appears frequently and asked why many operations ultimately rely on it. The other explained that cuBLAS is a matrix acceleration library specifically for NVIDIA GPUs, much faster than ordinary CUDA code, and cuBLASLt (cuBLAS Light) is a more flexible API that can be even faster. One participant observed that CUDA itself is already a high-level API, and the other agreed, adding that they appreciate NVIDIA's acceleration products for their ease of use. They discussed NVIDIA's moat, noting that it lies more in software than hardware. One participant asked about the difference between the CUDA driver and the CUDA toolkit, and the other clarified that the toolkit is for developers, while the driver is the underlying foundation that the toolkit requires to run.

They then talked about Triton. One participant asked what projects come to mind when thinking of CUDA, and the other mentioned operator acceleration and operator fusion, which they used in competitions. They noted that vLLM uses such techniques, though it depends on PyTorch. One participant asked what Triton is, and the other explained that it is a simplified version of CUDA that can also run on AMD devices. It is a language for writing operators, easy to use, and typically achieves 85–95% of native CUDA performance, though native CUDA requires more debugging. One participant asked if people who are very skilled at CUDA work at NVIDIA or at companies like OpenAI, and the other agreed, but noted that they personally use Triton more than CUDA, only resorting to CUDA for extreme optimization. They confirmed that Triton is currently the most standard operator fusion library and is widely used in open-source frameworks like SGLang.

The conversation shifted to Mixture of Experts (MoE). One participant asked about the latest developments in MoE and SFT, and the other said they had some understanding from doing inference acceleration. They explained that each expert produces an output, which is then aggregated into a final logit, but they were not familiar with how experts are divided (e.g., finance vs. programming) as they focus on acceleration rather than research. One participant asked what models they commonly use for inference acceleration, and the other replied that it depends on the competition, but they use models like the Qwen series and some sequence models. For daily use, they use Gemini, which is not open-source but is convenient for helping with their work. They do not optimize Gemini; they optimize open-source models like Qwen.

One participant asked why the participant's optimizations are not available online and why they have to write custom code. The other explained that while some optimizations exist online, they are rare, and custom code is faster than standard implementations because they pursue extreme speed while maintaining high precision. They do not reduce layers to avoid affecting precision. One participant asked if the acceleration involves fusing matrix operations, moving CPU tasks to the GPU, or pre-computing. The other confirmed that pre-computation is common, and that CUDA graph requires recording the graph first. They discussed PyTorch's compile feature, noting that while mainstream models often claim PyTorch compile is fastest, hand-written code is always faster because it is more targeted and avoids overhead. However, they acknowledged that PyTorch compile is a powerful tool, though less convenient for customization.

They discussed Flash Attention again. One participant asked why Flash Attention uses a tiling approach to move attention computation from quadratic memory to SRAM. The other explained that SRAM is static memory that does not move addresses, which is helpful for running graphs. When asked why tiling is necessary instead of moving everything to SRAM at once, the other said it is because SRAM cannot hold everything, and the CPU is better at handling things in chunks. One participant asked if the participant aspires to create similar hardware-level optimizations for inference, and the other said it is possible, but they are currently focused on model optimization.

They discussed the Qwen model series. One participant asked what size of Qwen the other runs, and the response was 2B, because a small model is sufficient for optimization—if it works on a small model, it will work on a large one. They confirmed that they use Triton to write custom inference code with operator fusion for optimization. One participant asked if their optimized code is faster than Llama.cpp or vLLM, and the other said it is generally faster, though vLLM is more convenient and general-purpose. The custom code is typically 500 to 2,000 lines of Python, with CUDA code being longer. One participant asked if the participant encounters many people more senior in this area, and the other said very few, as most people prefer using vLLM or automated tools like Claude Code, which they feel misses the true spirit of competition. They noted that the competition organizers review submissions to check if code is AI-generated and assess the participant's background, so even if someone wins first place with a weak resume, they might be scrutinized.

The conversation concluded with one participant thanking the other and saying they would organize the notes and send them over. The other agreed and said goodbye.
