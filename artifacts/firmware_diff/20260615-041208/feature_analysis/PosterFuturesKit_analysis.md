## What this feature does
The PosterFuturesKit framework update introduces a new `PFTFutureResult` class alongside the existing `PFTFuture` class, implementing a robust Future/Promise pattern with explicit error handling and result management. The new class adds thread-safe locking mechanisms (`_lock`, `_lock_error`, `_lock_result`) to coordinate access to the `_error` and `_result` properties, preventing race conditions during state transitions. The update also adds new error handling paths for `flatMap` and `recover` operations, introducing specific error messages when continuations return `nil` (indicating a programming error).

## How is it implemented
The implementation consists of two primary classes: `PFTFuture` and the newly added `PFTFutureResult`.

**PFTFuture (Existing):**
- Implements `flatMap:withBlock:continuationScheduler:schedulerProvider:` and `recover:withBlock:onErrorScheduler:schedulerProvider:` methods.
- Uses blocks to handle success and failure cases.
- The `flatMap` method chains futures, while `recover` handles errors.
- New error messages were added for when continuations return `nil`:
  - `"flatMap continuation returned nil — this is a programming error. Call stack: %{public}@"`
  - `"recover continuation returned nil — this is a programming error. Call stack: %{public}@"`

**PFTFutureResult (New):**
- A new class added in this update to represent the resolved state of a Future.
- Contains properties:
  - `_error`: Stores the error if the future failed.
  - `_result`: Stores the result if the future succeeded.
  - `_lock`: An `_os_unfair_lock` for thread-safe access.
  - `_lock_error`: Lock specifically for the `_error` property.
  - `_lock_result`: Lock specifically for the `_result` property.
- The class uses locks to ensure that only one of `_error` or `_result` is set at any given time, preventing concurrent modification issues.

**Data Flow:**
1. When a `PFTFuture` completes, it creates a `PFTFutureResult` object.
2. The result object's `_result` or `_error` property is set based on the future's outcome.
3. The locks (`_lock`, `_lock_error`, `_lock_result`) are used to synchronize access to these properties, ensuring thread safety.
4. If a `flatMap` or `recover` continuation returns `nil`, a specific error is thrown with a message indicating a programming error.

**Decompiled Pseudocode (Inferred):**
```c
// PFTFutureResult class
class PFTFutureResult {
    id _error;
    id _result;
    _os_unfair_lock _lock;
    _os_unfair_lock _lock_error;
    _os_unfair_lock _lock_result;

    // Initialization
    - (instancetype)init {
        self = [super init];
        _lock = _os_unfair_lock_create();
        _lock_error = _os_unfair_lock_create();
        _lock_result = _os_unfair_lock_create();
        _error = nil;
        _result = nil;
        return self;
    }

    // Set result with locking
    - (void)setResult:(id)result {
        _os_unfair_lock_lock(&_lock);
        _result = result;
        _os_unfair_lock_unlock(&_lock);
    }

    // Set error with locking
    - (void)setError:(id)error {
        _os_unfair_lock_lock(&_lock_error);
        _error = error;
        _os_unfair_lock_unlock(&_lock_error);
    }

    // Get result with locking
    - (id)result {
        id res = nil;
        _os_unfair_lock_lock(&_lock_result);
        res = _result;
        _os_unfair_lock_unlock(&_lock_result);
        return res;
    }

    // Get error with locking
    - (id)error {
        id err = nil;
        _os_unfair_lock_lock(&_lock_error);
        err = _error;
        _os_unfair_lock_unlock(&_lock_error);
        return err;
    }
}

// PFTFuture methods (updated with new error handling)
- (void)flatMap:(id (^)(id))block continuationScheduler:(id)continuationScheduler schedulerProvider:(id)schedulerProvider {
    // ... existing logic ...
    id continuation = block(result);
    if (continuation == nil) {
        // New error handling
        NSError *error = [NSError errorWithDomain:@"PFTFuture" code:1001 userInfo:@{NSLocalizedDescriptionKey: @"flatMap continuation returned nil — this is a programming error. Call stack: %{public}@"}];
        [self completeWithError:error];
    } else {
        // Continue with the chained future
        [continuation continueWithBlock:^{ ... }];
    }
}

- (void)recover:(id (^)(id))block onErrorScheduler:(id)onErrorScheduler {
    // ... existing logic ...
    id continuation = block(error);
    if (continuation == nil) {
        // New error handling
        NSError *error = [NSError errorWithDomain:@"PFTFuture" code:1002 userInfo:@{NSLocalizedDescriptionKey: @"recover continuation returned nil — this is a programming error. Call stack: %{public}@"}];
        [self completeWithError:error];
    } else {
        // Continue with the recovery block
        [continuation continueWithBlock:^{ ... }];
    }
}
```

## How to trigger this feature
The feature is triggered when a `PFTFuture` is created and subsequently completed (either successfully or with an error). The new `PFTFutureResult` class is instantiated when the future completes, and its properties are set based on the future's outcome. The new error handling paths in `flatMap` and `recover` are triggered when the respective continuation blocks return `nil`.

**Trigger Conditions:**
1. **Future Completion:** When a `PFTFuture` completes (either with a result or an error), a `PFTFutureResult` object is created.
2. **flatMap Continuation Returns Nil:** When the `flatMap` method's continuation block returns `nil`, a `PFTFutureResult` is created with an error indicating a programming error.
3. **recover Continuation Returns Nil:** When the `recover` method's continuation block returns `nil`, a `PFTFutureResult` is created with an error indicating a programming error.

## Evidence
- **New Symbols:**
  - `-[PFTFutureResult init]`: Initialization method for the new `PFTFutureResult` class.
  - `_OBJC_IVAR_$_PFTFutureResult._lock`: Lock for the result object.
  - `_OBJC_IVAR_$_PFTFutureResult._lock_error`: Lock for the error property.
  - `_OBJC_IVAR_$_PFTFutureResult._lock_result`: Lock for the result property.
  - `__BSIsInternalInstall`: Internal installation flag.
  - `__OBJC_$_PROP_LIST_PFTFuture.181`: Property list for `PFTFuture`.
  - `___66+[PFTFuture recover:withBlock:onErrorScheduler:schedulerProvider:]_block_invoke.12`: Block for `recover` method.
  - `___71+[PFTFuture flatMap:withBlock:continuationScheduler:schedulerProvider:]_block_invoke.8`: Block for `flatMap` method.
  - `___71+[PFTFuture flatMap:withBlock:continuationScheduler:schedulerProvider:]_block_invoke_2.10`: Block for `flatMap` method (continued).
  - `___71+[PFTFuture flatMap:withBlock:continuationScheduler:schedulerProvider:]_block_invoke_2.cold.1`: Cold path for `flatMap` method.
  - `___66+[PFTFuture recover:withBlock:onErrorScheduler:schedulerProvider:]_block_invoke_4`: Block for `recover` method (continued).
  - `___71+[PFTFuture flatMap:withBlock:continuationScheduler:schedulerProvider:]_block_invoke_3`: Block for `flatMap` method (continued).
  - `___71+[PFTFuture flatMap:withBlock:continuationScheduler:schedulerProvider:]_block_invoke_4`: Block for `flatMap` method (continued).
  - `_objc_msgSend$setResult:`: Method to set the result.

- **New CStrings:**
  - `"+[PFTFuture flatMap:withBlock:continuationScheduler:schedulerProvider:]_block_invoke_2"`: Method selector for `flatMap` block.
  - `"+[PFTFuture recover:withBlock:onErrorScheduler:schedulerProvider:]_block_invoke_3"`: Method selector for `recover` block.
  - `"T@\"NSError\",C,N"`: Type string for `NSError`.
  - `"T@,&,N"`: Type string for `id`.
  - `"_lock_error"`: Lock variable name.
  - `"_lock_result"`: Lock variable name.
  - `"flatMap continuation returned nil — this is a programming error. Call stack: %{public}@"`: Error message for `flatMap` continuation returning `nil`.
  - `"recover continuation returned nil — this is a programming error. Call stack: %{public}@"`: Error message for `recover` continuation returning `nil`.
  - `"{os_unfair_lock_s=\"_os_unfair_lock_opaque\"I}"`: Type string for `_os_unfair_lock`.
  - `"T@\"NSError\",C,N,V_error"`: Type string for `NSError` with `error` property.
  - `"T@,&,N,V_result"`: Type string for `id` with `result` property.

- **Section Changes:**
  - `__TEXT.__text`: Increased by 0x4f0 (1216 bytes).
  - `__TEXT.__auth_stubs`: Increased by 0x10 (16 bytes).
  - `__TEXT.__objc_methlist`: Increased by 0x8 (8 bytes).
  - `__TEXT.__cstring`: Increased by 0xa2 (162 bytes).
  - `__TEXT.__gcc_except_tab`: Increased by 0x10 (16 bytes).
  - `__TEXT.__oslogstring`: Increased by 0x34 (52 bytes).
  - `__TEXT.__unwind_info`: Increased by 0x40 (64 bytes).
  - `__TEXT.__objc_classname`: Unchanged.
  - `__TEXT.__objc_methname`: Increased by 0x8 (8 bytes).
  - `__TEXT.__objc_methtype`: Increased by 0x27 (39 bytes).
  - `__TEXT.__objc_stubs`: Increased by 0x40 (64 bytes).
  - `__DATA_CONST.__got`: Increased by 0x8 (8 bytes).
  - `__DATA_CONST.__const`: Increased by 0x1e0 (480 bytes).
  - `__DATA_CONST.__objc_classlist`: Unchanged.
  - `__DATA_CONST.__objc_protolist`: Unchanged.
  - `__DATA_CONST.__objc_imageinfo`: Unchanged.
  - `__DATA_CONST.__objc_selrefs`: Increased by 0x10 (16 bytes).
  - `__DATA_CONST.__objc_superrefs`: Increased by 0x8 (8 bytes).
  - `__AUTH_CONST.__auth_got`: Increased by 0x8 (8 bytes).
  - `__AUTH_CONST.__auth_ptr`: Unchanged.
  - `__AUTH_CONST.__const`: Increased by 0x28 (40 bytes).
  - `__AUTH_CONST.__cfstring`: Decreased by 0x20 (32 bytes).
  - `__AUTH_CONST.__objc_const`: Increased by 0x20 (32 bytes).
  - `__AUTH.__objc_data`: Increased by 0x8 (8 bytes).
  - `__DATA.__objc_ivar`: Increased by 0x4 (4 bytes).
  - `__DATA.__data`: Increased by 0x18 (24 bytes).
  - `__DATA.__bss`: Increased by 0x28 (40 bytes).
  - `__DATA_DIRTY.__objc_data`: Increased by 0x40 (64 bytes).

- **UUID Change:**
  - From `0C3084AE-DC6D-3DDF-AE9D-1445DCF64007` to `6D1299D4-040A-3574-BF99-3224EC118DE0`.

- **Function Count Change:**
  - From 830 to 834 (+4 functions).

- **Symbol Count Change:**
  - From 3140 to 3146 (+6 symbols).

- **CString Count Change:**
  - From 952 to 957 (+5 strings).