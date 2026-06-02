---
audio: false
generated: true
lang: zh
layout: post
title: IntelliJ结构替换模板
translated: true
type: note
---

以下是 IntelliJ 结构替换模板的 10 个分类示例。这些模板在代码重构、编码规范实施和自动化常见代码转换方面具有强大功效。

**基础重构与简化：**

1.  **将 `if (condition) return true; else return false;` 替换为 `return condition;`**

      * **搜索模板：**
        ```java
        if ($CONDITION$) {
            return true;
        } else {
            return false;
        }
        ```
      * **替换模板：**
        ```java
        return $CONDITION$;
        ```
      * **适用场景：** 简化布尔返回语句。

2.  **将 `if (condition) { statement; }` 替换为 `if (!condition) { continue/break/return; }`（卫语句）**

      * **搜索模板：**
        ```java
        if ($CONDITION$) {
            $STATEMENTS$;
        }
        ```
      * **替换模板：**（此模板更侧重于转换建议，需手动调整内部逻辑）
        ```java
        if (!$CONDITION$) {
            // 可考虑在此处使用 continue、break 或 return
        }
        $STATEMENTS$;
        ```
      * **适用场景：** 鼓励使用卫语句优化代码流程。通常会在定位结构后使用"替换"操作。

**集合与流操作：**

3.  **将 `for (Type item : collection) { if (item.getProperty() == value) { ... } }` 替换为 Stream `filter`**

      * **搜索模板：**
        ```java
        for ($TYPE$ $ITEM$ : $COLLECTION$) {
            if ($ITEM$.$METHOD$($VALUE$)) {
                $STATEMENTS$;
            }
        }
        ```
      * **替换模板：**
        ```java
        $COLLECTION$.stream()
            .filter($ITEM$ -> $ITEM$.$METHOD$($VALUE$))
            .forEach($ITEM$ -> $STATEMENTS$); // 或使用 .map().collect() 等
        ```
      * **适用场景：** 将传统循环迁移至 Java Stream 进行过滤。此为通用示例，实际可能需要更具体的模板来处理 `map`、`collect` 等操作。

4.  **将 `new ArrayList<>().add(item1); new ArrayList<>().add(item2);` 替换为 `List.of(item1, item2);`**

      * **搜索模板：**（可能需要多个模板处理不同数量的 `add` 调用，或使用更复杂的正则表达式。此为针对两个元素的简化方案）：
        ```java
        java.util.ArrayList<$TYPE$> $LIST$ = new java.util.ArrayList<>();
        $LIST$.add($ITEM1$);
        $LIST$.add($ITEM2$);
        ```
      * **替换模板：**
        ```java
        java.util.List<$TYPE$> $LIST$ = java.util.List.of($ITEM1$, $ITEM2$);
        ```
      * **适用场景：** 使用 Java 9+ 的 `List.of()` 创建不可变列表。

**错误处理与资源管理：**

5.  **将 `try { ... } catch (Exception e) { e.printStackTrace(); }` 替换为更规范的日志记录**

      * **搜索模板：**
        ```java
        try {
            $STATEMENTS$;
        } catch (java.lang.Exception $EXCEPTION$) {
            $EXCEPTION$.printStackTrace();
        }
        ```
      * **替换模板：**
        ```java
        try {
            $STATEMENTS$;
        } catch (java.lang.Exception $EXCEPTION$) {
            // 替换为偏好的日志框架，例如：
            // logger.error("发生错误", $EXCEPTION$);
            throw new RuntimeException($EXCEPTION$); // 或抛出特定异常
        }
        ```
      * **适用场景：** 提倡使用规范的错误日志记录替代直接打印堆栈跟踪。

6.  **将 `try { ... } finally { closeable.close(); }` 替换为 `try-with-resources`**

      * **搜索模板：**
        ```java
        java.io.Closeable $CLOSEABLE$ = null;
        try {
            $CLOSEABLE$ = $INITIALIZATION$;
            $STATEMENTS$;
        } finally {
            if ($CLOSEABLE$ != null) {
                $CLOSEABLE$.close();
            }
        }
        ```
      * **替换模板：**
        ```java
        try ($CLOSEABLE$ = $INITIALIZATION$) {
            $STATEMENTS$;
        }
        ```
      * **适用场景：** 使用 `try-with-resources`（Java 7+）现代化资源管理。

**类与方法结构：**

7.  **查找可声明为 `final` 的字段**

      * **搜索模板：**
        ```java
        class $CLASS$ {
            $TYPE$ $FIELD$;
        }
        ```
      * **替换模板：**（主要用于定位，然后通过快速修复处理）
        ```java
        class $CLASS$ {
            // 若字段仅被赋值一次，可考虑添加 final 修饰符
            final $TYPE$ $FIELD$;
        }
        ```
      * **适用场景：** 识别提升不可变性的机会。需设置过滤器仅显示未被多次赋值的字段。

8.  **将 `private static final Logger logger = LoggerFactory.getLogger(MyClass.class);` 替换为自定义日志工具**

      * **搜索模板：**
        ```java
        private static final org.slf4j.Logger $LOGGER_VAR$ = org.slf4j.LoggerFactory.getLogger($CLASS_NAME$.class);
        ```
      * **替换模板：**
        ```java
        private static final org.slf4j.Logger $LOGGER_VAR$ = com.yourcompany.util.LoggerProvider.getLogger(); // 或使用工具类中更具体的 getLogger($CLASS_NAME$.class)
        ```
      * **适用场景：** 在代码库中强制实施特定的日志初始化模式。

**注解与样板代码：**

9.  **为覆写超类方法的方法添加 `@Override` 注解（若缺失）**

      * **搜索模板：**（此操作较复杂，通常由 IntelliJ 内置检查处理更佳，此处仅为演示）
        ```java
        class $CLASS$ {
            $RETURN_TYPE$ $METHOD$($PARAMS$) {
                $STATEMENTS$;
            }
        }
        ```
      * **替换模板：**（同样用于定位，然后应用快速修复）
        ```java
        class $CLASS$ {
            @Override // 若方法覆写超类方法则添加此注解
            $RETURN_TYPE$ $METHOD$($PARAMS$) {
                $STATEMENTS$;
            }
        }
        ```
      * **适用场景：** 强制实施最佳实践并捕获拼写错误。需使用过滤器验证方法是否存在于超类/接口中。

10. **将重复的 `getter/setter` 方法替换为 Lombok 注解**

      * **搜索模板：**（针对单个 getter，此类操作在类级别会高度重复）
        ```java
        public $TYPE$ get$PROPERTY_NAME$() {
            return this.$FIELD_NAME$;
        }
        ```
      * **替换模板：**（此为概念性示例，实际需删除 getter 并在字段或类上添加 `@Getter`）
        ```java
        // 建议使用 @lombok.Getter 注解替换：
        // @lombok.Getter
        // private $TYPE$ $FIELD_NAME$;
        ```
      * **适用场景：** 自动化迁移至 Lombok。对于完整类，可定位类本身并根据现有方法建议使用 `@Data` 或 `@Getter/@Setter` 注解。这是较复杂且可能需多步骤转换的高级应用。

**在 IntelliJ 中的使用方法：**

1.  进入 `Analyze（分析）` -> `Inspect Code...（检查代码...）`
2.  在 `Inspection Profile（检查配置文件）` 窗口中，点击配置文件名称旁的 `...` 进行编辑
3.  导航至 `Java` -> `General（常规）` -> `Structural Search Inspection（结构搜索检查）`
4.  点击 `+` 按钮添加新的搜索/替换模板
5.  定义 `Search Template（搜索模板）` 和 `Replacement Template（替换模板）`
6.  在 `Variables（变量）` 选项卡中定义变量约束条件（如类型、文本、数量）
7.  对代码运行检查，IntelliJ 将建议替换项或高亮显示查找结果

这些示例展现了结构搜索与替换功能的多样性。模板定义越具体、约束条件越严格，替换操作的准确性和实用性就越高。
