---
audio: false
date: 2025-09-10
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: Maven中跳过Angular构建
translated: true
type: note
---

简短回答：是的——你可以跳过 Angular/npm 构建，但不能使用像 `--skip-web` 这样的内置标志。请使用以下方法之一。

### 1) 在多模块构建中排除 Web 模块

如果你的 Angular 应用是独立的 Maven 模块（例如 `web`），只需在反应器中排除它：

```
mvn -pl '!web' -am clean package
```

或者仅构建后端模块：

```
mvn -pl :backend -am clean package
```

（`-am` 会构建所需的依赖项；`!web` 语法会排除该模块。）

### 2) 添加“跳过前端”属性（适用于 frontend-maven-plugin 或 exec）

使用属性控制 npm 目标的执行，并通过命令行切换。

**POM（web 模块或父级）：**

```xml
<properties>
  <skip.frontend>false</skip.frontend>
</properties>

<build>
  <plugins>
    <!-- 示例：com.github.eirslett:frontend-maven-plugin -->
    <plugin>
      <groupId>com.github.eirslett</groupId>
      <artifactId>frontend-maven-plugin</artifactId>
      <version>...你的版本...</version>
      <configuration>
        <skip>${skip.frontend}</skip>
      </configuration>
      <executions>
        <execution>
          <id>npm-build</id>
          <phase>prepare-package</phase>
          <goals>
            <goal>npm</goal>
          </goals>
          <configuration>
            <arguments>run build</arguments>
          </configuration>
        </execution>
      </executions>
    </plugin>

    <!-- 如果你使用 exec-maven-plugin 调用 npm -->
    <plugin>
      <groupId>org.codehaus.mojo</groupId>
      <artifactId>exec-maven-plugin</artifactId>
      <version>...你的版本...</version>
      <executions>
        <execution>
          <id>npm-build</id>
          <phase>prepare-package</phase>
          <goals><goal>exec</goal></goals>
          <configuration>
            <skip>${skip.frontend}</skip>
            <executable>npm</executable>
            <arguments>
              <argument>run</argument>
              <argument>build</argument>
            </arguments>
          </configuration>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

**命令行：**

```
mvn -Dskip.frontend=true clean package
```

### 3) 使用 Maven 配置文件

将前端构建仅绑定到“with-frontend”配置文件中，并在开发中将“skip-frontend”配置文件设为默认。

**POM：**

```xml
<profiles>
  <profile>
    <id>with-frontend</id>
    <activation>
      <property>
        <name>!skip.frontend</name>
      </property>
    </activation>
    <build>
      <plugins>
        <!-- 同上方的插件配置，但不带 skip -->
      </plugins>
    </build>
  </profile>
</profiles>
```

**命令行：**

* 正常（跳过）：`mvn -Dskip.frontend clean package`
* 发布（构建 UI）：`mvn -Pwith-frontend clean package`

---

## 如果你*确实*需要构建 UI 时的加速技巧

* 确保 Angular 的持久缓存已开启（Angular CLI 默认启用缓存；在 CI 中保持 `node_modules` 和 `.angular/cache` 被缓存）。
* 仅在发布时运行 `ng build`；在开发中，单独提供 UI 服务（`npm start`），并让 Spring 提供预构建的静态资源（例如，将 `dist/` 放在 `src/main/resources/static` 下用于打包构建）。
* 考虑拆分仓库，使 Angular 应用完全不是 Maven 模块；仅在前端文件更改时构建它。
* 如果你使用的是较新的 Angular，请使用默认的 esbuild/Vite 构建器，并在 CI 发布构建中禁用源映射。

---

### 总结

使用 `-pl '!web'` 排除 Web 模块，**或者**添加 `skip.frontend` 属性并配置你的插件执行以遵循它。虽然没有标准的 `mvn package --skip-web`，但上述两种模式是可靠且常见的。
