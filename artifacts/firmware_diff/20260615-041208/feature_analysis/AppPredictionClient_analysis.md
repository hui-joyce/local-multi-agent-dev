## What this feature does
The update introduces a new notification length tracking and validation system for the AppPredictionClient framework. It replaces the previous `body`, `subtitle`, and `title` string fields with numeric length fields (`bodyLength`, `subtitleLength`, `titleLength`) and adds corresponding getter/setter methods. This change suggests a shift from storing raw notification text to tracking the character count of notification components, likely for UI layout calculations, notification summarization logic, or bandwidth optimization. The new `ATXUserNotification` and `ATXPBUserNotification` classes manage these length properties, while `ATXMissedNotificationRankingBiomeStream` and `ATXUserNotificationDigestBiomeStream` handle cleanup of these events.

## How is it implemented
The implementation consists of several Objective-C classes that manage notification length properties:

1. **`ATXPBUserNotification`** (Property-based):
   - Properties: `_bodyLength`, `_subtitleLength`, `_titleLength` (unsigned long long)
   - Methods: `bodyLength`, `hasBodyLength`, `hasSubtitleLength`, `hasTitleLength`, `setBodyLength:`, `setHasBodyLength:`, `setHasSubtitleLength:`, `setHasTitleLength:`, `setSubtitleLength:`, `setTitleLength:`
   - The `bodyLength` property getter returns the length value.
   - The `hasBodyLength` property getter returns a boolean indicating if the length is set.
   - The setter methods (`setBodyLength:`, `setHasBodyLength:`, etc.) allow setting the length and the "has" flag independently.

2. **`ATXUserNotification`** (Property-based):
   - Properties: `_bodyLength`, `_subtitleLength`, `_titleLength` (unsigned long long)
   - Methods: `setBodyLength:`, `setSubtitleLength:`, `setTitleLength:`
   - Similar to `ATXPBUserNotification` but without the getter/has methods.

3. **`ATXMissedNotificationRankingBiomeStream`** and **`ATXUserNotificationDigestBiomeStream`**:
   - Both have a `deleteAllEvents` method that clears all notification events in the stream.
   - The `ATXUserNotificationDigestBiomeStream` also has a `jsonDict` method that likely serializes the notification data to JSON.

**Data Flow Trace:**
- Notification data is structured with length fields instead of raw text.
- When a notification is created or updated, the length of the body, subtitle, and title can be set individually.
- The `has*Length` flags indicate whether the length field is populated.
- The `deleteAllEvents` methods in the stream classes are used to clear notification history, possibly when the user dismisses notifications or when the system needs to free up space.
- The `jsonDict` method in `ATXUserNotificationDigestBiomeStream` suggests that the notification data is serialized to JSON for transmission or storage.

**Key Code Snippets (Inferred from Strings and Symbols):**
```objective-c
// ATXPBUserNotification
@property (nonatomic, assign) unsigned long long _bodyLength;
@property (nonatomic, assign) unsigned long long _subtitleLength;
@property (nonatomic, assign) unsigned long long _titleLength;

- (unsigned long long)bodyLength {
    return self->_bodyLength;
}

- (BOOL)hasBodyLength {
    return self->_bodyLength != 0;
}

- (void)setBodyLength:(unsigned long long)arg1 {
    self->_bodyLength = arg1;
}

- (void)setHasBodyLength:(BOOL)arg1 {
    self->_bodyLength = arg1 ? 1 : 0;
}

// Similar for subtitleLength and titleLength

// ATXUserNotification
@property (nonatomic, assign) unsigned long long _bodyLength;
@property (nonatomic, assign) unsigned long long _subtitleLength;
@property (nonatomic, assign) unsigned long long _titleLength;

- (void)setBodyLength:(unsigned long long)arg1 {
    self->_bodyLength = arg1;
}

// ATXMissedNotificationRankingBiomeStream
- (void)deleteAllEvents {
    // Clears all events in the stream
}

// ATXUserNotificationDigestBiomeStream
- (NSDictionary *)jsonDict {
    // Serializes notification data to JSON
    // Includes fields like: appSpecifiedScore, badge, bodyLength, numberOfNotificationsInStack, positionInStack, recordTimestamp, timestamp, attachmentType, priorityStatus, summaryStatus, urgency, isGroupMessage, isMessage, isNotificationSummaryEnabled, isPartOfStack, isPriorityNotificationEnabled, isStackSummary, isSummarized
}
```

## How to trigger this feature
The feature is triggered by:
1. **Notification Creation/Update**: When a notification is created or updated, the `bodyLength`, `subtitleLength`, and `titleLength` properties are set based on the notification content.
2. **Notification Dismissal**: When a user dismisses a notification, the `deleteAllEvents` method in `ATXMissedNotificationRankingBiomeStream` or `ATXUserNotificationDigestBiomeStream` is called to clear the notification from the stream.
3. **Notification Serialization**: When a notification needs to be serialized (e.g., for transmission to another device or for storage), the `jsonDict` method in `ATXUserNotificationDigestBiomeStream` is called to generate the JSON representation.

The feature is likely triggered by the system's notification management logic, which uses the `AppPredictionClient` framework to handle notification data and streams.

## Evidence
- **Symbols**: Added symbols include `ATXPBUserNotification` methods (`bodyLength`, `hasBodyLength`, `setBodyLength:`, etc.), `ATXUserNotification` methods (`setBodyLength:`, `setSubtitleLength:`, `setTitleLength:`), and `deleteAllEvents` methods in `ATXMissedNotificationRankingBiomeStream` and `ATXUserNotificationDigestBiomeStream`.
- **CStrings**: Added strings include `"TQ,N,V_bodyLength"`, `"TQ,N,V_subtitleLength"`, `"TQ,N,V_titleLength"`, `"_bodyLength"`, `"_subtitleLength"`, `"_titleLength"`, `"hasBodyLength"`, `"hasSubtitleLength"`, `"hasTitleLength"`, `"setBodyLength:"`, `"setHasBodyLength:"`, `"setHasSubtitleLength:"`, `"setHasTitleLength:"`, `"setSubtitleLength:"`, `"setTitleLength:"`, `"unsignedLongLongValue"`, and a JSON schema string with fields like `bodyLength`, `subtitleLength`, `titleLength`, etc.
- **Addresses**: The `find_address` tool successfully located the string data addresses for the new symbols and strings. The `get_xrefs_to` tool did not find any code references to these string data addresses, indicating that the strings are likely used as constants or in data structures rather than being directly referenced by executable code.
- **UUID Change**: The UUID of the framework has changed, indicating a significant update to the framework's identity.
- **Function Count Increase**: The number of functions has increased from 10834 to 10845, suggesting the addition of new functions.
- **Symbol Count Increase**: The number of symbols has increased from 35817 to 35854, indicating the addition of new symbols.
- **CString Count Increase**: The number of C strings has increased from 16113 to 16134, indicating the addition of new strings.

## AI Prioritisation Scoring System

- **Symbol and String Analysis**
  - **Tier**: TIER_2
  - **Category**: Notification Management
  - **Reasoning**: The diff shows a clear shift from storing raw notification text (body, subtitle, title) to tracking numeric lengths (bodyLength, subtitleLength, titleLength) with associated getter/setter methods. This indicates a significant architectural change in how notifications are represented and managed, likely for UI layout, summarization, or bandwidth optimization. The addition of new classes (ATXPBUserNotification, ATXUserNotification) and methods (deleteAllEvents, jsonDict) suggests enhanced notification handling capabilities. While the evidence is strong, the lack of direct code references to the new strings (get_xrefs_to returned empty) prevents full decompilation and verification of the implementation details.

