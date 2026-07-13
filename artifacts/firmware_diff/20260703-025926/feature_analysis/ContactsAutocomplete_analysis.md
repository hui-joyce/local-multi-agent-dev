## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "Final assembly 1. finalResults: %{private}@"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 34 (2 AI-authored, 32 auto-generated); comments: 4 (2 AI-authored, 2 auto-generated); across 2 function(s); verified persisted in .i64: 34 named variables, 2 comments.
- **Apple Security Notes**: matches advisory component `Contacts` — Apple confirms a security-relevant change here; this analysis examines the likely vulnerability patch.

## What this feature does

The `ContactsAutocomplete` framework has been updated to include new logic for handling "Stewie" (Emergency SOS via Satellite) related terms. The changes introduce a mechanism to fetch, cache, and manage localized emergency and "avocet" (a codename associated with satellite features) phrases. This ensures that the autocomplete system can prioritize or recognize specific emergency-related contact or search terms, likely to facilitate emergency communication even when standard network connectivity is unavailable.

## How is it implemented


### Decompilation at `0x21978f84c`

```c
__int64 __fastcall -[CNACTStewieFacade emergencyTerms](id *facade)
{
  void *localizedEmergencyPhrases; // x0
  void *arrayWithObjects; // x0
  void *cndistinctObjects; // x0
  __int64 n_v5; // x22
  __int64 n_v6; // x0
  __int64 n_v7; // x0
  __int64 n_v8; // x0
  __int64 n_v9; // x23
  __int64 n_v10; // x0
  void *void_v11; // x25
  void *currentEnvironment; // x0
  __int64 n_v13; // x0
  __int64 n_v14; // x0
  __int64 n_v15; // x0
  __int64 n_v16; // x0
  __int64 n_v17; // x0
  __int64 n_v18; // x0
  __int64 n_v19; // x20
  __int64 n_v20; // x0
  _QWORD n_v22[2]; // [xsp+8h] [xbp-58h] BYREF
  __int64 n_v23; // [xsp+18h] [xbp-48h]
  __int64 vars8; // [xsp+68h] [xbp+8h]

  n_v23 = *MEMORY[0x278A3C7F8];
  MEMORY[0x21FF7CDA0]();
  MEMORY[0x21FF7CEC0](facade);
  if ( ((unsigned int)objc_msgSend(facade, "withLock_isEmergencyEnabled") & 1) != 0 )
  {
    if ( (unsigned int)objc_msgSend((id)MEMORY[0x21FF7CC20](facade), "isMemoValid:", facade[3]) )
    {
      MEMORY[0x21FF7CD70](objc_msgSend(facade[3], "value"));
    }
    else
    {
      localizedEmergencyPhrases = objc_msgSend((id)MEMORY[0x21FF7CC20](facade), "localizedEmergencyPhrases");
      n_v22[0] = MEMORY[0x21FF7CD70](localizedEmergencyPhrases);
      n_v22[1] = MEMORY[0x21FF7CD70](objc_msgSend(facade, "numbers"));
      arrayWithObjects = objc_msgSend(
                           (id)MEMORY[0x21FF7CD70](objc_msgSend(MEMORY[0x2789728C0], "arrayWithObjects:count:", n_v22, 2)),
                           "_cn_flatten");
      cndistinctObjects = objc_msgSend((id)MEMORY[0x21FF7CD70](arrayWithObjects), "_cn_distinctObjects");
      n_v5 = MEMORY[0x21FF7CD70](cndistinctObjects);
      n_v6 = MEMORY[0x21FF7CCE0]();
      n_v7 = MEMORY[0x21FF7CCD0](n_v6);
      n_v8 = contactSearchLog(n_v7);
      n_v9 = MEMORY[0x21FF7CD70](n_v8);
      n_v10 = MEMORY[0x21FF7CF00](n_v9, 2);
      if ( (_DWORD)n_v10 )
        n_v10 = -[CNACTStewieFacade emergencyTerms].cold.1(n_v5, n_v9);
      MEMORY[0x21FF7CCD0](n_v10);
      void_v11 = (void *)MEMORY[0x2789B0408];
      currentEnvironment = objc_msgSend(
                             (id)MEMORY[0x21FF7CD70](objc_msgSend(MEMORY[0x2789B0358], "currentEnvironment")),
                             "timeProvider");
      objc_msgSend((id)MEMORY[0x21FF7CD70](currentEnvironment), "timestamp");
      facade[3] = (id)MEMORY[0x21FF7CD70](objc_msgSend(void_v11, "timestampedWithValue:timestamp:", n_v5));
      n_v13 = MEMORY[0x21FF7CD30]();
      n_v14 = MEMORY[0x21FF7CCE0](n_v13);
      MEMORY[0x21FF7CCD0](n_v14);
      MEMORY[0x21FF7CD70](objc_msgSend(facade[3], "value"));
      n_v15 = MEMORY[0x21FF7CCC0]();
      n_v16 = MEMORY[0x21FF7CCB0](n_v15);
      MEMORY[0x21FF7CCA0](n_v16);
    }
  }
  n_v17 = MEMORY[0x21FF7CED0](facade);
  n_v18 = MEMORY[0x21FF7CC90](n_v17);
  if ( *MEMORY[0x278A3C7F8] == n_v23 )
  {
    if ( ((vars8 ^ (2 * vars8)) & 0x4000000000000000LL) != 0 )
      __break(0xC471u);
    JUMPOUT(0x21FF7CB90LL);
  }
  n_v19 = MEMORY[0x21FF7CA20](n_v18);
  MEMORY[0x21FF7CED0](facade);
  n_v20 = MEMORY[0x21FF7C9F0](n_v19);
  return -[CNACTStewieFacade isEmergencyEnabled](n_v20);
}
```

### Decompilation at `0x21978fb24`

```c
void __fastcall -[CNACTStewieFacade avocetTerms](id *facade)
{
  void *localizedAvocetPhrases; // x0
  void *cndistinctObjects; // x0
  __int64 n_v4; // x21
  __int64 n_v5; // x0
  __int64 n_v6; // x22
  void *void_v7; // x23
  void *currentEnvironment; // x0
  __int64 n_v9; // x0
  __int64 n_v10; // x0
  __int64 n_v11; // x0
  __int64 n_v12; // x0
  __int64 vars8; // [xsp+38h] [xbp+8h]

  MEMORY[0x21FF7CDA0]();
  MEMORY[0x21FF7CEC0](facade);
  if ( ((unsigned int)objc_msgSend(facade, "withLock_isAvocetEnabled") & 1) != 0 )
  {
    if ( (unsigned int)objc_msgSend((id)MEMORY[0x21FF7CC20](facade), "isMemoValid:", facade[4]) )
    {
      MEMORY[0x21FF7CD70](objc_msgSend(facade[4], "value"));
    }
    else
    {
      localizedAvocetPhrases = objc_msgSend((id)MEMORY[0x21FF7CC20](facade), "localizedAvocetPhrases");
      cndistinctObjects = objc_msgSend((id)MEMORY[0x21FF7CD70](localizedAvocetPhrases), "_cn_distinctObjects");
      n_v4 = MEMORY[0x21FF7CD70](cndistinctObjects);
      n_v5 = contactSearchLog(n_v4);
      n_v6 = MEMORY[0x21FF7CD70](n_v5);
      if ( (unsigned int)MEMORY[0x21FF7CF00](n_v6, 2) )
        -[CNACTStewieFacade avocetTerms].cold.1(n_v4, n_v6);
      MEMORY[0x21FF7CCC0]();
      void_v7 = (void *)MEMORY[0x2789B0408];
      currentEnvironment = objc_msgSend(
                             (id)MEMORY[0x21FF7CD70](objc_msgSend(MEMORY[0x2789B0358], "currentEnvironment")),
                             "timeProvider");
      objc_msgSend((id)MEMORY[0x21FF7CD70](currentEnvironment), "timestamp");
      facade[4] = (id)MEMORY[0x21FF7CD70](objc_msgSend(void_v7, "timestampedWithValue:timestamp:", n_v4));
      n_v9 = MEMORY[0x21FF7CD30]();
      n_v10 = MEMORY[0x21FF7CCE0](n_v9);
      MEMORY[0x21FF7CCC0](n_v10);
      MEMORY[0x21FF7CD70](objc_msgSend(facade[4], "value"));
      n_v11 = MEMORY[0x21FF7CCB0]();
      MEMORY[0x21FF7CCA0](n_v11);
    }
  }
  n_v12 = MEMORY[0x21FF7CED0](facade);
  MEMORY[0x21FF7CC90](n_v12);
  if ( ((vars8 ^ (2 * vars8)) & 0x4000000000000000LL) != 0 )
    __break(0xC471u);
  JUMPOUT(0x21FF7CB90LL);
}
```

The implementation centers on the `CNACTStewieFacade` class, which now manages two distinct sets of terms: `emergencyTerms` and `avocetTerms`. 

For both sets of terms, the implementation follows a "check-then-fetch" pattern. The methods first verify if the respective feature (Emergency or Avocet) is enabled using a thread-safe locking mechanism (`withLock_isEmergencyEnabled` / `withLock_isAvocetEnabled`). If enabled, the code checks if a valid, cached "memo" of the terms exists. If the cache is valid, it returns the existing values. If the cache is invalid or missing, the system fetches localized phrases from the environment, flattens them into a distinct list, and updates the internal cache with a timestamped value. This ensures that the autocomplete system always has access to the most current, localized emergency phrases without redundant, expensive lookups.

## How to trigger this feature

This feature is triggered automatically by the `ContactsAutocomplete` system when a user initiates a search or contact lookup. The system checks the status of the Stewie/Emergency SOS subsystem; if the device is in a state where satellite emergency features are relevant or enabled, the `CNACTStewieFacade` will populate its internal term lists to assist in ranking or identifying emergency-related search results.

## Vulnerability Assessment

1. **Security-relevant change**: The change introduces a new caching mechanism for sensitive emergency-related strings and adds logging for these operations.
2. **Patch mechanism**: The implementation uses a thread-safe locking mechanism (`withLock_`) to prevent race conditions when accessing or updating the cached emergency terms. By checking `isMemoValid` before fetching new data, it ensures that the system does not perform unnecessary or potentially inconsistent updates to the term lists.
3. **Evidence**: The decompiled code shows explicit calls to `withLock_isEmergencyEnabled` and `withLock_isAvocetEnabled` before any data processing occurs. The use of `timestampedWithValue:timestamp:` indicates a robust cache invalidation strategy. The transition from `%{public}@` to `%{private}@` in the logging strings (as seen in the diff) is a significant privacy improvement, ensuring that sensitive contact or search terms are not leaked into system logs.

## AI Prioritisation Scoring System

- **static_analysis**
  - **Tier**: TIER_1
  - **Category**: privacy_and_safety
  - **Reasoning**: The changes involve sensitive emergency communication logic and include a privacy-focused update to logging (public to private) for search terms, which is a critical security/privacy improvement.

