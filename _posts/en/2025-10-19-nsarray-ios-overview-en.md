---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: NSArray Overview for iOS Development
translated: false
type: note
---

### What is NSArray?

`NSArray` is a class in Apple's Foundation framework, part of the iOS SDK (and macOS, etc.). It represents an immutable, ordered collection of objects, similar to an array in other languages. This means once you create an `NSArray`, you can't add, remove, or replace elements—you can only read from it. It's commonly used in Objective-C for iOS app development to store and manage lists of data, like user preferences, database query results, or UI elements.

Key features:
- **Immutable**: Fixed size and contents after creation (use `NSMutableArray` for mutable versions).
- **Type-safe for objects**: Stores pointers to Objective-C objects (e.g., `NSString`, `NSNumber`, custom classes). It doesn't support primitives directly—wrap them in `NSNumber` or similar.
- **Indexed access**: Elements are accessed by integer index (0-based).
- **Thread-safe**: Generally safe for concurrent reads, but not writes (since it's immutable).
- **Integration**: Works seamlessly with other Foundation classes like `NSDictionary`, `NSString`, and Cocoa Touch UI components.

In Swift, `NSArray` is bridged to `Array`, but if you're working in Objective-C (common for legacy iOS code), you'll use `NSArray` directly.

### How to Use NSArray in iOS

To use `NSArray` in an iOS project:
1. Import the Foundation framework (it's usually included by default in iOS apps).
   ```objc
   #import <Foundation/Foundation.h>
   ```

2. **Creating an NSArray**:
   - Literal syntax (iOS 6+): `@[object1, object2, ...]`
   - Init method: `[[NSArray alloc] initWithObjects:object1, object2, nil]`
   - From a C array: `initWithArray:copyItems:`

   Example:
   ```objc
   NSArray *fruits = @[@"apple", @"banana", @"cherry"];
   // Or:
   NSArray *numbers = [[NSArray alloc] initWithObjects:@1, @2, @3, nil];
   ```

3. **Accessing Elements**:
   - `objectAtIndex:` for getting an item.
   - `count` for length.
   - `firstObject` / `lastObject` for edges.
   - `containsObject:` to check existence.

   Example:
   ```objc
   NSString *firstFruit = [fruits objectAtIndex:0]; // "apple"
   NSUInteger count = [fruits count]; // 3
   BOOL hasOrange = [fruits containsObject:@"orange"]; // NO
   ```

4. **Iterating**:
   - Fast enumeration: `for (id obj in array) { ... }`
   - `enumerateObjectsUsingBlock:` for block-based iteration (iOS 4+).

   Example:
   ```objc
   for (NSString *fruit in fruits) {
       NSLog(@"Fruit: %@", fruit);
   }
   ```

5. **Common Operations**:
   - Sorting: `sortedArrayUsingSelector:` or `sortedArrayUsingComparator:`.
   - Filtering: `filteredArrayUsingPredicate:` (with NSPredicate).
   - Joining: `componentsJoinedByString:` for strings.
   - Writing to file: `writeToFile:atomically:`.

   Example (filtering):
   ```objc
   NSPredicate *predicate = [NSPredicate predicateWithFormat:@"length > 5"];
   NSArray *longFruits = [fruits filteredArrayUsingPredicate:predicate];
   // Results: @[@"banana", @"cherry"]
   ```

6. **In iOS Contexts**:
   - **Table Views**: Pass an `NSArray` to `UITableView`'s data source methods like `tableView:numberOfRowsInSection:` (via `count`) and `tableView:cellForRowAtIndexPath:` (via `objectAtIndex:`).
   - **User Defaults**: Store/retrieve with `NSUserDefaults`: `[defaults setObject:array forKey:@"savedItems"];`.
   - **JSON Handling**: Convert to/from `NSData` with `JSONObjectWithData:options:error:`.

For mutable needs (e.g., adding items dynamically), switch to `NSMutableArray`:
```objc
NSMutableArray *mutableFruits = [NSMutableArray arrayWithArray:fruits];
[mutableFruits addObject:@"date"];
```

### Tips
- Always check for `nil` or bounds to avoid crashes: Use `objectAtIndex:` with index validation.
- Performance: O(1) for access, O(n) for searches.
- Modern iOS: Consider Swift's `Array` for new projects—it's more type-safe.

[NSArray Documentation](https://developer.apple.com/documentation/foundation/nsarray)
[NSMutableArray Documentation](https://developer.apple.com/documentation/foundation/nsmutablearray)
