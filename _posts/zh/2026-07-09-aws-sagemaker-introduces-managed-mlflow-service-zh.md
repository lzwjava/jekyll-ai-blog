---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AWS SageMaker推出托管式MLflow服务
translated: true
type: note
---

问题：AWS博客《扩展MLflow以实现企业级AI：SageMaker AI与MLflow的新特性》讲了什么？

回答：

这篇博客**并非介绍新的机器学习算法**，而是宣布**AWS已将MLflow打造成Amazon SageMaker AI内部一项完全托管、无服务器的企业级服务**。（[Amazon Web Services, Inc.][1]）

如果你曾在本地使用MLflow，通常需要运行类似这样的命令：

```bash
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root s3://my-bucket/mlruns
```

然后你需要维护：

* PostgreSQL/SQLite
* S3存储
* 身份验证
* 备份
* 扩展
* 升级
* IAM

AWS的意思是：

> “别再自己操心这些了。”

取而代之的是，SageMaker会自动提供一个MLflow服务器（“MLflow应用”），空闲时缩至零，实验运行时自动扩展。（[Amazon Web Services, Inc.][1]）

---

### MLflow的实际作用

可以把MLflow想象成**GitHub + TensorBoard + 机器学习实验数据库**。

每次训练运行都会记录：

```text
运行 #104

模型：
    GPT-2 124M

数据集：
    SEC EDGAR 15.5B tokens

超参数：
    lr = 3e-4
    batch_size = 512
    seq_len = 1024

指标：
    train_loss
    val_loss
    perplexity

工件：
    checkpoint.pt
    tokenizer.json
    config.yaml
```

几个月后，你还能回答这些问题：

* 哪个学习率效果最好？
* 哪个检查点产生的验证损失最低？
* 使用了哪个数据集版本？
* 训练这个模型用的是哪个Git提交？

---

### 对于大语言模型训练

假设你在训练NanoGPT：

```bash
python train.py \
    --lr=3e-4 \
    --bs=512 \
    --dataset=fineweb
```

MLflow会自动记录

```
实验
 ├── 运行1
 │      lr=3e-4
 │      val_loss=2.34
 │
 ├── 运行2
 │      lr=2e-4
 │      val_loss=2.29
 │
 └── 运行3
        lr=1e-4
        val_loss=2.42
```

无需手动维护电子表格。

---

### 这次AWS公告的新内容是什么？

AWS新增了多项企业级功能：

* **无服务器MLflow**（无需管理基础设施）
* 自动扩展（包括缩至零）
* 创建SageMaker Studio域时自动配置
* 自动MLflow版本升级
* AWS IAM集成
* 跨账户共享
* 原生集成SageMaker Pipelines
* 自动记录SageMaker微调任务和模型定制工作流（[Amazon Web Services, Inc.][1]）

以前你需要管理一个MLflow追踪服务器。现在AWS将其作为一个**MLflow应用**呈现，基础设施已被抽象化。（[Amazon Web Services, Inc.][1]）

---

### 这对你的工作流程重要吗？

根据我对你的设置（NanoGPT/NanoChat训练、自定义数据集、Hermes智能体、本地RTX 4070、MI300X）的了解，**可能不太重要**。

你的工作流程大致如下：

```
train.py
      ↓
checkpoint.pt
      ↓
Hermes智能体
      ↓
分析曲线
比较运行
生成报告
```

智能体已经可以检查：

* 训练损失
* 验证损失
* 吞吐量
* GPU利用率
* 超参数
* 检查点

如果你只运行几十或几百次实验，轻量级解决方案（TensorBoard、W&B或本地MLflow）通常就足够了。

当你遇到以下情况时，AWS提供的服务会更有价值：

* 20多名研究人员
* 数千次实验
* 集中化治理
* 多个AWS账户
* 生产级MLOps流水线

这才是本次公告的目标受众。（[Amazon Web Services, Inc.][1]）

因此，对于独立研究员或小型AI初创公司，你使用智能体分析日志的想法完全合理。MLflow主要提供标准化的元数据存储和界面，而智能分析——比较运行结果、发现异常、推荐超参数——确实可以委托给大语言模型智能体。

参考资料：

* [扩展MLflow以实现企业级AI（AWS博客）](https://aws.amazon.com/blogs/machine-learning/scaling-mlflow-for-enterprise-ai-whats-new-in-sagemaker-ai-with-mlflow/?utm_source=chatgpt.com)
* [使用Amazon SageMaker AI与无服务器MLflow加速AI开发](https://aws.amazon.com/blogs/aws/accelerate-ai-development-using-amazon-sagemaker-ai-with-serverless-mlflow/?utm_source=chatgpt.com)
* [Amazon SageMaker上的托管MLflow（GA公告，2024年）](https://aws.amazon.com/blogs/aws/manage-ml-and-generative-ai-experiments-using-amazon-sagemaker-with-mlflow/?utm_source=chatgpt.com)

[1]: https://aws.amazon.com/blogs/machine-learning/scaling-mlflow-for-enterprise-ai-whats-new-in-sagemaker-ai-with-mlflow/?utm_source=chatgpt.com "扩展MLflow以实现企业级AI：SageMaker AI与MLflow的新特性 | 人工智能"
