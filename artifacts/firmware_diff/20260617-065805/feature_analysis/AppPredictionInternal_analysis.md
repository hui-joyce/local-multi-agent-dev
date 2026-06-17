## What this feature does
The `AppPredictionInternal` framework update introduces a new notification management and pruning mechanism for the "Biome" feature (likely a personalized content or notification stream). The core functionality involves:
1.  **Purging Biome Streams:** A new function `_purgeNotificationBiomeStreamsIfNeeded` was added to clear persisted text content from private notification streams associated with the Biome feature. This is explicitly documented by the string "ATXNotificationAndSuggestionDatabase: Purging private notification streams to remove persisted text content".
2.  **Pruning Logic:** Two new functions handle the actual pruning logic based on hard limits:
    *   `pruneSuggestionsBasedOnHardLimitsWithXPCActivity:`: Prunes suggestion notifications.
    *   `pruneNotificationsBasedOnHardLimitsWithXPCActivity:`: Prunes general notifications.
    Both functions utilize an `XPCActivity` context, suggesting they are triggered by or interact with an XPC (Inter-Process Communication) service, likely from a background daemon or a separate app component.
3.  **Notification Analysis & Management:** The framework retains existing functionality for analyzing notifications (`analyze`), retrieving notifications by bundle ID and timestamp (`allNotificationsFromBundleId:sinceTimestamp:`), fetching bundle IDs on the lock screen (`allBundleIdsOfNotificationsOnLockscreen`), and updating notifications from events (`updateNotificationFromEvent:`).
4.  **Data Management:** The `deleteAllData` function allows for the complete removal of local notification data, and `currentActiveSuggestions` tracks the active suggestions.
5.  **Lifecycle:** The `analyze` function appears to be the main entry point or orchestrator, likely checking conditions before invoking the purge or pruning logic.

## How is it implemented
The implementation revolves around the `ATXNotificationAndSuggestionDatabase` class. The flow appears to be:

1.  **Entry Point (`analyze`):** The `analyze` function (address `0x22b6733cd` / `0x22b679cc0` / `0x22b712b6c`) serves as the primary controller. It likely evaluates the state of the notification database.
2.  **Purge Trigger:** If conditions are met (e.g., storage limits, user preference, or a specific event), `analyze` calls `_purgeNotificationBiomeStreamsIfNeeded` (address `0x22b7dbf60`).
3.  **Purge Execution:** `_purgeNotificationBiomeStreamsIfNeeded` (address `0x22b747326`) iterates through the "Biome" notification streams and deletes the text content. It uses the key `__kATXBiomeNotificationPurgeCompleteKey` (address `0x2843cbb58`) to signal completion, possibly to an external process.
4.  **Pruning (Hard Limits):** The system also implements hard limits for notification storage.
    *   `pruneSuggestionsBasedOnHardLimitsWithXPCActivity:` (address `0x22b67303c`) removes old suggestions.
    *   `pruneNotificationsBasedOnHardLimitsWithXPCActivity:` (address `0x22b672c23`) removes old general notifications.
    *   These functions are dispatched via `objc_msgSend` and take an `XPCActivity` object as an argument, indicating they are called by an external IPC client.
5.  **Data Retrieval:**
    *   `allNotificationsFromBundleId:sinceTimestamp:` (address `0x22b7e14c0`) fetches notifications for a specific app (bundle ID) since a specific time.
    *   `allBundleIdsOfNotificationsOnLockscreen` (address `0x22b672b20`) retrieves which apps have notifications currently displayed on the lock screen.
6.  **Variable Renaming & Flow:**
    *   Local variables within the decompiled functions (e.g., `v4`, `v5`) represent the `ATXNotificationAndSuggestionDatabase` instance, the `XPCActivity` object, and specific notification objects.
    *   The `analyze` function likely checks if the total number of notifications exceeds a threshold or if a specific "purge" flag is set.
    *   The `deleteAllData` function (address `0x22b761d17`) performs a full wipe of the local database, resetting counters and clearing all stored items.

**Decompile Snippet (Simulated based on context):**
```c
// ATXNotificationAndSuggestionDatabase::analyze
void ATXNotificationAndSuggestionDatabase::analyze() {
    // Check if we need to purge Biome streams
    if (shouldPurgeBiomeStreams()) {
        _purgeNotificationBiomeStreamsIfNeeded();
    }
    
    // Check if we need to prune based on hard limits
    // This part is likely triggered by an XPC call
    if (isHardLimitExceeded()) {
        pruneSuggestionsBasedOnHardLimitsWithXPCActivity(xpcActivity);
        pruneNotificationsBasedOnHardLimitsWithXPCActivity(xpcActivity);
    }
    
    // Update local state based on new events
    updateNotificationFromEvent(event);
}

// ATXNotificationAndSuggestionDatabase::_purgeNotificationBiomeStreamsIfNeeded
void ATXNotificationAndSuggestionDatabase::_purgeNotificationBiomeStreamsIfNeeded() {
    // Iterate through streams tagged as "Biome"
    for (NotificationStream *stream : biomeStreams) {
        // Remove text content from the stream
        stream->textContent = nil;
        stream->totalCount = 0;
    }
    
    // Signal completion to the XPC client
    [[NSNotificationCenter defaultCenter] postNotificationName:@"__kATXBiomeNotificationPurgeCompleteKey" object:nil];
}

// ATXNotificationAndSuggestionDatabase::pruneNotificationsBasedOnHardLimitsWithXPCActivity
void ATXNotificationAndSuggestionDatabase::pruneNotificationsBasedOnHardLimitsWithXPCActivity(XPCActivity *activity) {
    // Calculate total size of notifications
    long long totalSize = calculateTotalNotificationSize();
    
    if (totalSize > HARD_LIMIT_BYTES) {
        // Determine which notifications to remove (oldest or least important)
        NSArray *notificationsToDelete = [self getOldestNotificationsToPrune:count];
        
        for (Notification *notif in notificationsToDelete) {
            [self deleteNotification:notif];
        }
        
        // Send response back to XPC client
        [activity sendResponse:@{@"prunedCount": @(notificationsToDelete.count)}];
    }
}
```

## How to trigger this feature
Based on the function names and the presence of `XPCActivity` parameters, this feature is triggered by external requests via Inter-Process Communication (XPC).
1.  **XPC Call:** An external process (likely a system daemon or a specific app like "Biome") sends an XPC request to the `ATXNotificationAndSuggestionDatabase` class.
2.  **Selector:** The specific selectors that trigger the new functionality are:
    *   `purgeNotificationBiomeStreamsIfNeeded`
    *   `pruneSuggestionsBasedOnHardLimitsWithXPCActivity`
    *   `pruneNotificationsBasedOnHardLimitsWithXPCActivity`
3.  **Internal State:** The `analyze` method might also trigger the purge internally if local conditions (e.g., storage full) are met, but the new functions are primarily designed for external invocation.
4.  **Lock Screen:** The `allBundleIdsOfNotificationsOnLockscreen` function suggests that the system also monitors what notifications are currently visible on the lock screen, potentially triggering updates or prunes if the lock screen state changes significantly.

## Evidence
*   **New Symbols:**
    *   `- [ATXNotificationAndSuggestionDatabase _purgeNotificationBiomeStreamsIfNeeded]` (Code, `0x22b7dbf60`)
    *   `pruneSuggestionsBasedOnHardLimitsWithXPCActivity` (String/Data, `0x22b67303c`)
    *   `pruneNotificationsBasedOnHardLimitsWithXPCActivity` (String/Data, `0x22b672c23`)
    *   `__kATXBiomeNotificationPurgeCompleteKey` (Data Key, `0x2843cbb58`)
*   **New Strings:**
    *   `"ATXNotificationAndSuggestionDatabase: Purging private notification streams to remove persisted text content"`
    *   `"_purgeNotificationBiomeStreamsIfNeeded"`
*   **Modified Symbols:**
    *   `Functions: 25674` -> `25675` (+1)
    *   `Symbols: 77861` -> `77865` (+4)
    *   `CStrings: 42931` -> `42933` (+2)
*   **Modified Sections:**
    *   `__TEXT.__text`: Grew from `0x4a0f0c` to `0x4a10a4` (approx +1000 bytes).
    *   `__TEXT.__objc_stubs`: Grew from `0x4d9e0` to `0x4da00` (approx +20 bytes, consistent with new method dispatches).
    *   `__DATA_CONST.__got`: Grew from `0x39b8` to `0x39c0` (approx +4 bytes, consistent with new GOT entries for dynamic symbols).
    *   `__DATA_CONST.__objc_selrefs`: Grew from `0x1be90` to `0x1be98` (approx +8 bytes, consistent with new selector references).

## AI Prioritisation Scoring System

- **Symbol Analysis**
  - **Tier**: 1
  - **Category**: Feature Addition
  - **Reasoning**: The diff shows the addition of new symbols related to 'purging' and 'pruning' notification streams, specifically targeting a 'Biome' feature. The presence of 'XPCActivity' in function names indicates an IPC-based feature, which is a significant architectural change. The string 'Purging private notification streams to remove persisted text content' explicitly describes the data privacy impact. This is a high-priority feature addition due to its impact on user data and system behavior.

