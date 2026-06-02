---
audio: false
generated: true
image: false
lang: en
layout: post
title: Java Bytecode
translated: false
type: note
---

```bash
javac Fibonacci.java

javap -c Fibonacci
```

```java
public class Fibonacci {
  public Fibonacci();
    Code:
       0: aload_0
       1: invokespecial #1                  // Method java/lang/Object."<init>":()V
       4: return

  public static int fibonacci(int);
    Code:
       0: iload_0
       1: iconst_1
       2: if_icmpgt     7
       5: iload_0
       6: ireturn
       7: iload_0
       8: iconst_1
       9: isub
      10: invokestatic  #7                  // Method fibonacci:(I)I
      13: iload_0
      14: iconst_2
      15: isub
      16: invokestatic  #7                  // Method fibonacci:(I)I
      19: iadd
      20: ireturn

  public static void main(java.lang.String[]);
    Code:
       0: bipush        10
       2: istore_1
       3: getstatic     #13                 // Field java/lang/System.out:Ljava/io/PrintStream;
       6: iload_1
       7: invokedynamic #19,  0             // InvokeDynamic #0:makeConcatWithConstants:(I)Ljava/lang/String;
      12: invokevirtual #23                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
      15: iconst_0
      16: istore_2
      17: iload_2
      18: iload_1
      19: if_icmpge     43
      22: getstatic     #13                 // Field java/lang/System.out:Ljava/io/PrintStream;
      25: iload_2
      26: invokestatic  #7                  // Method fibonacci:(I)I
      29: invokedynamic #29,  0             // InvokeDynamic #1:makeConcatWithConstants:(I)Ljava/lang/String;
      34: invokevirtual #30                 // Method java/io/PrintStream.print:(Ljava/lang/String;)V
      37: iinc          2, 1
      40: goto          17
      43: getstatic     #13                 // Field java/lang/System.out:Ljava/io/PrintStream;
      46: invokevirtual #33                 // Method java/io/PrintStream.println:()V
      49: return
}
```
