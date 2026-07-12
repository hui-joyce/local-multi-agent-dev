## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "B36@0:8@16B24@28"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 2 (2 AI-authored, 0 auto-generated); comments: 3 (1 AI-authored, 2 auto-generated); across 2 function(s); verified persisted in .i64: 8 named variables, 4 comments.

## What this feature does
This update introduces a refined validation mechanism for incoming iMessage group payloads. It adds logic to determine whether a message payload should be accepted based on its interaction history and sender characteristics. Specifically, it introduces a mechanism to strip server-side bag keys from payloads, likely to prevent unauthorized or malformed configuration data from being processed by the group message controller.

## How is it implemented


### Decompilation at `0x88d58`

```c
bool __cdecl -[MessageGroupController _shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:](
        MessageGroupController *self,
        SEL sel_a2,
        id payload,
        bool isKnownSender,
        id payloadType)
{
  return isKnownSender
      || payload
      && !objc_msgSend(payload, "isFiltered")
      && (int)objc_msgSend(payload, "getNumberOfTimesRespondedToThread") > 0
      || ((unsigned int)objc_msgSend(payloadType, "isEqualToString:", off_12B838[0]) & 1) == 0
      && ((unsigned int)objc_msgSend(payloadType, "isEqualToString:", off_12B840[0]) & 1) == 0;
}
```

The implementation centers on the `-[MessageGroupController _shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:]` method. The logic evaluates the incoming payload using three primary conditions:
1. **Explicit Acceptance**: If the `isKnownSender` flag is true, the payload is accepted immediately.
2. **Payload Filtering and Engagement**: If the sender is unknown, the system checks if the payload is marked as filtered. If it is not filtered, it further verifies the engagement level by checking if the number of times the user has responded to the thread is greater than zero.
3. **Type-Based Validation**: The method performs a check against specific message types (represented by string constants) to determine if the payload should be processed.

The new symbol `_IMSharedHelperPayloadByStrippingServerBagKeys` suggests that the system now proactively sanitizes payloads by removing server-bag-related keys before they reach the processing logic, ensuring that only validated, stripped data is handled by the `MessageGroupController`.

## How to trigger this feature
This feature is triggered automatically when an iMessage group payload is received. The logic is invoked during the message processing pipeline to decide whether to accept the payload into an existing chat session. It is most likely to be exercised when receiving messages from unknown senders or when the system needs to verify the legitimacy of a group message payload before rendering it in the UI.

## Vulnerability Assessment
This change appears to be a security-hardening measure. By introducing `_IMSharedHelperPayloadByStrippingServerBagKeys` and adding a check for `getNumberOfTimesRespondedToThread`, the implementation mitigates potential risks associated with processing untrusted or malicious group message payloads. 

The previous implementation likely lacked sufficient validation for payloads from unknown senders, potentially allowing for "message injection" or unauthorized state changes within a group chat. By requiring a non-zero response count for unknown senders and stripping server-bag keys, the system reduces the attack surface for exploits that rely on malformed payloads to trigger unintended behavior or bypass chat filters. This is a defensive update aimed at improving the integrity of group message handling.

## Evidence
- **Symbol Added**: `_IMSharedHelperPayloadByStrippingServerBagKeys`
- **Method Added**: `-[MessageGroupController _shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:]`
- **Strings Added**: `"MessageGroupController-strip-payload-keys"`, `"getNumberOfTimesRespondedToThread"`
- **Binary**: `/System/Library/Messages/PlugIns/iMessage.imservice/iMessage`

## AI Prioritisation Scoring System

- **static_analysis**
  - **Tier**: TIER_1
  - **Category**: security_patch
  - **Reasoning**: This update implements a new validation layer for incoming iMessage payloads, including payload sanitization and sender-based filtering, which directly addresses potential message-injection vulnerabilities.

