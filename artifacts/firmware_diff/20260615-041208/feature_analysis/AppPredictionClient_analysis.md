## What this feature does
The `AppPredictionClient` framework has been updated to introduce a new notification length tracking and ranking system, replacing the previous body/title/subtitle tracking. The new implementation focuses on tracking the length of notification bodies, subtitles, and titles (in characters) rather than the presence of these fields. This suggests a shift towards analyzing notification content volume for ranking or prediction purposes, likely to prioritize notifications with more substantial content or to filter out very short, low-value notifications. The feature involves new Objective-C classes (`ATXPBUserNotification`, `ATXUserNotification`, `ATXMissedNotificationRankingBiomeStream`) and associated notification digest streams.

## How is it implemented
The implementation consists of several new Objective-C classes and methods:

1. **`ATXPBUserNotification`**: A new class representing a user notification with properties for body length, subtitle length, and title length. It includes methods to set and get these lengths:
   - `bodyLength` (getter)
   - `hasBodyLength` (getter)
   - `setBodyLength:` (setter)
   - `hasSubtitleLength` (getter)
   - `setHasSubtitleLength:` (setter)
   - `subtitleLength` (getter)
   - `setSubtitleLength:` (setter)
   - `setTitleLength:` (setter)
   - `titleLength` (getter)

2. **`ATXUserNotification`**: An updated version of the user notification class with similar length tracking properties.

3. **`ATXMissedNotificationRankingBiomeStream`**: A new class for ranking missed notifications, with a `deleteAllEvents` method.

4. **`ATXUserNotificationDigestBiomeStream`**: A new class for digesting user notification events, with a `deleteAllEvents` method and a `jsonDict` method that returns a dictionary containing various notification fields including the new length fields.

The implementation uses Objective-C runtime features like `objc_msgSend` for method calls and includes block invocations for the `deleteAllEvents` methods. The data flow suggests that notification lengths are being tracked and potentially used for ranking or filtering notifications.

## How to trigger this feature
The feature is triggered by the presence of the new `AppPredictionClient` framework in the system. The new notification length tracking and ranking functionality would be invoked when:
- The system processes user notifications
- The system needs to rank or filter notifications based on their content length
- The `ATXMissedNotificationRankingBiomeStream` or `ATXUserNotificationDigestBiomeStream` classes are instantiated and their methods are called

The feature is likely triggered by system events related to notification processing, such as when a notification is received, when the user interacts with the notification center, or when the system needs to update notification rankings.

## Evidence
- **New Symbols**: Added symbols include `ATXPBUserNotification` methods and properties, `ATXUserNotification` methods, and `ATXMissedNotificationRankingBiomeStream` methods.
- **New CStrings**: Added strings include notification length field names (`bodyLength`, `subtitleLength`, `titleLength`), setter/getter method names, and a complex dictionary format string containing various notification fields.
- **Removed Symbols**: Removed symbols include the old `ATXPBUserNotification` methods and properties related to body, subtitle, and title presence (`hasBody`, `hasSubtitle`, `hasTitle`, `setBody:`, `setSubtitle:`, `setTitle:`).
- **UUID Change**: The framework's UUID has changed from `634FFD6C-E956-3D9D-8F0A-F3BFE981D4CF` to `4B098232-A975-34F6-86D2-4F9B6FDA769B`, indicating a significant update.
- **Function Count**: Increased from 10834 to 10845, suggesting new code has been added.
- **Symbol Count**: Increased from 35817 to 35854, confirming new symbols have been added.
- **CString Count**: Increased from 16113 to 16134, indicating new strings have been added.

## AI Prioritisation Scoring System

- **symbol_analysis**
  - **Tier**: TIER_1
  - **Category**: notification_ranking
  - **Reasoning**: High-signal indicators: Added symbols related to notification length tracking and ranking, new CStrings with notification field names, removed old notification presence tracking, UUID change, and function/symbol count increases. The feature represents a significant shift in notification processing logic from presence-based to length-based tracking for ranking purposes.

