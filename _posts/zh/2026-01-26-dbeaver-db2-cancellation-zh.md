---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: DBeaver DB2 后台任务取消
translated: true
type: note
---

Question: 在 DBeaver 中使用 DB2 时，有时在加载项目期间我需要取消后台任务，但尽管显示“loading item”，左侧面板（Navigator）仍会显示表且数据依然可以加载。

Answer:

这种行为在 DBeaver 配合 DB2（尤其是 DB2 LUW 或 z/OS）使用时非常常见。后台的 Metadata 加载或 Cache 操作可能看起来卡住或耗时极长，而主数据获取（例如打开表的 Data 标签页）通常独立运行并能正常显示结果。

### 为什么会发生这种情况
- 当你展开 Schemas/Tables 或打开对象时，DBeaver 会运行多个后台任务，例如：
  - 加载 Table/Column Metadata
  - 构建 Procedure/Argument Caches (`Load ArgumentsCache`)
  - 解析 Result set metadata
  - 加载 Schema 统计信息或 Table cache (`Load DB2TableCache`)
- 在 DB2 中，由于以下原因，这些任务可能会变慢：
  - 对象数量庞大
  - 远程连接或高延迟连接
  - DB2 特定的 JDBC driver 行为
  - 在服务器端执行开销较大的 Catalog 查询
- Navigator（左侧面板）或状态栏中显示的 "Loading item..." 消息通常来自这些辅助后台作业之一。
- 实际的表数据加载（默认执行 `SELECT * FROM table FETCH FIRST 200 ROWS ONLY`）是一个独立的操作，通常完成得更快。因此即使后台任务仍在运行或看似挂起，你也能看到数据。

### 你可以做什么
1. **安全地取消后台任务**
   - 进入 **Window → Show View → Background Tasks**（或点击右下角的进度指示器）。
   - 找到运行时间过长的任务（通常命名为 "Load DB2TableCache"、"Load schema statistics"、"Discover resultset metadata" 等）。
   - 右键点击 → **Cancel** 或使用红色方块/取消按钮。
   → 在大多数情况下，如果数据已经加载，这样做是安全的——它只是停止了额外的 Metadata 收集。

2. **预防或减少这些缓慢的后台任务**
   - 在 **Preferences → Connections → Metadata** 中，取消勾选或限制类似 "Load schema statistics on connection" 或 "Auto-discover metadata" 的选项。
   - 针对 DB2：如果 Driver properties 中有相关选项，尝试关闭 "Read table statistics" 或类似设置。
   - 在 **Preferences → Editors → Data Editor** 中增加 Fetch size 或更改 Result set 限制，以减轻初始加载压力（尽管这影响的是数据而非 Metadata）。
   - 使用 **Database → Metadata → Clear metadata cache**（有时有助于重置卡住的缓存）。

3. **如果问题持续发生的变通方法**
   - 第一次加载后，再次打开同一张表通常会更快（因为 Cache 已构建）。
   - 如果任务永远无法完成且阻塞了 UI：请重复取消操作或重启 DBeaver。
   - 考虑将 DBeaver 更新到最新版本——随时间推移，一些 DB2 Metadata 加载的 Bug 已得到改进（请查看 Release notes 中的 DB2 修复内容）。
   - 在 DBeaver 的 Driver Manager 中使用更新的或优化过的 DB2 JDBC driver（例如来自 IBM 的 db2jcc4.jar）。

这种“数据加载正常”与“加载项目/后台任务卡住”并存的情况是 DBeaver + DB2 组合中的已知模式，通常并非数据检索本身的 Bug。

References:

- [Background tasks taking a while or getting "stuck"](https://github.com/dbeaver/dbeaver/issues/38702)
- [very long "Load DB2TableCache" during query execution](https://github.com/dbeaver/dbeaver/issues/12425)
- [DB2 : infinite load schema statistics](https://github.com/dbeaver/dbeaver/issues/21216)
- [Background Tasks documentation](https://dbeaver.com/docs/dbeaver/Background-Tasks)
