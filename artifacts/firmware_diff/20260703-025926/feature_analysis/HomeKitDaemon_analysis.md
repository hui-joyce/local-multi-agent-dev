## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "%@ addedWalletKey: %@, passJSONDict: %@"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 103 (0 AI-authored, 103 auto-generated); comments: 4 (0 AI-authored, 4 auto-generated); across 4 function(s); verified persisted in .i64: 103 named variables, 4 comments.

## What this feature does

The HomeKitDaemon update introduces significant enhancements to the management of HomeKit wallet keys and Matter-enabled accessory diagnostics. The primary functional changes include:

1.  **Wallet Key Provisioning**: Improved handling of ISO credentials for HomeKit wallet keys, specifically focusing on the asynchronous provisioning of NFC information and credential synchronization.
2.  **Matter Accessory Diagnostics**: New infrastructure for querying and reporting diagnostic information from Matter-enabled accessories, including support for Matter-specific operational certificate fetching and event routing.
3.  **Notification Logic**: Refined logic for handling characteristic change notifications for Matter locks, ensuring that bulletin notifications are only triggered by genuine state changes rather than characteristic read requests.
4.  **Device Setup & Resident Sync**: Enhanced controller logic for device setup and resident synchronization, including improved handling of remote requests and watchdog timers for companion link clients.

## How is it implemented


### Decompilation at `0x22edc3c78`

```c
__int64 __fastcall -[HMDHomeWalletKeyManager addISOCredentialWithPassAtURL:walletKey:flow:completion:](
        void *void_a1,
        __int64 n_a2,
        __int64 n_a3,
        void *void_a4,
        __int64 n_a5,
        __int64 n_a6)
{
  __int64 n_v11; // x0
  __int64 n_v12; // x0
  void *nfcInfos; // x22
  __int64 n_v14; // x0
  void *namap; // x0
  void *void_v16; // x25
  void *schedulerWithDispatchQueue; // x0
  void *reschedule; // x0
  void *void_v19; // x27
  __int64 n_v20; // x1
  __int64 n_v21; // x2
  __int64 n_v22; // x3
  __int64 addCompletionBlock; // x0
  __int64 n_v24; // x0
  __int64 n_v25; // x0
  __int64 n_v26; // x0
  __int64 n_v27; // x0
  __int64 n_v28; // x0
  __int64 n_v29; // x0
  __int64 n_v30; // x0
  __int64 n_v31; // x0
  __int64 n_v32; // x0
  __int64 n_v33; // x0
  __int64 n_v34; // x0
  _QWORD n_v36[5]; // [xsp+0h] [xbp-C0h] BYREF
  _QWORD n_v37[7]; // [xsp+28h] [xbp-98h] BYREF

  n_v11 = MEMORY[0x2347EC9D0](void_a1, n_a2);
  n_v12 = MEMORY[0x2347EC9F0](n_v11);
  MEMORY[0x2347ECA00](n_v12);
  nfcInfos = (void *)MEMORY[0x2347EC990](objc_msgSend(void_a4, "nfcInfos"));
  n_v37[0] = MEMORY[0x278A3C7E8];
  n_v37[1] = 3221225472LL;
  n_v37[2] = __83__HMDHomeWalletKeyManager_addISOCredentialWithPassAtURL_walletKey_flow_completion___block_invoke;
  n_v37[3] = &unk_2793B6258;
  n_v37[4] = void_a1;
  n_v37[5] = n_a3;
  n_v37[6] = n_a5;
  n_v14 = MEMORY[0x2347EC9F0]();
  MEMORY[0x2347EC9D0](n_v14);
  namap = objc_msgSend((id)MEMORY[0x2347EC990](objc_msgSend(nfcInfos, "na_map:", n_v37)), "combineAllFutures");
  void_v16 = (void *)MEMORY[0x2347EC990](namap);
  schedulerWithDispatchQueue = objc_msgSend(
                                 MEMORY[0x2789E6050],
                                 "schedulerWithDispatchQueue:",
                                 MEMORY[0x2347EC990](objc_msgSend(void_a1, "workQueue")));
  reschedule = objc_msgSend(void_v16, "reschedule:", MEMORY[0x2347EC990](schedulerWithDispatchQueue));
  void_v19 = (void *)MEMORY[0x2347EC990](reschedule);
  n_v36[0] = MEMORY[0x278A3C7E8];
  n_v36[1] = 3221225472LL;
  n_v36[2] = __83__HMDHomeWalletKeyManager_addISOCredentialWithPassAtURL_walletKey_flow_completion___block_invoke_2;
  n_v36[3] = &unk_2793BDA98;
  n_v36[4] = n_a6;
  MEMORY[0x2347ECA00](void_v19, n_v20, n_v21, n_v22);
  addCompletionBlock = MEMORY[0x2347ECB70](objc_msgSend(void_v19, "addCompletionBlock:", n_v36));
  n_v24 = MEMORY[0x2347EC900](addCompletionBlock);
  n_v25 = MEMORY[0x2347EC8F0](n_v24);
  n_v26 = MEMORY[0x2347EC8D0](n_v25);
  n_v27 = MEMORY[0x2347EC8E0](n_v26);
  n_v28 = MEMORY[0x2347EC8C0](n_v27);
  n_v29 = MEMORY[0x2347EC8B0](n_v28);
  n_v30 = MEMORY[0x2347EC930](n_v29);
  n_v31 = MEMORY[0x2347EC930](n_v30);
  n_v32 = MEMORY[0x2347EC930](n_v31);
  n_v33 = MEMORY[0x2347EC8A0](n_v32);
  n_v34 = MEMORY[0x2347EC890](n_v33);
  return MEMORY[0x2347EC870](n_v34);
}
```

### Decompilation at `0x22f4a0468`

```c
__int64 __fastcall -[HMDSiriSecureAccessoryAccessController initWithDataSource:watchAuthDataSource:](
        __int64 n_a1,
        __int64 n_a2,
        __int64 n_a3,
        __int64 n_a4)
{
  __int64 n_v7; // x0
  __int64 n_v8; // x0
  __int64 n_v9; // x21
  __int64 n_v10; // x0
  __int64 n_v11; // x0
  __int64 n_v12; // x0
  _QWORD n_v14[2]; // [xsp+0h] [xbp-30h] BYREF

  n_v7 = MEMORY[0x2347EC9D0](n_a1, n_a2);
  MEMORY[0x2347EC9F0](n_v7);
  n_v14[0] = n_a1;
  n_v14[1] = off_2794117F0;
  n_v8 = MEMORY[0x2347EC7D0](n_v14, 0x1FB7FC150uLL);
  n_v9 = n_v8;
  if ( n_v8 )
  {
    n_v10 = MEMORY[0x2347ECB30](n_v8 + 8, n_a3);
    n_v11 = MEMORY[0x2347EC9F0](n_v10);
    *(_QWORD *)(n_v9 + 16) = n_a4;
    n_v8 = MEMORY[0x2347EC930](n_v11);
  }
  n_v12 = MEMORY[0x2347EC890](n_v8);
  MEMORY[0x2347EC870](n_v12);
  return n_v9;
}
```

### Decompilation at `0x22eba5c68`

```c
__int64 __fastcall +[HMDHome sanitizedOriginalSourceForMessage:](__int64 n_a1, void *void_a2)
{
  __int64 n_v4; // x21
  void *messagePayload; // x0
  void *void_v6; // x20
  __int64 unsignedIntegerValue; // x0
  void *source; // x23
  __int64 n_v9; // x8
  __int64 n_v10; // x9
  __int64 n_v11; // x23
  __int64 n_v12; // x0
  __int64 n_v13; // x24
  __int64 n_v14; // x0
  __int64 n_v15; // x0
  __int64 n_v16; // x0
  __int64 n_v17; // x0
  __int64 n_v18; // x0
  __int64 n_v19; // x0
  __int64 n_v21; // x0
  int n_v22; // [xsp+0h] [xbp-70h] BYREF
  __int64 n_v23; // [xsp+4h] [xbp-6Ch]
  __int16 n_v24; // [xsp+Ch] [xbp-64h]
  __CFString *cfstr_v25; // [xsp+Eh] [xbp-62h]
  __int16 n_v26; // [xsp+16h] [xbp-5Ah]
  void *void_v27; // [xsp+18h] [xbp-58h]
  __int64 n_v28; // [xsp+28h] [xbp-48h]

  n_v28 = *MEMORY[0x278A3C7F8];
  MEMORY[0x2347EC9D0]();
  n_v4 = MEMORY[0x2347EC820](n_a1);
  messagePayload = objc_msgSend(
                     (id)MEMORY[0x2347EC990](objc_msgSend(void_a2, "messagePayload")),
                     "hmf_numberForKey:",
                     &stru_284693590);
  void_v6 = (void *)MEMORY[0x2347EC990](messagePayload);
  MEMORY[0x2347EC8C0]();
  if ( !void_v6 )
  {
    source = objc_msgSend(void_a2, "source");
    goto LABEL_17;
  }
  unsignedIntegerValue = (__int64)objc_msgSend(void_v6, "unsignedIntegerValue");
  source = (void *)unsignedIntegerValue;
  if ( unsignedIntegerValue > 1069 )
  {
    if ( (unsigned __int64)(unsignedIntegerValue - 1070) <= 0x3C
      && ((1LL << ((unsigned __int8)unsignedIntegerValue - 46)) & 0x1004010040100401LL) != 0
      || (unsigned __int64)(unsignedIntegerValue - 1140) <= 0x3C
      && ((1LL << ((unsigned __int8)unsignedIntegerValue - 116)) & 0x1004010040100401LL) != 0 )
    {
      goto LABEL_17;
    }
    if ( (unsigned __int64)(unsignedIntegerValue - 1210) <= 0x14 )
    {
      n_v9 = 1LL << ((unsigned __int8)unsignedIntegerValue + 70);
      n_v10 = 1049601;
LABEL_12:
      if ( (n_v9 & n_v10) != 0 )
        goto LABEL_17;
    }
  }
  else
  {
    if ( (unsigned __int64)unsignedIntegerValue < 0xB )
      goto LABEL_17;
    if ( (unsigned __int64)(unsignedIntegerValue - 1000) <= 0x3C )
    {
      n_v9 = 1LL << ((unsigned __int8)unsignedIntegerValue + 24);
      n_v10 = 0x1004010040100401LL;
      goto LABEL_12;
    }
  }
  n_v11 = MEMORY[0x2347EC6D0]();
  MEMORY[0x2347ECA00]();
  n_v12 = MEMORY[0x2347EAA90](n_v4);
  n_v13 = MEMORY[0x2347EC990](n_v12);
  n_v14 = MEMORY[0x2347ECBA0](n_v13, 16);
  if ( (_DWORD)n_v14 )
  {
    n_v15 = MEMORY[0x2347EAA80](n_v4);
    n_v22 = 138543874;
    n_v23 = MEMORY[0x2347EC990](n_v15);
    n_v24 = 2114;
    cfstr_v25 = &stru_284693590;
    n_v26 = 2114;
    void_v27 = void_v6;
    n_v16 = MEMORY[0x2347EBB30](
              &dword_22E68A000,
              n_v13,
              16,
              "%{public}@Unknown value for '%{public}@': %{public}@",
              &n_v22,
              32);
    n_v14 = MEMORY[0x2347EC8E0](n_v16);
  }
  n_v17 = MEMORY[0x2347EC8D0](n_v14);
  MEMORY[0x2347EC8A0](n_v17);
  j__OBJC_CLASS___HMDACWGKeyManager_613(n_v11);
  source = 0;
LABEL_17:
  n_v18 = MEMORY[0x2347EC890]();
  n_v19 = MEMORY[0x2347EC870](n_v18);
  if ( *MEMORY[0x278A3C7F8] == n_v28 )
    return (__int64)source;
  n_v21 = MEMORY[0x2347EBAE0](n_v19);
  return -[HMDHome _areWriteRequestsAllowed:message:completion:](n_v21);
}
```

### Decompilation at `0x22eba9b38`

```c
__int64 __fastcall -[HMDHome _handleMatterLockChangedCharacteristics:message:remoteRequest:](
        void *void_a1,
        __int64 n_a2,
        void *void_a3,
        void *void_a4,
        char char_a5)
{
  __int64 n_v9; // x0
  unsigned __int8 primaryResident; // w24
  __int64 n_v11; // x0
  __int64 n_v12; // x0
  __int64 n_v13; // x22
  __int64 n_v14; // x0
  __int64 n_v15; // x23
  __int64 n_v16; // x0
  __int64 n_v17; // x0
  const char *str_v18; // x3
  __int64 n_v19; // x1
  __int64 n_v20; // x5
  unsigned int name; // w25
  __int64 n_v22; // x0
  __int64 n_v23; // x0
  __int64 n_v24; // x23
  __int64 n_v25; // x0
  __int64 n_v26; // x0
  __int64 n_v27; // x0
  __int64 naeach; // x0
  __int64 n_v29; // x0
  __int64 result; // x0
  __int64 n_v31; // x0
  _QWORD n_v32[6]; // [xsp+8h] [xbp-98h] BYREF
  char char_v33; // [xsp+38h] [xbp-68h]
  int n_v34; // [xsp+40h] [xbp-60h] BYREF
  __int64 n_v35; // [xsp+44h] [xbp-5Ch]
  __int16 n_v36; // [xsp+4Ch] [xbp-54h]
  void *void_v37; // [xsp+4Eh] [xbp-52h]
  __int64 n_v38; // [xsp+58h] [xbp-48h]

  n_v38 = *MEMORY[0x278A3C7F8];
  n_v9 = MEMORY[0x2347EC9D0](void_a1, n_a2);
  MEMORY[0x2347EC9F0](n_v9);
  primaryResident = (unsigned __int8)objc_msgSend(
                                       (id)MEMORY[0x2347EC990](objc_msgSend(void_a1, "primaryResident")),
                                       "isCurrentDevice");
  n_v11 = MEMORY[0x2347EC8C0]();
  if ( (primaryResident & 1) == 0 )
  {
    n_v13 = MEMORY[0x2347EC6D0](n_v11);
    MEMORY[0x2347ECA00]();
    n_v14 = MEMORY[0x2347EAA90](void_a1);
    n_v15 = MEMORY[0x2347EC990](n_v14);
    n_v16 = MEMORY[0x2347ECBA0](n_v15, 1);
    if ( (_DWORD)n_v16 )
    {
      n_v17 = MEMORY[0x2347EAA80](void_a1);
      n_v34 = 138543362;
      n_v35 = MEMORY[0x2347EC990](n_v17);
      str_v18 = "%{public}@Not handling Matter lock changed characteristic notification because this device is not the primary resident.";
      n_v19 = n_v15;
      n_v20 = 12;
LABEL_9:
      n_v26 = MEMORY[0x2347EBB30](&dword_22E68A000, n_v19, 1, str_v18, &n_v34, n_v20);
      n_v16 = MEMORY[0x2347EC8D0](n_v26);
    }
LABEL_10:
    n_v27 = MEMORY[0x2347EC8C0](n_v16);
    MEMORY[0x2347EC8A0](n_v27);
    naeach = j__OBJC_CLASS___HMDACWGKeyManager_613(n_v13);
    goto LABEL_11;
  }
  if ( (unsigned int)objc_msgSend(
                       (id)MEMORY[0x2347EC990](objc_msgSend(void_a4, "name")),
                       "isEqualToString:",
                       &stru_28468BF10) )
  {
    n_v12 = MEMORY[0x2347EC8C0]();
    goto LABEL_7;
  }
  name = (unsigned int)objc_msgSend(
                         (id)MEMORY[0x2347EC990](objc_msgSend(void_a4, "name")),
                         "isEqualToString:",
                         &stru_28468BEB0);
  n_v22 = MEMORY[0x2347EC8D0]();
  n_v12 = MEMORY[0x2347EC8C0](n_v22);
  if ( name )
  {
LABEL_7:
    n_v13 = MEMORY[0x2347EC6D0](n_v12);
    MEMORY[0x2347ECA00]();
    n_v23 = MEMORY[0x2347EAA90](void_a1);
    n_v24 = MEMORY[0x2347EC990](n_v23);
    n_v16 = MEMORY[0x2347ECBA0](n_v24, 1);
    if ( (_DWORD)n_v16 )
    {
      n_v25 = MEMORY[0x2347EAA80](void_a1);
      n_v34 = 138543618;
      n_v35 = MEMORY[0x2347EC990](n_v25);
      n_v36 = 2112;
      void_v37 = void_a4;
      str_v18 = "%{public}@_handleMatterLockChangedCharacteristics: We are seeing characteristics changed, but from a cha"
                "racteristic read request. These values have not just actually changed, so we should not show a bulletin. message=%@";
      n_v19 = n_v24;
      n_v20 = 22;
      goto LABEL_9;
    }
    goto LABEL_10;
  }
  n_v32[0] = MEMORY[0x278A3C7E8];
  n_v32[1] = 3221225472LL;
  n_v32[2] = __73__HMDHome__handleMatterLockChangedCharacteristics_message_remoteRequest___block_invoke;
  n_v32[3] = &unk_2793B87F8;
  n_v32[4] = void_a1;
  MEMORY[0x2347EC9F0](n_v12);
  n_v32[5] = void_a4;
  char_v33 = char_a5;
  naeach = MEMORY[0x2347EC930](objc_msgSend(void_a3, "na_each:", n_v32));
LABEL_11:
  n_v29 = MEMORY[0x2347EC890](naeach);
  result = MEMORY[0x2347EC870](n_v29);
  if ( *MEMORY[0x278A3C7F8] != n_v38 )
  {
    n_v31 = MEMORY[0x2347EBAE0](result);
    return __73__HMDHome__handleMatterLockChangedCharacteristics_message_remoteRequest___block_invoke(n_v31);
  }
  return result;
}
```

The implementation relies on several new controller classes and manager methods:

*   **Wallet Key Management**: The `HMDHomeWalletKeyManager` handles the complex lifecycle of adding ISO credentials. It uses a future-based approach to map and combine NFC information across multiple sources, ensuring that all necessary credentials are ready before finalizing the wallet pass. The process is scheduled on a dedicated work queue to maintain responsiveness.
*   **Matter Lock Notifications**: The `_handleMatterLockChangedCharacteristics` method in `HMDHome` acts as a gatekeeper. It first verifies if the current device is the primary resident. If it is, it inspects the incoming message to distinguish between actual state changes and simple read requests. If the change is identified as a read request, it suppresses the bulletin notification to prevent redundant user alerts.
*   **Diagnostic Controller**: The `HMDAppleMediaAccessoryDiagnosticInfoController` provides a structured way to collect and describe diagnostic data. It integrates with the existing HomeKit infrastructure to allow the daemon to query accessory states and report them back to the system or remote clients.
*   **Configuration Logging**: New log event classes (`HMDConfigurationLogEvent`) have been added to track widget counts and home configurations, providing better telemetry for HomeKit performance and usage patterns.

## How to trigger this feature

*   **Wallet Key Provisioning**: Triggered when a user adds a supported lock to their home or when the system automatically attempts to provision a wallet key during device setup or migration.
*   **Matter Diagnostics**: Triggered by internal system requests or remote diagnostic queries directed at Matter-enabled accessories.
*   **Lock Notifications**: Triggered by characteristic change events from Matter-enabled locks. The suppression logic is triggered automatically when the daemon receives a characteristic read request that mimics a change event.

## Vulnerability Assessment

The changes appear to be focused on functional stability and feature parity rather than security patches. The logic added to `_handleMatterLockChangedCharacteristics` is a functional improvement to prevent "notification spam" rather than a mitigation for a specific vulnerability. No structural changes to memory management, bounds checking, or authentication protocols were observed in the decompiled code. The use of `combineAllFutures` and `reschedule` in the wallet key manager suggests a focus on handling asynchronous operations more reliably, which reduces the likelihood of race conditions during the provisioning flow.

## Evidence

*   **Symbols**: `HMDHomeWalletKeyManager`, `HMDAppleMediaAccessoryDiagnosticInfoController`, `HMDDeviceSetupConfiguringController`.
*   **Strings**: `%{public}@[Flow: %@] Acquiring wallet provisioning assertion`, `%{public}@_handleMatterLockChangedCharacteristics: We are seeing characteristics changed, but from a characteristic read request`.
*   **Addresses**: `0x22eba9b38` (Matter lock handling), `0x22edc3c78` (Wallet key credential addition).

## AI Prioritisation Scoring System

- **feature_analysis**
  - **Tier**: TIER_2
  - **Category**: HomeKitDaemon
  - **Reasoning**: The changes represent significant functional updates to HomeKit wallet key provisioning and Matter accessory diagnostics. While these are core business-logic updates with clear functional impact, they do not appear to be security-critical patches or privilege boundary changes.

