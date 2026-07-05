## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "%@-%@-r1"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 20 (20 AI-authored, 0 auto-generated); comments: 3 (1 AI-authored, 2 auto-generated); across 2 function(s); verified persisted in .i64: 24 named variables, 2 comments.

## What this feature does

The `IMSharedUtilities` framework update introduces a new server-side message payload processing mechanism designed to handle "server bags" (structured message metadata) and selectively strip keys based on sender identity. The two new symbols—`_IMServerBagValueForKnownSender` and `_IMSharedHelperPayloadByStrippingServerBagKeys`—indicate a shift toward sender-aware message handling.

Key evidence:
- New strings: `"known-sender"`, `"unknown-sender"`, `"Server bag set, stripping payload keys %@ for sender (known: %{BOOL}d)"` suggest the system now distinguishes between known and unknown senders when processing message payloads.
- The format string `"%@-%@-r1"` likely represents a structured identifier (e.g., `senderID-receiverID-r1`).
- The framework version bumped from `1450.500.221.2.9` to `1450.500.221.2.14`, with symbol count increasing by 2 and string count by 7, indicating a focused but non-trivial addition.
- Removal of several dylibs (`AVFoundation`, `swift_*`) and symbols suggests refactoring or consolidation, but the core functionality is additive.

This feature appears to implement a **sender-based payload filtering system** for iMessage-style shared utilities, likely used to optimize or sanitize message payloads before delivery or storage based on whether the sender is trusted/known.

## How is it implemented

### Decompiled Function: `IMServerBagValueForKnownSender`

```c
__int64 IMServerBagValueForKnownSender()
{
  __int64 server_bag_value; // x0
  __int64 mask_check; // [xsp+28h] [xbp+8h]

  sub_1A9FC0660(MEMORY[0x1E6707260]);
  server_bag_value = sub_1A9FBF540(MEMORY[0x1E673F8D0]);
  if ( ((mask_check ^ (2 * mask_check)) & 0x4000000000000000LL) != 0 )
    __break(0xC471u);
  return sub_1A9FB8BE0(server_bag_value);
}
```

### Decompiled Function: `IMSharedHelperPayloadByStrippingServerBagKeys`

```c
__int64 __fastcall IMSharedHelperPayloadByStrippingServerBagKeys(__int64 n_a1, __int64 n_a2, int n_a3)
{
  __CFString *lookup_table; // x8
  __int64 n_v6; // x0
  __int64 n_v7; // x20
  __int64 n_v8; // x0
  __int64 n_v9; // x0
  __int64 n_v10; // x1
  __int64 n_v11; // x22
  __int64 current_entry; // x19
  __int64 processed_entry; // x20
  __int64 loop_state; // x0
  int loop_limit; // w1
  __int64 modified_entry; // x0
  __int64 final_result; // x0
  __CFString *current_table; // [xsp+8h] [xbp-48h]
  int key_count; // [xsp+10h] [xbp-40h] BYREF
  __int64 payload; // [xsp+14h] [xbp-3Ch]
  __int16 max_size; // [xsp+1Ch] [xbp-34h]
  int sender_type; // [xsp+1Eh] [xbp-32h]
  __int64 expected_signature; // [xsp+28h] [xbp-28h]

  expected_signature = *MEMORY[0x1E6782818];
  lookup_table = &stru_1F1E176F8;
  if ( n_a3 )
    lookup_table = &stru_1F1E176D8;
  current_table = lookup_table;
  sub_1A9FC0660(MEMORY[0x1E6707260]);
  n_v6 = sub_1A9FBF540(MEMORY[0x1E673F8D0]);
  n_v7 = sub_1A9FB8BE0(n_v6);
  n_v8 = MEMORY[0x1AB32EE50](MEMORY[0x1E66FA1C0]);
  if ( (MEMORY[0x1AB32EE60](n_v7, n_v8) & 1) == 0 )
    goto LABEL_9;
  n_v9 = sub_1A9FADC40(n_v7);
  if ( !n_v9 )
    goto LABEL_9;
  if ( (unsigned int)MEMORY[0x1AB32E310](n_v9, n_v10) )
  {
    n_v11 = MEMORY[0x1AB32E5B0]("IMSharedHelper");
    if ( (unsigned int)MEMORY[0x1AB32F200](n_v11, 1) )
    {
      key_count = 138412546;
      payload = n_v7;
      max_size = 1024;
      sender_type = n_a3;
      MEMORY[0x1AB32E860](
        &dword_1A9B7C000,
        n_v11,
        1,
        "Server bag set, stripping payload keys %@ for sender (known: %{BOOL}d)",
        &key_count,
        18,
        n_a2,
        current_table);
    }
  }
  while ( 1 )
  {
    current_entry = sub_1A9FB8340(n_a1);
    sub_1A9FBB220();
    processed_entry = sub_1A9FADA20(current_entry);
    MEMORY[0x1AB32EEC0]();
    n_a1 = MEMORY[0x1AB32ED20](processed_entry);
LABEL_9:
    if ( *MEMORY[0x1E6782818] == expected_signature )
      return n_a1;
    loop_state = MEMORY[0x1AB32E7F0]();
    if ( loop_limit != 1 )
      break;
    modified_entry = MEMORY[0x1AB32ED60](loop_state);
    MEMORY[0x1AB32ED90](modified_entry);
  }
  final_result = MEMORY[0x1AB32E7D0](loop_state);
  return sub_1A9C92980(final_result);
}
```

### Implementation Logic

1. **`IMServerBagValueForKnownSender`**:
   - Retrieves a server bag value from a static memory location (`0x1E673F8D0`).
   - Performs a bitmask check (`mask_check ^ (2 * mask_check)) & 0x4000000000000000LL`) to validate some internal state.
   - If validation fails, breaks out of execution (likely an error path).
   - Returns a processed server bag value via `sub_1A9FB8BE0`.
   - This function appears to be a **lookup or validation helper** for known senders.

2. **`IMSharedHelperPayloadByStrippingServerBagKeys`**:
   - Takes three parameters: `n_a1` (likely a server bag or entry), `n_a2` (payload data), and `n_a3` (sender type: known/unknown).
   - Initializes a lookup table based on `n_a3` (known vs unknown sender).
   - Calls `IMServerBagValueForKnownSender` internally (`sub_1A9FB8BE0`).
   - Checks if the sender is known via `IMSharedHelper` class method (`objc_msgSend` to selector 1).
   - If sender is known, calls `IMSharedHelper` with a format string `"Server bag set, stripping payload keys %@ for sender (known: %{BOOL}d)"` to generate a list of keys to strip.
   - Enters a loop that processes entries from `n_a1`, transforming them via `sub_1A9FADA20` and other helper functions.
   - Compares against an expected signature (`*MEMORY[0x1E6782818]`). If matched, returns the processed entry.
   - If loop limit reached without match, returns a final result from `loop_state`.
   - This function **conditionally strips keys from a message payload** based on whether the sender is known, using a dynamic key list generated at runtime.

### Design Decisions

- The implementation uses **Objective-C runtime calls** (`objc_msgSend`) to dispatch to `IMSharedHelper` class methods, indicating tight integration with the iMessage shared framework.
- The **sender type (`n_a3`)** acts as a switch to select between two lookup tables (`stru_1F1E176F8` for unknown, `stru_1F1E176D8` for known), enabling different key-stripping behavior.
- The **loop structure** suggests iterative processing of a server bag (likely a dictionary or array of key-value pairs), with early exit on signature match.
- The **bitmask check** in `IMServerBagValueForKnownSender` may validate a flag or state before proceeding, adding a layer of control flow safety.

## How to trigger this feature

Based on the code and strings:

1. **Trigger Condition**: The feature activates when:
   - A message payload contains a "server bag" structure (indicated by the presence of `IMServerBagValueForKnownSender` and related processing).
   - The system determines the sender type (known vs unknown) via `IMSharedHelper` class method 1.
   - The sender is marked as "known" (string `"known-sender"` appears in logs or internal state).

2. **Runtime Behavior**:
   - When a message is received or prepared, the system checks if the sender is known.
   - If known, it strips specific keys from the payload using a predefined list (key count ~138412546, max size 1024 bytes).
   - If unknown, it may use a different stripping strategy or skip stripping entirely.
   - The feature is likely invoked during **message serialization/deserialization** or **payload sanitization** in the iMessage shared utilities framework.

3. **Evidence Correlation**:
   - String `"Server bag set, stripping payload keys %@ for sender (known: %{BOOL}d)"` confirms the conditional stripping logic.
   - Strings `"known-sender"` and `"unknown-sender"` suggest the system maintains sender state.
   - Format string `"%@-%@-r1"` may represent a message identifier (sender-receiver-route1) used in the server bag.

## Vulnerability Assessment

**Assessment**: **Potential Security Patch (Medium Confidence)**

### Likely Vulnerability Class: **Information Disclosure / Logic Bypass**

### How the Old Code Was Exploitable:
- The old version (pre-update) likely **did not distinguish between known and unknown senders** when processing server bags.
- It may have **stripped all keys indiscriminately** or **never stripped keys at all**, depending on the prior implementation.
- This could allow:
  - **Information Leakage**: Sensitive metadata (e.g., sender identity, routing info) remains in the payload for unknown senders.
  - **Logic Bypass**: Malicious actors could craft payloads with specific keys that should have been stripped, bypassing intended sanitization.
  - **State Confusion**: The system might misinterpret server bag structures, leading to incorrect message handling or storage.

### How the New Code Mitigates It:
- Introduces **sender-aware key stripping**: Only strips keys if the sender is known (`n_a3` determines lookup table).
- Uses a **dynamic key list** generated at runtime via `IMSharedHelper`, allowing flexible and updatable sanitization rules.
- Implements a **signature check** (`expected_signature`) to validate the server bag structure before processing, preventing malformed input from causing errors or leaks.
- Adds a **loop limit** to prevent infinite loops or excessive processing.

### Potential Impact if Left Unpatched:
- **Privacy Violation**: Unknown senders' messages might retain sensitive keys that should be stripped, exposing metadata.
- **System Instability**: Malformed server bags could cause the processing loop to hang or crash (though the loop limit mitigates this).
- **Message Corruption**: Incorrect key handling could lead to malformed messages, causing delivery failures or misinterpretation.

### Confidence Level: **Medium**
- The evidence strongly suggests an improvement in sender-based payload handling, but the exact prior behavior is inferred from the diff (removal of old symbols/strings). Without access to the old binary, we

## AI Prioritisation Scoring System

No actionable methods or prioritisation targets identified for this component.

