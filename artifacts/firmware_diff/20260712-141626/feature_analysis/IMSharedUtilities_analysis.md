## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "%@-%@-r1"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 3 (3 AI-authored, 0 auto-generated); comments: 4 (2 AI-authored, 2 auto-generated); across 2 function(s); verified persisted in .i64: 24 named variables, 3 comments.

## What this feature does
This feature introduces a dynamic payload sanitization mechanism for incoming messages. It filters and strips specific keys from message payload dictionaries based on the trust level of the sender—specifically distinguishing between a "known sender" (e.g., someone in the user's contacts) and an "unknown sender". The exact keys to be stripped are determined by this trust level, and the entire stripping mechanism can be remotely enabled or disabled by Apple via a Server Bag configuration.

## How is it implemented


### Decompilation at `0x1a9c92778`

```c
__int64 IMServerBagValueForKnownSender()
{
  __int64 extracted_server_bag; // x0
  __int64 mask_check; // [xsp+28h] [xbp+8h]

  sub_1A9FC0660(MEMORY[0x1E6707260]);
  extracted_server_bag = sub_1A9FBF540(MEMORY[0x1E673F8D0]);
  if ( ((mask_check ^ (2 * mask_check)) & 0x4000000000000000LL) != 0 )
    __break(0xC471u);
  return sub_1A9FB8BE0(extracted_server_bag);
}
```

### Decompilation at `0x1a9c927f8`

```c
__int64 __fastcall IMSharedHelperPayloadByStrippingServerBagKeys(
        __int64 payload_dict,
        __int64 keys_to_strip,
        int is_known_sender)
{
  __CFString *lookup_table; // x8
  __int64 intermediate_value_1; // x0
  __int64 bag_value; // x20
  __int64 intermediate_value_3; // x0
  __int64 intermediate_value_4; // x0
  __int64 intermediate_value_5; // x1
  __int64 os_log_obj; // x22
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
  if ( is_known_sender )
    lookup_table = &stru_1F1E176D8;
  current_table = lookup_table;
  sub_1A9FC0660(MEMORY[0x1E6707260]);
  intermediate_value_1 = sub_1A9FBF540(MEMORY[0x1E673F8D0]);
  bag_value = sub_1A9FB8BE0(intermediate_value_1);
  intermediate_value_3 = MEMORY[0x1AB32EE50](MEMORY[0x1E66FA1C0]);
  if ( (MEMORY[0x1AB32EE60](bag_value, intermediate_value_3) & 1) == 0 )
    goto LABEL_9;
  intermediate_value_4 = sub_1A9FADC40(bag_value);
  if ( !intermediate_value_4 )
    goto LABEL_9;
  if ( (unsigned int)MEMORY[0x1AB32E310](intermediate_value_4, intermediate_value_5) )
  {
    os_log_obj = MEMORY[0x1AB32E5B0]("IMSharedHelper");
    if ( (unsigned int)MEMORY[0x1AB32F200](os_log_obj, 1) )
    {
      key_count = 138412546;
      payload = bag_value;
      max_size = 1024;
      sender_type = is_known_sender;
      MEMORY[0x1AB32E860](
        &dword_1A9B7C000,
        os_log_obj,
        1,
        "Server bag set, stripping payload keys %@ for sender (known: %{BOOL}d)",
        &key_count,
        18,
        keys_to_strip,
        current_table);
    }
  }
  while ( 1 )
  {
    current_entry = sub_1A9FB8340(payload_dict);
    sub_1A9FBB220();
    processed_entry = sub_1A9FADA20(current_entry);
    MEMORY[0x1AB32EEC0]();
    payload_dict = MEMORY[0x1AB32ED20](processed_entry);
LABEL_9:
    if ( *MEMORY[0x1E6782818] == expected_signature )
      return payload_dict;
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

The implementation relies on two newly introduced functions that handle the configuration and the actual sanitization of the payload. 

First, a dedicated function is used to query the system's Server Bag to retrieve the current configuration values related to known and unknown senders. 

The core logic resides in a second function responsible for stripping the payload keys. This function receives the original payload dictionary and a boolean flag indicating whether the sender is known. Based on this boolean flag, the function selects one of two lookup tables (which correspond to the lists of keys to strip for "known-sender" versus "unknown-sender"). 

The function then queries the Server Bag configuration to verify if the payload stripping feature is currently active. If the feature is enabled, it logs a message indicating that the server bag is set and that it is stripping the payload keys for the sender, explicitly noting the sender's known status. Finally, it iterates through the payload dictionary, removes the keys specified in the selected lookup table, and returns the sanitized dictionary for further processing by the system.

## How to trigger this feature
This feature is triggered automatically during the receipt and processing of an incoming message (such as an iMessage) handled by the `IMSharedUtilities` framework. The system evaluates the sender's identity to determine if they are known or unknown, checks the current Server Bag configuration to see if the sanitization feature is enabled, and if so, processes the message payload through the stripping function before passing it to higher-level frameworks or the BlastDoor service.

## Vulnerability Assessment
This change represents a significant security and privacy mitigation, likely designed to thwart zero-click exploits delivered via malicious message payloads. 

By stripping specific, potentially dangerous keys from payloads—especially those originating from unknown senders—Apple is proactively reducing the attack surface of the messaging stack. Historically, zero-click vulnerabilities in iMessage have relied on attackers sending complex, malformed, or unexpected key-value pairs in the message dictionary to trigger memory corruption (such as Out-of-Bounds reads/writes or Use-After-Free vulnerabilities) or logic bugs in downstream parsers. 

By implementing a Server Bag-controlled sanitization step, Apple can dynamically respond to new exploitation techniques by remotely updating the list of stripped keys without requiring a full iOS firmware update. If left unpatched, the absence of this sanitization would leave the device vulnerable to remote code execution or sandbox escapes via maliciously crafted messages from untrusted sources.

## Evidence
*   **Added Symbols:**
    *   `_IMServerBagValueForKnownSender`
    *   `_IMSharedHelperPayloadByStrippingServerBagKeys`
*   **Added Strings:**
    *   `"Server bag set, stripping payload keys %@ for sender (known: %{BOOL}d)"`
    *   `"known-sender"`
    *   `"unknown-sender"`
    *   `"%@-%@-r1"`

## AI Prioritisation Scoring System

- **Feature Analysis**
  - **Tier**: TIER_1
  - **Category**: Security Mitigation
  - **Reasoning**: Introduces a dynamic, server-configurable payload sanitization mechanism based on sender trust level (known vs. unknown). This is a critical security boundary enforcement designed to mitigate zero-click remote code execution attacks by stripping potentially malicious keys from untrusted message payloads.

