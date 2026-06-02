---
audio: false
generated: true
lang: en
layout: post
title: Using Scala’s Collection Library in Java
translated: false
type: note
---

To use the `scala.collection` package in Java, you can leverage the interoperability between Scala and Java since both languages compile to JVM bytecode. This allows Java code to call Scala classes, including those in the `scala.collection` package, provided the Scala library is accessible to your Java project. Below is a step-by-step guide to achieve this, complete with explanations and examples.

---

### **Step 1: Include the Scala Library in Your Java Project**
Since the `scala.collection` package is part of the Scala standard library, you need to include the Scala library in your Java project's classpath. This can be done by adding the Scala library dependency to your build tool:

- **Maven**:
  Add the following to your `pom.xml`:
  ```xml
  <dependency>
      <groupId>org.scala-lang</groupId>
      <artifactId>scala-library</artifactId>
      <version>2.13.12</version> <!-- Use the version that matches your needs -->
  </dependency>
  ```

- **Gradle**:
  Add this to your `build.gradle`:
  ```gradle
  implementation 'org.scala-lang:scala-library:2.13.12'
  ```

This ensures that Scala classes, including those in `scala.collection`, are available to your Java code.

---

### **Step 2: Import Scala Collection Classes**
Once the Scala library is in your classpath, you can import specific classes from the `scala.collection` package in your Java code. For example, to use Scala's immutable `List`, you would import:

```java
import scala.collection.immutable.List;
```

Other commonly used collections include:
- `scala.collection.immutable.Set`
- `scala.collection.immutable.Map`
- `scala.collection.mutable.Buffer`

Note that Scala collections come in both mutable and immutable variants, unlike Java’s collections, which are typically mutable unless wrapped (e.g., via `Collections.unmodifiableList`).

---

### **Step 3: Creating Scala Collections in Java**
Scala collections are typically created using companion objects, which provide factory methods like `apply`. However, since Java doesn’t support Scala’s syntax directly (e.g., `List(1, 2, 3)`), you need to work with these methods explicitly. Additionally, Scala’s `apply` method for collections like `List` expects a `Seq` as an argument when called from Java, due to how Scala’s varargs are compiled.

To bridge Java and Scala collections, use the conversion utilities provided by Scala, such as `scala.collection.JavaConverters` (for Scala 2.12 and earlier) or `scala.jdk.CollectionConverters` (for Scala 2.13 and later). Here’s how to create a Scala `List` from a Java `List`:

#### **Example: Creating a Scala List**
```java
import scala.collection.immutable.List;
import scala.collection.Seq;
import scala.jdk.CollectionConverters;
import java.util.Arrays;

public class ScalaCollectionExample {
    public static void main(String[] args) {
        // Create a Java List
        java.util.List<Integer> javaList = Arrays.asList(1, 2, 3);

        // Convert Java List to Scala Seq
        Seq<Integer> scalaSeq = CollectionConverters.asScala(javaList);

        // Create a Scala List using the companion object
        List<Integer> scalaList = List$.MODULE$.apply(scalaSeq);

        // Print the Scala List
        System.out.println(scalaList); // Output: List(1, 2, 3)
    }
}
```

- **`CollectionConverters.asScala`**: Converts a Java `List` to a Scala `Seq` (specifically a `mutable.Buffer` in Scala 2.13, which is a subtype of `Seq`).
- **`List$.MODULE$`**: Accesses the singleton instance of the `List` companion object in Scala, allowing you to call its `apply` method.
- **`apply(scalaSeq)`**: Creates a new immutable Scala `List` from the `Seq`.

---

### **Step 4: Using Scala Collections**
Once you have a Scala collection in Java, you can use its methods. However, be aware of differences between Scala and Java:
- **Immutability**: Many Scala collections (e.g., `scala.collection.immutable.List`) are immutable, meaning methods return new collections rather than modifying the original.
- **Type Erasure**: Both Scala and Java use type erasure, so you may need to cast results when retrieving elements.
- **Functional Methods**: Scala collections support functional operations like `map`, `filter`, etc., which you can use with Java 8+ lambdas.

#### **Example: Accessing Elements**
```java
// Get the first element
Integer head = (Integer) scalaList.head();
System.out.println("Head: " + head); // Output: Head: 1

// Get the tail (everything except the head)
List<Integer> tail = scalaList.tail();
System.out.println("Tail: " + tail); // Output: Tail: List(2, 3)
```

#### **Example: Mapping Over a Scala List**
Using a lambda to double each element:
```java
import scala.Function1;

Function1<Integer, Integer> doubler = x -> x * 2;
List<Integer> doubledList = scalaList.map(doubler);
System.out.println("Doubled: " + doubledList); // Output: Doubled: List(2, 4, 6)
```

Here, `Function1` is a Scala interface representing a function with one argument, which aligns with Java’s lambda syntax.

---

### **Key Considerations**
- **Type Safety**: Scala collections are parameterized, but method return types may appear as `Object` in Java due to type erasure. Cast as needed (e.g., `(Integer) scalaList.head()`).
- **Performance**: Crossing the Java-Scala boundary introduces some overhead, though it’s typically minor.
- **Paradigm Shift**: Scala collections emphasize immutability and functional programming, which may differ from Java’s imperative style. For example, you can’t “add” to an immutable `List`—you create a new one instead (e.g., using `:+` to append, which returns a new `List`).
- **Version Compatibility**: Ensure the Scala library version matches your needs. For Scala 2.13+, use `scala.jdk.CollectionConverters`; for 2.12 or earlier, use `scala.collection.JavaConverters`.

---

### **Summary**
You can use the `scala.collection` package in Java by:
1. Adding the Scala library to your project’s classpath (e.g., via Maven or Gradle).
2. Importing the desired Scala collection classes (e.g., `scala.collection.immutable.List`).
3. Creating Scala collections using companion objects (e.g., `List$.MODULE$.apply`) and converting Java collections to Scala `Seq` with `CollectionConverters`.
4. Manipulating the collections with Scala methods, using casts and lambdas as needed.

This approach allows you to leverage Scala’s powerful collection library in Java, such as its immutable data structures or functional operations, while working within Java’s ecosystem.
