## What this feature does
The `AppPredictionClient` framework has been updated to introduce a new notification metadata tracking system focused on **length validation** and **biome stream cleanup**. The update replaces the original `body`, `subtitle`, and `title` string fields with numeric `bodyLength`, `subtitleLength`, and `titleLength` integer fields. This change suggests a shift from storing raw text to tracking the character count of notification components, likely to optimize memory usage, enable dynamic UI rendering, or support notification summarization logic. Additionally, two new biome stream classes (`ATXMissedNotificationRankingBiomeStream` and `ATXUserNotificationDigestBiomeStream`) have been added, both featuring a `deleteAllEvents` method, indicating a new mechanism for managing and purging notification history based on user activity or time-based rules.

## How is it implemented
The implementation involves two distinct but related changes:

1.  **Notification Data Structure Refactoring**:
    *   The `ATXPBUserNotification` and `ATXUserNotification` classes have been modified.
    *   The original string-based properties (`body`, `subtitle`, `title`) have been removed.
    *   New integer properties (`bodyLength`, `subtitleLength`, `titleLength`) have been added to store the length of the corresponding notification text.
    *   New accessor methods (`hasBodyLength`, `hasSubtitleLength`, `hasTitleLength`) and mutator methods (`setBodyLength:`, `setSubtitleLength:`, `setTitleLength:`) have been introduced to manage these new fields.
    *   The `ATXUserNotification` class also gained a `bodyLength` property, while `ATXPBUserNotification` gained the length properties.
    *   The `ATXUserNotificationDigestBiomeStream` class has been enhanced with a `deleteAllEvents` method, suggesting it can now clear its internal event log.

2.  **Biome Stream Management**:
    *   Two new classes, `ATXMissedNotificationRankingBiomeStream` and `ATXUserNotificationDigestBiomeStream`, have been added to the framework.
    *   Both classes implement a `deleteAllEvents` method, which is a critical function for clearing historical notification data.
    *   The presence of these classes implies a new feature for managing notification history, potentially for "missed" notifications or a "digest" view of notifications.

3.  **String and Symbol Changes**:
    *   The diff shows the removal of strings like `"T@\"NSString\",&,N,V_body"`, `"hasBody"`, etc., and the addition of strings like `"TQ,N,V_bodyLength"`, `"hasBodyLength"`, etc. This confirms the shift from string storage to length tracking.
    *   The addition of `"_bodyLength"`, `"_subtitleLength"`, `"_titleLength"` as C strings suggests these are the new variable names used in the code.
    *   The UUID of the framework has changed, indicating a new build or version of the framework.
    *   The number of functions, symbols, and C strings has increased, reflecting the addition of new classes and methods.

## How to trigger this feature
The feature is triggered by the presence of the new `AppPredictionClient` framework in the system. The framework is responsible for handling notification prediction and management. The new `deleteAllEvents` method in the `ATXMissedNotificationRankingBiomeStream` and `ATXUserNotificationDigestBiomeStream` classes can be triggered by:

1.  **User Action**: The user might manually clear their notification history.
2.  **Time-based**: The system might automatically clear old notifications after a certain period.
3.  **Event-based**: The system might clear notifications when a new event occurs, such as a new message or a system update.

The `bodyLength`, `subtitleLength`, and `titleLength` properties are likely used to determine the size of the notification text, which can be used to:

1.  **Optimize Memory**: By storing the length of the text instead of the text itself, the system can reduce memory usage.
2.  **Dynamic UI Rendering**: The system can use the length of the text to determine how to render the notification in the UI, such as truncating long text or adding ellipses.
3.  **Notification Summarization**: The system can use the length of the text to determine whether to summarize the notification or show the full text.

## Evidence
*   **Symbol Changes**:
    *   Added: `ATXMissedNotificationRankingBiomeStream`, `ATXPBUserNotification`, `ATXUserNotification`, `ATXUserNotificationDigestBiomeStream`, `ATXUserNotificationLoggingEvent`.
    *   Removed: `ATXPBUserNotification` (original version), `ATXUserNotification` (original version).
*   **String Changes**:
    *   Added: `"&G3"`, `"TQ,N,V_bodyLength"`, `"TQ,N,V_subtitleLength"`, `"TQ,N,V_titleLength"`, `"_bodyLength"`, `"_subtitleLength"`, `"_titleLength"`, `"hasBodyLength"`, `"hasSubtitleLength"`, `"hasTitleLength"`, `"setBodyLength:"`, `"setHasBodyLength:"`, `"setHasSubtitleLength:"`, `"setHasTitleLength:"`, `"setSubtitleLength:"`, `"setTitleLength:"`, `"unsignedLongLongValue"`, `"{?=\"appSpecifiedScore\"b1\"badge\"b1\"bodyLength\"b1\"numberOfNotificationsInStack\"b1\"positionInStack\"b1\"recordTimestamp\"b1\"subtitleLength\"b1\"timestamp\"b1\"titleLength\"b1\"attachmentType\"b1\"priorityStatus\"b1\"summaryStatus\"b1\"urgency\"b1\"isGroupMessage\"b1\"isMessage\"b1\"isNotificationSummaryEnabled\"b1\"isPartOfStack\"b1\"isPriorityNotificationEnabled\"b1\"isStackSummary\"b1\"isSummarized\"b1}"`.
    *   Removed: `"T@\"NSString\",&,N,V_body"`, `"hasBody"`, `"{?=\"appSpecifiedScore\"b1\"badge\"b1\"numberOfNotificationsInStack\"b1\"positionInStack\"b1\"recordTimestamp\"b1\"timestamp\"b1\"attachmentType\"b1\"priorityStatus\"b1\"summaryStatus\"b1\"urgency\"b1\"isGroupMessage\"b1\"isMessage\"b1\"isNotificationSummaryEnabled\"b1\"isPartOfStack\"b1\"isPriorityNotificationEnabled\"b1\"isStackSummary\"b1\"isSummarized\"b1}"`.
*   **Framework Metadata**:
    *   Version: `627.11.0.0.0` -> `627.11.0.1.0`.
    *   UUID: `634FFD6C-E956-3D9D-8F0A-F3BFE981D4CF` -> `4B098232-A975-34F6-86D2-4F9B6FDA769B`.
    *   Functions: `10834` -> `10845`.
    *   Symbols: `35817` -> `35854`.
    *   CStrings: `16113` -> `16134`.

## AI Prioritisation Scoring System

- **metadata_analysis**
  - **Tier**: TIER_2
  - **Category**: DATA/IPC/SYNC
  - **Reasoning**: The update introduces a new notification length tracking system and biome stream management, which are important for notification handling and memory optimization, but not critical for system stability or security.

