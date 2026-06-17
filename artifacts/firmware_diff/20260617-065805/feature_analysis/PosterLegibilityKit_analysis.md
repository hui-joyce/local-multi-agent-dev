## What this feature does
The `PosterLegibilityKit` framework update introduces a new runtime check for the `isFinished` state of an Objective-C message send operation. This feature appears to be a guard mechanism that verifies whether a specific asynchronous or deferred operation (likely related to text layout or rendering, given the "PosterLegibility" context) has completed before proceeding. The new symbol `_objc_msgSend$isFinished` suggests a custom wrapper or patch around the standard `objc_msgSend` function to inject this state check, potentially preventing race conditions or ensuring proper synchronization in the rendering pipeline.

## How is it implemented
The implementation consists of a new stub function `_objc_msgSend$isFinished` located at address `0x222f82a40` within the `__objc_stubs` section. This function acts as a thin wrapper that delegates the actual work to an existing function at address `0x28284B748`.

The decompiled pseudocode for the new stub is as follows:

```c
__int64 objc_msgSend_isFinished(void *a1, const char *a2, ...)
{
  // Delegate to the existing implementation at 0x28284B748
  // Arguments are passed through: a1 (likely the receiver object), a2 (selector string)
  return MEMORY[0x28284B748](a1, off_2790941A0);
}
```

**Analysis of the Call Chain:**
1.  **Entry Point:** The new symbol `_objc_msgSend$isFinished` is the entry point for this feature.
2.  **Delegation:** It immediately calls the function at `0x28284B748`.
3.  **Argument Handling:** The second argument `a2` (the selector string) is not passed directly to the target function. Instead, it is replaced by a constant offset `off_2790941A0`. This suggests the target function at `0x28284B748` expects a specific internal representation of the selector or a pre-computed value rather than the raw string.
4.  **Return Value:** The return value of the target function is returned directly.

**Data Flow Trace:**
*   The feature intercepts calls to `_objc_msgSend$isFinished`.
*   It forwards the receiver (`a1`) and a transformed selector argument to the underlying logic at `0x28284B748`.
*   The underlying logic determines the "finished" state and returns a boolean or status code.
*   The string "isFinished" (at `0x222f7e3b7`) serves as the selector name for this new method, indicating that this stub is registered in the Objective-C runtime's method table.

**Note on Unresolved Address:**
The address `0x28284B748` referenced in the decompiled function could not be resolved via `find_address`. This indicates that the function at this address is either:
1.  An internal implementation detail of the `objc_msgSend` machinery itself (e.g., a helper within the runtime).
2.  A function that was removed or renamed in the current binary version, leaving a dangling reference in the stub.
3.  Located in a different binary component that is not part of the current diff analysis scope.

Given the context of `PosterLegibilityKit`, the function at `0x28284B748` likely contains the core logic for checking the completion status of a layout or rendering task, utilizing the `off_2790941A0` offset to look up the specific selector's state within a global or class-specific data structure.

## How to trigger this feature
This feature is triggered dynamically by the Objective-C runtime when a message is sent to an object that has the selector `isFinished` registered.
1.  **Selector Registration:** The string "isFinished" is added to the `__objc_selrefs` section (size increased from `0x1210` to `0x1218`), meaning a new method named `isFinished` is now available on the objects handled by this framework.
2.  **Runtime Invocation:** Any code that calls `[object isFinished]` will be routed through the new `_objc_msgSend$isFinished` stub.
3.  **Execution Path:** The stub executes the logic at `0x28284B748` to determine the result.

It is likely invoked by higher-level components in the rendering pipeline (e.g., `PosterLegibilityKit`'s main rendering loop or a dependent framework) to check if a specific text layout or image processing task is complete before proceeding to the next step.

## Evidence
*   **New Symbol:** `_objc_msgSend$isFinished` (Address: `0x222f82a40`, Segment: `__objc_stubs`). This is a code stub added to the binary.
*   **New String:** `"isFinished"` (Address: `0x222f7e3b7`). This is the selector name associated with the new symbol.
*   **Symbol Count Change:** Increased by 1 (2864 -> 2865).
*   **String Count Change:** Increased by 1 (1389 -> 1390).
*   **Section Drift:**
    *   `__TEXT.__text`: Increased by 0x24 (36 bytes).
    *   `__TEXT.__objc_methname`: Increased by 0x9 (9 bytes).
    *   `__TEXT.__objc_stubs`: Increased by 0x20 (32 bytes).
    *   `__DATA_CONST.__objc_selrefs`: Increased by 0x8 (8 bytes).
*   **Dependency Changes:**
    *   Removed dependency: `/usr/lib/libMobileGestalt.dylib`.
    *   Removed dependency: `/usr/lib/libSystem.B.dylib`.
    *   Removed dependency: `/usr/lib/libobjc.A.dylib`.
*   **UUID Change:** Changed from `B427C366-ACD1-38E7-AE36-A084DFDE649E` to `7A7CD13A-C2E7-399F-B171-8C4C73314537`. This indicates a complete re-signing or re-identification of the framework binary, often accompanying significant internal changes.
*   **Decompiled Function:**
    ```c
    __int64 objc_msgSend_isFinished(void *a1, const char *a2, ...)
    {
      return MEMORY[0x28284B748](a1, off_2790941A0);
    }
    ```

## AI Prioritisation Scoring System

- **Symbol/String Analysis + Decompilation**
  - **Tier**: TIER_2
  - **Category**: Runtime/IPC
  - **Reasoning**: The diff shows the addition of a new Objective-C method '_objc_msgSend$isFinished' and the corresponding selector string 'isFinished'. The decompiled stub reveals a delegation pattern to an internal function at 0x28284B748, implementing a state check. This suggests a new feature for checking the completion status of operations within the PosterLegibilityKit rendering pipeline. While the UUID change is significant, the specific addition of a runtime check for 'isFinished' is a functional change rather than just a version bump, warranting a TIER_2 classification.

