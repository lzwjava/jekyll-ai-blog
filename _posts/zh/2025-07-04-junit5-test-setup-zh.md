---
audio: false
generated: true
lang: zh
layout: post
title: JUnit 5文件测试配置
translated: true
type: note
---

以下是仅使用 **JUnit 5**（不包含 Mockito）来测试算法解决方案并读取输入文件（`1.in`）的简化设置：

---

### 1. 更新 `pom.xml`（仅 JUnit）
```xml
<dependencies>
    <!-- JUnit 5 -->
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter-api</artifactId>
        <version>5.9.2</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter-engine</artifactId>
        <version>5.9.2</version>
        <scope>test</scope>
    </dependency>
</dependencies>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.0.0-M7</version>
        </plugin>
    </plugins>
</build>
```

---

### 2. 目录结构
```
src/
├── main/
│   ├── java/com/algorithm/solutions/codeforces/CF123A.java  # 示例解决方案
│   └── resources/codeforces/1.in                           # 输入文件
└── test/
    ├── java/com/algorithm/solutions/codeforces/CF123ATest.java  # 测试类
    └── resources/codeforces/1.expected                         # 期望输出（可选）
```

---

### 3. 示例测试类（`CF123ATest.java`）
```java
package com.algorithm.solutions.codeforces;

import org.junit.jupiter.api.Test;
import java.io.*;

import static org.junit.jupiter.api.Assertions.*;

class CF123ATest {

    @Test
    void testWithInputFile() throws IOException {
        // 从 src/test/resources 重定向标准输入
        InputStream originalIn = System.in;
        FileInputStream fileIn = new FileInputStream("src/test/resources/codeforces/1.in");
        System.setIn(fileIn);

        // 重定向标准输出以捕获输出内容
        PrintStream originalOut = System.out;
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));

        // 运行解决方案
        CF123A.main(new String[0]);

        // 恢复原始流
        System.setIn(originalIn);
        System.setOut(originalOut);

        // 验证输出（可选：与 1.expected 文件比较）
        String output = outContent.toString().trim();
        assertTrue(output.endsWith("42"));  // 示例断言
    }
}
```

---

### 4. 主要特性：
1. **输入重定向**
   - 从 `src/test/resources` 读取 `1.in` 作为 `System.in`。
   - 使用 `ByteArrayOutputStream` 捕获 `System.out`。

2. **输出验证**
   - 根据期望输出进行断言（或检查关键模式）。

3. **资源清理**
   - 测试完成后恢复原始的 `System.in`/`System.out`。

---

### 5. 运行测试
```bash
mvn test
```
或通过 IDE（IntelliJ/Eclipse/VSCode）运行。

---

### 6. 替代方案：参数化测试（多组输入）
```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvFileSource;

@ParameterizedTest
@CsvFileSource(resources = "/codeforces/test_cases.csv", numLinesToSkip = 1)
void testMultipleCases(String input, String expected) {
    System.setIn(new ByteArrayInputStream(input.getBytes()));
    ByteArrayOutputStream out = new ByteArrayOutputStream();
    System.setOut(new PrintStream(out));

    CF123A.main(new String[0]);

    assertEquals(expected, out.toString().trim());
}
```
创建 `src/test/resources/codeforces/test_cases.csv`：
```csv
input,expected
1 2 3,6
4 5 6,15
```

---

这个方案提供了**轻量级测试设置**，包含：
- 无 Mockito 依赖
- 输入/输出重定向
- 兼容 IDE/Maven
- 支持基于文件的测试

如需针对特定问题调整此设置，请随时告知！
