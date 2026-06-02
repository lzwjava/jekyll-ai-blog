---
audio: false
generated: true
lang: zh
layout: post
title: 升级Guice以修复不安全警告
translated: true
type: note
---

```
警告信息显示：

```
WARNING: A terminally deprecated method in sun.misc.Unsafe has been called
WARNING: sun.misc.Unsafe::staticFieldBase has been called by com.google.inject.internal.aop.HiddenClassDefiner (file:/opt/homebrew/Cellar/maven/3.9.10/libexec/lib/guice-5.1.0-classes.jar)
WARNING: Please consider reporting this to the maintainers of class com.google.inject.internal.aop.HiddenClassDefiner
WARNING: sun.misc.Unsafe::staticFieldBase will be removed in a future release
```

这是**Java虚拟机（JVM）发出的警告**，并非直接源自你的代码。意味着你使用的某个库（本例中是Guice，具体为`guice-5.1.0-classes.jar`）内部调用了`sun.misc.Unsafe`中的方法（`staticFieldBase`）。

`sun.misc.Unsafe`是Java内部API，专供JDK内部进行底层操作使用。它不属于标准Java API，并且不鼓励使用，因为它可能导致不稳定或未定义的行为，且在未来的Java版本中可能被修改或移除。JVM正在提醒你，这个特定方法已被"最终弃用"，即将被移除——这意味着如果该库继续使用它且未提供替代方案，最终将导致你的应用程序崩溃。

**如何"消除"此警告：**

由于该用法存在于第三方库（Guice）中，你无法通过直接修改代码来"消除"它。以下是可采取的方案，按推荐顺序排列：

1.  **升级Guice（最推荐方案）：**
    最佳且可持续的解决方案是升级到不再使用`sun.misc.Unsafe`的新版Guice，或已迁移至标准Java API（如JDK 9引入的`VarHandle`或JDK 22标准化的外部函数与内存API JEP 454）的版本。

    从版本`guice-5.1.0-classes.jar`来看，你正在使用Guice 5.1.0。请查阅官方Guice版本及其文档，确认是否有专门针对新版Java中`sun.misc.Unsafe`使用问题的更新。通常，库维护者会关注这些弃用通知并提供更新版本。

      * **操作：** 修改你的`pom.xml`以使用更新的Guice版本。你需要找到与当前Java版本（你使用的是JDK 21）兼容的最新稳定版Guice。

    ```xml
    <dependency>
        <groupId>com.google.inject</groupId>
        <artifactId>guice</artifactId>
        <version>LATEST_GUICE_VERSION</version> </dependency>
    ```

    如果你的项目使用了其他Guice模块（如`guice-assistedinject`），可能也需要一并更新。

2.  **抑制警告（临时解决方案 - 不推荐长期使用）：**
    虽然不应长期依赖此方法，但如果该警告目前仅影响观感且不妨碍应用程序功能，可以在运行时抑制该警告。这需要通过JVM命令行参数实现。

    对于JDK 24（你当前目标是21，但随着Java发展需了解此信息），默认设置为`warn`。要抑制该警告，可显式设置为`allow`：

    可将以下配置添加到`exec-maven-plugin`中：

    ```xml
    <plugin>
        <groupId>org.codehaus.mojo</groupId>
        <artifactId>exec-maven-plugin</artifactId>
        <version>3.5.0</version>
        <configuration>
            <executable>bash</executable>
            <arguments>
                <argument>-c</argument>
                <argument>java --add-opens java.base/sun.misc=ALL-UNNAMED --sun-misc-unsafe-memory-access=allow -cp ${project.build.directory}/classes com.lzw.solutions.uva.${problem}.Main &lt; src/main/resources/uva/${problem}/1.in</argument>
            </arguments>
        </configuration>
    </plugin>
    ```

    *自我修正：* 主要警告是关于`sun.misc.Unsafe::staticFieldBase`被"最终弃用"，而非非法反射访问。因此，除非同时出现"非法反射访问"警告，否则`--add-opens java.base/sun.misc=ALL-UNNAMED`可能并非必需。针对"最终弃用"警告更直接的参数是`--sun-misc-unsafe-memory-access=allow`。

    **但请注意这是临时解决方案。** 该参数仅指示JVM允许使用`sun.misc.Unsafe`方法而不打印警告，并未解决根本问题——`sun.misc.Unsafe`最终将被移除，你的应用程序在未来JDK版本中可能崩溃。

3.  **向Guice维护者报告（警告信息已建议）：**
    警告本身建议"请考虑向`com.google.inject.internal.aop.HiddenClassDefiner`类的维护者报告此问题"。虽然你使用的是特定版本，但若确认该问题在新版Guice中仍然存在（按理应已修复），向维护团队报告将惠及社区。

**总结而言，最佳解决方案是升级Guice依赖。** `sun.misc.Unsafe` API处于持续演进状态，库需要适配Java提供的更新、更安全且官方支持的API。
