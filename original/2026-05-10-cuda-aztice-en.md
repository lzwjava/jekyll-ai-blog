---
audio: false
generated: false
image: false
lang: en
layout: post
title: Exploring a Lightweight CUDA-Powered Deep Learning Library
translated: false
---

Two participants: [aztice](https://github.com/aztice) and [lzwjava](https://github.com/lzwjava).

The following conversation was transcribed using Whisper on an RTX 4070, then refined and organized with the help of AI tools. The original conversation was in Chinese.

Note: Because both transcription and refinement were AI-assisted, some details may be inaccurate or paraphrased. Please verify any important information independently before relying on it.

---

This meeting covered a broad technical discussion centered on a personal open-source project called [Axono](https://github.com/AxonoOfficial/Axono)—a lightweight, CUDA-accelerated tensor computation library that functions similarly to a minimal PyTorch. The conversation explored the library’s architecture, its CUDA kernel implementations, memory management between CPU and GPU, and the challenges of solo development. It also delved into the developer’s competitive AI engineering experience, including a notable 17th-place finish in an international big data competition ([IKCEST 2025](https://aistudio.baidu.com/competition/detail/1196/0/introduction)) and ongoing participation in a model optimization challenge where they currently rank 8th among 16 finalists. Along the way, the dialogue touched on tooling practices like AI-assisted coding, the rationale for switching from pure CUDA to CUBLAS in a V2 redesign, the choice of communication language between the participants, and the value of hands-on engineering over theoretical knowledge.

## The Axono Project: A Minimal PyTorch-Like Library in CUDA

### Project Overview and Motivation

The discussion began with one participant introducing a project called [Axono](https://github.com/AxonoOfficial/Axono), which lives in a GitHub organization. The developer described it as a lightweight inference library, noting that it supports multiple data precision types including int8, int16, int32, int64, float32, and float64. The library includes commonly used operators: matrix multiplication (matmul), addition, and simple activation functions. When asked whether it is a Python library like PyTorch, the developer confirmed that it is, but emphasized that development has slowed considerably because only one person is working on it—making progress exhausting.

The library is primarily designed for Linux, and while a Windows version exists on the machine being used for the demo, there is no official Windows packaging. The developer noted that the current release shown is version 1.0, but clarified that the showcased version is not the latest 1.0—it’s an older release. When asked how many versions have been published, the answer was roughly a dozen or two. The development environment is on a machine equipped with an NVIDIA V100 GPU.

### Current State and V2 Redesign

The conversation shifted to the project’s structure. The developer explained that the current codebase (around several thousand lines) is quite messy, which has motivated a complete rewrite for version V2. The V0 version has significant timing issues, so V1 is being developed from scratch to replace it. However, V1 is not yet complete because the entire process is quite troublesome. A key architectural change is that V1 will no longer support pure CUDA—it will force the use of CUBLAS. However, the developer noted that they might eventually provide compatibility for older devices that still need pure CUDA.

The group discussed a question about whether Axono could be used to write a small neural network like a digit classifier for MNIST. The library does not currently support a Linear layer—a key requirement for building such a model. The developer acknowledged this limitation but pointed out that since Axono has matrix multiplication, one could theoretically represent a Linear layer using arrays. It was agreed that this would be an interesting experiment, and one participant mentioned they would take the code and investigate whether a minimal MNIST implementation is possible despite the missing Linear abstraction.

### Tensor Operations and Shape Handling

One participant demonstrated how to declare a tensor variable and explore its shape. During a demo with matrix multiplication, they walked through an example: matrix A with shape (2, 3) and matrix B with shape (3, 2), noting that the result should have shape (2, 2). There was some confusion about broadcasting versus standard matrix multiplication—the developer clarified that the library does not fuse shapes directly; rather, it multiplies the inner dimensions and produces the outer ones as the result shape.

Regarding shape transformations, the developer stated that currently, only a transpose method is provided. There is no general reshape or shape-change method available. The transpose implementation simply flips rows and columns (A[i][j] becomes A[j][i]), but the code for this is relatively lengthy. When asked about higher-dimensional tensors, the library only supports 2-dimensional transposition—it does not handle multiple dimensions being transposed simultaneously. The developer noted that the convention is to pass two dimensions (dim0 and dim1) explicitly.

### CUDA Implementation: From CPU to GPU and Back

#### The Kernel Launch Pipeline

The developer explained the underlying CUDA implementation, starting with matrix multiplication. The process begins by allocating memory, setting up a launch configuration, and then calling a kernel. Inside the kernel, a simplified computation loop over rows and columns produces the result. The library includes optimizations: one kernel is called `matmul_optimized` with a column tile approach designed to make the overall computation run faster.

To optimize performance, the developer uses block sizes and shared memory. Specifically, they move block size parameters into a temporary template, pulling data into shared memory tiles to accelerate matrix multiplication. The tile concept involves splitting each matrix into small blocks (tiles) for more efficient computation—similar to the tiling technique used in Flash Attention.

#### Shared Memory and Kernel Structure

One participant asked for an explanation of shared memory in this context. The developer confessed they don’t have a perfect intuitive explanation, describing it as a technique to load matrix tiles into shared memory—a faster memory space on the GPU—to speed up repeated accesses. The code also includes boundary checks to ensure indices stay within source and destination tensor bounds. The `idx` variable is used to compute positions in both source and destination tensors for transpose operations.

The trace of the matrix multiplication code showed that the library checks tensor shape compatibility before launching the kernel. A `calculate_launch_config` function computes grid size and block size. The block size is set to 256. The grid size formula uses an “upward rounding” approach: `(num_elements + block_size - 1) / block_size`. One participant initially questioned this formula, wondering why `num_elements` isn’t simply divided by `block_size`. The developer explained that the `+ block_size - 1` trick ensures integer ceiling division—when the number of elements is not evenly divisible, this formula rounds up to allocate enough blocks. This is a common technique in competitive programming (OI) and general GPU kernel design.

#### Memory Transfers Between CPU and GPU

The conversation deepened on how data moves between CPU and GPU. The developer described that during kernel execution, data is “thrown into” the kernel directly—this is the transfer process. When asked which library handles this transfer, the developer said it is their own custom wrapper. However, they clarified that the data does not actually move from CPU to GPU at kernel launch time; the tensors are initialized and allocated on the GPU from the start. What gets passed to the kernel is just the pointer to the GPU memory. The kernel then operates directly on that GPU-resident data.

The developer drew an analogy: CPU uses a pointer to call GPU functions, and the GPU kernel accesses that memory through the provided pointer. They emphasized that GPU and CPU operate separately—CPU cannot directly access GPU memory, so CUDA (or CUBLAS) provides the mechanism to call GPU functions. After GPU computation finishes, data can be transmitted back to CPU for display or further processing. The term “sync” (or “sink”) was discussed: sometimes CPU must sync with GPU, waiting for the GPU to complete its task before proceeding. In PyTorch, many processes are asynchronous by default, but explicit sync operations ensure data integrity and avoid errors. The group agreed that the operational system is primarily CPU-driven, and GPU results must be brought back to CPU for user-facing output or subsequent steps.

### Code Walkthrough: Key Components

#### The Dispatch_Fill Pattern

The group examined a `dispatch_fill` function in the codebase. Its purpose is to fill a tensor with specific values. It works by dispatching based on data type—different types map to different internal implementations, essentially achieving a form of generic programming in C++. The function calculates launch configuration, then fills values into the tensor’s data pointer. A `memory_copy` step is involved: one version uses a source pointer and a `fill_value` to copy data from one location to another. The developer confirmed that `tensor.data` is simply a raw pointer, not a library object.

#### Element-Wise Addition Kernel

The developer showed an element-wise addition kernel. This kernel performs per-element addition: for each index `idx`, it computes `result[idx] = a[idx] + b[idx]`. This is a straightforward parallel pattern where each thread handles one element. The kernel includes a constraint: only compute if `idx` is less than `num_elements`, acting as a guard against out-of-bounds access. The developer noted that for understanding such detailed concepts, they often prefer to copy the code to an AI tool and ask for an explanation rather than memorizing the details themselves.

#### The Transpose Kernel

The transpose CUDA kernel code was examined in detail. The kernel handles 2D transposition with parameters for source, destination, dimension sizes, source stride, destination stride, and dimension indices (dim0, dim1). The computation uses `idx` to compute coordinates, then calculates source and destination indices by multiplying coordinates by strides and adding offsets. The `remainder` operation is used to compute the remaining dimension during index calculation. The developer noted that the kernel includes handling for INF (infinity) values—when a value exceeds representable range, it produces INF rather than causing an error, which is acceptable behavior.

### Development Practices: AI Assistance and Code Review

The developer candidly stated that most of the CUDA kernels were written with AI assistance—they would not hand-code all of this from scratch because it would be too exhausting. However, they emphasized that they clearly understand what each piece of code does. Using AI still requires iteration: adjusting prompts, dealing with compilation errors, debugging, and ensuring correctness. They typically ask the AI to generate 50-100 lines at a time rather than entire components at once, and then fix small bugs as they arise. One participant commented that the code structure looks very polished, and the developer’s approach is impressive given the complexity.

## Competitive AI Engineering and Model Optimization

### The IKCEST 2025 Competition: 17th Place Out of 1,700 Teams

The developer shared their experience in the [IKCEST 2025](https://aistudio.baidu.com/competition/detail/1196/0/introduction) international big data competition, where they achieved 17th place out of approximately 1,700 participating teams. The competition requires team registration with school information—the team must include at least one currently enrolled student from the registered institution. The developer participated as a team from Hong Kong, using their school affiliation.

The developer presented their competition PPT. The team name was “everywhere we go” (with a small typo in the original slide). The developer acknowledged difficulty finding reliable teammates in Hong Kong; they do not personally know others with similar interests. For a subsequent competition, they have teamed up with a graduate student who can provide meaningful help, unlike typical undergraduates.

### Competition Workflow and Technical Approach

The competition involved a problem requiring answers to be derived from figure inputs. The developer’s pipeline used OCR recognition as the first step, specifically PPOCR (PaddleOCR from Baidu’s PaddlePaddle framework). They noted that in Hong Kong, many people dislike domestic Chinese tools and prefer Western alternatives, but the developer uses PaddleOCR without such bias and finds it works well. The OCR results produced string extractions, and the team combined this with a detection network (similar to YOLO) to locate text regions before recognition.

The leaderboard metrics during the competition included an accuracy score (0.47381 in one example), recorded on October 27th. The developer noted that the exact metric details were somewhat forgotten but represented recognition results and string extraction quality. The competition’s top-performing team used multiple optimization tricks to achieve much faster inference speed, though the developer couldn’t recall all their specific techniques.

### Current Competition: Model Serving Optimization

The developer is currently participating in another competition focused on model serving optimization. This competition started with around 480 teams, which were quickly reduced to 16 finalists after a single elimination round. The developer’s team is ranked 8th among these 16 finalists, using the team name “forgive me out.” Their teammate is a graduate student from East China Normal University.

The competition metrics include accuracy (with a cap at 0.7—scores above 0.7 are treated as 1.0, and most teams easily achieve 0.7), TTFT (Time to First Token), and throughput (tokens per second). The developer identified TTFT and throughput as the truly difficult metrics—accuracy is essentially a given. They have submitted 54 cumulative submissions over a period of about one month, with 27 submissions counted for the ranking. Their throughput score is 38 (on whatever scale the competition uses). The top-ranked team leads across all three metrics.

For this competition, the developer wrote the solution from scratch by hand, reasoning that AI-generated code is too error-prone for this kind of work. It took them about two weeks to write the model into a graph representation that could be deployed. They are currently in the final stage, and the top three teams will advance to a final event in Vietnam.

### Measuring Engineering Skill: The Ultimate Test

When asked what constitutes a high level of engineering competence in this domain, the developer offered a concrete benchmark: successfully writing a multi-modal language model (like Qwen-VL-2B or similar) from scratch and deploying it into a Kubernetes cluster. This requires deep understanding of attention mechanisms and the ability to handle the constraints of CUDA kernels—for instance, no dynamic shapes allowed; everything must be stable. The developer stated that achieving this would indicate a skill level roughly equivalent to theirs, emphasizing that this is genuinely difficult and requires years of dedicated work.

### Language Choice for Communication

The participants experimented with switching to English during the discussion, but encountered challenges. While both were capable of English communication, the technical vocabulary (especially CUDA-specific terms) caused comprehension difficulties. One participant noted that their spoken English vocabulary is stronger in conversational contexts than in technical jargon, so they sometimes struggled when unfamiliar technical terms were used in English. They agreed that Chinese communication is roughly twice as efficient as English for these technical discussions, acknowledging that improving English proficiency is valuable for international platforms and future career growth. They decided to continue primarily in Chinese for this conversation, with the intention of practicing English more over time.

## Personal Background, Future Plans, and Broader Interests

### Learning Journey and Technical Breadth

The developer has been working on these systems for about three years. Their knowledge extends beyond just neural network algorithms—they understand a wide range of topics including multi-modal models (VLMs), detection models, and OCR pipelines. They described their expertise as “broad but messy,” acknowledging that they explore widely rather than specializing deeply in a single area. In addition to the Axono library, their GitHub includes older projects: a small PHP-based project, a JSON database experiment, and a very early project from when they first started learning Python. The GitHub organization they run is something they established a long time ago; it is essentially a solo operation.

### Upcoming Commitments

The meeting occurred in May. The developer mentioned they need to travel to City University of Hong Kong later that day—they are currently in Shenzhen and plan to cross the border. They have visited many Hong Kong university campuses (Chinese University of Hong Kong, Hong Kong University, Hong Kong Polytechnic University, HKUST), sometimes for classes and sometimes for events with friends. When asked about the general skill level of students at those institutions, they declined to offer a direct evaluation, noting that in their experience, many students are average and may not be able to outperform them in practical competition settings.

### Interest in Collaboration

One participant expressed interest in collaborating on competitions, believing their infrastructure background could complement the developer’s strengths. The developer responded candidly: they feel the participant is “not quite qualified yet” for the level required in big data infrastructure competitions, noting that these competitions demand both strong systems knowledge and algorithmic skills. However, they offered a clear path: if the participant can successfully write a multi-modal LLM from scratch and deploy it into a Kubernetes cluster themselves, that would demonstrate equivalent ability. The developer acknowledged that they would be willing to work together once that level is reached.

## Concluding Thoughts

The conversation wrapped up after covering substantial technical ground. The participants acknowledged they had discussed a lot, with one suggesting they might take a break. The developer’s need to prepare lunch before heading to Hong Kong provided a natural stopping point. The meeting concluded on a friendly note, with an informal invitation to stay in touch and perhaps meet in person across the border in the future.

---

Project link: [Axono on GitHub](https://github.com/AxonoOfficial/Axono)
