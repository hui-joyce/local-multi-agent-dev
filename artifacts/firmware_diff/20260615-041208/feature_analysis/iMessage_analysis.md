## What this feature does
The `iMessage` binary update introduces a new payload processing mechanism specifically designed to handle group message payloads. The new symbol `_IMSharedHelperPayloadByStrippingServerBagKeys` and the associated string "MessageGroupController-strip-payload-keys" indicate a feature that strips server bag keys from iMessage group payloads. This is likely part of a privacy or data sanitization feature, possibly related to the "Message Group Controller" functionality, ensuring that server-side metadata (server bags) is removed from group messages before they are processed or stored locally.

## How is it implemented
The implementation consists of a new helper function `IMSharedHelperPayloadByStrippingServerBagKeys` which appears to be a wrapper around an existing internal function `_IMSharedHelperPayloadByStrippingServerBagKeys`. The decompiled code shows:

```c
__int64 IMSharedHelperPayloadByStrippingServerBagKeys()
{
  return _IMSharedHelperPayloadByStrippingServerBagKeys();
}
```

This function takes no arguments and simply delegates to the internal implementation. The function name suggests it operates on an `IMSharedHelperPayload` structure, stripping server bag keys from it.

The string "MessageGroupController-strip-payload-keys" suggests that this functionality is exposed via a method on the `MessageGroupController` class, likely as a selector for Objective-C message sending. The selector string format `MessageGroupController-strip-payload-keys` follows the pattern of `ClassName-methodName`.

The new symbol `_shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:` suggests a new method for handling group message payloads, checking conditions like whether the chat exists and if the sender is known. This is likely part of the same group message handling flow.

The string "B36@0:8@16B24@28" appears to be a format string, possibly related to binary data processing or serialization, which might be used in the payload stripping logic.

The function count increased by 1 (1668 -> 1669), and the symbol count increased by 1 (892 -> 893), confirming the addition of this new function. The CStrings count increased by 5 (5119 -> 5124), indicating the addition of several new strings, including the ones mentioned above.

## How to trigger this feature
The exact trigger conditions are not fully clear from the available evidence, but based on the symbol name `_shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:`, it appears that this feature is triggered when:
1. A group message payload is received or being processed.
2. The chat associated with the group message already exists (`existingChat`).
3. The sender of the message is known (`isKnownSender`).
4. The message type is appropriate (`type`).

The `IMSharedHelperPayloadByStrippingServerBagKeys` function is likely called as part of the group message processing pipeline, possibly when the message is being prepared for local storage or display.

## Evidence
- **New Symbol**: `_IMSharedHelperPayloadByStrippingServerBagKeys` (address: 0xc7210)
- **New Strings**:
  - "B36@0:8@16B24@28"
  - "MessageGroupController-strip-payload-keys"
  - "_shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:"
  - "getNumberOfTimesRespondedToThread"
- **New Function**: `IMSharedHelperPayloadByStrippingServerBagKeys` (address: 0xc7210)
- **Function Count Change**: 1668 -> 1669
- **Symbol Count Change**: 892 -> 893
- **CStrings Count Change**: 5119 -> 5124
- **Section Address Changes**: Various `__TEXT` and `__DATA_CONST` sections have shifted, indicating the addition of new code and data.

## AI Prioritisation Scoring System

- **symbol_addition**
  - **Tier**: TIER_1
  - **Category**: messaging_privacy
  - **Reasoning**: Added symbol '_IMSharedHelperPayloadByStrippingServerBagKeys' and related strings indicate a new feature for stripping server bag keys from iMessage group payloads, which is a privacy-related functionality. The function is part of the MessageGroupController subsystem, suggesting it's a core feature for handling group messages.

