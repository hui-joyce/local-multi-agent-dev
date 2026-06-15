## What this feature does
The `AppPredictionInternal` framework update introduces a new notification management and pruning mechanism for a database class named `ATXNotificationAndSuggestionDatabase`. The primary functionality involves purging private notification streams to remove persisted text content, which is critical for managing storage and performance. The feature also includes logic to analyze notifications, delete all data, retrieve current active suggestions, and prune notifications/suggestions based on hard limits triggered by XPC activity. The addition of the constant `__kATXBiomeNotificationPurgeCompleteKey` suggests a signaling mechanism for when the purge operation completes.

## How is it implemented
The implementation centers around the `ATXNotificationAndSuggestionDatabase` class, which appears to be a singleton or globally accessible database manager for notifications and suggestions. The key methods added in this update are:

1.  **`_purgeNotificationBiomeStreamsIfNeeded`**: This method is responsible for the core "purging" logic. It likely iterates through internal data structures (notification streams) and removes entries that are no longer needed or have exceeded certain limits. The string "Purging private notification streams to remove persisted text content" confirms its purpose.
2.  **`analyze`**: This method likely processes incoming notification events or suggestions to determine their relevance, priority, or eligibility for display. The block names `analyze]_block_invoke` suggest it's a block-based method, possibly used as a callback.
3.  **`deleteAllData`**: A destructive operation that clears the entire database. This is likely a fallback or a user-initiated action (e.g., "Clear All Notifications").
4.  **`currentActiveSuggestions`**: Retrieves the list of suggestions currently being shown or considered for display.
5.  **`updateNotificationFromEvent:`**: Updates an existing notification object based on a new event (e.g., a new message received).
6.  **`allBundleIdsOfNotificationsOnLockscreen`**: Queries the database for all notification bundle IDs that are currently visible on the lock screen.
7.  **`allNotificationsFromBundleId:sinceTimestamp:`**: A query method to fetch notifications belonging to a specific app (bundle ID) that occurred after a given timestamp.
8.  **`pruneSuggestionsBasedOnHardLimitsWithXPCActivity:`** and **`pruneNotificationsBasedOnHardLimitsWithXPCActivity:`**: These are the most critical new methods. They implement a "hard limit" pruning strategy, likely triggered by an XPC (Inter-Process Communication) activity. This suggests an external process (perhaps a system daemon or a different app) can request the database to prune its data if it exceeds a certain size or count. The "hard limits" implies strict enforcement, possibly to prevent the database from growing too large and consuming excessive memory or battery.

The implementation heavily relies on Objective-C blocks (`_block_invoke`), indicating a functional programming style within the class. The presence of `GCC_except_table` entries suggests the code includes exception handling, which is important for robustness, especially for operations like `deleteAllData` or network-related queries.

The framework also depends on several Swift libraries (`libswift_StringProcessing.dylib`, `libswiftos.dylib`, `libswiftsimd.dylib`), indicating that the database logic involves complex string manipulation, OS-level operations, and numerical computations (likely for calculating limits or timestamps).

The UUID change (`8F790799-CB95-3F25-902B-B373C006F5D6` -> `C66CC4AE-35D5-3058-A686-B4B375382EE7`) and the slight increase in function count (25674 -> 25675) and symbol count (77861 -> 77865) confirm that this is a significant but incremental update to the framework, adding new functionality without a complete rewrite.

## How to trigger this feature
The feature is triggered by:
1.  **Internal Logic**: The `analyze` method is likely called periodically or upon receiving new events to process notifications.
2.  **External XPC Request**: The `pruneSuggestionsBasedOnHardLimitsWithXPCActivity:` and `pruneNotificationsBasedOnHardLimitsWithXPCActivity:` methods are explicitly triggered by XPC activity. This means an external process can send a request to the `AppPredictionInternal` framework to prune the database if it exceeds predefined limits.
3.  **User Action**: The `deleteAllData` method can be triggered by a user action, such as clearing all notifications from the settings menu.
4.  **Lock Screen Updates**: The `updateNotificationFromEvent:` and `allBundleIdsOfNotificationsOnLockscreen` methods are likely triggered by system events related to the lock screen, such as a new message arriving or the lock screen being unlocked.

The `__kATXBiomeNotificationPurgeCompleteKey` constant is likely used as a key in a dictionary or a notification center to signal when the purge operation has completed, allowing other parts of the system to react accordingly.

## Evidence
*   **New Symbols**:
    *   `-[ATXNotificationAndSuggestionDatabase _purgeNotificationBiomeStreamsIfNeeded]`
    *   `GCC_except_table173`, `GCC_except_table178` (Exception handling)
    *   `___47-[ATXNotificationAndSuggestionDatabase analyze]_block_invoke.341` (Block for analyze)
    *   `___53-[ATXNotificationAndSuggestionDatabase deleteAllData]_block_invoke.289` (Block for deleteAllData)
    *   `___64-[ATXNotificationAndSuggestionDatabase currentActiveSuggestions]_block_invoke.204` (Block for currentActiveSuggestions)
    *   `___68-[ATXNotificationAndSuggestionDatabase updateNotificationFromEvent:]_block_invoke.131` (Block for updateNotificationFromEvent)
    *   `___79-[ATXNotificationAndSuggestionDatabase allBundleIdsOfNotificationsOnLockscreen]_block_invoke.286` (Block for allBundleIdsOfNotificationsOnLockscreen)
    *   `___84-[ATXNotificationAndSuggestionDatabase allNotificationsFromBundleId:sinceTimestamp:]_block_invoke.276` (Block for allNotificationsFromBundleId)
    *   `___89-[ATXNotificationAndSuggestionDatabase pruneSuggestionsBasedOnHardLimitsWithXPCActivity:]_block_invoke.317` (Block for pruneSuggestionsBasedOnHardLimits)
    *   `___89-[ATXNotificationAndSuggestionDatabase pruneNotificationsBasedOnHardLimitsWithXPCActivity:]_block_invoke.304` (Block for pruneNotificationsBasedOnHardLimits)
    *   `__kATXBiomeNotificationPurgeCompleteKey` (Constant for purge completion signal)
    *   `_objc_msgSend$_purgeNotificationBiomeStreamsIfNeeded` (Message send for the purge method)
*   **New CStrings**:
    *   `"ATXNotificationAndSuggestionDatabase: Purging private notification streams to remove persisted text content"` (Description of the purge functionality)
    *   `"_purgeNotificationBiomeStreamsIfNeeded"` (Method name)
*   **Section Changes**:
    *   `__TEXT.__text`: Increased by 0x1000 (4096 bytes)
    *   `__TEXT.__objc_methlist`: Increased by 0x8 (8 bytes)
    *   `__TEXT.__oslogstring`: Increased by 0x50 (80 bytes)
    *   `__TEXT.__objc_methname`: Increased by 0x10 (16 bytes)
    *   `__TEXT.__objc_stubs`: Increased by 0x100 (256 bytes)
    *   `__DATA_CONST.__got`: Increased by 0x8 (8 bytes)
    *   `__DATA_CONST.__objc_selrefs`: Increased by 0x8 (8 bytes)
    *   `__DATA_CONST.__objc_superrefs`: Increased by 0x1000 (4096 bytes)
    *   `__DATA_CONST.__objc_arraydata`: Increased by 0x10 (16 bytes)
*   **Framework Dependencies**:
    *   Removed: `/usr/lib/swift/libswift_StringProcessing.dylib`, `/usr/lib/swift/libswiftos.dylib`, `/usr/lib/swift/libswiftsimd.dylib`
    *   This suggests a refactoring or optimization of the Swift dependencies, possibly moving some logic to the framework itself or using a different set of libraries.

## AI Prioritisation Scoring System

- **Feature Analysis**
  - **Tier**: TIER_2
  - **Category**: System Framework Update
  - **Reasoning**: The update introduces significant new functionality for managing and pruning notification and suggestion data within the AppPredictionInternal framework. The addition of methods for purging streams, analyzing notifications, and pruning based on hard limits via XPC activity indicates a substantial change in how the system handles predictive notifications and suggestions. The presence of new symbols, strings, and changes to section sizes, along with the removal of some Swift dependencies, suggests a refactoring and optimization of the existing codebase. The feature is likely critical for maintaining system performance and user experience by preventing the notification and suggestion database from growing too large.

