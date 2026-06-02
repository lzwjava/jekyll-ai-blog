---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 使用PyTorch DDP进行分布式训练
translated: true
type: note
---

### 卡帕西解读概览
在YouTube视频《Let's build GPT: from scratch, in code, spelled out》（约2小时58分处开始）中，安德烈·卡帕西深入讲解了使用PyTorch进行大语言模型分布式训练的方法。他重点演示了如何将单GPU训练循环扩展到多GPU（例如8个）而无需大幅修改代码。核心思想是在每个GPU上运行**相同进程**，各自处理数据集中互不重叠的分片，并通过梯度平均实现同步。这使得有效批次大小成为单GPU批次大小的倍数。他强调简化流程，使用PyTorch的DistributedDataParallel（DDP）模块，并逐步演示了类似GPT-2模型的代码实例。

卡帕西用了一个比喻：想象一组研究员（GPU）独立分析数据集的不同部分，但定期"比对笔记"（梯度平均）以保持解决方案一致。他使用`torchrun --standalone --nproc_per_node=8 train_gpt2.py`启动训练，该命令会自动设置`RANK`、`WORLD_SIZE`和`LOCAL_RANK`等环境变量。

### 分布式训练
卡帕西将分布式训练解释为在保持核心前向/反向传播基本不变的前提下跨GPU并行化的方法：
- 每个GPU启动一个进程（例如8个GPU对应8个进程）
- 每个进程运行**相同的模型代码**，但处理数据集的**独特分片**（按秩分片）
- 反向传播结束后，梯度**在所有进程间平均**（通过全规约操作）并应用于每个模型副本，模拟单一大批次更新
- 关键优势：将通信（梯度同步）与计算（反向传播）重叠以提高效率
- 数据分片：对于批次数据，起始索引= `rank * batch_size * seq_len`，步长为`batch_size * seq_len * world_size`。各进程使用相同随机种子保证顺序一致，但按不同分片处理
- 对于变长输入（如评估中的选项），填充至批次最大长度并使用掩码在损失计算中忽略填充部分

他指出："前向传播保持不变，反向传播也基本不变，我们只是附加了这个平均操作"

### 分布式数据并行（DDP）
DDP是卡帕西进行多GPU训练的首选，相比旧的`DataParallel`能更好处理梯度同步和多节点设置。按此方式包装模型：`model = DDP(model, device_ids=[local_rank])`
- **梯度流**：每个GPU在其数据分片上计算本地梯度。`loss.backward()`后，DDP触发**全规约**操作跨秩平均梯度，并将平均值送回每个秩
- **同步细节**：通信发生在反向传播**过程中**（重叠进行），而非结束后，最大限度减少空闲时间
- **梯度累积**：为在多个微步骤中累积梯度（例如4步实现更大有效批次），仅在最后微步同步。卡帕西在前几步设置`model.require_backward_grad_sync = False`，最后一步设为`True`，或使用`torch.distributed.barrier()`简化操作。为避免代码复杂化，不采用`no_sync()`上下文
- 日志和检查点：仅主进程（秩0）处理这些操作以避免信息泛滥
- 清理：始终在最后调用`torch.distributed.destroy_process_group()`

引述："DDP的功能是...在反向传播结束后，它会调用所谓的全规约操作，基本上对所有秩的梯度进行平均，然后将这个平均值存放到每个秩上"

对于损失记录（由于梯度已平均），需对标量损失进行规约：使用`all_reduce`（op=`ReduceOp.SUM`）跨秩求和，然后在秩0上除以`world_size`

### 秩的概念
秩是每个进程的唯一整数ID（0到`world_size - 1`，例如8个GPU对应0-7），通过`os.getenv('RANK')`设置。它决定：
- **数据分配**：对数据集分片，使得仅当`i % world_size == rank`时的样本由该秩处理
- **设备绑定**：使用`local_rank`（单节点内GPU索引，通过`os.getenv('LOCAL_RANK')`获取）设置`torch.cuda.set_device(local_rank)`
- **控制流**：秩0作为"主节点"专用于打印损失、保存检查点或聚合评估指标等任务，其他秩静默计算
- **同步**：用于屏障和规约操作（如统计量的全规约）

在评估阶段（例如H-SWAG数据集），每个秩计算本地计数（正确预测数、总样本数），全规约求和后由秩0计算准确率

卡帕西强调：确定性种子确保所有秩看到相同的乱序排列，但各秩会过滤出非重叠的分片

### 评估与实现补充说明
卡帕西演示了多选数据集（H-SWAG）的分布式评估：分片样本、计算本地准确率、全规约计数、由秩0打印结果。对于预测，选择每个样本平均损失最低（或概率最高）的选项，使用填充/掩码技术

实用技巧：
- 批次大小按GPU设置；全局有效批次大小= 单GPU批次 × 世界大小 × 累积步数
- 序列长度（上下文）保持固定（例如1024个词元）

本节直接建立在先前单GPU代码基础上，展示了为扩展规模所需的最小改动

[Let's build GPT: from scratch, in code, spelled out](https://www.youtube.com/watch?v=l8pRSuU81PU)
