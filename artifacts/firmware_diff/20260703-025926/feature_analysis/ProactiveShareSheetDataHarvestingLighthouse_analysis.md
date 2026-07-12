## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "@\"NSDictionary\"8@?0"`
- **Analysis mode**: evidence_only
- **Database annotations** — variable renames: 0 (0 AI-authored, 0 auto-generated); comments: 0 (0 AI-authored, 0 auto-generated); across 0 function(s); verified persisted in .i64: 0 named variables, 0 comments.
- **Apple Security Notes**: matches advisory component `Share Sheet` — Apple confirms a security-relevant change here; this analysis examines the likely vulnerability patch.

## What this feature does

The `ProactiveShareSheetDataHarvestingLighthouse` framework has undergone a significant architectural shift in the transition from iOS 17.0.3 to 17.1. The component has moved away from a generic `MLBatchProvider`-based evaluation system toward a specialized, tightly integrated "Shadow Evaluation" pipeline for People Suggester. This system is designed to harvest share sheet interaction data, label it with engagement evidence, and perform "shadow" evaluations of CoreML models—running new models in the background against real-world data to compare their performance against production models without impacting the user experience.

## How is it implemented


_No decompilation was captured for this component (the analyzer did not call `decompile_function`); the description below is derived from the symbol-level diff evidence, not from decompiled code._

The implementation shift is evidenced by the complete removal of the `LCFShadowEvaluation` and `MLBatchProvider` Objective-C classes, replaced by a Swift-centric architecture. The binary now includes extensive support for `PeopleSuggester` and `CoreML` integration, as indicated by the new `__swift_FORCE_LOAD_` symbols for `swiftCoreLocation`, `swiftFileProvider`, `swiftIntents`, and `swiftUniformTypeIdentifiers`.

The logic has transitioned from a generic batch-processing model to a domain-specific `ShadowEvaluationManager`. The new code utilizes `BMMLSELabeledDataStore` to manage labeled data streams and `_PSCoreMLScoringModel` for candidate scoring. The binary diff shows a significant increase in the `__TEXT` section (from 0x4a7b8 to 0x506e4) and a jump in function count (845 to 939), reflecting the addition of complex Swift-based data structures and dictionary-based storage for feature vectors. The framework now explicitly handles model configuration via `getModelURL:` and `getModelConfig:`, and includes robust error handling for missing labeling evidence or model availability, ensuring that shadow evaluations do not proceed if the necessary scoring model class is unavailable.

## How to trigger this feature

The feature is triggered by the `com.apple.proactive.shareheet.peoplesuggester.shadowEvaluation` subsystem. It is likely activated during share sheet interactions where the system collects "labeling evidence" (e.g., user engagement with suggested recipients). The system processes these events in batches, checks for the presence of a positive label, and if the criteria are met, invokes the `ShadowEvaluationManager` to score candidates against the current CoreML model configuration.

## Vulnerability Assessment

1. **Security-relevant change**: The update replaces a generic, potentially loosely-typed `MLBatchProvider` interface with a strictly defined, domain-specific `LabeledDataStore` and `ShadowEvaluationManager`.
2. **Patch mechanism**: The new implementation introduces explicit validation checks for model configuration and labeling evidence (e.g., "Feature %s is missing a value", "Share event %s missing positive label, skipping"). By moving to a strongly-typed Swift implementation and enforcing these checks, the system mitigates risks associated with malformed input data or invalid model states that could have previously led to undefined behavior or crashes in the `LCFShadowEvaluation` pipeline.
3. **Evidence**: The removal of `LCFShadowEvaluation` and the addition of specific error-handling strings like "Share event %s missing positive label, skipping" and "Feature %s is missing a value" indicate a hardening of the data ingestion pipeline. The transition to Swift-based dictionary storage and the use of `BMMLSELabeledDataStore` provide better memory safety and type enforcement compared to the previous Objective-C `MLBatchProvider` implementation.

## Evidence

- **Removed Classes**: `LCFShadowEvaluation`, `LCFProactivePredictionRanker`, `LCFProactiveMetricsComputation`.
- **Added Symbols**: `_OBJC_CLASS_$__PSCoreMLScoringModel`, `_OBJC_CLASS_$__PSPredictionContext`, `_OBJC_CLASS_$_BMMLSELabeledDataStoreFeature`.
- **New Strings**: "com.apple.proactive.shareheet.peoplesuggester.shadowEvaluation", "Share event %s missing positive label, skipping", "Error reading labelled data stream: %@".
- **Binary Changes**: `__TEXT` section size increase (+0x5f2c), function count increase (+94), and new dylib dependencies on `PeopleSuggester` and various Swift libraries.

## AI Prioritisation Scoring System

- **binary_diff_analysis**
  - **Tier**: TIER_1
  - **Category**: privacy_sensitive_framework
  - **Reasoning**: The component handles sensitive user interaction data for ML model training and evaluation. The architectural shift to a more robust, type-safe, and validated data harvesting pipeline represents a significant security and privacy-relevant update to how share sheet engagement data is processed.

