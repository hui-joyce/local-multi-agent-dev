## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "%s: entered - Launching test script is not supported on this OS!"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 72 (2 AI-authored, 70 auto-generated); comments: 7 (3 AI-authored, 4 auto-generated); across 4 function(s); verified persisted in .i64: 72 named variables, 16 comments.

## What this feature does

The `demod_helper` binary has been updated to include more rigorous security validation for demo-mode manifests. The primary functional change is the introduction of a "rigorous" security check mode for segmented manifests, which includes enhanced signature verification, blocklist management for specific file paths, and stricter OS version compatibility checks. The feature ensures that demo-mode configurations—specifically those involving HomeKit data and factory-signed components—are validated against the current OS version and manifest requirements before allowing installation or restoration.

## How is it implemented


### Decompilation at `0x10000ecd8`

```c
bool __cdecl -[MSDDemoManifestCheck secureManifestCheckForSegmentedManifest:options:](
        MSDDemoManifestCheck *self,
        SEL sel_a2,
        id id_a3,
        id id_a4)
{
  id id_v7; // x0
  id id_v8; // x0
  NSSet *allowedISTSignedComponents; // x22
  id getAllowedISTSignedComponents; // x22
  void *manifestVersion; // x22
  bool flag_v12; // w21

  id_v7 = objc_retain(id_a3);
  id_v8 = objc_retain(id_a4);
  if ( !id_a3 )
  {
    sub_10002BF4C(id_v8);
LABEL_9:
    flag_v12 = 0;
    goto LABEL_6;
  }
  allowedISTSignedComponents = objc_retainAutoreleasedReturnValue(-[MSDDemoManifestCheck allowedISTSignedComponents](self, "allowedISTSignedComponents"));
  objc_release(allowedISTSignedComponents);
  if ( !allowedISTSignedComponents )
  {
    getAllowedISTSignedComponents = objc_retainAutoreleasedReturnValue(
                                      -[MSDDemoManifestCheck getAllowedISTSignedComponents:](
                                        self,
                                        "getAllowedISTSignedComponents:",
                                        id_a3));
    -[MSDDemoManifestCheck setAllowedISTSignedComponents:](
      self,
      "setAllowedISTSignedComponents:",
      getAllowedISTSignedComponents);
    objc_release(getAllowedISTSignedComponents);
  }
  -[MSDDemoManifestCheck setSegmentedManifestWithRigorousFlag:](self, "setSegmentedManifestWithRigorousFlag:", id_a3);
  manifestVersion = objc_retainAutoreleasedReturnValue(objc_msgSend(id_a3, "objectForKey:", CFSTR("Version")));
  -[MSDDemoManifestCheck setManifestVersion:](
    self,
    "setManifestVersion:",
    objc_msgSend(manifestVersion, "unsignedIntValue"));
  objc_release(manifestVersion);
  if ( !-[MSDDemoManifestCheck runSecurityCheck:](self, "runSecurityCheck:", id_a4) )
  {
    sub_10002BED4();
    goto LABEL_9;
  }
  -[MSDDemoManifestCheck registerEntitlementNotificationHandler](self, "registerEntitlementNotificationHandler");
  flag_v12 = 1;
LABEL_6:
  objc_release(id_a4);
  objc_release(id_a3);
  return flag_v12;
}
```

### Decompilation at `0x10000d120`

```c
id __cdecl -[MSDDemoManifestCheck verifyFactoryManifestSignature:forDataSectionKeys:](
        MSDDemoManifestCheck *self,
        SEL sel_a2,
        id id_a3,
        id id_a4)
{
  id id_v7; // x0
  id id_v8; // x0
  NSMutableDictionary *securityOptions; // x21
  void *void_v10; // x23
  void *objectForKey; // x25
  void *void_v12; // x24
  id verifyManifestSignature; // x22
  __int64 vars8; // [xsp+48h] [xbp+8h]

  id_v7 = objc_retain(id_a3);
  id_v8 = objc_retain(id_a4);
  securityOptions = objc_opt_new(&OBJC_CLASS___NSMutableDictionary);
  void_v10 = (void *)MGCopyAnswer(CFSTR("ProductVersion"), 0);
  objectForKey = objc_retainAutoreleasedReturnValue(objc_msgSend(id_a3, "objectForKey:", CFSTR("Info")));
  void_v12 = 0;
  if ( !objectForKey )
    void_v12 = objc_retainAutoreleasedReturnValue(objc_msgSend(0, "objectForKey:", CFSTR("MinimumOSVersion")));
  if ( ((unsigned int)objc_msgSend(void_v10, "isEqualToString:", void_v12) & 1) == 0 )
    -[NSMutableDictionary setObject:forKey:](
      securityOptions,
      "setObject:forKey:",
      &__kCFBooleanTrue,
      CFSTR("ExcludeBlocklistItem"));
  verifyManifestSignature = objc_retainAutoreleasedReturnValue(
                              -[MSDDemoManifestCheck verifyManifestSignature:forDataSectionKeys:withOptions:](
                                self,
                                "verifyManifestSignature:forDataSectionKeys:withOptions:",
                                id_a3,
                                id_a4,
                                securityOptions));
  objc_release(objectForKey);
  objc_release(void_v10);
  objc_release(securityOptions);
  objc_release(void_v12);
  objc_release(id_a4);
  objc_release(id_a3);
  if ( ((vars8 ^ (2 * vars8)) & 0x4000000000000000LL) != 0 )
    __break(0xC471u);
  return objc_autoreleaseReturnValue(verifyManifestSignature);
}
```

### Decompilation at `0x10000f56c`

```c
bool __cdecl -[MSDDemoManifestCheck runSecurityChecksForSection:dataType:componentName:options:](
        MSDDemoManifestCheck *self,
        SEL sel_a2,
        id id_a3,
        id id_a4,
        id id_a5,
        id id_a6)
{
  id id_v11; // x0
  id id_v12; // x0
  id id_v13; // x0
  id id_v14; // x0
  NSSet *settingsComponentNames; // x24
  unsigned int containsObject; // w25
  unsigned __int8 n_v17; // w0
  bool flag_v18; // w23

  id_v11 = objc_retain(id_a4);
  id_v12 = objc_retain(id_a5);
  id_v13 = objc_retain(id_a6);
  id_v14 = objc_retain(id_a3);
  settingsComponentNames = objc_retainAutoreleasedReturnValue(-[MSDDemoManifestCheck settingsComponentNames](self, "settingsComponentNames"));
  containsObject = -[NSSet containsObject:](settingsComponentNames, "containsObject:", id_a5);
  objc_release(settingsComponentNames);
  if ( containsObject )
    n_v17 = -[MSDDemoManifestCheck runSettingsSecurityCheckForSection:component:](
              self,
              "runSettingsSecurityCheckForSection:component:",
              id_a3,
              id_a5);
  else
    n_v17 = -[MSDDemoManifestCheck runFileSecurityChecksForSection:dataType:options:](
              self,
              "runFileSecurityChecksForSection:dataType:options:",
              id_a3,
              id_a4,
              id_a6);
  flag_v18 = n_v17;
  objc_release(id_a3);
  objc_release(id_a6);
  objc_release(id_a5);
  objc_release(id_a4);
  return flag_v18;
}
```

### Decompilation at `0x10000edd0`

```c
bool __cdecl -[MSDDemoManifestCheck runSecurityCheck:](MSDDemoManifestCheck *self, SEL sel_a2, id id_a3)
{
  id id_v5; // x0
  id getSecurityCheckSectionNames; // x20
  id getappIconLayoutBackupName; // x21
  id getBackupSectionName; // x22
  __int64 n_v9; // x1
  __int64 n_v10; // x2
  __int64 n_v11; // x3
  __int64 n_v12; // x4
  __int64 n_v13; // x5
  __int64 n_v14; // x6
  __int64 n_v15; // x7
  NSObject *nsobject_v16; // x24
  NSDictionary *segmentedManifestWithRigorousFlag; // x24
  id id_v18; // x0
  id id_v19; // x0
  id id_v20; // x0
  id id_v21; // x0
  __int64 n_v22; // x0
  __int64 n_v23; // x1
  __int64 n_v24; // x2
  __int64 n_v25; // x3
  __int64 n_v26; // x4
  __int64 n_v27; // x5
  __int64 n_v28; // x6
  __int64 n_v29; // x7
  NSObject *nsobject_v30; // x23
  char char_v31; // w23
  id id_v33; // x0
  _QWORD n_v34[4]; // [xsp+0h] [xbp-C0h] BYREF
  id id_v35; // [xsp+20h] [xbp-A0h]
  MSDDemoManifestCheck *msddemomanif_v36; // [xsp+28h] [xbp-98h]
  id id_v37; // [xsp+30h] [xbp-90h]
  id id_v38; // [xsp+38h] [xbp-88h]
  id id_v39; // [xsp+40h] [xbp-80h]
  __int64 *int64_v40; // [xsp+48h] [xbp-78h]
  __int64 n_v41; // [xsp+50h] [xbp-70h] BYREF
  __int64 *p_n_v41; // [xsp+58h] [xbp-68h]
  __int64 n_v43; // [xsp+60h] [xbp-60h]
  char char_v44; // [xsp+68h] [xbp-58h]
  uint8_t buf[24]; // [xsp+70h] [xbp-50h] BYREF

  id_v5 = objc_retain(id_a3);
  n_v41 = 0;
  p_n_v41 = &n_v41;
  n_v43 = 0x2020000000LL;
  char_v44 = 0;
  getSecurityCheckSectionNames = objc_retainAutoreleasedReturnValue(
                                   -[MSDDemoManifestCheck getSecurityCheckSectionNames](
                                     self,
                                     "getSecurityCheckSectionNames"));
  getappIconLayoutBackupName = objc_retainAutoreleasedReturnValue(-[MSDDemoManifestCheck getappIconLayoutBackupName](self, "getappIconLayoutBackupName"));
  getBackupSectionName = objc_retainAutoreleasedReturnValue(-[MSDDemoManifestCheck getBackupSectionName](self, "getBackupSectionName"));
  nsobject_v16 = (NSObject *)objc_retainAutoreleasedReturnValue((id)sub_100022D34(
                                                                      getBackupSectionName,
                                                                      n_v9,
                                                                      n_v10,
                                                                      n_v11,
                                                                      n_v12,
                                                                      n_v13,
                                                                      n_v14,
                                                                      n_v15));
  if ( os_log_type_enabled(nsobject_v16, OS_LOG_TYPE_DEFAULT) )
  {
    *(_WORD *)buf = 0;
    _os_log_impl(
      (void *)&_mh_execute_header,
      nsobject_v16,
      OS_LOG_TYPE_DEFAULT,
      "Starting rigorous security checks",
      buf,
      2u);
  }
  objc_release(nsobject_v16);
  segmentedManifestWithRigorousFlag = objc_retainAutoreleasedReturnValue(
                                        -[MSDDemoManifestCheck segmentedManifestWithRigorousFlag](
                                          self,
                                          "segmentedManifestWithRigorousFlag"));
  n_v34[0] = _NSConcreteStackBlock;
  n_v34[1] = 3221225472LL;
  n_v34[2] = sub_10000F068;
  n_v34[3] = &unk_100050DF0;
  id_v18 = objc_retain(getSecurityCheckSectionNames);
  id_v35 = getSecurityCheckSectionNames;
  msddemomanif_v36 = self;
  int64_v40 = &n_v41;
  id_v19 = objc_retain(id_a3);
  id_v37 = id_a3;
  id_v20 = objc_retain(getappIconLayoutBackupName);
  id_v38 = getappIconLayoutBackupName;
  id_v21 = objc_retain(getBackupSectionName);
  id_v39 = getBackupSectionName;
  -[NSDictionary enumerateKeysAndObjectsUsingBlock:](
    segmentedManifestWithRigorousFlag,
    "enumerateKeysAndObjectsUsingBlock:",
    n_v34);
  objc_release(segmentedManifestWithRigorousFlag);
  if ( (p_n_v41[3] & 1) != 0 )
  {
    nsobject_v30 = (NSObject *)objc_retainAutoreleasedReturnValue((id)sub_100022D34(
                                                                        n_v22,
                                                                        n_v23,
                                                                        n_v24,
                                                                        n_v25,
                                                                        n_v26,
                                                                        n_v27,
                                                                        n_v28,
                                                                        n_v29));
    if ( os_log_type_enabled(nsobject_v30, OS_LOG_TYPE_DEFAULT) )
    {
      *(_DWORD *)buf = 136315138;
      *(_QWORD *)&buf[4] = "-[MSDDemoManifestCheck runSecurityCheck:]";
      _os_log_impl(
        (void *)&_mh_execute_header,
        nsobject_v30,
        OS_LOG_TYPE_DEFAULT,
        "%s:Cleared all checks for manifest. Approving future installations",
        buf,
        0xCu);
    }
  }
  else
  {
    id_v33 = objc_retainAutoreleasedReturnValue((id)sub_100022D34(
                                                      n_v22,
                                                      n_v23,
                                                      n_v24,
                                                      n_v25,
                                                      n_v26,
                                                      n_v27,
                                                      n_v28,
                                                      n_v29));
    sub_10002BFC4(id_v33, buf);
    nsobject_v30 = *(NSObject **)buf;
  }
  objc_release(nsobject_v30);
  char_v31 = *((_BYTE *)p_n_v41 + 24);
  objc_release(id_v39);
  objc_release(id_v38);
  objc_release(id_v37);
  objc_release(id_v35);
  objc_release(getBackupSectionNa
// [truncated: decompiler/model output too long or degenerate]
```

The implementation centers on the `MSDDemoManifestCheck` class, which now orchestrates security checks through a more granular, block-based approach. 

In `secureManifestCheckForSegmentedManifest:options:`, the system initializes the security context by retrieving allowed signed components and setting a "rigorous" flag on the manifest. It then triggers the security check process, which iterates through manifest sections. If the security check passes, it registers an entitlement notification handler to maintain the security state.

The `verifyFactoryManifestSignature:forDataSectionKeys:` method implements a version-aware validation logic. It compares the device's `ProductVersion` against the `MinimumOSVersion` specified in the manifest. If these versions do not match, it dynamically injects an `ExcludeBlocklistItem` flag into the options dictionary, which instructs the subsequent security verification process to skip specific blocklisted items during the signature check.

The `runSecurityChecksForSection:dataType:componentName:options:` method acts as a dispatcher. It checks if a component is part of the "settings" category by querying a set of component names. If it is a settings component, it routes the request to a specialized settings security check; otherwise, it defaults to standard file-based security checks.

## How to trigger this feature

This feature is triggered during the processing of demo-mode manifests, specifically when the system attempts to verify a segmented manifest or perform a factory manifest signature check. It is invoked by the `demod_helper` daemon when it receives a request to install or restore a demo configuration, particularly when the manifest contains sections related to `HomeKitDomain` or requires rigorous validation due to OS version mismatches.

## Vulnerability Assessment

The changes represent a hardening of the demo-mode installation process. By introducing explicit version checking and the ability to exclude blocklisted items dynamically, the system prevents potential mismatches between the demo manifest and the host OS that could lead to unstable or insecure states. 

The addition of `ExcludeBlocklistItem` logic suggests a mitigation for potential out-of-bounds or unauthorized access issues where certain files (like `homed` datastore files) might be incorrectly handled during a restore if the OS version is not strictly compatible. The use of `malloc` checks and improved logging indicates a focus on memory safety and observability during the security check phase. No direct vulnerabilities were identified; rather, these changes appear to be a proactive security patch to ensure that demo-mode configurations cannot bypass system-level file protections or integrity checks.

## Evidence

- **New Symbols/Methods**: `-[MSDDemoManifestCheck runSecurityCheck:]`, `-[MSDDemoManifestCheck secureManifestCheckForSegmentedManifest:options:]`, `-[MSDDemoManifestCheck verifyFactoryManifestSignature:forDataSectionKeys:]`.
- **New Strings**: `ExcludeBlocklistItem`, `HomeKitDomain`, `Library/homed/datastore.sqlite`, `RigorousTestingOverride`.
- **Logic Changes**: The introduction of `NSMutableDictionary` for options in `verifyFactoryManifestSignature` allows for dynamic security policy adjustments based on `ProductVersion` vs `MinimumOSVersion`.
- **Binary Diff**: Increased function count and `__oslogstring` section size, reflecting the addition of detailed security logging and new validation logic.

## AI Prioritisation Scoring System

- **feature_analysis**
  - **Tier**: TIER_1
  - **Category**: security_hardening
  - **Reasoning**: The changes involve critical security boundary enforcement for demo-mode manifests, including signature verification, OS version compatibility checks, and dynamic blocklist management for sensitive system files.

