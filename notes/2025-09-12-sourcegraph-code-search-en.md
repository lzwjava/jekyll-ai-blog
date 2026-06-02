---
audio: false
date: 2025-09-12
generated: true
image: false
lang: en
layout: post
model: mistralai/mistral-medium-3.1
title: Sourcegraph Code Search Guide
translated: false
type: note
---

Sourcegraph is a powerful code search and navigation tool that allows developers to search across multiple repositories, understand code dependencies, and navigate large codebases efficiently. This guide covers **search syntax, best practices, and language-specific searches (Java & Python)**.

---

## **1. Basic Search Syntax**
Sourcegraph supports **literal, regex, and structural search** with filters.

### **1.1. Literal Search**
Search for exact text:
```
"def calculate_sum"
```

### **1.2. Regex Search**
Use `/.../` for regex:
```
/def \w+_sum\(/
```

### **1.3. Structural Search (Beta)**
Search for code patterns (e.g., function definitions):
```
type:func def calculate_sum
```

### **1.4. Filters**
Refine searches with filters:
- `repo:` – Search in a specific repo
  ```
  repo:github.com/elastic/elasticsearch "def search"
  ```
- `file:` – Search in specific files
  ```
  file:src/main/java "public class"
  ```
- `lang:` – Search in a specific language
  ```
  lang:python "def test_"
  ```
- `type:` – Search for symbols (functions, classes, etc.)
  ```
  type:func lang:go "func main"
  ```

---

## **2. Advanced Search Techniques**
### **2.1. Boolean Operators**
- `AND` (default): `def calculate AND sum`
- `OR`: `def calculate OR def sum`
- `NOT`: `def calculate NOT def subtract`

### **2.2. Wildcards**
- `*` – Matches any sequence of characters
  ```
  "def calculate_*"
  ```
- `?` – Matches a single character
  ```
  "def calculate_?"
  ```

### **2.3. Case Sensitivity**
- Case-insensitive by default
- Force case-sensitive with `case:yes`
  ```
  case:yes "Def Calculate"
  ```

### **2.4. Search in Comments**
Use `patternType:literal` to search in comments:
```
patternType:literal "// TODO:"
```

---

## **3. Searching Java Code**
### **3.1. Find Classes**
```
type:symbol lang:java "public class"
```
### **3.2. Find Methods**
```
type:func lang:java "public void"
```
### **3.3. Find Annotations**
```
lang:java "@Override"
```
### **3.4. Find Imports**
```
lang:java "import org.springframework"
```
### **3.5. Find Exception Handling**
```
lang:java "try {" AND "catch (Exception"
```

---

## **4. Searching Python Code**
### **4.1. Find Functions**
```
type:func lang:python "def calculate"
```
### **4.2. Find Classes**
```
type:symbol lang:python "class Calculator"
```
### **4.3. Find Imports**
```
lang:python "import pandas"
```
### **4.4. Find Decorators**
```
lang:python "@app.route"
```
### **4.5. Find Docstrings**
```
lang:python '"""'
```

---

## **5. Best Practices**
1. **Use `lang:`** to narrow down results.
2. **Combine filters** (`repo:`, `file:`, `type:`) for precision.
3. **Use regex** for flexible pattern matching.
4. **Save searches** for frequent queries.
5. **Use `case:yes`** when needed.

---

## **6. Example Queries**

| **Goal** | **Query** |
|----------|-----------|
| Find all Java `main` methods | `lang:java "public static void main"` |
| Find Python test functions | `lang:python "def test_"` |
| Find TODO comments in Go | `lang:go "// TODO:"` |
| Find Spring Boot controllers | `lang:java "@RestController"` |
| Find all `if` statements in JS | `lang:javascript "if ("` |

---

## **7. Conclusion**
Sourcegraph’s search is **powerful and flexible**, supporting **literal, regex, and structural searches** across multiple languages. By mastering filters (`lang:`, `repo:`, `type:`), you can efficiently navigate large codebases.

### **Next Steps**
- Try **saved searches** for recurring queries.
- Explore **code intelligence** (hover tooltips, cross-repo navigation).
- Use **Sourcegraph extensions** (VS Code, JetBrains).

Would you like a deeper dive into any specific feature? 🚀
