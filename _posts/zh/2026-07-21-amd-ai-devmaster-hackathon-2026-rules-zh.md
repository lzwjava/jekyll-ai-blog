---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD AI DevMaster 黑客马拉松 2026 规则
translated: true
type: note
---

问题：**这份AMD AI DevMaster Hackathon文档是什么？**

回答：

这是 **AMD AI DevMaster Hackathon 2026** 的规则/规范文档。该比赛由 AMD 赞助，开发者需构建针对 **AMD Radeon GPU + ROCm** 优化的 AI 应用程序。

核心思想：

> 用 AI 构建有用的东西，但确保计算密集型部分在 AMD GPU 上通过 ROCm 本地运行。

共有 **3 个赛道**：

---

## 赛道 1 — 多模态 AI 内容创作（可能与你最相关）

围绕以下内容构建 AI 工具：

* 图像生成
* 图像编辑
* 风格迁移
* 视频风格化
* 文生视频
* 图生视频
* 增强/超分辨率
* 批量内容创作

示例：

```
输入：
  照片/视频/文本提示词

GPU 流水线：
  Stable Diffusion / FLUX / ControlNet / LoRA
  + ROCm 加速

输出：
  动漫风格视频
  赛博朋克视频
  营销内容
  短视频生成
```

必需技术栈：

* 来自 Radeon 云的 AMD Radeon GPU
* ROCm
* PyTorch ROCm
* 允许使用 ComfyUI / Diffusers / Transformers
* 允许使用 OpenCV / FFmpeg / Pillow

封闭 API 不能作为核心。至少一条关键推理路径必须在 AMD GPU 上本地运行。

交付物：

* 源代码
* README
* PDF 项目描述
* 3–5 分钟演示视频

---

## 赛道 2 — 私域本地 AI 代理（也非常适合你）

大致意思是：

> 构建一个运行在 AMD GPU 上的本地类 ChatGPT 代理。

示例：

* 个人助手
* 编码代理
* 知识库代理
* 文档/邮件助手
* 生活管理代理

必需能力：

以下 **5 项中至少具备 2 项**：

1. RAG
2. 工具调用
3. 多步规划
4. 本地记忆
5. 权限/隐私控制

可能架构：

```
               用户
                 |
            Web UI / CLI
                 |
            代理路由器
                 |
       +---------+---------+
       |                   |
   本地 LLM           工具
   Qwen/Llama          |
       |               |
   ROCm/vLLM      浏览器
                  文件
                  Git
                  日历

        AMD Radeon GPU
```

推荐工具：

* vLLM
* llama.cpp
* Transformers + PyTorch ROCm
* LangChain/LlamaIndex/Dify 等

鉴于你已有的 `ww`、`iclaw`、代理实验，本赛道非常匹配。

---

## 赛道 3 — 物理 AI / 机器人

机器人仿真：

* 机械臂
* 人形机器人
* 四足机器人
* 自动驾驶

使用：

* Genesis
* MuJoCo
* LeRobot
* OpenVLA

需要仿真 + AI 控制 + AMD GPU 加速。

除非你想进入机器人领域，否则可能不太相关。

---

## 奖品

每个赛道：

| 名次 | 奖金 |
| ---- | ---: |
| 第1名 | $5,000 |
| 第2名 | $3,500 |
| 第3名 | $1,500 |

---

## 时间线

重要日期：

* 报名开放：2026年7月10日
* 提交开放：2026年7月15日
* 截止日期：2026年8月6日 23:59 北京时间/新加坡时间

---

## 我对你的建议

鉴于你的背景：

* GPT-2 训练
* nanoGPT
* 代理 CLI 工具
* 博客/视频自动化
* AMD ROCm 兴趣

我会选择 **赛道 2**。

一个有力的项目想法：

# "OpenClaw 本地 AI 代理"

```
AMD Radeon GPU
        |
     Qwen3 / Llama
        |
   代理运行时
        |
 +------+-------+
 |      |       |
RAG   工具   记忆
 |      |       |
博客  Git   向量数据库
PDF   Shell  SQLite
视频
```

演示：

1. 用户问：

   > "创建今天的 AI 研究视频"

2. 代理：

```
搜索论文
      |
摘要
      |
生成 markdown
      |
生成图片
      |
生成视频
      |
发布
```

一切都在 AMD GPU 上本地运行。

这直接展示了：

* 本地推理
* 工具调用
* 工作流编排
* 实用价值

评委明确评估这些能力。

要想获胜，不要构建另一个聊天机器人。构建一个 **运行在 Radeon 上的个人 AI 操作系统**。
