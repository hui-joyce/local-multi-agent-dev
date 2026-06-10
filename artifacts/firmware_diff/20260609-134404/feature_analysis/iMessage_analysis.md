## What this feature does
This feature introduces a new server-side payload processing mechanism for iMessage group chats, specifically designed to handle and strip "server bag keys" from incoming message payloads. The addition of the symbol `_IMSharedHelperPayloadByStrippingServerBagKeys` indicates a new utility function that processes message data structures. The feature appears to be related to the "MessageGroupController" and involves logic for determining whether a group message payload should be accepted based on existing chat state, sender knowledge, and message type. It also includes functionality to track how many times a thread has been responded to.

## How is it implemented
The implementation consists of several interconnected components:

1.  **Payload Stripping Utility (`_IMSharedHelperPayloadByStrippingServerBagKeys` at `0xc7210`)**:
    *   This is a newly added exported symbol, suggesting it's a standalone helper function.
    *   The name implies it takes a payload (likely a dictionary or structured data) and removes specific keys associated with a "server bag". This is a common pattern in secure messaging to prevent server-side metadata from leaking into the client-side view of the message.
    *   The hex string `"B36@0:8@16B24@28"` found at `0x112581` is a Swift struct definition. In Swift's ABI, this format describes a struct with 3 properties (`36` bits for the struct itself, `8` bits for the first property, `16` bits for the second, `24` bits for the third, `28` bits for the fourth). This suggests the payload being manipulated is a complex Swift struct, likely conforming to a protocol like `IMSharedHelperPayload`.

2.  **Message Group Controller Integration (`MessageGroupController-strip-payload-keys` at `0xe529e`)**:
    *   This Objective-C method name points to a method within the `MessageGroupController` class.
    *   The method name `strip-payload-keys` directly correlates with the new helper function. It suggests that `MessageGroupController` now calls this new helper to sanitize incoming group message payloads before processing them.
    *   This method is located at `0xe529e`.

3.  **Message Acceptance Logic (`_shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:` at `0x102463`)**:
    *   This is a new Objective-C method selector (method name with parameters).
    *   The parameters suggest a decision-making process:
        *   `existingChat`: A boolean or object indicating if a chat with the sender already exists.
        *   `isKnownSender`: A boolean indicating if the sender is a known contact.
        *   `type`: The type of the message payload.
    *   This method likely implements the logic to decide whether a new group message should be added to the user's chat list or if it should be merged into an existing thread. This is crucial for managing group chat history and preventing duplicate or unwanted threads.

4.  **Thread Response Tracking (`getNumberOfTimesRespondedToThread` at `0x10623e`)**:
    *   This method retrieves a count of how many times a specific thread has been responded to.
    *   This functionality is likely used for UI updates (e.g., showing a "3 people responded" badge) or for server-side logic to manage thread activity.

**Data Flow Hypothesis**:
When a group message arrives, the `MessageGroupController` receives the raw payload. It first calls `strip-payload-keys` (using the new helper) to remove server-side metadata. Then, it likely calls `_shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:` to determine if this message should create a new chat thread or be appended to an existing one. Finally, it might update the response count for the thread using `getNumberOfTimesRespondedToThread`.

## How to trigger this feature
The feature is triggered by the receipt of a new group message payload that requires processing under the new logic. Specifically:

1.  **Payload Reception**: The `iMessage` service receives a group message payload from the server.
2.  **Payload Sanitization**: The `MessageGroupController` intercepts the payload and invokes the new `strip-payload-keys` method. This happens automatically upon message arrival.
3.  **Thread Decision**: The controller then evaluates the message against the new acceptance logic (`_shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:`).
    *   If the sender is unknown and no chat exists, a new thread is created.
    *   If the sender is known or a chat exists, the message is appended to the existing thread.
4.  **UI Update**: If the message is accepted into a thread, the `getNumberOfTimesRespondedToThread` method is likely called to update the UI with the latest response count.

The feature is tightly coupled with the group chat management system and is activated whenever a group message is delivered to the device.

## Evidence
*   **New Symbol**: `_IMSharedHelperPayloadByStrippingServerBagKeys` (Address: `0xc7210`). This is the core new functionality for sanitizing payloads.
*   **New Struct Definition**: `"B36@0:8@16B24@28"` (Address: `0x112581`). This defines the memory layout of the payload struct being manipulated, confirming the data structure involved.
*   **New Method**: `MessageGroupController-strip-payload-keys` (Address: `0xe529e`). This shows the integration point in the main group chat controller, indicating the new sanitization step is part of the message handling pipeline.
*   **New Method Selector**: `_shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:` (Address: `0x102463`). This provides the logic for managing chat threads based on sender and message type.
*   **New Method**: `getNumberOfTimesRespondedToThread` (Address: `0x10623e`). This adds functionality for tracking and reporting thread activity.
*   **Metadata Changes**:
    *   **Version Bump**: `1450.500.221.2.9` -> `1450.500.221.2.14`. Indicates a significant update.
    *   **Symbol Count**: `892` -> `893`. Confirms one new symbol was added.
    *   **CStrings Count**: `5119` -> `5124`. Confirms 5 new strings were added, matching our findings.
    *   **UUID Change**: `95C89B97-D474-32AB-83F0-DFAC73717D2C` -> `3BBE6D71-A477-31DA-A41C-1FDFE5C36B8F`. The binary's bundle identifier or signing key has changed, which is expected in a new build.
    *   **Address Shifts**: All section addresses (`__TEXT.__text`, `__TEXT.__auth_stubs`, etc.) have shifted slightly, which is normal due to the addition of new code and data.

## AI Prioritisation Scoring System

- **Symbol Analysis + String Search**
  - **Tier**: TIER_2
  - **Category**: DATA/IPC/SYNC
  - **Reasoning**: The feature introduces a new payload sanitization mechanism for iMessage group chats, specifically targeting the removal of server-side metadata ('server bag keys'). This is a significant change to the data handling pipeline, affecting how group messages are processed and stored. While not a critical security vulnerability (TIER_1), it represents a substantial change in data privacy and message integrity handling, making it higher priority than minor UI or logging changes. The implementation involves new helper functions and logic for thread management, impacting the core group chat experience.

