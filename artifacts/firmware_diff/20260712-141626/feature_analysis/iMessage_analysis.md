## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "B36@0:8@16B24@28"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 55 (2 AI-authored, 53 auto-generated); comments: 4 (2 AI-authored, 2 auto-generated); across 2 function(s); verified persisted in .i64: 151 named variables, 204 comments.

## What this feature does

This update introduces new security and privacy mitigations for handling incoming iMessage group chat payloads. It specifically targets abuse vectors where unknown senders could manipulate group chats (e.g., changing group names or adding participants) or inject malicious configurations. The feature enforces strict interaction requirements before accepting specific types of group messages from unknown senders and sanitizes incoming payloads by stripping out server bag keys.

## How is it implemented


### Decompilation at `0x88d58`

```c
bool __cdecl -[MessageGroupController _shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:](
        MessageGroupController *self,
        SEL selector,
        id groupPayload,
        bool isKnownSender,
        id groupPayloadType)
{
  return isKnownSender
      || groupPayload
      && !objc_msgSend(groupPayload, "isFiltered")
      && (int)objc_msgSend(groupPayload, "getNumberOfTimesRespondedToThread") > 0
      || ((unsigned int)objc_msgSend(groupPayloadType, "isEqualToString:", off_12B838[0]) & 1) == 0
      && ((unsigned int)objc_msgSend(groupPayloadType, "isEqualToString:", off_12B840[0]) & 1) == 0;
}
```

The implementation introduces a new Objective-C method, `_shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:`, within the `MessageGroupController`. This method evaluates incoming group message payloads against a set of boolean conditions to determine if they should be processed. 

The logic dictates that a payload is accepted if any of the following are true:
1. The sender is already known (`isKnownSender` is true).
2. The payload type does not match two specific restricted string constants (likely representing sensitive group modification events).
3. If the payload type *does* match the restricted types and the sender is unknown, the payload is only accepted if it is not marked as filtered and the user has previously interacted with the thread (verified by calling `getNumberOfTimesRespondedToThread` and ensuring the count is greater than 0).

Additionally, the binary introduces a call to the external symbol `_IMSharedHelperPayloadByStrippingServerBagKeys`, which is associated with the newly added string `MessageGroupController-strip-payload-keys`. This indicates that before processing, certain payloads are explicitly sanitized to remove server bag keys, preventing malicious payloads from overriding local configuration values.

## How to trigger this feature

This feature is triggered automatically when the device receives a group message payload, particularly from an unknown sender. The validation logic is invoked to determine whether the payload should be accepted and processed by the Messages app, or silently discarded/filtered. The payload sanitization is triggered during the parsing phase of these incoming messages.

## Vulnerability Assessment

This is a high-priority security and privacy patch addressing two distinct vulnerability classes:

1. **Logic Flaw / Abuse Vector**: Previously, an attacker could send unsolicited group message payloads (such as renaming a group or changing its metadata) to a user who had never interacted with the sender or the group. By enforcing that the user must have responded to the thread (`getNumberOfTimesRespondedToThread > 0`) for restricted payload types from unknown senders, the patch effectively mitigates unsolicited group chat abuse, spam, and potential harassment.
2. **Configuration Injection**: The introduction of `_IMSharedHelperPayloadByStrippingServerBagKeys` suggests a vulnerability where an attacker could embed server bag keys within a message payload. If processed blindly by the receiving device, this could allow the attacker to override local server bag configurations, potentially bypassing security checks, altering application behavior, or redirecting endpoints. The new code sanitizes the payload by stripping these keys, neutralizing the injection vector.

If left unpatched, these issues could allow remote attackers to manipulate group chat states for unknown users and potentially exploit configuration parsing logic.

## Evidence

*   **Added Symbols**:
    *   `_IMSharedHelperPayloadByStrippingServerBagKeys`
*   **Added Strings**:
    *   `_shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:`
    *   `getNumberOfTimesRespondedToThread`
    *   `MessageGroupController-strip-payload-keys`
*   **Decompiled Logic**: The decompilation of `_shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:` at `0x88d58` confirms the exact boolean logic used to gate payload acceptance based on sender status, payload type, and prior user interaction.

## AI Prioritisation Scoring System

- **Feature Analysis**
  - **Tier**: TIER_1
  - **Category**: Security/Privacy
  - **Reasoning**: Introduces strict validation for group message payloads from unknown senders, requiring prior user interaction for specific payload types. Also adds sanitization to strip server bag keys from payloads, mitigating potential configuration injection and abuse.

