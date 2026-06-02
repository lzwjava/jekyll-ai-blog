---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Maven部署插件与Nexus冲突
translated: true
type: note
---

是的——这是一个**常见的 Maven 部署问题**。
如果**你的自定义部署插件**和**默认的 Maven 部署插件**同时在 `deploy` 阶段运行，Maven 会尝试向 Nexus **重复上传相同的构件**。

这通常会导致：

* 第一次部署 → 成功 ✅
* 第二次部署 → 失败 ❌（HTTP 400 / 构件已存在 / 不允许覆盖）

大多数 Nexus 仓库**不允许重新部署**发行版构件，因此第二次上传会被拒绝。

---

## 问题成因

Maven 生命周期已自动绑定此插件：

```
deploy 阶段
 └── maven-deploy-plugin（默认）
```

如果你还添加了类似配置：

```xml
<plugin>
  <groupId>com.company</groupId>
  <artifactId>custom-deploy-plugin</artifactId>
  <executions>
    <execution>
      <phase>deploy</phase>
      <goals>
        <goal>deploy</goal>
      </goals>
    </execution>
  </executions>
</plugin>
```

则两者都会运行：

```
deploy 阶段
 ├── 自定义部署插件
 └── maven-deploy-plugin（默认）
```

因此 Nexus 会收到：

```
PUT artifact.jar  （成功）
PUT artifact.jar  （400 错误请求）
```

---

## 解决方案（3 种正确方式）

### 方案 1 — 禁用默认部署插件（最常用）

```xml
<plugin>
  <artifactId>maven-deploy-plugin</artifactId>
  <version>3.1.1</version>
  <configuration>
    <skip>true</skip>
  </configuration>
</plugin>
```

仅保留自定义部署插件。

---

### 方案 2 — 调整自定义插件执行阶段

将自定义插件运行在 **deploy 之前**的阶段，例如：

```xml
<phase>package</phase>
```

执行顺序变为：

```
package → 自定义插件
deploy  → 默认部署插件
```

避免重复上传。

---

### 方案 3 — 完全禁用部署（由 CI 控制）

如果 CI 负责部署：

```
mvn deploy -DskipDeploy
```

或

```xml
<properties>
  <maven.deploy.skip>true</maven.deploy.skip>
</properties>
```

---

## 如何确认是该问题

执行：

```
mvn -X deploy
```

查找 **两次部署执行记录**：

```
--- custom-deploy-plugin:deploy ---
Uploading to nexus...

--- maven-deploy-plugin:deploy ---
Uploading to nexus...
```

如果看到两次上传 → 即为问题所在。

---

## 典型的 Nexus 错误信息

```
400 Bad Request
Repository does not allow updating assets
Artifact already exists
```

或

```
Return code is: 400, ReasonPhrase: Bad Request.
```

---

## 最佳实践

如果存在**自定义部署逻辑**，务必：

* 禁用默认部署插件
  或
* 将自定义插件绑定到更早阶段

绝不要让两者同时在 `deploy` 阶段运行。

---

这是**企业级 Maven + Nexus 配置中非常常见的陷阱**，尤其在以下场景：

* 公司添加了内部部署插件
* 父 POM 已配置默认部署
* 子 POM 又添加了另一个部署插件
