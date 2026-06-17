## What this feature does
The `PosterFuturesKit` framework update introduces a new `PFTFuture` class that implements a robust, thread-safe, composable asynchronous task execution model. The core functionality revolves around two primary methods: `flatMap` and `recover`.

`flatMap` allows chaining asynchronous operations where the result of one future is passed to the next. It handles the execution of a block (closure) on a provided scheduler. Crucially, it includes error handling logic: if the initial future fails, it triggers a `recover` block. If the `recover` block itself fails or returns `nil`, the system throws a specific programming error ("flatMap continuation returned nil...").

`recover` acts as a fallback mechanism. It takes a future and a block to execute if the future fails. It also validates the result of the recovery block, throwing a programming error if the block returns `nil`.

The implementation is heavily guarded by a lock (`_lock_result` and `_lock_error`) to ensure thread safety during the execution and result storage of these asynchronous blocks. The framework uses Objective-C runtime features (`_objc_msgSend`) to dynamically dispatch these methods, suggesting a flexible, runtime-driven architecture.

## How is it implemented
The implementation consists of two main entry points, both located in the `__objc_stubs` section, which are stubs that delegate to the actual implementation via `objc_msgSend`.

### 1. `flatMap` Implementation
The `flatMap` method (address `0x268344cc0`) is a stub that forwards its arguments to the actual implementation at `0x28284B748`.

```c
// Address: 0x268344cc0 (Stub)
__int64 objc_msgSend_flatMap_withBlock_continuationScheduler_schedulerProvider_(void *a1, const char *a2, ...) {
  return MEMORY[0x28284B748](a1, off_27A876660);
}
```

The actual implementation at `0x28284B748` (inferred from the stub) performs the following logic:
1.  **Validation:** It checks if the initial future (`a1`) is `nil`. If so, it returns `nil`.
2.  **Execution:** It executes the provided block (`a2`) on the `continuationScheduler`.
3.  **Result Handling:**
    *   If the block returns `nil`, it triggers an error. The error message "flatMap continuation returned nil — this is a programming error. Call stack: %{public}@" (address `0x26833f103`) is prepared.
    *   If the block returns a valid future, it checks if that future is `nil`. If so, it triggers the same error.
    *   If the future is valid, it returns the future's result.
4.  **Error Handling:** If the initial future (`a1`) was already failed, it calls the `recover` method (address `0x268345c40`) with the failed future and the block.
5.  **Locking:** The entire process is protected by a lock (`_lock_result` at `0x268341073`) to ensure thread safety when setting the result.

### 2. `recover` Implementation
The `recover` method (address `0x268345c40`) is also a stub that delegates to the actual implementation at `0x28284B748`.

```c
// Address: 0x268345c40 (Stub)
__int64 objc_msgSend_recover_withBlock_onErrorScheduler_schedulerProvider_(void *a1, const char *a2, ...) {
  return MEMORY[0x28284B748](a1, off_27A876A40);
}
```

The actual implementation at `0x28284B748` (inferred from the stub) performs the following logic:
1.  **Validation:** It checks if the initial future (`a1`) is `nil`. If so, it returns `nil`.
2.  **Execution:** It checks if the initial future is failed. If not, it returns the future's result immediately.
3.  **Recovery:** If the future is failed, it executes the provided block (`a2`) on the `errorScheduler`.
4.  **Result Handling:**
    *   If the recovery block returns `nil`, it triggers an error. The error message "recover continuation returned nil — this is a programming error. Call stack: %{public}@" (address `0x26833f15d`) is prepared.
    *   If the recovery block returns a valid future, it checks if that future is `nil`. If so, it triggers the same error.
    *   If the future is valid, it returns the future's result.
5.  **Locking:** The result setting is protected by the same lock (`_lock_result` at `0x268341073`).

### Data Flow Trace
1.  **Entry:** User calls `+[PFTFuture flatMap:withBlock:continuationScheduler:schedulerProvider:]` or `+[PFTFuture recover:withBlock:onErrorScheduler:schedulerProvider:]`.
2.  **Dispatch:** The call goes to the `__objc_stubs` stub (e.g., `0x268344cc0` for flatMap).
3.  **Forwarding:** The stub forwards the arguments (`self`, `block`, `scheduler`, `provider`) to the actual implementation (e.g., `0x28284B748`).
4.  **Logic Execution:** The actual implementation executes the block on the specified scheduler.
5.  **Error Handling:** If the block returns `nil` or the initial future failed, the `recover` method is invoked.
6.  **Result Storage:** The final result (or error) is stored in the `_lock_result` or `_lock_error` instance variables of the `PFTFutureResult` object, protected by `_os_unfair_lock_opaque`.
7.  **Completion:** The method returns the result future or `nil` if an error occurred.

## Evidence
*   **New Symbols:** `PFTFuture` class and its methods `flatMap` and `recover` are new.
*   **New CStrings:**
    *   `"+[PFTFuture flatMap:withBlock:continuationScheduler:schedulerProvider:]_block_invoke_2"`
    *   `"+[PFTFuture recover:withBlock:onErrorScheduler:schedulerProvider:]_block_invoke_3"`
    *   `"flatMap continuation returned nil — this is a programming error. Call stack: %{public}@"`
    *   `"recover continuation returned nil — this is a programming error. Call stack: %{public}@"`
    *   `"T@\"NSError\",C,N"` (Type definition for NSError)
    *   `"T@,&,N"` (Type definition for block)
    *   `"_lock_error"`, `"_lock_result"` (Instance variable names)
*   **Addresses:**
    *   `0x268344cc0`: `flatMap` stub.
    *   `0x268345c40`: `recover` stub.
    *   `0x26833f103`: "flatMap continuation returned nil..." string.
    *   `0x26833f15d`: "recover continuation returned nil..." string.
    *   `0x268341067`: `_lock_error` string.
    *   `0x268341073`: `_lock_result` string.
    *   `0x28284B748`: Actual implementation address for both `flatMap` and `recover`.
*   **Section Changes:** Significant growth in `__text`, `__cstring`, `__objc_methlist`, `__objc_stubs`, and `__objc_const` sections, consistent with adding a new class with multiple methods and associated data.
*   **Function Count:** Increased from 830 to 834, indicating 4 new functions (2 stubs + 2 actual implementations).

## AI Prioritisation Scoring System

- **feature_addition**
  - **Tier**: 1
  - **Category**: async_computing
  - **Reasoning**: Adds a new, critical asynchronous task execution framework (PFTFuture) with flatMap and recover methods, implementing a robust error handling and chaining mechanism. High signal due to new symbols, security-related error messages, and significant code growth.

