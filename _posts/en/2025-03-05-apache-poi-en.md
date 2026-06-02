---
audio: false
generated: true
lang: en
layout: post
title: Apache POI Library
translated: false
type: note
---

It seems there might be a typo in your query "how to use com.apache.poi." In Java, Apache POI's package name starts with `org.apache.poi`, not `com.apache.poi`, as Apache projects typically use the `org` domain. I’ll assume you meant `org.apache.poi`, which is a popular Java library for working with Microsoft Office file formats like Excel, Word, and PowerPoint. Below is a guide on how to use it, focusing on the most common use case: handling Excel files.

---

### **What is Apache POI?**

Apache POI (Poor Obfuscation Implementation) is a Java library that allows you to read, write, and manipulate Microsoft Office documents programmatically. It’s widely used for Excel files (.xls and .xlsx), but it also supports Word and PowerPoint formats.

---

### **Step 1: Add Apache POI to Your Project**

To use Apache POI, you need to include it in your Java project. If you’re using **Maven**, add the following dependencies to your `pom.xml` file:

- For basic Excel support (both .xls and .xlsx):

```xml
<dependency>
    <groupId>org.apache.poi</groupId>
    <artifactId>poi</artifactId>
    <version>5.2.2</version>
</dependency>
```

- For .xlsx files specifically (requires additional OOXML support):

```xml
<dependency>
    <groupId>org.apache.poi</groupId>
    <artifactId>poi-ooxml</artifactId>
    <version>5.2.2</version>
</dependency>
```

**Note**: Check the [Apache POI website](https://poi.apache.org/) or Maven Central for the latest version.

If you’re not using Maven, download the JAR files from the Apache POI website and add them to your project’s classpath.

---

### **Step 2: Basic Usage for Excel Files**

Apache POI provides classes to work with Excel workbooks, sheets, rows, and cells. Here’s how to get started with reading and writing Excel files.

#### **Reading an Excel File**

To read an Excel file, you’ll use `WorkbookFactory` to create a `Workbook` instance, then navigate through sheets, rows, and cells.

Here’s a simple example to read and print the contents of an Excel file:

```java
import org.apache.poi.ss.usermodel.*;
import java.io.FileInputStream;
import java.io.IOException;

public class ExcelReader {
    public static void main(String[] args) {
        String filePath = "example.xlsx"; // Path to your Excel file
        try (FileInputStream fis = new FileInputStream(filePath);
             Workbook workbook = WorkbookFactory.create(fis)) {
            // Loop through all sheets
            for (int i = 0; i < workbook.getNumberOfSheets(); i++) {
                Sheet sheet = workbook.getSheetAt(i);
                System.out.println("Sheet: " + sheet.getSheetName());
                // Loop through rows and cells
                for (Row row : sheet) {
                    for (Cell cell : row) {
                        DataFormatter formatter = new DataFormatter();
                        String value = formatter.formatCellValue(cell);
                        System.out.print(value + "\t");
                    }
                    System.out.println(); // New line after each row
                }
                System.out.println(); // New line after each sheet
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

**Key Points**:

- `WorkbookFactory.create()` works with both .xls (HSSF) and .xlsx (XSSF) files.
- `DataFormatter` simplifies handling different cell types (strings, numbers, dates) by formatting them as strings.
- Use `try-with-resources` to automatically close the file and workbook.

#### **Handling Different Cell Types**

If you need to process cell values based on their type (e.g., string, number, date), check the cell type explicitly:

```java
Cell cell = row.getCell(0); // Get first cell in a row
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
        System.out.println("Unknown cell type");
}
```

#### **Writing to an Excel File**

To create or modify an Excel file, you’ll create a workbook, add sheets, rows, and cells, then save it.

Here’s an example to create a new .xlsx file:

```java
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import java.io.FileOutputStream;
import java.io.IOException;

public class ExcelWriter {
    public static void main(String[] args) {
        try (Workbook workbook = new XSSFWorkbook()) {
            Sheet sheet = workbook.createSheet("MySheet");
            Row row = sheet.createRow(0); // First row
            Cell cell = row.createCell(0); // First cell
            cell.setCellValue("Hello, POI!");

            // Write to file
            try (FileOutputStream fos = new FileOutputStream("output.xlsx")) {
                workbook.write(fos);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

**Key Points**:

- Use `XSSFWorkbook` for .xlsx files or `HSSFWorkbook` for .xls files.
- Call `workbook.write()` to save the file.

---

### **Step 3: Key Classes and Concepts**

Here are the main classes you’ll use in Apache POI for Excel:

- **`Workbook`**: Represents the entire Excel file (`XSSFWorkbook` for .xlsx, `HSSFWorkbook` for .xls).
- **`Sheet`**: A single sheet in the workbook.
- **`Row`**: A row in a sheet.
- **`Cell`**: A cell in a row.
- **`WorkbookFactory`**: Creates a workbook from a file or stream, handling both file types.
- **`DataFormatter`**: Formats cell values as strings.
- **`DateUtil`**: Helps identify and handle date-formatted numeric cells.

For other formats:

- **Word**: Use `XWPFDocument` (.docx) or `HWPFDocument` (.doc).
- **PowerPoint**: Use `XMLSlideShow` (.pptx) or `HSLFSlideShow` (.ppt).

---

### **Step 4: Tips and Best Practices**

- **Resource Management**: Always use `try-with-resources` to close files and workbooks, preventing memory leaks.
- **Error Handling**: Catch `IOException` for file operations and check for null rows/cells when accessing by index (e.g., `sheet.getRow(i)` may return null).
- **Large Files**: For large Excel files, consider the streaming API (`SXSSFWorkbook` for writing, `XSSFSheetXMLHandler` for reading) to reduce memory usage.
- **Compatibility**: POI may not support all features of the latest Office formats—check the [official documentation](https://poi.apache.org/) for details.

---

### **Summary**

To use `org.apache.poi`:

1. Add the library to your project (e.g., via Maven).
2. Use `WorkbookFactory` to read existing files or create new workbooks with `XSSFWorkbook`/`HSSFWorkbook`.
3. Access and manipulate data via `Sheet`, `Row`, and `Cell` objects.
4. Save changes by writing to a file.
5. Handle exceptions and close resources properly.

This covers the basics of using Apache POI, with a focus on Excel files. If you had a specific task in mind (e.g., working with Word or PowerPoint), let me know, and I can tailor the explanation further!
