## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "%@ - Could not find session with uniqueID %@ to setForceTCPFallbackOnCellUsingReinitiate, ignoring..."`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 0 (0 AI-authored, 0 auto-generated); comments: 0 (0 AI-authored, 0 auto-generated); across 0 function(s); verified persisted in .i64: 0 named variables, 0 comments.

## What this feature does

The `identityservicesd` binary manages Apple ID account synchronization, Key Transparency (KT) data, and secure messaging sessions (IDS). This update introduces a new security entitlement `com.apple.security.IDSEncryption.SecondaryEncryptionDisabled` and `com.apple.security.IDSEncryption.SecondaryRegistrationDisabled`, indicating a shift in how the system handles secondary encryption and registration for Apple ID accounts.

The feature implements a new identifier `_IDSSecondaryIdentityIdentifier` (address `0x100e34128`), which appears to be a data structure or constant used to track secondary identity information. This identifier is referenced by code at address `0x100e34128` (via `get_xrefs_to`), suggesting it is actively used in the binary's logic.

The diff shows the removal of several networking-related symbols and strings, including:
- `_IDSGlobalLinkOptionCallScreeningMode`
- `_NEVirtualInterfaceCreateNexus`
- `_nw_agent_add_to_interface`
- `_nw_endpoint_create_apple_service`
- `_nw_endpoint_get_apple_service_apple_id`
- `_nw_endpoint_get_apple_service_name`
- `_nw_endpoint_set_interface`
- `_nw_endpoint_set_txt_record`
- `_nw_interface_create_with_name`
- `_nw_txt_record_create_dictionary`
- `_nw_txt_record_set_key`

These removed symbols suggest that the binary is no longer responsible for creating or managing certain network interfaces and endpoints, possibly delegating this functionality to another component or simplifying the networking stack.

The addition of `_IDSSecondaryIdentityIdentifier` and the removal of networking-related symbols indicate a refactoring of the identity services to better support secondary encryption and registration, potentially improving security and privacy by reducing the attack surface related to network operations.

## How is it implemented

The implementation of the new feature involves the following changes:

1. **New Identifier**: The symbol `_IDSSecondaryIdentityIdentifier` is added, which is a data symbol located at address `0x100e34128`. This identifier is likely used to store or reference secondary identity information, such as a secondary Apple ID account or a secondary encryption key.

2. **Removed Networking Symbols**: Several networking-related symbols are removed, including:
   - `_IDSGlobalLinkOptionCallScreeningMode`
   - `_NEVirtualInterfaceCreateNexus`
   - `_nw_agent_add_to_interface`
   - `_nw_endpoint_create_apple_service`
   - `_nw_endpoint_get_apple_service_apple_id`
   - `_nw_endpoint_get_apple_service_name`
   - `_nw_endpoint_set_interface`
   - `_nw_endpoint_set_txt_record`
   - `_nw_interface_create_with_name`
   - `_nw_txt_record_create_dictionary`
   - `_nw_txt_record_set_key`

   These symbols were likely part of the networking stack used for creating and managing network interfaces and endpoints. Their removal suggests that the binary is no longer responsible for these operations, possibly delegating them to another component or simplifying the networking stack.

3. **New Strings**: Several new strings are added, including:
   - `"%@ - Could not find session with uniqueID %@ to setForceTCPFallbackOnCellUsingReinitiate, ignoring..."`
   - `"%@ - Could not find session with uniqueID %@ to setForceTCPFallbackOnWiFiUsingReinitiate, ignoring..."`
   - `"%@[%@]"`
   - `"%@[%llu]"`
   - `"%s - sessionID %@"`
   - `"%s - sessionID %@, setForceTCPFallbackOnCell: %@"`
   - `"%s - sessionID %@, setForceTCPFallbackOnWiFi: %@"`
   - `"-[IDSGroupAgent createNewSessionForClientRequest:isClient:registrationCompletionBlock:]"`
   - `"-[IDSGroupAgent registerAgent]_block_invoke"`
   - `"-[IDSGroupAgent registerEntitledAgent]_block_invoke"`
   - `"-[IDSLinkManager clearSharedSessionHasJoinedForIDSSession:]"`
   - `"-[IDSLinkManager setForceTCPFallbackOnCell:forceTCPFallbackOnCell:]"`
   - `"-[IDSLinkManager setForceTCPFallbackOnWiFi:forceTCPFallbackOnWiFi:]"`
   - `"-[IDSLinkManager setIsReliableUnicastSession:isClient:forIDSSession:]"`
   - `"20:46:27"`
   - `"<%@: %p { guid: %@, sendingURI: %@, sendingPushToken: %@, receivingURI: %@, receivingPushToken: %@ }>"`
   - `"<%@> link: %@ didFinishConvergenceForRelaySessionID: %@."`
   - `@\"CUTUnsafePromise\"52@0:8@\"NSData\"16@\"IDSCryptionContext\"24@\"IDSMPPublicDeviceIdentityContainer\"32@\"NSString\"40B48"`
   - `@\"NSData\"80@0:8@\"NSData\"16@\"IDSCryptionContext\"24B32B36@\"NSDictionary\"40@\"IDSMPPublicDeviceIdentityContainer\"48^@56^@64^@72"`
   - `@\"NSData\"80@0:8@\"NSData\"16@\"IDSCryptionContext\"24B32B36@\"NSDictionary\"40^@48@\"<IDSEncryptionSyncQueue>\"56^@64^@72"`
   - `@64@0:8@16@24@32@40@48Q56`
   - `@80@0:8@16@24B32B36@40@48^@56^@64^@72`
   - `@80@0:8@16@24B32B36@40^@48@56^@64^@72`
   - `@88@0:8@16@24B32B36@40@48^q56q64^@72^@80`
   - `"ActivityMonitorSubscription"`
   - `"Adding queued query fromURI: %@  service: %@   forRefresh: %@ preventNew: %@ first query: %@ identifier: %@ for URIs: %@"`
   - `"Apple ID account is not registered for service. Cannot perform self verification."`
   - `"B64@0:8@?16@24@32@40@48@56"`
   - `"B72@0:8@\"NSArray\"16@\"NSData\"24@\"IDSURI\"32@\"NSString\"40@\"IDSPeerIDQueryContext\"48@\"NSString\"56@?<v@?@\"IDSURI\"@\"NSArray\"@\"NSArray\"@\"NSDictionary\"@\"NSString\"B@\"NSDictionary\"B>64"`
   - `"B72@0:8@16@24@32@40@48@56@?64"`
   - `"B76@0:8@16@24@32@40B48B52B56@60@?68"`
   - `"Broadcasting did leave group session: %@"`
   - `"Checking disabled account {serviceIdentifier: %@, shouldRepair: %@, registrationError: %lld, shouldCheckKTStates: %@ }"`
   - `"Checking if we need to reregister to update KT data."`
   - `"Checking to see if we can repair the KT account."`
   - `"Checking to see if we've hit query cache threshold... {current threshold: %ld}"`
   - `"Created session (%@) %@ with %lu destinations %@"`
   - `"Currently unregistered due to KT server rejection. Updating error."`
   - `"Default is set to drop public key from KT account key response."`
   - `"Default is set to drop signature from KT account key response."`
   - `"Delaying notification of unregistered KT data {delay: %f seconds}"`
   - `"EndpointForURI"`
   - `"Enqueueing cleanup tasks if needed"`
   - `"Error fetching account status. Returning unknown. { error: %@ }"`
   - `"Fetched current KT CDP Status. { IDSKTAccountStatus: %@ }"`
   - `"FirewallPopulate"`
   - `"GDRQuery"`
   - `"IDSCryptionContext"`
   - `"IDSGroupEntitledAgent"`
   - `"IDSKTDropPublicKeyFromResponseDuringReg"`
   - `"IDSKTDropSignatureFromResponseDuringReg"`
   - `"IDSSessionEndedReasonNonUserParticipantRejected"`
   - `"Incoming message - processing metrics {ECSuccess: %@, legacySuccess: %@, secondarySuccess: %@, command: %@}"`
   - `"InfoQuery"`
   - `"Inputed account status not valid, doing nothing. { accountStatus: %@ }"`
   - `"KT says account isn't ready. Not trying to repair account."`
   - `"KTFetch"`
   - `"KTKickVerification"`
   - `"KTOptIn"`
   - `"MessageSend"`
   - `"Multi-Server Configuration"`
   - `"Music%@"`
   - `"No account found for %@"`
   - `"No accounts need updating."`
   - `"No registered account matching fromID: %@, bailing..."`
   - `"Not reregistering to update KT Data."`
   - `"Oct  6 2023"`
   - `"Posting notification of unregistered KT data"`
   - `"QRAlloc"`
   - `"QRserver type: %@"`
   - `"Query time was: %f  (identifier: %@) (URIs: %@) (service: %@) (fromURI: %@"`
   - `"QueryIdentifier"`
   - `"QueryReason"`
   - `"Received KTAccountStatus from transparency. { KTAccountStatus: %@, currentKTAccountStatus: %@ }"`
   - `"Received account status that we have no update for."`
   - `"Received account status update from KT. { KTAccountStatus: %@ }"`
   - `"Received notification of update to KT CDP status."`
   - `"Registering to update KT Data."`
   - `"Registration failed due to bad KT Account Key. Checking state to see if are ready to register."`
   - `"RemoteDevice"`
   - `"Reported to transparency of bad account key. { error: %@ }"`
   - `"Safari%@"`
   - `"Selected account {accountMatchingFromID: %@"`
   - `"SessionMemberLookup"`
   - `"Single-Server Configuration"`
   - `"Skipping notification of unregistered KT data; we've already done it"`
   - `"Starting ID query from URI: %@ Service: %@ identifier: %@ reason: %@ for IDs: %@"`
   - `"StatusLookup"`
   - `"StatusLookupPiggyback"`
   - `"T@\"IDSPushToken\",R,N,V_receivingPushToken"`
   - `"T@\"IDSURI\",R,N,V_receivingURI"`
   - `"T@\"NEPolicySession\",&,N,V_policySessionWithEntitlment"`
   - `"T@\"NSDictionary\",C,V_qrForceExperiment"`
   - `"T@\"NSMutableDictionary\",&,N,V_sessionIDToEvaluators"`
   - `"T@\"NSObject<OS_nw_agent>\",&,N,V_entitledAgent"`
   - `"TB,N,V_downgradeOnLock"`
   - `"Tq,N,V_mostRecentKTCDPAccountStatus"`
   - `"TransparencyAccountStatusChanged"`
   - `"Tried to add tinker disabled service, ignoring {service: %@"`
   - `"Tried to load a tinker disabled account -- dropping! { uniqueID: %@, service: %@, serviceType: %@, accountType: %d, accountInfo: %@ }"`
   - `"Tried to setup tinker disabled service directly, ignoring..."`
   - `"URIDecrypt"`
   - `"URIEncrypt"`
   - `"URIToQueryFrom:"`
   - `"URIVerify"`
   - `"URIWithUnprefixedURI:"`
   - `"We are at %ld entries -- no need to remove"`
   - `"We are over {current count: %ld} -- removing older entries"`
   - `"We are still over {current count: %ld} -- removing everything"`
   - `"We previously registered without a signature, but we have one now."`
   - `"We're at %@ queries for this hour for service: %@"`
   - `"We're at %@ queries for this hour for service: %@, can't do more"`
   - `"Will not send QR allocation request for session: %@"`
   - `"_IDSKTAccountStatusForKTAccountStatus:"`
   - `"_addCompletionBlock:forURIs:fromURI:fromService:context:queryIdentifier:"`
   - `"_asyncRemoveExcessiveQueryEntriesIfNeeded"`
   - `"_cleanupUntrackedValidators {self: %@, remainingUsers: %@, _stateMachineByUserIDKeys: %@, _registrations: %@"`
   - `"_configurePushHandler:"`
   -

## AI Prioritisation Scoring System

No actionable methods or prioritisation targets identified for this component.

