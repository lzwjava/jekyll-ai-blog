---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenAI巨额现金消耗解读
translated: true
type: note
---

**问题：OpenAI 为何如此烧钱，近期泄露的财务消息又说了什么？**

回答：是的。像 OpenAI 这样的前沿人工智能公司极其资本密集。核心原因很简单：

> 训练和服务前沿模型，更像是运营一家半导体公司加云服务提供商，而不是一个普通的软件初创公司。

近期泄露的财务报告称，OpenAI 在2025年拥有约**130亿美元收入，但总支出约340亿美元**，运营亏损巨大。报道的数字存在争议，因为某些会计项目（如与企业重组相关的估值变化）夸大了总体亏损，但根本问题是真实存在的：OpenAI 在算力和研究上投入了巨额资金。([Quartz][1])

资金主要流向以下几个部分：

---

## 1. GPU 算力（最大头）

每一次 ChatGPT 请求都需要推理计算。

示例：

```
用户提示
    |
    v
分词器
    |
    v
GPU 集群
    |
    +-- 注意力层
    +-- MLP 层
    +-- KV 缓存内存
    |
    v
生成的 Token
```

一个 GPT 类模型：

* 拥有数千亿个参数
* 需要数千到数万块 GPU
* 巨大的网络需求（InfiniBand / NVLink）
* 7x24 小时持续服务

粗略的成本模型：

```
每个 Token 成本 =
    GPU 摊销
  + 电力
  + 数据中心
  + 网络
  + 工程
```

即使每次查询仅花费几分之一美分，数十亿次查询也会变成数百万美元。

---

## 2. 训练前沿模型

训练成本极其高昂。

简化公式：

```
训练 FLOPs ≈ 6 × 参数数量 × Token 数量
```

示例：

GPT 类似模型：

```
1万亿 参数
× 20万亿 Token
× 6

≈ 1.2e26 FLOPs
```

按现代 GPU 效率计算，这意味着：

```
10,000 块 GPU
× 数月时间
```

仅 GPU 账单就可能高达数亿美元。

---

## 3. 人工智能研究员薪资高昂

OpenAI 竞相争夺的人才市场包括：

* Google DeepMind
* Anthropic
* Meta FAIR
* xAI
* Microsoft AI

顶尖研究员的成本包括：

```
薪资
+
股票
+
计算预算
+
团队
```

核心人员的总薪酬每年可达数百万美元。

---

## 4. 基础设施建设

这一点常被低估。

OpenAI 需要类似这样的系统：

```
                    模型
                      |
        +-------------+-------------+
        |                           |
   训练基础设施             服务基础设施
        |                           |
   分布式 PyTorch           批处理
   检查点保存                KV 缓存
   故障恢复                 量化
   数据管道                 路由
```

这类似于构建：

* Google 搜索基础设施
* AWS 云基础设施
* 一家超级计算机公司

---

## 5. 数据获取与合作

大型模型需要：

* 授权数据集
* 出版商
* 云服务协议
* 内容合作伙伴关系

这些成本正在增长。

---

## 为何收入已达数十亿仍要如此烧钱？

因为 OpenAI 押注的是一个赢家通吃的市场。

其战略是：

```
现在投入数十亿美元
        |
        v
构建最佳模型
        |
        v
获取开发者/用户
        |
        v
创建生态系统锁定
        |
        v
未来盈利
```

这与以下情况类似：

* 2000年代的亚马逊
* 盈利前投资的特斯拉
* 半导体晶圆厂

---

## 有趣的工程问题

未来可能不仅仅是“更大的模型”。

经济规律正推动以下方向：

### 1. 更高效的推理

示例：

* 量化
* 推测性解码
* MoE 模型（混合专家模型）
* 定制 ASIC

这就是像 Taalas 这样的公司引人关注的原因。

不再是这样：

```
GPU：
通用计算
+
大容量内存
+
高功耗
```

未来的人工智能硬件可能变成：

```
ASIC：
固定变压器工作负载
+
更低功耗
+
更高吞吐量
```

---

### 2. 更小的专用模型

不再是这样：

```
一个巨型 GPT 模型服务所有任务
```

未来可能出现：

```
路由器
 |
 +-- 编码模型
 +-- 视觉模型
 +-- 推理模型
 +-- 小型本地模型
```

类似于 CPU/GPU 的专业化分工。

---

### 3. AI 智能体提升利用率

今天：

```
人类提问
     |
模型回答
     |
结束
```

未来：

```
目标
 |
智能体
 |
1000 次工具调用
 |
软件变更
 |
业务成果
```

用户的支付意愿可能会显著提高。

---

我的观点：从工程角度看，泄露的数字并不令人惊讶。前沿人工智能基本上是一场**构建新计算平台的竞赛**。不同寻常之处在于，“工厂”不是芯片晶圆厂；而是一个运行神经网络的大型 GPU 集群。

关键问题不仅是“OpenAI 能赚钱吗？”，还有：

```
人工智能能否变得足够廉价，
让每个人都或每家公司每天
消耗数千次人工智能推理运算？
```

如果答案是肯定的，那么今天的烧钱就像是基础设施投资。如果答案是否定的，那么经济账就会变得非常困难。

参考资料：

* ([Quartz][1])
* ([theinformation.com][2])
* ([wsj.com][3])

[1]: https://qz.com/openai-leaked-financials-losses-revenue-ipo-061626?utm_source=chatgpt.com "OpenAI 2025 financials leaked: $38.5B loss ahead of IPO"
[2]: https://www.theinformation.com/articles/openai-burned-3-7-billion-first-three-months-2026?utm_source=chatgpt.com "OpenAI Burned $3.7 Billion in First Three Months of 2026 — The Information"
[3]: https://www.wsj.com/tech/ai/openai-anthropic-ipo-finances-04b3cfb9?utm_source=chatgpt.com "An Inside Look at OpenAI and Anthropic’s Finances Ahead of Their IPOs"
