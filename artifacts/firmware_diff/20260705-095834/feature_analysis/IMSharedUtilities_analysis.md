## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "%@-%@-r1"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 2 (2 AI-authored, 0 auto-generated); comments: 4 (2 AI-authored, 2 auto-generated); across 2 function(s); verified persisted in .i64: 24 named variables, 3 comments.

## What this feature does

The `IMSharedUtilities` framework update introduces a mechanism to dynamically filter and strip specific payload keys from server-side configuration data (the "Server Bag") based on the sender's identity. This feature distinguishes between "known" and "unknown" senders to enforce stricter data sanitization, likely to prevent the leakage of sensitive configuration keys or to ensure compatibility with legacy/restricted client states.

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
        __int64 n_a2,
        int is_known_sender)
{
  __CFString *lookup_table; // x8
  __int64 intermediate_value_1; // x0
  __int64 intermediate_value_2; // x20
  __int64 intermediate_value_3; // x0
  __int64 intermediate_value_4; // x0
  __int64 intermediate_value_5; // x1
  __int64 intermediate_value_6; // x22
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
  intermediate_value_2 = sub_1A9FB8BE0(intermediate_value_1);
  intermediate_value_3 = MEMORY[0x1AB32EE50](MEMORY[0x1E66FA1C0]);
  if ( (MEMORY[0x1AB32EE60](intermediate_value_2, intermediate_value_3) & 1) == 0 )
    goto LABEL_9;
  intermediate_value_4 = sub_1A9FADC40(intermediate_value_2);
  if ( !intermediate_value_4 )
    goto LABEL_9;
  if ( (unsigned int)MEMORY[0x1AB32E310](intermediate_value_4, intermediate_value_5) )
  {
    intermediate_value_6 = MEMORY[0x1AB32E5B0]("IMSharedHelper");
    if ( (unsigned int)MEMORY[0x1AB32F200](intermediate_value_6, 1) )
    {
      key_count = 138412546;
      payload = intermediate_value_2;
      max_size = 1024;
      sender_type = is_known_sender;
      MEMORY[0x1AB32E860](
        &dword_1A9B7C000,
        intermediate_value_6,
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

The implementation centers on the new function `IMSharedHelperPayloadByStrippingServerBagKeys`. This function accepts a payload and a boolean flag indicating the sender's status. It retrieves the current server bag configuration and checks it against a predefined lookup table. 

The logic performs a conditional check: if the sender is identified as "known," it selects a specific set of keys to strip; otherwise, it defaults to a different set. The function iterates through the provided payload entries, comparing them against the determined filter criteria. If a match is found, the key is removed from the payload. The process includes integrated logging that records the stripping action, specifically noting the sender type and the keys being processed, which aids in debugging server-side configuration synchronization. The helper function `IMServerBagValueForKnownSender` acts as a wrapper to retrieve the relevant server bag value, ensuring that the stripping logic operates on the most current and validated configuration state.

## How to trigger this feature

This feature is triggered internally by the `IMSharedHelper` subsystem whenever a server bag payload is received or processed. It is invoked during the parsing of configuration data where the sender's identity is verified. The trigger condition is dependent on the `n_a3` parameter (the sender type boolean), which is determined by the upstream messaging service's classification of the incoming sender.

## Vulnerability Assessment

This update appears to be a hardening measure rather than a direct patch for a critical vulnerability. By explicitly stripping payload keys based on sender identity, the framework reduces the attack surface for potential configuration-based exploits. It prevents "unknown" or potentially untrusted senders from influencing or accessing sensitive server-side configuration parameters that should only be available to "known" (authenticated/trusted) entities. This is a proactive security control designed to enforce the principle of least privilege regarding server bag data access.

## Evidence

- **New Symbols**: `_IMServerBagValueForKnownSender`, `_IMSharedHelperPayloadByStrippingServerBagKeys`
- **New Strings**: `"Server bag set, stripping payload keys %@ for sender (known: %{BOOL}d)"`, `"known-sender"`, `"unknown-sender"`
- **Logic**: The implementation uses a conditional lookup table based on the `sender_type` boolean to determine which keys to strip from the payload, followed by an iterative removal process.

## AI Prioritisation Scoring System

- **static_analysis**
  - **Tier**: TIER_2
  - **Category**: security_hardening
  - **Reasoning**: This is a security-focused hardening update that implements data sanitization for server-side configuration payloads, preventing unauthorized access to sensitive keys based on sender identity.

