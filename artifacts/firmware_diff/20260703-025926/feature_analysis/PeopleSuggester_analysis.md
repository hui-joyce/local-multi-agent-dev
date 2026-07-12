## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "%@ not in metadata"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 119 (0 AI-authored, 119 auto-generated); comments: 3 (0 AI-authored, 3 auto-generated); across 3 function(s); verified persisted in .i64: 119 named variables, 3 comments.

## What this feature does

The `PeopleSuggester` framework update introduces a more robust and configurable machine learning pipeline for generating share sheet suggestions. The changes focus on transitioning from static feature management to a dynamic, plist-driven configuration system (`_PSConfig`). This allows the system to load model configurations, vocabularies, and feature definitions at runtime, improving the flexibility of the suggestion engine. Additionally, the update enhances the CoreML scoring model by integrating a more sophisticated feature vector extraction process and adding telemetry support for tracking suggestion performance.

## How is it implemented


### Decompilation at `0x1b7bb0a84`

```c
__int64 __fastcall -[_PSCoreMLScoringModel getSuggestionProxiesForCandidateToFeatureVectorDictGetter:predictionContext:messageInteractionCache:shareInteractionCache:](
        void *void_a1,
        __int64 n_a2,
        __int64 n_a3,
        __int64 n_a4)
{
  __int64 n_v7; // x0
  __int64 generalChannel; // x20
  __int64 n_v9; // x0
  void *keysSortedByValueUsingComparator; // x21
  __int64 generalChannel_2; // x20
  __int64 n_v12; // x0
  __int64 getModelPath; // x24
  void *countByEnumeratingWithState; // x0
  void *countByEnumeratingWithState_2; // x25
  __int64 n_v16; // x26
  void *i; // x22
  void *void_v18; // x27
  __int64 objectForKeyedSubscript; // x19
  __int64 candidateIdentifier; // x20
  void *bundleId; // x28
  unsigned int isEqual; // w23
  __int64 n_v23; // x0
  __int64 recipientsId; // x21
  void *void_v25; // x21
  __int64 bundleId_2; // x23
  void *initWithBundleID; // x27
  __int64 n_v28; // x0
  __int64 n_v29; // x0
  __int64 generalChannel_3; // x28
  __int64 n_v31; // x0
  __int64 n_v32; // x0
  __int64 n_v33; // x0
  __int64 n_v34; // x0
  __int64 n_v35; // x0
  __int64 n_v36; // x0
  __int64 n_v37; // x0
  __int64 n_v38; // x0
  __int64 n_v39; // x0
  __int64 n_v40; // x0
  void *void_v42; // [xsp+38h] [xbp-158h]
  void *void_v43; // [xsp+40h] [xbp-150h]
  void *scoreCandidates; // [xsp+48h] [xbp-148h]
  __int128 n_v45; // [xsp+50h] [xbp-140h] BYREF
  __int128 n_v46; // [xsp+60h] [xbp-130h]
  __int128 n_v47; // [xsp+70h] [xbp-120h]
  __int128 n_v48; // [xsp+80h] [xbp-110h]
  _BYTE n_v49[128]; // [xsp+90h] [xbp-100h] BYREF
  int n_v50; // [xsp+110h] [xbp-80h] BYREF
  void *void_v51; // [xsp+114h] [xbp-7Ch]
  __int64 n_v52; // [xsp+128h] [xbp-68h]
  __int64 vars8; // [xsp+198h] [xbp+8h]

  n_v52 = *MEMORY[0x1E6782818];
  n_v7 = MEMORY[0x1B8BA38B0](void_a1, n_a2);
  MEMORY[0x1B8BA38C0](n_v7);
  void_v43 = (void *)MEMORY[0x1B8BA3710](MEMORY[0x1E66FA270]);
  generalChannel = MEMORY[0x1B8BA3850](objc_msgSend(off_1E7ADAF00, "generalChannel"));
  n_v9 = MEMORY[0x1B8BA3A10](generalChannel, 1);
  if ( (_DWORD)n_v9 )
  {
    LOWORD(n_v50) = 0;
    n_v9 = MEMORY[0x1B8BA3110](&dword_1B7ABC000, generalChannel, 1, "_PSCoreMLScoringModel ranking", &n_v50, 2);
  }
  MEMORY[0x1B8BA3780](n_v9);
  scoreCandidates = (void *)MEMORY[0x1B8BA3850](objc_msgSend(void_a1, "scoreCandidates:predictionContext:", n_a3, n_a4));
  keysSortedByValueUsingComparator = (void *)MEMORY[0x1B8BA3850](
                                               objc_msgSend(
                                                 scoreCandidates,
                                                 "keysSortedByValueUsingComparator:",
                                                 &__block_literal_global_169));
  generalChannel_2 = MEMORY[0x1B8BA3850](objc_msgSend(off_1E7ADAF00, "generalChannel"));
  n_v12 = MEMORY[0x1B8BA3A10](generalChannel_2, 1);
  if ( (_DWORD)n_v12 )
  {
    n_v50 = 138477827;
    void_v51 = keysSortedByValueUsingComparator;
    n_v12 = MEMORY[0x1B8BA3110](
              &dword_1B7ABC000,
              generalChannel_2,
              1,
              "_PSCoreMLScoringModel sorted score array: %{private}@",
              &n_v50,
              12);
  }
  MEMORY[0x1B8BA3780](n_v12);
  getModelPath = MEMORY[0x1B8BA3850](objc_msgSend(void_a1, "getModelPath"));
  n_v45 = 0u;
  n_v46 = 0u;
  n_v47 = 0u;
  n_v48 = 0u;
  MEMORY[0x1B8BA38B0]();
  countByEnumeratingWithState = objc_msgSend(
                                  keysSortedByValueUsingComparator,
                                  "countByEnumeratingWithState:objects:count:",
                                  &n_v45,
                                  n_v49,
                                  16);
  if ( countByEnumeratingWithState )
  {
    countByEnumeratingWithState_2 = countByEnumeratingWithState;
    n_v16 = *(_QWORD *)n_v46;
    void_v42 = keysSortedByValueUsingComparator;
    do
    {
      for ( i = 0; i != countByEnumeratingWithState_2; i = (char *)i + 1 )
      {
        if ( *(_QWORD *)n_v46 != n_v16 )
          MEMORY[0x1B8BA3670](void_v42);
        void_v18 = *(void **)(*((_QWORD *)&n_v45 + 1) + 8LL * (_QWORD)i);
        objectForKeyedSubscript = MEMORY[0x1B8BA3850](objc_msgSend(scoreCandidates, "objectForKeyedSubscript:", void_v18));
        candidateIdentifier = MEMORY[0x1B8BA3850](objc_msgSend(void_v18, "candidateIdentifier"));
        bundleId = (void *)MEMORY[0x1B8BA3850](objc_msgSend(void_v18, "bundleId"));
        isEqual = (unsigned int)objc_msgSend(
                                  bundleId,
                                  "isEqual:",
                                  MEMORY[0x1B8BA3850](objc_msgSend(off_1E7ADAD58, "sharePlayBundleId")));
        n_v23 = MEMORY[0x1B8BA3790]();
        MEMORY[0x1B8BA3800](n_v23);
        if ( isEqual )
        {
          recipientsId = MEMORY[0x1B8BA3850](objc_msgSend(void_v18, "recipientsId"));
          MEMORY[0x1B8BA3780]();
          candidateIdentifier = recipientsId;
        }
        void_v25 = (void *)MEMORY[0x1B8BA35D0](off_1E7ADAFF0);
        bundleId_2 = MEMORY[0x1B8BA3850](objc_msgSend(void_v18, "bundleId"));
        initWithBundleID = objc_msgSend(
                             void_v25,
                             "initWithBundleID:interactionRecipients:contactID:reason:reasonType:modelScore:",
                             bundleId_2,
                             candidateIdentifier,
                             0,
                             objc_msgSend(
                               (id)MEMORY[0x1B8BA35D0](MEMORY[0x1E6707260]),
                               "initWithFormat:",
                               &stru_1F30173E0,
                               getModelPath,
                               objectForKeyedSubscript),
                             getModelPath,
                             objectForKeyedSubscript);
        n_v28 = MEMORY[0x1B8BA3800]();
        n_v29 = MEMORY[0x1B8BA37B0](n_v28);
        if ( initWithBundleID )
        {
          objc_msgSend(void_v43, "add
// [truncated: decompiler/model output too long or degenerate]
```

### Decompilation at `0x1b7af88c0`

```c
__int64 __fastcall -[_PSEnsembleModel getCoreMLSuggestionProxiesWithPredictionContext:modelSuggestionProxiesDict:candidateToFeatureVectorDictGetter:](
        void *void_a1,
        __int64 n_a2,
        __int64 n_a3,
        void *void_a4,
        __int64 n_a5)
{
  __int64 n_v9; // x0
  __int64 n_v10; // x0
  __int64 objectForKeyedSubscript; // x0
  int n_v12; // w24
  __int64 suggestionSignpost; // x24
  __int64 n_v14; // x0
  void *coreMLScoringModel; // x24
  __int64 messageInteractionCache; // x25
  void *getSuggestionProxiesForCandidateToFeatureVectorDictGetter; // x0
  void *setObject; // x0
  __int64 n_v19; // x0
  __int64 n_v20; // x0
  __int64 n_v21; // x0
  __int64 suggestionSignpost_2; // x23
  __int64 n_v23; // x0
  __int64 n_v24; // x0
  __int64 n_v25; // x0
  _WORD n_v27[8]; // [xsp+0h] [xbp-70h] BYREF
  _WORD n_v28[8]; // [xsp+10h] [xbp-60h] BYREF

  n_v9 = MEMORY[0x1B8BA3880](void_a1, n_a2);
  n_v10 = MEMORY[0x1B8BA38A0](n_v9);
  MEMORY[0x1B8BA38B0](n_v10);
  objectForKeyedSubscript = MEMORY[0x1B8BA3850](objc_msgSend(void_a4, "objectForKeyedSubscript:", &stru_1F300A720));
  if ( objectForKeyedSubscript )
  {
    n_v12 = MEMORY[0x1B8BA30D0]("PeopleSuggester", "sharesheet_v2_model_suggestions");
    objectForKeyedSubscript = MEMORY[0x1B8BA37A0]();
    if ( n_v12 )
    {
      suggestionSignpost = MEMORY[0x1B8BA3850](objc_msgSend(off_1E7ADAF00, "suggestionSignpost"));
      n_v14 = MEMORY[0x1B8BA3A20]();
      if ( (_DWORD)n_v14 )
      {
        n_v28[0] = 0;
        n_v14 = MEMORY[0x1B8BA3120](
                  &dword_1B7ABC000,
                  suggestionSignpost,
                  1,
                  0xEEEEB0B5B2B2EEEELL,
                  "_PSShareSheetCoreMLSuggestions",
                  " enableTelemetry=YES ",
                  n_v28,
                  2);
      }
      MEMORY[0x1B8BA37C0](n_v14);
      coreMLScoringModel = (void *)MEMORY[0x1B8BA3850](objc_msgSend(void_a1, "coreMLScoringModel"));
      messageInteractionCache = MEMORY[0x1B8BA3850](objc_msgSend(void_a1, "messageInteractionCache"));
      getSuggestionProxiesForCandidateToFeatureVectorDictGetter = objc_msgSend(
                                                                    coreMLScoringModel,
                                                                    "getSuggestionProxiesForCandidateToFeatureVectorDictG"
                                                                    "etter:predictionContext:messageInteractionCache:shar"
                                                                    "eInteractionCache:",
                                                                    n_a5,
                                                                    n_a3,
                                                                    messageInteractionCache,
                                                                    MEMORY[0x1B8BA3850](objc_msgSend(void_a1, "shareInteractionCache")));
      setObject = objc_msgSend(
                    void_a4,
                    "setObject:forKeyedSubscript:",
                    MEMORY[0x1B8BA3850](getSuggestionProxiesForCandidateToFeatureVectorDictGetter),
                    &stru_1F300A720);
      n_v19 = MEMORY[0x1B8BA37E0](setObject);
      n_v20 = MEMORY[0x1B8BA37B0](n_v19);
      n_v21 = MEMORY[0x1B8BA37D0](n_v20);
      MEMORY[0x1B8BA37C0](n_v21);
      suggestionSignpost_2 = MEMORY[0x1B8BA3850](objc_msgSend(off_1E7ADAF00, "suggestionSignpost"));
      n_v23 = MEMORY[0x1B8BA3A20]();
      if ( (_DWORD)n_v23 )
      {
        n_v27[0] = 0;
        n_v23 = MEMORY[0x1B8BA3120](
                  &dword_1B7ABC000,
                  suggestionSignpost_2,
                  2,
                  0xEEEEB0B5B2B2EEEELL,
                  "_PSShareSheetCoreMLSuggestions",
                  &unk_1B7BE1A8D,
                  n_v27,
                  2);
      }
      objectForKeyedSubscript = MEMORY[0x1B8BA37B0](n_v23);
    }
  }
  n_v24 = MEMORY[0x1B8BA3790](objectForKeyedSubscript);
  n_v25 = MEMORY[0x1B8BA3780](n_v24);
  return MEMORY[0x1B8BA3760](n_v25);
}
```

### Decompilation at `0x1b7af8aa8`

```c
__int64 __fastcall -[_PSEnsembleModel getHeuristicSuggestionProxies:supportedBundleIDs:modelSuggestionProxiesDict:](
        void *void_a1,
        __int64 n_a2,
        void *void_a3,
        __int64 n_a4,
        void *void_a5)
{
  __int64 n_v9; // x0
  __int64 n_v10; // x0
  __int64 objectForKeyedSubscript; // x24
  __int64 generalChannel; // x24
  __int64 suggestionSignpost; // x24
  __int64 n_v14; // x0
  void *heuristics; // x24
  __int64 suggestionDate; // x25
  void *hyperRecentHeuristicSuggestionProxiesWithReferenceDate; // x0
  void *setObject; // x0
  __int64 n_v19; // x0
  __int64 n_v20; // x0
  __int64 n_v21; // x0
  __int64 suggestionSignpost_2; // x24
  __int64 n_v23; // x0
  __int64 objectForKeyedSubscript_2; // x24
  __int64 generalChannel_2; // x24
  __int64 suggestionSignpost_3; // x24
  __int64 n_v27; // x0
  void *heuristics_2; // x0
  void *setObject_2; // x0
  __int64 n_v30; // x0
  __int64 suggestionSignpost_4; // x24
  __int64 n_v32; // x0
  __int64 objectForKeyedSubscript_3; // x24
  __int64 n_v34; // x0
  __int64 generalChannel_3; // x24
  __int64 suggestionSignpost_5; // x24
  __int64 n_v37; // x0
  void *heuristics_3; // x0
  void *setObject_3; // x0
  __int64 n_v40; // x0
  __int64 suggestionSignpost_6; // x23
  __int64 n_v42; // x0
  __int64 n_v43; // x0
  __int64 n_v44; // x0
  _WORD n_v46[8]; // [xsp+0h] [xbp-B0h] BYREF
  _WORD n_v47[8]; // [xsp+10h] [xbp-A0h] BYREF
  _WORD n_v48[8]; // [xsp+20h] [xbp-90h] BYREF
  _WORD n_v49[8]; // [xsp+30h] [xbp-80h] BYREF
  _WORD n_v50[8]; // [xsp+40h] [xbp-70h] BYREF
  _WORD n_v51[8]; // [xsp+50h] [xbp-60h] BYREF

  n_v9 = MEMORY[0x1B8BA3880](void_a1, n_a2);
  n_v10 = MEMORY[0x1B8BA38A0](n_v9);
  MEMORY[0x1B8BA38B0](n_v10);
  objectForKeyedSubscript = MEMORY[0x1B8BA3850](objc_msgSend(void_a5, "objectForKeyedSubscript:", &stru_1F300A760));
  MEMORY[0x1B8BA37C0]();
  if ( objectForKeyedSubscript )
  {
    generalChannel = MEMORY[0x1B8BA3850](objc_msgSend(off_1E7ADAF00, "generalChannel"));
    if ( (unsigned int)MEMORY[0x1B8BA3A10](generalChannel, 2) )
      -[_PSEnsembleModel getHeuristicSuggestionProxies:supportedBundleIDs:modelSuggestionProxiesDict:].cold.1(generalChannel);
    MEMORY[0x1B8BA37C0]();
    suggestionSignpost = MEMORY[0x1B8BA3850](objc_msgSend(off_1E7ADAF00, "suggestionSignpost"));
    n_v14 = MEMORY[0x1B8BA3A20]();
    if ( (_DWORD)n_v14 )
    {
      n_v51[0] = 0;
      n_v14 = MEMORY[0x1B8BA3120](
                &dword_1B7ABC000,
                suggestionSignpost,
                1,
                0xEEEEB0B5B2B2EEEELL,
                "_PSShareSheetPeopleHyperRecencyHeuristic",
                " enableTelemetry=YES ",
                n_v51,
                2);
    }
    MEMORY[0x1B8BA37C0](n_v14);
    heuristics = (void *)MEMORY[0x1B8BA3850](objc_msgSend(void_a1, "heuristics"));
    suggestionDate = MEMORY[0x1B8BA3850](objc_msgSend(void_a3, "suggestionDate"));
    hyperRecentHeuristicSuggestionProxiesWithReferenceDate = objc_msgSend(
                                                               heuristics,
                                                               "hyperRecentHeuristicSuggestionProxiesWithReferenceDate:pr"
                                                               "edictionContextBundleId:",
                                                               suggestionDate,
                                                               MEMORY[0x1B8BA3850](objc_msgSend(void_a3, "bundleID")));
    setObject = objc_msgSend(
                  void_a5,
                  "setObject:forKeyedSubscript:",
                  MEMORY[0x1B8BA3850](hyperRecentHeuristicSuggestionProxiesWithReferenceDate),
                  &stru_1F300A760);
    n_v19 = MEMORY[0x1B8BA37F0](setObject);
    n_v20 = MEMORY[0x1B8BA37E0](n_v19);
    n_v21 = MEMORY[0x1B8BA37D0](n_v20);
    MEMORY[0x1B8BA37C0](n_v21);
    suggestionSignpost_2 = MEMORY[0x1B8BA3850](objc_msgSend(off_1E7ADAF00, "suggestionSignpost"));
    n_v23 = MEMORY[0x1B8BA3A20]();
    if ( (_DWORD)n_v23 )
    {
      n_v50[0] = 0;
      n_v23 = MEMORY[0x1B8BA3120](
                &dword_1B7ABC000,
                suggestionSignpost_2,
                2,
                0xEEEEB0B5B2B2EEEELL,
                "_PSShareSheetPeopleHyperRecencyHeuristic",
                &unk_1B7BE1A8D,
                n_v50,
                2);
    }
    MEMORY[0x1B8BA37C0](n_v23);
  }
  objectForKeyedSubscript_2 = MEMORY[0x1B8BA3850](objc_msgSend(void_a5, "objectForKeyedSubscript:", &stru_1F300A780));
  MEMORY[0x1B8BA37C0]();
  if ( objectForKeyedSubscript_2 )
  {
    generalChannel_2 = MEMORY[0x1B8BA3850](objc_msgSend(off_1E7ADAF00, "generalChannel"));
    if ( (unsigned int)MEMORY[0x1B8BA3A10](generalChannel_2, 2) )
      -[_PSEnsembleModel getHeuristicSuggestionProxies:supportedBundleIDs:modelSuggestionProxiesDict:].cold.2(generalChannel_2);
    MEMORY[0x1B8BA37C0]();
    suggestionSignpost_3 = MEMORY[0x1B8BA3850](objc_msgSend(off_1E7ADAF00, "suggestionSignpost"));
    n_v27 = MEMORY[0x1B8BA3A20]();
    if ( (_DWORD)n_v27 )
    {
      n_v49[0] = 0;
      n_v27 = MEMORY[0x1B8BA3120](
                &dword_1B7ABC000,
                suggestionSignpost_3,
                1,
                0xEEEEB0B5B2B2EEEELL,
                "_PSShareSheetPeopleInPhoneCallHeuristic",
                " enableTelemetry=YES ",
                n_v49,
                2);
    }
    MEMORY[0x1B8BA37C0](n_v27);
    heuristics_2 = objc_msgSend(
                     (id)MEMORY[0x1B8BA3850](objc_msgSend(void_a1, "heuristics")),
                     "inPhoneCallHeuristicSuggestionProxiesWithBundleIds:predictionContext:",
                     n_a4,
                     void_a3);
    setObject_2 = objc_msgSend(
                    void_a5,
                    "setObject:forKeyedSubscript:",
                    MEMORY[0x1B8BA3850](heuristics_2),
                    &stru_1F300A780);
    n_v30 = MEMORY[0x1B8BA37D0](setObject_2);
    MEMORY[0x1B8BA37C0](n_v30);
    suggestionSignpost_4 = MEMORY[0x1
// [truncated: decompiler/model output too long or degenerate]
```

The implementation centers on the `_PSEnsembleModel` and `_PSCoreMLScoringModel` classes. The `_PSEnsembleModel` now utilizes a dynamic configuration loader to fetch model parameters and feature definitions. When generating suggestions, the model checks for the existence of specific keys in a dictionary (e.g., `sharesheet_v2_model_suggestions`) and, if present, triggers a CoreML-based scoring process.

The scoring logic involves fetching a `candidateToFeatureVectorDictGetter` which is used to map interaction data into a feature tensor. The system uses signposting to instrument the suggestion process, allowing for performance monitoring and telemetry collection. The `_PSCoreMLScoringModel` handles the heavy lifting of reformatting candidate dictionaries into tensors, performing batch predictions, and managing the initialization state of the ML model. The framework also includes new utility methods for prewarming photo frameworks and extracting person IDs from shared photo attachments, indicating a deeper integration with the Photos framework to improve suggestion relevance.

## How to trigger this feature

This feature is triggered during the standard share sheet invocation flow. When a user attempts to share content, the `PeopleSuggester` framework is queried to provide a list of suggested recipients. The system evaluates the current context (e.g., shared photo attachments, recent interactions, and bundle ID mappings) and, if the CoreML model is initialized and configured, it executes the scoring pipeline to return ranked suggestions.

## Vulnerability Assessment

The changes appear to be a functional refactor rather than a security patch. The introduction of `_PSConfig` and the dynamic loading of plists increases the attack surface slightly, as the system now relies on external configuration files. However, the code includes robust error handling for plist loading and tensor creation (e.g., checking for nil values and logging errors). The use of `%{sensitive}@` in log strings suggests that the developers are aware of privacy concerns and are actively masking sensitive user data in logs. No obvious memory safety issues (like UAF or OOB) were identified in the modified code paths; the memory management appears to follow standard Objective-C reference counting patterns.

## Evidence

- **Symbols**: Added `+[_PSConfig _loadPlistNamed:]`, `+[_PSPhotoUtils prewarmPhotosFrameworks]`, and various `_PSCoreMLScoringModel` methods.
- **Strings**: Added `Error creating tensor: %@`, `Final ZKW suggestions post-transformers: %{sensitive}@`, and `_PSShareSheetCoreMLSuggestions`.
- **Binary Diff**: Significant increase in `__TEXT` and `__DATA_CONST` segments, reflecting the addition of new classes and configuration logic.
- **Decompilation**: The decompiled `getCoreMLSuggestionProxies...` method confirms the integration of telemetry signposts and the use of a dictionary-based getter for feature vectors.

## AI Prioritisation Scoring System

- **feature_analysis**
  - **Tier**: TIER_2
  - **Category**: core_logic
  - **Reasoning**: The update is a significant refactor of the suggestion engine's configuration and ML pipeline. While it improves performance and flexibility, it does not appear to be a security-critical patch.

