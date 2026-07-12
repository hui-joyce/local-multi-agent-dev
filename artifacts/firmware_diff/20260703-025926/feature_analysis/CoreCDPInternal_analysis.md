## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "\"%@: Used precomputed escrowRecordHealthCheckFailureCount bit and determined escrow record state is %s.\""`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 72 (0 AI-authored, 72 auto-generated); comments: 6 (2 AI-authored, 4 auto-generated); across 6 function(s); verified persisted in .i64: 72 named variables, 4 comments.

## What this feature does

The update to `CoreCDPInternal` introduces support for "Custodian Recovery" within the Cloud Data Protection (CDP) flow. This feature allows users to designate a recovery contact (custodian) to assist in account recovery, providing a new recovery option alongside traditional methods like recovery keys. The framework has been updated to handle the lifecycle of these recovery options, including their population in the UI, status checks for circle/clique membership, and improved error handling for missing contexts or entitlements.

## How is it implemented


### Decompilation at `0x24c440f50`

```c
__int64 __fastcall -[CDPDRecoveryValidatedJoinFlowController _populateUserInfo:recoveryIndexHandlers:withRecoveryOptions:](
        __int64 n_a1,
        __int64 n_a2,
        void *void_a3,
        void *void_a4,
        void *void_a5)
{
  __int64 n_v8; // x0
  __int64 n_v9; // x0
  void *countByEnumeratingWithState; // x0
  void *countByEnumeratingWithState_2; // x23
  __int64 n_v12; // x28
  __int64 n_v13; // x22
  void *i; // x21
  void *void_v15; // x25
  void *objectForKeyedSubscript; // x24
  __int64 array; // x0
  void *addObject; // x0
  __int64 n_v19; // x26
  void *setObject; // x0
  __int64 n_v21; // x0
  __int64 n_v22; // x0
  __int64 n_v23; // x0
  __int64 n_v24; // x0
  __int64 result; // x0
  __int64 n_v26; // x0
  void *void_v27; // [xsp+8h] [xbp-128h]
  __int128 n_v28; // [xsp+10h] [xbp-120h] BYREF
  __int128 n_v29; // [xsp+20h] [xbp-110h]
  __int128 n_v30; // [xsp+30h] [xbp-100h]
  __int128 n_v31; // [xsp+40h] [xbp-F0h]
  _BYTE n_v32[128]; // [xsp+50h] [xbp-E0h] BYREF
  __int64 n_v33; // [xsp+D0h] [xbp-60h]

  n_v33 = *MEMORY[0x278A3C7F8];
  n_v8 = MEMORY[0x24FD44A60](n_a1, n_a2);
  n_v9 = MEMORY[0x24FD44A80](n_v8);
  MEMORY[0x24FD44A90](n_v9);
  n_v28 = 0u;
  n_v29 = 0u;
  n_v30 = 0u;
  n_v31 = 0u;
  void_v27 = void_a5;
  countByEnumeratingWithState = objc_msgSend(void_a5, "countByEnumeratingWithState:objects:count:", &n_v28, n_v32, 16);
  if ( countByEnumeratingWithState )
  {
    countByEnumeratingWithState_2 = countByEnumeratingWithState;
    n_v12 = *(_QWORD *)n_v29;
    n_v13 = *MEMORY[0x27897E558];
    do
    {
      for ( i = 0; i != countByEnumeratingWithState_2; i = (char *)i + 1 )
      {
        if ( *(_QWORD *)n_v29 != n_v12 )
          MEMORY[0x24FD44840](void_v27);
        void_v15 = *(void **)(*((_QWORD *)&n_v28 + 1) + 8LL * (_QWORD)i);
        if ( void_v15 )
        {
          if ( MEMORY[0x24FD44A30](objc_msgSend(void_a3, "objectForKeyedSubscript:", n_v13)) )
          {
            objectForKeyedSubscript = objc_msgSend(
                                        (id)MEMORY[0x24FD44A30](objc_msgSend(void_a3, "objectForKeyedSubscript:", n_v13)),
                                        "mutableCopy");
            array = MEMORY[0x24FD449B0]();
          }
          else
          {
            array = MEMORY[0x24FD44A30](objc_msgSend(MEMORY[0x278972978], "array"));
            objectForKeyedSubscript = (void *)array;
          }
          MEMORY[0x24FD449A0](array);
          addObject = objc_msgSend(
                        objectForKeyedSubscript,
                        "addObject:",
                        MEMORY[0x24FD44A30](objc_msgSend(void_v15, "localizedRecoveryOption")));
          MEMORY[0x24FD449A0](addObject);
          MEMORY[0x24FD44A30](objc_msgSend(void_v15, "recoveryHandler"));
          n_v19 = MEMORY[0x24FD44A40]();
          setObject = objc_msgSend(
                        void_a4,
                        "setObject:forKeyedSubscript:",
                        n_v19,
                        MEMORY[0x24FD44A30](
                          objc_msgSend(
                            MEMORY[0x27897EC98],
                            "numberWithUnsignedInteger:",
                            objc_msgSend(void_a4, "count"))));
          n_v21 = MEMORY[0x24FD449B0](setObject);
          n_v22 = MEMORY[0x24FD449A0](n_v21);
          MEMORY[0x24FD44990](n_v22);
          MEMORY[0x24FD44980](objc_msgSend(void_a3, "setObject:forKeyedSubscript:", objectForKeyedSubscript, n_v13));
        }
      }
      countByEnumeratingWithState_2 = objc_msgSend(
                                        void_v27,
                                        "countByEnumeratingWithState:objects:count:",
                                        &n_v28,
                                        n_v32,
                                        16);
    }
    while ( countByEnumeratingWithState_2 );
  }
  n_v23 = MEMORY[0x24FD449E0]();
  n_v24 = MEMORY[0x24FD44940](n_v23);
  result = MEMORY[0x24FD44920](n_v24);
  if ( *MEMORY[0x278A3C7F8] != n_v33 )
  {
    n_v26 = MEMORY[0x24FD44530](result);
    return -[CDPDRecoveryValidatedJoinFlowController _userInfoForLimit:withDevice:](n_v26);
  }
  return result;
}
```

### Decompilation at `0x24c48dcf8`

```c
_QWORD *__fastcall -[CDPDStateMachine initWithContext:uiProvider:connection:](
        void *void_a1,
        __int64 n_a2,
        __int64 n_a3,
        __int64 n_a4,
        __int64 n_a5)
{
  _QWORD *initWithContext; // x0
  _QWORD *qword_v10; // x20
  __int64 n_v11; // x0

  MEMORY[0x24FD44A60](void_a1, n_a2);
  initWithContext = objc_msgSend(void_a1, "initWithContext:uiProvider:", n_a3, n_a4);
  qword_v10 = initWithContext;
  if ( initWithContext )
  {
    n_v11 = MEMORY[0x24FD44A60]();
    qword_v10[11] = n_a5;
    initWithContext = (_QWORD *)MEMORY[0x24FD449E0](n_v11);
  }
  MEMORY[0x24FD44920](initWithContext);
  return qword_v10;
}
```

### Decompilation at `0x24c4889e4`

```c
__int64 __fastcall -[CDPDClientHandler circleStatusForContext:completion:](
        void *void_a1,
        __int64 n_a2,
        __int64 n_a3,
        __int64 n_a4)
{
  __int64 n_v8; // x0
  void *initWithContext; // x23
  __int64 n_v10; // x22
  __int64 n_v11; // x0
  __int64 n_v12; // x0
  __int64 n_v13; // x0
  __int64 n_v14; // x22
  __int64 n_v15; // x0
  __int64 n_v16; // x0
  __int64 n_v17; // x0
  __int64 n_v18; // x22
  __int64 n_v19; // x0
  __int64 n_v20; // x0
  __int64 n_v21; // x0
  __int64 n_v23; // [xsp+8h] [xbp-38h] BYREF

  n_v8 = MEMORY[0x24FD44A60]();
  MEMORY[0x24FD44A80](n_v8);
  if ( ((unsigned int)objc_msgSend(void_a1, "_allowStateMachineAccess") & 1) != 0 )
  {
    if ( n_a3 )
    {
      n_v23 = 0;
      initWithContext = objc_msgSend(
                          objc_msgSend((id)MEMORY[0x24FD447B0](MEMORY[0x2789B1C00]), "initWithContext:", n_a3),
                          "cachedSOSCircleStatus:",
                          &n_v23);
      n_v10 = n_v23;
      n_v11 = MEMORY[0x24FD44AA0]();
      if ( n_a4 )
        n_v11 = (*(__int64 (__fastcall **)(__int64, void *, __int64))(n_a4 + 16))(n_a4, initWithContext, n_v10);
      n_v12 = MEMORY[0x24FD44960](n_v11);
      goto LABEL_15;
    }
    n_v17 = MEMORY[0x24FD44460]();
    n_v18 = MEMORY[0x24FD44A30](n_v17);
    if ( (unsigned int)MEMORY[0x24FD44BF0](n_v18, 16) )
      -[CDPDClientHandler cliqueStatusForContext:completion:].cold.2(n_a2, n_v18);
    n_v15 = MEMORY[0x24FD44960]();
    if ( n_a4 )
    {
      n_v16 = -5003;
      goto LABEL_14;
    }
  }
  else
  {
    n_v13 = MEMORY[0x24FD44460]();
    n_v14 = MEMORY[0x24FD44A30](n_v13);
    if ( (unsigned int)MEMORY[0x24FD44BF0](n_v14, 16) )
      -[CDPDClientHandler cliqueStatusForContext:completion:].cold.1(n_a2, n_v14);
    n_v15 = MEMORY[0x24FD44960]();
    if ( n_a4 )
    {
      n_v16 = -5302;
LABEL_14:
      n_v19 = MEMORY[0x24FD444B0](n_v16, 0);
      n_v20 = MEMORY[0x24FD44A30](n_v19);
      n_v12 = (*(__int64 (__fastcall **)(__int64, __int64, __int64))(n_a4 + 16))(n_a4, 0xFFFFFFFFLL, n_v20);
LABEL_15:
      n_v15 = MEMORY[0x24FD44950](n_v12);
    }
  }
  n_v21 = MEMORY[0x24FD44940](n_v15);
  return MEMORY[0x24FD44920](n_v21);
}
```

### Decompilation at `0x24c442624`

```c
void __fastcall -[CDPDRecoveryValidatedJoinFlowController _custodianRecoveryOptionWithCompletion:](
        __int64 n_a1,
        __int64 n_a2,
        __int64 n_a3)
{
  __int64 n_v4; // x0
  __int64 n_v5; // x0
  __int64 n_v6; // x20
  __int64 n_v7; // x0
  void *void_v8; // x20
  __CFString *cfstr_v9; // x2
  void *builderForKey; // x0
  void *setLocalizedRecoveryOption; // x0
  __int64 n_v12; // x0
  void *setTelemetryRecoveryOption; // x0
  __int64 setRecoveryHandler; // x0
  _QWORD n_v15[5]; // [xsp+8h] [xbp-58h] BYREF
  _WORD n_v16[8]; // [xsp+30h] [xbp-30h] BYREF
  __int64 vars8; // [xsp+68h] [xbp+8h]

  n_v4 = MEMORY[0x24FD44A60](n_a1, n_a2);
  n_v5 = MEMORY[0x24FD44460](n_v4);
  n_v6 = MEMORY[0x24FD44A30](n_v5);
  n_v7 = MEMORY[0x24FD44BF0](n_v6, 0);
  if ( (_DWORD)n_v7 )
  {
    n_v16[0] = 0;
    n_v7 = MEMORY[0x24FD44580](&dword_24C42F000, n_v6, 0, "Creating recovery option: Custodian", n_v16, 2);
  }
  MEMORY[0x24FD44940](n_v7);
  void_v8 = (void *)MEMORY[0x24FD447D0](off_279C430F8);
  if ( (unsigned int)objc_msgSend(MEMORY[0x2789B1C20], "isICSCHarmonizationEnabled") )
    cfstr_v9 = &stru_2862D1E38;
  else
    cfstr_v9 = &stru_2862D1E58;
  builderForKey = objc_msgSend(
                    (id)MEMORY[0x24FD44A30](objc_msgSend(MEMORY[0x2789B1BC8], "builderForKey:", cfstr_v9)),
                    "localizedString");
  setLocalizedRecoveryOption = objc_msgSend(void_v8, "setLocalizedRecoveryOption:", MEMORY[0x24FD44A30](builderForKey));
  n_v12 = MEMORY[0x24FD44960](setLocalizedRecoveryOption);
  MEMORY[0x24FD44950](n_v12);
  setTelemetryRecoveryOption = objc_msgSend(void_v8, "setTelemetryRecoveryOption:", *MEMORY[0x2789B2120]);
  n_v15[0] = MEMORY[0x278A3C7E8];
  n_v15[1] = 3221225472LL;
  n_v15[2] = __82__CDPDRecoveryValidatedJoinFlowController__custodianRecoveryOptionWithCompletion___block_invoke;
  n_v15[3] = &unk_279C44758;
  n_v15[4] = n_a3;
  MEMORY[0x24FD44A60](setTelemetryRecoveryOption);
  setRecoveryHandler = MEMORY[0x24FD449E0](objc_msgSend(void_v8, "setRecoveryHandler:", n_v15));
  MEMORY[0x24FD44920](setRecoveryHandler);
  if ( ((vars8 ^ (2 * vars8)) & 0x4000000000000000LL) != 0 )
    __break(0xC471u);
  JUMPOUT(0x24FD447F0LL);
}
```

The implementation adds new controller methods to `CDPDRecoveryValidatedJoinFlowController` to manage the creation and population of recovery options. Specifically, the `_custodianRecoveryOptionWithCompletion:` method initializes a recovery option object, sets localized strings based on whether "ICSCHarmonization" is enabled, and assigns a recovery handler block to manage the completion of the custodian recovery process.

The `_populateUserInfo:recoveryIndexHandlers:withRecoveryOptions:` method iterates through available recovery options, dynamically building a list of localized recovery strings and mapping them to their respective handlers in a dictionary. This ensures that the UI can correctly present and execute the appropriate recovery logic based on the user's selection.

Additionally, `CDPDClientHandler` has been updated with `circleStatusForContext:completion:` and `cliqueStatusForContext:completion:`. These methods enforce access control by checking for valid state machine access before querying the Secure Object Sync (SOS) circle status. If the context is missing or access is denied, the methods return specific error codes (e.g., -5003, -5302) via the completion handler, ensuring that sensitive account status information is not leaked or accessed without proper authorization.

## How to trigger this feature

This feature is triggered during the account sign-in or recovery flow when the system determines that the user has configured a recovery contact. It is invoked when the `CDPDRecoveryValidatedJoinFlowController` is tasked with presenting recovery options to the user. The flow requires a valid `CDPContext` and appropriate entitlements to proceed; otherwise, the system will fail out with an error.

## Vulnerability Assessment

The changes include stricter access control checks in `CDPDClientHandler`, which mitigate potential unauthorized access to account status information. By explicitly checking for a valid context and enforcing entitlement requirements before allowing state machine access, the framework reduces the risk of privilege escalation or information disclosure regarding the user's circle/clique status. The addition of explicit error handling for missing contexts and entitlements is a security-hardening measure that ensures the system fails securely rather than proceeding with undefined or insecure states.

## Evidence

- **New Symbols**: `-[CDPDRecoveryValidatedJoinFlowController _custodianRecoveryOptionWithCompletion:]`, `-[CDPDClientHandler circleStatusForContext:completion:]`, `-[CDPDClientHandler cliqueStatusForContext:completion:]`.
- **New Strings**: `"Creating recovery option: Custodian"`, `"%s: Missing entitlement, failing!"`, `"CUSTODIAN_RECOVERY_HELP_PROMPT_MESSAGE"`.
- **Framework Dependency**: Added `CoreData.framework`.
- **Logic Changes**: Introduction of `isSilentEscrowRecordRepairEnabledV2` and enhanced error reporting for missing entitlements.

## AI Prioritisation Scoring System

- **feature_analysis**
  - **Tier**: TIER_1
  - **Category**: security_boundary
  - **Reasoning**: The update introduces new recovery mechanisms (Custodian Recovery) and enforces stricter access control/entitlement checks for sensitive account status queries, which are critical security boundaries.

