---
audio: false
generated: true
lang: en
layout: post
title: Java Exceptions
translated: false
type: note
---

Here's an extensive list of Java exceptions, categorized into **Checked Exceptions, Unchecked Exceptions (Runtime), and Errors**.

---

## **1. Checked Exceptions (Must be handled or declared using `throws`)**

1. **IOException** – General I/O failure.
2. **FileNotFoundException** – File is missing or inaccessible.
3. **InterruptedException** – Thread interruption occurs.
4. **SQLException** – Issues related to database access.
5. **ParseException** – Error while parsing data formats.
6. **MalformedURLException** – Invalid URL format.
7. **ClassNotFoundException** – Class is not found at runtime.
8. **InstantiationException** – Cannot instantiate an abstract class or interface.
9. **IllegalAccessException** – Access to a class, method, or field is not allowed.
10. **NoSuchMethodException** – Method does not exist.
11. **NoSuchFieldException** – Field does not exist in the class.
12. **TimeoutException** – A blocking operation timed out.
13. **UnsupportedEncodingException** – Encoding is not supported.
14. **URISyntaxException** – Invalid URI syntax.
15. **NotBoundException** – Name not found in an RMI registry.
16. **AlreadyBoundException** – Name already bound in an RMI registry.
17. **CloneNotSupportedException** – Object does not implement `Cloneable`.
18. **DataFormatException** – Invalid format in compressed data.
19. **EOFException** – Unexpected end of file reached.
20. **NotSerializableException** – Object is not serializable.
21. **LineUnavailableException** – Audio line is unavailable.
22. **UnsupportedAudioFileException** – Unsupported audio file format.
23. **PrinterException** – Printing operation failure.
24. **ReflectiveOperationException** – General reflection error.
25. **ExecutionException** – Exception during concurrent task execution.
26. **ScriptException** – Issues with executing scripts.
27. **TransformerException** – XML transformation failure.
28. **XPathExpressionException** – Invalid XPath expression.
29. **SAXException** – Issues with XML parsing.
30. **JAXBException** – Issues with XML binding.
31. **MarshalException** – Error while marshalling XML data.
32. **UnmarshalException** – Error while unmarshalling XML data.
33. **DatatypeConfigurationException** – Invalid XML data type configuration.
34. **GSSException** – Issues with GSS security operations.
35. **KeyStoreException** – Problems with Java KeyStore.
36. **CertificateException** – Problems with certificate processing.
37. **InvalidKeyException** – Invalid key in cryptographic operations.
38. **NoSuchAlgorithmException** – Requested cryptographic algorithm is not available.
39. **NoSuchProviderException** – Requested security provider is not available.
40. **UnrecoverableKeyException** – Cannot recover a key from KeyStore.
41. **IllegalBlockSizeException** – Invalid block size for encryption.
42. **BadPaddingException** – Padding error in cryptography.

---

## **2. Unchecked Exceptions (Runtime Exceptions)**

43. **NullPointerException** – Accessing an object reference that is `null`.
44. **ArrayIndexOutOfBoundsException** – Accessing an invalid array index.
45. **StringIndexOutOfBoundsException** – Accessing an invalid string index.
46. **ArithmeticException** – Math errors like division by zero.
47. **NumberFormatException** – Converting an invalid string to a number.
48. **ClassCastException** – Invalid type casting.
49. **IllegalArgumentException** – Invalid argument passed to a method.
50. **IllegalStateException** – Method called at an invalid state.
51. **UnsupportedOperationException** – Method is not supported.
52. **ConcurrentModificationException** – Concurrent modification of a collection.
53. **NoSuchElementException** – Attempting to access a non-existent element in a collection.
54. **IllegalMonitorStateException** – Thread synchronization error.
55. **NegativeArraySizeException** – Creating an array with a negative size.
56. **StackOverflowError** – Infinite recursion leading to stack overflow.
57. **OutOfMemoryError** – JVM runs out of memory.
58. **SecurityException** – Security violation detected.
59. **MissingResourceException** – Resource bundle not found.
60. **EmptyStackException** – Attempting to access an element from an empty stack.
61. **TypeNotPresentException** – Type not found at runtime.
62. **EnumConstantNotPresentException** – Invalid enum constant.
63. **UncheckedIOException** – Unchecked version of `IOException`.
64. **DateTimeException** – Errors related to Java’s date-time API.
65. **InvalidClassException** – Issues with deserializing a class.
66. **IllegalCharsetNameException** – Invalid character set name.
67. **UnsupportedCharsetException** – Charset is not supported.
68. **ProviderNotFoundException** – Required service provider is missing.
69. **PatternSyntaxException** – Invalid regular expression syntax.
70. **InvalidPathException** – Invalid file path.
71. **ReadOnlyBufferException** – Attempting to modify a read-only buffer.
72. **BufferUnderflowException** – Buffer underflow occurs.
73. **BufferOverflowException** – Buffer overflow occurs.
74. **FileSystemAlreadyExistsException** – File system already exists.
75. **FileSystemNotFoundException** – File system is not found.
76. **ClosedWatchServiceException** – Watch service is closed.
77. **UncheckedExecutionException** – Issues in concurrent task execution.

---

## **3. Errors (Serious issues that should not be caught)**

78. **StackOverflowError** – Too many recursive method calls.
79. **OutOfMemoryError** – JVM runs out of memory.
80. **VirtualMachineError** – Critical JVM error.
81. **InternalError** – Unexpected internal JVM error.
82. **UnknownError** – Unknown critical error.
83. **AssertionError** – Assertion failed using `assert`.
84. **NoClassDefFoundError** – Class definition is missing at runtime.
85. **IncompatibleClassChangeError** – Incompatible changes to a class.
86. **AbstractMethodError** – Abstract method is not implemented.
87. **InstantiationError** – Instance creation failure.
88. **IllegalAccessError** – Illegal access to a class or method.
89. **NoSuchMethodError** – Method is not found.
90. **NoSuchFieldError** – Field is not found.
91. **ClassFormatError** – Invalid class format.
92. **UnsupportedClassVersionError** – Java class compiled with an unsupported version.
93. **AnnotationFormatError** – Issues with Java annotations.
94. **ExceptionInInitializerError** – Exception in a static initializer block.
95. **ThreadDeath** – Thread forcibly terminated.
96. **ServiceConfigurationError** – Service provider configuration issue.
97. **BootstrapMethodError** – Error in dynamic language support.
98. **VerifierError** – Bytecode verification failure.
99. **FactoryConfigurationError** – Error in XML factory configuration.

---

### **Conclusion**

This is a comprehensive list of Java exceptions and errors. If you need more details on any specific exception, let me know! 🚀
