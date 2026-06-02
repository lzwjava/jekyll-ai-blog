---
audio: false
date: 2025-09-11
generated: true
image: false
lang: zh
layout: post
model: mistralai/mistral-medium-3.1
title: 复杂工作流中大型语言模型的局限性
translated: true
type: note
---

你说得非常对！LLM（包括我）确实擅长**小而专注的任务**——比如解释单个概念、生成简短代码片段或调试特定错误——但在处理**复杂的多步骤工作流**时就会遇到困难，这些工作流通常涉及：

1. **多个相互关联的配置**（例如 Maven 的 `pom.xml` 文件、Jacoco 代理参数、Python 测试集成）
2. **有状态依赖**（例如"先更新 `module-A/pom.xml`，然后用这些标志运行 `mvn test`，最后合并报告"）
3. **跨系统交互**（例如 Java + Python + CI 工具如 Jenkins/GitHub Actions）
4. **上下文切换**（例如"现在忘记 Java 部分——我们如何在 Python 中解析 Jacoco XML？"）

---

### **为什么 LLM 难以处理复杂工作流**

1. **没有持久记忆**：除非你明确提醒，否则我们不会"记住"之前的步骤（即使如此，上下文窗口也有限制）
2. **线性思维**：我们逐步生成响应，但无法动态跟踪依赖关系（例如"你在运行代理之前执行了 `mvn clean` 吗？"）
3. **过度优化单一答案**：我们被训练提供*一个*完整答案，而不是迭代式指导
4. **没有执行环境**：我们无法运行命令来验证 `jacoco:prepare-agent` 是否在你的设置中实际工作

---

### **更好的方法："分而治之，逐步验证"**

对于像 **Jacoco + 多模块 Maven + Python 测试**这样的问题，将其分解为**原子步骤**并逐一验证。例如：

#### **步骤 1：验证 Jacoco 代理设置（Java 端）**

```bash
# 在单个模块中（例如 module-A）：
mvn clean test -Pcoverage
```

- **检查**：`target/site/jacoco/index.html` 是否存在？
- **调试**：如果不存在，分享 Jacoco 的 `pom.xml` 片段和错误日志

#### **步骤 2：生成合并报告（多模块）**

```bash
mvn jacoco:report-aggregate
```

- **检查**：是否创建了 `target/site/jacoco-aggregate/index.html`？
- **调试**：如果缺失，验证父 `pom.xml` 中的 `<module>` 路径

#### **步骤 3：为 Python 导出（XML/CSV）**

```bash
# 将 Jacoco 二进制文件转换为 XML
java -jar jacoco-cli.jar report jacoco.exec --xml output.xml
```

- **检查**：`output.xml` 是否包含 `<package>` 标签？
- **调试**：如果为空，确保测试运行时使用了代理（`-javaagent:jacocoagent.jar`）

#### **步骤 4：Python 集成**

```python
import xml.etree.ElementTree as ET
tree = ET.parse("output.xml")
coverage = tree.find(".//counter[@type='LINE'][@covered]")
print(f"覆盖行数: {coverage.get('covered')}/{coverage.get('missed')}")
```

- **检查**：脚本是否输出预期数字？
- **调试**：如果没有，分享 XML 结构和 Python 错误

---

### **如何有效使用 LLM**

1. **隔离问题**：
   - *"这是我 module-A 的 `pom.xml`。为什么 `jacoco:prepare-agent` 没有添加 VM 参数？"*
   - *（比"帮我为 5 个模块 + Python 设置 Jacoco"更好）*

2. **分享最小可复现上下文**：
   - 错误日志、配置片段（不是整个文件）以及**你已经尝试过的方法**

3. **迭代调试**：
   - **你**："步骤 1 失败，显示 `No tests run`。这是日志。"
   - **LLM**："在你的 `maven-surefire-plugin` 中添加 `<test>` 目标。"
   - **你**："现在步骤 2 工作了，但报告是空的..."

4. **让我们处理"微任务"**：
   - *"写一个 Python 脚本来解析 Jacoco XML，如果覆盖率 < 80% 就失败"*
   - *"解释 Maven 中 Jacoco 的 `<execution>` 标签"*

---

### **自动化复杂工作流的工具**

由于 LLM 无法管理状态，请使用：

- **Shell 脚本**（例如 `setup_coverage.sh` 来链式执行 Maven/Python 命令）
- **Makefiles**（定义 `make test-coverage` 来运行所有步骤）
- **CI 模板**（具有明确步骤的 GitHub Actions/Jenkins 流水线）
- **Docker**（容器化环境以避免"在我机器上能运行"的问题）

---

### **关键要点**

**LLM 就像是超级增强版的 `man` 手册或 Stack Overflow**——对于**独立组件**很出色，但不适合编排整个系统。对于复杂任务：

1. **分解问题**
2. **验证每个步骤**
3. **提出有针对性的问题**

你想让我更深入地探讨上面的任何步骤吗（例如在 Python 中解析 Jacoco XML 或多模块 Maven 设置）？
