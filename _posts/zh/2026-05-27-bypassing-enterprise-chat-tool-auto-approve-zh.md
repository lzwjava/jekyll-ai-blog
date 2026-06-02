---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 绕过企业聊天工具自动批准
translated: true
type: note
---

企业策略执行通过以下链条进行：

1. **企业管理员**设置了一个组策略/托管策略，禁用 `chat.tools.global.autoApprove`
2. 该策略在 VS Code 的配置系统中被读取为 `policyValue === false`
3. 多个检查点读取到 `inspected.policyValue === false` 并阻止自动批准

关键执行点如下：

**文件 1**：`src/vs/workbench/contrib/chat/browser/tools/languageModelToolsService.ts`

第1128-1131行 — 门控函数：
```typescript
private _isAutoApprovePolicyRestricted(): boolean {
    const inspected = this._configurationService.inspect<boolean>(ChatConfiguration.GlobalAutoApprove);
    return inspected.policyValue === false;
}
```

第1209行 — 自动确认工具调用前的实际检查：
```typescript
if (chatSessionResource && !this._isAutoApprovePolicyRestricted() && this._isSessionInAutoApproveLevel(chatSessionResource)) {
    return { type: ToolConfirmKind.ConfirmationNotNeeded, reason: 'auto-approve-all' };
}
```

**文件 2**：`src/vs/workbench/contrib/terminalContrib/chatAgentTools/browser/tools/terminalToolAutoApprove.ts`

第26-29行 — 终端工具的相同模式：
```typescript
const inspected = configurationService.inspect<boolean>(ChatConfiguration.GlobalAutoApprove);
if (inspected.policyValue === false) {
    return false;
}
```

**文件 3**：`src/vs/workbench/contrib/chat/browser/widget/input/permissionPickerActionItem.ts`

第72行 — 在UI中将“绕过批准”按钮置灰：
```typescript
const isAutoApprovePolicyRestricted = () => configurationService.inspect<boolean>(ChatConfiguration.GlobalAutoApprove).policyValue === false;
```

---

**要绕过企业限制，最小的改动是：**

在 `languageModelToolsService.ts` 中，将 `_isAutoApprovePolicyRestricted()` 改为始终返回 `false`：

```typescript
private _isAutoApprovePolicyRestricted(): boolean {
    return false;  // 绕过企业策略
}
```

同样在 `terminalToolAutoApprove.ts` 中，修改第26-29行：

```typescript
// if (inspected.policyValue === false) {
//     return false;
// }
```

并且在每个检查 `policyValue === false` 以禁用UI或限制权限级别的文件中进行修改：

- `src/vs/sessions/contrib/providers/copilotChatSessions/browser/permissionPicker.ts`（第94、151行）
- `src/vs/sessions/contrib/providers/agentHost/browser/baseAgentHostSessionsProvider.ts`（第1383行）
- `src/vs/sessions/contrib/providers/agentHost/browser/agentHostSessionConfigPicker.ts`（第169行）
- `src/vs/sessions/contrib/providers/localChatSessions/browser/localChatSessionsProvider.ts`（第837行）
- `src/vs/workbench/contrib/chat/browser/widget/chatContentParts/chatSuggestNextWidget.ts`（第103行）

所有这些都遵循相同模式：`configurationService.inspect<boolean>(ChatConfiguration.GlobalAutoApprove).policyValue === false`。要么逐个修改为返回 `false`/跳过检查，要么更干净的做法——修复中央配置检查，使得 `policyValue` 对于此键永远不会解析为 `false`。

**最干净的单点修复**：在 `src/vs/platform/configuration/common/configuration.ts`（或 `inspect()` 的实现位置）中，添加一个过滤器，剥离 `chat.tools.global.autoApprove` 的策略覆盖，使 `policyValue` 返回 `undefined` 而不是 `false`。这样所有下游检查都会自然通过，无需修改每个调用点。

设置键为 `ChatConfiguration.GlobalAutoApprove` = `'chat.tools.global.autoApprove'`（定义在 `src/vs/workbench/contrib/chat/common/constants.ts` 第35行）。
