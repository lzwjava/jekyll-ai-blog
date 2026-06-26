---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 慢速SCP传输至阿里云
translated: true
type: note
---

问题：为什么通过SCP传输到我的阿里云香港服务器（47.86.12.246）速度这么慢，只有约270–370 KB/s，而从该服务器上传到HuggingFace的测试速度却比从我的Mac上传更快？

答案：

先澄清一下日志实际显示的内容，因为这里混淆了两个不同的传输过程：

1. **Mac → 阿里云香港（SCP）**：约270–370 KB/s。这是慢的那个环节。
2. **阿里云香港 → HuggingFace（hf upload）**：约515 KB/s，比Mac直接上传到HF快2.7倍。

所以阿里云本身并不快——那台香港服务器只是相对于你的Mac而言，处在一个更有利的**中继位置**接近HF。步骤1的瓶颈在于**Mac → 香港这一段**，而且几乎可以肯定是你家庭/办公室的上行带宽，加上通往阿里云公网IP的GFW路径导致的，而非阿里云自身的问题。

为什么Mac → 香港的SCP速度这么慢：

- **SCP是单流TCP。** 只有一个连接，因此吞吐量受限于 `window_size / RTT`。在跨境路径上，如果存在丢包、BBR与CUBIC不匹配以及较小的接收窗口，你会被严重限制。你并没有用满带宽——而是受限于RTT和丢包。
- **SCP/SSH有加密和帧开销**，且不支持并行。日志中提到的“15ms链路”数值具有误导性；真实的国内→香港路径在GFW下会有抖动和丢包。
- **你的家庭上行带宽**很可能是硬上限（约2–5 Mbit/s上行 ≈ 300–600 KB/s）。370 KB/s ≈ 3 Mbit/s，这更像是你的ISP上行限制，而不是阿里云的问题。

应该怎么做——打破单流瓶颈：

```bash
# 1. rsync本身不支持多流，但可以压缩并断点续传：
rsync -avP --partial /Users/lzwjava/projects/sec-edgar-gpt-124m/model.safetensors \
  root@<IP_ADDRESS>:/tmp/

# 2. 并行流——真正的解决方法。使用rclone进行分块并行传输：
rclone copy model.safetensors hk:/tmp/ --transfers 8 --multi-thread-streams 8

# 3. 或者干脆跳过中继——直接从Mac上传到HF，使用
#    hf内置的xet/multipart，它已经支持并行分块：
hf upload lzwjava/sec-edgar-gpt-124m model.safetensors model.safetensors
```

AI原生做法：**停止中继。** 香港服务器唯一的好处是更接近HF端点。但 `hf upload` 已经支持并行分块传输和xet去重。从你的Mac直接使用带 `--transfers` 并行参数的路径，很可能比 Mac → SCP → 香港 → HF 更快，因为SCP的单流才是真正的罪魁祸首——你既要忍受缓慢的Mac→香港段，又要多一次复制，只是为了省下HF本来就能并行化的那段路径。

如果香港中继确实更优（值得实测），至少让Mac→香港段并行起来：

```bash
# 分割文件 + 并行scp，在香港端合并
split -b 50M model.safetensors model.part.
ls model.part.* | xargs -P8 -I{} scp {} root@<IP_ADDRESS>:/tmp/
ssh root@<IP_ADDRESS> 'cat /tmp/model.part.* > /tmp/model.safetensors'
```

在受丢包限制的跨境路径上，8个并行流通常能带来4–6倍的提升。

结论：阿里云本身并不快。SCP之所以慢，是因为它是一条单TCP流，经过有损的国内→香港路径，且受限于你的家庭上行带宽。请采用并行传输，或者砍掉中继，让 `hf upload` 直接从你的Mac进行分块上传。
