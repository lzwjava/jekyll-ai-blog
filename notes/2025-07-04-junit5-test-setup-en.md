---
audio: false
generated: true
lang: en
layout: post
title: JUnit 5 File-Based Testing Setup
translated: false
type: note
---

Here's a simplified setup using **only JUnit 5** (without Mockito) for testing your algorithm solutions with input files (`1.in`):

---

### 1. Update `pom.xml` (JUnit Only)
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

### 2. Directory Structure
```
src/
├── main/
│   ├── java/com/algorithm/solutions/codeforces/CF123A.java  # Example solution
│   └── resources/codeforces/1.in                           # Input file
└── test/
    ├── java/com/algorithm/solutions/codeforces/CF123ATest.java  # Test class
    └── resources/codeforces/1.expected                         # Expected output (optional)
```

---

### 3. Example Test Class (`CF123ATest.java`)
```java
package com.algorithm.solutions.codeforces;

import org.junit.jupiter.api.Test;
import java.io.*;

import static org.junit.jupiter.api.Assertions.*;

class CF123ATest {

    @Test
    void testWithInputFile() throws IOException {
        // Redirect stdin from src/test/resources
        InputStream originalIn = System.in;
        FileInputStream fileIn = new FileInputStream("src/test/resources/codeforces/1.in");
        System.setIn(fileIn);

        // Redirect stdout to capture output
        PrintStream originalOut = System.out;
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));

        // Run the solution
        CF123A.main(new String[0]);

        // Restore streams
        System.setIn(originalIn);
        System.setOut(originalOut);

        // Verify output (optionally compare with 1.expected)
        String output = outContent.toString().trim();
        assertTrue(output.endsWith("42"));  // Example assertion
    }
}
```

---

### 4. Key Features:
1. **Input Redirection**
   - Reads `1.in` from `src/test/resources` as `System.in`.
   - Uses `ByteArrayOutputStream` to capture `System.out`.

2. **Output Verification**
   - Assert against expected output (or check key patterns).

3. **Clean Resource Handling**
   - Restores original `System.in`/`System.out` after test.

---

### 5. Run Tests
```bash
mvn test
```
Or via IDE (IntelliJ/Eclipse/VSCode).

---

### 6. Alternative: Parameterized Tests (Multiple Inputs)
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
Create `src/test/resources/codeforces/test_cases.csv`:
```csv
input,expected
1 2 3,6
4 5 6,15
```

---

This gives you a **lightweight testing setup** with:
- No Mockito dependencies
- Input/output redirection
- IDE/Maven compatibility
- Support for file-based testing

Let me know if you'd like to adapt this for a specific problem!
