---
audio: false
generated: true
lang: en
layout: post
title: Training ML Models on GCP with NVIDIA GPUs
translated: false
type: note
---

Google Cloud Platform (GCP) provides robust options for training machine learning models using NVIDIA GPUs through services like Vertex AI (for managed training jobs) and Compute Engine (for custom virtual machines). However, NVIDIA RTX 4090 GPUs are not available on GCP. The RTX 4090 is a consumer-grade GPU primarily for desktops and gaming, not designed for cloud data centers. Instead, GCP offers enterprise-grade NVIDIA GPUs such as A100, H100, L4, and others, which are optimized for AI workloads and often outperform the RTX 4090 in training scenarios due to higher memory bandwidth and tensor core efficiency.

For multi-GPU setups (at least 2 GPUs), you can configure resources to use 2, 4, 8, or more GPUs depending on the machine type. I'll focus on Vertex AI for simplicity, as it's tailored for ML training and handles scaling automatically. If you need more control, I'll cover Compute Engine briefly.

## Prerequisites
- Set up a Google Cloud account and create a project.
- Enable the Vertex AI API and Compute Engine API in your project.
- Install the Google Cloud SDK (gcloud CLI) and the Vertex AI SDK if using Python.
- Prepare your training code in a Docker container (e.g., using TensorFlow or PyTorch with distributed training support like Horovod or torch.distributed).
- Ensure your model code supports multi-GPU training (e.g., via DataParallel or DistributedDataParallel in PyTorch).

## Using Vertex AI for Multi-GPU Training
Vertex AI is GCP's managed platform for ML workflows. It supports custom training jobs where you can specify machine types with multiple GPUs.

### Available GPU Types for Multi-GPU
Common NVIDIA GPUs supporting at least 2 attachments:
- NVIDIA H100 (80GB or Mega 80GB): High-performance for large models; supports 2, 4, or 8 GPUs.
- NVIDIA A100 (40GB or 80GB): Widely used for training; supports 2, 4, 8, or 16 GPUs.
- NVIDIA L4: Cost-effective for inference and lighter training; supports 2, 4, or 8 GPUs.
- NVIDIA T4 or V100: Older but still available; supports 2, 4, or 8 GPUs.

Full list includes GB200, B200, H200, P4, P100—check regions for availability, as not all are in every zone.

### Steps to Create a Training Job with at Least 2 GPUs
1. **Prepare Your Container**: Build a Docker image with your training script and push it to Google Container Registry or Artifact Registry. Example Dockerfile for PyTorch:
   ```
   FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime
   COPY train.py /app/train.py
   WORKDIR /app
   CMD ["python", "train.py"]
   ```

2. **Configure the Job Using gcloud CLI**:
   - Create a `config.yaml` file:
     ```yaml
     workerPoolSpecs:
       machineSpec:
         machineType: a3-highgpu-2g  # Example: 2x H100 GPUs; alternatives: a2-ultragpu-2g (2x A100), g2-standard-24 (2x L4)
         acceleratorType: NVIDIA_H100_80GB  # Or NVIDIA_A100_80GB, NVIDIA_L4
         acceleratorCount: 2  # At least 2
       replicaCount: 1
       containerSpec:
         imageUri: gcr.io/your-project/your-image:latest  # Your Docker image URI
     ```
   - Run the command:
     ```bash
     gcloud ai custom-jobs create \
       --region=us-central1 \  # Choose a region with GPU availability
       --display-name=your-training-job \
       --config=config.yaml
     ```

3. **Using Python SDK**:
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

4. **Monitor and Scale**:
   - Use the Vertex AI console to view job status and logs.
   - For distributed training across multiple machines (e.g., more replicas), add additional worker pools and use reduction servers if needed for large-scale jobs.
   - Costs: GPUs are billed per hour; check pricing in your region (e.g., 2x H100 might cost ~$6-10/hour).

5. **Tips for Multi-GPU Training**:
   - Enable distributed training in your code (e.g., `torch.nn.parallel.DistributedDataParallel`).
   - Use spot VMs or reservations for cost savings if interruptions are okay.
   - Verify GPU availability in your region/zone via the GCP console.

## Alternative: Using Compute Engine VMs
If you prefer a custom setup without Vertex AI:
1. Create a VM instance:
   - Go to Compute Engine > VM instances > Create instance.
   - Machine type: Select from A3 (H100), A2 (A100), G2 (L4) series, e.g., `a3-highgpu-2g` for 2x H100.
   - Boot disk: Use a Deep Learning VM image (pre-installed with CUDA, TensorFlow/PyTorch).
   - Add GPUs: Specify 2 accelerators of the chosen type.

2. SSH into the VM and run your training script:
   ```bash
   gcloud compute ssh your-vm-name --zone=your-zone
   python train.py  # Ensure CUDA is detected: nvidia-smi
   ```

3. For multi-GPU: Your code must handle it (e.g., `CUDA_VISIBLE_DEVICES=0,1`).

This is more hands-on but gives full control.

## Limitations and Alternatives
- If you specifically need RTX 4090-like performance, consider alternatives like AWS (which offers consumer GPUs in some cases) or on-premises setups.
- For free/limited GPU training, try Google Colab (up to 1-2 GPUs, but not guaranteed multi-GPU or 4090-equivalent).
- Always check quotas and request increases if needed via the GCP console.

[Configure compute resources for custom training | Vertex AI | Google Cloud](https://cloud.google.com/vertex-ai/docs/training/configure-compute)
[GPU machine types | Compute Engine Documentation | Google Cloud](https://cloud.google.com/compute/docs/gpus)
[Cloud GPUs (Graphics Processing Units) - Google Cloud](https://cloud.google.com/gpu)
