## What this feature does
The iMessage binary update introduces a new payload processing mechanism specifically designed to strip server bag keys from iMessage payloads. This functionality is critical for handling group message payloads and ensuring compatibility with the server's expected payload format. The feature includes a dedicated helper function (`_IMSharedHelperPayloadByStrippingServerBagKeys`) that processes payloads, and a new method selector (`MessageGroupController-strip-payload-keys`) that triggers this processing. Additionally, there's a new method (`_shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:`) that appears to validate group message payloads based on chat existence and sender status. The feature also introduces a new counter (`getNumberOfTimesRespondedToThread`) for tracking thread response history.

## How is it implemented
The implementation consists of several interconnected components:

1. **Payload Stripping Helper**: The function `_IMSharedHelperPayloadByStrippingServerBagKeys` (address: 0xc7210) is a wrapper that calls the actual implementation. This function is responsible for removing server bag keys from iMessage payloads.

2. **Payload Processing Method**: The selector `MessageGroupController-strip-payload-keys` (address: 0xe529e) is referenced by data offsets at addresses 1181248 and 560784. This suggests that the `MessageGroupController` class has a method to strip payload keys, which is called from other parts of the codebase.

3. **Group Message Validation**: The selector `_shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:` (address: 0x102463) is referenced by data offsets at addresses 826308, 1209816, and 826304. This method appears to validate whether a group message payload should be accepted based on whether the chat exists, if the sender is known, and the message type.

4. **Thread Response Counter**: The selector `getNumberOfTimesRespondedToThread` (address: 0x10623e) is referenced by data offsets at addresses 840676, 1213408, and 840672. This suggests a mechanism for tracking how many times a user has responded to a specific thread.

The data flow appears to be:
- When a group message payload is received, the `MessageGroupController-strip-payload-keys` method is called to process the payload
- Before accepting the group message, the `_shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:` method validates the payload
- The `getNumberOfTimesRespondedToThread` method tracks response history for threads

## How to trigger this feature
The feature is triggered when:
1. A group message payload is received and needs to be processed
2. The system needs to validate whether to accept a group message payload based on chat existence and sender status
3. The system needs to track or retrieve the number of times a user has responded to a specific thread

The new symbols and strings in the diff indicate that this is a new feature that was added in version 26.4.2, suggesting it's not yet fully integrated or is being developed.

## Evidence
- **New Symbol**: `_IMSharedHelperPayloadByStrippingServerBagKeys` (address: 0xc7210) - A new function for stripping server bag keys from payloads
- **New String**: `MessageGroupController-strip-payload-keys` (address: 0xe529e) - A new method selector for stripping payload keys
- **New String**: `_shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:` (address: 0x102463) - A new method selector for validating group message payloads
- **New String**: `getNumberOfTimesRespondedToThread` (address: 0x10623e) - A new method selector for tracking thread responses
- **New CStrings**: `B36@0:8@16B24@28` - An ObjC type encoding (method signature)
- **Function Count**: Increased from 1668 to 1669 (1 new function)
- **Symbol Count**: Increased from 892 to 893 (1 new symbol)
- **CString Count**: Increased from 5119 to 5124 (5 new strings)

## AI Prioritisation Scoring System

- **payload_processing**
  - **Tier**: TIER_1
  - **Category**: messaging
  - **Reasoning**: Added new payload processing functionality for iMessage group messages, including server bag key stripping and group message validation. This is a significant feature addition that affects core iMessage functionality.

