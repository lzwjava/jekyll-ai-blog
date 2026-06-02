---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Telegram引擎架构模式分析
translated: true
type: note
---

以下是仓库中实际代码示例的扩展分析：

---

## 1. TelegramEngine 外观模式 — 清晰的层级分离

`TelegramEngine` 类是架构的核心。它是一个正确的上帝对象——单一的入口点，将每个领域通过懒初始化子引擎进行命名空间划分：

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
    // ... 15+ 个更多领域
}
```

每个子引擎都是一个**外观**，包裹了 `_internal_*` 函数。公共 API 使用引擎级类型（`EngineMessage`、`EnginePeer`、`EngineMediaResource`），而内部实现使用原始的 Postbox 类型。这就是 45 波重构的实际应用：

```swift
// submodules/TelegramCore/Sources/TelegramEngine/Messages/TelegramEngineMessages.swift
public extension TelegramEngine {
    final class Messages {
        private let account: Account

        // 外观：清晰的公共签名使用 Engine 类型
        public func downloadMessage(messageId: EngineMessage.Id) -> Signal<EngineMessage?, NoError> {
            return _internal_downloadMessage(
                accountPeerId: self.account.peerId,
                postbox: self.account.postbox,
                network: self.account.network,
                messageId: messageId
            )
            |> map { message -> EngineMessage? in
                return message.flatMap(EngineMessage.init)  // 包装原始 -> Engine
            }
        }

        // 外观：委托给内部，桥接类型
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

模式：公共方法 → 类型桥接 → `_internal_*` 函数（面向 Postbox）。消费者模块绝不 `import Postbox`。

---

## 2. EngineMediaResource — 带有逃生口的包装类

`EngineMediaResource` 包装了原始的 `MediaResource` 协议，但提供了显式的逃生口（`_asResource()`）供需要原始类型时使用：

```swift
// submodules/TelegramCore/Sources/TelegramEngine/Resources/TelegramEngineResources.swift
public final class EngineMediaResource: Equatable {
    public struct Id: Equatable, Hashable {
        public var stringRepresentation: String
        public init(_ stringRepresentation: String) { self.stringRepresentation = stringRepresentation }
        public init(_ id: MediaResourceId) { self.stringRepresentation = id.stringRepresentation }
    }

    private let resource: MediaResource  // 原始 Postbox 协议

    public init(_ resource: MediaResource) { self.resource = resource }

    public func _asResource() -> MediaResource { return self.resource }  // 逃生口

    public var id: Id { return Id(self.resource.id) }

    public static func ==(lhs: EngineMediaResource, rhs: EngineMediaResource) -> Bool {
        return lhs.resource.isEqual(to: rhs.resource)
    }
}
```

以下划线为前缀的 `_asResource()` 表示“这打破了抽象，请谨慎使用”。命名约定在整个代码库中保持一致——`_internal_*` 用于面向 Postbox 的函数，`_as*` 用于解包。

---

## 3. EngineData — 类型安全的响应式数据订阅

这是代码库中最复杂的模式。它提供了一个类型安全、可组合的 API，用于订阅数据库视图而不暴露 Postbox 内部细节：

```swift
// submodules/TelegramCore/Sources/TelegramEngine/Data/TelegramEngineData.swift
public protocol TelegramEngineDataItem {
    associatedtype Result
}

// 内部桥接协议
protocol PostboxViewDataItem: TelegramEngineDataItem {
    var key: PostboxViewKey { get }
    func extract(view: PostboxView) -> Result
}

public extension TelegramEngine {
    final class EngineData {
        let accountPeerId: PeerId
        private let postbox: Postbox

        // 核心：将多个视图键合并为一个组合订阅
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

        // 类型安全重载：1、2、3、4、5 个元素，使用正确的元组类型
        public func subscribe<T0: TelegramEngineDataItem>(_ t0: T0) -> Signal<T0.Result, NoError> {
            return self._subscribe(items: [t0 as! AnyPostboxViewDataItem])
            |> map { results -> T0.Result in results[0] as! T0.Result }
        }

        public func subscribe<T0, T1>(_ t0: T0, _ t1: T1) -> Signal<(T0.Result, T1.Result), NoError>
        public func subscribe<T0, T1, T2>(_ t0: T0, _ t1: T1, _ t2: T2) -> Signal<(T0.Result, T1.Result, T2.Result), NoError>
        // ... 最多 5 个元素

        // 一次性变体
        public func get<T0: TelegramEngineDataItem>(_ t0: T0) -> Signal<T0.Result, NoError> {
            return self.subscribe(t0) |> take(1)
        }
    }
}
```

消费者代码中的用法如下：

```swift
context.engine.data.subscribe(
    EngineData.Item.Peer(id: peerId),
    EngineData.Item.PeerPresence(id: peerId)
)
|> map { peer, presence -> ... in
    // 完全类型化，无需 Postbox 导入
}
```

内部的 `_subscribe` 方法使用类型擦除（`[Any]`）处理异构集合，然后公共重载通过 `as!` 强制转换恢复类型。这是 Swift 泛型的极限应用——可变泛型（使用 `repeat each T` 注释掉）会让它更完美，但这需要 Swift 5.9+。

---

## 4. 自定义响应式框架 — SSignalKit

Telegram 没有使用 Combine 或 RxSwift。他们从头构建了自己的响应式框架，并使用 `pthread_mutex` 保证线程安全：

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

    // 便捷构造器
    public static func single(_ value: T) -> Signal<T, E> { ... }
    public static func fail(_ error: E) -> Signal<T, E> { ... }
    public static func never() -> Signal<T, E> { ... }
}

// 自定义管道操作符，用于函数式组合
infix operator |> : PipeRight

public func |> <T, U>(value: T, function: ((T) -> U)) -> U {
    return function(value)
}

// 异步桥接（iOS 13+）
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

`|>` 管道操作符被广泛使用——它将信号链转变为可读的管道：

```swift
context.engine.data.subscribe(EngineData.Item.Peer(id: peerId))
|> map { peer -> String in peer.debugDisplayableName }
|> deliverOnMainQueue
```

`SubscriberDisposable` 使用 `pthread_mutex`（而不是 `NSLock` 或 `os_unfair_lock`）——这是有意为之。`pthread_mutex` 是最具可移植性的，并且在所有 Apple 平台上具有定义明确的行为。对 `subscriber` 的弱引用确保即使信号链被废弃也能进行清理。

---

## 5. ValueBox — 底层存储协议

存储层是一个自定义的键值存储协议（由 SQLite/sqlcipher 支持），具有显式的事务控制：

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

    // 内置全文搜索
    func fullTextSet(_ table: ValueBoxFullTextTable, collectionId: String,
                     itemId: String, contents: String, tags: String)
    func fullTextMatch(_ table: ValueBoxFullTextTable, collectionId: String?,
                       query: String, tags: String?, values: (String, String) -> Bool)

    // 用于账户迁移的加密导出
    func exportEncrypted(to exportBasePath: String, encryptionParameters: ValueBoxEncryptionParameters)
}
```

关键设计决策：

- `ValueBoxKey` 是类型化的键（二进制或 int64）——没有字符串类型的混乱
- `ReadBuffer` 返回原始指针以实现零拷贝读取
- `MemoryBuffer` 用于写入——避免 Data 分配开销
- `secure: Bool` 用于删除——从磁盘擦除数据，而不仅仅是标记删除
- `ValueBoxFilterResult` 具有 `.accept`、`.skip`、`.stop`——支持提前终止的高效范围扫描
- 全文搜索是一等公民，而非后来附加的功能

---

## 6. Bazel 构建系统 — 模块化依赖图

BUILD 文件展示了 273 个子模块如何连接在一起：

```python
# Telegram/BUILD（摘录）
load("@build_bazel_rules_swift//swift:swift.bzl", "swift_library")
load("@build_bazel_rules_apple//apple:ios.bzl", "ios_application", "ios_extension")

# 字符串代码生成
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

# 本地化：为未使用的语言提供空存根
[
    genrule(
        name = "Localizable_{}.strings".format(language),
        outs = ["{}.lproj/Localizable.strings".format(language)],
        cmd = "touch $(OUTS)",
    ) for language in empty_languages
]
```

构建系统使用：

- 每个子模块使用 `swift_library`（细粒度依赖跟踪）
- 使用 `genrule` 进行代码生成（字符串、意图）
- 使用 `config_setting` 切换调试/发布/扩展
- 使用 `bool_flag` 实现构建时功能开关（`disableExtensions`、`disableProvisioningProfiles`）
- Bazel 缓存（`--cacheDir ~/telegram-bazel-cache`）用于增量构建

---

## 7. ChatController — 10,925 行的庞然大物

`ChatController.swift` 有 10,925 行 / 624 KB。它导入了 80 多个模块。这是主要的聊天界面——应用程序中最复杂的视图控制器：

```swift
// submodules/TelegramUI/Sources/ChatController.swift（导入摘录）
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
// ... 70+ 更多导入
```

ChatMessageBubbleItemNode（7,565 行）通过一个可组合的内容节点系统处理所有消息类型：

```swift
// submodules/TelegramUI/Components/Chat/ChatMessageBubbleItemNode/Sources/ChatMessageBubbleItemNode.swift
private struct BubbleItemAttributes {
    var index: Int?
    var isAttachment: Bool
    var neighborType: ChatMessageBubbleRelativePosition.NeighbourType
    var neighborSpacing: ChatMessageBubbleRelativePosition.NeighbourSpacing
}
```

每种消息类型（文本、文件、投票、游戏、发票、地图、联系人、赠品、礼物等）都有自己的 `ChatMessage*BubbleContentNode`——30 多个专门的内容节点组合到气泡中。这是大规模应用的策略模式。

---

## 8. ValueBox 加密 — 安全设计

```swift
public struct ValueBoxEncryptionParameters {
    public struct Key {
        public let data: Data
        public init?(data: Data) {
            if data.count == 32 { self.data = data }  // 256 位密钥
            else { return nil }
        }
    }
    public struct Salt {
        public let data: Data
        public init?(data: Data) {
            if data.count == 16 { self.data = data }  // 128 位盐值
            else { return nil }
        }
    }
    public let forceEncryptionIfNoSet: Bool  // 即使未显式配置也进行加密
}
```

`forceEncryptionIfNoSet` 标志意味着加密是可选退出而非选择加入的。`ValueBox` 上的 `exportEncrypted` 方法支持加密的账户导出/迁移——你的数据库永远不会以未加密的形式写入磁盘。

---

## 架构模式总结

| 模式 | 位置 | 原因 |
|---------|-------|------|
| 外观 + `_internal_*` | TelegramEngine | 将 Postbox 与消费者隔离 |
| 包装类 + `_as*` 逃生口 | EngineMediaResource | 类型安全并提供逃生口 |
| 类型擦除 + 类型化重载 | EngineData.subscribe | 异构集合与类型恢复 |
| 自定义响应式框架 | SSignalKit | 无外部依赖，完全控制 |
| `\|>` 管道操作符 | 无处不在 | 函数式组合，避免嵌套 |
| 基于协议的存储 | ValueBox | 零拷贝读取、类型化键、内置全文搜索 |
| 默认加密 | ValueBoxEncryptionParameters | 安全是默认而非选项 |
| 策略模式（30+ 节点） | ChatMessageBubbleContentNode | 每种消息类型可组合 |
| Bazel 模块化构建 | 273 个子模块 | 细粒度缓存、并行构建 |

这就是当一支由 IOI/ACM 金牌得主组成的团队设计 iOS 应用程序时会发生的情况。层级清晰，抽象是有意的，逃生口用下划线命名，以便你知道何时在打破规则。
