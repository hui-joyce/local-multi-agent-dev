## What this feature does
This feature implements a server bag stripping mechanism for iMessage payloads, specifically designed to handle "known-sender" and "unknown-sender" scenarios. The system processes incoming iMessage payloads, identifies the sender type, and conditionally strips specific server bag keys from the payload before returning the cleaned result. This functionality is critical for ensuring that iMessage payloads are properly formatted and stripped of unnecessary server-side metadata before being processed by the client.

## How is it implemented
The feature consists of two main functions: `IMServerBagValueForKnownSender` and `IMSharedHelperPayloadByStrippingServerBagKeys`.

### `IMServerBagValueForKnownSender`
This function retrieves a server bag value for a known sender. It performs the following steps:
1. Calls `sub_1A9FC0660` with a memory address `0x1E6707260` (likely initializing or accessing a global state).
2. Calls `sub_1A9FBF540` with a memory address `0x1E673F8D0` to retrieve some data.
3. Performs a bitwise check on the result (`vars8`) to validate the data.
4. Returns the result of `sub_1A9FB8BE0(v0)`, which likely processes the retrieved data.

### `IMSharedHelperPayloadByStrippingServerBagKeys`
This function is the core implementation for stripping server bag keys from iMessage payloads. It takes three parameters: `a1` (payload), `a2` (sender), and `a3` (known sender flag).

1. **Initialization**:
   - Retrieves a value from memory address `0x1E6782818`.
   - Sets up a `__CFString` pointer (`v5`) based on the `a3` flag (known sender).
   - Calls `sub_1A9FC0660` and `sub_1A9FBF540` (similar to the first function).

2. **Payload Processing**:
   - Calls `sub_1A9FB8BE0(v6)` to process the payload.
   - Calls `MEMORY[0x1AB32EE50](MEMORY[0x1E66FA1C0])` to retrieve some data.
   - Checks if the result of `MEMORY[0x1AB32EE60](v7, v8)` has the least significant bit set. If not, it skips to `LABEL_9`.
   - Calls `sub_1A9FADC40(v7)` to further process the payload.
   - Checks if the result (`v9`) is valid. If not, it skips to `LABEL_9`.
   - Calls `MEMORY[0x1AB32E310](v9, v10)` to check some condition.
   - If the condition is met, it:
     - Calls `MEMORY[0x1AB32E5B0]("IMSharedHelper")` to get the `IMSharedHelper` class.
     - Calls `MEMORY[0x1AB32F200](v11, 1)` to check if the class is valid.
     - Calls `MEMORY[0x1AB32E860]` with the following arguments:
       - `&dword_1A9B7C000` (likely a dictionary or mutable dictionary).
       - `v11` (the `IMSharedHelper` class).
       - `1` (likely a selector).
       - `"Server bag set, stripping payload keys %@ for sender (known: %{BOOL}d)"` (a format string).
       - `&v21` (an integer, set to `138412546`).
       - `18` (likely the length of the format string).
       - `a2` (the sender).
       - `v20` (the `__CFString` pointer).

3. **Loop**:
   - Calls `sub_1A9FB8340(a1)` to process the payload.
   - Calls `sub_1A9FBB220()` (likely a cleanup or logging function).
   - Calls `sub_1A9FADA20(v12)` to process the result.
   - Calls `MEMORY[0x1AB32EEC0]()` (likely a notification or callback).
   - Calls `MEMORY[0x1AB32ED20](v13)` to update `a1`.
   - Checks if the value at `0x1E6782818` matches `v25`. If so, it returns `a1`.
   - Calls `MEMORY[0x1AB32E7F0]()` to retrieve some data (`v15`).
   - Checks if `v16` is `1`. If not, it breaks the loop.
   - Calls `MEMORY[0x1AB32ED60](v15)` to process the data.
   - Calls `MEMORY[0x1AB32ED90](v17)` to further process the data.

4. **Final Step**:
   - Calls `MEMORY[0x1AB32E7D0](v15)` to retrieve some data (`v18`).
   - Calls `sub_1A9C92980(v18)` to return the final result.

### Call Chains and Data Flow
- The `IMSharedHelperPayloadByStrippingServerBagKeys` function is the main entry point for the feature.
- It uses the `IMServerBagValueForKnownSender` function to retrieve server bag values for known senders.
- The function uses the `IMSharedHelper` class to perform the actual stripping of server bag keys.
- The function loops through the payload, processing each item and updating the result until it finds a match or reaches the end of the loop.

## How to trigger this feature
The feature is triggered when an iMessage payload is received and needs to be processed. The `IMSharedHelperPayloadByStrippingServerBagKeys` function is called with the payload, sender, and a flag indicating whether the sender is known. The function then processes the payload, stripping server bag keys based on the sender type.

## Evidence
- **Symbols**:
  - `_IMServerBagValueForKnownSender`: Address `0x1a9c92778`
  - `_IMSharedHelperPayloadByStrippingServerBagKeys`: Address `0x1a9c927f8`
- **CStrings**:
  - `"%@-%@-r1"`
  - `"Server bag set, stripping payload keys %@ for sender (known: %{BOOL}d)"`
  - `"known-sender"`
  - `"unknown-sender"`
- **Addresses**:
  - `0x1a9f19fca`: String data for `"Server bag set, stripping payload keys"`
  - `0x1a9ee5f11`: String data for `"known-sender"` and `"unknown-sender"`
  - `0x1a9eec0c2`: String data for `"known-sender"`
  - `0x1a9eec59a`: String data for `"known-sender"`
  - `0x1a9eec5a7`: String data for `"unknown-sender"`
- **Decompiled Functions**:
  - `IMServerBagValueForKnownSender`: Retrieves server bag value for known sender.
  - `IMSharedHelperPayloadByStrippingServerBagKeys`: Strips server bag keys from iMessage payloads.

## AI Prioritisation Scoring System

- **symbolic_analysis**
  - **Tier**: 1
  - **Category**: messaging
  - **Reasoning**: Added symbols indicate new functionality for server bag handling in iMessage payloads, which is a critical feature for message processing and delivery.

