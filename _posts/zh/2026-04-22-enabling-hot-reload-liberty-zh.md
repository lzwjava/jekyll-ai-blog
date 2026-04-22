---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Liberty热重载功能启用
translated: true
type: note
---

**问题：**
当源代码文件被修改时，如何在 IBM WebSphere Liberty Profile 中启用 Java 代码和 EAR 变更的热加载（实时重载）？

---

**回答：**

相较于传统的应用服务器，IBM WebSphere Liberty（Liberty 配置）的热加载功能相当不错，但这取决于你*如何*构建部署和开发工作流。理解以下两个层次很重要：

---

# 1. 基础热重载（类文件/资源变更）

Liberty 支持自动检测以下文件的变更：

* `.class` 文件
* `.jsp`、`.html`、`.xml` 文件
* 部分配置文件

### ✅ 启用方法

在你的 `server.xml` 中，确保包含：

```xml
<applicationMonitor updateTrigger="mbean" dropinsEnabled="true"/>
```

或更常用的配置：

```xml
<applicationMonitor updateTrigger="polled" pollingRate="500ms"/>
```

### 工作原理？

* Liberty 扫描文件变更
* 当 `.class` 文件改变 → 重新加载类加载器
* 无需完全重启服务器

### ⚠️ 局限性

* 最适合**解压部署的应用**
* 对打包的 `.ear` 或 `.war` 文件效果不佳

---

# 2. 最佳实践：使用*解压的 EAR/WAR*（关键）

不要部署：

```
app.ear
```

而是使用：

```
app.ear/
  META-INF/
  lib/
  myapp.war/
    WEB-INF/classes/
```

### 为什么？

Liberty 监控文件系统变更。如果是打包的 EAR：

* 你必须重新构建 EAR → 速度慢
* Liberty 可能重新部署整个应用

使用解压的 EAR：

* 修改 `.class` → 即时重载
* 修改 JSP → 即时生效
* 无需打包步骤

---

# 3. 开发模式（推荐）

Liberty 提供了强大的开发模式：

### 使用 Maven：

```bash
mvn liberty:dev
```

### 或 Gradle：

```bash
gradle libertyDev
```

### 提供的功能：

* 自动编译 Java 源码
* 自动部署变更
* 浏览器实时重载
* 增量更新

👉 这是**最接近 Spring Boot DevTools 的体验**

---

# 4. EAR 变更 / 完全应用重载

如果修改：

* `application.xml`
* `lib/` 中的依赖
* EAR 的结构

Liberty 将会：

* 触发完全的应用重启（不是完全的服务器重启）

### 你可以通过以下方式强制重载：

```bash
touch server.xml
```

或使用 JMX（`updateTrigger="mbean"`）

---

# 5. IDE 集成（非常重要）

如果你使用：

### IntelliJ IDEA

* 使用**解压的工件**
* 启用：

  * "自动构建项目"
  * Registry：`compiler.automake.allow.when.app.running=true`

### Eclipse

* 使用 **WebSphere Liberty Tools**
* 启用：

  * "资源变更时自动发布"

---

# 6. 进阶：类加载器行为

Liberty 使用**动态类加载**，但需要注意：

* 静态字段**不会**重置
* 某些框架缓存机制较强

因此有时你必须：

```bash
mvn liberty:stop
mvn liberty:start
```

---

# 7. 常见陷阱（非常重要）

### ❌ 每次都打包 EAR

→ 会破坏热重载

### ❌ 错误使用共享库

→ 变更无法检测

### ❌ 框架干扰

例如：

* Hibernate 缓存
* Spring 单例 Bean

---

# 8. 实用工作流（推荐配置）

为获得最佳开发者体验：

1. 使用解压的 EAR/WAR
2. 运行：

   ```bash
   mvn liberty:dev
   ```
3. 编辑 Java 代码
4. 让 Maven 自动编译
5. Liberty 即时重载

---

# 9. 总结

| 场景             | 是否有效？ | 备注         |
| ---------------- | ---------- | ------------ |
| 变更 `.class`    | ✅         | 快速重载     |
| 变更 JSP/HTML    | ✅         | 即时生效     |
| 变更 EAR 结构    | ⚠️         | 应用重启     |
| 打包的 EAR       | ❌         | 避免         |
| 解压的 EAR       | ✅         | 最佳方案     |

---

如果需要，我可以展示：

* 适用于 Liberty 热重载的**完整 Maven 项目配置**
* 或与 **Tomcat / Spring Boot DevTools / JRebel** 进行比较（存在较大差异）