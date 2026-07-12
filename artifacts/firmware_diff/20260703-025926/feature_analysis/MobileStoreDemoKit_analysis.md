## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "-[MSDDemoManifestCheck runSecurityCheck:]"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 283 (3 AI-authored, 280 auto-generated); comments: 8 (2 AI-authored, 6 auto-generated); across 6 function(s); verified persisted in .i64: 283 named variables, 6 comments.

## What this feature does

The `MobileStoreDemoKit` framework has been updated to include more rigorous security validation for demo device manifests and enhanced control over peer device immersion levels. The primary functional additions involve a new security check mechanism for segmented manifests, which ensures that demo content and configuration files are properly signed and verified before being applied to a device. Additionally, the framework now supports remote management of "immersion levels" for peer demo devices, likely used to control the intensity or state of demo experiences across multiple connected units.

## How is it implemented


### Decompilation at `0x263467a6c`

```c
__int64 __fastcall -[MSDDemoManifestCheck secureManifestCheckForSegmentedManifest:options:](
        void *void_a1,
        __int64 n_a2,
        void *manifest,
        __int64 options)
{
  __int64 n_v7; // x0
  __int64 n_v8; // x0
  __int64 allowedISTSignedComponents; // x22
  void *setAllowedISTSignedComponents; // x0
  void *setManifestVersion; // x0
  void *secureManifestCheckForSegmentedManifest; // x0
  __int64 n_v13; // x21
  __int64 n_v14; // x0

  n_v7 = MEMORY[0x2639E0B20](void_a1, n_a2);
  n_v8 = MEMORY[0x2639E0B40](n_v7);
  if ( !manifest )
  {
    secureManifestCheckForSegmentedManifest = (void *)-[MSDDemoManifestCheck secureManifestCheckForSegmentedManifest:options:].cold.2(n_v8);
LABEL_9:
    n_v13 = 0;
    goto LABEL_6;
  }
  allowedISTSignedComponents = MEMORY[0x2639E0B00](objc_msgSend(void_a1, "allowedISTSignedComponents"));
  MEMORY[0x2639E0A50]();
  if ( !allowedISTSignedComponents )
  {
    setAllowedISTSignedComponents = objc_msgSend(
                                      void_a1,
                                      "setAllowedISTSignedComponents:",
                                      MEMORY[0x2639E0B00](objc_msgSend(void_a1, "getAllowedISTSignedComponents:", manifest)));
    MEMORY[0x2639E0A50](setAllowedISTSignedComponents);
  }
  objc_msgSend(void_a1, "setSegmentedManifestWithRigorousFlag:", manifest);
  setManifestVersion = objc_msgSend(
                         void_a1,
                         "setManifestVersion:",
                         objc_msgSend(
                           (id)MEMORY[0x2639E0B00](objc_msgSend(manifest, "objectForKey:", &stru_287638AE0)),
                           "unsignedIntValue"));
  MEMORY[0x2639E0A50](setManifestVersion);
  if ( ((unsigned int)objc_msgSend(void_a1, "runSecurityCheck:", options) & 1) == 0 )
  {
    secureManifestCheckForSegmentedManifest = (void *)-[MSDDemoManifestCheck secureManifestCheckForSegmentedManifest:options:].cold.1();
    goto LABEL_9;
  }
  secureManifestCheckForSegmentedManifest = objc_msgSend(void_a1, "registerEntitlementNotificationHandler");
  n_v13 = 1;
LABEL_6:
  n_v14 = MEMORY[0x2639E0A30](secureManifestCheckForSegmentedManifest);
  MEMORY[0x2639E0A20](n_v14);
  return n_v13;
}
```

### Decompilation at `0x263465eb4`

```c
void __fastcall -[MSDDemoManifestCheck verifyFactoryManifestSignature:forDataSectionKeys:](
        void *void_a1,
        __int64 n_a2,
        void *void_a3,
        __int64 n_a4)
{
  __int64 n_v7; // x0
  void *void_v8; // x21
  void *void_v9; // x23
  __int64 n_v10; // x24
  __int64 n_v11; // x0
  __int64 n_v12; // x0
  __int64 n_v13; // x0
  __int64 n_v14; // x0
  __int64 n_v15; // x0
  __int64 vars8; // [xsp+48h] [xbp+8h]

  n_v7 = MEMORY[0x2639E0B20](void_a1, n_a2);
  MEMORY[0x2639E0B40](n_v7);
  void_v8 = (void *)MEMORY[0x2639E09E0](MEMORY[0x278972998]);
  void_v9 = (void *)MEMORY[0x2639E0660](&stru_2876394A0, 0);
  n_v10 = 0;
  if ( !MEMORY[0x2639E0B00](objc_msgSend(void_a3, "objectForKey:", &stru_287638C80)) )
    n_v10 = MEMORY[0x2639E0B00](objc_msgSend(0, "objectForKey:", &stru_287638D40));
  if ( ((unsigned int)objc_msgSend(void_v9, "isEqualToString:", n_v10) & 1) == 0 )
    objc_msgSend(void_v8, "setObject:forKey:", MEMORY[0x278972A98], &stru_2876394C0);
  MEMORY[0x2639E0B00](objc_msgSend(void_a1, "verifyManifestSignature:forDataSectionKeys:withOptions:", void_a3, n_a4, void_v8));
  n_v11 = MEMORY[0x2639E0A80]();
  n_v12 = MEMORY[0x2639E0A60](n_v11);
  n_v13 = MEMORY[0x2639E0A40](n_v12);
  n_v14 = MEMORY[0x2639E0A70](n_v13);
  n_v15 = MEMORY[0x2639E0A30](n_v14);
  MEMORY[0x2639E0A20](n_v15);
  if ( ((vars8 ^ (2 * vars8)) & 0x4000000000000000LL) != 0 )
    __break(0xC471u);
  JUMPOUT(0x2639E0920LL);
}
```

### Decompilation at `0x263468300`

```c
void *__fastcall -[MSDDemoManifestCheck runSecurityChecksForSection:dataType:componentName:options:](
        void *void_a1,
        __int64 n_a2,
        __int64 n_a3,
        __int64 n_a4,
        __int64 n_a5,
        __int64 n_a6)
{
  __int64 n_v11; // x0
  __int64 n_v12; // x0
  __int64 n_v13; // x0
  unsigned int settingsComponentNames; // w25
  void *void_v15; // x0
  void *void_v16; // x23
  __int64 n_v17; // x0
  __int64 n_v18; // x0
  __int64 n_v19; // x0

  n_v11 = MEMORY[0x2639E0B20](void_a1, n_a2);
  n_v12 = MEMORY[0x2639E0B40](n_v11);
  n_v13 = MEMORY[0x2639E0B50](n_v12);
  MEMORY[0x2639E0B60](n_v13);
  settingsComponentNames = (unsigned int)objc_msgSend(
                                           (id)MEMORY[0x2639E0B00](objc_msgSend(void_a1, "settingsComponentNames")),
                                           "containsObject:",
                                           n_a5);
  MEMORY[0x2639E0A70]();
  if ( settingsComponentNames )
    void_v15 = objc_msgSend(void_a1, "runSettingsSecurityCheckForSection:component:", n_a3, n_a5);
  else
    void_v15 = objc_msgSend(void_a1, "runFileSecurityChecksForSection:dataType:options:", n_a3, n_a4, n_a6);
  void_v16 = void_v15;
  n_v17 = MEMORY[0x2639E0A50]();
  n_v18 = MEMORY[0x2639E0A40](n_v17);
  n_v19 = MEMORY[0x2639E0A30](n_v18);
  MEMORY[0x2639E0A20](n_v19);
  return void_v16;
}
```

### Decompilation at `0x263467b64`

```c
__int64 __fastcall -[MSDDemoManifestCheck runSecurityCheck:](void *void_a1, __int64 n_a2, const char *str_a3)
{
  const char *getSecurityCheckSectionNames; // x20
  const char *getappIconLayoutBackupName; // x21
  const char *getBackupSectionName; // x22
  __int64 n_v8; // x0
  __int64 n_v9; // x24
  __int64 n_v10; // x0
  void *segmentedManifestWithRigorousFlag; // x24
  __int64 n_v12; // x1
  __int64 n_v13; // x2
  __int64 n_v14; // x3
  __int64 n_v15; // x0
  __int64 n_v16; // x0
  __int64 n_v17; // x0
  __int64 enumerateKeysAndObjectsUsingBlock; // x0
  __int64 n_v19; // x0
  __int64 n_v20; // x23
  __int64 runSecurityCheck; // x0
  __int64 n_v22; // x0
  char char_v23; // w23
  __int64 n_v24; // x0
  __int64 n_v25; // x0
  __int64 n_v26; // x0
  __int64 n_v27; // x0
  __int64 n_v28; // x0
  __int64 n_v29; // x0
  __int64 n_v30; // x0
  __int64 n_v31; // x0
  __int64 n_v33; // x0
  __int64 n_v34; // x0
  __int64 n_v35; // x19
  __int64 n_v36; // x0
  const char *str_v37[10]; // [xsp+0h] [xbp-C0h] BYREF
  __int64 n_v38; // [xsp+50h] [xbp-70h] BYREF
  __int64 *p_n_v38; // [xsp+58h] [xbp-68h]
  __int64 n_v40; // [xsp+60h] [xbp-60h]
  char char_v41; // [xsp+68h] [xbp-58h]
  _DWORD n_v42[6]; // [xsp+70h] [xbp-50h] BYREF
  __int64 n_v43; // [xsp+88h] [xbp-38h]

  n_v43 = *MEMORY[0x278A3C7F8];
  MEMORY[0x2639E0B20](void_a1, n_a2);
  n_v38 = 0;
  p_n_v38 = &n_v38;
  n_v40 = 0x2020000000LL;
  char_v41 = 0;
  getSecurityCheckSectionNames = (const char *)MEMORY[0x2639E0B00](objc_msgSend(void_a1, "getSecurityCheckSectionNames"));
  getappIconLayoutBackupName = (const char *)MEMORY[0x2639E0B00](objc_msgSend(void_a1, "getappIconLayoutBackupName"));
  getBackupSectionName = (const char *)MEMORY[0x2639E0B00](objc_msgSend(void_a1, "getBackupSectionName"));
  n_v8 = defaultLogHandle(getBackupSectionName);
  n_v9 = MEMORY[0x2639E0B00](n_v8);
  n_v10 = MEMORY[0x2639E0C50](n_v9, 0);
  if ( (_DWORD)n_v10 )
  {
    LOWORD(n_v42[0]) = 0;
    n_v10 = MEMORY[0x2639E0800](&dword_263459000, n_v9, 0, "Starting rigorous security checks", n_v42, 2);
  }
  MEMORY[0x2639E0A70](n_v10);
  segmentedManifestWithRigorousFlag = (void *)MEMORY[0x2639E0B00](objc_msgSend(void_a1, "segmentedManifestWithRigorousFlag"));
  str_v37[0] = (const char *)MEMORY[0x278A3C7E8];
  str_v37[1] = (const char *)3221225472LL;
  str_v37[2] = (const char *)__41__MSDDemoManifestCheck_runSecurityCheck___block_invoke;
  str_v37[3] = (const char *)&unk_27A716070;
  n_v15 = MEMORY[0x2639E0B40](segmentedManifestWithRigorousFlag, n_v12, n_v13, n_v14);
  str_v37[4] = getSecurityCheckSectionNames;
  str_v37[5] = (const char *)void_a1;
  str_v37[9] = (const char *)&n_v38;
  n_v16 = MEMORY[0x2639E0B20](n_v15);
  str_v37[6] = str_a3;
  n_v17 = MEMORY[0x2639E0B50](n_v16);
  str_v37[7] = getappIconLayoutBackupName;
  MEMORY[0x2639E0B60](n_v17);
  str_v37[8] = getBackupSectionName;
  enumerateKeysAndObjectsUsingBlock = MEMORY[0x2639E0A70](
                                        objc_msgSend(
                                          segmentedManifestWithRigorousFlag,
                                          "enumerateKeysAndObjectsUsingBlock:",
                                          str_v37));
  if ( (p_n_v38[3] & 1) != 0 )
  {
    n_v19 = defaultLogHandle(enumerateKeysAndObjectsUsingBlock);
    n_v20 = MEMORY[0x2639E0B00](n_v19);
    runSecurityCheck = MEMORY[0x2639E0C50](n_v20, 0);
    if ( (_DWORD)runSecurityCheck )
    {
      n_v42[0] = 136315138;
      *(_QWORD *)&n_v42[1] = "-[MSDDemoManifestCheck runSecurityCheck:]";
      runSecurityCheck = MEMORY[0x2639E0800](
                           &dword_263459000,
                           n_v20,
                           0,
                           "%s:Cleared all checks for manifest. Approving future installations",
                           str_v37[0]);
    }
  }
  else
  {
    n_v33 = defaultLogHandle(enumerateKeysAndObjectsUsingBlock);
    n_v34 = MEMORY[0x2639E0B00](n_v33);
    runSecurityCheck = -[MSDDemoManifestCheck runSecurityCheck:].cold.1(n_v34, n_v42);
  }
  n_v22 = MEMORY[0x2639E0A60](runSecurityCheck);
  char_v23 = *((_BYTE *)p_n_v38 + 24);
  n_v24 = MEMORY[0x2639E0AC0](n_v22);
  n_v25 = MEMORY[0x2639E0AC0](n_v24);
  n_v26 = MEMORY[0x2639E0AC0](n_v25);
  n_v27 = MEMORY[0x2639E0AC0](n_v26);
  n_v28 = MEMORY[0x2639E0A50](n_v27);
  n_v29 = MEMORY[0x2639E0A40](n_v28);
  MEMORY[0x2639E0A30](n_v29);
  n_v30 = MEMORY[0x2639E07A0](&n_v38, 8);
  n_v31 = MEMORY[0x2639E0A20](n_v30);
  if ( *MEMORY[0x278A3C7F8] == n_v43 )
    return char_v23 & 1;
  n_v35 = MEMORY[0x2639E07D0](n_v31);
  MEMORY[0x2639E07A0](&n_v38, 8);
  n_v36 = MEMORY[0x2639E07B0](n_v35);
  return __41__MSDDemoManifestCheck_runSecurityCheck___block_invoke(n_v36);
}
```

### Decompilation at `0x26346d634`

```c
__int64 __fastcall -[MSDKPeerDemoDeviceManager setImmersionLevelOnPeer:immersionLevel:animationDuration:withCompletion:](
        void *void_a1,
        double flt_a2,
        double flt_a3,
        __int64 n_a4,
        void *peerDevice,
        const char *str_a6)
{
  void *void_v10; // x21
  __int64 n_v11; // x0
  __int64 n_v12; // x0
  __int64 n_v13; // x0
  __int64 n_v14; // x22
  __int64 n_v15; // x0
  __int64 n_v16; // x0
  __int64 n_v17; // x0
  void *remoteObjectProxyWithErrorHandler; // x22
  __int64 identifier; // x23
  __int64 n_v20; // x1
  __int64 n_v21; // x2
  __int64 n_v22; // x3
  __int64 seImmersionLevelOnPeerOfID; // x0
  __int64 n_v24; // x0
  __int64 n_v25; // x0
  __int64 n_v26; // x0
  __int64 n_v27; // x0
  __int64 n_v28; // x0
  __int64 n_v29; // x0
  __int64 result; // x0
  __int64 n_v31; // x19
  __int64 n_v32; // x0
  const char *str_v33[5]; // [xsp+0h] [xbp-C0h] BYREF
  _QWORD n_v34[5]; // [xsp+28h] [xbp-98h] BYREF
  int n_v35; // [xsp+50h] [xbp-70h]
  const char *setImmersionLevelOnPeer; // [xsp+54h] [xbp-6Ch]
  __int64 n_v37; // [xsp+68h] [xbp-58h]

  void_v10 = void_a1;
  n_v37 = *MEMORY[0x278A3C7F8];
  n_v11 = MEMORY[0x2639E0B20](void_a1, n_a4);
  n_v12 = MEMORY[0x2639E0B40](n_v11);
  n_v13 = defaultLogHandle(n_v12);
  n_v14 = MEMORY[0x2639E0B00](n_v13);
  n_v15 = MEMORY[0x2639E0C50](n_v14, 0);
  if ( (_DWORD)n_v15 )
  {
    n_v35 = 136315138;
    setImmersionLevelOnPeer = "-[MSDKPeerDemoDeviceManager setImmersionLevelOnPeer:immersionLevel:animationDuration:withCompletion:]";
    n_v15 = MEMORY[0x2639E0800](&dword_263459000, n_v14, 0, "%s: called.", str_v33[0]);
  }
  n_v16 = MEMORY[0x2639E0A50](n_v15);
  if ( str_a6 )
  {
    MEMORY[0x2639E0B50](n_v16);
    n_v17 = MEMORY[0x2639E0C10](void_v10);
    n_v34[0] = MEMORY[0x278A3C7E8];
    n_v34[1] = 3221225472LL;
    n_v34[2] = __101__MSDKPeerDemoDeviceManager_setImmersionLevelOnPeer_immersionLevel_animationDuration_withCompletion___block_invoke;
    n_v34[3] = &unk_27A7160C8;
    MEMORY[0x2639E0B40](n_v17);
    n_v34[4] = str_a6;
    remoteObjectProxyWithErrorHandler = (void *)MEMORY[0x2639E0B00](objc_msgSend(void_v10, "_remoteObjectProxyWithErrorHandler:", n_v34));
    identifier = MEMORY[0x2639E0B00](objc_msgSend(peerDevice, "identifier"));
    str_v33[0] = (const char *)MEMORY[0x278A3C7E8];
    str_v33[1] = (const char *)3221225472LL;
    str_v33[2] = (const char *)__101__MSDKPeerDemoDeviceManager_setImmersionLevelOnPeer_immersionLevel_animationDuration_withCompletion___block_invoke_2;
    str_v33[3] = (const char *)&unk_27A7160C8;
    MEMORY[0x2639E0B40](identifier, n_v20, n_v21, n_v22);
    str_v33[4] = str_a6;
    seImmersionLevelOnPeerOfID = MEMORY[0x2639E0A60](
                                   objc_msgSend(
                                     remoteObjectProxyWithErrorHandler,
                                     "seImmersionLevelOnPeerOfID:immersionLevel:animationDuration:withCompletion:",
                                     identifier,
                                     str_v33,
                                     flt_a2,
                                     flt_a3));
    n_v24 = MEMORY[0x2639E0A50](seImmersionLevelOnPeerOfID);
    n_v25 = MEMORY[0x2639E0AC0](n_v24);
    MEMORY[0x2639E0AC0](n_v25);
    n_v26 = MEMORY[0x2639E0C20](void_v10);
  }
  else
  {
    n_v27 = defaultLogHandle(n_v16);
    void_v10 = (void *)MEMORY[0x2639E0B00](n_v27);
    n_v26 = MEMORY[0x2639E0C50](void_v10, 16);
    if ( (_DWORD)n_v26 )
      n_v26 = -[MSDKPeerDemoDeviceManager setImmersionLevelOnPeer:immersionLevel:animationDuration:withCompletion:].cold.1(void_v10);
  }
  n_v28 = MEMORY[0x2639E0A40](n_v26);
  n_v29 = MEMORY[0x2639E0A30](n_v28);
  result = MEMORY[0x2639E0A20](n_v29);
  if ( *MEMORY[0x278A3C7F8] != n_v37 )
  {
    n_v31 = MEMORY[0x2639E07D0](result);
    MEMORY[0x2639E0C20](void_v10);
    n_v32 = MEMORY[0x2639E07B0](n_v31);
    return __101__MSDKPeerDemoDeviceManager_setImmersionLevelOnPeer_immersionLevel_animationDuration_withCompletion___block_invoke(n_v32);
  }
  return result;
}
```

The implementation of the security checks relies on the `MSDDemoManifestCheck` class, which now orchestrates a multi-stage verification process. When a segmented manifest is processed, the system first ensures that the allowed signed components are initialized. It then proceeds to verify the manifest version and triggers a security check that iterates through defined sections of the manifest. This process uses block-based enumeration to validate keys and objects against expected security policies. If the security checks pass, the system registers an entitlement notification handler to maintain the secure state.

For peer device management, the `MSDKPeerDemoDeviceManager` class has been updated to handle immersion level adjustments. This is implemented via an XPC-based remote proxy pattern. When a request to set an immersion level is received, the manager validates the input and then communicates with the remote peer device using an asynchronous XPC call. The implementation includes robust error handling and logging to ensure that if the remote proxy fails to initialize or the communication is interrupted, the system logs the failure appropriately.

## How to trigger this feature

The security check feature is triggered automatically when a new demo manifest is loaded or updated on the device, specifically when `secureManifestCheckForSegmentedManifest:options:` is invoked by the demo management subsystem. The immersion level control is triggered when the system or a user-initiated action calls `setImmersionLevelOnPeer:immersionLevel:animationDuration:withCompletion:` on the `MSDKPeerDemoDeviceManager`, typically during the configuration or synchronization phase of a demo device setup.

## Vulnerability Assessment

The changes in this update appear to be a hardening effort rather than a patch for a specific vulnerability. The introduction of `runSecurityCheck:` and the associated `verifyManifestSignature` methods suggests a shift toward more granular, section-based validation of demo manifests. By moving from a monolithic check to a segmented, block-based verification approach, the framework reduces the risk of partial manifest tampering. The addition of rigorous testing overrides and explicit blocklist management for file exclusions further indicates an effort to prevent unauthorized or malicious files from being restored or accessed during the demo lifecycle. No immediate memory safety vulnerabilities were identified in the new code paths; the logic follows standard Objective-C memory management patterns.

## Evidence

- **New Symbols**: `-[MSDDemoManifestCheck runSecurityCheck:]`, `-[MSDDemoManifestCheck verifyManifestSignature:forDataSectionKeys:withOptions:]`, `-[MSDKPeerDemoDeviceManager setImmersionLevelOnPeer:immersionLevel:animationDuration:withCompletion:]`.
- **New Strings**: "RigorousTestingOverride", "Excluding %{public}@ from section", "Library/homed/datastore.sqlite".
- **Logic Changes**: Transition from simple manifest verification to segmented, block-based security checks and the addition of XPC-based remote immersion level control.

## AI Prioritisation Scoring System

- **feature_analysis**
  - **Tier**: TIER_1
  - **Category**: security_hardening
  - **Reasoning**: The update introduces significant new security validation logic for demo manifests and expands the IPC surface for remote device management, which are critical areas for device integrity and security.

