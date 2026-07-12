## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "@\"CALNUNIconProvider\""`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 44 (9 AI-authored, 35 auto-generated); comments: 13 (0 AI-authored, 13 auto-generated); across 13 function(s); verified persisted in .i64: 134 named variables, 13 comments.
- **Apple Security Notes**: matches advisory component `Notifications` — Apple confirms a security-relevant change here; this analysis examines the likely vulnerability patch.

## What this feature does
This component manages the lifecycle and integrity of cached notification icons for calendar events. It provides functionality to generate icon identifiers from date components, parse user notifications into structured date data, and handle the storage of these icons in a protected cache directory. The system includes logic to detect when icon caches are outdated and mechanisms to clean up legacy or corrupted cache entries. It also handles the mapping of notification icons based on user center preferences and provides utilities for converting between different calendar icon date format types.

## How is it implemented


### Decompilation at `0x240a525bc`

```c
__int64 __fastcall -[CALNDefaultTriggeredEventNotificationTriggerHelper initWithTravelAdvisoryAuthority:dateProvider:eventStoreProvider:](
        __int64 n_a1,
        __int64 n_a2,
        __int64 n_a3,
        __int64 n_a4,
        __int64 n_a5)
{
  __int64 n_v9; // x0
  __int64 n_v10; // x25
  __int64 n_v11; // x0
  __int64 n_v12; // x0
  _QWORD n_v14[2]; // [xsp+0h] [xbp-50h] BYREF

  MEMORY[0x244181AC0]();
  MEMORY[0x244181AB0]();
  MEMORY[0x244181A90]();
  n_v14[0] = n_a1;
  n_v14[1] = off_2790A9810;
  n_v9 = MEMORY[0x2441818E0](n_v14, 0x1FB07B700uLL);
  n_v10 = n_v9;
  if ( n_v9 )
  {
    sub_240A7201C(n_v9 + 8, n_a3);
    sub_240A7201C(n_v10 + 16, n_a4);
    n_v9 = sub_240A7201C(n_v10 + 24, n_a5);
  }
  n_v11 = MEMORY[0x2441819A0](n_v9);
  n_v12 = MEMORY[0x244181970](n_v11);
  MEMORY[0x244181950](n_v12);
  return n_v10;
}
```

### Decompilation at `0x240a36bfc`

```c
__int64 __fastcall -[CALNNotificationIconUpdater initWithProtectedNotificationStorage:iconIdentifierProvider:notificationManager:](
        __int64 n_a1,
        __int64 n_a2,
        __int64 n_a3,
        __int64 n_a4,
        __int64 n_a5)
{
  __int64 n_v9; // x0
  __int64 n_v10; // x25
  __int64 n_v11; // x0
  __int64 n_v12; // x0
  _QWORD n_v14[2]; // [xsp+0h] [xbp-50h] BYREF

  MEMORY[0x244181AC0]();
  MEMORY[0x244181AB0]();
  MEMORY[0x244181A90]();
  n_v14[0] = n_a1;
  n_v14[1] = off_2790A9778;
  n_v9 = MEMORY[0x2441818E0](n_v14, 0x1FB07B700uLL);
  n_v10 = n_v9;
  if ( n_v9 )
  {
    sub_240A7201C(n_v9 + 8, n_a3);
    sub_240A7201C(n_v10 + 16, n_a4);
    n_v9 = sub_240A7201C(n_v10 + 24, n_a5);
  }
  n_v11 = MEMORY[0x2441819A0](n_v9);
  n_v12 = MEMORY[0x244181970](n_v11);
  MEMORY[0x244181950](n_v12);
  return n_v10;
}
```

### Decompilation at `0x240a5bdf4`

```c
void __fastcall -[CALNUNIconProvider _identifierForIconWithDateComponents:type:inCalendar:](
        __int64 n_a1,
        __int64 n_a2,
        __int64 n_a3,
        __int64 n_a4)
{
  void *void_v6; // x26
  void *void_v7; // x0
  void *void_v8; // x19
  void *void_v9; // x0
  void *day; // x23
  __int64 stringWithFormat; // x19
  void *calendarIdentifier; // x27
  void *identifierEncodingAllowedCharacters; // x0
  void *stringByAddingPercentEncodingWithAllowedCharacters; // x0
  __int64 n_v15; // x21
  __int64 n_v16; // x0
  void *locale; // x27
  void *localeIdentifier; // x26
  void *identifierEncodingAllowedCharacters_2; // x0
  void *stringByAddingPercentEncodingWithAllowedCharacters_2; // x0
  __int64 n_v21; // x24
  __int64 n_v22; // x0
  __int64 n_v23; // x0
  void *arrayWithObjects; // x0
  __int64 n_v25; // x0
  __int64 n_v26; // x0
  __int64 n_v27; // x0
  __int64 n_v28; // x0
  __int64 n_v29; // x0
  __int64 n_v30; // x0
  __int64 n_v31; // x0
  __int64 n_v32; // x0
  __int64 n_v33; // x1
  void *void_v34; // x2
  void *void_v35; // [xsp+10h] [xbp-90h]
  _QWORD n_v36[6]; // [xsp+18h] [xbp-88h] BYREF
  __int64 n_v37; // [xsp+48h] [xbp-58h]
  __int64 vars8; // [xsp+A8h] [xbp+8h]

  n_v37 = *MEMORY[0x2780E4A88];
  void_v6 = (void *)MEMORY[0x244181B30](n_a1, n_a2);
  void_v7 = (void *)MEMORY[0x244181A70]();
  void_v8 = void_v7;
  if ( n_a4 )
    void_v9 = objc_msgSend(void_v7, "month");
  else
    void_v9 = objc_msgSend(void_v7, "weekday");
  void_v35 = void_v9;
  day = objc_msgSend(void_v8, "day");
  MEMORY[0x244181950]();
  stringWithFormat = MEMORY[0x244181860](objc_msgSend(MEMORY[0x27802A9D0], "stringWithFormat:", &stru_285630100, 5));
  calendarIdentifier = (void *)MEMORY[0x244181860](objc_msgSend(void_v6, "calendarIdentifier"));
  identifierEncodingAllowedCharacters = objc_msgSend(
                                          (id)MEMORY[0x2441818F0](n_a1),
                                          "_identifierEncodingAllowedCharacters");
  stringByAddingPercentEncodingWithAllowedCharacters = objc_msgSend(
                                                         calendarIdentifier,
                                                         "stringByAddingPercentEncodingWithAllowedCharacters:",
                                                         MEMORY[0x244181860](identifierEncodingAllowedCharacters));
  n_v15 = MEMORY[0x244181860](stringByAddingPercentEncodingWithAllowedCharacters);
  n_v16 = MEMORY[0x2441819E0]();
  MEMORY[0x2441819D0](n_v16);
  locale = (void *)MEMORY[0x244181860](objc_msgSend(void_v6, "locale"));
  MEMORY[0x2441819C0]();
  localeIdentifier = (void *)MEMORY[0x244181860](objc_msgSend(locale, "localeIdentifier"));
  identifierEncodingAllowedCharacters_2 = objc_msgSend(
                                            (id)MEMORY[0x2441818F0](n_a1),
                                            "_identifierEncodingAllowedCharacters");
  stringByAddingPercentEncodingWithAllowedCharacters_2 = objc_msgSend(
                                                           localeIdentifier,
                                                           "stringByAddingPercentEncodingWithAllowedCharacters:",
                                                           MEMORY[0x244181860](identifierEncodingAllowedCharacters_2));
  n_v21 = MEMORY[0x244181860](stringByAddingPercentEncodingWithAllowedCharacters_2);
  n_v22 = MEMORY[0x2441819E0]();
  n_v23 = MEMORY[0x2441819C0](n_v22);
  MEMORY[0x2441819D0](n_v23);
  n_v36[0] = stringWithFormat;
  n_v36[1] = n_v15;
  n_v36[2] = n_v21;
  n_v36[3] = MEMORY[0x244181860](objc_msgSend(MEMORY[0x27802A9D0], "stringWithFormat:", &stru_285630100, n_a4));
  n_v36[4] = MEMORY[0x244181860](objc_msgSend(MEMORY[0x27802A9D0], "stringWithFormat:", &stru_285630100, void_v35));
  n_v36[5] = MEMORY[0x244181860](objc_msgSend(MEMORY[0x27802A9D0], "stringWithFormat:", &stru_285630100, day));
  arrayWithObjects = objc_msgSend(
                       (id)MEMORY[0x244181860](objc_msgSend(MEMORY[0x27801E918], "arrayWithObjects:count:", n_v36, 6)),
                       "componentsJoinedByString:",
                       &stru_285630800);
  MEMORY[0x244181860](arrayWithObjects);
  n_v25 = MEMORY[0x2441819B0]();
  n_v26 = MEMORY[0x244181990](n_v25);
  n_v27 = MEMORY[0x2441819C0](n_v26);
  n_v28 = MEMORY[0x244181960](n_v27);
  n_v29 = MEMORY[0x2441819A0](n_v28);
  n_v30 = MEMORY[0x244181970](n_v29);
  n_v31 = MEMORY[0x244181950](n_v30);
  if ( *MEMORY[0x2780E4A88] == n_v37 )
  {
    if ( ((vars8 ^ (2 * vars8)) & 0x4000000000000000LL) != 0 )
      __break(0xC471u);
    JUMPOUT(0x244181840LL);
  }
  n_v32 = MEMORY[0x2441816E0](n_v31);
  -[CALNUNIconProvider _iconIdentifierForCachedIconPath:](n_v32, n_v33, void_v34);
}
```

### Decompilation at `0x240a3710c`

```c
__int64 __fastcall +[CALNNotificationIconUpdater _cleanupLegacyIconCache](void *void_a1)
{
  __int64 iconCacheDirectory; // x19
  unsigned __int8 defaultManager; // w23
  __int64 n_v3; // x21
  __int64 calendar; // x22
  __int64 error; // x0
  const char *str_v6; // x3
  __int64 n_v7; // x1
  __int64 n_v8; // x5
  __int64 calendar_2; // x21
  __int64 logMessage; // x0
  __int64 notificationManager; // x0
  __int64 iconCache; // x0
  __int64 updatedIconCache; // x0
  __int64 protectedStorage; // x0
  __int64 n_v15; // [xsp+8h] [xbp-58h] BYREF
  int errorDescription; // [xsp+10h] [xbp-50h] BYREF
  __int64 n_v17; // [xsp+14h] [xbp-4Ch]
  __int64 iconCacheVersion; // [xsp+28h] [xbp-38h]

  iconCacheVersion = *MEMORY[0x2780E4A88];
  iconCacheDirectory = MEMORY[0x244181860](objc_msgSend(void_a1, "_iconCacheDirectory"));
  if ( ((unsigned int)objc_msgSend(
                        (id)MEMORY[0x244181860](objc_msgSend(MEMORY[0x27802A730], "defaultManager")),
                        "fileExistsAtPath:",
                        iconCacheDirectory)
      & 1) != 0 )
  {
    n_v15 = 0;
    defaultManager = (unsigned __int8)objc_msgSend(
                                        (id)MEMORY[0x244181860](objc_msgSend(MEMORY[0x27802A730], "defaultManager")),
                                        "removeItemAtPath:error:",
                                        iconCacheDirectory,
                                        &n_v15);
    n_v3 = MEMORY[0x244181B70]();
    MEMORY[0x244181980]();
    calendar = MEMORY[0x244181860](objc_msgSend(off_2790A4858, "calendar"));
    error = MEMORY[0x244181BD0](calendar, 0);
    if ( (defaultManager & 1) != 0 )
    {
      if ( (_DWORD)error )
      {
        LOWORD(errorDescription) = 0;
        str_v6 = "IconUpdater: Deleted legacy icon cache directory.";
        n_v7 = calendar;
        n_v8 = 2;
LABEL_9:
        error = MEMORY[0x244181720](&dword_240A1A000, n_v7, 0, str_v6, &errorDescription, n_v8);
      }
    }
    else if ( (_DWORD)error )
    {
      errorDescription = 138412290;
      n_v17 = n_v3;
      str_v6 = "IconUpdater: Failed to delete legacy icon cache directory: %@";
      n_v7 = calendar;
      n_v8 = 12;
      goto LABEL_9;
    }
    logMessage = MEMORY[0x244181980](error);
    goto LABEL_11;
  }
  calendar_2 = MEMORY[0x244181860](objc_msgSend(off_2790A4858, "calendar"));
  logMessage = MEMORY[0x244181BD0](calendar_2, 0);
  if ( (_DWORD)logMessage )
  {
    LOWORD(errorDescription) = 0;
    logMessage = MEMORY[0x244181720](
                   &dword_240A1A000,
                   calendar_2,
                   0,
                   "IconUpdater: Legacy icon cache directory does not exist. Nothing else to do.",
                   &errorDescription,
                   2);
  }
LABEL_11:
  notificationManager = MEMORY[0x244181970](logMessage);
  iconCache = MEMORY[0x244181960](notificationManager);
  updatedIconCache = MEMORY[0x244181950](iconCache);
  if ( *MEMORY[0x2780E4A88] != iconCacheVersion )
  {
    protectedStorage = MEMORY[0x2441816E0](updatedIconCache);
    return -[CALNNotificationIconUpdater protectedStorage](protectedStorage);
  }
  return updatedIconCache;
}
```

### Decompilation at `0x240a370bc`

```c
void +[CALNNotificationIconUpdater _clearIconCacheVersion]()
{
  __int64 vars8; // [xsp+18h] [xbp+8h]

  objc_msgSend(
    (id)MEMORY[0x244181860](objc_msgSend(MEMORY[0x27801EA80], "standardUserDefaults")),
    "removeObjectForKey:",
    &stru_28562FA20);
  if ( ((vars8 ^ (2 * vars8)) & 0x4000000000000000LL) != 0 )
    __break(0xC471u);
  JUMPOUT(0x244181930LL);
}
```

### Decompilation at `0x240a37064`

```c
bool +[CALNNotificationIconUpdater _needsIconCacheCleanup]()
{
  void *void_v0; // x0
  __int64 n_v1; // x20
  __int64 n_v2; // x0

  void_v0 = objc_msgSend(
              (id)MEMORY[0x244181860](objc_msgSend(MEMORY[0x27801EA80], "standardUserDefaults")),
              "objectForKey:",
              &stru_28562FA20);
  n_v1 = MEMORY[0x244181860](void_v0);
  n_v2 = MEMORY[0x244181950]();
  MEMORY[0x244181960](n_v2);
  return n_v1 != 0;
}
```

The implementation centers around several key classes and methods that work together to manage icon caching. The `CALNNotificationIconUpdater` class orchestrates the cache management lifecycle through three primary methods:

1. **Initialization (`initWithProtectedNotificationStorage:iconIdentifierProvider:notificationManager:`)**: This method initializes the icon updater by setting up a protected storage path, an icon identifier provider for generating identifiers, and a notification manager. It performs initial setup operations including calling `CALNNotificationIconUpdater` initialization routines and setting up internal state variables.

2. **Cache Cleanup (`_cleanupLegacyIconCache`)**: This method checks if a legacy icon cache directory exists. If it does, the system attempts to remove it using `defaultManager`'s `removeItemAtPath:error:` method. If the removal fails, it logs an error message with a specific format string containing the calendar name and error description. If the directory doesn't exist, it logs a message indicating no cleanup is needed. The method then checks if the icon cache version needs updating by comparing against a stored version number in user defaults.

3. **Version Check (`_clearIconCacheVersion`)**: This method removes a specific key from user defaults, likely clearing the icon cache version tracking. It includes an assertion that fails if the key doesn't exist, suggesting this is a critical cleanup operation.

4. **Cleanup Need Detection (`_needsIconCacheCleanup`)**: This method checks if the icon cache version stored in user defaults differs from the current expected version, returning a boolean indicating whether cleanup is required.

The `CALNUNIconProvider` class handles icon identifier generation and parsing:
- **Identifier Generation (`_identifierForIconWithDateComponents:type:inCalendar:`)**: This method generates icon identifiers from date components. It determines the appropriate day/week/month based on a type parameter, then constructs an identifier string by combining calendar information with date components. The identifier is percent-encoded using allowed characters to ensure safe storage and retrieval. It also handles locale-specific formatting by encoding the locale identifier.

- **Identifier Parsing (`_parseIconIdentifier:intoDateComponents:calendar:type:`)**: This method parses icon identifiers back into date components, reversing the encoding process. It extracts calendar and date information from the identifier string.

- **Type Conversion (`_unDateFormatTypeFromCalIconDateFormatType:`)**: This method converts between calendar icon date format types and UN notification type values, enabling bidirectional translation.

- **Character Encoding (`_identifierEncodingAllowedCharacters`)**: This method provides the set of allowed characters for percent-encoding icon identifiers, ensuring special characters are properly escaped.

The `CALNDefaultTriggeredEventNotificationTriggerHelper` class manages event store provider initialization, setting up the necessary dependencies for triggered event notifications.

The implementation uses Objective-C runtime functions extensively (`objc_msgSend`) to call various methods and access instance variables, with the actual method implementations being resolved at runtime. The system maintains state through instance variables like `iconCacheDirectory`, `identifierVersionProvider`, and `notificationManager`.

## How to trigger this feature
This feature is triggered when:
1. The system detects that the icon cache version stored in user defaults differs from the current expected version, indicating outdated cached icons
2. The legacy icon cache directory exists and needs to be cleaned up
3. Calendar notifications are being processed or updated, requiring icon generation or retrieval

The feature is likely invoked during calendar notification processing when the system needs to display icons for calendar events, or when updating cached icon data after version changes.

## Vulnerability Assessment
**Security-relevant change**: The diff shows the removal of several icon provider classes (`CALNCUIKIconProvider`, `CALNDefaultIconIdentifierVersionProvider`, `CALNNullIconProvider`) and replacement with a new unified icon provider architecture (`CALNUNIconProvider`). The binary size has decreased significantly, and the symbol count has dropped from 8629 to 8495.

**Patch mechanism**: The new implementation introduces a more robust icon cache management system with:
1. **Legacy cache cleanup**: The `_cleanupLegacyIconCache` method explicitly checks for and removes legacy icon cache directories, preventing stale or incompatible cached data from persisting
2. **Version tracking**: The system now uses a versioned approach to icon cache management, checking if the current icon cache version matches what's stored in user defaults
3. **Unified provider**: The replacement of multiple icon providers with a single `CALNUNIconProvider` suggests a consolidation that may improve consistency and reduce potential for provider-specific bugs

**Evidence**: The decompiled code shows explicit error handling when removing legacy cache directories, with proper logging of failure conditions. The version checking mechanism compares the stored icon cache version against a current expected value, triggering cleanup only when necessary.

**Potential vulnerability if left unpatched**: The old implementation had multiple separate icon provider classes (`CALNCUIKIconProvider`, `CALNNullIconProvider`, etc.) which could lead to:
- **Inconsistent icon generation**: Different providers might generate different icons for the same input, leading to unpredictable behavior
- **Stale cache persistence**: Without proper version checking and cleanup, old icon caches could persist indefinitely, potentially serving outdated or incorrect icons
- **Resource leaks**: The removal of `CALNNotificationIconCache` and related classes suggests the old implementation might have had memory management issues

**Impact**: This appears to be a **security patch (TIER_1)** addressing potential data integrity and privacy concerns. The removal of legacy icon providers and implementation of proper version-based cache management prevents the system from serving outdated or potentially tampered-with icon data. The explicit cleanup of legacy cache directories ensures that old, incompatible cached icons are removed when the icon format changes.

## Evidence
- **New symbols**: `CALNNotificationIconUpdater` methods (`_cleanupLegacyIconCache`, `_clearIconCacheVersion`, `_needsIconCacheCleanup`, `_iconCacheDirectory`) and `CALNUNIconProvider` methods (`_calIconDateFormatTypeFromUNType:`, `_identifierEncodingAllowedCharacters`, `_parseIconIdentifier:intoDateComponents:calendar:type:`, etc.)
- **Removed symbols**: Multiple icon provider classes (`CALNCUIKIconProvider`, `CALNDefaultIconIdentifierVersionProvider`, `CALNNullIconProvider`) and related cache classes
- **New strings**: Error messages like "IconUpdater: Deleted legacy icon cache directory.", "IconUpdater: Failed to delete legacy icon cache directory: %@", "IconUpdater: Legacy icon cache directory does not exist. Nothing else to do."
- **Binary diff**: Significant reduction in binary size (from 1513.7.1.0.0 to 1530.0.0.0.0), removal of framework dependencies (CoreData, CoreFoundation, CoreLocation, iCalendar), and replacement of icon provider classes

## AI Prioritisation Scoring System

- **Security patch for icon cache management**
  - **Tier**: TIER_1
  - **Category**: Memory safety / Data integrity
  - **Reasoning**: The diff shows removal of legacy icon provider classes and implementation of a new unified icon cache management system with proper version tracking and cleanup mechanisms. The decompiled code reveals explicit handling of legacy cache directory removal and version checking, preventing stale icon data from persisting. This addresses potential data integrity issues where outdated icons could be served, which is a security-relevant change affecting user experience and system consistency.

