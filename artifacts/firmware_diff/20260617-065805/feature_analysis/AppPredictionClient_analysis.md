## What this feature does
The `AppPredictionClient` binary has been updated to introduce a new notification management and ranking system, specifically focusing on "Missed" notifications and their associated "Biome" (stacking/grouping) logic. The changes replace the previous `body/subtitle/title` string-based notification model with a new `bodyLength/subtitleLength/titleLength` integer-based model. This suggests a shift towards more granular control over notification metadata, likely for a new notification summary or ranking feature. The new `ATXMissedNotificationRankingBiomeStream` class appears to handle the deletion of events from this new stream, while `ATXPBUserNotification` and `ATXUserNotification` classes manage the new length-based properties.

## How is it implemented
The implementation consists of several new Objective-C classes and methods that work together to manage the new notification structure:

1.  **`ATXMissedNotificationRankingBiomeStream`**: A new class responsible for managing a stream of missed notifications that are part of a "biome" (a group or stack).
    *   **`deleteAllEvents`**: A method that takes a block (`pruneWithPredicateBlock:`) and deletes all events from the stream that match the predicate. This is the core logic for clearing the stream based on a condition.
    *   **Decompiled Logic**:
        ```c
        void *__fastcall -[ATXMissedNotificationRankingBiomeStream deleteAllEvents](__int64 a1)
        {
          return objc_msgSend(*(id *)(a1 + 8), "pruneWithPredicateBlock:", &__block_literal_global_18);
        }
        ```
        The method retrieves the `pruneWithPredicateBlock:` selector and calls it on the object (offset by 8 bytes, likely the `NSHashTable` or similar collection).

2.  **`ATXPBUserNotification`**: A new class representing a user notification with the new length-based properties.
    *   **Properties**: `_bodyLength` (int), `_subtitleLength` (int), `_titleLength` (int).
    *   **Methods**:
        *   `bodyLength`: Returns the `bodyLength` property.
        *   `hasBodyLength`: Returns a boolean indicating if `bodyLength` is set (bit 2 of the flags).
        *   `setBodyLength:`: Sets the `bodyLength` property and updates the flags.
        *   `setHasBodyLength:`: Toggles the `hasBodyLength` flag.
        *   `setSubtitleLength:`: Sets the `subtitleLength` property.
        *   `setHasSubtitleLength:`: Toggles the `hasSubtitleLength` flag.
        *   `setTitleLength:`: Sets the `titleLength` property.
        *   `hasTitleLength`: Returns a boolean indicating if `titleLength` is set.
        *   `subtitleLength`: Returns the `subtitleLength` property.
        *   `titleLength`: Returns the `titleLength` property.
    *   **Decompiled Logic (Examples)**:
        ```c
        __int64 __fastcall -[ATXPBUserNotification bodyLength](__int64 a1)
        {
          return *(_QWORD *)(a1 + 24);
        }

        __int64 __fastcall -[ATXPBUserNotification hasBodyLength](__int64 a1)
        {
          return (*(unsigned __int8 *)(a1 + 216) >> 2) & 1;
        }

        __int64 __fastcall -[ATXPBUserNotification setBodyLength:](__int64 result, __int64 a2, __int64 a3)
        {
          *(_DWORD *)(result + 216) |= 4u; // Set bit 2 of the flags
          *(_QWORD *)(result + 24) = a3;   // Set the bodyLength value
          return result;
        }
        ```

3.  **`ATXUserNotification`**: A legacy class that appears to be transitioning to the new `ATXPBUserNotification` model. It has similar properties (`_body`, `_subtitle`, `_title`) but is being replaced.
    *   **Methods**: `setBodyLength:`, `setSubtitleLength:`, `setTitleLength:`. These methods seem to be stubs or bridges to the new length-based properties, possibly updating the old `_body` field or just acting as a compatibility layer.
    *   **Decompiled Logic (Examples)**:
        ```c
        __int64 objc_msgSend_setBodyLength_(void *a1, const char *a2, ...)
        {
          return MEMORY[0x1EF012918](a1, off_1E7F93820); // Calls a memory address, likely a C function or another ObjC method
        }
        ```

4.  **`ATXUserNotificationDigestBiomeStream`**: A new class for digesting (summarizing) a stream of user notifications.
    *   **`deleteAllEvents`**: Similar to `ATXMissedNotificationRankingBiomeStream`, it deletes all events from the stream based on a predicate block.

5.  **Data Structures**:
    *   New CStrings like `"TQ,N,V_bodyLength"`, `"TQ,N,V_subtitleLength"`, `"TQ,N,V_titleLength"` suggest new property definitions or serialization formats.
    *   A large JSON-like string `"{?=\"appSpecifiedScore\"b1\"badge\"b1\"bodyLength\"b1\"numberOfNotificationsInStack\"b1\"positionInStack\"b1\"recordTimestamp\"b1\"timestamp\"b1\"attachmentType\"b1\"priorityStatus\"b1\"summaryStatus\"b1\"urgency\"b1\"isGroupMessage\"b1\"isMessage\"b1\"isNotificationSummaryEnabled\"b1\"isPartOfStack\"b1\"isPriorityNotificationEnabled\"b1\"isStackSummary\"b1\"isSummarized\"b1\"}"` indicates a complex data structure being used, likely for notification metadata or a filter.

## How to trigger this feature
The feature is triggered by the presence of the new `AppPredictionClient` binary in the system, which is part of the iOS 26.4.2 (23E261) firmware update. The new classes and methods are loaded when the `AppPredictionClient` framework is initialized. The specific code paths for `ATXMissedNotificationRankingBiomeStream` and `ATXPBUserNotification` are invoked when the system needs to manage or display notifications that are part of a "biome" or have the new length-based properties. The `deleteAllEvents` methods are likely called by a higher-level notification manager when a user clears their notification center or when a specific condition (e.g., a new notification arrives) is met.

## Evidence
*   **Binary**: `/System/Library/PrivateFrameworks/AppPredictionClient.framework/AppPredictionClient`
*   **Version Change**: 627.11.0.0.0 -> 627.11.0.1.0
*   **Symbol Changes**:
    *   **Added**: `ATXMissedNotificationRankingBiomeStream`, `ATXPBUserNotification`, `ATXUserNotification`, `ATXUserNotificationDigestBiomeStream`, and numerous methods/properties related to `bodyLength`, `subtitleLength`, `titleLength`, and flags like `hasBodyLength`, `hasSubtitleLength`, `hasTitleLength`.
    *   **Removed**: `ATXPBUserNotification` methods related to `body`, `subtitle`, `title` (e.g., `body`, `hasBody`, `setBody:`).
*   **String Changes**:
    *   **Added**: `"TQ,N,V_bodyLength"`, `"TQ,N,V_subtitleLength"`, `"TQ,N,V_titleLength"`, `"hasBodyLength"`, `"hasSubtitleLength"`, `"hasTitleLength"`, `"setBodyLength:"`, `"setHasBodyLength:"`, `"setHasSubtitleLength:"`, `"setHasTitleLength:"`, `"setSubtitleLength:"`, `"setTitleLength:"`, `"unsignedLongLongValue"`, and a large JSON-like string with keys like `bodyLength`, `numberOfNotificationsInStack`, `positionInStack`, `timestamp`, `isGroupMessage`, `isPriorityNotificationEnabled`, `isSummarized`, etc.
    *   **Removed**: `"T@\"NSString\",&,N,V_body"`, `"hasBody"`, and the previous JSON-like string.
*   **Decompiled Functions**:
    *   `-[ATXMissedNotificationRankingBiomeStream deleteAllEvents]`: Calls `pruneWithPredicateBlock:`.
    *   `-[ATXPBUserNotification bodyLength]`: Returns the `bodyLength` property.
    *   `-[ATXPBUserNotification hasBodyLength]`: Checks if `bodyLength` is set.
    *   `-[ATXPBUserNotification setBodyLength:]`: Sets the `bodyLength` property and updates flags.
    *   `objc_msgSend_setBodyLength_`: A stub that calls a memory address.
    *   `objc_msgSend_setSubtitleLength_`: A stub that calls a memory address.
    *   `objc_msgSend_setTitleLength_`: A stub that calls a memory address.

## AI Prioritisation Scoring System

- **symbol_analysis**
  - **Tier**: TIER_1
  - **Category**: notification_management
  - **Reasoning**: The diff shows the introduction of a new notification ranking and biome system (`ATXMissedNotificationRankingBiomeStream`) and a new notification model (`ATXPBUserNotification`) with length-based properties (`bodyLength`, `subtitleLength`, `titleLength`). This indicates a significant change in how notifications are structured, managed, and potentially displayed, likely related to a new notification summary or grouping feature. The presence of AUTO-PROMOTE indicators (new symbols, security/privacy/IPC strings, migration logic) and the replacement of an old notification model with a new one strongly suggests this is a high-priority feature change.

