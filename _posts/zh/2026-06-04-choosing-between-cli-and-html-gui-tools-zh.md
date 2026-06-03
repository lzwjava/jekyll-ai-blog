---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 选择CLI还是HTML GUI工具
translated: true
type: note
---

问题：我是否应该将CLI工具构建为独立的HTML GUI，尤其是面向非工程师用户？GUI的权衡在什么情况下是合理的？

答案：

**简短回答：** CLI是你的原生环境，交付速度更快。HTML GUI能打开不同的市场（非工程师），但只有这个市场确实值得服务时才去构建。不要为“所有人”优化——首先要为核心用户优化。

**何时选择CLI：**
- 你（工程师）每天都在使用
- 你的用户是工程师/终端原生用户
- 迭代速度比精致更重要
- 与其他工具的集成（管道、脚本、容器）是一项功能

你交付更快，维护面更小，且能保持工作流顺畅。

**何时选择HTML GUI：**
- 非工程师需要它（会计、运维、产品经理）
- 该工具解决了一个有重复用户的业务问题
- 你有超越个人层面的采用目标
- 该领域天然适用于视觉交互（数据探索、仪表板）

示例：duckdb *可以*有一个用于SQL探索的HTML GUI，但工程师更喜欢在终端中使用`duckdb file.db`。用Python处理Excel时，GUI更有优势，因为最终用户并不运行Python。

**实用的混合方案：**

不要先构建CLI再构建GUI。**先构建库/守护进程**，然后再封装：

```python
# 核心逻辑作为库
# mylib/processor.py
class DataProcessor:
    def process(self, data, config):
        # 实际工作
        return result
```

**然后：** 在其上添加两个薄层：

1. **CLI封装**（约20行Click/Typer代码）：
```bash
myapp process --input data.csv --output result.json
```

2. **HTML GUI**（独立，约300-500行HTML/JS）：
```html
<!-- index.html -->
<input type="file" id="upload">
<button onclick="processLocal()">处理</button>
<script>
async function processLocal() {
  // 调用WASM或请求本地Python服务器
  // 在表格中显示结果
}
</script>
```

**对于类似于“sheer-excel”风格的电子表格处理：**

如果你想让非工程师以可视化方式操作表格数据，请使用 **[SheetJS](https://sheetjs.com/)**（或libre office.js）+ 一个简单的HTML封装：

```html
<input type="file" id="excel" accept=".xlsx">
<table id="grid"></table>
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.min.js"></script>
<script>
document.getElementById('excel').onchange = (e) => {
  const file = e.target.files[0];
  const workbook = XLSX.read(file, {type: 'array'});
  const data = XLSX.utils.sheet_to_json(workbook.Sheets[workbook.SheetNames[0]]);
  // 渲染到表格，允许编辑，导出回文件
};
</script>
```

这是**独立的**（一个.html文件 + SheetJS CDN），可离线工作，非工程师也能使用。

**你的实际决策：**

- **如果你自己就是用户，且合作者都是工程师：** 全天候用CLI。几天内交付，而非几周。
- **如果你想广泛销售/分发：** 用HTML GUI引导新用户，CLI给高级用户。先构建库，再构建两个封装。
- **如果你想保持AI原生：** 将核心构建为Python库，让LLM代理可以直接调用，之后如果有收入需求再封装UI。

根据你的背景（快速交付、技术深度、终端优先），我猜你从10个精良的CLI工具中获得的复合价值，会超过1个过度设计的GUI。先交付CLI，在自己的工作流中使用它，只有当非工程师真正出现时再添加GUI。

这个工具是什么？实际用户是谁？