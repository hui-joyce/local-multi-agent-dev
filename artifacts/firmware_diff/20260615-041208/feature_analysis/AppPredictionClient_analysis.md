## What this feature does
The `AppPredictionClient` framework has been updated to introduce a new notification length tracking and management system, replacing the previous body/subtitle/title tracking. The new implementation focuses on tracking the character count of notification titles, subtitles, and body lengths, along with flags indicating whether these fields are present. This suggests a shift towards optimizing notification display by tracking length metrics rather than raw content, likely for predictive rendering or UI layout calculations. The feature introduces new Objective-C classes (`ATXPBUserNotification`, `ATXUserNotification`, `ATXMissedNotificationRankingBiomeStream`) and associated selectors for managing these length properties.

## How is it implemented
The implementation consists of several key components:

1. **New Notification Classes**:
   - `ATXPBUserNotification`: A new class that tracks notification length properties (bodyLength, subtitleLength, titleLength) with corresponding getter and setter methods.
   - `ATXUserNotification`: An updated version of the existing notification class with similar length tracking properties.
   - `ATXMissedNotificationRankingBiomeStream`: A class that manages missed notifications, with a `deleteAllEvents` method that prunes events based on a predicate block.

2. **Length Property Management**:
   - **Getters**: `bodyLength`, `hasBodyLength`, `hasSubtitleLength`, `hasTitleLength`
   - **Setters**: `setBodyLength:`, `setHasBodyLength:`, `setSubtitleLength:`, `setHasTitleLength:`
   - The length properties are stored as `unsignedLongLong` values, indicating they track character counts.

3. **Key Decompiled Functions**:
   ```c
   // -[ATXMissedNotificationRankingBiomeStream deleteAllEvents]
   void *__fastcall -[ATXMissedNotificationRankingBiomeStream deleteAllEvents](__int64 a1)
   {
     return objc_msgSend(*(id *)(a1 + 8), "pruneWithPredicateBlock:", &__block_literal_global_18);
   }
   ```
   This function deletes all events from a missed notification stream by calling a pruning method with a predicate block.

   ```c
   // -[ATXPBUserNotification bodyLength]
   __int64 __fastcall -[ATXPBUserNotification bodyLength](__int64 a1)
   {
     return *(_QWORD *)(a1 + 24);
   }
   ```
   Retrieves the body length from a notification object.

   ```c
   // -[ATXPBUserNotification hasBodyLength]
   __int64 __fastcall -[ATXPBUserNotification hasBodyLength](__int64 a1)
   {
     return (*(unsigned __int8 *)(a1 + 216) >> 2) & 1;
   }
   ```
   Checks if the body length property is set.

   ```c
   // -[ATXPBUserNotification setBodyLength:]
   __int64 __fastcall -[ATXPBUserNotification setBodyLength:](__int64 result, __int64 a2, __int64 a3)
   {
     *(_DWORD *)(result + 216) |= 4u;
     *(_QWORD *)(result + 24) = a3;
     return result;
   }
   ```
   Sets the body length value and marks the property as present.

4. **Data Flow**:
   - Notification objects store length properties at specific offsets (24 bytes for bodyLength, 216 bytes for length flags).
   - The `deleteAllEvents` method uses a predicate block to filter and remove events, suggesting dynamic notification management.
   - String constants like `TQ,N,V_bodyLength` indicate property tracking in a structured format.

## How to trigger this feature
The feature is triggered when:
1. Notifications are processed or displayed, and the system needs to track their length properties.
2. The `ATXMissedNotificationRankingBiomeStream` is used to manage missed notifications, with `deleteAllEvents` called to prune events based on a predicate.
3. The new notification classes (`ATXPBUserNotification`, `ATXUserNotification`) are instantiated and their length properties are set or retrieved.
4. The UUID change suggests this is a new or significantly modified feature in the 26.4.2 update.

## Evidence
- **New Symbols**: 12 new Objective-C methods and 3 new instance variables related to notification length tracking.
- **New CStrings**: Strings like `TQ,N,V_bodyLength`, `TQ,N,V_subtitleLength`, `TQ,N,V_titleLength` indicate property tracking.
- **Address Changes**: Significant changes in section sizes (`__TEXT.__text`, `__TEXT.__objc_methlist`, etc.) indicate substantial code additions.
- **Decompiled Functions**: Key functions show length property management and event pruning logic.
- **String Constants**: Long string like `"{?=\"appSpecifiedScore\"b1\"badge\"b1\"bodyLength\"b1\"numberOfNotificationsInStack\"b1\"positionInStack\"b1\"recordTimestamp\"b1\"timestamp\"b1\"attachmentType\"b1\"priorityStatus\"b1\"summaryStatus\"b1\"urgency\"b1\"isGroupMessage\"b1\"isMessage\"b1\"isNotificationSummaryEnabled\"b1\"isPartOfStack\"b1\"isPriorityNotificationEnabled\"b1\"isStackSummary\"b1\"isSummarized\"b1\"}"` suggests a complex notification metadata structure.

## AI Prioritisation Scoring System

- **symbol_analysis**
  - **Tier**: 2
  - **Category**: notification_management
  - **Reasoning**: New notification length tracking system with significant code additions, suggesting a feature for optimizing notification display and management.

