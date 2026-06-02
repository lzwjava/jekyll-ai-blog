---
audio: false
generated: true
image: false
lang: en
layout: post
model: deepseek/deepseek-v3.2-exp
title: FMDB for iOS Database Operations
translated: false
type: note
---

FMDB is an Objective-C wrapper around SQLite that makes database operations easier and more intuitive for iOS and macOS developers.

## What is FMDB?

FMDB provides a cleaner, more object-oriented interface to SQLite with features like:
- Automatic connection management
- Error handling
- Thread safety
- Convenient methods for common operations

## Installation

### Using CocoaPods
Add to your Podfile:
```ruby
pod 'FMDB'
```

### Using Swift Package Manager
Add package dependency: `https://github.com/ccgus/fmdb`

## Basic Usage

### 1. Import and Setup
```swift
import FMDB

class DatabaseManager {
    private let database: FMDatabase

    init() {
        let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!
        let databaseURL = documentsPath.appendingPathComponent("mydatabase.sqlite")
        database = FMDatabase(url: databaseURL)
    }
}
```

### 2. Open and Close Database
```swift
func openDatabase() -> Bool {
    guard database.open() else {
        print("Unable to open database: \(database.lastErrorMessage())")
        return false
    }
    return true
}

func closeDatabase() {
    database.close()
}
```

### 3. Create Tables
```swift
func createTables() {
    guard openDatabase() else { return }

    let createTableSQL = """
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        age INTEGER
    );
    """

    do {
        try database.executeUpdate(createTableSQL, values: nil)
        print("Table created successfully")
    } catch {
        print("Error creating table: \(error.localizedDescription)")
    }

    closeDatabase()
}
```

### 4. Insert Data
```swift
func insertUser(name: String, email: String, age: Int) -> Bool {
    guard openDatabase() else { return false }

    let insertSQL = "INSERT INTO Users (name, email, age) VALUES (?, ?, ?)"

    do {
        try database.executeUpdate(insertSQL, values: [name, email, age])
        print("User inserted successfully")
        closeDatabase()
        return true
    } catch {
        print("Error inserting user: \(error.localizedDescription)")
        closeDatabase()
        return false
    }
}
```

### 5. Query Data
```swift
func getAllUsers() -> [User] {
    guard openDatabase() else { return [] }

    let querySQL = "SELECT * FROM Users"
    var users: [User] = []

    do {
        let resultSet = try database.executeQuery(querySQL, values: nil)

        while resultSet.next() {
            let id = resultSet.int(forColumn: "id")
            let name = resultSet.string(forColumn: "name") ?? ""
            let email = resultSet.string(forColumn: "email") ?? ""
            let age = resultSet.int(forColumn: "age")

            let user = User(id: Int(id), name: name, email: email, age: Int(age))
            users.append(user)
        }
    } catch {
        print("Error querying users: \(error.localizedDescription)")
    }

    closeDatabase()
    return users
}
```

### 6. Update Data
```swift
func updateUserAge(userId: Int, newAge: Int) -> Bool {
    guard openDatabase() else { return false }

    let updateSQL = "UPDATE Users SET age = ? WHERE id = ?"

    do {
        try database.executeUpdate(updateSQL, values: [newAge, userId])
        print("User updated successfully")
        closeDatabase()
        return true
    } catch {
        print("Error updating user: \(error.localizedDescription)")
        closeDatabase()
        return false
    }
}
```

### 7. Delete Data
```swift
func deleteUser(userId: Int) -> Bool {
    guard openDatabase() else { return false }

    let deleteSQL = "DELETE FROM Users WHERE id = ?"

    do {
        try database.executeUpdate(deleteSQL, values: [userId])
        print("User deleted successfully")
        closeDatabase()
        return true
    } catch {
        print("Error deleting user: \(error.localizedDescription)")
        closeDatabase()
        return false
    }
}
```

## Using FMDatabaseQueue for Thread Safety

For multi-threaded applications, use `FMDatabaseQueue`:

```swift
class ThreadSafeDatabaseManager {
    private let databaseQueue: FMDatabaseQueue

    init() {
        let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!
        let databaseURL = documentsPath.appendingPathComponent("mydatabase.sqlite")
        databaseQueue = FMDatabaseQueue(url: databaseURL)!
    }

    func insertUserThreadSafe(name: String, email: String, age: Int) {
        databaseQueue.inDatabase { db in
            let insertSQL = "INSERT INTO Users (name, email, age) VALUES (?, ?, ?)"
            do {
                try db.executeUpdate(insertSQL, values: [name, email, age])
                print("User inserted successfully")
            } catch {
                print("Error inserting user: \(error.localizedDescription)")
            }
        }
    }

    func getAllUsersThreadSafe(completion: @escaping ([User]) -> Void) {
        databaseQueue.inDatabase { db in
            var users: [User] = []
            let querySQL = "SELECT * FROM Users"

            do {
                let resultSet = try db.executeQuery(querySQL, values: nil)

                while resultSet.next() {
                    let id = resultSet.int(forColumn: "id")
                    let name = resultSet.string(forColumn: "name") ?? ""
                    let email = resultSet.string(forColumn: "email") ?? ""
                    let age = resultSet.int(forColumn: "age")

                    let user = User(id: Int(id), name: name, email: email, age: Int(age))
                    users.append(user)
                }

                DispatchQueue.main.async {
                    completion(users)
                }
            } catch {
                print("Error querying users: \(error.localizedDescription)")
                DispatchQueue.main.async {
                    completion([])
                }
            }
        }
    }
}
```

## Transactions

```swift
func performTransaction() {
    guard openDatabase() else { return }

    do {
        try database.beginTransaction()

        // Multiple operations
        try database.executeUpdate("INSERT INTO Users (name, email, age) VALUES (?, ?, ?)",
                                 values: ["John", "john@example.com", 25])
        try database.executeUpdate("INSERT INTO Users (name, email, age) VALUES (?, ?, ?)",
                                 values: ["Jane", "jane@example.com", 30])

        try database.commit()
        print("Transaction completed successfully")
    } catch {
        try? database.rollback()
        print("Transaction failed: \(error.localizedDescription)")
    }

    closeDatabase()
}
```

## Best Practices

1. **Always close the database** when you're done with it
2. **Use FMDatabaseQueue** for multi-threaded applications
3. **Use parameterized queries** to prevent SQL injection
4. **Handle errors properly** - check return values and catch exceptions
5. **Use transactions** for multiple related operations

## Data Model Example

```swift
struct User {
    let id: Int
    let name: String
    let email: String
    let age: Int
}
```

FMDB provides a robust and efficient way to work with SQLite databases in iOS applications, making database operations more manageable while maintaining the power and flexibility of SQLite.
