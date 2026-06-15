## What this feature does
This feature implements a server bag (identity) management system for iMessage, specifically handling the logic to determine if a sender is "known" or "unknown" and to strip specific keys from the message payload based on that status. The system uses a lookup table (`_IMServerBagValueForKnownSender`) to check sender identity and a processing function (`_IMSharedHelperPayloadByStrippingServerBagKeys`) to modify the message payload accordingly. The strings "known-sender" and "unknown-sender" suggest a binary classification of contacts, while "Server bag set, stripping payload keys..." indicates a transformation step that removes metadata from the message body before transmission or storage.

## How is it implemented
The implementation consists of two primary functions:

1.  **`_IMServerBagValueForKnownSender` (0x1a9c92778)**: This function appears to be a lookup or calculation routine. It takes a sender identifier (likely a phone number or handle) and returns a value indicating whether the sender is "known". It calls `sub_1A9FBF540` to retrieve data from a global table at `0x1E673F8D0` and `sub_1A9FB8BE0` to process it. The check `((vars8 ^ (2 * vars8)) & 0x4000000000000000LL) != 0` suggests a bit-manipulation check, possibly validating the integrity of the retrieved data or checking a specific flag.

2.  **`_IMSharedHelperPayloadByStrippingServerBagKeys` (0x1a9c927f8)**: This is the core payload processing function. It takes a payload (`a1`), a server bag (`a2`), and a sender type flag (`a3`).
    *   It first determines the sender type (`v21 = 138412546` likely corresponds to `known-sender` or `unknown-sender` based on the string offsets).
    *   It calls `sub_1A9FC0660` (likely a logging or state update function) and `sub_1A9FBF540` (data retrieval).
    *   It uses `sub_1A9FB8BE0` to process the payload.
    *   It calls `sub_1A9FADC40` to validate the result.
    *   **Crucially**, if the sender is known (`v11` resolves to "IMSharedHelper" via `objc_msgSend`), it calls `MEMORY[0x1AB32E860]` with the format string `"Server bag set, stripping payload keys %@ for sender (known: %{BOOL}d)"`. This function call is responsible for actually stripping keys from the payload.
    *   It then enters a loop that processes the payload further, calling `sub_1A9FB8340`, `sub_1A9FADA20`, and various `MEMORY[...]` functions (likely IPC or database operations like `0x1AB32EEC0`, `0x1AB32ED20`, `0x1AB32ED60`, `0x1AB32ED90`, `0x1AB32E7D0`).
    *   The function returns the modified payload (`a1` or a result from `sub_1A9C92980`).

**Call Chain Context:**
The `find_address` results show that the string "Server bag set, stripping payload keys..." is located at `0x1a9f19fca`. The `get_xrefs_to` calls on the string addresses returned empty results, suggesting that the string is not directly referenced by other code in the binary, but is instead passed as an argument to the function `IMSharedHelperPayloadByStrippingServerBagKeys` (as seen in the decompiled output: `MEMORY[0x1AB32E860](..., "Server bag set, stripping payload keys...", ...)`). This implies the string is a constant resource used by the function, rather than a dynamically referenced string in the call graph.

**Data Flow Trace:**
1.  **Input**: Payload (`a1`), Server Bag (`a2`), Sender Type Flag (`a3`).
2.  **Step 1**: Retrieve global data (`sub_1A9FC0660`, `sub_1A9FBF540`).
3.  **Step 2**: Determine if sender is known (`_IMServerBagValueForKnownSender` logic).
4.  **Step 3**: If sender is known (`a3` is true or derived), set a flag (`v21 = 138412546`).
5.  **Step 4**: Call the server bag processing function (`MEMORY[0x1AB32E860]`) with the "Server bag set..." string. This function modifies the payload (`a2`) to strip keys.
6.  **Step 5**: Process the payload in a loop (`sub_1A9FB8340`, `sub_1A9FADA20`, etc.), potentially involving IPC or database lookups.
7.  **Output**: Modified payload.

## How to trigger this feature
The feature is triggered when:
1.  A message is being prepared for transmission or storage.
2.  The sender's identity is available (passed as `a2` or derived).
3.  The system needs to determine if the sender is "known" or "unknown".
4.  The payload needs to be modified based on the sender's status (stripping server bag keys for known senders).
The presence of the `a3` parameter suggests that the caller can explicitly pass a flag indicating whether the sender is known, or the function itself might infer it from the server bag (`a2`). The `if (a3)` check implies that the "known-sender" path is conditional on this flag.

## Evidence
*   **Symbols**:
    *   `_IMServerBagValueForKnownSender`: Added symbol, likely a lookup function for sender identity.
    *   `_IMSharedHelperPayloadByStrippingServerBagKeys`: Added symbol, the main payload processing function.
*   **CStrings**:
    *   `"%@-%@-r1"`: Likely a format string for a server bag key.
    *   `"Server bag set, stripping payload keys %@ for sender (known: %{BOOL}d)"`: The key string used by the payload processing function, indicating the action being performed.
    *   `"known-sender"` and `"unknown-sender"`: Strings used for sender classification.
*   **Addresses**:
    *   `0x1a9c92778`: Address of `_IMServerBagValueForKnownSender`.
    *   `0x1a9c927f8`: Address of `_IMSharedHelperPayloadByStrippingServerBagKeys`.
    *   `0x1a9f19fca`: Address of the "Server bag set..." string.
*   **Decompiled Functions**:
    *   `IMServerBagValueForKnownSender`: Shows logic for determining sender status.
    *   `IMSharedHelperPayloadByStrippingServerBagKeys`: Shows the full flow of payload modification, including the call to the function that uses the "Server bag set..." string.

## AI Prioritisation Scoring System

- **Symbol and String Analysis**
  - **Tier**: TIER_1
  - **Category**: Messaging/Privacy
  - **Reasoning**: Added symbols (_IMServerBagValueForKnownSender, _IMSharedHelperPayloadByStrippingServerBagKeys) and strings ('known-sender', 'unknown-sender', 'Server bag set...') indicate a new feature for managing iMessage sender identity and payload modification. The AUTO-PROMOTE RULES for 'added exported symbols' and 'security/privacy strings' apply. The feature logic involves stripping message keys based on sender status, which is a significant privacy and messaging functionality change.

