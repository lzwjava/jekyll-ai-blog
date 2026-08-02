---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 先用AI特征化再扼杀
translated: true
type: note
---

问题：当企业内部库（例如自定义的Spring封装）因原始开发者离职而变得无法维护时，是否应使用AI重写或替换它们？

答案：是的，但决定并非“重写 vs 保留”——而是“先特性化描述，再逐步替换”。过去内部库多年无人问津的原因并非它们足够优秀，而是“阅读成本 > 重写风险”。大语言模型已将阅读成本降至接近零。这改变了权衡，但前提是按正确顺序操作。

**错误方法**：将封装代码直接丢进对话框，要求“干净重写”，然后直接交付。这会悄无声息地丢弃那些隐式领域知识的边界情况——针对特定下游服务的空值处理、为CVE补丁设置的retry hack、三年前事故后调优的超时配置。这些在LLM从第一性原理生成的“干净”版本中一概不存在。

**正确流程**——基于抽象的分支 + 特性化描述，每一步辅以AI：

```bash
# 1. 清单：在单体仓库中查找内部库的所有调用点
rg -l "com.yourcompany.internal.SpringWrapper" --type java > callsites.txt
wc -l callsites.txt

# 2. 将内部库及其调用点放入上下文，要求模型生成行为规范，而非重写方案。这一步是众人跳过的。
cat internal-lib/src/main/java/**/*.java > /tmp/lib_dump.txt
```

提示词（这才是真正的杠杆点）：
```
这是一个内部Spring封装库及其调用点。
请勿提出重写方案。而是：
1. 列出所有可观察行为（输入 -> 输出，包括错误路径）
2. 列出所有偏离标准Spring/Boot默认行为的地方
   （这通常是该封装库存在的原因）
3. 标记任何类似CVE补丁、retry/timeout调优，
   或针对特定下游服务的变通方案
```

```python
# 3. 将该规范转化为针对当前库的特性化测试
#    （黄金主测试——捕获真实行为，包括bug）
def test_wrapper_matches_golden_output():
    for case in golden_cases:
        assert current_wrapper.call(case.input) == case.expected  # 录制结果，非推导所得
```

```java
// 4. 基于抽象的分支：引入接口，当前实现置于其后，
//    让AI生成的新实现也置于同一接口之后
interface HttpClientPort {
    Response execute(Request req);
}
// 旧：SpringWrapperAdapter implements HttpClientPort  （未修改，仅封装）
// 新：ModernRestClientAdapter implements HttpClientPort  （AI生成候选方案）
```

```bash
# 5. 将一定比例的流量或部分调用点路由至新实现，
#    与黄金主测试和生产环境影子流量对比差异，然后逐个调用点完成替换。
```

**何时应直接删除而非重新实现**：若封装库仅是胶合标准Spring/Boot功能，而Spring本身已原生支持（例如自定义`RestTemplate`重试封装，而`RestClient` + `@Retryable`/resilience4j已覆盖）——不要重新实现封装库，直接迁移调用点至现代Spring API。AI在此处优势明显，因为它能机械比对“此自定义代码的功能”与“当前框架开箱即用的功能”，并告知你封装库已成冗余。

**何时不应触碰**：若第2步的规范揭示了隐藏在基础设施代码中的业务逻辑（费用计算、权限规则）。这不是库的问题，而是未文档化的领域逻辑——应将其提取为具名业务规则并附带测试，而非作为“Spring封装清理”的一部分。

核心结论：AI的职责不是重写代码，而是降低考古成本，使你能够安全应用那些古老但可靠的“扼杀者”模式/基于抽象的分支模式，而非一次性大改。

参考文献：
- [Strangler Fig模式 - Azure架构中心](https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig)
- [用于库/框架迁移的基于抽象的分支变体](https://layrs.me/course/hld/11-cloud-design-patterns/strangler-fig)
- [Strangler Fig模式 - CTO指南](https://www.wireapps.co.uk/blog/strangler-fig-pattern-guide)