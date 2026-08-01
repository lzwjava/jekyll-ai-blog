---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 快照存储成本详解
translated: true
type: note
---

问题：为什么AMD开发者云/DigitalOcean对一个133GB的MI300X快照收取7.99美元？

答案：

这**并非GPU计算费用**，而是**存储快照**的费用。

您的账单：

```
资源：
snapshots-gpu-mi300x1-192gb-devcloud-atl1-1780339218471

大小：
133.11 GB

时长：
744小时

周期：
07-01 00:00 → 08-01 00:00

费用：
$7.99
```

计算方式：

DigitalOcean快照定价为：

```
$0.06 / GB / 月
```

（[DigitalOcean][1]）

因此：

```
133.11 GB × $0.06 = $7.9866
```

约等于：

```
$7.99/月
```

与您的账单完全一致。

"744小时"只是计费周期（约31天×24小时）。快照存储本质上是按月计费，而非GPU运行时长计费。（[DigitalOcean][1]）

---

针对您的MI300X实验：

您可能执行了类似操作：

```
AMD开发者云 MI300X VM
        |
        |
   创建快照
        |
        |
   销毁GPU虚拟机
        |
        |
   快照保留
```

高成本的GPU机器已释放，但快照仍然存在：

```
快照
 ├── Ubuntu镜像
 ├── ROCm
 ├── PyTorch
 ├── 模型
 ├── 检查点
 └── 您的数据

133GB
```

您正在为这133GB的存档付费。

---

如果不再需要：

请前往：

```
DigitalOcean控制台
 -> 镜像
 -> 快照
 -> snapshots-gpu-mi300x1-192gb-devcloud-atl1-1780339218471
 -> 销毁
```

后续月度费用将变为：

```
$0
```

---

针对AI工作负载，更好的模式是：

### 仅保留代码+环境

示例：

```bash
# 保存环境
pip freeze > requirements.txt

# 保存Docker
docker save my-rocm-env > rocm-env.tar

# 上传模型/检查点
rclone copy ./checkpoint s3://mybucket/checkpoint
```

然后删除快照。

对于MI300X实验，133GB快照成本昂贵，因为其中大部分可能是：

```
/home
 ├── huggingface缓存
 │     ├── Qwen权重
 │     ├──数据集
 │
 ├── pytorch缓存
 ├── docker层
 └── 检查点
```

通常您只需要：

```
git仓库        < 1GB
配置文件       KB
检查点        视情况而定
```

将大模型存储在：

* Hugging Face Hub
* S3 / R2
* 廉价对象存储

然后重新创建机器。

对于您这类LLM基础设施实验（ROCm、MI300X、vLLM、训练），我建议避免长期保留快照。保留一个可复现的引导脚本：

```bash
#!/bin/bash

apt install rocm
pip install torch vllm transformers

git clone your-repo

huggingface-cli download model-name
```

这样，一个新MI300X节点可在约10-30分钟内重建，而无需永久支付$8/月。

参考：

* DigitalOcean快照定价（[DigitalOcean][1]）
* DigitalOcean Droplet定价（[DigitalOcean][2]）

[1]: https://docs.digitalocean.com/products/snapshots/details/?utm_source=chatgpt.com "快照详情 | DigitalOcean文档"
[2]: https://www.digitalocean.com/pricing/droplets?utm_source=chatgpt.com "Droplet定价 | DigitalOcean"
