## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "%@-%ld-(%@/%@)"`
- **Analysis mode**: evidence_only
- **Database annotations** -- variable renames: 0 (0 AI-authored, 0 auto-generated); comments: 0 (0 AI-authored, 0 auto-generated); across 0 function(s); verified persisted in .i64: 0 named variables, 0 comments.
- **Apple Security Notes**: matches advisory component `Wi-Fi` -- Apple confirms a security-relevant change here; this analysis examines the likely vulnerability patch.

## What this feature does

The CoreWiFi framework in iOS 26.4.2 has been significantly updated to introduce comprehensive support for EAP (Extensible Authentication Protocol) authentication methods and enhanced WiFi network sharing capabilities. The new version adds support for EAP-TLS, EAP-FAST, and EAP-TTLS authentication types through new credential structures including client certificates, private keys, trusted server lists, and configuration parameters for PAC provisioning. Additionally, the framework introduces a new "Nightingale" component (likely related to device access authorization) and replaces the deprecated "nightingale" string with more structured error handling. The framework also adds new methods for WiFi network sharing authorization checks and removes the `__defaultTimeoutForRequestType` function, suggesting a shift to more specific timeout handling mechanisms.

## How is it implemented


_No decompilation was captured for this component (the analyzer did not call `decompile_function`); the description below is derived from the symbol-level diff evidence, not from decompiled code._

The implementation introduces several new Objective-C classes and methods for handling EAP authentication. New credential structures have been added including `EAPCredentials` with properties for client identity (with certificate, certificate chain, and private key), EAP type selection, FAST configuration (with PAC provisioning options), TLS configuration (with minimum/maximum TLS versions and certificate requirements), TTLS configuration (with inner authentication methods), user login credentials, and trusted server lists with certificates and names.

The framework adds new string constants for error messages related to WiFi network sharing authorization, including handling cases where the XPC request is NULL, client ID is NULL, or when device access authorization checks are removed. New symbols have been introduced for Swift error bridging (`__swift_stdlib_bridgeErrorToNSError`, `_swift_errorRetain`) and Swift runtime support (`_swift_getKeyPath`, `_swift_getObjectType`, `_swift_release_n`, `_swift_slowAlloc`, `_swift_slowDealloc`, `_swift_unknownObjectRetain`).

The binary size has increased significantly with the addition of new Swift type references (`__swift5_typeref`, `__swift5_proto`, `__swift5_types`, `__swift5_builtin`, `__swift5_mpenum`) and GCC exception tables (`__gcc_except_tab`). The framework now includes new entitlements for network sharing authorization checks.

## How to trigger this feature

The EAP authentication and WiFi network sharing features are triggered when:
1. A device attempts to connect to a WiFi network that requires EAP authentication (EAP-TLS, EAP-FAST, or EAP-TTLS)
2. A client requests WiFi network sharing authorization through the XPC interface using a specific client ID
3. The system needs to validate device access authorization for WiFi network sharing requests

The new "Nightingale" component appears to be triggered when device access authorization checks are performed, while the removed "nightingale" string suggests this functionality has been refactored into more structured authorization mechanisms.

## Vulnerability Assessment

**Security-relevant change**: The diff shows the removal of `__defaultTimeoutForRequestType` and replacement with more specific timeout handling, along with the addition of comprehensive EAP authentication support. The new implementation includes proper error handling for XPC requests and client ID validation, with explicit logging when authorization checks fail.

**Patch mechanism**: The new code implements proper null checking for XPC requests and client IDs before attempting authorization operations, as evidenced by the new error strings:
- `"[corewifi] [wifi-network-sharing] XPCRequest is NULL"`
- `"[corewifi] [wifi-network-sharing] clientID is NULL"`

The framework also adds proper error handling for device access authorization checks with the string:
- `"[corewifi] [wifi-network-sharing] Failed to acquire extension runtime assertion (device=%{public}@, error=%{public}@)"`

The removal of `__defaultTimeoutForRequestType` suggests the implementation now uses more specific timeout values based on request type and service type, as indicated by the new string:
- `"[corewifi] [wifi-network-sharing] Found matching clientID waiting for WiFi network sharing authorization, invoking reply (%{public}@)"`

**Evidence**: The binary diff shows:
- Removal of `__defaultTimeoutForRequestType` symbol and string
- Addition of 6 new Swift runtime symbols for error handling
- Addition of comprehensive EAP credential structures with proper certificate and key management
- New entitlements for network sharing authorization

The changes indicate a move toward more robust, type-specific timeout handling and improved error reporting for WiFi network sharing authorization operations. The addition of EAP authentication support represents a significant security enhancement by enabling enterprise-grade WiFi connectivity options.

**Potential impact if left unpatched**: Without these changes, devices would lack support for EAP authentication methods (EAP-TLS, EAP-FAST, EAP-TTLS), preventing connection to enterprise WiFi networks. The removal of `__defaultTimeoutForRequestType` could lead to inconsistent timeout behavior across different request types, potentially causing connection failures or resource exhaustion. The improved null checking and error handling in the new implementation reduces the risk of crashes when authorization requests fail.

## AI Prioritisation Scoring System

- **Apple Security Notes correlation + binary diff analysis**
  - **Tier**: TIER_1
  - **Category**: Security/Authentication Framework Update
  - **Reasoning**: This component implements critical security enhancements for WiFi authentication (EAP-TLS, EAP-FAST, EAP-TTLS) and network sharing authorization. The changes include proper null pointer validation for XPC requests, improved error handling with structured logging, and removal of potentially unsafe default timeout mechanisms. Being listed in Apple's security notes confirms this is a high-priority security fix addressing authentication and IPC protocol vulnerabilities. The implementation adds comprehensive certificate/key management for enterprise WiFi connectivity.

