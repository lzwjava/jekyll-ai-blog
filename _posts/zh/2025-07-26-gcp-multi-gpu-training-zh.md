---
audio: false
generated: true
lang: zh
layout: post
title: 基于NVIDIA GPU在GCP平台训练机器学习模型
translated: true
type: note
---

Google Cloud Platform (GCP) 通过 Vertex AI（用于托管训练任务）和 Compute Engine（用于自定义虚拟机）等服务，为使用 NVIDIA GPU 训练机器学习模型提供了强大的选项。然而，GCP 不提供 NVIDIA RTX 4090 GPU。RTX 4090 是主要面向台式机和游戏的消费级 GPU，并非为云数据中心设计。相反，GCP 提供企业级 NVIDIA GPU，例如 A100、H100、L4 等，这些 GPU 针对 AI 工作负载进行了优化，并且由于更高的内存带宽和张量核心效率，在训练场景中通常优于 RTX 4090。

对于多 GPU 设置（至少 2 个 GPU），您可以根据机器类型配置资源以使用 2、4、8 或更多 GPU。为简单起见，我将重点介绍 Vertex AI，因为它专为 ML 训练而设计并能自动处理扩展。如果您需要更多控制，我将简要介绍 Compute Engine。

## 先决条件
- 设置 Google Cloud 账户并创建项目。
- 在您的项目中启用 Vertex AI API 和 Compute Engine API。
- 安装 Google Cloud SDK (gcloud CLI) 和 Vertex AI SDK（如果使用 Python）。
- 在 Docker 容器中准备您的训练代码（例如，使用支持分布式训练如 Horovod 或 torch.distributed 的 TensorFlow 或 PyTorch）。
- 确保您的模型代码支持多 GPU 训练（例如，通过 PyTorch 中的 DataParallel 或 DistributedDataParallel）。

## 使用 Vertex AI 进行多 GPU 训练
Vertex AI 是 GCP 用于 ML 工作流程的托管平台。它支持自定义训练任务，您可以在其中指定具有多个 GPU 的机器类型。

### 支持至少 2 个 GPU 的可用 GPU 类型
常见的支持至少 2 个 GPU 附件的 NVIDIA GPU：
- NVIDIA H100（80GB 或 Mega 80GB）：适用于大型模型的高性能 GPU；支持 2、4 或 8 个 GPU。
- NVIDIA A100（40GB 或 80GB）：广泛用于训练；支持 2、4、8 或 16 个 GPU。
- NVIDIA L4：适用于推理和较轻训练任务，性价比高；支持 2、4 或 8 个 GPU。
- NVIDIA T4 或 V100：较旧但仍可用；支持 2、4 或 8 个 GPU。

完整列表包括 GB200、B200、H200、P4、P100——请检查区域的可用性，因为并非所有区域都提供全部型号。

### 创建至少使用 2 个 GPU 的训练任务的步骤
1. **准备您的容器**：构建一个包含您训练脚本的 Docker 镜像，并将其推送到 Google Container Registry 或 Artifact Registry。PyTorch 的示例 Dockerfile：
   ```
   FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime
   COPY train.py /app/train.py
   WORKDIR /app
   CMD ["python", "train.py"]
   ```

2. **使用 gcloud CLI 配置任务**：
   - 创建一个 `config.yaml` 文件：
     ```yaml
     workerPoolSpecs:
       machineSpec:
         machineType: a3-highgpu-2g  # 示例：2x H100 GPU；备选：a2-ultragpu-2g (2x A100), g2-standard-24 (2x L4)
         acceleratorType: NVIDIA_H100_80GB  # 或 NVIDIA_A100_80GB, NVIDIA_L4
         acceleratorCount: 2  # 至少 2
       replicaCount: 1
       containerSpec:
         imageUri: gcr.io/your-project/your-image:latest  # 您的 Docker 镜像 URI
     ```
   - 运行命令：
     ```bash
     gcloud ai custom-jobs create \
       --region=us-central1 \  # 选择具有 GPU 可用性的区域
       --display-name=your-training-job \
       --config=config.yaml
     ```

3. **使用 Python SDK**：
   ```python
   from google.cloud import aiplatform

   aiplatform.init(project='your-project-id', location='us-central1')

   job = aiplatform.CustomJob(
       display_name='your-training-job',
       worker_pool_specs=[
           {
               'machine_spec': {
                   'machine_type': 'a3-highgpu-2g',  # 2x H100
                   'accelerator_type': 'NVIDIA_H100_80GB',
                   'accelerator_count': 2,
               },
               'replica_count': 1,
               'container_spec': {
                   'image_uri': 'gcr.io/your-project/your-image:latest',
               },
           }
       ],
   )
   job.run()
   ```

4. **监控和扩展**：
   - 使用 Vertex AI 控制台查看任务状态和日志。
   - 对于跨多台机器的分布式训练（例如，更多副本），请添加额外的工作线程池，并在大规模任务中根据需要使用归约服务器。
   - 成本：GPU 按小时计费；请检查您所在区域的价格（例如，2x H100 可能花费约 6-10 美元/小时）。

5. **多 GPU 训练提示**：
   - 在您的代码中启用分布式训练（例如，`torch.nn.parallel.DistributedDataParallel`）。
   - 如果可以接受中断，请使用 Spot VM 或预留实例以节省成本。
   - 通过 GCP 控制台验证您所在区域/可用区的 GPU 可用性。

## 备选方案：使用 Compute Engine 虚拟机
如果您更喜欢不使用 Vertex AI 的自定义设置：
1. 创建 VM 实例：
   - 转到 Compute Engine > VM 实例 > 创建实例。
   - 机器类型：从 A3 (H100)、A2 (A100)、G2 (L4) 系列中选择，例如，`a3-highgpu-2g` 用于 2x H100。
   - 启动磁盘：使用 Deep Learning VM 镜像（预装了 CUDA、TensorFlow/PyTorch）。
   - 添加 GPU：指定所选类型的 2 个加速器。

2. 通过 SSH 连接到 VM 并运行您的训练脚本：
   ```bash
   gcloud compute ssh your-vm-name --zone=your-zone
   python train.py  # 确保检测到 CUDA：nvidia-smi
   ```

3. 对于多 GPU：您的代码必须处理它（例如，`CUDA_VISIBLE_DEVICES=0,1`）。

这种方式更手动，但提供完全控制。

## 限制和备选方案
- 如果您特别需要类似 RTX 4090 的性能，请考虑其他方案，例如 AWS（在某些情况下提供消费级 GPU）或本地设置。
- 对于免费/有限的 GPU 训练，请尝试 Google Colab（最多 1-2 个 GPU，但不保证多 GPU 或 4090 等效性能）。
- 始终检查配额，并通过 GCP 控制台根据需要请求增加。

[为自定义训练配置计算资源 | Vertex AI | Google Cloud](https://cloud.google.com/vertex-ai/docs/training/configure-compute)
[GPU 机器类型 | Compute Engine 文档 | Google Cloud](https://cloud.google.com/compute/docs/gpus)
[Cloud GPUs (图形处理单元) - Google Cloud](https://cloud.google.com/gpu)
