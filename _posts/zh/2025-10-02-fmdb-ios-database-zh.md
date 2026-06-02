---
audio: false
generated: true
image: false
lang: zh
layout: post
model: deepseek/deepseek-v3.2-exp
title: iOS数据库操作之FMDB
translated: true
type: note
---

FMDB 是一个基于 SQLite 的 Objective-C 封装库，为 iOS 和 macOS 开发者提供了更简洁直观的数据库操作接口。

## 什么是 FMDB？

FMDB 为 SQLite 提供了更清晰、面向对象的接口，具备以下特性：

- 自动连接管理
- 错误处理机制
- 线程安全支持
- 常用操作的便捷方法

## 安装方式

### 使用 CocoaPods

在 Podfile 中添加：

```ruby
pod 'FMDB'
```

### 使用 Swift Package Manager

添加包依赖：`https://github.com/ccgus/fmdb`

## 基础用法

### 1. 导入与设置

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

### 2. 打开与关闭数据库

```swift
func openDatabase() -> Bool {
    guard database.open() else {
        print("无法打开数据库：\(database.lastErrorMessage())")
        return false
    }
    return true
}

func closeDatabase() {
    database.close()
}
```

### 3. 创建数据表

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
        print("数据表创建成功")
    } catch {
        print("创建数据表时出错：\(error.localizedDescription)")
    }

    closeDatabase()
}
```

### 4. 插入数据

```swift
func insertUser(name: String, email: String, age: Int) -> Bool {
    guard openDatabase() else { return false }

    let insertSQL = "INSERT INTO Users (name, email, age) VALUES (?, ?, ?)"

    do {
        try database.executeUpdate(insertSQL, values: [name, email, age])
        print("用户数据插入成功")
        closeDatabase()
        return true
    } catch {
        print("插入用户数据时出错：\(error.localizedDescription)")
        closeDatabase()
        return false
    }
}
```

### 5. 查询数据

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
        print("查询用户数据时出错：\(error.localizedDescription)")
    }

    closeDatabase()
    return users
}
```

### 6. 更新数据

```swift
func updateUserAge(userId: Int, newAge: Int) -> Bool {
    guard openDatabase() else { return false }

    let updateSQL = "UPDATE Users SET age = ? WHERE id = ?"

    do {
        try database.executeUpdate(updateSQL, values: [newAge, userId])
        print("用户数据更新成功")
        closeDatabase()
        return true
    } catch {
        print("更新用户数据时出错：\(error.localizedDescription)")
        closeDatabase()
        return false
    }
}
```

### 7. 删除数据

```swift
func deleteUser(userId: Int) -> Bool {
    guard openDatabase() else { return false }

    let deleteSQL = "DELETE FROM Users WHERE id = ?"

    do {
        try database.executeUpdate(deleteSQL, values: [userId])
        print("用户数据删除成功")
        closeDatabase()
        return true
    } catch {
        print("删除用户数据时出错：\(error.localizedDescription)")
        closeDatabase()
        return false
    }
}
```

## 使用 FMDatabaseQueue 实现线程安全

对于多线程应用，建议使用 `FMDatabaseQueue`：

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
                print("用户数据插入成功")
            } catch {
                print("插入用户数据时出错：\(error.localizedDescription)")
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
                print("查询用户数据时出错：\(error.localizedDescription)")
                DispatchQueue.main.async {
                    completion([])
                }
            }
        }
    }
}
```

## 事务处理

```swift
func performTransaction() {
    guard openDatabase() else { return }

    do {
        try database.beginTransaction()

        // 执行多个操作
        try database.executeUpdate("INSERT INTO Users (name, email, age) VALUES (?, ?, ?)",
                                 values: ["John", "john@example.com", 25])
        try database.executeUpdate("INSERT INTO Users (name, email, age) VALUES (?, ?, ?)",
                                 values: ["Jane", "jane@example.com", 30])

        try database.commit()
        print("事务执行成功")
    } catch {
        try? database.rollback()
        print("事务执行失败：\(error.localizedDescription)")
    }

    closeDatabase()
}
```

## 最佳实践

1. **始终记得关闭数据库**连接
2. **多线程应用使用 FMDatabaseQueue**
3. **使用参数化查询**防止 SQL 注入攻击
4. **妥善处理错误** - 检查返回值并捕获异常
5. **关联操作使用事务**保证数据一致性

## 数据模型示例

```swift
struct User {
    let id: Int
    let name: String
    let email: String
    let age: Int
}
```

FMDB 为 iOS 应用中的 SQLite 数据库操作提供了稳定高效的解决方案，在保持 SQLite 强大功能和灵活性的同时，让数据库操作变得更加易于管理。
