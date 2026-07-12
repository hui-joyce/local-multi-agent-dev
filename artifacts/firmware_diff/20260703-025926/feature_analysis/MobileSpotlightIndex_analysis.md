## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "%s:%d: Detected recurring crashes %lu hour window"`
- **Analysis mode**: evidence_only
- **Database annotations** — variable renames: 0 (0 AI-authored, 0 auto-generated); comments: 0 (0 AI-authored, 0 auto-generated); across 0 function(s); verified persisted in .i64: 0 named variables, 0 comments.

## What this feature does

The `MobileSpotlightIndex` component has undergone a significant update focused on enhancing index integrity, crash recovery, and localized data formatting. The primary functional changes include the introduction of a new class, `SRQueryNumberFormatters`, to handle locale-aware number and currency formatting, and the implementation of more robust error handling and state validation for index operations. The update also introduces new telemetry and signposting mechanisms to track index rebuilds and recurring crash states, providing better visibility into the health of the Spotlight indexing subsystem.

## How is it implemented


_No decompilation was captured for this component (the analyzer did not call `decompile_function`); the description below is derived from the symbol-level diff evidence, not from decompiled code._

The implementation changes are evidenced by the addition of the `SRQueryNumberFormatters` Objective-C class, which includes methods for initialization (`initWithLocale:`) and memory management (`dealloc`), along with instance variables for various formatters (`_currencyDecimalFormatter`, `_currencyFormatter`, `_decimalFormatter`, `_numberFormatter`). 

The binary diff reveals a shift toward stricter index state management. Numerous new error strings indicate that the system now explicitly checks for read-only index states before performing operations like `SIDeleteCSItems`, `SIBulkSetAttributes`, `SISetCodedAttributes`, and `processOneCS`. Furthermore, the addition of `SpotlightDisableIndexRebuild` suggests a new configuration-based mechanism to prevent index rebuilds under specific conditions. 

The telemetry footprint has expanded significantly, with new signposts for crash state tracking (`check_crash_state_signpost`) and detailed failure logging that captures process IDs, error codes, and memory offsets. The proliferation of `GCC_except_table` symbols and `block_invoke` functions suggests a refactoring of internal index processing logic, likely to improve concurrency or error handling during complex operations like `InnerMerge`, `OuterMerge`, and `PayloadIterate`.

## How to trigger this feature

This feature is triggered by standard Spotlight indexing operations, particularly those involving contact graph data or localized search queries. The new crash tracking logic is triggered automatically when the system detects recurring crashes within a specific time window (e.g., the new "1 hour" window vs. the previous "3 hour" window). The read-only index checks are triggered whenever a write operation is attempted on a locked or read-only index volume.

## Vulnerability Assessment

The changes appear to be a mix of stability improvements and defensive programming. The explicit checks for "index is read-only" across multiple API entry points suggest a mitigation against potential race conditions or state-inconsistency vulnerabilities where write operations might have previously been attempted on invalid index states. The refinement of the crash detection window (from 3 hours to 1 hour) indicates a more aggressive posture toward identifying and potentially disabling problematic indexing tasks to prevent system instability. No direct evidence of a memory-safety vulnerability patch (like a UAF or OOB) is present, but the increased use of `__message_assert` and `__si_assert_copy_extra` suggests a hardening of internal data structures and consistency checks.

## Evidence

- **New Class:** `SRQueryNumberFormatters` (with associated ivars and methods).
- **New Strings:** 
    - `"%s:%d: Detected recurring crashes %lu hour window"`
    - `"%s:%d: Index rebuild disabled by SpotlightDisableIndexRebuild"`
    - `"SIBulkSetAttributes failed: index is read-only"`
    - `"Cannot delete in SIDeleteCSItems because the index is read-only"`
- **Telemetry:** `check_crash_state_signpost`, `com.apple.spotlight.trace`.
- **Logic Changes:** Increased use of `__si_assert_copy_extra` and `__message_assert` across various index operations.

## AI Prioritisation Scoring System

- **binary_diff_analysis**
  - **Tier**: TIER_2
  - **Category**: system_stability_and_telemetry
  - **Reasoning**: The component update introduces significant new telemetry, state validation, and locale-aware formatting logic. While not a direct security patch, the hardening of index state checks and crash detection mechanisms represents a meaningful improvement to system reliability and internal subsystem integrity.

