---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 理解SGLang基准测试结果
translated: true
type: note
---

问题：如何理解 `sglang test` 基准测试的输出？

答案：

该测试本质上是对运行中的 SGLang 推理服务器进行**健康检查 + 延迟基准测试**。

你会看到：

```
URL:      http://localhost:30010
模型:    Qwen/Qwen2.5-0.5B-Instruct
最大上下文:  32,768 tokens
最大输出:  每个请求 128 tokens
```

含义：

* SGLang 服务器运行在端口 `30010`
* 加载的模型：

  ```
  Qwen/Qwen2.5-0.5B-Instruct
  ```

  0.5B 参数指令模型
* 上下文窗口：

  ```
  32,768 tokens
  ```

  模型理论上一次请求可读取约 32k tokens。
* 每个请求允许最大生成：

  ```
  128 个输出 tokens
  ```

---

## 1. 探测

```
探测（非流式）：20ms，33 入 / 3 出 -> 'OK.'
```

这是一个简单请求：

输入：

```
33 tokens
```

输出：

```
3 tokens
```

延迟：

```
20ms
```

它检查：

* HTTP 端点是否正常工作
* 分词器是否正常
* 模型能否生成
* 响应格式是否正确

相当于：

```bash
curl http://localhost:30010/generate \
  -d '{"text":"hello","max_new_tokens":3}'
```

---

## 2. 主要基准测试表

示例：

```
用例      输入     TTFT    总计   输出    tok/s
tiny        11t      10ms    36ms      9    252.0
```

每一行发送不同大小的提示。

---

# 列解释

## 输入

示例：

```
4,711t
```

意思是：

```
4,711 输入 tokens
```

重要提示：

Tokens ≠ 单词。

大致换算：

```
1 token ≈ 0.75 个英文单词
```

所以：

```
4711 tokens
≈ 3500 单词
```

---

## TTFT

首 Token 生成时间。

示例：

```
TTFT = 15ms
```

含义：

用户发送请求：

```
prompt
 |
 |
 v
SGLang
 |
 |
 v
第一个生成的 token
```

时间：

```
15ms
```

这衡量：

* 请求开销
* 提示处理
* KV 缓存初始化
* 调度器延迟

对于聊天应用：

TTFT 非常重要。

用户感受：

```
100ms  -> 瞬间
500ms  -> 尚可
2s     -> 缓慢
```

---

## 总计

总请求时间。

示例：

```
total = 218ms
```

时间线：

```
请求
 |
 |---- 14ms ----|
 首 token

 |--------------|
 生成

 完成
```

公式：

```
总计 ≈ TTFT + 生成时间
```

---

## 输出

生成的 tokens。

示例：

```
out = 67
```

模型生成了：

```
67 个 tokens
```

---

## tok/s

生成速度。

示例：

```
307.9 tok/s
```

意思是：

在首 token 之后：

```
模型每秒生成约 308 个 tokens
```

对于你的配置来说，这非常快，因为：

* Qwen2.5 0.5B 很小
* 很可能运行在 GPU 上
* SGLang 具有高效的运行时

---

## 完成

```
stop
```

表示生成自然结束。

其他可能情况：

```
length
```

意思是：

```
达到 max_tokens 限制
```

示例：

```json
max_tokens:128
```

且模型恰好生成了 128 个 tokens。

---

# 为什么长输入的总时间更快？

你会看到：

```
长文本：
1189 输入
TTFT 14ms
总计 218ms
67 输出

超长文本：
4711 输入
TTFT 15ms
总计 125ms
35 输出
```

看起来很奇怪。

为什么 4711 个 tokens 更快？

因为：

生成长度不同。

对比：

```
长文本：
67 个输出 tokens

超长文本：
35 个输出 tokens
```

生成时间占主导。

近似：

```
时间 =
提示处理
+
输出生成
```

对于 SGLang：

提示处理：

```
4711 tokens -> ~15ms
```

高度优化。

生成：

```
67 tokens / 308 tok/s
≈217ms
```

匹配：

```
总计 218ms
```

---

# 这个测试证明了什么

你的 SGLang 部署：

```
[ 正常 ] tiny
[ 正常 ] short
[ 正常 ] medium
[ 正常 ] long
[ 正常 ] huge
```

意思是：

### 1. 服务器正常工作

```
HTTP
 ↓
SGLang 运行时
 ↓
CUDA 内核
 ↓
模型
```

一切正常。

### 2. 长上下文正常工作

你测试了：

```
4,711 tokens
```

没有失败。

未达到：

```
32,768
```

但足以验证。

---

# 对于真正的 LLM 服务，你会关注不同的数据

生产环境基准测试通常衡量：

## Prefill 吞吐量

处理输入：

```
提示输入期间的 tokens/秒
```

示例：

```
5000 个输入 tokens
```

GPU 消化它们有多快？

## Decode 吞吐量

生成：

```
输出 tokens/秒
```

你的数据：

```
~300 tok/s
```

针对 Qwen2.5-0.5B。

## 并发用户

SGLang 的重要特性是：

连续批处理。

示例：

用户 A：

```
生成 100 tokens
```

用户 B 到达：

```
生成 100 tokens
```

SGLang 将它们批处理：

```
GPU：
A token
B token
A token
B token
...
```

而不是：

```
A 完成后
再 B 完成
```

---

对于你之前的 GPU 实验（RTX 4070 12GB），更有意义的下一步测试是：

```bash
python -m sglang.bench_serving \
  --backend sglang \
  --model Qwen/Qwen2.5-7B-Instruct \
  --num-prompts 100 \
  --request-rate 10
```

这衡量真实的服务行为：

```
请求/秒
延迟 p50/p95
输入 tok/s
输出 tok/s
```

这个小型的 `sglang test` 仅证明 **“引擎能工作”**。它像一个单元测试，而不是生产环境的基准测试。
