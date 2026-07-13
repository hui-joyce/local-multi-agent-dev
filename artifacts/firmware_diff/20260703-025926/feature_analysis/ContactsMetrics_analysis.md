## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "FractionAreCustom"`
- **Analysis mode**: evidence_only
- **Database annotations** — variable renames: 0 (0 AI-authored, 0 auto-generated); comments: 3 (3 AI-authored, 0 auto-generated); across 1 function(s); verified persisted in .i64: 0 named variables, 0 comments.
- **Apple Security Notes**: matches advisory component `Contacts` — Apple confirms a security-relevant change here; this analysis examines the likely vulnerability patch.

## What this feature does

The `ContactsMetrics` framework update introduces a new telemetry and analytics subsystem focused on tracking user interaction with "Posters" within the Contacts application. The framework now collects granular data regarding the composition and configuration of contact posters, including the total count of posters, the types of posters used (Memoji, Monogram, Photo, Custom), and the update status of these posters.

## How is it implemented


_No decompilation was captured for this component (the analyzer did not call `decompile_function`); the description below is derived from the symbol-level diff evidence, not from decompiled code._

The implementation involves the addition of several new constant keys and string identifiers to the `ContactsMetrics` binary. These keys are used to report metrics to the system's analytics pipeline. The binary now includes symbols such as `_CNMetricsKeyPosterCount` and `_CNMetricsKeyPosterFractionMemoji`, which serve as keys for dictionary-based telemetry payloads. The logic appears to be designed to aggregate poster-related statistics across the user's contact database and transmit them via the existing `CoreAnalytics` infrastructure. The increase in `__AUTH_CONST.__cfstring` and `__DATA_CONST.__const` segments confirms that these new metrics are being registered as static keys for reporting purposes.

## How to trigger this feature

This feature is triggered automatically by the system when the Contacts application or the underlying `Contacts` framework processes or displays contact posters. Users can trigger the collection of these metrics by creating, editing, or updating their own "Me Card" poster or the posters of other contacts. The telemetry is likely emitted periodically or upon specific lifecycle events related to poster management within the Contacts framework.

## Vulnerability Assessment

1. **Security-relevant change**: This update is a functional expansion of telemetry capabilities rather than a security patch. There is no evidence of changes to memory management, bounds checking, or privilege escalation vectors.
2. **Patch mechanism**: The changes are strictly additive, introducing new data points for analytics. No existing code paths were modified to mitigate vulnerabilities.
3. **Evidence**: The diff shows only the addition of new symbols and strings related to metrics. The binary structure remains stable, and there are no modifications to existing function logic that would suggest a security-critical fix.

## Evidence

- **New Symbols**: `_CNMetricsKeyPosterCount`, `_CNMetricsKeyPosterFractionAutoUpdating`, `_CNMetricsKeyPosterFractionCustom`, `_CNMetricsKeyPosterFractionMemoji`, `_CNMetricsKeyPosterFractionMonogram`, `_CNMetricsKeyPosterFractionPhoto`, `_CNMetricsKeyPosterFractionWithAny`, `_CNMetricsKeyPosterMeCardType`.
- **New Strings**: "FractionAreCustom", "FractionAreMemoji", "FractionAreMonogram", "FractionArePhoto", "FractionExplicitlyUpdating", "FractionWithPoster", "MeCardPosterType", "NumberOfPosters".
- **Binary Diff**: Increase in `__cstring` and `__AUTH_CONST.__cfstring` segments, indicating the addition of new telemetry keys.

## AI Prioritisation Scoring System

- **feature_analysis**
  - **Tier**: TIER_3
  - **Category**: telemetry
  - **Reasoning**: The changes are purely additive telemetry keys for tracking poster usage statistics and do not involve security-sensitive logic or vulnerability remediation.

