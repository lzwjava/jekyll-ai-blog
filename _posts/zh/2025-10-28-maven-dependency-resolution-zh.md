---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Maven多模块依赖解析
translated: true
type: note
---

是的，确实如此——在 Maven 多模块项目中，当一个模块（例如 EAR 模块）依赖另一个模块（例如 WAR 模块）时，Maven 默认会从本地 `.m2/repository` 解析依赖，而不是直接从其他模块的 `target/` 目录获取。这是因为 Maven 将模块间依赖视为标准工件引用（如同外部库），因此被依赖的工件必须经过安装（或至少完成打包并能在构建反应堆中被发现）。

### 原因解析
- **本地仓库解析机制**：Maven 的依赖解析机制会优先在本地仓库查找工件。`target/` 目录仅在单个模块构建期间临时使用，对于跨模块引用，Maven 要求工件必须被“发布”（安装）到仓库。
- **反应堆构建的局限性**：如果在**父 POM 根目录**执行 `mvn package`（或 `mvn install`），Maven 的反应堆会按拓扑顺序自动构建模块，在构建会话期间直接从其他模块的新鲜 `target/` 输出中解析依赖。但若**独立构建**依赖模块（例如进入 `ear-module && mvn package`），则无法感知 WAR 模块的 `target/` 内容——除非 WAR 工件已存在于 `.m2` 仓库，否则构建将失败。

### 针对 WAR 到 EAR 打包的特殊说明
在 EAR 项目中：
- EAR 插件（`maven-ear-plugin`）要求将 WAR（及其他模块）作为已解析的工件纳入 EAR 归档（例如通过 EAR POM 中的 `<modules>` 配置）。
- 如果 WAR 模块未被安装，会出现“无法解析依赖”或 EAR 中模块缺失的错误。

**解决方案**：当独立构建时，通常需要先在被依赖模块上执行 `mvn install`（或在完整反应堆构建中执行 `mvn package`）。最佳实践如下：
1. **推荐方案：从父项目构建**：在项目根目录执行 `mvn clean install`。这会自动处理构建顺序并将所有工件安装到 `.m2`。
2. **分模块构建场景**：
   - 先执行 `cd war-module && mvn clean install`（将 WAR 包安装到 `.m2`）
   - 再执行 `cd ear-module && mvn clean package`（或 `install`——EAR 通常只需 `package`）
3. **避免直接引用 target**：不要通过 `<systemPath>` 或文件路径直接引用 `target/` 目录，这种方案非常脆弱且会绕过 Maven 的校验和与传递性检查。

此行为在近期 Maven 版本中（截至 2025 年的 3.9.x）保持一致。更多细节请参阅官方多模块指南：

[构建生命周期导论 - 多模块项目](https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html#multi-module)
[Maven EAR 插件文档](https://maven.apache.org/plugins/maven-ear-plugin/ear-mojo.html)
