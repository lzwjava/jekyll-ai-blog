---
audio: false
generated: true
image: false
lang: en
layout: post
title: Java 8 InputStream to Byte Array
translated: false
type: note
---

Good catch 👍 — in **Java 8** `InputStream.readAllBytes()` does not exist (that was added in Java 9).
You need to read the request body manually into a `byte[]`.

Here are a few common ways:

---

### 1. Using `ByteArrayOutputStream` (most standard)

```java
public static byte[] toByteArray(InputStream input) throws IOException {
    ByteArrayOutputStream buffer = new ByteArrayOutputStream();
    byte[] data = new byte[1024];
    int nRead;
    while ((nRead = input.read(data, 0, data.length)) != -1) {
        buffer.write(data, 0, nRead);
    }
    buffer.flush();
    return buffer.toByteArray();
}
```

In your wrapper constructor:

```java
public CachedBodyHttpServletRequest(HttpServletRequest request) throws IOException {
    super(request);
    this.cachedBody = toByteArray(request.getInputStream());
}
```

---

### 2. Using Apache Commons IO (`IOUtils`)

If you already have **Apache Commons IO** on your classpath:

```java
import org.apache.commons.io.IOUtils;

public CachedBodyHttpServletRequest(HttpServletRequest request) throws IOException {
    super(request);
    this.cachedBody = IOUtils.toByteArray(request.getInputStream());
}
```

---

### 3. Using Guava (`ByteStreams`)

If you have Guava:

```java
import com.google.common.io.ByteStreams;

public CachedBodyHttpServletRequest(HttpServletRequest request) throws IOException {
    super(request);
    this.cachedBody = ByteStreams.toByteArray(request.getInputStream());
}
```

---

### Final touch for logging

```java
public String getBody() {
    return new String(this.cachedBody, StandardCharsets.UTF_8);
}
```

---

✅ So in Java 8, option **#1 with ByteArrayOutputStream** is the most portable.
Option **#2 or #3** is cleaner if you’re okay adding Commons IO or Guava.

---

Do you want me to refactor the full `CachedBodyHttpServletRequest` code into a **Java 8–ready version** (self-contained, no `readAllBytes()`)?
