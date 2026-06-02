---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在CLI中禁用Hermes Planning
translated: true
type: note
---

**问题：** 如何在 CLI 代理设置中禁用 Hermes 代理的规划/委派功能？它太慢了。

**回答：**

该输出来自你的自定义 `mimo` / `Hermes` 代理框架——带有 `delegate_task` 的编排循环。要禁用规划，具体方法取决于 Hermes 的实现方式。根据显示的模式（自我改进审查 → 规范审查 → 代码质量审查 → 委派），以下是追踪并禁用的方法：

## 1. 找到规划/委派配置

```bash
# 搜索编排入口点
grep -r "hermes\|delegate_task\|plan\|spec.*review\|code.*quality" ~/your-agent-repo --include="*.py" -l

# 或者如果它在配置文件中
find . -name "*.yaml" -o -name "*.toml" -o -name "*.json" | xargs grep -l "hermes\|delegate\|plan"
```

## 2. 常见禁用模式

**如果在配置文件中是一个标志：**

```yaml
# 代理配置
planning: false
delegate: false
review_steps: []
```

**如果是 CLI 标志：**

```bash
mimo --no-plan
mimo --disable-hermes
mimo --mode direct   # 跳过编排层
```

**如果是代码——找到编排循环：**

```python
# 查找类似下面的内容并短路它
class Hermes:
    def run(self, task):
        if self.config.get("planning", True):  # <-- 设置为 False
            plan = self.make_plan(task)
            for step in plan:
                self.delegate_task(step)
        else:
            self.execute_direct(task)  # 你想要的
```

## 3. 快速环境变量覆盖（常见模式）

```bash
HERMES_PLAN=false mimo "执行任务"
DISABLE_PLANNING=1 mimo "执行任务"
```

## 4. 如果是第三方代理框架

基于 UI（`⚕ Hermes`，`mimo-v2.5-pro`，token 计数器），这看起来可能是 **Nous Research 的 Hermes** 或一个自定义封装。分享仓库/工具名称，我可以给出精确步骤。或者：

```bash
mimo --help | grep -i "plan\|delegate\|review\|mode"
```

`mimo` 和 `Hermes` 背后的实际工具/仓库是什么？这样我就能给你确切的标志。
