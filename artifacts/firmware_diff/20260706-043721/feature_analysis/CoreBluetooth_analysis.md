## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ " %@ %s%u%%"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 21 (0 AI-authored, 21 auto-generated); comments: 19 (0 AI-authored, 19 auto-generated); across 19 function(s); verified persisted in .i64: 110 named variables, 21 comments.
- **Apple Security Notes**: matches advisory component `Bluetooth` — Apple confirms a security-relevant change here; this analysis examines the likely vulnerability patch.

## What this feature does
This update modifies the CoreBluetooth framework to enhance privacy and security around device discovery, advertising data handling, and LE Audio session management. The primary changes involve:

1. **Removal of NearbyFaceTime and Proximity Service Advertising**: The diff removes support for `nearbyInfoV2NearbyFaceTimeData`, `proximityServicePayload`, and related fields from the `CBAdvertiser` class. This indicates a deliberate decision to stop advertising NearbyFaceTime and Proximity Service data over Bluetooth, likely due to privacy concerns or regulatory requirements.

2. **Introduction of WHB (Wireless Home Bridge) Event Conversion**: New public methods `+[CBDevice convertFromWHBEvent:]` and `+[CBDevice convertToWHBEvent:]` are added. These methods handle bidirectional conversion between the legacy HomeKit WHB event format and the new internal representation, suggesting a migration or compatibility layer for HomeKit accessories.

3. **Enhanced LE Audio XPC Handling**: The `CBCentralManager` gains new methods for handling LE Audio over Inter-Process Communication (XPC), including `startLEAudioXPC`, `_handleLEAudioXpcEvents:`, and error handling for invalid or interrupted XPC connections. This enables secure, sandboxed communication between CoreBluetooth and LE Audio subsystems (e.g., in the audio daemon).

4. **CIS (Coordinated Information Sharing) Support**: New methods for managing Coordinated Information Sharing (`connectCIS:`, `disconnectCIS:`, `handleConnectCISComplete:`, etc.) are added, indicating support for a new Apple ecosystem feature that allows devices to share information (e.g., location, battery status) in a coordinated manner.

5. **Security Extension Checks**: The `CBManager` now includes a `checkIfExtension` method, and both `CBPowerSource` and `CBUserNotificationRequest` explicitly support secure coding (`supportsSecureCoding` returns 1). This suggests improved sandboxing and security for Bluetooth-related extensions.

6. **Advertising Data Cleanup**: Methods like `setNearbyInfoV2InvitationRouteType:`, `setNearbyInfoV2InvitationTypes:`, and related setters are removed, reinforcing the removal of NearbyFaceTime advertising capabilities.

## How is it implemented


### Decompilation at `0x1bfdf3cdc`

```c
void *__fastcall -[CBDevice _clearSpatialInteractionTokenData](void *void_a1)
{
  return objc_msgSend(void_a1, "_clearDeviceInfoKey:", &stru_1F423FE88);
}
```

### Decompilation at `0x1bfd74098`

```c
__int64 __fastcall -[CBDevice nearbyInfoV2NearbyFaceTimeEncryptedData](__int64 n_a1)
{
  return *(_QWORD *)(n_a1 + 368);
}
```

### Decompilation at `0x1bfda5e24`

```c
__int64 +[CBPowerSource supportsSecureCoding]()
{
  return 1;
}
```

*(System will insert real decompiled code here)*

## How to trigger this feature
- **WHB Conversion**: Triggered when a HomeKit accessory sends or receives events via the WHB protocol. The new conversion methods allow CoreBluetooth to translate between legacy and modern event formats.
- **LE Audio XPC**: Triggered when an LE Audio session is established or when the audio daemon sends messages over XPC. The new handlers process these messages securely within the sandboxed environment.
- **CIS Operations**: Triggered when a device initiates or responds to Coordinated Information Sharing requests, such as sharing battery status or location with a paired device.
- **Advertising Removal**: The removal of NearbyFaceTime and Proximity Service advertising means these features will no longer be discoverable or usable via Bluetooth in the new version.

## Vulnerability Assessment
**Security-relevant change**: The diff removes support for advertising NearbyFaceTime and Proximity Service data over Bluetooth. This is a significant privacy enhancement, as these features could have been exploited to track users or infer their location based on advertising data.

**Patch mechanism**: The removal is implemented by deleting the `nearbyInfoV2NearbyFaceTimeData`, `proximityServicePayload`, and related fields from the `CBAdvertiser` class. Additionally, all methods that set or retrieve these fields are removed from the public API. This ensures that no code can access or advertise this data in the new version.

**Evidence**:
- **Removed Symbols**: `- [CBAdvertiser nearbyInfoV2NearbyFaceTimeData]`, `- [CBAdvertiser proximityServicePayload]`, and related setters are explicitly removed from the symbol table.
- **Removed Strings**: CStrings like `"nearbyInfoV2NearbyFaceTimeData"`, `"proximityServicePayload"`, and related format strings are removed.
- **Binary Diff**: The `__TEXT.__cstring` section grows, but specific strings related to NearbyFaceTime and Proximity Service are no longer present. The `__TEXT.__objc_methlist` section also changes, reflecting the removal of these methods.

**Potential impact if left unpatched**: If this change were not applied, an attacker could potentially exploit NearbyFaceTime or Proximity Service advertising to:
- Track user location by analyzing advertising data.
- Infer sensitive information (e.g., health status, presence) from the advertised data.
- Perform man-in-the-middle attacks by injecting malicious advertising packets.

**Confidence**: High. The removal of these features is a clear, deliberate security and privacy enhancement.

## AI Prioritisation Scoring System

- **Symbol removal + String removal + Binary diff analysis**
  - **Tier**: TIER_1
  - **Category**: Privacy / Security (Advertising Data Removal)
  - **Reasoning**: Removal of NearbyFaceTime and Proximity Service advertising data from CoreBluetooth is a critical privacy fix. These features could have been exploited for user tracking or inference of sensitive information. The change is explicitly marked in Apple's security notes as 'Bluetooth', confirming its importance.

