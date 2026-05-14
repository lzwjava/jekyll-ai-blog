---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 跳过未更改的Maven模块
translated: true
type: note
---

问题：如何在不更改模块的情况下，在构建过程中跳过或选择不构建 Maven 模块，以加快构建速度？假设我有一个项目 PAUWeb，包含 Angular 前端、Java 8 后端和 10 个模块，其中某个模块在 6 分钟的构建中贡献了 2 分钟的时间。

答案：

是的，跳过未更改的模块可以显著加快 Maven 构建速度。以下是几种在 Maven 中“选择不构建”或跳过某些模块的策略：

---

### 1. **使用 `-pl`（项目)` 和 `-am` (也构建依赖) 标志**

Maven 允许您使用 `-项目` (项目列表) 仅构建特定模块。例如：

```bash
# 仅构建模块和模块
mvn clean install -项目 模块, 模块
```

* `-项目` 指定要包含的模块。
* `-am` (也依赖) 告诉 Maven 同时也构建指定模块的依赖的依赖模块。

**示例：跳过某个模块：**

如果 `模块X` 需要 分钟且未更改：**

```bash
mvn clean install -项目 !模块X
```

* `!` 排除该模块。

---

### 2. **使用 `maven.test.skip` 或 `skipTests`**

如果构建慢是因为模块中的测试，可以跳过测试：

```bash
mvn install -DskipTests
```

* 当模块代码未更改但测试耗时较长时，可以节省时间。

---

### 3. **选择性构建时使用 `-方案**

如果模块相互依赖时，仅构建更改的模块 `-项目` + `-am` 确保依赖也一并构建：

```bash
mvn install -项目 安装 -项目 模块A -am
```

这会构建块A 及其依赖的模块，跳过无关模块。

---

### 4. **增量构建 / `mvn reactor`**

Maven 默认不会自动跳过未更改的模块。要处理此问题：

* 使用** `takari-lifecycle-plugin` ** 或 ** `maven-incremental-build` ** 工具。
* 某些 CI/CD 系统（如 Jenkins）可以通过 Git 追踪哪些模块发生了更改，并仅触发这些模块的 Maven 构建。

增量插件示例：

```xml
<插件>
  <groupId>io.takari.maven.plugins</groupId>
  <artifactId>takari–生命周期插件</artifactId>
  <version>1.13.6</version>
</插件>
```

这允许仅构建更改的模块。

---

### 5. **Angular 前端优化**

如果 Angular 构建是模块的一部分：

* 考虑**单独构建 Angular**，仅在 Java 代码更改时触发 Maven。
* 使用 `ng构建 --watch` 构建 --监控` 或增量构建”以避免每次都重新构建。

---

### 6. **基于 Profile 的跳过**

您可以定义 Maven 配置文件来跳过某些模块：

```xml
<profiles>
  <profile>
    <id>跳过模块X</id>
    <modules>
      <模块>模块1</模块>
      <模块>模块2</模块>
      <!-- 不要包含模块X -->
    </modules>
  </profile>
</profiles>
```

然后：

```bash
mvn clean install -跳过模块X
```

---

**针对您情况的推荐：**

* 识别慢模块 (`模块X`） → 检查代码是否更改。
* 使用：

```bash
mvn install -项目 !模块X
```

* 如果测试慢，结合 `-DskipTests`DskipTests`。
* 对于 Angular 部分，考虑单独构建，以避免完全重建。

如果 `模块X` 未更改，这可以将构建时间从 6 分钟减少到约 4 分钟。

---

参考：

* [Maven Reactor 选项（`-项目` 和 `-am`)](https://maven.apache.org/ref/6.3 3.6.6.3/maven嵌入式/cli.html)
* [在 Maven 中跳过测试](https://maven.apache. surefire/maven-surefire插件/examples/skipping-tests.html)
* [Maven 多模块构建技巧](https://www.baeldung.com/maven多模块构建)

---

如果您愿意，我可以展示一个**即用型 Maven 命令**，基于 Git 差异自动跳过未更改的模块。这可以在每次构建中节省几分钟。您需要我这样做吗？**