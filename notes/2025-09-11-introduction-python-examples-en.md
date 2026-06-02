---
audio: false
date: 2025-09-11
generated: true
image: false
lang: en
layout: post
model: google/gemini-2.5-flash
title: Introduction to Python Code Examples
translated: false
type: note
---

Okay, "some Python code" can mean a lot of things! Python is incredibly versatile. I'll give you a few common examples, from very basic to slightly more involved, covering different concepts.

---

### 1. Hello World (The Classic Start)

This is the simplest possible Python program.

```python
# This is a comment. Comments are ignored by Python.
print("Hello, World!")
```

**Explanation:**

* `print()` is a built-in function that outputs the given argument to the console.
* `"Hello, World!"` is a string (text).

---

### 2. Variables, Basic Arithmetic, and User Input

This code demonstrates how to store data in variables, perform simple math, and get input from the user.

```python
# Variables to store data
name = input("What is your name? ") # Get input from the user
age_str = input("How old are you? ")

# Convert age from string to integer for calculations
age = int(age_str)

# Basic arithmetic
year_of_birth = 2023 - age # Assuming current year is 2023 for simplicity
# You could also use: import datetime; year_of_birth = datetime.date.today().year - age

# Print formatted output using an f-string (formatted string literal)
print(f"Hello, {name}! You are {age} years old.")
print(f"You were likely born in {year_of_birth}.")

# A simple conditional check
if age < 18:
    print("You are a minor.")
else:
    print("You are an adult.")
```

**Explanation:**

* `input()`: Prompts the user for text input and returns it as a string.
* `name`, `age_str`, `age`, `year_of_birth`: These are variables storing different types of data (string, integer).
* `int()`: Converts a string to an integer. This is necessary because `input()` always returns a string, and you can't do math directly with strings.
* `f-strings`: A convenient way to embed expressions inside string literals. Notice the `f` before the opening quote.
* `if/else`: Control flow statements that execute different blocks of code based on a condition.

---

### 3. Lists and Loops

Lists are ordered collections of items. Loops are used to repeat a block of code multiple times.

```python
# A list of fruits
fruits = ["apple", "banana", "cherry", "date"]

print("\nMy favorite fruits:")

# Loop through the list using a 'for' loop
for fruit in fruits:
    print(f"- {fruit.capitalize()}") # .capitalize() makes the first letter uppercase

# Accessing elements by index (lists are zero-indexed)
print(f"\nThe first fruit is: {fruits[0]}")
print(f"The last fruit is: {fruits[-1]}") # Negative index accesses from the end

# Add an element
fruits.append("elderberry")
print(f"Updated list: {fruits}")

# Remove an element
fruits.remove("banana")
print(f"List after removing banana: {fruits}")

# Loop using 'range' to get indices
print("\nFruits with their indices:")
for i in range(len(fruits)): # len() gives the number of items in the list
    print(f"Index {i}: {fruits[i]}")
```

**Explanation:**

* `[]`: Used to define a list.
* `for ... in ...`: A `for` loop that iterates over each item in a sequence (like a list).
* `fruit.capitalize()`: A string method that returns a copy of the string with its first character capitalized.
* `fruits[0]`: Accesses the first element (index 0).
* `fruits[-1]`: Accesses the last element.
* `list.append()`: Adds an item to the end of the list.
* `list.remove()`: Removes the first occurrence of a specified item.
* `range(len(fruits))`: Generates a sequence of numbers from 0 up to (but not including) the length of the list, useful for accessing elements by their index.

---

### 4. Functions

Functions are blocks of reusable code that perform a specific task.

```python
# Define a function that takes arguments
def greet_person(name, age):
    """
    This function greets a person and tells them their age.
    It's a good practice to include a docstring like this.
    """
    return f"Hello, {name}! You are {age} years old."

# Call the function
message1 = greet_person("Alice", 30)
print(message1)

# Call it again with different arguments
message2 = greet_person("Bob", 25)
print(message2)

# Define a function with a default parameter
def calculate_area(length, width=10):
    """Calculates the area of a rectangle."""
    return length * width

print(f"\nArea of a 5x10 rectangle: {calculate_area(5)}") # Uses default width
print(f"Area of a 5x7 rectangle: {calculate_area(5, 7)}") # Overrides default width
```

**Explanation:**

* `def`: Keyword to define a function.
* `greet_person(name, age)`: Function name and its parameters (inputs).
* `return`: Sends a value back from the function.
* Docstrings (`"""Docstring goes here"""`): Explain what the function does. Good for documentation.
* `calculate_area(length, width=10)`: Shows a default parameter. If `width` is not provided when calling the function, it defaults to 10.

---

### 5. Dictionaries

Dictionaries store data in key-value pairs. They are unordered (in older Python versions, ordered in Python 3.7+).

```python
# A dictionary representing a person
person = {
    "first_name": "Charlie",
    "last_name": "Smith",
    "age": 40,
    "city": "London",
    "occupations": ["Engineer", "Teacher"] # A list can be a value
}

print("\nPerson's details:")

# Accessing values by key
print(f"Name: {person['first_name']} {person['last_name']}")
print(f"Lives in: {person.get('city', 'Unknown')}") # .get() is safer, returns None/default if key not found
print(f"First occupation: {person['occupations'][0]}")

# Modifying a value
person["age"] = 41
print(f"New age: {person['age']}")

# Adding a new key-value pair
person["email"] = "charlie.smith@example.com"
print(f"Email: {person['email']}")

# Looping through a dictionary
print("\nAll keys:")
for key in person: # Loops through keys by default
    print(key)

print("\nAll values:")
for value in person.values():
    print(value)

print("\nAll key-value pairs:")
for key, value in person.items():
    print(f"{key}: {value}")
```

**Explanation:**

* `{}`: Used to define a dictionary.
* `"key": value`: Key-value pairs. Keys must be unique and immutable (like strings or numbers). Values can be any data type.
* `person['key']`: Accesses the value associated with `key`.
* `person.get('key', 'default_value')`: A safer way to access, avoids `KeyError` if the key doesn't exist, returning `default_value` instead.
* `dict.values()`: Returns a view object that displays a list of all the values in the dictionary.
* `dict.items()`: Returns a view object that displays a list of a dictionary's key-value tuple pairs.

---

This is just scratching the surface, but these examples cover many fundamental Python concepts you'll use frequently!
