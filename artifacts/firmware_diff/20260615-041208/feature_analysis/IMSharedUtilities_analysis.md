## What this feature does
This feature implements a server bag (server-side metadata) management system for iMessage, specifically handling the logic to strip server bag keys from the message payload based on whether the sender is known. The system distinguishes between "known" and "unknown" senders, applying different processing rules. It appears to be part of the `IMSharedUtilities` framework, which provides shared utilities for iMessage processing.

The feature performs the following:
1.  **Identifies Sender Type**: It checks if the sender is a "known" or "unknown" sender.
2.  **Strips Server Bag Keys**: If the sender is known, it strips specific keys from the server bag payload.
3.  **Validates Payload**: It validates the payload against a set of rules, possibly checking for specific keys or values.
4.  **Modifies Payload**: If validation passes, it modifies the payload, potentially adding or removing keys.
5.  **Returns Processed Payload**: It returns the processed payload, which can be used for further processing or storage.

## How is it implemented
The implementation consists of two main functions: `IMServerBagValueForKnownSender` and `IMSharedHelperPayloadByStrippingServerBagKeys`.

### `IMServerBagValueForKnownSender`
This function takes a sender identifier and returns a value associated with the known sender. It appears to perform some internal calculations and checks before returning the value.

```c
__int64 IMServerBagValueForKnownSender()
{
  __int64 v0; // x0
  __int64 vars8; // [xsp+28h] [xbp+8h]

  // Call some internal function with a memory address
  sub_1A9FC0660(MEMORY[0x1E6707260]);
  v0 = sub_1A9FBF540(MEMORY[0x1E673F8D0]);
  // Perform some bitwise operation and check
  if ( ((vars8 ^ (2 * vars8)) & 0x4000000000000000LL) != 0 )
    __break(0xC471u);
  // Return the result of another function call
  return sub_1A9FB8BE0(v0);
}
```

### `IMSharedHelperPayloadByStrippingServerBagKeys`
This function takes a payload, a sender identifier, and a flag indicating whether the sender is known. It processes the payload by stripping server bag keys based on the sender type.

```c
__int64 __fastcall IMSharedHelperPayloadByStrippingServerBagKeys(__int64 a1, __int64 a2, int a3)
{
  __CFString *v5; // x8
  __int64 v6; // x0
  __int64 v7; // x20
  __int64 v8; // x0
  __int64 v9; // x0
  __int64 v10; // x1
  __int64 v11; // x22
  __int64 v12; // x19
  __int64 v13; // x20
  __int64 v15; // x0
  int v16; // w1
  __int64 v17; // x0
  __int64 v18; // x0
  __CFString *v20; // [xsp+8h] [xbp-48h]
  int v21; // [xsp+10h] [xbp-40h] BYREF
  __int64 v22; // [xsp+14h] [xbp-3Ch]
  __int16 v23; // [xsp+1Ch] [xbp-34h]
  int v24; // [xsp+1Eh] [xbp-32h]
  __int64 v25; // [xsp+28h] [xbp-28h]

  // Get a value from memory
  v25 = *MEMORY[0x1E6782818];
  // Select a string based on the sender type
  v5 = &stru_1F1E176F8;
  if ( a3 ) // If sender is known
    v5 = &stru_1F1E176D8;
  v20 = v5;
  // Call some internal function
  sub_1A9FC0660(MEMORY[0x1E6707260]);
  v6 = sub_1A9FBF540(MEMORY[0x1E673F8D0]);
  v7 = sub_1A9FB8BE0(v6);
  // Call another internal function
  v8 = MEMORY[0x1AB32EE50](MEMORY[0x1E66FA1C0]);
  // Perform some check
  if ( (MEMORY[0x1AB32EE60](v7, v8) & 1) == 0 )
    goto LABEL_9;
  v9 = sub_1A9FADC40(v7);
  if ( !v9 )
    goto LABEL_9;
  // Perform another check
  if ( (unsigned int)MEMORY[0x1AB32E310](v9, v10) )
  {
    // Get a string
    v11 = MEMORY[0x1AB32E5B0]("IMSharedHelper");
    // Call a function with the string
    if ( (unsigned int)MEMORY[0x1AB32F200](v11, 1) )
    {
      v21 = 138412546;
      v22 = v7;
      v23 = 1024;
      v24 = a3;
      // Call a function with multiple arguments, including a format string
      MEMORY[0x1AB32E860](
        &dword_1A9B7C000,
        v11,
        1,
        "Server bag set, stripping payload keys %@ for sender (known: %{BOOL}d)",
        &v21,
        18,
        a2,
        v20);
    }
  }
  // Loop
  while ( 1 )
  {
    v12 = sub_1A9FB8340(a1);
    sub_1A9FBB220();
    v13 = sub_1A9FADA20(v12);
    // Call a function
    MEMORY[0x1AB32EEC0]();
    a1 = MEMORY[0x1AB32ED20](v13);
LABEL_9:
    // Compare a value with a constant
    if ( *MEMORY[0x1E6782818] == v25 )
      return a1;
    v15 = MEMORY[0x1AB32E7F0]();
    if ( v16 != 1 )
      break;
    v17 = MEMORY[0x1AB32ED60](v15);
    // Call a function
    MEMORY[0x1AB32ED90](v17);
  }
  v18 = MEMORY[0x1AB32E7D0](v15);
  // Call a function with the result
  return sub_1A9C92980(v18);
}
```

### Call Chains and Data Flow
1.  `IMServerBagValueForKnownSender` is called with a sender identifier. It performs some internal calculations and returns a value.
2.  `IMSharedHelperPayloadByStrippingServerBagKeys` is called with a payload, a sender identifier, and a flag indicating whether the sender is known.
3.  It selects a string based on the sender type.
4.  It calls `IMServerBagValueForKnownSender` to get a value.
5.  It performs some checks and calls other internal functions.
6.  It loops and performs further processing, including comparisons and function calls.
7.  It returns the processed payload.

## How to trigger this feature
The feature is triggered when a message is received or sent, and the system needs to process the server bag payload based on the sender type. The specific conditions for triggering the feature are not explicitly clear from the decompiled code, but it is likely triggered by the presence of a server bag payload and the need to process it.

## Evidence
- **Symbols**: `_IMServerBagValueForKnownSender`, `_IMSharedHelperPayloadByStrippingServerBagKeys`
- **CStrings**: `"%@-%@-r1"`, `"Server bag set, stripping payload keys %@ for sender (known: %{BOOL}d)"`, `"known-sender"`, `"unknown-sender"`
- **Addresses**: `0x1a9c92778` (IMServerBagValueForKnownSender), `0x1a9c927f8` (IMSharedHelperPayloadByStrippingServerBagKeys)
- **Function Count Change**: +2 (from 18684 to 18686)
- **Symbol Count Change**: +2 (from 3774 to 3776)
- **CString Count Change**: +7 (from 21352 to 21359)

## AI Prioritisation Scoring System

- **Symbol_Addition**
  - **Tier**: TIER_2
  - **Category**: Server_Bag_Management
  - **Reasoning**: The diff shows the addition of two new symbols (`_IMServerBagValueForKnownSender` and `_IMSharedHelperPayloadByStrippingServerBagKeys`) and several new CStrings related to server bag processing. The decompiled code reveals a feature that handles server bag payload stripping based on sender type, which is a significant change in the iMessage message processing logic. This feature is likely related to server-side message handling and could impact message delivery or storage.

