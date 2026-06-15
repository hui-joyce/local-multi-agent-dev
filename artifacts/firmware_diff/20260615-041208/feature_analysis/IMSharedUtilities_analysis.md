## What this feature does
This feature introduces server bag handling logic into the iMessage shared utilities framework. Specifically, it adds two new functions: `_IMServerBagValueForKnownSender` and `_IMSharedHelperPayloadByStrippingServerBagKeys`. The functionality appears to be related to processing and modifying iMessage payloads based on sender identity (known vs unknown). The strings "Server bag set, stripping payload keys" and "known-sender"/"unknown-sender" suggest the code determines if a sender is known and then strips specific keys from the message payload accordingly. This is likely part of the iMessage server bag mechanism used for message metadata and delivery tracking.

## How is it implemented
The implementation consists of two new functions that work together:

1. **`_IMServerBagValueForKnownSender`**: This function appears to retrieve or calculate a server bag value specifically for known senders. Based on the naming convention and the "known-sender" string, it likely checks the sender's status in the server bag and returns an appropriate value.

2. **`_IMSharedHelperPayloadByStrippingServerBagKeys`**: This function takes a payload and strips server bag keys from it, but only for known senders. The string "Server bag set, stripping payload keys %@ for sender (known: %{BOOL}d)" suggests this function accepts parameters for the payload and a boolean indicating whether the sender is known.

The implementation flow appears to be:
- Check if the sender is known (using the "known-sender" logic)
- If known, strip server bag keys from the payload
- Return the modified payload

The functions are likely called in sequence or in specific contexts where server bag processing is needed. The framework is `IMSharedUtilities`, which suggests these utilities are shared across iMessage components.

## How to trigger this feature
The feature is triggered when:
1. An iMessage is being processed and the sender is identified as "known"
2. The message payload contains server bag keys that need to be stripped
3. The code path is executed during iMessage payload processing or server bag handling

The trigger conditions are likely:
- Presence of a known sender in the message chain
- Detection of server bag keys in the payload that should be removed
- Specific iMessage processing contexts where server bag manipulation is required

## Evidence
**Symbols Added:**
- `_IMServerBagValueForKnownSender` - Function for retrieving server bag values for known senders
- `_IMSharedHelperPayloadByStrippingServerBagKeys` - Function for stripping server bag keys from payloads

**Strings Added:**
- `"%@-%@-r1"` - Likely a format string for server bag key generation or identification
- `"Server bag set, stripping payload keys %@ for sender (known: %{BOOL}d)"` - Descriptive string explaining the stripping functionality
- `"known-sender"` - String literal used for sender identification
- `"unknown-sender"` - String literal for unknown sender identification

**Binary Changes:**
- UUID changed from `F29C6B2A-61F6-32C3-B955-F42B045906D4` to `34548AD5-80C8-394A-8960-9C594FADBA4B`
- Function count increased from 18684 to 18686 (2 new functions)
- Symbol count increased from 3774 to 3776 (2 new symbols)
- CStrings count increased from 21352 to 21359 (7 new strings)
- Text section size increased from `0x321b20` to `0x321d28`

**Framework:** `/System/Library/PrivateFrameworks/IMSharedUtilities.framework/IMSharedUtilities`

## AI Prioritisation Scoring System

- **symbol_analysis**
  - **Tier**: TIER_2
  - **Category**: messaging
  - **Reasoning**: High-signal indicators present (new symbols, security/IPC-related strings, server bag functionality) but decompiler connection failed. Feature is related to iMessage server bag processing which is important but not critical security issue. Cannot verify exact implementation without decompilation.

