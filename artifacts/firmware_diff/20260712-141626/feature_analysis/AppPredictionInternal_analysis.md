## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "ATXNotificationAndSuggestionDatabase: Purging private notification streams to remove persisted text content"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 3 (3 AI-authored, 0 auto-generated); comments: 2 (1 AI-authored, 1 auto-generated); across 1 function(s); verified persisted in .i64: 10 named variables, 1 comments.

## What this feature does
This feature introduces a one-time purge mechanism for notification-related Biome streams within the `AppPredictionInternal` framework. It is designed to delete persisted text content from private notification streams, likely to address a privacy issue where sensitive notification text was being inadvertently stored or retained longer than intended.

## How is it implemented


### Decompilation at `0x22b312818`

```c
__int64 -[ATXNotificationAndSuggestionDatabase _purgeNotificationBiomeStreamsIfNeeded]()
{
  void *notificationPrefs; // x19
  __int64 purgeEnabled; // x20
  void *boolForKey; // x0
  __int64 log_handle; // x0
  __int64 log_obj; // x21
  __int64 is_log_enabled; // x0
  void *deleteAllEvents; // x0
  void *deleteAllEvents_2; // x0
  void *deleteAllEvents_3; // x0
  _WORD n_v10[8]; // [xsp+0h] [xbp-30h] BYREF

  notificationPrefs = objc_msgSend(
                        (id)MEMORY[0x22DA02CA0](MEMORY[0x278972A30]),
                        "initWithSuiteName:",
                        *MEMORY[0x27899F6D8]);
  purgeEnabled = *MEMORY[0x27899F6F0];
  boolForKey = objc_msgSend(notificationPrefs, "boolForKey:", *MEMORY[0x27899F6F0]);
  if ( ((unsigned __int8)boolForKey & 1) == 0 )
  {
    log_handle = __atxlog_handle_default();
    log_obj = MEMORY[0x22DA02F60](log_handle);
    is_log_enabled = MEMORY[0x22DA03180](log_obj, 0);
    if ( (_DWORD)is_log_enabled )
    {
      n_v10[0] = 0;
      is_log_enabled = MEMORY[0x22DA026F0](
                         &dword_22B164000,
                         log_obj,
                         0,
                         "ATXNotificationAndSuggestionDatabase: Purging private notification streams to remove persisted text content",
                         n_v10,
                         2);
    }
    MEMORY[0x22DA02E90](is_log_enabled);
    deleteAllEvents = objc_msgSend((id)MEMORY[0x22DA02E00](off_2792D3F78), "deleteAllEvents");
    MEMORY[0x22DA02E90](deleteAllEvents);
    deleteAllEvents_2 = objc_msgSend((id)MEMORY[0x22DA02E00](MEMORY[0x27899F330]), "deleteAllEvents");
    MEMORY[0x22DA02E90](deleteAllEvents_2);
    deleteAllEvents_3 = objc_msgSend((id)MEMORY[0x22DA02E00](MEMORY[0x27899F038]), "deleteAllEvents");
    MEMORY[0x22DA02E90](deleteAllEvents_3);
    boolForKey = objc_msgSend(notificationPrefs, "setBool:forKey:", 1, purgeEnabled);
  }
  return MEMORY[0x22DA02E60](boolForKey);
}
```

The implementation adds a new method, `-[ATXNotificationAndSuggestionDatabase _purgeNotificationBiomeStreamsIfNeeded]`. 
This method checks a specific boolean flag in `NSUserDefaults` (using a specific suite name) to determine if the purge has already been completed. The flag corresponds to the newly added symbol `__kATXBiomeNotificationPurgeCompleteKey`.
If the flag is not set (indicating the purge hasn't happened yet), the method logs a message: "ATXNotificationAndSuggestionDatabase: Purging private notification streams to remove persisted text content".
It then retrieves three distinct Biome stream instances (representing different notification event streams) and calls `deleteAllEvents` on each of them.
After successfully clearing the events, it sets the boolean flag to true in `NSUserDefaults` to ensure this purge operation only occurs once per device.

## How to trigger this feature
This feature is likely triggered automatically during the initialization or routine maintenance tasks of the `ATXNotificationAndSuggestionDatabase` (e.g., when the daemon starts up or when the database is first accessed after the firmware update). The `_purgeNotificationBiomeStreamsIfNeeded` method is called, and it executes the purge if the completion flag is not found in the user defaults.

## Vulnerability Assessment
This change appears to be a privacy-related mitigation rather than a traditional memory corruption fix. The explicit mention of "remove persisted text content" from "private notification streams" strongly suggests that notification content (which can contain highly sensitive personal information, such as messages, 2FA codes, or private alerts) was being logged or persisted in Biome streams when it shouldn't have been, or was not being properly expired.
If left unpatched, this could lead to a local privacy leak where an attacker with physical access to the device (or another process with access to the Biome streams) could extract sensitive notification text that the user believed was ephemeral or already dismissed. 
Because it addresses the unauthorized persistence of sensitive user data, this is a high-priority privacy fix.

## Evidence
- **Added Symbols**: `-[ATXNotificationAndSuggestionDatabase _purgeNotificationBiomeStreamsIfNeeded]`, `__kATXBiomeNotificationPurgeCompleteKey`
- **Added Strings**: `"ATXNotificationAndSuggestionDatabase: Purging private notification streams to remove persisted text content"`, `"_purgeNotificationBiomeStreamsIfNeeded"`
- **Decompilation**: The decompiled `_purgeNotificationBiomeStreamsIfNeeded` function clearly shows the check-and-purge logic using `NSUserDefaults` and `deleteAllEvents` on three objects.

## AI Prioritisation Scoring System

- **Decompilation and string analysis**
  - **Tier**: TIER_1
  - **Category**: Privacy/Data Leak
  - **Reasoning**: The update introduces a one-time purge of private notification Biome streams to remove persisted text content. This indicates a mitigation for a privacy vulnerability where sensitive notification data was improperly stored or retained.

