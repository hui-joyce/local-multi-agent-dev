## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "B36@0:8@16B24@28"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 1 (1 AI-authored, 0 auto-generated); comments: 3 (2 AI-authored, 1 auto-generated); across 1 function(s); verified persisted in .i64: 4 named variables, 2 comments.

## What this feature does

This update introduces a refined validation mechanism for incoming iMessage group payloads within the `MessageGroupController`. It implements a conditional logic gate that determines whether a group message payload should be accepted based on the sender's status, the payload's filtering state, and the interaction history associated with the thread. Additionally, it introduces a helper function, `_IMSharedHelperPayloadByStrippingServerBagKeys`, which appears to facilitate the sanitization of payload keys, likely to prevent the processing of unauthorized or deprecated server-side configuration keys.

## How is it implemented


### Decompilation at `0x88d58`

```c
bool __cdecl -[MessageGroupController _shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:](
        MessageGroupController *self,
        SEL selector,
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

The implementation centers on the `_shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:` method. The logic evaluates acceptance using a series of boolean checks. First, it permits the payload if the sender is already known. If the sender is unknown, it proceeds to verify if the payload is unfiltered and checks if the user has previously responded to the thread by querying the thread's response count. Finally, it performs a check against specific payload types to ensure they do not match restricted or legacy identifiers. The introduction of `_IMSharedHelperPayloadByStrippingServerBagKeys` suggests that the system now actively strips specific keys from the server bag before processing, ensuring that only validated payload structures are handled by the group controller.

## How to trigger this feature

This feature is triggered automatically when an incoming group message payload is received by the `iMessage.imservice` plugin. The logic is invoked during the message processing pipeline to decide whether to accept or reject the payload based on the sender's identity and the payload's metadata.

## Vulnerability Assessment

This change appears to be a security-hardening measure. By introducing explicit checks for `isFiltered` status and a minimum threshold for `getNumberOfTimesRespondedToThread`, the system prevents the automatic processing of potentially malicious or spam-related group payloads from unknown senders. The addition of `_IMSharedHelperPayloadByStrippingServerBagKeys` further mitigates risks associated with server-side configuration injection, ensuring that the client does not honor unauthorized payload keys that could lead to unexpected behavior or privilege escalation within the messaging context. This is a defensive update aimed at improving the integrity of group message handling.

## Evidence

- **Symbol Added**: `_IMSharedHelperPayloadByStrippingServerBagKeys`
- **Method Added**: `-[MessageGroupController _shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:]`
- **Strings Added**: `"MessageGroupController-strip-payload-keys"`, `"getNumberOfTimesRespondedToThread"`
- **Binary**: `/System/Library/Messages/PlugIns/iMessage.imservice/iMessage`

## AI Prioritisation Scoring System

- **static_analysis**
  - **Tier**: TIER_1
  - **Category**: security_hardening
  - **Reasoning**: The changes implement new validation logic for incoming IPC payloads and introduce a key-stripping mechanism, which are direct mitigations against potential message-based injection or spam/abuse vectors.

