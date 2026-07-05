## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "%@ addedWalletKey: %@, passJSONDict: %@"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 0 (0 AI-authored, 0 auto-generated); comments: 0 (0 AI-authored, 0 auto-generated); across 0 function(s); verified persisted in .i64: 0 named variables, 0 comments.

## What this feature does

The `HomeKitDaemonLegacy` component has undergone significant changes between iOS 17.0.3 and 17.1, primarily focused on:

1. **Wallet Key Management Enhancements**: New flows for auto-adding wallet keys during device setup, handling NFC reader key updates, and managing home keys in the Wallet. This includes new methods like `autoAddWalletKeyWithFlow:`, `handleNFCReaderKeyUpdatedForWalletKey:`, and various wallet key update operations.

2. **Diagnostic Info Improvements**: The `HMDAppleMediaAccessoryDiagnosticInfoController` class has been enhanced with better diagnostic information handling, including support for HH2 (HomeKit Hub 2) mode detection and improved diagnostic data retrieval.

3. **Device Setup Configuration**: The `HMDDeviceSetupConfiguringController` has been significantly expanded with new methods for managing companion link clients, RP clients, and configuring device setup states.

4. **Home Wallet Key Management**: The `HMDHomeWalletKey` and `HMDHomeWalletKeyManager` classes have been substantially modified to support wallet key operations, including adding, removing, and updating wallet keys with NFC support.

5. **Widget and Action Set Management**: Enhanced handling of HomeKit widgets and action sets, with improved monitoring and execution capabilities.

6. **Security and Privacy Updates**: Removal of `HMDRadarInitiating` and related TTR (Time To Respond) management, along with updates to secure accessory access controls.

## How is it implemented

### Key New Classes and Methods

**HMDHomeWalletKey** (New Class):
```c
// Initialization with PKPass
void HMDHomeWalletKey::initWithPKPass(HMFFlow *flow)
{
    // Initialize wallet key from PKPass
    // Validate NFC info
    // Set up secure element information
}

// Check for missing NFC info
bool HMDHomeWalletKey::isMissingNFCInfo()
{
    // Verify secureElementIdentifier, applicationIdentifier, etc.
    // Return true if critical NFC info is missing
}
```

**HMDHomeWalletKeyManager** (Enhanced):
```c
// Add wallet key with various flows
void HMDHomeWalletKeyManager::addWalletKeyWithOptions(
    HMDHomeWalletKey *walletKey,
    NSDictionary *options,
    HMDHomeWalletKeyAssertion *assertion,
    HMFFlow *flow,
    void (^completion)(void))
{
    // Validate options and assertion
    // Create pass directory
    // Generate NFC info if needed
    // Add to wallet
    // Handle completion
}

// Auto-add wallet key flows
void HMDHomeWalletKeyManager::autoAddWalletKeyWithFlow(HMFFlow *flow)
{
    // Check if already added
    // Validate home and accessory
    // Execute auto-add flow
}

// Handle NFC reader key updates
void HMDHomeWalletKeyManager::handleNFCReaderKeyUpdatedForWalletKey(
    HMDHomeWalletKey *walletKey,
    HMFFlow *flow,
    void (^completion)(void))
{
    // Update wallet key with new NFC info
    // Handle conflicts
    // Complete operation
}
```

**HMDAppleMediaAccessoryDiagnosticInfoController** (Enhanced):
```c
// Initialize with HH2 mode support
HMDAppleMediaAccessoryDiagnosticInfoController *initWithDataSource(
    HMDAppleMediaAccessoryDiagnosticInfoControllerDataSource *dataSource,
    bool isHH2Mode)
{
    // Set up diagnostic info controller
    // Configure for HH2 mode if enabled
}

// Get diagnostic info description
NSString *HMDAppleMediaAccessoryDiagnosticInfoController::diagnosticInfoDescriptionWithData(
    NSData *data)
{
    // Parse diagnostic info data
    // Generate human-readable description
    // Return formatted string
}
```

**HMDDeviceSetupConfiguringController** (Enhanced):
```c
// Setup companion link client
void HMDDeviceSetupConfiguringController::setupCompanionLinkClient()
{
    // Create companion link client
    // Configure with control flags
    // Start client
}

// Setup RP client after timeout
void HMDDeviceSetupConfiguringController::setupRPClientAfter(
    dispatch_time_t timeout)
{
    // Wait for timeout
    // Setup RP client
    // Start client
}

// Query configuring state
void HMDDeviceSetupConfiguringController::queryConfiguringState(
    HMDAccessory *accessory,
    void (^completion)(ConfiguringState state))
{
    // Send query request
    // Handle response
    // Return state
}
```

### Implementation Details

The implementation follows a flow-based architecture where:

1. **Wallet Key Operations** are orchestrated through `HMFFlow` objects, allowing for flexible execution paths based on device state and user actions.

2. **NFC Support** is integrated through careful validation of NFC info components (secure element identifier, application identifier, etc.) before attempting wallet key operations.

3. **Diagnostic Information** is collected and formatted for better user experience, with special handling for HomeKit Hub 2 devices.

4. **Device Setup** is managed through a state machine approach with companion link and RP clients, ensuring proper coordination during accessory setup.

## How to trigger this feature

The feature is triggered through:

1. **Device Setup Process**: When a new HomeKit accessory is being set up, the system automatically checks for wallet key support and initiates the appropriate flow.

2. **NFC Reader Updates**: When the NFC reader key is updated on a home, the system detects this change and triggers wallet key update operations.

3. **Accessory State Changes**: When an accessory's wallet key support status changes, the system responds with appropriate wallet key management actions.

4. **Home Management Events**: When homes are added, removed, or updated, the system manages wallet keys associated with those homes.

## Vulnerability Assessment

**Security Improvements**:
- Enhanced NFC info validation prevents incomplete wallet key operations
- Better diagnostic information collection improves troubleshooting
- Improved home wallet key management reduces potential for key conflicts
- Removal of `HMDRadarInitiating` suggests privacy/security hardening

**Potential Vulnerability Mitigations**:
- The new wallet key management flows include proper validation of NFC info components
- Enhanced diagnostic info handling provides better visibility into accessory states
- Improved error handling and flow management reduces race conditions
- Better state management for home wallet keys prevents orphaned keys

**Risk Level**: Medium - The changes represent security and reliability improvements rather than new vulnerabilities. The removal of `HMDRadarInitiating` and related TTR management suggests the system is being hardened against timing-based attacks or information leakage.

## Evidence

### New Symbols (Added in 17.1):
- `HMDHomeWalletKey` - New class for managing home keys in wallet
- `HMDHomeWalletKeyManager` - Manager for wallet key operations
- `HMDHomeWalletKeyAccessoryManager` - Accessory-specific wallet key management
- `HMDHomeWalletKeySecureElementInfo` - Secure element info for wallet keys
- `HMDHomeKeyDataRecorder` - Recorder for home key data
- `HMDAppleMediaAccessoryDiagnosticInfoController` - Enhanced diagnostic info controller
- `HMDDeviceSetupConfiguringController` - Enhanced device setup controller
- Various new flows for wallet key operations

### New Strings (Added in 17.1):
- Wallet key management strings (auto-add, update, remove operations)
- NFC-related diagnostic messages
- Enhanced diagnostic info descriptions
- Home wallet key operation messages

### Removed Symbols:
- `HMDRadarInitiating` - Removed TTR management
- `HMDRadarInitiating` related variables
- `HMDHomeKitCoreServer` - Simplified HomeKit core server
- `HMDHomeKitCoreXPC*` - Removed XPC connections

### Removed Strings:
- Radar/TTR related messages
- HomeKit Core server messages
- PineBoard secure access messages

### Binary Changes:
- Significant expansion of HomeKit wallet key management code
- Enhanced diagnostic info handling
- Simplified HomeKit core server implementation
- Removal of radar/TTR infrastructure

## AI Prioritisation Scoring System

- **dyld_shared_cache_diff**
  - **Tier**: TIER_2
  - **Category**: HomeKit Wallet Key Management
  - **Reasoning**: Core business-logic update for HomeKit wallet key management with NFC support. Introduces new wallet key management flows, enhanced diagnostic info handling, and improved device setup configuration. These changes affect HomeKit accessory setup and wallet key operations, which are important for user experience and device functionality.

