---
audio: false
generated: true
lang: zh
layout: post
title: XML Schema 数据类型
translated: true
type: note
---

XML Schema 定义了一套丰富的内置数据类型，可用于指定元素和属性中允许的数据类型。这些数据类型确保 XML 内容符合预期的格式和约束条件。

XML Schema 中的内置数据类型大致分为**基本类型**和**派生类型**。派生类型基于基本类型创建，通过应用限制或其他修改方式形成。

**基本数据类型（19种内置类型）：**

这些是基础且不可再分的数据类型，所有其他内置和用户定义的简单类型都由此派生。

* **String：** 表示字符串
* **Boolean：** 表示逻辑值（true 或 false，也可用 1 或 0 表示）
* **Decimal：** 表示任意精度的十进制数字
* **Float：** 表示单精度 32 位浮点数
* **Double：** 表示双精度 64 位浮点数
* **Duration：** 表示时间间隔
* **DateTime：** 表示特定的时间点，包含日期和时间
* **Time：** 表示 24 小时周期内的特定时间点
* **Date：** 表示日历日期
* **gYearMonth：** 表示特定年份和月份
* **gYear：** 表示特定年份
* **gMonthDay：** 表示特定月份和日期
* **gDay：** 表示月中的特定某天
* **gMonth：** 表示年中的特定某月
* **HexBinary：** 表示十六进制格式的二进制数据
* **Base64Binary：** 表示 Base64 编码的二进制数据
* **AnyURI：** 表示统一资源标识符（URI）
* **QName：** 表示限定名（带命名空间前缀的名称）
* **NOTATION：** 表示模式中声明的记法名称

**派生数据类型（约25种内置类型）：**

这些数据类型通过应用长度、范围、模式等约束条件从基本类型派生而来。

**从 `string` 派生的类型：**

* `normalizedString`：表示将换行符、制表符和回车符替换为空格，且没有前导或尾随空格的字符串
* `token`：表示没有前导或尾随空白，且内部没有两个或以上连续空白字符的规范化字符串
* `language`：表示符合 RFC 3066 定义的语言标识符
* `NMTOKEN`：表示名称标记（可包含字母、数字、点号、连字符和下划线）
* `NMTOKENS`：表示以空格分隔的 `NMTOKEN` 列表
* `Name`：表示 XML 名称（必须以字母或下划线开头，后跟字母、数字、点号、连字符或下划线）
* `NCName`：表示无冒号名称（类似 `Name` 但不能包含冒号）
* `ID`：表示 XML 文档内的唯一标识符
* `IDREF`：表示对同一文档中 `ID` 值的引用
* `IDREFS`：表示以空格分隔的 `IDREF` 值列表
* `ENTITY`：表示对 DTD 中声明的未解析实体的引用（在 XML Schema 中较少使用）
* `ENTITIES`：表示以空格分隔的 `ENTITY` 值列表（在 XML Schema 中较少使用）

**从 `decimal` 派生的类型：**

* `integer`：表示整数（无小数部分）
* `nonPositiveInteger`：表示小于等于 0 的整数
* `negativeInteger`：表示严格小于 0 的整数
* `long`：表示 64 位有符号整数
* `int`：表示 32 位有符号整数
* `short`：表示 16 位有符号整数
* `byte`：表示 8 位有符号整数
* `nonNegativeInteger`：表示大于等于 0 的整数
* `unsignedLong`：表示 64 位无符号整数
* `unsignedInt`：表示 32 位无符号整数
* `unsignedShort`：表示 16 位无符号整数
* `unsignedByte`：表示 8 位无符号整数
* `positiveInteger`：表示严格大于 0 的整数

**其他派生类型：**

* `dateTimeStamp`（XML Schema 1.1 中引入）：类似于 `dateTime` 但包含时区信息
* `yearMonthDuration`（XML Schema 1.1 中引入）：表示以年和月为单位的时长
* `dayTimeDuration`（XML Schema 1.1 中引入）：表示以天、小时、分钟和秒为单位的时长
* `precisionDecimal`（XML Schema 1.1 中引入）：表示保留精度的十进制数字

**用户定义数据类型：**

除了内置类型，XML Schema 还允许您使用以下机制定义自己的简单和复杂数据类型：

* **限制：** 通过限制现有类型（内置或用户定义）的范围或格式来创建新类型
* **列表：** 定义其值为另一个简单类型值序列的类型
* **联合：** 定义其值可以来自两个或多个其他简单类型值空间的类型

在 XML Schema 中定义元素和属性时，使用 `type` 属性指定内容应遵循的数据类型。这确保了数据的有效性并促进了数据处理。

例如：

```xml
<xs:element name="age" type="xs:positiveInteger"/>
<xs:element name="name" type="xs:string"/>
<xs:attribute name="status" type="xs:token"/>
```

在此代码片段中，`age` 元素被定义为保存正整数，`name` 元素保存字符串，`status` 属性保存 token（具有特定空白处理的规范化字符串）。

理解这些数据类型是创建有效且定义良好的 XML Schema 的基础。您可以在 W3C XML Schema Part 2: Datatypes 规范中找到完整的详细信息和正式定义。
