## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "T@\"NSDate\",&,N,V_assocWhenNotChargingStartTime"`
- **Analysis mode**: decompiled
- **Database annotations** -- variable renames: 20 (0 AI-authored, 20 auto-generated); comments: 9 (0 AI-authored, 9 auto-generated); across 9 function(s); verified persisted in .i64: 20 named variables, 9 comments.
- **Apple Security Notes**: matches advisory component `Wi-Fi` -- Apple confirms a security-relevant change here; this analysis examines the likely vulnerability patch.

## What this feature does
The `WiFiPolicy` framework introduced a new class, `WiFiUsageSession`, which tracks WiFi usage duration segmented by the device's charging state. This feature allows the system to distinguish between WiFi activity when the device is plugged in versus when it is on battery power. The class maintains four key properties: `assocWhenNotChargingStartTime`, `assocWhileChargingStartTime`, `assocWhenNotChargingDuration`, and `assocWhileChargingDuration`. It also tracks the current charging state via the boolean property `isDeviceCharging`. The new method `tallyAssocDurationWithChargingState` appears to be the core logic responsible for calculating or updating these duration metrics based on the current charging state, likely by comparing timestamps and accumulating time spent in each state.

## How is it implemented


### Decompilation at `0x239ad5d4c`

```c
double __fastcall -[WiFiUsageSession assocWhenNotChargingDuration](__int64 n_a1)
{
  return *(double *)(n_a1 + 9680);
}
```

### Decompilation at `0x239ad5cf4`

```c
__int64 __fastcall -[WiFiUsageSession assocWhenNotChargingStartTime](__int64 n_a1)
{
  return *(_QWORD *)(n_a1 + 9664);
}
```

### Decompilation at `0x239ac9aa8`

```c
void __fastcall -[WiFiUsageSession tallyAssocDurationWithChargingState](__int64 n_a1)
{
  __int64 n_v2; // x20
  void *date; // x0
  void *timeIntervalSinceDate; // x0
  double flt_v5; // d0
  void *timeIntervalSinceDate_2; // x0
  double flt_v7; // d0
  double flt_v8; // d0
  double flt_v9; // d0
  void *void_v10; // [xsp+8h] [xbp-18h]
  void *void_v11; // [xsp+8h] [xbp-18h]
  __int64 vars8; // [xsp+28h] [xbp+8h]

  n_v2 = n_a1 + 0x2000;
  date = (void *)MEMORY[0x23A1F5150](objc_msgSend(MEMORY[0x278392A48], "date"));
  if ( *(_BYTE *)(n_v2 + 1000) == 1 )
  {
    if ( !*(_BYTE *)(n_v2 + 994) )
    {
      if ( !*(_QWORD *)(n_a1 + 9656) )
        goto LABEL_17;
      objc_msgSend(date, "timeIntervalSinceDate:");
      *(double *)(n_a1 + 9672) = flt_v8 + *(double *)(n_a1 + 9672);
      *(_QWORD *)(n_a1 + 9656) = 0;
      goto LABEL_16;
    }
    void_v10 = date;
    if ( *(_QWORD *)(n_a1 + 9664) )
    {
      timeIntervalSinceDate = objc_msgSend(date, "timeIntervalSinceDate:");
      *(double *)(n_a1 + 9680) = flt_v5 + *(double *)(n_a1 + 9680);
      *(_QWORD *)(n_a1 + 9664) = 0;
      MEMORY[0x23A1F5110](timeIntervalSinceDate);
    }
    if ( !*(_QWORD *)(n_a1 + 9656) )
    {
      MEMORY[0x23A1F5130](void_v10);
      *(_QWORD *)(n_a1 + 9656) = void_v10;
LABEL_16:
      MEMORY[0x23A1F5110]();
    }
  }
  else
  {
    if ( !*(_BYTE *)(n_v2 + 994) )
    {
      if ( !*(_QWORD *)(n_a1 + 9664) )
        goto LABEL_17;
      objc_msgSend(date, "timeIntervalSinceDate:");
      *(double *)(n_a1 + 9680) = flt_v9 + *(double *)(n_a1 + 9680);
      *(_QWORD *)(n_a1 + 9664) = 0;
      goto LABEL_16;
    }
    void_v11 = date;
    if ( *(_QWORD *)(n_a1 + 9656) )
    {
      timeIntervalSinceDate_2 = objc_msgSend(date, "timeIntervalSinceDate:");
      *(double *)(n_a1 + 9672) = flt_v7 + *(double *)(n_a1 + 9672);
      *(_QWORD *)(n_a1 + 9656) = 0;
      MEMORY[0x23A1F5110](timeIntervalSinceDate_2);
    }
    if ( !*(_QWORD *)(n_a1 + 9664) )
    {
      MEMORY[0x23A1F5130](void_v11);
      *(_QWORD *)(n_a1 + 9664) = void_v11;
      goto LABEL_16;
    }
  }
LABEL_17:
  if ( ((vars8 ^ (2 * vars8)) & 0x4000000000000000LL) != 0 )
    __break(0xC471u);
  JUMPOUT(0x23A1F5040LL);
}
```

The implementation centers around the `WiFiUsageSession` class, which was added in this update. The class exposes several accessor methods (`assocWhenNotChargingDuration`, `assocWhileChargingDuration`, `isDeviceCharging`) and mutator methods (`setAssocWhenNotChargingDuration:`, `setAssocWhileChargingDuration:`, `setIsDeviceCharging:`) to manage the session state. The critical function, `tallyAssocDurationWithChargingState`, is responsible for the core logic. Based on the symbol names and the presence of `NSDate` types in the property declarations, this function likely takes a timestamp or duration input and updates the `assocWhenNotChargingDuration` and `assocWhileChargingDuration` properties by comparing them against the current time or a provided reference time, while checking the `isDeviceCharging` flag to determine which bucket the current usage falls into. The decompiled code would show logic branching on `isDeviceCharging` to increment the appropriate duration counter. The class is implemented in Objective-C, utilizing standard property storage and method dispatching (`objc_msgSend`).

## How to trigger this feature
This feature is triggered by the creation of a `WiFiUsageSession` object, which happens when the system begins tracking WiFi usage. The session is likely instantiated as part of the broader WiFi policy management subsystem when a connection event occurs or at specific intervals. The `tallyAssocDurationWithChargingState` method is called periodically (e.g., on a timer or connection event) to update the duration counters. The trigger for the *feature* (the tracking of segmented WiFi usage) is effectively the presence of the `WiFiUsageSession` class itself and its integration into the WiFi policy framework's lifecycle. The specific invocation of `tallyAssocDurationWithChargingState` would be triggered by system events related to WiFi activity (e.g., connection, disconnection, or periodic polling).

## Vulnerability Assessment
This change appears to be a **functional enhancement** rather than a security patch. The introduction of `WiFiUsageSession` with charging-state-aware duration tracking is a new feature for battery usage reporting or WiFi policy optimization (e.g., to encourage/disconnect WiFi when on battery vs. charging). There is no evidence in the diff or symbol names of memory safety fixes (like bounds checking, null pointer checks, or lock acquisition/release) that would indicate a patch for Use-After-Free, Out-of-Bounds access, or Race Conditions. The new class and its methods are standard Objective-C property management and duration calculation logic. While the feature itself is benign, if it were implemented incorrectly in a broader context (e.g., if `tallyAssocDurationWithChargingState` had buffer overflows or race conditions in its implementation), it could be a vulnerability. However, based solely on the provided evidence (new class symbols and method names), no specific security vulnerability is being patched. The change to the UUID and symbol counts confirms it's a new binary component, but the nature of the symbols points to feature addition.

## Evidence
- **New Symbols**: The diff shows 11 new symbols added in Version 2 (`+` prefix) related to `WiFiUsageSession`:
    - Accessors: `-[WiFiUsageSession assocWhenNotChargingDuration]`, `-[WiFiUsageSession assocWhileChargingDuration]`, `-[WiFiUsageSession isDeviceCharging]`
    - Mutators: `-[WiFiUsageSession setAssocWhenNotChargingDuration:]`, `-[WiFiUsageSession setAssocWhileChargingDuration:]`, `-[WiFiUsageSession setIsDeviceCharging:]`
    - Core Logic: `-[WiFiUsageSession tallyAssocDurationWithChargingState]`
- **New CStrings**: Corresponding string literals for the new properties and methods are added (e.g., `"assocWhenNotChargingDuration"`, `"setIsDeviceCharging:"`).
- **New Ivars**: New instance variables are declared for the class (e.g., `_OBJC_IVAR_$_WiFiUsageSession._isDeviceCharging`).
- **Binary Diff**: The `WiFiPolicy` binary grew from 6559 to 6570 functions and 21402 to 21430 symbols, with a corresponding increase in CStrings. The `__TEXT.__text` segment grew from 0xd7bfc to 0xd7f28.
- **Removed Items**: Some old symbols (`GCC_except_table58`, `___block_literal_global.350`) and the dependency on `/System/Library/Frameworks/CFNetwork.framework/CFNetwork` were removed, but these are likely unrelated to the new `WiFiUsageSession` feature.
- **Address Resolution**: All key symbols (`assocWhenNotChargingDuration`, `tallyAssocDurationWithChargingState`, etc.) were successfully resolved to code addresses in the new binary (e.g., `0x239ad5d4c`, `0x239ac9aa8`).
- **Xrefs**: No cross-references were found for the resolved data addresses, which is expected as these are new symbols not yet widely referenced in other binaries within the scope of this specific diff analysis.

## AI Prioritisation Scoring System

- **Symbol Analysis & Feature Inference**
  - **Tier**: TIER_2
  - **Category**: Feature Addition (Battery/WiFi Policy)
  - **Reasoning**: This is a new feature addition (WiFiUsageSession class) for tracking WiFi usage based on charging state. It is not a security patch (no memory safety fixes, no privilege changes). It falls into TIER_2 as it represents a core business-logic update to the WiFi policy subsystem, likely affecting user experience (battery usage reporting) or system behavior (WiFi connection policies based on power state). It has observable runtime impact but is not critical security infrastructure.

