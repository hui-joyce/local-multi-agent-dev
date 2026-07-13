## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "&G3"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 2 (2 AI-authored, 0 auto-generated); comments: 8 (2 AI-authored, 6 auto-generated); across 6 function(s); verified persisted in .i64: 22 named variables, 6 comments.

## What this feature does
This update introduces a major privacy enhancement to the `AppPredictionClient` framework by removing the storage and transmission of raw notification text. In previous versions, notification-related classes (`ATXPBUserNotification` and `ATXUserNotification`) stored the actual `NSString` content of a notification's title, subtitle, and body. This update completely removes those string properties and replaces them with integer properties that only record the lengths of the text (`titleLength`, `subtitleLength`, and `bodyLength`). Additionally, it introduces new methods to delete all events from specific notification-related Biome streams (`ATXMissedNotificationRankingBiomeStream` and `ATXUserNotificationDigestBiomeStream`).

## How is it implemented


### Decompilation at `0x1c19806b8`

```c
void *__fastcall -[ATXFaceGalleryBiomeStream deleteAllEvents](__int64 self)
{
  return objc_msgSend(*(id *)(self + 8), "pruneWithPredicateBlock:", &__block_literal_global_5);
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

### Decompilation at `0x1c194a834`

```c
__int64 __fastcall -[ATXUserNotification bodyLength](__int64 n_a1)
{
  return *(_QWORD *)(n_a1 + 88);
}
```

### Decompilation at `0x1c19cb2d4`

```c
__int64 __fastcall -[ATXPBUserNotification setBodyLength:](__int64 result, __int64 n_a2, __int64 bodyLength)
{
  *(_DWORD *)(result + 216) |= 4u;
  *(_QWORD *)(result + 24) = bodyLength;
  return result;
}
```

### Decompilation at `0x1c1963a38`

```c
__int64 __fastcall -[ATXAppModeEntity jsonDict](id *id_a1)
{
  __int64 identifier; // x19
  __int64 n_v3; // x20
  void *scoreMetadata; // x0
  __int64 n_v5; // x22
  __int64 n_v6; // x23
  __int64 firstObject; // x25
  __int64 n_v8; // x26
  __int64 n_v9; // x0
  __int64 n_v10; // x0
  __int64 n_v11; // x0
  __int64 n_v12; // x0
  __int64 n_v13; // x0
  _QWORD n_v15[3]; // [xsp+8h] [xbp-78h] BYREF
  _QWORD n_v16[3]; // [xsp+20h] [xbp-60h] BYREF
  __int64 n_v17; // [xsp+38h] [xbp-48h]
  __int64 vars8; // [xsp+88h] [xbp+8h]

  n_v17 = *MEMORY[0x1E6782818];
  n_v15[0] = &stru_1F40E71F8;
  identifier = MEMORY[0x1C6166B00](objc_msgSend(id_a1, "identifier"));
  n_v3 = identifier;
  if ( !identifier )
    n_v3 = MEMORY[0x1C6166B00](objc_msgSend(MEMORY[0x1E66FA2A8], "null"));
  n_v16[0] = n_v3;
  n_v15[1] = &stru_1F40E7218;
  scoreMetadata = objc_msgSend((id)MEMORY[0x1C6166B00](objc_msgSend(id_a1, "scoreMetadata")), "jsonDict");
  n_v5 = MEMORY[0x1C6166B00](scoreMetadata);
  n_v6 = n_v5;
  if ( !n_v5 )
    n_v6 = MEMORY[0x1C6166B00](objc_msgSend(MEMORY[0x1E66FA2A8], "null"));
  n_v16[1] = n_v6;
  n_v15[2] = &stru_1F40E7238;
  firstObject = MEMORY[0x1C6166B00](objc_msgSend(id_a1[3], "firstObject"));
  n_v8 = firstObject;
  if ( !firstObject )
    n_v8 = MEMORY[0x1C6166B00](objc_msgSend(MEMORY[0x1E66FA2A8], "null"));
  n_v16[2] = n_v8;
  MEMORY[0x1C6166B00](objc_msgSend(MEMORY[0x1E66FA218], "dictionaryWithObjects:forKeys:count:", n_v16, n_v15, 3));
  if ( !firstObject )
    MEMORY[0x1C6166A90]();
  n_v9 = MEMORY[0x1C6166A80]();
  if ( !n_v5 )
    n_v9 = MEMORY[0x1C6166A60](n_v9);
  n_v10 = MEMORY[0x1C6166A50](n_v9);
  n_v11 = MEMORY[0x1C6166A40](n_v10);
  if ( !identifier )
    n_v11 = MEMORY[0x1C6166A30](n_v11);
  n_v12 = MEMORY[0x1C6166A10](n_v11);
  if ( *MEMORY[0x1E6782818] == n_v17 )
  {
    if ( ((vars8 ^ (2 * vars8)) & 0x4000000000000000LL) != 0 )
      __break(0xC471u);
    JUMPOUT(0x1C6166910LL);
  }
  n_v13 = MEMORY[0x1C6166450](n_v12);
  return -[ATXAppModeEntity debugDescription](n_v13);
}
```

The implementation fundamentally changes the data structures used for notification prediction and logging. The `NSString` properties for `title`, `subtitle`, and `body` have been removed and replaced with 64-bit unsigned integers (`unsigned long long`). 

The decompiled code for `-[ATXPBUserNotification setBodyLength:]` demonstrates this new behavior: it takes the 64-bit integer length, stores it directly into the instance variable at offset `24`, and updates a bitfield at offset `216` (using a bitwise OR operation `|= 4u`) to flag that the `bodyLength` field has been set. The getter `-[ATXUserNotification bodyLength]` simply retrieves this 64-bit integer. The Protobuf `has` bitfield struct signature was also updated to reflect these new length-based flags instead of the old string-based flags.

Furthermore, the newly added `deleteAllEvents` methods (which share identical code folding in the binary) are implemented by invoking `pruneWithPredicateBlock:` on the underlying Biome stream object. This allows the system to systematically purge all stored notification events from the stream.

## How to trigger this feature
This feature is triggered automatically by the iOS system when processing, logging, or generating machine learning predictions based on user notifications. When a notification arrives, the App Prediction subsystem now extracts and stores only the character counts of the text fields rather than the text itself. The `deleteAllEvents` functionality is likely triggered during user-initiated privacy resets (e.g., clearing Siri & Search history) or during routine system data retention pruning.

## Vulnerability Assessment
This change is a proactive privacy and security mitigation designed to prevent Information Disclosure. By storing raw notification text, previous versions risked leaking highly sensitive user information—such as personal messages, two-factor authentication (2FA) codes, or private emails—into system logs, Biome streams, or on-disk databases. These stores could potentially be accessed by other processes, extracted during diagnostics collection, or exposed if a separate sandbox escape vulnerability were exploited.

By replacing the raw text with integer lengths, Apple preserves the metadata necessary for machine learning models (e.g., predicting user engagement based on the size of a message) while completely eliminating the risk of exposing the actual content. The addition of `deleteAllEvents` further strengthens the data lifecycle management, ensuring that any residual notification metadata can be securely wiped. If left unpatched, the older implementation would continue to pose a systemic privacy risk by unnecessarily persisting sensitive user data.

## AI Prioritisation Scoring System

- **Diff Analysis & Decompilation**
  - **Tier**: TIER_1
  - **Category**: Privacy Enhancement / Information Disclosure Mitigation
  - **Reasoning**: Removes raw notification text (title, subtitle, body) from AppPrediction models and replaces them with lengths, mitigating a significant privacy and information disclosure risk where sensitive notification content could be logged or stored in Biome streams.

