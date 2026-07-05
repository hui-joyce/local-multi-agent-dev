## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "%s Found Build Products Layout: Flat via inspecting test bundle directory %{public}@ - Using runner %{public}@"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 57 (2 AI-authored, 55 auto-generated); comments: 7 (2 AI-authored, 5 auto-generated); across 5 function(s); verified persisted in .i64: 57 named variables, 5 comments.

## What this feature does

The update to `WorkflowKit` introduces a new "Smart Prompt" infrastructure designed to handle output content collection and authorization for Shortcuts actions. This feature allows the system to intercept workflow outputs, collect them into a structured format, and present a user-facing authorization dialog (e.g., "Allow “%1$@” to output %2$@?") before proceeding. Additionally, the update includes new support for device-specific triggers (`WFAppInFocusTrigger`, `WFArriveLocationTrigger`, etc.) and improved test runner capabilities for internal Apple testing.

## How is it implemented

The implementation centers on the `WFDialogTransformer` and `WFDatabase(SmartPrompts)` categories. The `presentAlertWithSmartPromptConfiguration:completionHandler:` method orchestrates the display of authorization requests, while `saveOutputActionSmartPromtDataForWorkflowReference:error:` handles the persistence of smart prompt data by injecting a specialized action into the workflow's action list.

### Decompiled: `-[WFDialogTransformer presentAlertWithSmartPromptConfiguration:completionHandler:]`
```c
__int64 __fastcall -[WFDialogTransformer presentAlertWithSmartPromptConfiguration:completionHandler:](void *a1)
{
  __int64 v2; // x21
  void *v3; // x19
  void *v4; // x0
  __int64 v5; // x23
  __int64 v6; // x0
  __int64 v7; // x0
  __int64 v8; // x0
  __int64 v9; // x0
  _QWORD v11[5]; // [xsp+8h] [xbp-58h] BYREF

  v2 = MEMORY[0x1C78C3BB0]();
  v3 = (void *)MEMORY[0x1C78C3B00]();
  v4 = objc_msgSend(
         v3,
         "authorizationDialogRequestWithAttribution:",
         MEMORY[0x1C78C3850](objc_msgSend(a1, "privacyAttribution")));
  v5 = MEMORY[0x1C78C3850](v4);
  v6 = MEMORY[0x1C78C39B0]();
  v7 = MEMORY[0x1C78C39F0](v6);
  v11[0] = off_1DD5D4ED8;
  v11[1] = 3221225472LL;
  v11[2] = __82__WFDialogTransformer_presentAlertWithSmartPromptConfiguration_completionHandler___block_invoke;
  v11[3] = &unk_1DD5D8E00;
  v11[4] = v2;
  MEMORY[0x1C78C3B30](v7);
  v8 = MEMORY[0x1C78C3A60](objc_msgSend(a1, "showDialogRequest:completionHandler:", v5, v11));
  v9 = MEMORY[0x1C78C39B0](v8);
  return MEMORY[0x1C78C3A00](v9);
}
```

### Decompiled: `-[WFDatabase(SmartPrompts) saveOutputActionSmartPromtDataForWorkflowReference:error:]`
```c
__int64 __fastcall -[WFDatabase(SmartPrompts) saveOutputActionSmartPromtDataForWorkflowReference:error:](
        __int64 a1,
        __int64 a2,
        __int64 a3,
        _QWORD *a4)
{
  void *v5; // x19
  __int64 v6; // x0
  void *v7; // x0
  void *v8; // x21
  __int64 v9; // x22
  void *v10; // x23
  void *v11; // x23
  void *v12; // x0
  void *v13; // x24
  void *v14; // x25
  void *v15; // x26
  void *v16; // x0
  __int64 v17; // x0
  __int64 v18; // x0
  __int64 v19; // x0
  __int64 v20; // x0
  __int64 v21; // x0
  __int64 v22; // x0
  __int64 v23; // x0
  __int64 v25; // [xsp+8h] [xbp-58h] BYREF

  v25 = 0;
  v5 = (void *)MEMORY[0x1C78C3850](objc_msgSend(off_1D8853AF0, "workflowWithReference:database:error:", a3, a1, &v25));
  v6 = MEMORY[0x1C78C3C00]();
  if ( a4 )
    *a4 = MEMORY[0x1C78C3A90](v6);
  v7 = objc_msgSend((id)MEMORY[0x1C78C3850](objc_msgSend(v5, "actions")), "lastObject");
  v8 = (void *)MEMORY[0x1C78C3850](v7);
  MEMORY[0x1C78C39F0]();
  v9 = MEMORY[0x1C78C3850](objc_msgSend(v8, "generateUUIDIfNecessaryWithUUIDProvider:", 0));
  v10 = (void *)MEMORY[0x1C78C37C0](off_1D88544B8);
  v11 = objc_msgSend(
          v10,
          "initWithOutputUUID:outputName:variableProvider:aggrandizements:",
          v9,
          MEMORY[0x1C78C3850](objc_msgSend(v8, "outputName")),
          v8,
          0);
  MEMORY[0x1C78C3A10]();
  v12 = objc_msgSend(
          (id)MEMORY[0x1C78C3850](objc_msgSend(off_1D8853B08, "sharedRegistry")),
          "createActionWithIdentifier:serializedParameters:",
          &stru_1DD64CEA0,
          0);
  v13 = (void *)MEMORY[0x1C78C3850](v12);
  MEMORY[0x1C78C3A20]();
  v14 = (void *)MEMORY[0x1C78C3850](objc_msgSend(v13, "inputParameter"));
  v15 = objc_msgSend((id)MEMORY[0x1C78C37C0](objc_msgSend(v14, "stateClass")), "initWithVariable:", v11);
  v16 = objc_msgSend(v13, "setParameterState:forKey:", v15, MEMORY[0x1C78C3850](objc_msgSend(v14, "key")));
  MEMORY[0x1C78C3A40](v16);
  objc_msgSend(v5, "addAction:", v13);
  v17 = MEMORY[0x1C78C3A30](objc_msgSend(v5, "save"));
  v18 = MEMORY[0x1C78C3A20](v17);
  v19 = MEMORY[0x1C78C3A10](v18);
  v20 = MEMORY[0x1C78C3A00](v19);
  v21 = MEMORY[0x1C78C39F0](v20);
  v22 = MEMORY[0x1C78C39E0](v21);
  v23 = MEMORY[0x1C78C39B0](v22);
  return MEMORY[0x1C78C39D0](v23);
}
```

## How to trigger this feature

The feature is triggered when a workflow executes an action that produces output requiring user authorization. The `WFDialogTransformer` intercepts the execution flow, generates an `authorizationDialogRequest`, and presents it to the user. The `saveOutputActionSmartPromtDataForWorkflowReference` method is likely called during the workflow configuration or saving phase to ensure the necessary smart prompt action is attached to the workflow.

## Vulnerability Assessment

The introduction of "Smart Prompts" and explicit authorization dialogs for workflow outputs is a significant security and privacy enhancement. By requiring user consent before a workflow can output sensitive data (e.g., to another app or service), the system mitigates potential data exfiltration risks. The removal of various `WFSystemEventObserver` and `WFCallStatusSystemEventProvider` components suggests a refactoring of how the system handles background events, likely to improve stability and reduce unnecessary background activity.

## Evidence

- **Strings**: `Allow “%1$@” to output %2$@?`, `saveOutputActionSmartPromtDataForWorkflowReference:error:`
- **Symbols**: `-[WFDialogTransformer presentAlertWithSmartPromptConfiguration:completionHandler:]`, `-[WFDatabase(SmartPrompts) saveOutputActionSmartPromtDataForWorkflowReference:error:]`
- **Binary Diff**: Significant changes in `__TEXT.__objc_methlist` and `__TEXT.__cstring` reflect the addition of the Smart Prompt infrastructure and the removal of legacy system event providers.

## AI Prioritisation Scoring System

- **static_analysis**
  - **Tier**: TIER_1
  - **Category**: security_privacy
  - **Reasoning**: The introduction of Smart Prompts and explicit authorization dialogs for workflow outputs is a critical privacy and security boundary change, directly impacting how Shortcuts handles user data.

