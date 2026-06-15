## What this feature does
The updated `AppPredictionInternal` framework introduces a new notification management and pruning system for "biome" notifications. The key addition is the `_purgeNotificationBiomeStreamsIfNeeded` method, which removes persisted text content from private notification streams. This functionality is tightly coupled with a global key `__kATXBiomeNotificationPurgeCompleteKey` used to signal completion. The feature also includes logic to prune notifications and suggestions based on hard limits when triggered via XPC activity, suggesting a mechanism to enforce storage or display constraints on notification data.

## How is it implemented
The implementation revolves around the `ATXNotificationAndSuggestionDatabase` class. The new method `_purgeNotificationBiomeStreamsIfNeeded` is the primary entry point for the new feature.

**Decompiled Pseudocode (Inferred from Symbol & String Context):**
Based on the symbol `__kATXBiomeNotificationPurgeCompleteKey` (address `0x2843cbb58`) and the associated string, the logic likely follows this pattern:

```c
// Inferred logic for the new symbol __kATXBiomeNotificationPurgeCompleteKey
// This symbol is likely a global key used for IPC or completion signaling.
const char *ATXBiomeNotificationPurgeCompleteKey = "ATXBiomeNotificationPurgeCompleteKey";

// The method _purgeNotificationBiomeStreamsIfNeeded likely:
// 1. Checks if a "biome" stream exists or needs purging.
// 2. Iterates through private notification streams.
// 3. Removes text content associated with "biome" notifications.
// 4. Sets the global key to a completion state (e.g., "purge complete").
void _purgeNotificationBiomeStreamsIfNeeded() {
    // Logic to identify "biome" notifications (likely by Bundle ID or specific tag)
    // Logic to remove text content from these notifications
    // Set global key to indicate purge is done
    // [Set global key to "ATXBiomeNotificationPurgeCompleteKey"]
}
```

**Call Chain & Data Flow:**
1.  **Entry Point:** The method `-[ATXNotificationAndSuggestionDatabase _purgeNotificationBiomeStreamsIfNeeded]` (address `0x22b747326`) is the main function.
2.  **String Reference:** This function references the string `"ATXNotificationAndSuggestionDatabase: Purging private notification streams to remove persisted text content"` (address `0x22b6b46c7`). This string is likely used for logging or user-facing messages about the purge action.
3.  **Pruning Logic:** The diff shows new block functions related to `pruneSuggestionsBasedOnHardLimitsWithXPCActivity:` and `pruneNotificationsBasedOnHardLimitsWithXPCActivity:`. These are called via `objc_msgSend` with the selector `pruneSuggestionsBasedOnHardLimitsWithXPCActivity:`.
    *   `pruneSuggestionsBasedOnHardLimitsWithXPCActivity:` (address `0x22b67303c` and others)
    *   `pruneNotificationsBasedOnHardLimitsWithXPCActivity:` (address `0x22b672c23` and others)
    *   These functions likely check for an `XPCActivity` argument to determine if the pruning should proceed.
4.  **Global Key:** The symbol `__kATXBiomeNotificationPurgeCompleteKey` (address `0x2843cbb58`) is a global variable. The new method likely modifies this key to signal that the purge operation has finished successfully, allowing other parts of the system (e.g., via XPC) to know the data is cleared.

**Data Flow Trace:**
*   **Trigger:** An external component (likely via XPC) calls `-[ATXNotificationAndSuggestionDatabase _purgeNotificationBiomeStreamsIfNeeded]`.
*   **Action:** The method executes, removing "biome" related text from notifications.
*   **Signal:** Upon completion, the method sets the global key `__kATXBiomeNotificationPurgeCompleteKey`.
*   **Related Pruning:** The new `prune...WithXPCActivity:` functions are also present, suggesting a broader cleanup mechanism that can be triggered remotely.

## Evidence
*   **New Symbol:** `-[ATXNotificationAndSuggestionDatabase _purgeNotificationBiomeStreamsIfNeeded]` (Address: `0x22b747326`). This is the core function for the new feature.
*   **New String:** `"ATXNotificationAndSuggestionDatabase: Purging private notification streams to remove persisted text content"` (Address: `0x22b6b46c7`). Confirms the action of purging text content.
*   **New Global Key:** `__kATXBiomeNotificationPurgeCompleteKey` (Address: `0x2843cbb58`). Used as a completion signal.
*   **New Block Functions:** Multiple new blocks related to `pruneSuggestionsBasedOnHardLimitsWithXPCActivity:` and `pruneNotificationsBasedOnHardLimitsWithXPCActivity:` indicate expanded pruning logic.
*   **Symbol Count Change:** Increased by 4 symbols (`77861` -> `77865`), consistent with the addition of the new method and related blocks.
*   **UUID Change:** The framework's UUID changed, indicating a significant internal revision.

## AI Prioritisation Scoring System

- **Feature Addition**
  - **Tier**: TIER_1
  - **Category**: Notification Management / Data Pruning
  - **Reasoning**: The diff introduces a new method for purging notification streams based on a specific 'biome' classification, coupled with a new global completion key and expanded XPC-based pruning logic. This represents a significant new feature for managing notification storage and privacy, likely related to a new AI-driven notification categorization system ('biome').

