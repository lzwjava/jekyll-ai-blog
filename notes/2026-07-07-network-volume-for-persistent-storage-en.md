---
audio: false
generated: true
image: false
lang: en
layout: post
title: Network Volume for Persistent Storage
translated: false
type: note
---

Question: RunPod storage: choose **Volume Disk** or **Network Volume**?

Answer:

For most serious workloads (models, datasets, deployments), choose **Network Volume**.

Comparison:

|                     | Volume Disk                              | Network Volume                         |
| ------------------- | ---------------------------------------- | -------------------------------------- |
| Scope               | Single Pod only                          | Shared across Pods                     |
| Lifetime            | Tied to Pod lifecycle                    | Independent of Pods                    |
| Delete Pod          | Data deleted                             | Data remains                           |
| Move to another GPU | No                                       | Yes                                    |
| Multiple Pods       | No                                       | Yes                                    |
| Startup speed       | Fast (local disk)                        | Slightly slower                        |
| Cost                | $0.10/GB/mo running, $0.20/GB/mo stopped | Usually cheaper for long-lived storage |
| Best for            | Temporary cache                          | Models, datasets, production           |

For your use case:

* SGLang
* LibreChat
* LLM weights (7B/14B/30B)
* model cache
* training data
* scripts you want to reuse

→ **Network Volume is the right choice.**

Typical setup:

```
RunPod Network Volume
        |
        mounted at
        |
    /workspace

        |
        +-- models/
        |     +-- llama/
        |     +-- qwen/
        |
        +-- datasets/
        |
        +-- scripts/
        |
        +-- configs/
```

Then you can:

1. Create Pod A with RTX 4090
2. Download models:

```bash
cd /workspace
huggingface-cli download Qwen/Qwen3-8B --local-dir models/qwen3-8b
```

3. Delete Pod A.

Later:

4. Create Pod B with A6000/H100/RTX 2000 Ada
5. Attach the same Network Volume
6. Models are already there.

For AI development, the pattern is:

```
Network Volume = persistent state
Pod = disposable compute
```

Similar to:

```
Docker container  -> Pod
Docker volume    -> Network Volume
```

I would avoid putting anything important in `/workspace` on the normal Volume Disk.

For your current RunPod setup (SGLang + LibreChat chatbot), I would use:

```
Network Volume: 50-200GB
    /workspace/models
    /workspace/huggingface-cache
    /workspace/projects
```

Then recreate Pods freely when changing GPUs.
