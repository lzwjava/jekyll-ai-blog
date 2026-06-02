---
audio: false
generated: true
lang: zh
layout: post
title: Apache POI库
translated: true
type: note
---

您的查询中似乎存在拼写错误 "how to use com.apache.poi"。在Java中，Apache POI的包名以`org.apache.poi`开头，而非`com.apache.poi`，因为Apache项目通常使用`org`域名。我将假定您指的是`org.apache.poi`，这是一个用于处理Microsoft Office文件格式（如Excel、Word和PowerPoint）的流行Java库。以下是如何使用它的指南，重点介绍最常见的用例：处理Excel文件。

---

### **什么是Apache POI？**

Apache POI（Poor Obfuscation Implementation）是一个Java库，允许您以编程方式读取、写入和操作Microsoft Office文档。它广泛用于Excel文件（.xls和.xlsx），但也支持Word和PowerPoint格式。

---

### **步骤1：将Apache POI添加到项目中**

要使用Apache POI，您需要将其包含在Java项目中。如果使用**Maven**，请将以下依赖项添加到`pom.xml`文件中：

- 对于基本的Excel支持（包括.xls和.xlsx）：

```xml
<dependency>
    <groupId>org.apache.poi</groupId>
    <artifactId>poi</artifactId>
    <version>5.2.2</version>
</dependency>
```

- 特别是对于.xlsx文件（需要额外的OOXML支持）：

```xml
<dependency>
    <groupId>org.apache.poi</groupId>
    <artifactId>poi-ooxml</artifactId>
    <version>5.2.2</version>
</dependency>
```

**注意**：请查看[Apache POI官网](https://poi.apache.org/)或Maven Central以获取最新版本。

如果不使用Maven，请从Apache POI网站下载JAR文件，并将其添加到项目的类路径中。

---

### **步骤2：Excel文件的基本用法**

Apache POI提供了用于处理Excel工作簿、工作表、行和单元格的类。以下是开始读取和写入Excel文件的方法。

#### **读取Excel文件**

要读取Excel文件，您将使用`WorkbookFactory`创建一个`Workbook`实例，然后导航工作表、行和单元格。

以下是一个简单的示例，用于读取并打印Excel文件的内容：

```java
import org.apache.poi.ss.usermodel.*;
import java.io.FileInputStream;
import java.io.IOException;

public class ExcelReader {
    public static void main(String[] args) {
        String filePath = "example.xlsx"; // Excel文件的路径
        try (FileInputStream fis = new FileInputStream(filePath);
             Workbook workbook = WorkbookFactory.create(fis)) {
            // 遍历所有工作表
            for (int i = 0; i < workbook.getNumberOfSheets(); i++) {
                Sheet sheet = workbook.getSheetAt(i);
                System.out.println("工作表: " + sheet.getSheetName());
                // 遍历行和单元格
                for (Row row : sheet) {
                    for (Cell cell : row) {
                        DataFormatter formatter = new DataFormatter();
                        String value = formatter.formatCellValue(cell);
                        System.out.print(value + "\t");
                    }
                    System.out.println(); // 每行后换行
                }
                System.out.println(); // 每个工作表后换行
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

**关键点**：

- `WorkbookFactory.create()`适用于.xls（HSSF）和.xlsx（XSSF）文件。
- `DataFormatter`通过将不同单元格类型（字符串、数字、日期）格式化为字符串来简化处理。
- 使用`try-with-resources`自动关闭文件和 workbook。

#### **处理不同的单元格类型**

如果需要根据单元格类型（例如字符串、数字、日期）处理单元格值，请显式检查单元格类型：

```java
Cell cell = row.getCell(0); // 获取行中的第一个单元格
switch (cell.getCellType()) {
    case STRING:
        System.out.println(cell.getStringCellValue());
        break;
    case NUMERIC:
        if (DateUtil.isCellDateFormatted(cell)) {
            System.out.println(cell.getDateCellValue());
        } else {
            System.out.println(cell.getNumericCellValue());
        }
        break;
    case BOOLEAN:
        System.out.println(cell.getBooleanCellValue());
        break;
    default:
        System.out.println("未知单元格类型");
}
```

#### **写入Excel文件**

要创建或修改Excel文件，您需要创建一个工作簿，添加工作表、行和单元格，然后保存它。

以下是一个创建新的.xlsx文件的示例：

```java
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import java.io.FileOutputStream;
import java.io.IOException;

public class ExcelWriter {
    public static void main(String[] args) {
        try (Workbook workbook = new XSSFWorkbook()) {
            Sheet sheet = workbook.createSheet("MySheet");
            Row row = sheet.createRow(0); // 第一行
            Cell cell = row.createCell(0); // 第一个单元格
            cell.setCellValue("Hello, POI!");

            // 写入文件
            try (FileOutputStream fos = new FileOutputStream("output.xlsx")) {
                workbook.write(fos);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

**关键点**：

- 对于.xlsx文件使用`XSSFWorkbook`，对于.xls文件使用`HSSFWorkbook`。
- 调用`workbook.write()`保存文件。

---

### **步骤3：关键类和概念**

以下是Apache POI中用于Excel的主要类：

- **`Workbook`**：表示整个Excel文件（.xlsx使用`XSSFWorkbook`，.xls使用`HSSFWorkbook`）。
- **`Sheet`**：工作簿中的单个工作表。
- **`Row`**：工作表中的一行。
- **`Cell`**：行中的一个单元格。
- **`WorkbookFactory`**：从文件或流创建工作簿，处理两种文件类型。
- **`DataFormatter`**：将单元格值格式化为字符串。
- **`DateUtil`**：帮助识别和处理日期格式的数字单元格。

对于其他格式：

- **Word**：使用`XWPFDocument`（.docx）或`HWPFDocument`（.doc）。
- **PowerPoint**：使用`XMLSlideShow`（.pptx）或`HSLFSlideShow`（.ppt）。

---

### **步骤4：提示和最佳实践**

- **资源管理**：始终使用`try-with-resources`关闭文件和工作簿，防止内存泄漏。
- **错误处理**：捕获文件操作的`IOException`，并在按索引访问时检查空行/单元格（例如，`sheet.getRow(i)`可能返回null）。
- **大文件**：对于大型Excel文件，考虑使用流式API（写入使用`SXSSFWorkbook`，读取使用`XSSFSheetXMLHandler`）以减少内存使用。
- **兼容性**：POI可能不支持最新Office格式的所有功能——请查看[官方文档](https://poi.apache.org/)了解详情。

---

### **总结**

要使用`org.apache.poi`：

1. 将库添加到项目中（例如通过Maven）。
2. 使用`WorkbookFactory`读取现有文件，或使用`XSSFWorkbook`/`HSSFWorkbook`创建新的工作簿。
3. 通过`Sheet`、`Row`和`Cell`对象访问和操作数据。
4. 通过写入文件保存更改。
5. 正确处理异常并关闭资源。

这涵盖了使用Apache POI的基础知识，重点是Excel文件。如果您有特定任务（例如处理Word或PowerPoint），请告诉我，我可以进一步调整说明！
