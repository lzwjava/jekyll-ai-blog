---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复Maven双重部署
translated: true
type: note
---

能否通过将自定义 Maven 部署插件的执行 id 设为 `default-deploy` 来解决重复部署问题？

是的——**这实际上是一种简洁的 Maven 原生解决方案。**  
如果你将执行命名为 **`default-deploy`**，它**会覆盖 `maven-deploy-plugin` 的默认生命周期绑定**，从而避免 Maven 重复运行它。

Maven 生命周期内部定义为：

```text
阶段：deploy
执行 id：default-deploy
插件：maven-deploy-plugin
```

因此，如果你定义了相同的执行 id，Maven **会替换**默认的那个，而不是额外添加一个。

---

## 正确方式

```xml
<plugin>
  <artifactId>maven-deploy-plugin</artifactId>
  <executions>
    <execution>
      <id>default-deploy</id>   <!-- 覆盖默认执行 -->
      <phase>deploy</phase>
      <goals>
        <goal>deploy</goal>
      </goals>
    </execution>
  </executions>
</plugin>
```

现在 Maven 只运行**一次**。

---

## 为何有效

Maven 按以下规则合并执行：

```text
插件 + 执行 id
```

因此：

之前：

```text
默认生命周期：
  maven-deploy-plugin（id=default-deploy）

你的 pom：
  maven-deploy-plugin（id=custom-deploy）
```

结果 → 两个执行

之后：

```text
默认生命周期：
  maven-deploy-plugin（id=default-deploy）

你的 pom：
  maven-deploy-plugin（id=default-deploy）
```

结果 → 一个执行（被覆盖）

---

## 这实际上比 skip=true 更好

因为：

* 保持生命周期清晰
* 避免全局禁用插件
* 与父 POM 兼容性良好
* 在多模块构建中更易维护

---

## 重要注意事项

这仅适用于覆盖 **maven-deploy-plugin** 本身的情况。

如果你在使用**另一个自定义插件**，例如：

```xml
com.company:custom-deploy-plugin
```

那么即使将其命名为 `default-deploy` 也**不会覆盖** Maven 默认插件——  
你仍然会得到**两次部署**。

因为 Maven 按以下规则匹配：

```text
groupId + artifactId + executionId
```

不同插件 ≠ 覆盖。

---

## 总结

✔ 相同插件 + `id=default-deploy` → 覆盖默认执行  
✔ 不同插件 + `id=default-deploy` → 仍会重复部署  
✔ 最安全：覆盖或跳过默认插件

所以你的想法是**正确且常用的**。