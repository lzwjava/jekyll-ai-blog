---
audio: false
generated: true
image: false
lang: en
layout: post
title: TelegramEngine Architectural Pattern Analysis
translated: false
type: note
---

Here's the extended analysis with actual code examples from the repo:

---

## 1. TelegramEngine Facade Pattern — Clean Layer Separation

The `TelegramEngine` class is the crown jewel of the architecture. It's a god-object-done-right — a single entry point that namespaces every domain into lazy-initialized sub-engines:

```swift
// submodules/TelegramCore/Sources/TelegramEngine/TelegramEngine.swift
public final class TelegramEngine {
    public let account: Account

    public init(account: Account) {
        self.account = account
    }

    public lazy var secureId: SecureId = { return SecureId(account: self.account) }()
    public lazy var peers: Peers = { return Peers(account: self.account) }()
    public lazy var messages: Messages = { return Messages(account: self.account) }()
    public lazy var resources: Resources = { return Resources(account: self.account) }()
    public lazy var data: EngineData = {
        return EngineData(accountPeerId: self.account.peerId, postbox: self.account.postbox)
    }()
    public lazy var preferences: Preferences = { return Preferences(account: self.account) }()
    // ... 15+ more domains
}
```

Each sub-engine is a **facade** that wraps `_internal_*` functions. The public API uses engine-level types (`EngineMessage`, `EnginePeer`, `EngineMediaResource`), while the internal implementations use raw Postbox types. This is the 45-wave refactor in action:

```swift
// submodules/TelegramCore/Sources/TelegramEngine/Messages/TelegramEngineMessages.swift
public extension TelegramEngine {
    final class Messages {
        private let account: Account

        // Facade: clean public signature uses Engine types
        public func downloadMessage(messageId: EngineMessage.Id) -> Signal<EngineMessage?, NoError> {
            return _internal_downloadMessage(
                accountPeerId: self.account.peerId,
                postbox: self.account.postbox,
                network: self.account.network,
                messageId: messageId
            )
            |> map { message -> EngineMessage? in
                return message.flatMap(EngineMessage.init)  // wrap raw -> Engine
            }
        }

        // Facade: delegates to internal, bridges types
        public func deleteMessagesInteractively(messageIds: [MessageId], type: InteractiveMessagesDeletionType) -> Signal<Void, NoError> {
            self.account.stateManager.messagesRemovedContext.addIsMessagesDeletedInteractively(
                ids: messageIds.map { id -> DeletedMessageId in
                    if id.namespace == Namespaces.Message.Cloud &&
                       (id.peerId.namespace == Namespaces.Peer.CloudUser ||
                        id.peerId.namespace == Namespaces.Peer.CloudGroup) {
                        return .global(id.id)
                    } else {
                        return .messageId(id)
                    }
                }
            )
            return _internal_deleteMessagesInteractively(account: self.account, messageIds: messageIds, type: type)
        }
    }
}
```

The pattern: public method → type-bridge → `_internal_*` function (Postbox-facing). Consumer modules never `import Postbox`.

---

## 2. EngineMediaResource — Wrapper Class with Escape Hatch

The `EngineMediaResource` wraps the raw `MediaResource` protocol but provides an explicit escape hatch (`_asResource()`) for when you need the raw type:

```swift
// submodules/TelegramCore/Sources/TelegramEngine/Resources/TelegramEngineResources.swift
public final class EngineMediaResource: Equatable {
    public struct Id: Equatable, Hashable {
        public var stringRepresentation: String
        public init(_ stringRepresentation: String) { self.stringRepresentation = stringRepresentation }
        public init(_ id: MediaResourceId) { self.stringRepresentation = id.stringRepresentation }
    }

    private let resource: MediaResource  // raw Postbox protocol

    public init(_ resource: MediaResource) { self.resource = resource }

    public func _asResource() -> MediaResource { return self.resource }  // escape hatch

    public var id: Id { return Id(self.resource.id) }

    public static func ==(lhs: EngineMediaResource, rhs: EngineMediaResource) -> Bool {
        return lhs.resource.isEqual(to: rhs.resource)
    }
}
```

The underscore-prefixed `_asResource()` signals "this breaks the abstraction, use deliberately." The naming convention is consistent across the codebase — `_internal_*` for Postbox-facing functions, `_as*` for unwraps.

---

## 3. EngineData — Type-Safe Reactive Data Subscription

This is the most sophisticated pattern in the codebase. It provides a type-safe, composable API for subscribing to database views without exposing Postbox internals:

```swift
// submodules/TelegramCore/Sources/TelegramEngine/Data/TelegramEngineData.swift
public protocol TelegramEngineDataItem {
    associatedtype Result
}

// Internal bridge protocol
protocol PostboxViewDataItem: TelegramEngineDataItem {
    var key: PostboxViewKey { get }
    func extract(view: PostboxView) -> Result
}

public extension TelegramEngine {
    final class EngineData {
        let accountPeerId: PeerId
        private let postbox: Postbox

        // Core: merge multiple view keys into one combined subscription
        private func _subscribe(items: [AnyPostboxViewDataItem]) -> Signal<[Any], NoError> {
            var keys = Set<PostboxViewKey>()
            for item in items {
                for key in item.keys(data: self) { keys.insert(key) }
            }
            return self.postbox.combinedView(keys: Array(keys))
            |> map { views -> [Any] in
                var results: [Any] = []
                for item in items {
                    results.append(item._extract(data: self, views: views.views))
                }
                return results
            }
        }

        // Type-safe overloads for 1, 2, 3, 4, 5 items with correct tuple types
        public func subscribe<T0: TelegramEngineDataItem>(_ t0: T0) -> Signal<T0.Result, NoError> {
            return self._subscribe(items: [t0 as! AnyPostboxViewDataItem])
            |> map { results -> T0.Result in results[0] as! T0.Result }
        }

        public func subscribe<T0, T1>(_ t0: T0, _ t1: T1) -> Signal<(T0.Result, T1.Result), NoError>
        public func subscribe<T0, T1, T2>(_ t0: T0, _ t1: T1, _ t2: T2) -> Signal<(T0.Result, T1.Result, T2.Result), NoError>
        // ... up to 5 items

        // One-shot variant
        public func get<T0: TelegramEngineDataItem>(_ t0: T0) -> Signal<T0.Result, NoError> {
            return self.subscribe(t0) |> take(1)
        }
    }
}
```

Usage in consumer code looks like this:
```swift
context.engine.data.subscribe(
    EngineData.Item.Peer(id: peerId),
    EngineData.Item.PeerPresence(id: peerId)
)
|> map { peer, presence -> ... in
    // fully typed, no Postbox imports needed
}
```

The `_subscribe` internal method uses type erasure (`[Any]`) to handle the heterogeneous collection, then the public overloads restore types via `as!` casts. This is Swift generics pushed to their limits — variadic generics (commented out with `repeat each T`) would make this perfect, but that's Swift 5.9+ territory.

---

## 4. Custom Reactive Framework — SSignalKit

Telegram doesn't use Combine or RxSwift. They built their own reactive framework from scratch with `pthread_mutex` for thread safety:

```swift
// submodules/SSignalKit/SwiftSignalKit/Source/Signal.swift
public final class Signal<T, E> {
    private let generator: (Subscriber<T, E>) -> Disposable

    public init(_ generator: @escaping(Subscriber<T, E>) -> Disposable) {
        self.generator = generator
    }

    public func start(next: ((T) -> Void)! = nil, error: ((E) -> Void)! = nil,
                      completed: (() -> Void)! = nil) -> Disposable {
        let subscriber = Subscriber<T, E>(next: next, error: error, completed: completed)
        let disposable = self.generator(subscriber)
        return SubscriberDisposable(subscriber: subscriber, disposable: disposable)
    }

    // Convenience constructors
    public static func single(_ value: T) -> Signal<T, E> { ... }
    public static func fail(_ error: E) -> Signal<T, E> { ... }
    public static func never() -> Signal<T, E> { ... }
}

// Custom pipe operator for functional composition
infix operator |> : PipeRight

public func |> <T, U>(value: T, function: ((T) -> U)) -> U {
    return function(value)
}

// Async bridge (iOS 13+)
@available(iOS 13.0, *)
public extension Signal where E == NoError {
    func get() async -> T {
        let disposable = MetaDisposable()
        return await withCheckedContinuation { continuation in
            disposable.set((self |> take(1)).startStandalone(next: { value in
                continuation.resume(returning: value)
            }))
        }
    }
}
```

The `|>` pipe operator is used pervasively — it turns signal chains into readable pipelines:
```swift
context.engine.data.subscribe(EngineData.Item.Peer(id: peerId))
|> map { peer -> String in peer.debugDisplayableName }
|> deliverOnMainQueue
```

The `SubscriberDisposable` uses `pthread_mutex` (not `NSLock` or `os_unfair_lock`) — this is deliberate. `pthread_mutex` is the most portable and has well-defined behavior across all Apple platforms. The weak reference to `subscriber` ensures cleanup even if the signal chain is abandoned.

---

## 5. ValueBox — Low-Level Storage Protocol

The storage layer is a custom key-value store protocol (backed by SQLite/sqlcipher) with explicit transaction control:

```swift
// submodules/Postbox/Sources/ValueBox.swift
public protocol ValueBox {
    func begin()
    func commit()
    func checkpoint()

    func range(_ table: ValueBoxTable, start: ValueBoxKey, end: ValueBoxKey,
               values: (ValueBoxKey, ReadBuffer) -> Bool, limit: Int)
    func filteredRange(_ table: ValueBoxTable, start: ValueBoxKey, end: ValueBoxKey,
                       values: (ValueBoxKey, ReadBuffer) -> ValueBoxFilterResult, limit: Int)
    func get(_ table: ValueBoxTable, key: ValueBoxKey) -> ReadBuffer?
    func set(_ table: ValueBoxTable, key: ValueBoxKey, value: MemoryBuffer)
    func remove(_ table: ValueBoxTable, key: ValueBoxKey, secure: Bool)
    func exists(_ table: ValueBoxTable, key: ValueBoxKey) -> Bool
    func count(_ table: ValueBoxTable, start: ValueBoxKey, end: ValueBoxKey) -> Int

    // Full-text search built in
    func fullTextSet(_ table: ValueBoxFullTextTable, collectionId: String,
                     itemId: String, contents: String, tags: String)
    func fullTextMatch(_ table: ValueBoxFullTextTable, collectionId: String?,
                       query: String, tags: String?, values: (String, String) -> Bool)

    // Encrypted export for account migration
    func exportEncrypted(to exportBasePath: String, encryptionParameters: ValueBoxEncryptionParameters)
}
```

Key design decisions:
- `ValueBoxKey` is a typed key (binary or int64) — no stringly-typed nonsense
- `ReadBuffer` returns raw pointers for zero-copy reads
- `MemoryBuffer` for writes — avoids Data allocation overhead
- `secure: Bool` on remove — wipes data from disk, not just marks deleted
- `ValueBoxFilterResult` has `.accept`, `.skip`, `.stop` — efficient range scanning with early termination
- Full-text search is a first-class citizen, not bolted on

---

## 6. Bazel Build System — Modular Dependency Graph

The BUILD file shows how 273 submodules are wired together:

```python
# Telegram/BUILD (excerpt)
load("@build_bazel_rules_swift//swift:swift.bzl", "swift_library")
load("@build_bazel_rules_apple//apple:ios.bzl", "ios_application", "ios_extension")

# Code generation for strings
genrule(
    name = "GeneratedPresentationStrings",
    srcs = [
        "//build-system:GenerateStrings/GenerateStrings.py",
        "Telegram-iOS/en.lproj/Localizable.strings",
    ],
    cmd = '''
        python3 $(location //build-system:GenerateStrings/GenerateStrings.py) \\
            --source=$(location Telegram-iOS/en.lproj/Localizable.strings) \\
            --outImplementation=$(location GeneratedPresentationStrings/Sources/PresentationStrings.m) \\
            --outHeader=$(location GeneratedPresentationStrings/PublicHeaders/PresentationStrings/PresentationStrings.h) \\
            --outData=$(location GeneratedPresentationStrings/Resources/PresentationStrings.data)
    ''',
)

# Localization as empty stubs for unused languages
[
    genrule(
        name = "Localizable_{}.strings".format(language),
        outs = ["{}.lproj/Localizable.strings".format(language)],
        cmd = "touch $(OUTS)",
    ) for language in empty_languages
]
```

The build system uses:
- `swift_library` for each submodule (fine-grained dependency tracking)
- `genrule` for code generation (strings, intents)
- `config_setting` for debug/release/extension toggles
- `bool_flag` for build-time feature flags (`disableExtensions`, `disableProvisioningProfiles`)
- Bazel caching (`--cacheDir ~/telegram-bazel-cache`) for incremental builds

---

## 7. ChatController — The 10,925-Line Monster

`ChatController.swift` is 10,925 lines / 624 KB. It imports 80+ modules. This is the main chat screen — the most complex view controller in the app:

```swift
// submodules/TelegramUI/Sources/ChatController.swift (imports excerpt)
import Foundation
import UIKit
import Postbox
import SwiftSignalKit
import Display
import AsyncDisplayKit
import TelegramCore
import SafariServices
import MobileCoreServices
import Intents
import LegacyComponents
import TelegramPresentationData
import TelegramUIPreferences
// ... 70+ more imports
```

The ChatMessageBubbleItemNode (7,565 lines) handles every message type through a composable content node system:

```swift
// submodules/TelegramUI/Components/Chat/ChatMessageBubbleItemNode/Sources/ChatMessageBubbleItemNode.swift
private struct BubbleItemAttributes {
    var index: Int?
    var isAttachment: Bool
    var neighborType: ChatMessageBubbleRelativePosition.NeighbourType
    var neighborSpacing: ChatMessageBubbleRelativePosition.NeighbourSpacing
}
```

Each message type (text, file, poll, game, invoice, map, contact, giveaway, gift, etc.) has its own `ChatMessage*BubbleContentNode` — 30+ specialized content nodes composed into the bubble. This is the strategy pattern at massive scale.

---

## 8. ValueBox Encryption — Security by Design

```swift
public struct ValueBoxEncryptionParameters {
    public struct Key {
        public let data: Data
        public init?(data: Data) {
            if data.count == 32 { self.data = data }  // 256-bit key
            else { return nil }
        }
    }
    public struct Salt {
        public let data: Data
        public init?(data: Data) {
            if data.count == 16 { self.data = data }  // 128-bit salt
            else { return nil }
        }
    }
    public let forceEncryptionIfNoSet: Bool  // encrypt even if not explicitly configured
}
```

The `forceEncryptionIfNoSet` flag means encryption is opt-out, not opt-in. The `exportEncrypted` method on `ValueBox` enables encrypted account export/migration — your database is never written to disk unencrypted.

---

## Summary of Architectural Patterns

| Pattern | Where | Why |
|---------|-------|-----|
| Facade + `_internal_*` | TelegramEngine | Isolate Postbox from consumers |
| Wrapper class + `_as*` escape | EngineMediaResource | Type safety with escape hatch |
| Type erasure + typed overloads | EngineData.subscribe | Heterogeneous collection with type recovery |
| Custom reactive framework | SSignalKit | No external dependencies, full control |
| `\|>` pipe operator | Everywhere | Functional composition without nesting |
| Protocol-based storage | ValueBox | Zero-copy reads, typed keys, FTS built-in |
| Encrypted-by-default | ValueBoxEncryptionParameters | Security as default, not option |
| Strategy pattern (30+ nodes) | ChatMessageBubbleContentNode | Every message type composable |
| Bazel modular build | 273 submodules | Fine-grained caching, parallel builds |

This is what happens when a team of IOI/ACM gold medalists designs an iOS app. The layers are clean, the abstractions are intentional, and the escape hatches are named with underscores so you know when you're breaking the rules.
