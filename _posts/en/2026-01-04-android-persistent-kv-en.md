---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Android Persistent Key-Value Storage Class
translated: false
type: note
---

Question: Which class is used for simple key-value persistent storage in Android?

A) SQLiteDatabase  
B) FileOutputStream  
C) SharedPreferences  
D) ContentValues

Answer: 

The correct answer is **C) SharedPreferences**.

**Explanation**:

- **SharedPreferences** is the Android API specifically designed for storing and retrieving small amounts of primitive data as key-value pairs (e.g., booleans, floats, ints, longs, strings, and string sets). It is lightweight, easy to use, and persists data across app restarts and device reboots. Data is stored in an XML file in the app's private directory.

- **SQLiteDatabase** is used for structured relational database storage using SQL queries, suitable for larger or more complex data sets, not simple key-value pairs.

- **FileOutputStream** is a low-level API for writing raw bytes to files, requiring manual handling of file I/O and data serialization—not intended for simple key-value storage.

- **ContentValues** is a helper class that holds key-value pairs temporarily to insert or update rows in a SQLite database via ContentResolver or SQLiteDatabase; it does not provide persistent storage itself.

SharedPreferences is the standard and recommended choice for simple persistent key-value storage in Android applications.