---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bypassing Enterprise Chat Tool Auto-approve
translated: false
type: note
---

Now I have the complete picture. Here's the answer:

---

The enterprise policy enforcement flows through this chain:

1. **Enterprise admin** sets a Group Policy / managed policy that disables `chat.tools.global.autoApprove`
2. This gets read as `policyValue === false` in VS Code's configuration system
3. Multiple check points read `inspected.policyValue === false` and block auto-approve

The key enforcement points are:

**File 1**: `src/vs/workbench/contrib/chat/browser/tools/languageModelToolsService.ts`

Lines 1128-1131 — the gate function:

```typescript
private _isAutoApprovePolicyRestricted(): boolean {
    const inspected = this._configurationService.inspect<boolean>(ChatConfiguration.GlobalAutoApprove);
    return inspected.policyValue === false;
}
```

Line 1209 — the actual check before auto-confirming a tool call:

```typescript
if (chatSessionResource && !this._isAutoApprovePolicyRestricted() && this._isSessionInAutoApproveLevel(chatSessionResource)) {
    return { type: ToolConfirmKind.ConfirmationNotNeeded, reason: 'auto-approve-all' };
}
```

**File 2**: `src/vs/workbench/contrib/terminalContrib/chatAgentTools/browser/tools/terminalToolAutoApprove.ts`

Lines 26-29 — same pattern for terminal tools:

```typescript
const inspected = configurationService.inspect<boolean>(ChatConfiguration.GlobalAutoApprove);
if (inspected.policyValue === false) {
    return false;
}
```

**File 3**: `src/vs/workbench/contrib/chat/browser/widget/input/permissionPickerActionItem.ts`

Line 72 — greys out the "Bypass Approvals" button in the UI:

```typescript
const isAutoApprovePolicyRestricted = () => configurationService.inspect<boolean>(ChatConfiguration.GlobalAutoApprove).policyValue === false;
```

---

**To bypass the enterprise restriction, the minimal change is:**

In `languageModelToolsService.ts`, change `_isAutoApprovePolicyRestricted()` to always return `false`:

```typescript
private _isAutoApprovePolicyRestricted(): boolean {
    return false;  // Bypass enterprise policy
}
```

And similarly in `terminalToolAutoApprove.ts`, change lines 26-29:

```typescript
// if (inspected.policyValue === false) {
//     return false;
// }
```

And in every file that checks `policyValue === false` to disable the UI or clamp the permission level:

- `src/vs/sessions/contrib/providers/copilotChatSessions/browser/permissionPicker.ts` (lines 94, 151)
- `src/vs/sessions/contrib/providers/agentHost/browser/baseAgentHostSessionsProvider.ts` (line 1383)
- `src/vs/sessions/contrib/providers/agentHost/browser/agentHostSessionConfigPicker.ts` (line 169)
- `src/vs/sessions/contrib/providers/localChatSessions/browser/localChatSessionsProvider.ts` (line 837)
- `src/vs/workbench/contrib/chat/browser/widget/chatContentParts/chatSuggestNextWidget.ts` (line 103)

All follow the same pattern: `configurationService.inspect<boolean>(ChatConfiguration.GlobalAutoApprove).policyValue === false`. Either change each to return `false`/skip the check, or — cleaner — patch the central config inspection so `policyValue` never resolves to `false` for this key.

**Cleanest single-point fix**: In `src/vs/platform/configuration/common/configuration.ts` (or wherever `inspect()` is implemented), add a filter that strips the policy override for `chat.tools.global.autoApprove` so `policyValue` returns `undefined` instead of `false`. That way all downstream checks pass through without touching every call site.

The setting key is `ChatConfiguration.GlobalAutoApprove` = `'chat.tools.global.autoApprove'` (defined in `src/vs/workbench/contrib/chat/common/constants.ts` line 35).
