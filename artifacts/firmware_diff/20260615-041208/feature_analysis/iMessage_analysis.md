## What this feature does
The iMessage binary update introduces a new payload processing mechanism specifically designed to handle group message payloads. The feature adds a dedicated helper function `_IMSharedHelperPayloadByStrippingServerBagKeys` which appears to process and strip server bag keys from incoming group message payloads. This is supported by the addition of the string "MessageGroupController-strip-payload-keys", indicating a controller responsible for stripping payload keys. The feature also adds a new method selector `_shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:` which suggests logic for determining whether a group message payload should be accepted based on chat existence and sender knowledge. Additionally, a new string "getNumberOfTimesRespondedToThread" implies tracking of response counts within message threads.

## How is it implemented
The implementation centers around the newly added symbol `_IMSharedHelperPayloadByStrippingServerBagKeys` located at address `0xc7210`. The decompiled function shows it acts as a wrapper that calls an internal implementation `_IMSharedHelperPayloadByStrippingServerBagKeys()`.

**Decompiled Pseudocode:**
```c
__int64 IMSharedHelperPayloadByStrippingServerBagKeys()
{
  return _IMSharedHelperPayloadByStrippingServerBagKeys();
}
```

**Call Chain Analysis:**
1. The symbol `_IMSharedHelperPayloadByStrippingServerBagKeys` (0xc7210) is a code symbol that wraps an internal function.
2. The string "MessageGroupController-strip-payload-keys" (0xe529e) is referenced by code, suggesting it is called by the `MessageGroupController` class.
3. The string "_shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:" (0x102463) is referenced by code, indicating a method in the `MessageGroupController` or related class that checks conditions for accepting group messages.
4. The string "getNumberOfTimesRespondedToThread" (0x10623e) is referenced by code, suggesting a method to retrieve response counts.

**Data Flow Trace:**
- The `MessageGroupController` likely invokes the "strip-payload-keys" operation.
- Before processing, it probably calls `_shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:` to validate the message.
- The `_IMSharedHelperPayloadByStrippingServerBagKeys` function is the core logic for stripping server bag keys, which are likely metadata keys added by the server for group messages.
- The "getNumberOfTimesRespondedToThread" string suggests that the feature also tracks how many times a user has responded to a specific thread, which could be used to determine message acceptance or delivery status.

## How to trigger this feature
The feature is triggered when:
1. A group message payload is received.
2. The `MessageGroupController` processes the payload.
3. The `_shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:` method is called to check if the chat exists and the sender is known.
4. If the conditions are met, the `_IMSharedHelperPayloadByStrippingServerBagKeys` function is called to strip server bag keys from the payload.
5. The "getNumberOfTimesRespondedToThread" method is likely called to update or retrieve the response count for the thread.

## Evidence
- **New Symbol:** `_IMSharedHelperPayloadByStrippingServerBagKeys` at address `0xc7210` (Type: symbol).
- **New Strings:**
  - "MessageGroupController-strip-payload-keys" at address `0xe529e` (Type: string_data).
  - "_shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:" at address `0x102463` (Type: string_data).
  - "getNumberOfTimesRespondedToThread" at address `0x10623e` (Type: string_data).
- **ObjC Type Encoding:** "B36@0:8@16B24@28" (Type: ObjC type encoding, skipped).
- **Function Count Change:** Increased from 1668 to 1669.
- **Symbol Count Change:** Increased from 892 to 893.
- **CStrings Count Change:** Increased from 5119 to 5124.
- **UUID Change:** From `95C89B97-D474-32AB-83F0-DFAC73717D2C` to `3BBE6D71-A477-31DA-A41C-1FDFE5C36B8F`.

## AI Prioritisation Scoring System

- **symbol_and_string_analysis**
  - **Tier**: TIER_1
  - **Category**: messaging
  - **Reasoning**: Added symbols and strings indicate new group message payload processing logic, including stripping server bag keys and checking message acceptance conditions. This is a significant feature addition to the iMessage system.

