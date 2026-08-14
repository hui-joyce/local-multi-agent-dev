## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ " URLBagKey=%{public,signpost.telemetry:string1,name=URLBagKey}@  enableTelemetry=YES "`
- **Analysis mode**: decompiled
- **Database annotations** -- variable renames: 134 (0 AI-authored, 134 auto-generated); comments: 3 (0 AI-authored, 3 auto-generated); across 3 function(s); verified persisted in .i64: 134 named variables, 3 comments.
- **Apple Security Notes**: matches advisory component `AuthKit` -- Apple confirms a security-relevant change here; this analysis examines the likely vulnerability patch.

## What this feature does

The AuthKit framework has been significantly enhanced with new authentication and security features in iOS 26.6 (23G71). The most notable changes include:

**New Authentication Classes:**
- `AKBasicServerRequest` and `AKBasicServerResponse` - New classes for handling basic server requests and responses, supporting secure coding protocol
- These classes handle HTTP-based authentication flows with proper request/response serialization

**Enhanced ADP (Account Data Protocol) Flow:**
- New methods `beginADPFlowWithID:altDSID:completion:` and `completeADPFlowWithID:success:completion:` in `AKWalrusController`
- These methods manage the complete ADP flow lifecycle with proper error handling and telemetry

**Failure Injection Headers:**
- New `AKFeatureManager` class with `isFailureInjectionHeaderEnabled` method
- Methods for generating and managing failure injection headers (`failureInjectionHeadersForURL:completion:`)

**PDP (Privacy Data Protection) Blob Generation:**
- New `_enrichPostbackWithPDBlob:model:completion:` method in `AKAccountRecoveryStepChangePassword`
- Enhanced PDP blob generation with proper eligibility checking and error handling

**Local Authentication Improvements:**
- New `AKAccountRecoveryStepLocalAuthentication` class with multiple authentication methods
- Methods for local secret prompting, client info extraction, and response processing

**Telemetry and Analytics:**
- New strings for telemetry tracking (`URLBagKey`, `adpCohort`, `rcUpsellEligibilityCohort`)
- Enhanced event tracking with timestamps and flow IDs

**Security Enhancements:**
- New strings related to adult age verification (`ADULT_AGE_VERIFICATION_STATUS_REQUIRED_SPYGLASS`)
- Unverified adult background restriction flags (`UNVERIFIED_ADULT_BACKGROUND_RESTRICTION_REQUIRED`, `UNVERIFIED_ADULT_BACKGROUND_RESTRICTION_REQUIRED_MINI_BUDDY`)
- New security keys and certificate parsing functions (`_CTEvaluateKeyTransparency`, `_X509ExtensionParseKeyTransparencyLeaf`)

**Removed Features:**
- `AKAccountManager` methods for timestamp and cohort tracking have been removed, suggesting these features were migrated to the new classes
- Some older exception tables and block implementations have been removed

## How is it implemented


### Decompilation at `0x193dff2c8`

```c
__int64 __fastcall -[AKAccountRecoveryStepChangePassword _enrichPostbackWithPDPBlob:model:completion:](
        __int64 n_a1,
        void *void_a2,
        __int64 n_a3,
        __int64 n_a4,
        __int64 n_a5)
{
  __int64 n_v5; // x0
  __int64 n_v6; // x0
  __int64 n_v7; // x0
  __int64 n_v8; // x0
  __int64 n_v9; // x0
  __int64 n_v10; // x0
  __int64 n_v11; // x0
  __int64 isPDPEligibleForAccount; // x0
  __int64 n_v13; // x0
  void *void_v14; // x0
  __int64 n_v15; // x3
  __int64 n_v16; // x0
  __int64 result; // x0
  void *void_v18; // [xsp+18h] [xbp-2B8h]
  void *void_v19; // [xsp+28h] [xbp-2A8h]
  void *initWithPassword; // [xsp+78h] [xbp-258h]
  __int64 n_v21; // [xsp+80h] [xbp-250h]
  unsigned int n_v22; // [xsp+8Ch] [xbp-244h]
  void *sharedInstance; // [xsp+A0h] [xbp-230h]
  char char_v24; // [xsp+ACh] [xbp-224h]
  __int64 n_v25; // [xsp+B0h] [xbp-220h]
  unsigned int n_v26; // [xsp+BCh] [xbp-214h]
  void *sharedInstance_2; // [xsp+C8h] [xbp-208h]
  __int64 n_v28; // [xsp+D0h] [xbp-200h]
  unsigned int n_v29; // [xsp+DCh] [xbp-1F4h]
  __int64 username; // [xsp+E8h] [xbp-1E8h]
  void *context; // [xsp+F0h] [xbp-1E0h]
  void *sharedInstance_3; // [xsp+F8h] [xbp-1D8h]
  __int64 n_v33; // [xsp+100h] [xbp-1D0h]
  unsigned int n_v34; // [xsp+10Ch] [xbp-1C4h]
  void *sharedManager; // [xsp+120h] [xbp-1B0h]
  unsigned int isDBRTwoEnabled; // [xsp+12Ch] [xbp-1A4h]
  __int64 n_v37; // [xsp+130h] [xbp-1A0h]
  unsigned int n_v38; // [xsp+13Ch] [xbp-194h]
  __int64 n_v41; // [xsp+158h] [xbp-178h] BYREF
  int n_v42; // [xsp+160h] [xbp-170h]
  int n_v43; // [xsp+164h] [xbp-16Ch]
  __int64 (__fastcall *int64fastcal_v44)(); // [xsp+168h] [xbp-168h]
  void *void_v45; // [xsp+170h] [xbp-160h]
  __int64 n_v46; // [xsp+178h] [xbp-158h] BYREF
  __int64 n_v47; // [xsp+180h] [xbp-150h] BYREF
  __int64 n_v48; // [xsp+188h] [xbp-148h] BYREF
  __int64 n_v49; // [xsp+190h] [xbp-140h] BYREF
  unsigned __int8 n_v50; // [xsp+19Fh] [xbp-131h]
  __int64 n_v51; // [xsp+1A0h] [xbp-130h] BYREF
  __int64 n_v52; // [xsp+1A8h] [xbp-128h] BYREF
  void *void_v53; // [xsp+1B0h] [xbp-120h] BYREF
  __int64 n_v54; // [xsp+1B8h] [xbp-118h] BYREF
  __int64 objectForKeyedSubscript; // [xsp+1C0h] [xbp-110h] BYREF
  __int64 objectForKeyedSubscript_2; // [xsp+1C8h] [xbp-108h] BYREF
  char char15_v57[15]; // [xsp+1D0h] [xbp-100h] BYREF
  unsigned __int8 n_v58; // [xsp+1DFh] [xbp-F1h]
  __int64 n_v59; // [xsp+1E0h] [xbp-F0h] BYREF
  char char_v60; // [xsp+1EFh] [xbp-E1h]
  id sharedInstance_4; // [xsp+1F0h] [xbp-E0h]
  __int64 authKitAccountWithAltDSID; // [xsp+1F8h] [xbp-D8h] BYREF
  char char15_v63[15]; // [xsp+200h] [xbp-D0h] BYREF
  unsigned __int8 n_v64; // [xsp+20Fh] [xbp-C1h]
  __int64 n_v65; // [xsp+210h] [xbp-C0h] BYREF
  __int64 altDSIDForAccount; // [xsp+218h] [xbp-B8h] BYREF
  char char15_v67[15]; // [xsp+220h] [xbp-B0h] BYREF
  unsigned __int8 n_v68; // [xsp+22Fh] [xbp-A1h]
  __int64 n_v69; // [xsp+230h] [xbp-A0h] BYREF
  __int64 iCloudAccountForAppleID; // [xsp+238h] [xbp-98h] BYREF
  char char15_v71[15]; // [xsp+240h] [xbp-90h] BYREF
  unsigned __int8 n_v72; // [xsp+24Fh] [xbp-81h]
  __int64 n_v73; // [xsp+250h] [xbp-80h] BYREF
  int n_v74; // [xsp+25Ch] [xbp-74h]
  char char15_v75[15]; // [xsp+260h] [xbp-70h] BYREF
  unsigned __int8 n_v76; // [xsp+26Fh] [xbp-61h]
  __int64 n_v77; // [xsp+270h] [xbp-60h] BYREF
  __int64 n_v78; // [xsp+278h] [xbp-58h] BYREF
  id id_v79; // [xsp+280h] [xbp-50h] BYREF
  id id2_v80[2]; // [xsp+288h] [xbp-48h] BYREF
  __int64 n_v81; // [xsp+298h] [xbp-38h]
  char char24_v82[24]; // [xsp+2A0h] [xbp-30h] BYREF
  __int64 n_v83; // [xsp+2B8h] [xbp-18h]

  n_v83 = *MEMORY[0x1E5DB2C30];
  n_v81 = n_a1;
  id2_v80[1] = void_a2;
  id2_v80[0] = 0;
  sub_193F00978(id2_v80, n_a3);
  id_v79 = 0;
  sub_193F00978(&id_v79, n_a4);
  n_v78 = 0;
  n_v5 = sub_193F00978(&n_v78, n_a5);
  if ( *(_QWORD *)(n_v81 + 8) )
  {
    sharedManager = (void *)MEMORY[0x193FFF920](objc_msgSend(off_1E6812730, "sharedManager"));
    isDBRTwoEnabled = (unsigned int)objc_msgSend(sharedManager, "isDBRTwoEnabled");
    MEMORY[0x1E5DAECD0](sharedManager);
    if ( isDBRTwoEnabled )
    {
      sharedInstance_3 = (void *)MEMORY[0x193FFF920](objc_msgSend(off_1E6812428, "sharedInstance"));
      context = (void *)MEMORY[0x193FFF920](objc_msgSend(id_v79, "context"));
      username = MEMORY[0x193FFF920](objc_msgSend(context, "username"));
      iCloudAccountForAppleID = MEMORY[0x193FFF920](objc_msgSend(sharedInstance_3, "iCloudAccountForAppleID:"));
      MEMORY[0x1E5DAECD0](username);
      MEMORY[0x1E5DAECD0](context);
      n_v8 = MEMORY[0x1E5DAECD0](sharedInstance_3);
      if ( iCloudAccountForAppleID )
      {
        sharedInstance_2 = (void *)MEMORY[0x193FFF920](objc_msgSend(off_1E6812428, "sharedInstance"));
        altDSIDForAccount = MEMORY[0x193FFF920](objc_msgSend(sharedInstance_2, "altDSIDForAccount:", iCloudAccountForAppleID));
        n_v10 = MEMORY[0x1E5DAECD0](sharedInstance_2);
        if ( altDSIDForAccount )
        {
          sharedInstance = (void *)MEMORY[0x193FFF920](objc_msgSend(off_1E6812428, "sharedInstance"));
          authKitAccountWithAltDSID = MEMORY[0x193FFF920](
                                        objc_msgSend(
                                          sharedInstance,
                                          "authKitAccountWithAltDSID:error:",
                                          altDSIDForAccount,
                                          0));
          isPDPEligibleForAccount = MEMORY[0x1E5DAECD0](sharedInstance);
          char_v60 = 0;
          char_v24 = 1;
          if ( authKitAccountWithAltDSID )
          {
            sharedInstance_4 = (id)MEMORY[0x193FFF920](objc_msgSend(off_1E6812428, "sharedInstance"));
            char_v60 = 1;
            isPDPEligibleForAccount = (__int64)objc_msgSend(
                                                 sharedInstance_4,
                                                 "isPDPEligibleForAccount:",
// [truncated: decompiler/model output too long or degenerate]
```

### Decompilation at `0x193d70bec`

```c
__int64 +[AKAttestationRequestData supportsSecureCoding]()
{
  return 1;
}
```

### Decompilation at `0x193de50d4`

```c
__int64 __fastcall -[AKAccountRecoveryStepLocalAuthentication _beginLocalAuthenticationWithResponse:model:completion:](
        void *void_a1,
        void *void_a2,
        __int64 n_a3,
        __int64 n_a4,
        __int64 n_a5)
{
  __int64 n_v5; // x0
  __int64 n_v6; // x0
  __int64 result; // x0
  void *request; // [xsp+8h] [xbp-1F8h]
  void *void_v9; // [xsp+10h] [xbp-1F0h]
  __int64 dictionaryWithObjects; // [xsp+18h] [xbp-1E8h]
  void *cliUtilities; // [xsp+20h] [xbp-1E0h]
  void *resourceLoadDelegate; // [xsp+28h] [xbp-1D8h]
  void *void_v13; // [xsp+30h] [xbp-1D0h]
  void *cliUtilities_2; // [xsp+40h] [xbp-1C0h]
  __int64 n_v15; // [xsp+78h] [xbp-188h]
  __int64 akerrorWithCode; // [xsp+80h] [xbp-180h]
  __int64 n_v17; // [xsp+90h] [xbp-170h]
  __int64 akerrorWithCode_2; // [xsp+98h] [xbp-168h]
  __int64 n_v19; // [xsp+A0h] [xbp-160h]
  unsigned int n_v20; // [xsp+ACh] [xbp-154h]
  __int64 httpResponse; // [xsp+C0h] [xbp-140h]
  __int64 configuration; // [xsp+C8h] [xbp-138h]
  void *cliUtilities_3; // [xsp+D0h] [xbp-130h]
  __int64 configuration_2; // [xsp+D8h] [xbp-128h]
  __int64 n_v25; // [xsp+E8h] [xbp-118h]
  __int64 akerrorWithCode_3; // [xsp+F0h] [xbp-110h]
  __int64 n_v27; // [xsp+F8h] [xbp-108h]
  unsigned int n_v28; // [xsp+104h] [xbp-FCh]
  __int64 n_v31; // [xsp+128h] [xbp-D8h] BYREF
  int n_v32; // [xsp+130h] [xbp-D0h]
  int n_v33; // [xsp+134h] [xbp-CCh]
  __int64 (__fastcall *int64fastcal_v34)(); // [xsp+138h] [xbp-C8h]
  void *void_v35; // [xsp+140h] [xbp-C0h]
  __int64 n_v36; // [xsp+148h] [xbp-B8h] BYREF
  __int64 n_v37; // [xsp+150h] [xbp-B0h] BYREF
  void *mutableCopy; // [xsp+158h] [xbp-A8h] BYREF
  id configuration_3; // [xsp+160h] [xbp-A0h] BYREF
  id promptForLocalSecretWithModel; // [xsp+168h] [xbp-98h] BYREF
  _BYTE n_v41[15]; // [xsp+170h] [xbp-90h] BYREF
  unsigned __int8 n_v42; // [xsp+17Fh] [xbp-81h]
  __int64 n_v43; // [xsp+180h] [xbp-80h] BYREF
  int n_v44; // [xsp+18Ch] [xbp-74h]
  _BYTE n_v45[15]; // [xsp+190h] [xbp-70h] BYREF
  unsigned __int8 n_v46; // [xsp+19Fh] [xbp-61h]
  __int64 n_v47; // [xsp+1A0h] [xbp-60h] BYREF
  __int64 localAuthClientInfoFromResponse; // [xsp+1A8h] [xbp-58h] BYREF
  __int64 n_v49; // [xsp+1B0h] [xbp-50h] BYREF
  id id_v50; // [xsp+1B8h] [xbp-48h] BYREF
  id id2_v51[2]; // [xsp+1C0h] [xbp-40h] BYREF
  id id_v52; // [xsp+1D0h] [xbp-30h]
  __CFString *cfstr_v53; // [xsp+1D8h] [xbp-28h] BYREF
  id id_v54; // [xsp+1E0h] [xbp-20h] BYREF
  __int64 n_v55; // [xsp+1E8h] [xbp-18h]

  n_v55 = *MEMORY[0x1E5DB2C30];
  id_v52 = void_a1;
  id2_v51[1] = void_a2;
  id2_v51[0] = 0;
  sub_193F00978(id2_v51, n_a3);
  id_v50 = 0;
  sub_193F00978(&id_v50, n_a4);
  n_v49 = 0;
  sub_193F00978(&n_v49, n_a5);
  localAuthClientInfoFromResponse = MEMORY[0x193FFF920](objc_msgSend(id_v52, "_localAuthClientInfoFromResponse:", id2_v51[0]));
  if ( localAuthClientInfoFromResponse )
  {
    cliUtilities_3 = (void *)MEMORY[0x193FFF920](objc_msgSend(id_v50, "cliUtilities"));
    configuration = MEMORY[0x193FFF920](objc_msgSend(id_v50, "configuration"));
    httpResponse = MEMORY[0x193FFF920](objc_msgSend(id2_v51[0], "httpResponse"));
    objc_msgSend(
      cliUtilities_3,
      "updateConfiguration:fromXMLAttributes:response:",
      configuration,
      localAuthClientInfoFromResponse);
    MEMORY[0x1E5DAECD0](httpResponse);
    MEMORY[0x1E5DAECD0](configuration);
    MEMORY[0x1E5DAECD0](cliUtilities_3);
    configuration_2 = MEMORY[0x193FFF920](objc_msgSend(id_v50, "configuration"));
    MEMORY[0x1E5DAECD0](configuration_2);
    if ( configuration_2 )
    {
      promptForLocalSecretWithModel = (id)MEMORY[0x193FFF920](objc_msgSend(id_v52, "_promptForLocalSecretWithModel:", id_v50));
      if ( objc_msgSend(promptForLocalSecretWithModel, "length") )
      {
        configuration_3 = (id)MEMORY[0x193FFF920](objc_msgSend(id_v50, "configuration"));
        request = (void *)MEMORY[0x193FFF920](objc_msgSend(configuration_3, "request"));
        mutableCopy = objc_msgSend(request, "mutableCopy");
        MEMORY[0x1E5DAECD0](request);
        cliUtilities = (void *)MEMORY[0x193FFF920](objc_msgSend(id_v50, "cliUtilities"));
        void_v9 = mutableCopy;
        cfstr_v53 = &stru_1EFF46D30;
        id_v54 = promptForLocalSecretWithModel;
        dictionaryWithObjects = MEMORY[0x193FFF920](
                                  objc_msgSend(
                                    MEMORY[0x1E5D2A2D8],
                                    "dictionaryWithObjects:forKeys:count:",
                                    &id_v54,
                                    &cfstr_v53,
                                    1));
        objc_msgSend(cliUtilities, "signXMLRequest:withPostbackDictionary:", void_v9);
        MEMORY[0x1E5DAECD0](dictionaryWithObjects);
        MEMORY[0x1E5DAECD0](cliUtilities);
        resourceLoadDelegate = (void *)MEMORY[0x193FFF920](objc_msgSend(configuration_3, "resourceLoadDelegate"));
        objc_msgSend(resourceLoadDelegate, "signRequest:", mutableCopy);
        MEMORY[0x1E5DAECD0](resourceLoadDelegate);
        cliUtilities_2 = (void *)MEMORY[0x193FFF920](objc_msgSend(id_v50, "cliUtilities"));
        void_v13 = mutableCopy;
        n_v31 = MEMORY[0x1E5DB2C10];
        n_v32 = -1073741824;
        n_v33 = 0;
        int64fastcal_v34 = __99__AKAccountRecoveryStepLocalAuthentication__beginLocalAuthenticationWithResponse_model_completion___block_invoke;
        void_v35 = &unk_1E6815FB0;
        n_v37 = MEMORY[0x1E5DAECD8](n_v49);
        n_v36 = MEMORY[0x1E5DAECD8](id_v52);
        objc_msgSend(cliUtilities_2, "beginDataTaskWithRequest:completionHandler:", void_v13, &n_v31);
        MEMORY[0x1E5DAECD0](cliUtilities_2);
        sub_193F00978(&n_v36, 0);
        sub_193F00978(&n_v37, 0);
        sub_193F00978(&mutableCopy, 0);
        sub_193F00978(&configuration_3, 0);
        n_v44 = 0;
      }
      else
      {
        AKPrintError(&stru_1EFF46DF0);
        if ( n_v49 )
        {
          n_v15 = n_v49;
          akerrorWithCode = MEMORY[0x193FFF9
// [truncated: decompiler/model output too long or degenerate]
```

The implementation shows a complete rewrite of the authentication flow with new classes replacing older functionality. The `AKBasicServerRequest` and `AKBasicServerResponse` classes handle the core HTTP authentication protocol, with proper support for secure coding (NSCoding) for archiving.

The ADP flow implementation in `AKWalrusController` manages the complete lifecycle from initiation to completion, with proper error handling and telemetry tracking. The flow includes:
- Flow initialization with unique IDs and alternative DSIDs
- Request transmission to the daemon service
- Response handling and completion callback

The PDP blob generation is integrated into the password change flow, with eligibility checking based on account state and proper error handling for generation failures.

Local authentication has been enhanced with a new step-based recovery flow that includes:
- Client info extraction from responses
- Configuration updates based on server responses
- Secret prompting and verification

The new implementation also includes comprehensive telemetry tracking with URL bag keys, flow IDs, and various cohort identifiers for analytics purposes.

## How to trigger this feature

The new authentication features are triggered through:
1. **ADP Flow Initiation**: When an account needs to be authenticated or updated, the `beginADPFlowWithID:altDSID:completion:` method is called with a unique flow ID and alternative DSID
2. **Password Recovery**: When a user initiates password recovery, the `AKAccountRecoveryStepLocalAuthentication` class handles the local authentication flow
3. **PDP Blob Generation**: During password change operations, if PDP is eligible for the account, the `_enrichPostbackWithPDBlob:model:completion:` method is called
4. **Failure Injection**: When requests need to be tested with failure scenarios, the `failureInjectionHeadersForURL:error:` method generates appropriate headers

The features are integrated into the existing authentication controller (`AKAppleIDAuthenticationController`) which orchestrates the different authentication methods and flows.

## Vulnerability Assessment

**Security-Relevant Change:**
The diff shows the introduction of new security features and removal of older, potentially vulnerable code paths:

1. **New Secure Coding Support**: `AKBasicServerRequest` and `AKBasicServerResponse` now support secure coding, which is critical for proper serialization/deserialization of authentication data

2. **Enhanced PDP Protection**: The new `_enrichPostbackWithPDBlob:model:completion:` method implements proper PDP blob generation with eligibility checking, which is a privacy protection mechanism

3. **Adult Age Verification**: New strings and constants related to adult age verification (`ADULT_AGE_VERIFICATION_STATUS_REQUIRED_SPYGLASS`, `UNVERIFIED_ADULT_BACKGROUND_RESTRICTION_REQUIRED`) suggest enhanced age verification controls

4. **Failure Injection Headers**: The new `AKFeatureManager` and related methods for generating failure injection headers suggest improved testing and validation of authentication flows

5. **Certificate Transparency**: New functions for parsing key transparency leaves (`_CTEvaluateKeyTransparency`, `_X509ExtensionParseKeyTransparencyLeaf`) indicate enhanced certificate validation

**Patch Mechanism:**
The changes appear to be **new feature additions** rather than security patches for existing vulnerabilities. The evidence shows:
- Addition of new classes and methods
- Removal of older, less secure implementation paths (AKAccountManager)
- Introduction of new privacy and security features

**Evidence:**
1. **New Symbols**: `+ [AKBasicServerRequest supportsSecureCoding]`, `+ [AKBasicServerResponse supportsSecureCoding]`
2. **New Strings**: `"com.apple.private.security.revoke"`, `"%s[%d] revoked access to %s"`
3. **New Constants**: `_AKOSEDomainAdultAgeVerificationStatusRequiredSpyglass`, `_CTEvaluateKeyTransparency`
4. **Removed Symbols**: Multiple `AKAccountManager` methods removed, suggesting migration to new architecture

**Assessment:**
This appears to be a **feature enhancement release** rather than a security patch. The changes introduce new authentication mechanisms and privacy features, but don't appear to fix specific vulnerabilities in the existing code. The removal of `AKAccountManager` methods suggests architectural refactoring rather than vulnerability mitigation.

**Tier Assignment:** TIER_2 - The changes represent core business logic updates to the authentication system with observable runtime behavior, but don't appear to address specific security vulnerabilities.

## AI Prioritisation Scoring System

- **Apple Security Notes correlation + binary diff analysis**
  - **Tier**: TIER_2
  - **Category**: Authentication Framework Enhancement
  - **Reasoning**: The AuthKit changes represent new authentication features (ADP flow, PDP blob generation, local auth improvements) rather than security patches. While the changes include privacy enhancements (adult age verification, certificate transparency), they appear to be feature additions rather than fixes for specific vulnerabilities. The removal of AKAccountManager methods suggests architectural refactoring to new classes (AKBasicServerRequest/Response). No evidence of memory safety fixes, privilege escalation prevention, or critical security boundary changes.

