## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "&G3"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 2 (2 AI-authored, 0 auto-generated); comments: 6 (2 AI-authored, 4 auto-generated); across 4 function(s); verified persisted in .i64: 4 named variables, 4 comments.

## What this feature does

This update to the `AppPredictionClient` framework introduces a more efficient data representation for notification-related telemetry and logging. Specifically, it replaces full string storage for notification titles, subtitles, and bodies with length-based metadata (integer counts). Additionally, it adds new functionality to the Biome stream management system to support the bulk deletion of events for missed notification rankings and notification digests.

## How is it implemented


### Decompilation at `0x1c19806b8`

```c
void *__fastcall -[ATXFaceGalleryBiomeStream deleteAllEvents](__int64 stream_instance)
{
  return objc_msgSend(*(id *)(stream_instance + 8), "pruneWithPredicateBlock:", &__block_literal_global_5);
}
```

### Decompilation at `0x1c19cb3e4`

```c
__int64 __fastcall -[ATXPBUserNotification hasSubtitleLength](__int64 n_a1)
{
  return (*(unsigned __int8 *)(n_a1 + 216) >> 6) & 1;
}
```

### Decompilation at `0x1c19cb380`

```c
__int64 __fastcall -[ATXPBUserNotification hasTitleLength](__int64 n_a1)
{
  return *(_BYTE *)(n_a1 + 217) & 1;
}
```

### Decompilation at `0x1c19cb320`

```c
__int64 __fastcall -[ATXPBUserNotification hasBodyLength](__int64 pb_user_notification)
{
  return (*(unsigned __int8 *)(pb_user_notification + 216) >> 2) & 1;
}
```

The implementation shifts from storing the actual content of notification strings to storing their lengths. This is reflected in the `ATXPBUserNotification` class, where the previous `NSString` properties for body, subtitle, and title have been removed in favor of `unsigned long long` length properties. The class now uses bitmask-based flags to track whether these lengths are present, allowing for more compact serialization.

The Biome stream management updates involve the addition of `deleteAllEvents` methods for `ATXMissedNotificationRankingBiomeStream` and `ATXUserNotificationDigestBiomeStream`. These methods leverage existing pruning infrastructure by invoking a predicate-based cleanup process on the underlying data stream, ensuring that historical notification ranking and digest data can be cleared efficiently.

## How to trigger this feature

The length-based notification logging is triggered whenever the system processes or logs a notification event through the `ATXPBUserNotification` protocol, which now automatically captures the length of the notification components instead of the full text. The `deleteAllEvents` functionality is triggered by system-level maintenance tasks or user-initiated actions that request the clearing of notification history or ranking data within the Biome framework.

## Vulnerability Assessment

This change appears to be a privacy-focused optimization rather than a security patch. By storing only the length of notification strings rather than the full content, the framework reduces the amount of sensitive user data persisted in logs and telemetry streams. This minimizes the risk of accidental exposure of private notification content (e.g., message bodies or titles) in diagnostic logs or backups. No evidence of memory corruption or privilege escalation mitigation was observed; the changes are structural and data-handling related.

## Evidence

- **Symbols Added**: `-[ATXPBUserNotification bodyLength]`, `-[ATXPBUserNotification subtitleLength]`, `-[ATXPBUserNotification titleLength]`, `-[ATXMissedNotificationRankingBiomeStream deleteAllEvents]`, `-[ATXUserNotificationDigestBiomeStream deleteAllEvents]`.
- **Symbols Removed**: `-[ATXPBUserNotification body]`, `-[ATXPBUserNotification subtitle]`, `-[ATXPBUserNotification title]`.
- **Data Structure**: The `ATXPBUserNotification` class now uses a bitfield structure to track the presence of length metadata, replacing the previous string-based storage.
- **Binary Diff**: Increase in `__objc_methlist` and `__objc_ivar` sections consistent with the addition of new property accessors and instance variables.

## AI Prioritisation Scoring System

- **feature_analysis**
  - **Tier**: TIER_2
  - **Category**: privacy_optimization
  - **Reasoning**: The changes represent a significant privacy-focused refactor of data logging, reducing the persistence of sensitive user content in telemetry, which is a core functional and privacy-impacting update.

