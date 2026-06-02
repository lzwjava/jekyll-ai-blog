---
audio: false
generated: true
lang: en
layout: post
title: XML Schema Data Types
translated: false
type: note
---

XML Schema defines a rich set of built-in data types that can be used to specify the kind of data allowed in elements and attributes. These data types ensure that the XML content adheres to the intended format and constraints.

The built-in data types in XML Schema are broadly categorized into **primitive** and **derived** types. Derived types are based on primitive types and are created by applying restrictions or other modifications.

**Primitive Data Types (19 built-in):**

These are the fundamental, indivisible data types from which all other built-in and user-defined simple types are derived.

* **String:** Represents character strings.
* **Boolean:** Represents logical values (true or false, can also be represented as 1 or 0).
* **Decimal:** Represents arbitrary-precision decimal numbers.
* **Float:** Represents single-precision 32-bit floating-point numbers.
* **Double:** Represents double-precision 64-bit floating-point numbers.
* **Duration:** Represents a time interval.
* **DateTime:** Represents a specific point in time, including date and time.
* **Time:** Represents a specific point in time within a 24-hour period.
* **Date:** Represents a calendar date.
* **gYearMonth:** Represents a specific year and month.
* **gYear:** Represents a specific year.
* **gMonthDay:** Represents a specific month and day.
* **gDay:** Represents a specific day of the month.
* **gMonth:** Represents a specific month of the year.
* **HexBinary:** Represents binary data as hexadecimal values.
* **Base64Binary:** Represents binary data encoded in Base64.
* **AnyURI:** Represents a Uniform Resource Identifier (URI).
* **QName:** Represents a qualified name (a name with a namespace prefix).
* **NOTATION:** Represents the name of a notation declared in the schema.

**Derived Data Types (around 25 built-in):**

These data types are derived from the primitive types by applying constraints (facets) such as length, range, patterns, etc.

**Derived from `string`:**

* `normalizedString`: Represents character strings with line feeds, tabs, and carriage returns replaced by spaces, and with no leading or trailing spaces.
* `token`: Represents normalized strings with no leading or trailing whitespace, and no internal sequences of two or more whitespace characters.
* `language`: Represents a language identifier as defined by RFC 3066.
* `NMTOKEN`: Represents a name token (can contain letters, digits, periods, hyphens, and underscores).
* `NMTOKENS`: Represents a whitespace-separated list of `NMTOKEN`s.
* `Name`: Represents an XML name (must start with a letter or underscore, followed by letters, digits, periods, hyphens, or underscores).
* `NCName`: Represents a non-colonized name (like `Name` but cannot contain a colon).
* `ID`: Represents a unique identifier within an XML document.
* `IDREF`: Represents a reference to an `ID` value in the same document.
* `IDREFS`: Represents a whitespace-separated list of `IDREF` values.
* `ENTITY`: Represents a reference to an unparsed entity declared in a DTD (less common in XML Schema).
* `ENTITIES`: Represents a whitespace-separated list of `ENTITY` values (less common in XML Schema).

**Derived from `decimal`:**

* `integer`: Represents whole numbers (no fractional part).
* `nonPositiveInteger`: Represents integers less than or equal to 0.
* `negativeInteger`: Represents integers strictly less than 0.
* `long`: Represents 64-bit signed integers.
* `int`: Represents 32-bit signed integers.
* `short`: Represents 16-bit signed integers.
* `byte`: Represents 8-bit signed integers.
* `nonNegativeInteger`: Represents integers greater than or equal to 0.
* `unsignedLong`: Represents 64-bit unsigned integers.
* `unsignedInt`: Represents 32-bit unsigned integers.
* `unsignedShort`: Represents 16-bit unsigned integers.
* `unsignedByte`: Represents 8-bit unsigned integers.
* `positiveInteger`: Represents integers strictly greater than 0.

**Other Derived Types:**

* `dateTimeStamp` (in XML Schema 1.1): Similar to `dateTime` but also includes timezone information.
* `yearMonthDuration` (in XML Schema 1.1): Represents a duration in years and months.
* `dayTimeDuration` (in XML Schema 1.1): Represents a duration in days, hours, minutes, and seconds.
* `precisionDecimal` (in XML Schema 1.1): Represents decimal numbers with preserved precision.

**User-Defined Data Types:**

In addition to the built-in types, XML Schema allows you to define your own simple and complex data types using mechanisms like:

* **Restriction:** Creating a new type by limiting the range or format of an existing type (either built-in or user-defined).
* **List:** Defining a type whose values are sequences of values from another simple type.
* **Union:** Defining a type whose values can be drawn from the value spaces of two or more other simple types.

When defining elements and attributes in an XML Schema, you use the `type` attribute to specify which data type the content should adhere to. This ensures data validity and facilitates data processing.

For example:

```xml
<xs:element name="age" type="xs:positiveInteger"/>
<xs:element name="name" type="xs:string"/>
<xs:attribute name="status" type="xs:token"/>
```

In this snippet, the `age` element is defined to hold a positive integer, the `name` element a string, and the `status` attribute a token (a normalized string with specific whitespace handling).

Understanding these data types is fundamental to creating effective and well-defined XML Schemas. You can find the complete details and formal definitions in the W3C XML Schema Part 2: Datatypes specification.
