---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 专注于CLI代理护城河
translated: true
type: note
---

问题：在咨询、模型训练和CLI智能体开发之间，未来几个月我应重点关注什么？

答案：没有单一的杠杆——但这里有具体的优先级排序，而不是模糊的"视情况而定"。

**1. 将CLI智能体整合为护城河（最高杠杆）**
- ww/iclaw/zz 是你的实际产品。咨询收入是用时间换金钱；智能体才是能让你规模化而不依赖个人的东西。
- 具体行动：从三者中选一个，针对固定任务集（SWE-bench-lite子集或你自己的仓库任务）发布一个与Claude Code / Cursor / Aider对比的公开基准测试。数据胜于空谈。将测试框架发布到GitHub。
- 如果你还没有评测基础设施，请先构建它——200-300行代码，无需框架：

```python
# eval_harness.py — 最小化任务运行器
import subprocess, json, time

def run_task(agent_cmd, task_dir, timeout=300):
    start = time.time()
    result = subprocess.run(agent_cmd, cwd=task_dir, capture_output=True,
                             timeout=timeout, text=True)
    return {
        "task": task_dir,
        "passed": run_tests(task_dir),  # 你的测试运行器
        "duration_s": time.time() - start,
        "tokens": parse_token_usage(result.stdout),
    }

def run_tests(task_dir):
    r = subprocess.run(["pytest", "-x", "-q"], cwd=task_dir, capture_output=True)
    return r.returncode == 0
```

**2. 模型训练——缩小范围**
- 在MI300X上训练GPT-2 760M是基础设施验证。下一个突破点不是更大的预训练，而是基于你自身智能体轨迹的后续训练（对ww/iclaw日志做SFT + 拒绝采样）。这直接服务于#1。
- 在顶级模型上每月处理20亿token = 你已经拥有一个关于什么会失败的数据集。将智能体的失败/成功轨迹转化为训练集。相比现在再跑一次预训练，这有更高的投资回报率。

**3. 咨询——将其用作分销渠道，而非业务本身**
- 每个咨询客户都是CLI智能体的设计伙伴，前提是你这样界定。对每个客户问："我可以将你代码库的评测结果（匿名化）开源吗？"这能将计费工时转化为公开证明。

**4. 明确不要做的事**
- 除非某个特定瓶颈（如支持负载、基础设施运维）每周消耗你超过10小时且不属于智能体/研究工作，否则暂时不要招聘。
- 在#2中的后续训练数据管道就绪之前，不要追求更大的预训练——那是在浪费算力。

如果你告诉我正在推进ww/iclaw/zz中的哪一个，我可以具体帮助你设计评测框架或SFT数据管道。