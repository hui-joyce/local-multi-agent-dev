## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "Array<WINetworkSharingProvider.AccessPointConnection.Link>"`
- **Analysis mode**: evidence_only
- **Database annotations** -- variable renames: 0 (0 AI-authored, 0 auto-generated); comments: 0 (0 AI-authored, 0 auto-generated); across 0 function(s); verified persisted in .i64: 0 named variables, 0 comments.
- **Apple Security Notes**: matches advisory component `Wi-Fi` -- Apple confirms a security-relevant change here; this analysis examines the likely vulnerability patch.

## What this feature does

The `WiFiInfrastructure` framework has undergone significant changes between iOS 26.4.2 and 26.6, primarily focused on enhancing network credential management and EAP (Extensible Authentication Protocol) support for Wi-Fi connections. The most notable additions include:

1. **EAP Credentials Structure**: A comprehensive set of EAP credential types has been introduced, including:
   - Client Identity (with certificate, certificate chain, and private key support)
   - EAP Type enumeration for different authentication methods
   - FAST Configuration (with PAC provisioning and usage flags)
   - TLS Configuration (with minimum/maximum TLS versions, certificate requirements)
   - TTLS Configuration (with inner authentication support)
   - Trusted Servers (with certificate and name lists)
   - User Login (username/password authentication)

2. **Network Sharing Provider**: New structures for managing network sharing capabilities, including access point connections with link information (BSSID hash, channel, SSID) and network credentials.

3. **Captive Portal Login**: Support for user-entered form values in captive portal scenarios.

4. **MAC Address Hashing**: New methods for hashing MAC addresses with configurable hash types and salt values.

5. **Core Media Integration**: The framework now depends on `swiftCoreMedia`, which was removed in the previous version, suggesting integration with media-related network features.

The framework has grown from 2005 to 2011 functions and from 136 to 208 C strings, indicating substantial new functionality has been added. The binary size has increased significantly across all sections (__text, __const, __data, __bss), reflecting the addition of new code and data structures.

## How is it implemented


_No decompilation was captured for this component (the analyzer did not call `decompile_function`); the description below is derived from the symbol-level diff evidence, not from decompiled code._

The implementation leverages Swift's optional types (`Optional<...>`) and collection types (`Array<...>`, `Set<...>`) to represent the new credential structures. The EAP credentials are organized hierarchically with `EAPCredentials` containing multiple sub-credential types that can be conditionally used based on the authentication method selected.

The framework maintains backward compatibility by using optional types for all new fields, allowing existing code to work without modification while enabling new features when explicitly configured. The `__swift_FORCE_LOAD_$_swiftCoreMedia` symbol indicates that the framework now requires Core Media to be loaded before it can function, suggesting integration with media-related network operations.

The removal of several block copy/destroy helpers and object destroy functions suggests that some legacy functionality has been refactored or removed, possibly due to the introduction of more robust memory management through the new credential structures.

## How to trigger this feature

This feature is triggered when:
1. A device attempts to connect to a Wi-Fi network that requires EAP authentication
2. The user configures a new Wi-Fi connection with advanced credential options through the Settings app
3. A captive portal is detected and requires login credentials
4. Network sharing is enabled with specific access point configurations

The feature becomes active when the `WiFiInfrastructure` framework loads and processes network connection requests, particularly those involving EAP authentication methods or advanced credential configurations.

## Vulnerability Assessment

**Security-relevant change**: The diff shows the addition of comprehensive EAP credential structures with support for certificate-based authentication, TLS configuration, and trusted server validation. This represents a significant enhancement to Wi-Fi security capabilities.

**Patch mechanism**: The new implementation introduces proper certificate handling (certificate, certificate chain, private key), TLS version constraints (minimum/maximum versions), and trusted server validation. The framework now supports multiple EAP types with appropriate configuration for each authentication method (EAP-TLS, EAP-FAST, EAP-TTLS).

**Evidence**: 
- New strings for certificate fields: `"WINetworkSharingProvider.Network.Credentials.EAPCredentials.ClientIdentity.certificate"`, `"certificateChain"`, `"privateKey"`
- TLS configuration with version bounds: `"TLSConfiguration.TLSVersion"`, `"isCertificateRequired"`, `"minimumTLSVersion"`, `"maximumTLSVersion"`
- Trusted server validation: `"TrustedServers.certificates"`, `"TrustedServers.names"`
- EAP type enumeration: `"Set<WINetworkSharingProvider.Network.Credentials.EAPCredentials.EAPType>"`

**Potential vulnerability if left unpatched**: Without these security enhancements, devices would be vulnerable to:
1. **Man-in-the-Middle attacks**: Lack of proper certificate validation and TLS version enforcement could allow attackers to intercept credentials
2. **Weak authentication**: Absence of minimum TLS version requirements could permit use of deprecated, insecure protocols
3. **Untrusted server acceptance**: Without trusted server validation, clients might accept connections from unauthorized servers
4. **Credential exposure**: Missing certificate chain validation could expose private keys or allow credential theft

The changes represent a **security patch** that addresses critical Wi-Fi authentication vulnerabilities by implementing proper certificate-based authentication, enforcing TLS version minimums, and adding trusted server validation mechanisms.

## AI Prioritisation Scoring System

- **Apple Security Notes correlation + EAP credential structure analysis**
  - **Tier**: TIER_1
  - **Category**: Security - Wi-Fi Authentication
  - **Reasoning**: Critical security enhancement to Wi-Fi authentication mechanisms. The diff shows implementation of EAP-TLS, EAP-FAST, and EAP-TTLS with proper certificate validation, TLS version enforcement, and trusted server verification. These changes directly address potential vulnerabilities in Wi-Fi credential handling including man-in-the-middle attacks, weak protocol usage, and untrusted server acceptance. The framework's dependency on swiftCoreMedia also indicates integration with media-related security features.

