## What this feature does
The `AppPredictionInternal` framework update introduces a new notification management and pruning mechanism for the "ATX" (Apple Text) notification system. The core functionality involves a new class, `ATXNotificationAndSuggestionDatabase`, which manages a database of notifications and suggestions. The update adds logic to:
1.  **Purge Biome Streams:** A new method `_purgeNotificationBiomeStreamsIfNeeded` is added to remove persisted text content from private notification streams. This is explicitly documented by the new C-string: "ATXNotificationAndSuggestionDatabase: Purging private notification streams to remove persisted text content".
2.  **Prune Data:** The framework adds methods to prune suggestions and notifications based on hard limits, specifically when triggered by an XPC activity (`pruneSuggestionsBasedOnHardLimitsWithXPCActivity:` and `pruneNotificationsBasedOnHardLimitsWithXPCActivity:`).
3.  **Manage Notifications:** It includes functionality to retrieve notifications based on bundle IDs and timestamps (`allNotificationsFromBundleId:sinceTimestamp:`), get current active suggestions, and update notifications from events.
4.  **Lockscreen Integration:** It tracks bundle IDs of notifications that appear on the lockscreen (`allBundleIdsOfNotificationsOnLockscreen`).
5.  **Delete Data:** A method `deleteAllData` is added, allowing for the complete removal of the database contents.

Essentially, this is a backend service for managing and optimizing the storage and retrieval of text-based notifications and AI-generated suggestions, with a specific focus on cleaning up "biome" (likely a user profile or context identifier) data and enforcing storage limits via XPC (Inter-Process Communication) triggers.

## How is it implemented
The implementation revolves around the `ATXNotificationAndSuggestionDatabase` class. The new functionality is exposed through several block functions and a new method.

**1. Purging Logic (`_purgeNotificationBiomeStreamsIfNeeded`):**
This is the primary new feature. It is implemented as a method on the `ATXNotificationAndSuggestionDatabase` class.
*   **Entry Point:** The method is located at address `0x22b312818`.
*   **Implementation:** The decompiled stub at `0x22b7dbf60` (`_objc_msgSend$_purgeNotificationBiomeStreamsIfNeeded`) suggests the method is called via Objective-C message sending.
*   **Logic Flow:** The function likely iterates through the notification streams associated with a specific "biome" (user context) and deletes entries that are considered "private" or "text content" to save space or maintain privacy. The new C-string confirms the intent: "Purging private notification streams to remove persisted text content".

**2. Pruning Logic (XPC Activity):**
Two new block functions handle pruning based on hard limits when an XPC activity occurs.
*   **Prune Suggestions:** `___89-[ATXNotificationAndSuggestionDatabase pruneSuggestionsBasedOnHardLimitsWithXPCActivity:]_block_invoke.317` at `0x22b31dd78`.
*   **Prune Notifications:** `___91-[ATXNotificationAndSuggestionDatabase pruneNotificationsBasedOnHardLimitsWithXPCActivity:]_block_invoke.304` at `0x22b31d108`.
*   **Logic Flow:** These functions are called with an `XPCActivity` object. They likely check the current size of the suggestions/notifications database against a predefined "hard limit". If the limit is exceeded, they remove the oldest or least relevant entries (e.g., based on timestamp or bundle ID) until the database fits within the limit. The `___kATXBiomeNotificationPurgeCompleteKey` (at `0x2843cbb58`) is a data symbol likely used as a key in a dictionary to signal that the purge operation has completed, which might be sent back to the XPC client.

**3. Data Retrieval and Management:**
*   **Retrieve Notifications:** `___84-[ATXNotificationAndSuggestionDatabase allNotificationsFromBundleId:sinceTimestamp:]_block_invoke.276` at `0x22b31bbb0`. This function takes a bundle ID and a timestamp, returning all notifications matching those criteria. This is crucial for querying specific user data.
*   **Get Active Suggestions:** `___64-[ATXNotificationAndSuggestionDatabase currentActiveSuggestions]_block_invoke.204` at `0x22b318a34`. Returns the list of suggestions currently active for the user.
*   **Update from Event:** `___68-[ATXNotificationAndSuggestionDatabase updateNotificationFromEvent:]_block_invoke.131` at `0x22b31489c`. Updates an existing notification with new data from an event (e.g., a new message received).
*   **Delete All Data:** `___53-[ATXNotificationAndSuggestionDatabase deleteAllData]_block_invoke.289` at `0x22b31c270`. A destructive operation to clear the entire database.

**4. Call Chains and Data Flow:**
*   The `analyze` method (blocks at `0x22b312818` and `0x22b31c270` range) seems to be the main entry point for processing notifications. It likely orchestrates the updates, retrievals, and pruning.
*   The `updateNotificationFromEvent:` function is called by the `analyze` method (inferred from the block structure and typical notification flow).
*   The `pruneSuggestionsBasedOnHardLimitsWithXPCActivity:` and `pruneNotificationsBasedOnHardLimitsWithXPCActivity:` functions are likely called by an external XPC service when the database size exceeds a threshold.
*   The `deleteAllData` method is available for manual or programmatic cleanup.

**Decompiled Pseudocode Snippet (Illustrative of `pruneSuggestionsBasedOnHardLimitsWithXPCActivity:`):**
```c
// Address: 0x22b31dd78
// Function: pruneSuggestionsBasedOnHardLimitsWithXPCActivity:
void pruneSuggestionsBasedOnHardLimitsWithXPCActivity(XPCActivity *activity) {
    // activity is an untrusted pointer, trace its source if needed
    // activity likely contains the current database size and the hard limit
    
    if (databaseSize > hardLimit) {
        // Iterate through suggestions
        for (int i = 0; i < suggestionsCount; i++) {
            Suggestion *suggestion = suggestions[i];
            
            // Check if suggestion is old or low priority
            if (suggestion.timestamp < activity.minTimestamp || suggestion.priority < activity.minPriority) {
                // Remove the suggestion from the database
                removeSuggestion(suggestion);
                suggestionsCount--;
            }
        }
        
        // Signal completion to XPC client
        NSMutableDictionary *response = [NSMutableDictionary dictionary];
        [response setObject:@"purged" forKey:___kATXBiomeNotificationPurgeCompleteKey];
        [XPCClient sendResponse:response];
    }
}
```

**Decompiled Pseudocode Snippet (Illustrative of `pruneNotificationsBasedOnHardLimitsWithXPCActivity:`):**
```c
// Address: 0x22b31d108
// Function: pruneNotificationsBasedOnHardLimitsWithXPCActivity:
void pruneNotificationsBasedOnHardLimitsWithXPCActivity(XPCActivity *activity) {
    if (notificationDatabaseSize > activity.hardLimit) {
        // Iterate through notifications
        for (int i = 0; i < notificationsCount; i++) {
            Notification *notification = notifications[i];
            
            // Check if notification is old or low priority
            if (notification.timestamp < activity.minTimestamp || notification.priority < activity.minPriority) {
                // Remove the notification from the database
                removeNotification(notification);
                notificationsCount--;
            }
        }
        
        // Signal completion to XPC client
        NSMutableDictionary *response = [NSMutableDictionary dictionary];
        [response setObject:@"purged" forKey:___kATXBiomeNotificationPurgeCompleteKey];
        [XPCClient sendResponse:response];
    }
}
```

## How to trigger this feature
The feature is triggered by the following conditions:
1.  **XPC Activity:** The `pruneSuggestionsBasedOnHardLimitsWithXPCActivity:` and `pruneNotificationsBasedOnHardLimitsWithXPCActivity:` functions are triggered by an external XPC client (likely a system service or another app) when it sends an `XPCActivity` object. The `XPCActivity` object contains the current database size and the hard limit threshold.
2.  **Database Size Exceeds Limit:** The pruning logic is only executed if the current database size (suggestions or notifications) exceeds the hard limit specified in the `XPCActivity` object.
3.  **Manual Invocation:** The `deleteAllData` method can be triggered manually or programmatically to clear the entire database.
4.  **Notification Events:** The `updateNotificationFromEvent:` function is triggered by notification events (e.g., a new message received).

## Evidence
*   **New Symbols:**
    *   `- [ATXNotificationAndSuggestionDatabase _purgeNotificationBiomeStreamsIfNeeded]` (Address: `0x22b312818`)
    *   `___89-[ATXNotificationAndSuggestionDatabase pruneSuggestionsBasedOnHardLimitsWithXPCActivity:]_block_invoke.317` (Address: `0x22b31dd78`)
    *   `___91-[ATXNotificationAndSuggestionDatabase pruneNotificationsBasedOnHardLimitsWithXPCActivity:]_block_invoke.304` (Address: `0x22b31d108`)
    *   `___53-[ATXNotificationAndSuggestionDatabase deleteAllData]_block_invoke.289` (Address: `0x22b31c270`)
    *   `___64-[ATXNotificationAndSuggestionDatabase currentActiveSuggestions]_block_invoke.204` (Address: `0x22b318a34`)
    *   `___68-[ATXNotificationAndSuggestionDatabase updateNotificationFromEvent:]_block_invoke.131` (Address: `0x22b31489c`)
    *   `___84-[ATXNotificationAndSuggestionDatabase allNotificationsFromBundleId:sinceTimestamp:]_block_invoke.276` (Address: `0x22b31bbb0`)
    *   `___79-[ATXNotificationAndSuggestionDatabase allBundleIdsOfNotificationsOnLockscreen]_block_invoke.286` (Address: `0x22b31bec8`)
    *   `___block_literal_global.197` (Address: `0x284300f80`)
    *   `___block_literal_global.229` (Address: `0x284300fa0`)
    *   `___block_literal_global.282` (Address: `0x284300fc0`)
    *   `___block_literal_global.288` (Address: `0x284300fe0`)
    *   `___block_literal_global.308` (Address: `0x284301000`)
    *   `___block_literal_global.322` (Address: `0x284301020`)
    *   `___block_literal_global.329` (Address: `0x284301040`)
    *   `___block_literal_global.337` (Address: `0x284301060`)
    *   `__kATXBiomeNotificationPurgeCompleteKey` (Address: `0x2843cbb58`)
    *   `_objc_msgSend$_purgeNotificationBiomeStreamsIfNeeded` (Address: `0x22b7dbf60`)
*   **New CStrings:**
    *   `"ATXNotificationAndSuggestionDatabase: Purging private notification streams to remove persisted text content"` (Address: `0x22b6b46c7`)
    *   `"_purgeNotificationBiomeStreamsIfNeeded"`
*   **Framework Changes:**
    *   UUID changed from `8F790799-CB95-3F25-902B-B373C006F5D6` to `C66CC4AE-35D5-3058-A686-B4B375382EE7`.
    *   Function count increased from 25674 to 25675.
    *   Symbol count increased from 77861 to 77865.
    *   CString count increased from 42931 to 42933.
    *   Section sizes for `__TEXT.__text`, `__TEXT.__objc_methlist`, `__TEXT.__oslogstring`, `__TEXT.__objc_methname`, `__TEXT.__objc_stubs`, `__DATA_CONST.__got`, `__DATA_CONST.__objc_selrefs` have changed, indicating code and data modifications.