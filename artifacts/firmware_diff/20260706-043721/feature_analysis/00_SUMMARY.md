# Feature Analysis Summary — iOS 26.0

- **Total components in diff**: 5647  (**HIGH_SIGNAL**: 4594, **LOW_SIGNAL**: 1053)
- **Analysed** (report written): 100  |  **Apple Security Notes matches**: 186  |  **Suppressed TIER_3**: 0  |  **HIGH_SIGNAL not analysed** (budget/security filter): 4494

Tier shown is the LLM-assigned tier for analysed components, otherwise a deterministic estimate from the security score (4=Apple Security Notes, 3=hard indicator, 2=security vocabulary, 1=code change, 0=asset/UI/log).

## 🔴 Apple Security Notes matches — highest priority

<details><summary>Show 186 components</summary>

| Component | Tier | Sec score | Apple Security Notes | Report |
|---|---|---|---|---|
| AAGKAuthenticationPlugin | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| AAIDMSAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| AAIDSAuthenticationPlugin | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| ACDatabaseBackupNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| AKAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | [report](AKAccountNotificationPlugin_analysis.md) |
| AMSAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | [report](AMSAccountNotificationPlugin_analysis.md) |
| AMSAccountSyncNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| AMSUIAuthenticationViewService | TIER_1 | 4 | `Authentication Services` | [report](AMSUIAuthenticationViewService_analysis.md) |
| ASDAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | [report](ASDAccountNotificationPlugin_analysis.md) |
| AppleAccountAuthenticationDelegate | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| AppleIDAuthentication | TIER_1 | 4 | `Authentication Services` | [report](AppleIDAuthentication_analysis.md) |
| AppleIDSSOAuthentication | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| AppleIDSSOAuthenticationPlugin | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| AppleIDSSONotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| AppleMIDIBluetoothDriver | TIER_1 | 4 | `Bluetooth` | [report](AppleMIDIBluetoothDriver_analysis.md) |
| AppleMobileFileIntegrity | TIER_1 | 4 | `AppleMobileFileIntegrity` | [report](AppleMobileFileIntegrity_analysis.md) |
| AppleNeuralEngine | TIER_1 | 4 | `Apple Neural Engine` | [report](AppleNeuralEngine_analysis.md) |
| Audio-QuickLook | TIER_1 | 4 | `QuickLook` | _not analysed_ |
| AuthenticationServices | TIER_1 | 4 | `Authentication Services` | [report](AuthenticationServices_analysis.md) |
| AuthenticationServicesAgent | TIER_1 | 4 | `Authentication Services` | [report](AuthenticationServicesAgent_analysis.md) |
| AuthenticationServicesCore | TIER_1 | 4 | `Authentication Services` | [report](AuthenticationServicesCore_analysis.md) |
| AuthenticationServicesUI | TIER_1 | 4 | `Authentication Services` | [report](AuthenticationServicesUI_analysis.md) |
| BTCloudPairingAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| BackgroundShortcutRunner | TIER_1 | 4 | `Shortcuts` | [report](BackgroundShortcutRunner_analysis.md) |
| BluetoothFirmware | TIER_1 | 4 | `Bluetooth` | _not analysed_ |
| BluetoothManager | TIER_1 | 4 | `Bluetooth` | _not analysed_ |
| BluetoothServicesUI | TIER_1 | 4 | `Bluetooth` | _not analysed_ |
| BluetoothUIService | TIER_1 | 4 | `Bluetooth` | [report](BluetoothUIService_analysis.md) |
| CDPAccountNotificationPlugin_IOS | TIER_1 | 4 | `Notifications` | _not analysed_ |
| CalendarNotification | TIER_1 | 4 | `Notifications` | [report](CalendarNotification_analysis.md) |
| CallHistoryDataMigrator | TIER_1 | 4 | `Call History` | _not analysed_ |
| CallHistorySyncHelper | TIER_1 | 4 | `Call History` | [report](CallHistorySyncHelper_analysis.md) |
| ClassKitAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| ClassKitNotificationUI | TIER_1 | 4 | `Notifications` | _not analysed_ |
| CloudKit | TIER_1 | 4 | `CloudKit` | [report](CloudKit_analysis.md) |
| CloudKitAuthenticationPlugin | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| CloudKitNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| CompanionNotificationSettings | TIER_1 | 4 | `Notifications` | [report](CompanionNotificationSettings_analysis.md) |
| CoreAudio | TIER_1 | 4 | `CoreAudio` | [report](CoreAudio_analysis.md) |
| CoreBluetooth | TIER_1 | 4 | `Bluetooth` | [report](CoreBluetooth_analysis.md) |
| CoreBluetoothUI | TIER_1 | 4 | `Bluetooth` | [report](CoreBluetoothUI_analysis.md) |
| CoreIDVAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| CoreLocationAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| CoreRecentsAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| CoreRoutineAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| DMDAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| DefaultMediaPlayer-QuickLook | TIER_1 | 4 | `QuickLook` | _not analysed_ |
| ExposureNotification | TIER_1 | 4 | `Notifications` | _not analysed_ |
| ExposureNotificationDaemon | TIER_1 | 4 | `Notifications` | _not analysed_ |
| ExposureNotificationRemoteViewService | TIER_1 | 4 | `Notifications` | _not analysed_ |
| ExposureNotificationSettingsUI | TIER_1 | 4 | `Notifications` | _not analysed_ |
| FMFLocatorAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| FaceTimeNotificationCore | TIER_1 | 4 | `Notifications` | _not analysed_ |
| FaceTimeNotificationUI | TIER_1 | 4 | `Notifications` | _not analysed_ |
| FamilyNotification | TIER_1 | 4 | `Notifications` | [report](FamilyNotification_analysis.md) |
| FindMyDeviceAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| FindMyDeviceUserNotificationsXPCService | TIER_1 | 4 | `Notifications` | _not analysed_ |
| FindMyNotificationsSettings | TIER_1 | 4 | `Notifications` | [report](FindMyNotificationsSettings_analysis.md) |
| GameCenterAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| Gif-QuickLook | TIER_1 | 4 | `QuickLook` | _not analysed_ |
| GoogleAuthenticationPlugin | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| HSAAuthentication | TIER_1 | 4 | `Authentication Services` | [report](HSAAuthentication_analysis.md) |
| HealthKitAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| HomeKitAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| IAPAuthentication | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| IDSAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| IMAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| INDAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| Image-QuickLook | TIER_1 | 4 | `QuickLook` | _not analysed_ |
| ImageIO | TIER_1 | 4 | `ImageIO` | [report](ImageIO_analysis.md) |
| KerberosAuthenticationPlugin | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| KeychainSyncAccountNotification | TIER_1 | 4 | `Notifications` | _not analysed_ |
| LocalAuthentication | TIER_1 | 4 | `Authentication Services` | [report](LocalAuthentication_analysis.md) |
| LocalAuthenticationCredentialServices | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| LocalAuthenticationEmbeddedUI | TIER_1 | 4 | `Authentication Services` | [report](LocalAuthenticationEmbeddedUI_analysis.md) |
| LocalAuthenticationRGBCapture | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| LocalAuthenticationUI | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| LockdownModeAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | [report](LockdownModeAccountNotificationPlugin_analysis.md) |
| MBPrebuddyAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| MFAAuthentication | TIER_1 | 4 | `Authentication Services` | [report](MFAAuthentication_analysis.md) |
| MessageAccountAuthenticationPlugin | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| MessageAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| MessagesNotificationFiltering | TIER_1 | 4 | `Notifications` | _not analysed_ |
| MobileStorageMounter | TIER_1 | 4 | `MobileStorageMounter` | [report](MobileStorageMounter_analysis.md) |
| MobileSyncAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| Movie-QuickLook | TIER_1 | 4 | `QuickLook` | _not analysed_ |
| NewsNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| NotificationCenter | TIER_1 | 4 | `Notifications` | _not analysed_ |
| NotificationsFlowDelegatePlugin | TIER_1 | 4 | `Notifications` | [report](NotificationsFlowDelegatePlugin_analysis.md) |
| PCSAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | [report](PCSAccountNotificationPlugin_analysis.md) |
| PassbookAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| PhotosAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| Platform-Bluetooth | TIER_1 | 4 | `Bluetooth` | _not analysed_ |
| QuickLook | TIER_1 | 4 | `QuickLook` | [report](QuickLook_analysis.md) |
| QuickLookThumbnailGeneration | TIER_1 | 4 | `QuickLook` | _not analysed_ |
| QuickLookThumbnailing | TIER_1 | 4 | `QuickLook` | [report](QuickLookThumbnailing_analysis.md) |
| QuickLookThumbnailingDaemon | TIER_1 | 4 | `QuickLook` | [report](QuickLookThumbnailingDaemon_analysis.md) |
| RPAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| RemindersAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| Safari | TIER_1 | 4 | `Safari` | [report](Safari_analysis.md) |
| SearchPartyAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| SecureBackupNotification | TIER_1 | 4 | `Notifications` | _not analysed_ |
| SharingAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| ShortcutUIKit | TIER_1 | 4 | `Shortcuts` | _not analysed_ |
| Shortcuts | TIER_1 | 4 | `Shortcuts` | [report](Shortcuts_analysis.md) |
| ShortcutsCloudKitAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| ShortcutsUI | TIER_1 | 4 | `Shortcuts` | [report](ShortcutsUI_analysis.md) |
| SignpostNotification | TIER_1 | 4 | `Notifications` | _not analysed_ |
| SocialAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| SpokenNotificationsModule | TIER_1 | 4 | `Notifications` | _not analysed_ |
| System | TIER_1 | 4 | `System` | _not analysed_ |
| ThreatNotification | TIER_1 | 4 | `Notifications` | _not analysed_ |
| ThreatNotificationCore | TIER_1 | 4 | `Notifications` | _not analysed_ |
| ThreatNotificationUI | TIER_1 | 4 | `Notifications` | _not analysed_ |
| TipsNotificationExtension | TIER_1 | 4 | `Notifications` | _not analysed_ |
| UserNotifications | TIER_1 | 4 | `Notifications` | [report](UserNotifications_analysis.md) |
| UserNotificationsCore | TIER_1 | 4 | `Notifications` | [report](UserNotificationsCore_analysis.md) |
| UserNotificationsKit | TIER_1 | 4 | `Notifications` | [report](UserNotificationsKit_analysis.md) |
| UserNotificationsSettings | TIER_1 | 4 | `Notifications` | [report](UserNotificationsSettings_analysis.md) |
| UserNotificationsUI | TIER_1 | 4 | `Notifications` | _not analysed_ |
| VoiceShortcutClient | TIER_1 | 4 | `Shortcuts` | [report](VoiceShortcutClient_analysis.md) |
| VoiceShortcutsUI | TIER_1 | 4 | `Shortcuts` | _not analysed_ |
| VoiceShortcutsUICardKitProviderSupport | TIER_1 | 4 | `Shortcuts` | _not analysed_ |
| WebBookmarksNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| WebKit | TIER_1 | 4 | `WebKit` | _not analysed_ |
| YahooAuthenticationPlugin | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| com.apple.Siri.ActionPredictionNotifications | TIER_1 | 4 | `Notifications` | _not analysed_ |
| com.apple.askpermission.AccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| com.apple.driver.AppleMobileFileIntegrity | TIER_1 | 4 | `AppleMobileFileIntegrity` | [report](com.apple.driver.AppleMobileFileIntegrity_analysis.md) |
| com.apple.security.sandbox | TIER_1 | 4 | `Sandbox` | [report](com.apple.security.sandbox_analysis.md) |
| iCloudNotification | TIER_1 | 4 | `Notifications` | [report](iCloudNotification_analysis.md) |
| libAWDProtobufBluetooth.dylib | TIER_1 | 4 | `Bluetooth` | [report](libAWDProtobufBluetooth.dylib_analysis.md) |
| liblog_IOHIDFamily.dylib | TIER_1 | 4 | `IOHIDFamily` | _not analysed_ |
| AAAccountNotificationPlugin | TIER_2 | 4 | `Notifications` | [report](AAAccountNotificationPlugin_analysis.md) |
| ADAccountsNotificationPlugin | TIER_2 | 4 | `Notifications` | [report](ADAccountsNotificationPlugin_analysis.md) |
| AISAccountNotificationPlugin | TIER_2 | 4 | `Notifications` | [report](AISAccountNotificationPlugin_analysis.md) |
| AMSAccountAuthenticationPlugin | TIER_2 | 4 | `Authentication Services` | [report](AMSAccountAuthenticationPlugin_analysis.md) |
| AccountNotificationPlugin | TIER_2 | 4 | `Notifications` | [report](AccountNotificationPlugin_analysis.md) |
| AccountSuggestionNotificationPlugin | TIER_2 | 4 | `Notifications` | [report](AccountSuggestionNotificationPlugin_analysis.md) |
| AdaptiveVoiceShortcuts | TIER_2 | 4 | `Shortcuts` | [report](AdaptiveVoiceShortcuts_analysis.md) |
| BluetoothAudio | TIER_2 | 4 | `Bluetooth` | [report](BluetoothAudio_analysis.md) |
| BluetoothServices | TIER_2 | 4 | `Bluetooth` | [report](BluetoothServices_analysis.md) |
| BluetoothSettings | TIER_2 | 4 | `Bluetooth` | [report](BluetoothSettings_analysis.md) |
| CallHistory | TIER_2 | 4 | `Call History` | [report](CallHistory_analysis.md) |
| CloudDocsAccountNotificationPlugin | TIER_2 | 4 | `Notifications` | [report](CloudDocsAccountNotificationPlugin_analysis.md) |
| CoreMedia | TIER_2 | 4 | `CoreMedia` | [report](CoreMedia_analysis.md) |
| FamilyControlsAuthenticationUI | TIER_2 | 4 | `Authentication Services` | [report](FamilyControlsAuthenticationUI_analysis.md) |
| FindMyBluetooth | TIER_2 | 4 | `Bluetooth` | [report](FindMyBluetooth_analysis.md) |
| GameCenterAccountAuthenticationPlugin | TIER_2 | 4 | `Authentication Services` | [report](GameCenterAccountAuthenticationPlugin_analysis.md) |
| HAENotifications | TIER_2 | 4 | `Notifications` | [report](HAENotifications_analysis.md) |
| HealthBluetoothPeripheral | TIER_2 | 4 | `Bluetooth` | [report](HealthBluetoothPeripheral_analysis.md) |
| IOKit | TIER_2 | 4 | `IOKit` | [report](IOKit_analysis.md) |
| LocalAuthenticationCore | TIER_2 | 4 | `Authentication Services` | [report](LocalAuthenticationCore_analysis.md) |
| LocalAuthenticationCoreUI | TIER_2 | 4 | `Authentication Services` | [report](LocalAuthenticationCoreUI_analysis.md) |
| LocalAuthenticationPreboard | TIER_2 | 4 | `Authentication Services` | [report](LocalAuthenticationPreboard_analysis.md) |
| LocalAuthenticationPrivateUI | TIER_2 | 4 | `Authentication Services` | [report](LocalAuthenticationPrivateUI_analysis.md) |
| MetricKit | TIER_2 | 4 | `MetricKit` | [report](MetricKit_analysis.md) |
| MobileBluetooth | TIER_2 | 4 | `Bluetooth` | [report](MobileBluetooth_analysis.md) |
| NotesAccountNotificationPlugin | TIER_2 | 4 | `Notifications` | [report](NotesAccountNotificationPlugin_analysis.md) |
| NotificationsSettings | TIER_2 | 4 | `Notifications` | [report](NotificationsSettings_analysis.md) |
| PoirotSQLite | TIER_2 | 4 | `SQLite` | [report](PoirotSQLite_analysis.md) |
| QuickLookSupport | TIER_2 | 4 | `QuickLook` | [report](QuickLookSupport_analysis.md) |
| QuickLookUICore | TIER_2 | 4 | `QuickLook` | [report](QuickLookUICore_analysis.md) |
| SessionPushNotifications | TIER_2 | 4 | `Notifications` | [report](SessionPushNotifications_analysis.md) |
| ShortcutsActions | TIER_2 | 4 | `Shortcuts` | [report](ShortcutsActions_analysis.md) |
| ShortcutsSettings | TIER_2 | 4 | `Shortcuts` | [report](ShortcutsSettings_analysis.md) |
| ShortcutsViewService | TIER_2 | 4 | `Shortcuts` | [report](ShortcutsViewService_analysis.md) |
| Siri | TIER_2 | 4 | `Siri` | [report](Siri_analysis.md) |
| SiriNotificationsIntents | TIER_2 | 4 | `Notifications` | [report](SiriNotificationsIntents_analysis.md) |
| TVAppServicesAccountNotificationPlugin | TIER_2 | 4 | `Notifications` | [report](TVAppServicesAccountNotificationPlugin_analysis.md) |
| TetsuoNotifications | TIER_2 | 4 | `Notifications` | [report](TetsuoNotifications_analysis.md) |
| UserNotificationsServer | TIER_2 | 4 | `Notifications` | [report](UserNotificationsServer_analysis.md) |
| UserNotificationsServices | TIER_2 | 4 | `Notifications` | [report](UserNotificationsServices_analysis.md) |
| UserNotificationsUIKit | TIER_2 | 4 | `Notifications` | [report](UserNotificationsUIKit_analysis.md) |
| VoiceShortcuts | TIER_2 | 4 | `Shortcuts` | [report](VoiceShortcuts_analysis.md) |
| _AuthenticationServices_SwiftUI | TIER_2 | 4 | `Authentication Services` | [report](AuthenticationServices_SwiftUI_analysis.md) |
| _QuickLook_SwiftUI | TIER_2 | 4 | `QuickLook` | [report](QuickLook_SwiftUI_analysis.md) |
| com.apple.iokit.IOHIDFamily | TIER_2 | 4 | `IOHIDFamily` | [report](com.apple.iokit.IOHIDFamily_analysis.md) |
| com.apple.kernel | TIER_2 | 4 | `Kernel` | [report](com.apple.kernel_analysis.md) |
| libsystem_sandbox.dylib | TIER_2 | 4 | `Sandbox` | [report](libsystem_sandbox.dylib_analysis.md) |
| AADataclassEnableNotificationPlugin | TIER_3 | 4 | `Notifications` | [report](AADataclassEnableNotificationPlugin_analysis.md) |
| AppNotificationsLoggingClient | TIER_3 | 4 | `Notifications` | [report](AppNotificationsLoggingClient_analysis.md) |
| HealthExposureNotificationUI | TIER_3 | 4 | `Notifications` | [report](HealthExposureNotificationUI_analysis.md) |
| Notes | TIER_3 | 4 | `Notes` | [report](Notes_analysis.md) |
| SwiftSQLite | TIER_3 | 4 | `SQLite` | [report](SwiftSQLite_analysis.md) |
| UserNotificationsTranslation | TIER_3 | 4 | `Notifications` | [report](UserNotificationsTranslation_analysis.md) |

</details>

## Analysed components (reports written)

<details><summary>Show 100 components</summary>

| Component | Tier | Sec score | Apple Security Notes | Report |
|---|---|---|---|---|
| AKAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | [report](AKAccountNotificationPlugin_analysis.md) |
| AMSAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | [report](AMSAccountNotificationPlugin_analysis.md) |
| AMSUIAuthenticationViewService | TIER_1 | 4 | `Authentication Services` | [report](AMSUIAuthenticationViewService_analysis.md) |
| ASDAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | [report](ASDAccountNotificationPlugin_analysis.md) |
| AppleIDAuthentication | TIER_1 | 4 | `Authentication Services` | [report](AppleIDAuthentication_analysis.md) |
| AppleMIDIBluetoothDriver | TIER_1 | 4 | `Bluetooth` | [report](AppleMIDIBluetoothDriver_analysis.md) |
| AppleMobileFileIntegrity | TIER_1 | 4 | `AppleMobileFileIntegrity` | [report](AppleMobileFileIntegrity_analysis.md) |
| AppleNeuralEngine | TIER_1 | 4 | `Apple Neural Engine` | [report](AppleNeuralEngine_analysis.md) |
| AuthenticationServices | TIER_1 | 4 | `Authentication Services` | [report](AuthenticationServices_analysis.md) |
| AuthenticationServicesAgent | TIER_1 | 4 | `Authentication Services` | [report](AuthenticationServicesAgent_analysis.md) |
| AuthenticationServicesCore | TIER_1 | 4 | `Authentication Services` | [report](AuthenticationServicesCore_analysis.md) |
| AuthenticationServicesUI | TIER_1 | 4 | `Authentication Services` | [report](AuthenticationServicesUI_analysis.md) |
| BackgroundShortcutRunner | TIER_1 | 4 | `Shortcuts` | [report](BackgroundShortcutRunner_analysis.md) |
| BluetoothUIService | TIER_1 | 4 | `Bluetooth` | [report](BluetoothUIService_analysis.md) |
| CalendarNotification | TIER_1 | 4 | `Notifications` | [report](CalendarNotification_analysis.md) |
| CallHistorySyncHelper | TIER_1 | 4 | `Call History` | [report](CallHistorySyncHelper_analysis.md) |
| CloudKit | TIER_1 | 4 | `CloudKit` | [report](CloudKit_analysis.md) |
| CompanionNotificationSettings | TIER_1 | 4 | `Notifications` | [report](CompanionNotificationSettings_analysis.md) |
| CoreAudio | TIER_1 | 4 | `CoreAudio` | [report](CoreAudio_analysis.md) |
| CoreBluetooth | TIER_1 | 4 | `Bluetooth` | [report](CoreBluetooth_analysis.md) |
| CoreBluetoothUI | TIER_1 | 4 | `Bluetooth` | [report](CoreBluetoothUI_analysis.md) |
| FamilyNotification | TIER_1 | 4 | `Notifications` | [report](FamilyNotification_analysis.md) |
| FindMyNotificationsSettings | TIER_1 | 4 | `Notifications` | [report](FindMyNotificationsSettings_analysis.md) |
| HSAAuthentication | TIER_1 | 4 | `Authentication Services` | [report](HSAAuthentication_analysis.md) |
| ImageIO | TIER_1 | 4 | `ImageIO` | [report](ImageIO_analysis.md) |
| LocalAuthentication | TIER_1 | 4 | `Authentication Services` | [report](LocalAuthentication_analysis.md) |
| LocalAuthenticationEmbeddedUI | TIER_1 | 4 | `Authentication Services` | [report](LocalAuthenticationEmbeddedUI_analysis.md) |
| LockdownModeAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | [report](LockdownModeAccountNotificationPlugin_analysis.md) |
| MFAAuthentication | TIER_1 | 4 | `Authentication Services` | [report](MFAAuthentication_analysis.md) |
| MobileStorageMounter | TIER_1 | 4 | `MobileStorageMounter` | [report](MobileStorageMounter_analysis.md) |
| NotificationsFlowDelegatePlugin | TIER_1 | 4 | `Notifications` | [report](NotificationsFlowDelegatePlugin_analysis.md) |
| PCSAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | [report](PCSAccountNotificationPlugin_analysis.md) |
| QuickLook | TIER_1 | 4 | `QuickLook` | [report](QuickLook_analysis.md) |
| QuickLookThumbnailing | TIER_1 | 4 | `QuickLook` | [report](QuickLookThumbnailing_analysis.md) |
| QuickLookThumbnailingDaemon | TIER_1 | 4 | `QuickLook` | [report](QuickLookThumbnailingDaemon_analysis.md) |
| Safari | TIER_1 | 4 | `Safari` | [report](Safari_analysis.md) |
| Shortcuts | TIER_1 | 4 | `Shortcuts` | [report](Shortcuts_analysis.md) |
| ShortcutsUI | TIER_1 | 4 | `Shortcuts` | [report](ShortcutsUI_analysis.md) |
| UserNotifications | TIER_1 | 4 | `Notifications` | [report](UserNotifications_analysis.md) |
| UserNotificationsCore | TIER_1 | 4 | `Notifications` | [report](UserNotificationsCore_analysis.md) |
| UserNotificationsKit | TIER_1 | 4 | `Notifications` | [report](UserNotificationsKit_analysis.md) |
| UserNotificationsSettings | TIER_1 | 4 | `Notifications` | [report](UserNotificationsSettings_analysis.md) |
| VoiceShortcutClient | TIER_1 | 4 | `Shortcuts` | [report](VoiceShortcutClient_analysis.md) |
| com.apple.driver.AppleMobileFileIntegrity | TIER_1 | 4 | `AppleMobileFileIntegrity` | [report](com.apple.driver.AppleMobileFileIntegrity_analysis.md) |
| com.apple.security.sandbox | TIER_1 | 4 | `Sandbox` | [report](com.apple.security.sandbox_analysis.md) |
| iCloudNotification | TIER_1 | 4 | `Notifications` | [report](iCloudNotification_analysis.md) |
| libAWDProtobufBluetooth.dylib | TIER_1 | 4 | `Bluetooth` | [report](libAWDProtobufBluetooth.dylib_analysis.md) |
| AAAccountNotificationPlugin | TIER_2 | 4 | `Notifications` | [report](AAAccountNotificationPlugin_analysis.md) |
| ADAccountsNotificationPlugin | TIER_2 | 4 | `Notifications` | [report](ADAccountsNotificationPlugin_analysis.md) |
| AISAccountNotificationPlugin | TIER_2 | 4 | `Notifications` | [report](AISAccountNotificationPlugin_analysis.md) |
| AMSAccountAuthenticationPlugin | TIER_2 | 4 | `Authentication Services` | [report](AMSAccountAuthenticationPlugin_analysis.md) |
| AccountNotificationPlugin | TIER_2 | 4 | `Notifications` | [report](AccountNotificationPlugin_analysis.md) |
| AccountSuggestionNotificationPlugin | TIER_2 | 4 | `Notifications` | [report](AccountSuggestionNotificationPlugin_analysis.md) |
| AdaptiveVoiceShortcuts | TIER_2 | 4 | `Shortcuts` | [report](AdaptiveVoiceShortcuts_analysis.md) |
| BluetoothAudio | TIER_2 | 4 | `Bluetooth` | [report](BluetoothAudio_analysis.md) |
| BluetoothServices | TIER_2 | 4 | `Bluetooth` | [report](BluetoothServices_analysis.md) |
| BluetoothSettings | TIER_2 | 4 | `Bluetooth` | [report](BluetoothSettings_analysis.md) |
| CallHistory | TIER_2 | 4 | `Call History` | [report](CallHistory_analysis.md) |
| CloudDocsAccountNotificationPlugin | TIER_2 | 4 | `Notifications` | [report](CloudDocsAccountNotificationPlugin_analysis.md) |
| CoreMedia | TIER_2 | 4 | `CoreMedia` | [report](CoreMedia_analysis.md) |
| FamilyControlsAuthenticationUI | TIER_2 | 4 | `Authentication Services` | [report](FamilyControlsAuthenticationUI_analysis.md) |
| FindMyBluetooth | TIER_2 | 4 | `Bluetooth` | [report](FindMyBluetooth_analysis.md) |
| GameCenterAccountAuthenticationPlugin | TIER_2 | 4 | `Authentication Services` | [report](GameCenterAccountAuthenticationPlugin_analysis.md) |
| HAENotifications | TIER_2 | 4 | `Notifications` | [report](HAENotifications_analysis.md) |
| HealthBluetoothPeripheral | TIER_2 | 4 | `Bluetooth` | [report](HealthBluetoothPeripheral_analysis.md) |
| IOKit | TIER_2 | 4 | `IOKit` | [report](IOKit_analysis.md) |
| LocalAuthenticationCore | TIER_2 | 4 | `Authentication Services` | [report](LocalAuthenticationCore_analysis.md) |
| LocalAuthenticationCoreUI | TIER_2 | 4 | `Authentication Services` | [report](LocalAuthenticationCoreUI_analysis.md) |
| LocalAuthenticationPreboard | TIER_2 | 4 | `Authentication Services` | [report](LocalAuthenticationPreboard_analysis.md) |
| LocalAuthenticationPrivateUI | TIER_2 | 4 | `Authentication Services` | [report](LocalAuthenticationPrivateUI_analysis.md) |
| MetricKit | TIER_2 | 4 | `MetricKit` | [report](MetricKit_analysis.md) |
| MobileBluetooth | TIER_2 | 4 | `Bluetooth` | [report](MobileBluetooth_analysis.md) |
| NotesAccountNotificationPlugin | TIER_2 | 4 | `Notifications` | [report](NotesAccountNotificationPlugin_analysis.md) |
| NotificationsSettings | TIER_2 | 4 | `Notifications` | [report](NotificationsSettings_analysis.md) |
| PoirotSQLite | TIER_2 | 4 | `SQLite` | [report](PoirotSQLite_analysis.md) |
| QuickLookSupport | TIER_2 | 4 | `QuickLook` | [report](QuickLookSupport_analysis.md) |
| QuickLookUICore | TIER_2 | 4 | `QuickLook` | [report](QuickLookUICore_analysis.md) |
| SessionPushNotifications | TIER_2 | 4 | `Notifications` | [report](SessionPushNotifications_analysis.md) |
| ShortcutsActions | TIER_2 | 4 | `Shortcuts` | [report](ShortcutsActions_analysis.md) |
| ShortcutsSettings | TIER_2 | 4 | `Shortcuts` | [report](ShortcutsSettings_analysis.md) |
| ShortcutsViewService | TIER_2 | 4 | `Shortcuts` | [report](ShortcutsViewService_analysis.md) |
| Siri | TIER_2 | 4 | `Siri` | [report](Siri_analysis.md) |
| SiriNotificationsIntents | TIER_2 | 4 | `Notifications` | [report](SiriNotificationsIntents_analysis.md) |
| TVAppServicesAccountNotificationPlugin | TIER_2 | 4 | `Notifications` | [report](TVAppServicesAccountNotificationPlugin_analysis.md) |
| TetsuoNotifications | TIER_2 | 4 | `Notifications` | [report](TetsuoNotifications_analysis.md) |
| UserNotificationsServer | TIER_2 | 4 | `Notifications` | [report](UserNotificationsServer_analysis.md) |
| UserNotificationsServices | TIER_2 | 4 | `Notifications` | [report](UserNotificationsServices_analysis.md) |
| UserNotificationsUIKit | TIER_2 | 4 | `Notifications` | [report](UserNotificationsUIKit_analysis.md) |
| VoiceShortcuts | TIER_2 | 4 | `Shortcuts` | [report](VoiceShortcuts_analysis.md) |
| _AuthenticationServices_SwiftUI | TIER_2 | 4 | `Authentication Services` | [report](AuthenticationServices_SwiftUI_analysis.md) |
| _QuickLook_SwiftUI | TIER_2 | 4 | `QuickLook` | [report](QuickLook_SwiftUI_analysis.md) |
| com.apple.iokit.IOHIDFamily | TIER_2 | 4 | `IOHIDFamily` | [report](com.apple.iokit.IOHIDFamily_analysis.md) |
| com.apple.kernel | TIER_2 | 4 | `Kernel` | [report](com.apple.kernel_analysis.md) |
| libsystem_sandbox.dylib | TIER_2 | 4 | `Sandbox` | [report](libsystem_sandbox.dylib_analysis.md) |
| AADataclassEnableNotificationPlugin | TIER_3 | 4 | `Notifications` | [report](AADataclassEnableNotificationPlugin_analysis.md) |
| AppNotificationsLoggingClient | TIER_3 | 4 | `Notifications` | [report](AppNotificationsLoggingClient_analysis.md) |
| HealthExposureNotificationUI | TIER_3 | 4 | `Notifications` | [report](HealthExposureNotificationUI_analysis.md) |
| Notes | TIER_3 | 4 | `Notes` | [report](Notes_analysis.md) |
| SwiftSQLite | TIER_3 | 4 | `SQLite` | [report](SwiftSQLite_analysis.md) |
| UserNotificationsTranslation | TIER_3 | 4 | `Notifications` | [report](UserNotificationsTranslation_analysis.md) |

</details>

## HIGH_SIGNAL — flagged security-relevant but not analysed (2444, over budget)

<details><summary>Show 2444 components</summary>

| Component | Tier | Sec score | Apple Security Notes | Report |
|---|---|---|---|---|
| AAGKAuthenticationPlugin | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| AAIDMSAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| AAIDSAuthenticationPlugin | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| ACDatabaseBackupNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| AMSAccountSyncNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| AppleAccountAuthenticationDelegate | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| AppleIDSSOAuthentication | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| AppleIDSSOAuthenticationPlugin | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| AppleIDSSONotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| Audio-QuickLook | TIER_1 | 4 | `QuickLook` | _not analysed_ |
| BTCloudPairingAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| BluetoothFirmware | TIER_1 | 4 | `Bluetooth` | _not analysed_ |
| BluetoothManager | TIER_1 | 4 | `Bluetooth` | _not analysed_ |
| BluetoothServicesUI | TIER_1 | 4 | `Bluetooth` | _not analysed_ |
| CDPAccountNotificationPlugin_IOS | TIER_1 | 4 | `Notifications` | _not analysed_ |
| CallHistoryDataMigrator | TIER_1 | 4 | `Call History` | _not analysed_ |
| ClassKitAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| ClassKitNotificationUI | TIER_1 | 4 | `Notifications` | _not analysed_ |
| CloudKitAuthenticationPlugin | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| CloudKitNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| CoreIDVAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| CoreLocationAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| CoreRecentsAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| CoreRoutineAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| DMDAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| DefaultMediaPlayer-QuickLook | TIER_1 | 4 | `QuickLook` | _not analysed_ |
| ExposureNotification | TIER_1 | 4 | `Notifications` | _not analysed_ |
| ExposureNotificationDaemon | TIER_1 | 4 | `Notifications` | _not analysed_ |
| ExposureNotificationRemoteViewService | TIER_1 | 4 | `Notifications` | _not analysed_ |
| ExposureNotificationSettingsUI | TIER_1 | 4 | `Notifications` | _not analysed_ |
| FMFLocatorAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| FaceTimeNotificationCore | TIER_1 | 4 | `Notifications` | _not analysed_ |
| FaceTimeNotificationUI | TIER_1 | 4 | `Notifications` | _not analysed_ |
| FindMyDeviceAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| FindMyDeviceUserNotificationsXPCService | TIER_1 | 4 | `Notifications` | _not analysed_ |
| GameCenterAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| Gif-QuickLook | TIER_1 | 4 | `QuickLook` | _not analysed_ |
| GoogleAuthenticationPlugin | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| HealthKitAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| HomeKitAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| IAPAuthentication | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| IDSAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| IMAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| INDAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| Image-QuickLook | TIER_1 | 4 | `QuickLook` | _not analysed_ |
| KerberosAuthenticationPlugin | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| KeychainSyncAccountNotification | TIER_1 | 4 | `Notifications` | _not analysed_ |
| LocalAuthenticationCredentialServices | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| LocalAuthenticationRGBCapture | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| LocalAuthenticationUI | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| MBPrebuddyAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| MessageAccountAuthenticationPlugin | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| MessageAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| MessagesNotificationFiltering | TIER_1 | 4 | `Notifications` | _not analysed_ |
| MobileSyncAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| Movie-QuickLook | TIER_1 | 4 | `QuickLook` | _not analysed_ |
| NewsNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| NotificationCenter | TIER_1 | 4 | `Notifications` | _not analysed_ |
| PassbookAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| PhotosAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| Platform-Bluetooth | TIER_1 | 4 | `Bluetooth` | _not analysed_ |
| QuickLookThumbnailGeneration | TIER_1 | 4 | `QuickLook` | _not analysed_ |
| RPAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| RemindersAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| SearchPartyAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| SecureBackupNotification | TIER_1 | 4 | `Notifications` | _not analysed_ |
| SharingAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| ShortcutUIKit | TIER_1 | 4 | `Shortcuts` | _not analysed_ |
| ShortcutsCloudKitAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| SignpostNotification | TIER_1 | 4 | `Notifications` | _not analysed_ |
| SocialAccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| SpokenNotificationsModule | TIER_1 | 4 | `Notifications` | _not analysed_ |
| System | TIER_1 | 4 | `System` | _not analysed_ |
| ThreatNotification | TIER_1 | 4 | `Notifications` | _not analysed_ |
| ThreatNotificationCore | TIER_1 | 4 | `Notifications` | _not analysed_ |
| ThreatNotificationUI | TIER_1 | 4 | `Notifications` | _not analysed_ |
| TipsNotificationExtension | TIER_1 | 4 | `Notifications` | _not analysed_ |
| UserNotificationsUI | TIER_1 | 4 | `Notifications` | _not analysed_ |
| VoiceShortcutsUI | TIER_1 | 4 | `Shortcuts` | _not analysed_ |
| VoiceShortcutsUICardKitProviderSupport | TIER_1 | 4 | `Shortcuts` | _not analysed_ |
| WebBookmarksNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| WebKit | TIER_1 | 4 | `WebKit` | _not analysed_ |
| YahooAuthenticationPlugin | TIER_1 | 4 | `Authentication Services` | _not analysed_ |
| com.apple.Siri.ActionPredictionNotifications | TIER_1 | 4 | `Notifications` | _not analysed_ |
| com.apple.askpermission.AccountNotificationPlugin | TIER_1 | 4 | `Notifications` | _not analysed_ |
| liblog_IOHIDFamily.dylib | TIER_1 | 4 | `IOHIDFamily` | _not analysed_ |
| ACTFramework | TIER_1 | 3 | — | _not analysed_ |
| ANECompiler | TIER_1 | 3 | — | _not analysed_ |
| ARKitDaemon | TIER_1 | 3 | — | _not analysed_ |
| AVConference | TIER_1 | 3 | — | _not analysed_ |
| AVD.videodecoder | TIER_1 | 3 | — | _not analysed_ |
| AccessibilitySharedSupport | TIER_1 | 3 | — | _not analysed_ |
| Accessory Updater Service | TIER_1 | 3 | — | _not analysed_ |
| Anvil | TIER_1 | 3 | — | _not analysed_ |
| AppleAVE2FW_H17.im4p | TIER_1 | 3 | — | _not analysed_ |
| AppleAccountUI | TIER_1 | 3 | — | _not analysed_ |
| AppleCV3D | TIER_1 | 3 | — | _not analysed_ |
| AppleMCTF | TIER_1 | 3 | — | _not analysed_ |
| AppleMediaServices | TIER_1 | 3 | — | _not analysed_ |
| AppleMediaServicesUI | TIER_1 | 3 | — | _not analysed_ |
| AppleVideoEncoder | TIER_1 | 3 | — | _not analysed_ |
| AskTo | TIER_1 | 3 | — | _not analysed_ |
| AskToCore | TIER_1 | 3 | — | _not analysed_ |
| AskToDaemon | TIER_1 | 3 | — | _not analysed_ |
| AudioToolbox | TIER_1 | 3 | — | _not analysed_ |
| BaseBoard | TIER_1 | 3 | — | _not analysed_ |
| BiomeLibrary | TIER_1 | 3 | — | _not analysed_ |
| BiometricKit | TIER_1 | 3 | — | _not analysed_ |
| BiometricSupport | TIER_1 | 3 | — | _not analysed_ |
| BlockMonitoring | TIER_1 | 3 | — | _not analysed_ |
| BookStoreUI | TIER_1 | 3 | — | _not analysed_ |
| CDMFoundation | TIER_1 | 3 | — | _not analysed_ |
| CameraColorProcessing | TIER_1 | 3 | — | _not analysed_ |
| CameraUI | TIER_1 | 3 | — | _not analysed_ |
| ChatKit | TIER_1 | 3 | — | _not analysed_ |
| ChronoCore | TIER_1 | 3 | — | _not analysed_ |
| ChronoServices | TIER_1 | 3 | — | _not analysed_ |
| CloudKitDaemon | TIER_1 | 3 | — | _not analysed_ |
| CloudTelemetryService | TIER_1 | 3 | — | _not analysed_ |
| CommCenter | TIER_1 | 3 | — | _not analysed_ |
| ContactsUI | TIER_1 | 3 | — | _not analysed_ |
| ContactsUICore | TIER_1 | 3 | — | _not analysed_ |
| ContainerManagerCommon | TIER_1 | 3 | — | _not analysed_ |
| CoreBrightness | TIER_1 | 3 | — | _not analysed_ |
| CoreCDPInternal | TIER_1 | 3 | — | _not analysed_ |
| CoreData | TIER_1 | 3 | — | _not analysed_ |
| CoreDiagnostics | TIER_1 | 3 | — | _not analysed_ |
| CoreEmbeddedSpeechRecognition | TIER_1 | 3 | — | _not analysed_ |
| CoreHandwriting | TIER_1 | 3 | — | _not analysed_ |
| CoreIDVShared | TIER_1 | 3 | — | _not analysed_ |
| CoreImage | TIER_1 | 3 | — | _not analysed_ |
| CoreML | TIER_1 | 3 | — | _not analysed_ |
| CorePhotogrammetry | TIER_1 | 3 | — | _not analysed_ |
| CoreRE | TIER_1 | 3 | — | _not analysed_ |
| CoreRepairCore | TIER_1 | 3 | — | _not analysed_ |
| CoreSDB | TIER_1 | 3 | — | _not analysed_ |
| CoreServices | TIER_1 | 3 | — | _not analysed_ |
| CoreSpeech | TIER_1 | 3 | — | _not analysed_ |
| CoreSpotlight | TIER_1 | 3 | — | _not analysed_ |
| CoreUARP | TIER_1 | 3 | — | _not analysed_ |
| CoreUI | TIER_1 | 3 | — | _not analysed_ |
| CoreWiFi | TIER_1 | 3 | — | _not analysed_ |
| CryptexServer | TIER_1 | 3 | — | _not analysed_ |
| DeviceSharing | TIER_1 | 3 | — | _not analysed_ |
| DifferentialPrivacy | TIER_1 | 3 | — | _not analysed_ |
| DirectResource | TIER_1 | 3 | — | _not analysed_ |
| DoNotDisturbServer | TIER_1 | 3 | — | _not analysed_ |
| DumpPanic | TIER_1 | 3 | — | _not analysed_ |
| EmbeddedAcousticRecognition | TIER_1 | 3 | — | _not analysed_ |
| ExtensionFoundation | TIER_1 | 3 | — | _not analysed_ |
| FaceTimeMessageStore | TIER_1 | 3 | — | _not analysed_ |
| FamilyCircle | TIER_1 | 3 | — | _not analysed_ |
| FileProviderDaemon | TIER_1 | 3 | — | _not analysed_ |
| FinHealthCore | TIER_1 | 3 | — | _not analysed_ |
| FinHealthXPCServices | TIER_1 | 3 | — | _not analysed_ |
| FitnessProductDetail | TIER_1 | 3 | — | _not analysed_ |
| FontSettings | TIER_1 | 3 | — | _not analysed_ |
| Foundation | TIER_1 | 3 | — | _not analysed_ |
| Freeform | TIER_1 | 3 | — | _not analysed_ |
| GESS | TIER_1 | 3 | — | _not analysed_ |
| GameCenterFoundation | TIER_1 | 3 | — | _not analysed_ |
| GameController | TIER_1 | 3 | — | _not analysed_ |
| GenerativeAssistantSettings | TIER_1 | 3 | — | _not analysed_ |
| GenerativeModelsFoundation | TIER_1 | 3 | — | _not analysed_ |
| GeoServices | TIER_1 | 3 | — | _not analysed_ |
| GraphComputeRT | TIER_1 | 3 | — | _not analysed_ |
| H264H9.videoencoder | TIER_1 | 3 | — | _not analysed_ |
| H9.videoencoder | TIER_1 | 3 | — | _not analysed_ |
| HDRProcessing | TIER_1 | 3 | — | _not analysed_ |
| HeadphoneSettingsUI | TIER_1 | 3 | — | _not analysed_ |
| HealthAppHealthDaemon | TIER_1 | 3 | — | _not analysed_ |
| HealthAppHealthDaemonSupport | TIER_1 | 3 | — | _not analysed_ |
| HealthDaemon | TIER_1 | 3 | — | _not analysed_ |
| HealthKit | TIER_1 | 3 | — | _not analysed_ |
| HearingTest | TIER_1 | 3 | — | _not analysed_ |
| HomeEnergyDaemon | TIER_1 | 3 | — | _not analysed_ |
| HomeKit | TIER_1 | 3 | — | _not analysed_ |
| HomeKitDaemon | TIER_1 | 3 | — | _not analysed_ |
| HomeKitDaemonLegacy | TIER_1 | 3 | — | _not analysed_ |
| IAP | TIER_1 | 3 | — | _not analysed_ |
| IDSFoundation | TIER_1 | 3 | — | _not analysed_ |
| IMAP | TIER_1 | 3 | — | _not analysed_ |
| IMDPersistence | TIER_1 | 3 | — | _not analysed_ |
| IMDaemonCore | TIER_1 | 3 | — | _not analysed_ |
| IMFoundation | TIER_1 | 3 | — | _not analysed_ |
| IOGPU | TIER_1 | 3 | — | _not analysed_ |
| IconFoundation | TIER_1 | 3 | — | _not analysed_ |
| ImageCaptureCore | TIER_1 | 3 | — | _not analysed_ |
| ImagePlaygroundInternal | TIER_1 | 3 | — | _not analysed_ |
| InstallCoordination | TIER_1 | 3 | — | _not analysed_ |
| InstalledContentLibrary | TIER_1 | 3 | — | _not analysed_ |
| IntelligencePlatformLibrary | TIER_1 | 3 | — | _not analysed_ |
| JITAppKit | TIER_1 | 3 | — | _not analysed_ |
| JavaScriptCore | TIER_1 | 3 | — | _not analysed_ |
| KeychainCircle | TIER_1 | 3 | — | _not analysed_ |
| LighthouseBackground | TIER_1 | 3 | — | _not analysed_ |
| LinkServices | TIER_1 | 3 | — | _not analysed_ |
| MLIR_ML | TIER_1 | 3 | — | _not analysed_ |
| MacinTalk | TIER_1 | 3 | — | _not analysed_ |
| MailUI | TIER_1 | 3 | — | _not analysed_ |
| Maps | TIER_1 | 3 | — | _not analysed_ |
| MapsOfflineService | TIER_1 | 3 | — | _not analysed_ |
| Measure | TIER_1 | 3 | — | _not analysed_ |
| MediaAnalysis | TIER_1 | 3 | — | _not analysed_ |
| MediaExperience | TIER_1 | 3 | — | _not analysed_ |
| MediaML | TIER_1 | 3 | — | _not analysed_ |
| MediaPlayer | TIER_1 | 3 | — | _not analysed_ |
| MediaRemote | TIER_1 | 3 | — | _not analysed_ |
| Mercury | TIER_1 | 3 | — | _not analysed_ |
| Message | TIER_1 | 3 | — | _not analysed_ |
| MetalPerformanceShadersGraph | TIER_1 | 3 | — | _not analysed_ |
| MetalTools | TIER_1 | 3 | — | _not analysed_ |
| MetricsFramework | TIER_1 | 3 | — | _not analysed_ |
| MicroLocationDaemon | TIER_1 | 3 | — | _not analysed_ |
| MigrationKit | TIER_1 | 3 | — | _not analysed_ |
| MobileMail | TIER_1 | 3 | — | _not analysed_ |
| MobileMailUI | TIER_1 | 3 | — | _not analysed_ |
| MobileSpotlightIndex | TIER_1 | 3 | — | _not analysed_ |
| ModelCatalog | TIER_1 | 3 | — | _not analysed_ |
| ModelCatalogRuntime | TIER_1 | 3 | — | _not analysed_ |
| ModuleACM | TIER_1 | 3 | — | _not analysed_ |
| MusicKitInternal | TIER_1 | 3 | — | _not analysed_ |
| NanoMailBridgeSettings | TIER_1 | 3 | — | _not analysed_ |
| Network | TIER_1 | 3 | — | _not analysed_ |
| NetworkExtension | TIER_1 | 3 | — | _not analysed_ |
| NetworkInfo | TIER_1 | 3 | — | _not analysed_ |
| NeutrinoCore | TIER_1 | 3 | — | _not analysed_ |
| NeutrinoKit | TIER_1 | 3 | — | _not analysed_ |
| NightingaleTraining | TIER_1 | 3 | — | _not analysed_ |
| OSAnalyticsPrivate | TIER_1 | 3 | — | _not analysed_ |
| OnDeviceStorageCore | TIER_1 | 3 | — | _not analysed_ |
| PDFKit | TIER_1 | 3 | — | _not analysed_ |
| PHASE | TIER_1 | 3 | — | _not analysed_ |
| PaperBoardUI | TIER_1 | 3 | — | _not analysed_ |
| PassKitUI | TIER_1 | 3 | — | _not analysed_ |
| PerfPowerMetricMonitor | TIER_1 | 3 | — | _not analysed_ |
| PersistentConnection | TIER_1 | 3 | — | _not analysed_ |
| PhoneCallFlowDelegatePlugin | TIER_1 | 3 | — | _not analysed_ |
| PhotoAnalysis | TIER_1 | 3 | — | _not analysed_ |
| PhotoLibraryServices | TIER_1 | 3 | — | _not analysed_ |
| PhotoLibraryServicesCore | TIER_1 | 3 | — | _not analysed_ |
| PhotosGraph | TIER_1 | 3 | — | _not analysed_ |
| PhotosUICore | TIER_1 | 3 | — | _not analysed_ |
| PhotosUIFoundation | TIER_1 | 3 | — | _not analysed_ |
| PlatformSSO | TIER_1 | 3 | — | _not analysed_ |
| PosterBoardServices | TIER_1 | 3 | — | _not analysed_ |
| PosterFoundation | TIER_1 | 3 | — | _not analysed_ |
| PosterUIFoundation | TIER_1 | 3 | — | _not analysed_ |
| ProtectedCloudKeySyncing | TIER_1 | 3 | — | _not analysed_ |
| QuartzCore | TIER_1 | 3 | — | _not analysed_ |
| RESync | TIER_1 | 3 | — | _not analysed_ |
| RealityFoundation | TIER_1 | 3 | — | _not analysed_ |
| Reminders | TIER_1 | 3 | — | _not analysed_ |
| ReplicatorCore | TIER_1 | 3 | — | _not analysed_ |
| ReplicatorServices | TIER_1 | 3 | — | _not analysed_ |
| ReportCrash | TIER_1 | 3 | — | _not analysed_ |
| RunningBoard | TIER_1 | 3 | — | _not analysed_ |
| SCSharingReminders | TIER_1 | 3 | — | _not analysed_ |
| SIMSetupSupport | TIER_1 | 3 | — | _not analysed_ |
| STExtractionService | TIER_1 | 3 | — | _not analysed_ |
| Scandium | TIER_1 | 3 | — | _not analysed_ |
| SecurityFoundation | TIER_1 | 3 | — | _not analysed_ |
| SensitiveContentAnalysis | TIER_1 | 3 | — | _not analysed_ |
| Setup | TIER_1 | 3 | — | _not analysed_ |
| SeymourServices | TIER_1 | 3 | — | _not analysed_ |
| Sharing | TIER_1 | 3 | — | _not analysed_ |
| SharingUI | TIER_1 | 3 | — | _not analysed_ |
| SiriCam | TIER_1 | 3 | — | _not analysed_ |
| SiriPaymentsIntents | TIER_1 | 3 | — | _not analysed_ |
| SiriSettingsIntents | TIER_1 | 3 | — | _not analysed_ |
| SiriSharedUI | TIER_1 | 3 | — | _not analysed_ |
| SiriSocialConversationSuggestionsPlugin | TIER_1 | 3 | — | _not analysed_ |
| SiriTTSService | TIER_1 | 3 | — | _not analysed_ |
| SiriTTSTrainingAgent | TIER_1 | 3 | — | _not analysed_ |
| SiriWellnessIntents | TIER_1 | 3 | — | _not analysed_ |
| SocialConversationFlowDelegatePlugin | TIER_1 | 3 | — | _not analysed_ |
| SoftwareUpdateCore | TIER_1 | 3 | — | _not analysed_ |
| Speech | TIER_1 | 3 | — | _not analysed_ |
| SpotlightUIShared | TIER_1 | 3 | — | _not analysed_ |
| SpringBoard | TIER_1 | 3 | — | _not analysed_ |
| SpringBoardHome | TIER_1 | 3 | — | _not analysed_ |
| StickerKit | TIER_1 | 3 | — | _not analysed_ |
| StorageKit | TIER_1 | 3 | — | _not analysed_ |
| StorageSettingsUI | TIER_1 | 3 | — | _not analysed_ |
| SwiftUI | TIER_1 | 3 | — | _not analysed_ |
| SwiftUICore | TIER_1 | 3 | — | _not analysed_ |
| Symbolication | TIER_1 | 3 | — | _not analysed_ |
| SyncedDefaults | TIER_1 | 3 | — | _not analysed_ |
| SyncedDefaultsDaemon | TIER_1 | 3 | — | _not analysed_ |
| TDGSharing | TIER_1 | 3 | — | _not analysed_ |
| TSTables | TIER_1 | 3 | — | _not analysed_ |
| TVAppServices | TIER_1 | 3 | — | _not analysed_ |
| TextComposer | TIER_1 | 3 | — | _not analysed_ |
| TextToSpeech | TIER_1 | 3 | — | _not analysed_ |
| TextToSpeechBundleSupport | TIER_1 | 3 | — | _not analysed_ |
| TipKit | TIER_1 | 3 | — | _not analysed_ |
| TipKitCore | TIER_1 | 3 | — | _not analysed_ |
| TokenGenerationInference | TIER_1 | 3 | — | _not analysed_ |
| TranslationDaemon | TIER_1 | 3 | — | _not analysed_ |
| TrustKit | TIER_1 | 3 | — | _not analysed_ |
| Tungsten | TIER_1 | 3 | — | _not analysed_ |
| UARPUpdaterServiceDFU | TIER_1 | 3 | — | _not analysed_ |
| UARPUpdaterServiceHID | TIER_1 | 3 | — | _not analysed_ |
| UARPUpdaterServiceUSBPD | TIER_1 | 3 | — | _not analysed_ |
| UARPiCloud | TIER_1 | 3 | — | _not analysed_ |
| UIKit | TIER_1 | 3 | — | _not analysed_ |
| UIKitCore | TIER_1 | 3 | — | _not analysed_ |
| UnifiedAssetFramework | TIER_1 | 3 | — | _not analysed_ |
| VFX | TIER_1 | 3 | — | _not analysed_ |
| VectorKit | TIER_1 | 3 | — | _not analysed_ |
| VirtualAudio | TIER_1 | 3 | — | _not analysed_ |
| Vision | TIER_1 | 3 | — | _not analysed_ |
| VoiceProcessor | TIER_1 | 3 | — | _not analysed_ |
| WeatherCore | TIER_1 | 3 | — | _not analysed_ |
| WeatherMaps | TIER_1 | 3 | — | _not analysed_ |
| WidgetKit | TIER_1 | 3 | — | _not analysed_ |
| WorkoutCore | TIER_1 | 3 | — | _not analysed_ |
| _StoreKit_SwiftUI | TIER_1 | 3 | — | _not analysed_ |
| accessoryupdaterd | TIER_1 | 3 | — | _not analysed_ |
| adc-rheia-d9x.im4p | TIER_1 | 3 | — | _not analysed_ |
| amsondevicestoraged | TIER_1 | 3 | — | _not analysed_ |
| ansf.t8140.release.im4p | TIER_1 | 3 | — | _not analysed_ |
| aonsensed | TIER_1 | 3 | — | _not analysed_ |
| apfs_checkseal | TIER_1 | 3 | — | _not analysed_ |
| apfs_condenser | TIER_1 | 3 | — | _not analysed_ |
| apfs_stats | TIER_1 | 3 | — | _not analysed_ |
| apfs_vol_converter | TIER_1 | 3 | — | _not analysed_ |
| applekeystored | TIER_1 | 3 | — | _not analysed_ |
| appstorecomponentsd | TIER_1 | 3 | — | _not analysed_ |
| apsd | TIER_1 | 3 | — | _not analysed_ |
| backupd | TIER_1 | 3 | — | _not analysed_ |
| batteryintelligenced | TIER_1 | 3 | — | _not analysed_ |
| bluetoothd | TIER_1 | 3 | — | _not analysed_ |
| com.apple.AGXG17P | TIER_1 | 3 | — | _not analysed_ |
| com.apple.DriverKit-AppleBCMWLAN | TIER_1 | 3 | — | _not analysed_ |
| com.apple.MobileInstallationHelperService | TIER_1 | 3 | — | _not analysed_ |
| com.apple.StreamingUnzipService | TIER_1 | 3 | — | _not analysed_ |
| com.apple.driver.AppleAVD | TIER_1 | 3 | — | _not analysed_ |
| com.apple.driver.AppleAVE2 | TIER_1 | 3 | — | _not analysed_ |
| com.apple.driver.AppleConvergedIPCOLYBTControl | TIER_1 | 3 | — | _not analysed_ |
| com.apple.driver.AppleConvergedPCI | TIER_1 | 3 | — | _not analysed_ |
| com.apple.driver.AppleEventLogHandler | TIER_1 | 3 | — | _not analysed_ |
| com.apple.driver.AppleH16ANEInterface | TIER_1 | 3 | — | _not analysed_ |
| com.apple.driver.AppleH16CameraInterface | TIER_1 | 3 | — | _not analysed_ |
| com.apple.driver.AppleM2ScalerCSCDriver | TIER_1 | 3 | — | _not analysed_ |
| com.apple.driver.AppleOLYHAL | TIER_1 | 3 | — | _not analysed_ |
| com.apple.driver.AppleSEPKeyStore | TIER_1 | 3 | — | _not analysed_ |
| com.apple.driver.AppleT8140PCIe | TIER_1 | 3 | — | _not analysed_ |
| com.apple.filesystems.apfs | TIER_1 | 3 | — | _not analysed_ |
| com.apple.iokit.IONVMeFamily | TIER_1 | 3 | — | _not analysed_ |
| com.apple.iokit.IOPCIFamily | TIER_1 | 3 | — | _not analysed_ |
| com.apple.iokit.IOSCSIBlockCommandsDevice | TIER_1 | 3 | — | _not analysed_ |
| com.apple.iokit.IOSurface | TIER_1 | 3 | — | _not analysed_ |
| com.apple.networkextension | TIER_1 | 3 | — | _not analysed_ |
| com.apple.plugin.IOgPTPPlugin | TIER_1 | 3 | — | _not analysed_ |
| com.apple.sbd | TIER_1 | 3 | — | _not analysed_ |
| com.apple.security.AppleImage4 | TIER_1 | 3 | — | _not analysed_ |
| coreidvd | TIER_1 | 3 | — | _not analysed_ |
| corespeechd | TIER_1 | 3 | — | _not analysed_ |
| cryptexd | TIER_1 | 3 | — | _not analysed_ |
| debugserver | TIER_1 | 3 | — | _not analysed_ |
| deleted_helper | TIER_1 | 3 | — | _not analysed_ |
| demod | TIER_1 | 3 | — | _not analysed_ |
| diskimagescontroller | TIER_1 | 3 | — | _not analysed_ |
| driverkitd | TIER_1 | 3 | — | _not analysed_ |
| dyld | TIER_1 | 3 | — | _not analysed_ |
| exclave_ExclaveStackshotServer | TIER_1 | 3 | — | _not analysed_ |
| exclave_pmm_exclave | TIER_1 | 3 | — | _not analysed_ |
| exclave_roottask | TIER_1 | 3 | — | _not analysed_ |
| exclave_sharedcache | TIER_1 | 3 | — | _not analysed_ |
| familycircled | TIER_1 | 3 | — | _not analysed_ |
| financed | TIER_1 | 3 | — | _not analysed_ |
| findmylocated | TIER_1 | 3 | — | _not analysed_ |
| fsck_apfs | TIER_1 | 3 | — | _not analysed_ |
| fsck_hfs | TIER_1 | 3 | — | _not analysed_ |
| gpsd | TIER_1 | 3 | — | _not analysed_ |
| h17_ane_fw_theia_d9x.im4p | TIER_1 | 3 | — | _not analysed_ |
| iCloudDriveCore | TIER_1 | 3 | — | _not analysed_ |
| icprefd-xpc | TIER_1 | 3 | — | _not analysed_ |
| identityservicesd | TIER_1 | 3 | — | _not analysed_ |
| installcoordination_proxy | TIER_1 | 3 | — | _not analysed_ |
| installcoordinationd | TIER_1 | 3 | — | _not analysed_ |
| keybagd | TIER_1 | 3 | — | _not analysed_ |
| launchd | TIER_1 | 3 | — | _not analysed_ |
| libARI.dylib | TIER_1 | 3 | — | _not analysed_ |
| libAce3Updater.dylib | TIER_1 | 3 | — | _not analysed_ |
| libAppPatch.dylib | TIER_1 | 3 | — | _not analysed_ |
| libAudioDSP.dylib | TIER_1 | 3 | — | _not analysed_ |
| libBBUpdaterDynamic.dylib | TIER_1 | 3 | — | _not analysed_ |
| libBNNS.dylib | TIER_1 | 3 | — | _not analysed_ |
| libLLVM.dylib | TIER_1 | 3 | — | _not analysed_ |
| libNFC_Comet.dylib | TIER_1 | 3 | — | _not analysed_ |
| libORTools.dylib | TIER_1 | 3 | — | _not analysed_ |
| libPCITransport.dylib | TIER_1 | 3 | — | _not analysed_ |
| libT200Updater.dylib | TIER_1 | 3 | — | _not analysed_ |
| libWebKitSwift.dylib | TIER_1 | 3 | — | _not analysed_ |
| libauthinstall.dylib | TIER_1 | 3 | — | _not analysed_ |
| libdispatch.dylib | TIER_1 | 3 | — | _not analysed_ |
| libdispatch_debug.dylib | TIER_1 | 3 | — | _not analysed_ |
| libdispatch_profile.dylib | TIER_1 | 3 | — | _not analysed_ |
| libimage4.dylib | TIER_1 | 3 | — | _not analysed_ |
| libmalloc_exclaves_introspector | TIER_1 | 3 | — | _not analysed_ |
| libmis.dylib | TIER_1 | 3 | — | _not analysed_ |
| libmobileassetd.dylib | TIER_1 | 3 | — | _not analysed_ |
| libnetworkextension.dylib | TIER_1 | 3 | — | _not analysed_ |
| libsqlite3.dylib | TIER_1 | 3 | — | _not analysed_ |
| libswiftCore.dylib | TIER_1 | 3 | — | _not analysed_ |
| libsystem_containermanager.dylib | TIER_1 | 3 | — | _not analysed_ |
| libsystem_malloc.dylib | TIER_1 | 3 | — | _not analysed_ |
| libsystem_malloc_debug.dylib | TIER_1 | 3 | — | _not analysed_ |
| libsystem_networkextension.dylib | TIER_1 | 3 | — | _not analysed_ |
| libusd_ms.dylib | TIER_1 | 3 | — | _not analysed_ |
| livefiles_apfs.dylib | TIER_1 | 3 | — | _not analysed_ |
| livefiles_exfat.dylib | TIER_1 | 3 | — | _not analysed_ |
| locationd | TIER_1 | 3 | — | _not analysed_ |
| lockdownd | TIER_1 | 3 | — | _not analysed_ |
| logd | TIER_1 | 3 | — | _not analysed_ |
| managedappdistributiond | TIER_1 | 3 | — | _not analysed_ |
| mediaremoted | TIER_1 | 3 | — | _not analysed_ |
| misagent | TIER_1 | 3 | — | _not analysed_ |
| mlhostd | TIER_1 | 3 | — | _not analysed_ |
| mount_apfs | TIER_1 | 3 | — | _not analysed_ |
| nanoregistryd | TIER_1 | 3 | — | _not analysed_ |
| neagent | TIER_1 | 3 | — | _not analysed_ |
| nearbyd | TIER_1 | 3 | — | _not analysed_ |
| nehelper | TIER_1 | 3 | — | _not analysed_ |
| nesessionmanager | TIER_1 | 3 | — | _not analysed_ |
| nfcd | TIER_1 | 3 | — | _not analysed_ |
| online-auth-agent | TIER_1 | 3 | — | _not analysed_ |
| osanalyticshelper | TIER_1 | 3 | — | _not analysed_ |
| passd | TIER_1 | 3 | — | _not analysed_ |
| ptpcamerad | TIER_1 | 3 | — | _not analysed_ |
| rans.t8140.release.im4p | TIER_1 | 3 | — | _not analysed_ |
| replayd | TIER_1 | 3 | — | _not analysed_ |
| safetycheckd | TIER_1 | 3 | — | _not analysed_ |
| securityd | TIER_1 | 3 | — | _not analysed_ |
| seserviced | TIER_1 | 3 | — | _not analysed_ |
| spaceattributiond | TIER_1 | 3 | — | _not analysed_ |
| srp-mdns-proxy | TIER_1 | 3 | — | _not analysed_ |
| storagekitd | TIER_1 | 3 | — | _not analysed_ |
| storagekitfsrunner | TIER_1 | 3 | — | _not analysed_ |
| subridged | TIER_1 | 3 | — | _not analysed_ |
| threadradiod | TIER_1 | 3 | — | _not analysed_ |
| txm.iphoneos.release.im4p | TIER_1 | 3 | — | _not analysed_ |
| usbaudiod | TIER_1 | 3 | — | _not analysed_ |
| wifianalyticsd | TIER_1 | 3 | — | _not analysed_ |
| wifip2pd | TIER_1 | 3 | — | _not analysed_ |
| AAAFoundation | TIER_2 | 2 | — | _not analysed_ |
| AACClient | TIER_2 | 2 | — | _not analysed_ |
| AACCore | TIER_2 | 2 | — | _not analysed_ |
| ABMHelper | TIER_2 | 2 | — | _not analysed_ |
| ACCBaker | TIER_2 | 2 | — | _not analysed_ |
| ACCHWComponentAuthService | TIER_2 | 2 | — | _not analysed_ |
| ACSEFoundation | TIER_2 | 2 | — | _not analysed_ |
| AEBookPlugins | TIER_2 | 2 | — | _not analysed_ |
| AFKUser | TIER_2 | 2 | — | _not analysed_ |
| AGXCompilerCore | TIER_2 | 2 | — | _not analysed_ |
| AGXGPURawCounter | TIER_2 | 2 | — | _not analysed_ |
| AGXMetalG17P | TIER_2 | 2 | — | _not analysed_ |
| AIMLExperimentationAnalytics | TIER_2 | 2 | — | _not analysed_ |
| AMSEngagementViewService | TIER_2 | 2 | — | _not analysed_ |
| AMSMediaServiceOwner | TIER_2 | 2 | — | _not analysed_ |
| ANECompilerService | TIER_2 | 2 | — | _not analysed_ |
| ANEServices | TIER_2 | 2 | — | _not analysed_ |
| ANEStorageMaintainer | TIER_2 | 2 | — | _not analysed_ |
| ANSTKit | TIER_2 | 2 | — | _not analysed_ |
| AONSense.dylib | TIER_2 | 2 | — | _not analysed_ |
| AOPHaptics | TIER_2 | 2 | — | _not analysed_ |
| APConfigurationSystem | TIER_2 | 2 | — | _not analysed_ |
| APFS | TIER_2 | 2 | — | _not analysed_ |
| APFoundation | TIER_2 | 2 | — | _not analysed_ |
| APTransport | TIER_2 | 2 | — | _not analysed_ |
| ARKitCore | TIER_2 | 2 | — | _not analysed_ |
| ASConfigurationSubscriber | TIER_2 | 2 | — | _not analysed_ |
| ASEProcessing | TIER_2 | 2 | — | _not analysed_ |
| ASMessagesProvider | TIER_2 | 2 | — | _not analysed_ |
| ASOctaneSupportXPCService | TIER_2 | 2 | — | _not analysed_ |
| ASPCarryLog | TIER_2 | 2 | — | _not analysed_ |
| ASRBridge | TIER_2 | 2 | — | _not analysed_ |
| ATFoundation | TIER_2 | 2 | — | _not analysed_ |
| AUDeveloperSettings | TIER_2 | 2 | — | _not analysed_ |
| AUSettings | TIER_2 | 2 | — | _not analysed_ |
| AVCHalogen | TIER_2 | 2 | — | _not analysed_ |
| AVFAudio | TIER_2 | 2 | — | _not analysed_ |
| AVFCapture | TIER_2 | 2 | — | _not analysed_ |
| AVFCore | TIER_2 | 2 | — | _not analysed_ |
| AVKit | TIER_2 | 2 | — | _not analysed_ |
| AVRouting | TIER_2 | 2 | — | _not analysed_ |
| AXCoreUtilities | TIER_2 | 2 | — | _not analysed_ |
| AXMotionCuesServer | TIER_2 | 2 | — | _not analysed_ |
| AXSoundDetectionUI | TIER_2 | 2 | — | _not analysed_ |
| AXSpeechAssetServices | TIER_2 | 2 | — | _not analysed_ |
| AXTapToSpeakTime | TIER_2 | 2 | — | _not analysed_ |
| AccelerateGPU | TIER_2 | 2 | — | _not analysed_ |
| Accessibility | TIER_2 | 2 | — | _not analysed_ |
| AccessibilityAuditCategories | TIER_2 | 2 | — | _not analysed_ |
| AccessibilityPlatformTranslation | TIER_2 | 2 | — | _not analysed_ |
| AccessibilitySettings | TIER_2 | 2 | — | _not analysed_ |
| AccessibilitySharedUISupport | TIER_2 | 2 | — | _not analysed_ |
| AccessibilityUIService | TIER_2 | 2 | — | _not analysed_ |
| AccessibilityUIUtilities | TIER_2 | 2 | — | _not analysed_ |
| AccessibilityUtilities | TIER_2 | 2 | — | _not analysed_ |
| AccessoryComponentAuth | TIER_2 | 2 | — | _not analysed_ |
| AccessorySetupKit | TIER_2 | 2 | — | _not analysed_ |
| AccessorySetupUI | TIER_2 | 2 | — | _not analysed_ |
| AccountSuggestions | TIER_2 | 2 | — | _not analysed_ |
| Accounts | TIER_2 | 2 | — | _not analysed_ |
| AccountsDaemon | TIER_2 | 2 | — | _not analysed_ |
| AccountsUI | TIER_2 | 2 | — | _not analysed_ |
| AccountsUISettings | TIER_2 | 2 | — | _not analysed_ |
| ActionButtonConfigurationUI | TIER_2 | 2 | — | _not analysed_ |
| ActionButtonSelector | TIER_2 | 2 | — | _not analysed_ |
| ActionButtonSettings | TIER_2 | 2 | — | _not analysed_ |
| ActionKit | TIER_2 | 2 | — | _not analysed_ |
| ActionKitUI | TIER_2 | 2 | — | _not analysed_ |
| ActionPredictionHeuristics | TIER_2 | 2 | — | _not analysed_ |
| ActionPredictionHeuristicsInternal | TIER_2 | 2 | — | _not analysed_ |
| ActiveSyncSettings | TIER_2 | 2 | — | _not analysed_ |
| ActivityAchievements | TIER_2 | 2 | — | _not analysed_ |
| ActivityAchievementsDaemon | TIER_2 | 2 | — | _not analysed_ |
| ActivityAchievementsUI | TIER_2 | 2 | — | _not analysed_ |
| ActivityKit | TIER_2 | 2 | — | _not analysed_ |
| ActivityProgressUI | TIER_2 | 2 | — | _not analysed_ |
| ActivitySharingDaemonCore | TIER_2 | 2 | — | _not analysed_ |
| ActivitySharingServices | TIER_2 | 2 | — | _not analysed_ |
| ActivityUI | TIER_2 | 2 | — | _not analysed_ |
| AdAttributionKit | TIER_2 | 2 | — | _not analysed_ |
| AdPlatforms | TIER_2 | 2 | — | _not analysed_ |
| AdPlatformsCommon | TIER_2 | 2 | — | _not analysed_ |
| AdaptiveMusic | TIER_2 | 2 | — | _not analysed_ |
| AdaptiveMusicApp | TIER_2 | 2 | — | _not analysed_ |
| AddressBookLegacy | TIER_2 | 2 | — | _not analysed_ |
| AeroML | TIER_2 | 2 | — | _not analysed_ |
| AfibBurden | TIER_2 | 2 | — | _not analysed_ |
| AirPlayHalogen | TIER_2 | 2 | — | _not analysed_ |
| AirPlayReceiver | TIER_2 | 2 | — | _not analysed_ |
| AirPlaySender | TIER_2 | 2 | — | _not analysed_ |
| AirPlaySenderService | TIER_2 | 2 | — | _not analysed_ |
| AirPlaySupport | TIER_2 | 2 | — | _not analysed_ |
| AirTrafficDevice | TIER_2 | 2 | — | _not analysed_ |
| AnnounceDaemon | TIER_2 | 2 | — | _not analysed_ |
| AppAnalytics | TIER_2 | 2 | — | _not analysed_ |
| AppAttestInternal | TIER_2 | 2 | — | _not analysed_ |
| AppC3D | TIER_2 | 2 | — | _not analysed_ |
| AppClipDeveloperSettings | TIER_2 | 2 | — | _not analysed_ |
| AppDistribution | TIER_2 | 2 | — | _not analysed_ |
| AppDistributionLaunchAngel | TIER_2 | 2 | — | _not analysed_ |
| AppInstallationSettings | TIER_2 | 2 | — | _not analysed_ |
| AppIntentSchemas | TIER_2 | 2 | — | _not analysed_ |
| AppIntents | TIER_2 | 2 | — | _not analysed_ |
| AppIntentsServices | TIER_2 | 2 | — | _not analysed_ |
| AppLaunchPlugin | TIER_2 | 2 | — | _not analysed_ |
| AppLaunchSuggestionsPlugin | TIER_2 | 2 | — | _not analysed_ |
| AppMigrationKit | TIER_2 | 2 | — | _not analysed_ |
| AppPlaceholderSync | TIER_2 | 2 | — | _not analysed_ |
| AppPredictionClient | TIER_2 | 2 | — | _not analysed_ |
| AppPredictionFoundation | TIER_2 | 2 | — | _not analysed_ |
| AppPredictionInternal | TIER_2 | 2 | — | _not analysed_ |
| AppPredictionUI | TIER_2 | 2 | — | _not analysed_ |
| AppPredictionUIFoundation | TIER_2 | 2 | — | _not analysed_ |
| AppPredictionUIWidget | TIER_2 | 2 | — | _not analysed_ |
| AppProtection | TIER_2 | 2 | — | _not analysed_ |
| AppProtectionUI | TIER_2 | 2 | — | _not analysed_ |
| AppRecommendations | TIER_2 | 2 | — | _not analysed_ |
| AppSSO | TIER_2 | 2 | — | _not analysed_ |
| AppSSOCore | TIER_2 | 2 | — | _not analysed_ |
| AppSSOKerberos | TIER_2 | 2 | — | _not analysed_ |
| AppSSOUIService | TIER_2 | 2 | — | _not analysed_ |
| AppServerSupport | TIER_2 | 2 | — | _not analysed_ |
| AppState | TIER_2 | 2 | — | _not analysed_ |
| AppStore | TIER_2 | 2 | — | _not analysed_ |
| AppStoreComponents | TIER_2 | 2 | — | _not analysed_ |
| AppStoreDaemon | TIER_2 | 2 | — | _not analysed_ |
| AppStoreKit | TIER_2 | 2 | — | _not analysed_ |
| AppSystemSettingsUI | TIER_2 | 2 | — | _not analysed_ |
| AppleAccount | TIER_2 | 2 | — | _not analysed_ |
| AppleAccountSettings | TIER_2 | 2 | — | _not analysed_ |
| AppleBasebandLink | TIER_2 | 2 | — | _not analysed_ |
| AppleCVHWA | TIER_2 | 2 | — | _not analysed_ |
| AppleCareSupport | TIER_2 | 2 | — | _not analysed_ |
| AppleConvergedFirmwareUpdater | TIER_2 | 2 | — | _not analysed_ |
| AppleConvergedTransport.dylib | TIER_2 | 2 | — | _not analysed_ |
| AppleCredentialManagerDaemon | TIER_2 | 2 | — | _not analysed_ |
| AppleDepth | TIER_2 | 2 | — | _not analysed_ |
| AppleDeviceQueryService | TIER_2 | 2 | — | _not analysed_ |
| AppleDeviceQuerySupport | TIER_2 | 2 | — | _not analysed_ |
| AppleFirmwareUpdate | TIER_2 | 2 | — | _not analysed_ |
| AppleHIDTransportSupport | TIER_2 | 2 | — | _not analysed_ |
| AppleHPMLib | TIER_2 | 2 | — | _not analysed_ |
| AppleIDAMDriver | TIER_2 | 2 | — | _not analysed_ |
| AppleIDSetup | TIER_2 | 2 | — | _not analysed_ |
| AppleIDSetupDaemon | TIER_2 | 2 | — | _not analysed_ |
| AppleIDSetupUI | TIER_2 | 2 | — | _not analysed_ |
| AppleIDSetupUIService | TIER_2 | 2 | — | _not analysed_ |
| AppleKeyStore | TIER_2 | 2 | — | _not analysed_ |
| AppleLockdownMode | TIER_2 | 2 | — | _not analysed_ |
| AppleMIDIUSBDriver | TIER_2 | 2 | — | _not analysed_ |
| AppleMediaDiscovery | TIER_2 | 2 | — | _not analysed_ |
| AppleMediaServicesKitInternal | TIER_2 | 2 | — | _not analysed_ |
| AppleMediaServicesKitSupport | TIER_2 | 2 | — | _not analysed_ |
| AppleMediaServicesUIDynamic | TIER_2 | 2 | — | _not analysed_ |
| AppleMediaServicesUIPaymentSheets | TIER_2 | 2 | — | _not analysed_ |
| AppleMesaLib | TIER_2 | 2 | — | _not analysed_ |
| AppleMipcRouter | TIER_2 | 2 | — | _not analysed_ |
| ApplePDPHelper | TIER_2 | 2 | — | _not analysed_ |
| ApplePhotonDetectorServices | TIER_2 | 2 | — | _not analysed_ |
| AppleProResHWDecoder.videodecoder | TIER_2 | 2 | — | _not analysed_ |
| AppleProResHWEncoder.videoencoder | TIER_2 | 2 | — | _not analysed_ |
| AppleProxServiceFilter | TIER_2 | 2 | — | _not analysed_ |
| ApplePushService | TIER_2 | 2 | — | _not analysed_ |
| AppleSARHelper | TIER_2 | 2 | — | _not analysed_ |
| AppleSPUAccCompassPlugin | TIER_2 | 2 | — | _not analysed_ |
| AppleSPUDispCompassPlugin | TIER_2 | 2 | — | _not analysed_ |
| AppleSPULib | TIER_2 | 2 | — | _not analysed_ |
| AppleTV | TIER_2 | 2 | — | _not analysed_ |
| AppleTracingSupportSymbolication | TIER_2 | 2 | — | _not analysed_ |
| AppleVisionProApp | TIER_2 | 2 | — | _not analysed_ |
| AppleWirelessChargingServiceFilter | TIER_2 | 2 | — | _not analysed_ |
| ArchetypeEngine | TIER_2 | 2 | — | _not analysed_ |
| AssetCacheLocatorService | TIER_2 | 2 | — | _not analysed_ |
| AssetExplorer | TIER_2 | 2 | — | _not analysed_ |
| AssetViewer | TIER_2 | 2 | — | _not analysed_ |
| AssistantServices | TIER_2 | 2 | — | _not analysed_ |
| AssistantSettingsSupport | TIER_2 | 2 | — | _not analysed_ |
| AttentionAwareness | TIER_2 | 2 | — | _not analysed_ |
| AttributeGraph | TIER_2 | 2 | — | _not analysed_ |
| AudioAccessoryServices | TIER_2 | 2 | — | _not analysed_ |
| AudioCodecs | TIER_2 | 2 | — | _not analysed_ |
| AudioDSPGraph | TIER_2 | 2 | — | _not analysed_ |
| AudioDSPManager | TIER_2 | 2 | — | _not analysed_ |
| AudioFlowDelegatePlugin | TIER_2 | 2 | — | _not analysed_ |
| AudioServerApplication | TIER_2 | 2 | — | _not analysed_ |
| AudioServerDriver | TIER_2 | 2 | — | _not analysed_ |
| AudioServerDriverTransports_Base | TIER_2 | 2 | — | _not analysed_ |
| AudioServerDriverTransports_IOP | TIER_2 | 2 | — | _not analysed_ |
| AudioSession | TIER_2 | 2 | — | _not analysed_ |
| AudioSessionServer | TIER_2 | 2 | — | _not analysed_ |
| AudioSuggestionsPlugin | TIER_2 | 2 | — | _not analysed_ |
| AudioToolboxCore | TIER_2 | 2 | — | _not analysed_ |
| AudioUIPlugin | TIER_2 | 2 | — | _not analysed_ |
| AuthKit | TIER_2 | 2 | — | _not analysed_ |
| AuthKitUI | TIER_2 | 2 | — | _not analysed_ |
| AuthKitUIService | TIER_2 | 2 | — | _not analysed_ |
| AutoBugCaptureCore | TIER_2 | 2 | — | _not analysed_ |
| AutoFillCore | TIER_2 | 2 | — | _not analysed_ |
| AutoFillUI | TIER_2 | 2 | — | _not analysed_ |
| AutomationModeUI | TIER_2 | 2 | — | _not analysed_ |
| AvatarKit | TIER_2 | 2 | — | _not analysed_ |
| AvatarPersistence | TIER_2 | 2 | — | _not analysed_ |
| AvatarUI | TIER_2 | 2 | — | _not analysed_ |
| BKLibrary | TIER_2 | 2 | — | _not analysed_ |
| BTAudioHALPlugin | TIER_2 | 2 | — | _not analysed_ |
| BTLEServer | TIER_2 | 2 | — | _not analysed_ |
| BackBoard | TIER_2 | 2 | — | _not analysed_ |
| BackBoardHIDEventFoundation | TIER_2 | 2 | — | _not analysed_ |
| BackBoardServices | TIER_2 | 2 | — | _not analysed_ |
| BackgroundAssets | TIER_2 | 2 | — | _not analysed_ |
| BackgroundTaskAgent | TIER_2 | 2 | — | _not analysed_ |
| BackgroundTasks | TIER_2 | 2 | — | _not analysed_ |
| BackupAgent2 | TIER_2 | 2 | — | _not analysed_ |
| BannerKit | TIER_2 | 2 | — | _not analysed_ |
| BarcodeSupport | TIER_2 | 2 | — | _not analysed_ |
| BarcodeSupportUI | TIER_2 | 2 | — | _not analysed_ |
| BaseBoardUI | TIER_2 | 2 | — | _not analysed_ |
| BasebandTraceHelper | TIER_2 | 2 | — | _not analysed_ |
| BatteryAlgorithms | TIER_2 | 2 | — | _not analysed_ |
| BatteryCenter | TIER_2 | 2 | — | _not analysed_ |
| BatteryIntelligence | TIER_2 | 2 | — | _not analysed_ |
| BatteryUsageUI | TIER_2 | 2 | — | _not analysed_ |
| BiomeFoundation | TIER_2 | 2 | — | _not analysed_ |
| BiomeStorage | TIER_2 | 2 | — | _not analysed_ |
| BiomeStreams | TIER_2 | 2 | — | _not analysed_ |
| BiometricKitUI | TIER_2 | 2 | — | _not analysed_ |
| Blackbeard | TIER_2 | 2 | — | _not analysed_ |
| BlastDoor | TIER_2 | 2 | — | _not analysed_ |
| BlueTool | TIER_2 | 2 | — | _not analysed_ |
| BoardServices | TIER_2 | 2 | — | _not analysed_ |
| BookAnalytics | TIER_2 | 2 | — | _not analysed_ |
| BookCore | TIER_2 | 2 | — | _not analysed_ |
| BookDataStore | TIER_2 | 2 | — | _not analysed_ |
| BookEPUB | TIER_2 | 2 | — | _not analysed_ |
| BookFoundation | TIER_2 | 2 | — | _not analysed_ |
| BookLibraryCore | TIER_2 | 2 | — | _not analysed_ |
| Books | TIER_2 | 2 | — | _not analysed_ |
| BooksUI | TIER_2 | 2 | — | _not analysed_ |
| BrailleTranslation | TIER_2 | 2 | — | _not analysed_ |
| Bridge | TIER_2 | 2 | — | _not analysed_ |
| BridgeAppStoreDaemonSettings | TIER_2 | 2 | — | _not analysed_ |
| BridgePreferences | TIER_2 | 2 | — | _not analysed_ |
| BrowserEngineKit | TIER_2 | 2 | — | _not analysed_ |
| BuddyMigrator | TIER_2 | 2 | — | _not analysed_ |
| BulletinBoard | TIER_2 | 2 | — | _not analysed_ |
| BulletinDistributorCompanion | TIER_2 | 2 | — | _not analysed_ |
| BundleComplicationMigrationService | TIER_2 | 2 | — | _not analysed_ |
| BusinessChatService | TIER_2 | 2 | — | _not analysed_ |
| BusinessChatViewService | TIER_2 | 2 | — | _not analysed_ |
| BusinessFoundation | TIER_2 | 2 | — | _not analysed_ |
| CAFCombine | TIER_2 | 2 | — | _not analysed_ |
| CAFUI | TIER_2 | 2 | — | _not analysed_ |
| CDDataAccess | TIER_2 | 2 | — | _not analysed_ |
| CFNetwork | TIER_2 | 2 | — | _not analysed_ |
| CMCapture | TIER_2 | 2 | — | _not analysed_ |
| CMCaptureCore | TIER_2 | 2 | — | _not analysed_ |
| CMContinuityCaptureCore | TIER_2 | 2 | — | _not analysed_ |
| CMFSyncAgent | TIER_2 | 2 | — | _not analysed_ |
| CMImaging | TIER_2 | 2 | — | _not analysed_ |
| CMPhoto | TIER_2 | 2 | — | _not analysed_ |
| CPMS | TIER_2 | 2 | — | _not analysed_ |
| CTBlastDoorSupport | TIER_2 | 2 | — | _not analysed_ |
| CTKUIService | TIER_2 | 2 | — | _not analysed_ |
| CTLazuliSupport | TIER_2 | 2 | — | _not analysed_ |
| CacheDelete | TIER_2 | 2 | — | _not analysed_ |
| Calculate | TIER_2 | 2 | — | _not analysed_ |
| CalculateUI | TIER_2 | 2 | — | _not analysed_ |
| Calculator | TIER_2 | 2 | — | _not analysed_ |
| CalendarDaemon | TIER_2 | 2 | — | _not analysed_ |
| CalendarDatabase | TIER_2 | 2 | — | _not analysed_ |
| CalendarFoundation | TIER_2 | 2 | — | _not analysed_ |
| CalendarUIKit | TIER_2 | 2 | — | _not analysed_ |
| CallDirectorySettings | TIER_2 | 2 | — | _not analysed_ |
| CallForwardingTelephonySettings | TIER_2 | 2 | — | _not analysed_ |
| CallKit | TIER_2 | 2 | — | _not analysed_ |
| CallWaitingTelephonySettings | TIER_2 | 2 | — | _not analysed_ |
| CallingLineIdRestrictionTelephonySettings | TIER_2 | 2 | — | _not analysed_ |
| Camera | TIER_2 | 2 | — | _not analysed_ |
| CameraEditKit | TIER_2 | 2 | — | _not analysed_ |
| CameraEffectsKit | TIER_2 | 2 | — | _not analysed_ |
| CameraOverlayAngel | TIER_2 | 2 | — | _not analysed_ |
| CameraSettings | TIER_2 | 2 | — | _not analysed_ |
| CaptiveNetwork | TIER_2 | 2 | — | _not analysed_ |
| CaptiveNetworkSupport | TIER_2 | 2 | — | _not analysed_ |
| CarAccessoryFramework | TIER_2 | 2 | — | _not analysed_ |
| CarCamera | TIER_2 | 2 | — | _not analysed_ |
| CarCommandsFlowDelegatePlugin | TIER_2 | 2 | — | _not analysed_ |
| CarKit | TIER_2 | 2 | — | _not analysed_ |
| CarKitSettings | TIER_2 | 2 | — | _not analysed_ |
| CarPlay | TIER_2 | 2 | — | _not analysed_ |
| CarPlayAssetUI | TIER_2 | 2 | — | _not analysed_ |
| CarPlaySettings | TIER_2 | 2 | — | _not analysed_ |
| CarPlaySupport | TIER_2 | 2 | — | _not analysed_ |
| CarPlayUI | TIER_2 | 2 | — | _not analysed_ |
| CarPlayUIServices | TIER_2 | 2 | — | _not analysed_ |
| CarouselPreferenceServices | TIER_2 | 2 | — | _not analysed_ |
| CascadeEngine | TIER_2 | 2 | — | _not analysed_ |
| CascadeSets | TIER_2 | 2 | — | _not analysed_ |
| Celestial | TIER_2 | 2 | — | _not analysed_ |
| CellularBridgeUI | TIER_2 | 2 | — | _not analysed_ |
| CellularPlanManager | TIER_2 | 2 | — | _not analysed_ |
| Charts | TIER_2 | 2 | — | _not analysed_ |
| CheckerBoard | TIER_2 | 2 | — | _not analysed_ |
| CheckerBoardRemoteSetup | TIER_2 | 2 | — | _not analysed_ |
| Chirp | TIER_2 | 2 | — | _not analysed_ |
| ChronoKit | TIER_2 | 2 | — | _not analysed_ |
| ChronoUIServices | TIER_2 | 2 | — | _not analysed_ |
| CiderAudioServer | TIER_2 | 2 | — | _not analysed_ |
| CipherML | TIER_2 | 2 | — | _not analysed_ |
| CircleJoinRequested | TIER_2 | 2 | — | _not analysed_ |
| ClarityBoard | TIER_2 | 2 | — | _not analysed_ |
| ClarityUIServer | TIER_2 | 2 | — | _not analysed_ |
| ClassKit | TIER_2 | 2 | — | _not analysed_ |
| ClassificationAndReportingSettingsBundle | TIER_2 | 2 | — | _not analysed_ |
| Climate | TIER_2 | 2 | — | _not analysed_ |
| ClipServices | TIER_2 | 2 | — | _not analysed_ |
| ClockKit | TIER_2 | 2 | — | _not analysed_ |
| ClockKitUI | TIER_2 | 2 | — | _not analysed_ |
| Closures | TIER_2 | 2 | — | _not analysed_ |
| CloudAsset | TIER_2 | 2 | — | _not analysed_ |
| CloudAssets | TIER_2 | 2 | — | _not analysed_ |
| CloudAttestation | TIER_2 | 2 | — | _not analysed_ |
| CloudDocs | TIER_2 | 2 | — | _not analysed_ |
| CloudKeychainProxy | TIER_2 | 2 | — | _not analysed_ |
| CloudKitSettings | TIER_2 | 2 | — | _not analysed_ |
| CloudPhotoLibrary | TIER_2 | 2 | — | _not analysed_ |
| CloudRecommendation | TIER_2 | 2 | — | _not analysed_ |
| CloudRecommendationUI | TIER_2 | 2 | — | _not analysed_ |
| CloudServices | TIER_2 | 2 | — | _not analysed_ |
| CloudSharing | TIER_2 | 2 | — | _not analysed_ |
| CloudSubscriptionFeatures | TIER_2 | 2 | — | _not analysed_ |
| CloudTabsMigrator | TIER_2 | 2 | — | _not analysed_ |
| CloudTelemetryTools | TIER_2 | 2 | — | _not analysed_ |
| Coherence | TIER_2 | 2 | — | _not analysed_ |
| ColorSync | TIER_2 | 2 | — | _not analysed_ |
| CommCenterRootHelper | TIER_2 | 2 | — | _not analysed_ |
| CommunicationsSetupUI | TIER_2 | 2 | — | _not analysed_ |
| CommunicationsUI | TIER_2 | 2 | — | _not analysed_ |
| CommunicationsUICore | TIER_2 | 2 | — | _not analysed_ |
| CompanionCamera | TIER_2 | 2 | — | _not analysed_ |
| CompanionServices | TIER_2 | 2 | — | _not analysed_ |
| ComputationalGraph | TIER_2 | 2 | — | _not analysed_ |
| ComputeSafeguards | TIER_2 | 2 | — | _not analysed_ |
| ConditionInducer | TIER_2 | 2 | — | _not analysed_ |
| ContactlessReaderUI | TIER_2 | 2 | — | _not analysed_ |
| Contacts | TIER_2 | 2 | — | _not analysed_ |
| ContactsAutocompleteUI | TIER_2 | 2 | — | _not analysed_ |
| ContactsFoundation | TIER_2 | 2 | — | _not analysed_ |
| ContentKit | TIER_2 | 2 | — | _not analysed_ |
| ContextualSuggestionClient | TIER_2 | 2 | — | _not analysed_ |
| ContinuityCaptureShieldUI | TIER_2 | 2 | — | _not analysed_ |
| ContinuousExposeModule | TIER_2 | 2 | — | _not analysed_ |
| ControlCenterUI | TIER_2 | 2 | — | _not analysed_ |
| ControlCenterUIKit | TIER_2 | 2 | — | _not analysed_ |
| ControlsFlowDelegatePlugin | TIER_2 | 2 | — | _not analysed_ |
| ConversationKit | TIER_2 | 2 | — | _not analysed_ |
| CookingKit | TIER_2 | 2 | — | _not analysed_ |
| CopresenceCore | TIER_2 | 2 | — | _not analysed_ |
| CoreALD | TIER_2 | 2 | — | _not analysed_ |
| CoreAUC | TIER_2 | 2 | — | _not analysed_ |
| CoreAccessories | TIER_2 | 2 | — | _not analysed_ |
| CoreAppleCVA | TIER_2 | 2 | — | _not analysed_ |
| CoreAudioKit | TIER_2 | 2 | — | _not analysed_ |
| CoreAuthUI | TIER_2 | 2 | — | _not analysed_ |
| CoreCDP | TIER_2 | 2 | — | _not analysed_ |
| CoreCDPUI | TIER_2 | 2 | — | _not analysed_ |
| CoreCaptureDaemon | TIER_2 | 2 | — | _not analysed_ |
| CoreDuet | TIER_2 | 2 | — | _not analysed_ |
| CoreDynamicUIPlugin | TIER_2 | 2 | — | _not analysed_ |
| CoreEmoji | TIER_2 | 2 | — | _not analysed_ |
| CoreFollowUp | TIER_2 | 2 | — | _not analysed_ |
| CoreFollowUpUI | TIER_2 | 2 | — | _not analysed_ |
| CoreFoundation | TIER_2 | 2 | — | _not analysed_ |
| CoreGraphics | TIER_2 | 2 | — | _not analysed_ |
| CoreHAP | TIER_2 | 2 | — | _not analysed_ |
| CoreHaptics | TIER_2 | 2 | — | _not analysed_ |
| CoreIDCred | TIER_2 | 2 | — | _not analysed_ |
| CoreIDCredBuilder | TIER_2 | 2 | — | _not analysed_ |
| CoreIDV | TIER_2 | 2 | — | _not analysed_ |
| CoreIDVRGBLiveness | TIER_2 | 2 | — | _not analysed_ |
| CoreIDVUI | TIER_2 | 2 | — | _not analysed_ |
| CoreIK | TIER_2 | 2 | — | _not analysed_ |
| CoreKnowledge | TIER_2 | 2 | — | _not analysed_ |
| CoreLocation | TIER_2 | 2 | — | _not analysed_ |
| CoreLocationReplay | TIER_2 | 2 | — | _not analysed_ |
| CoreLocationTiles | TIER_2 | 2 | — | _not analysed_ |
| CoreMIDI | TIER_2 | 2 | — | _not analysed_ |
| CoreMediaIO | TIER_2 | 2 | — | _not analysed_ |
| CoreMediaStream | TIER_2 | 2 | — | _not analysed_ |
| CoreMotion | TIER_2 | 2 | — | _not analysed_ |
| CoreNFC | TIER_2 | 2 | — | _not analysed_ |
| CoreNLP | TIER_2 | 2 | — | _not analysed_ |
| CoreOC | TIER_2 | 2 | — | _not analysed_ |
| CoreODI | TIER_2 | 2 | — | _not analysed_ |
| CoreODIEssentials | TIER_2 | 2 | — | _not analysed_ |
| CoreParsec | TIER_2 | 2 | — | _not analysed_ |
| CoreRC | TIER_2 | 2 | — | _not analysed_ |
| CoreRCHIDService | TIER_2 | 2 | — | _not analysed_ |
| CoreRealityIO | TIER_2 | 2 | — | _not analysed_ |
| CoreRecents | TIER_2 | 2 | — | _not analysed_ |
| CoreRecognition | TIER_2 | 2 | — | _not analysed_ |
| CoreRepairKit | TIER_2 | 2 | — | _not analysed_ |
| CoreRepairLite | TIER_2 | 2 | — | _not analysed_ |
| CoreRepairUI | TIER_2 | 2 | — | _not analysed_ |
| CoreRoutine | TIER_2 | 2 | — | _not analysed_ |
| CoreRoutineHelperService | TIER_2 | 2 | — | _not analysed_ |
| CoreSceneUnderstanding | TIER_2 | 2 | — | _not analysed_ |
| CoreSpeechExclave | TIER_2 | 2 | — | _not analysed_ |
| CoreSpeechFoundation | TIER_2 | 2 | — | _not analysed_ |
| CoreSpeechUtils | TIER_2 | 2 | — | _not analysed_ |
| CoreSuggestions | TIER_2 | 2 | — | _not analysed_ |
| CoreSuggestionsInternals | TIER_2 | 2 | — | _not analysed_ |
| CoreSuggestionsUI | TIER_2 | 2 | — | _not analysed_ |
| CoreSymbolication | TIER_2 | 2 | — | _not analysed_ |
| CoreTelephony | TIER_2 | 2 | — | _not analysed_ |
| CoreThreadCommissionerServiced | TIER_2 | 2 | — | _not analysed_ |
| CoreUtils | TIER_2 | 2 | — | _not analysed_ |
| CoreUtilsSwift | TIER_2 | 2 | — | _not analysed_ |
| CoverSheet | TIER_2 | 2 | — | _not analysed_ |
| CoverSheetKit | TIER_2 | 2 | — | _not analysed_ |
| CreateML | TIER_2 | 2 | — | _not analysed_ |
| CryptexKit | TIER_2 | 2 | — | _not analysed_ |
| CryptoKit | TIER_2 | 2 | — | _not analysed_ |
| CryptoKitPrivate | TIER_2 | 2 | — | _not analysed_ |
| CryptoTokenKit | TIER_2 | 2 | — | _not analysed_ |
| DACalDAV | TIER_2 | 2 | — | _not analysed_ |
| DADaemonCalDAV | TIER_2 | 2 | — | _not analysed_ |
| DADaemonSupport | TIER_2 | 2 | — | _not analysed_ |
| DAEAS | TIER_2 | 2 | — | _not analysed_ |
| DAEASOAuthFramework | TIER_2 | 2 | — | _not analysed_ |
| DEPClientLibrary | TIER_2 | 2 | — | _not analysed_ |
| DKPairingUIService | TIER_2 | 2 | — | _not analysed_ |
| DMCApps | TIER_2 | 2 | — | _not analysed_ |
| DMCEnrollmentLibrary | TIER_2 | 2 | — | _not analysed_ |
| DMCEnrollmentProvider | TIER_2 | 2 | — | _not analysed_ |
| DMCUtilities | TIER_2 | 2 | — | _not analysed_ |
| DPSubmissionService | TIER_2 | 2 | — | _not analysed_ |
| DTXConnectionServices | TIER_2 | 2 | — | _not analysed_ |
| DVTInstrumentsFoundation | TIER_2 | 2 | — | _not analysed_ |
| DaemonUtils | TIER_2 | 2 | — | _not analysed_ |
| DailyBriefingFlowPlugin | TIER_2 | 2 | — | _not analysed_ |
| DashBoard | TIER_2 | 2 | — | _not analysed_ |
| DataAccess | TIER_2 | 2 | — | _not analysed_ |
| DataDetectorsCore | TIER_2 | 2 | — | _not analysed_ |
| DataDetectorsUI | TIER_2 | 2 | — | _not analysed_ |
| DeepThoughtBiomeFoundation | TIER_2 | 2 | — | _not analysed_ |
| DefaultAppsPasswordManagerSettings | TIER_2 | 2 | — | _not analysed_ |
| Dendrite | TIER_2 | 2 | — | _not analysed_ |
| DesktopServicesPriv | TIER_2 | 2 | — | _not analysed_ |
| DeveloperSettings | TIER_2 | 2 | — | _not analysed_ |
| DeviceAccess | TIER_2 | 2 | — | _not analysed_ |
| DeviceActivity | TIER_2 | 2 | — | _not analysed_ |
| DeviceCheck | TIER_2 | 2 | — | _not analysed_ |
| DeviceCheckInternal | TIER_2 | 2 | — | _not analysed_ |
| DeviceDataResetXPCServiceWorker | TIER_2 | 2 | — | _not analysed_ |
| DeviceDiscoveryUICore | TIER_2 | 2 | — | _not analysed_ |
| DeviceExpertIntents | TIER_2 | 2 | — | _not analysed_ |
| DeviceExpertUI | TIER_2 | 2 | — | _not analysed_ |
| DeviceIdentity | TIER_2 | 2 | — | _not analysed_ |
| DeviceManagement | TIER_2 | 2 | — | _not analysed_ |
| DeviceManagementTools | TIER_2 | 2 | — | _not analysed_ |
| DiagnosticExtensionsDaemon | TIER_2 | 2 | — | _not analysed_ |
| DiagnosticRequest | TIER_2 | 2 | — | _not analysed_ |
| DiagnosticRequestService | TIER_2 | 2 | — | _not analysed_ |
| Diagnostics | TIER_2 | 2 | — | _not analysed_ |
| DiagnosticsReporterServices | TIER_2 | 2 | — | _not analysed_ |
| DialAssistTelephonySettings | TIER_2 | 2 | — | _not analysed_ |
| DialogEngine | TIER_2 | 2 | — | _not analysed_ |
| DigitalAccess | TIER_2 | 2 | — | _not analysed_ |
| DigitalSeparation | TIER_2 | 2 | — | _not analysed_ |
| DigitalSeparationUI | TIER_2 | 2 | — | _not analysed_ |
| DisembarkUI | TIER_2 | 2 | — | _not analysed_ |
| DiskArbitration | TIER_2 | 2 | — | _not analysed_ |
| DiskImages2 | TIER_2 | 2 | — | _not analysed_ |
| DisplayAndBrightnessSettings | TIER_2 | 2 | — | _not analysed_ |
| DistributedEvaluation | TIER_2 | 2 | — | _not analysed_ |
| DockKitCore | TIER_2 | 2 | — | _not analysed_ |
| DocumentCamera | TIER_2 | 2 | — | _not analysed_ |
| DocumentManager | TIER_2 | 2 | — | _not analysed_ |
| DocumentManagerCore | TIER_2 | 2 | — | _not analysed_ |
| DocumentManagerExecutables | TIER_2 | 2 | — | _not analysed_ |
| DocumentManagerUICore | TIER_2 | 2 | — | _not analysed_ |
| DocumentUnderstanding | TIER_2 | 2 | — | _not analysed_ |
| DocumentUnderstandingClient | TIER_2 | 2 | — | _not analysed_ |
| DrawingBoard | TIER_2 | 2 | — | _not analysed_ |
| DuetActivityScheduler | TIER_2 | 2 | — | _not analysed_ |
| Dyld | TIER_2 | 2 | — | _not analysed_ |
| EAFirmwareUpdater | TIER_2 | 2 | — | _not analysed_ |
| EAUpdaterService | TIER_2 | 2 | — | _not analysed_ |
| EXDisplayPipe | TIER_2 | 2 | — | _not analysed_ |
| EcosystemAnalytics | TIER_2 | 2 | — | _not analysed_ |
| Email | TIER_2 | 2 | — | _not analysed_ |
| EmailCore | TIER_2 | 2 | — | _not analysed_ |
| EmailDaemon | TIER_2 | 2 | — | _not analysed_ |
| EmailFoundation | TIER_2 | 2 | — | _not analysed_ |
| EmbeddedDataReset | TIER_2 | 2 | — | _not analysed_ |
| EmbeddingService | TIER_2 | 2 | — | _not analysed_ |
| EmojiFoundation | TIER_2 | 2 | — | _not analysed_ |
| EnergyKitFoundation | TIER_2 | 2 | — | _not analysed_ |
| EngagementCollector | TIER_2 | 2 | — | _not analysed_ |
| EnhancedLoggingState | TIER_2 | 2 | — | _not analysed_ |
| EscrowSecurityAlert | TIER_2 | 2 | — | _not analysed_ |
| Espresso | TIER_2 | 2 | — | _not analysed_ |
| EventKit | TIER_2 | 2 | — | _not analysed_ |
| EventKitUI | TIER_2 | 2 | — | _not analysed_ |
| EventViewService | TIER_2 | 2 | — | _not analysed_ |
| ExtensionKit | TIER_2 | 2 | — | _not analysed_ |
| FMDMagSafeSetupRemoteUI | TIER_2 | 2 | — | _not analysed_ |
| FMFCore | TIER_2 | 2 | — | _not analysed_ |
| FMFindingUI | TIER_2 | 2 | — | _not analysed_ |
| FMIPCore | TIER_2 | 2 | — | _not analysed_ |
| FRC | TIER_2 | 2 | — | _not analysed_ |
| FSKit | TIER_2 | 2 | — | _not analysed_ |
| FTRemoteEventHIDSessionFilter | TIER_2 | 2 | — | _not analysed_ |
| FTServices | TIER_2 | 2 | — | _not analysed_ |
| FaceTime | TIER_2 | 2 | — | _not analysed_ |
| FamilyCircleUI | TIER_2 | 2 | — | _not analysed_ |
| FastpathLib | TIER_2 | 2 | — | _not analysed_ |
| FeatureStore | TIER_2 | 2 | — | _not analysed_ |
| FedStats | TIER_2 | 2 | — | _not analysed_ |
| FedStatsPluginCore | TIER_2 | 2 | — | _not analysed_ |
| FeedbackCore | TIER_2 | 2 | — | _not analysed_ |
| FeedbackLogger | TIER_2 | 2 | — | _not analysed_ |
| FileProvider | TIER_2 | 2 | — | _not analysed_ |
| Files | TIER_2 | 2 | — | _not analysed_ |
| FilesystemMetadataSnapshotService | TIER_2 | 2 | — | _not analysed_ |
| FinHealthInsights | TIER_2 | 2 | — | _not analysed_ |
| FinanceDaemon | TIER_2 | 2 | — | _not analysed_ |
| FinanceKit | TIER_2 | 2 | — | _not analysed_ |
| FinanceKitUI | TIER_2 | 2 | — | _not analysed_ |
| FinanceUIService | TIER_2 | 2 | — | _not analysed_ |
| FindMy | TIER_2 | 2 | — | _not analysed_ |
| FindMyAppCore | TIER_2 | 2 | — | _not analysed_ |
| FindMyBase | TIER_2 | 2 | — | _not analysed_ |
| FindMyCloudKit | TIER_2 | 2 | — | _not analysed_ |
| FindMyCommon | TIER_2 | 2 | — | _not analysed_ |
| FindMyCore | TIER_2 | 2 | — | _not analysed_ |
| FindMyCrypto | TIER_2 | 2 | — | _not analysed_ |
| FindMyDevice | TIER_2 | 2 | — | _not analysed_ |
| FindMyDeviceHelperXPCService | TIER_2 | 2 | — | _not analysed_ |
| FindMyPairing | TIER_2 | 2 | — | _not analysed_ |
| FindMyRemoteUIService | TIER_2 | 2 | — | _not analysed_ |
| FindMyServerInteraction | TIER_2 | 2 | — | _not analysed_ |
| FindMyUICore | TIER_2 | 2 | — | _not analysed_ |
| FinishRestoreFromBackup | TIER_2 | 2 | — | _not analysed_ |
| Fitness | TIER_2 | 2 | — | _not analysed_ |
| FitnessActions | TIER_2 | 2 | — | _not analysed_ |
| FitnessAsset | TIER_2 | 2 | — | _not analysed_ |
| FitnessAwards | TIER_2 | 2 | — | _not analysed_ |
| FitnessBrowsing | TIER_2 | 2 | — | _not analysed_ |
| FitnessCanvas | TIER_2 | 2 | — | _not analysed_ |
| FitnessCanvasUI | TIER_2 | 2 | — | _not analysed_ |
| FitnessCoachingServices | TIER_2 | 2 | — | _not analysed_ |
| FitnessFiltering | TIER_2 | 2 | — | _not analysed_ |
| FitnessLibrary | TIER_2 | 2 | — | _not analysed_ |
| FitnessMarketing | TIER_2 | 2 | — | _not analysed_ |
| FitnessOnboarding | TIER_2 | 2 | — | _not analysed_ |
| FitnessSearch | TIER_2 | 2 | — | _not analysed_ |
| FitnessSettings | TIER_2 | 2 | — | _not analysed_ |
| FitnessUI | TIER_2 | 2 | — | _not analysed_ |
| FitnessWorkoutPlan | TIER_2 | 2 | — | _not analysed_ |
| FlightUtilitiesCore | TIER_2 | 2 | — | _not analysed_ |
| FocusEngine | TIER_2 | 2 | — | _not analysed_ |
| FocusSettings | TIER_2 | 2 | — | _not analysed_ |
| FocusSettingsUI | TIER_2 | 2 | — | _not analysed_ |
| FocusUI | TIER_2 | 2 | — | _not analysed_ |
| FontInstallViewService | TIER_2 | 2 | — | _not analysed_ |
| FreeformDataclassOwner | TIER_2 | 2 | — | _not analysed_ |
| FrontBoard | TIER_2 | 2 | — | _not analysed_ |
| FrontBoardServices | TIER_2 | 2 | — | _not analysed_ |
| GAXBackboardServer | TIER_2 | 2 | — | _not analysed_ |
| GAXSpringboardServer | TIER_2 | 2 | — | _not analysed_ |
| GCoreFramework | TIER_2 | 2 | — | _not analysed_ |
| GNSSPassthroughLib | TIER_2 | 2 | — | _not analysed_ |
| GPUTools | TIER_2 | 2 | — | _not analysed_ |
| GPUToolsCapture | TIER_2 | 2 | — | _not analysed_ |
| GPUToolsCore | TIER_2 | 2 | — | _not analysed_ |
| GPUToolsDiagnostics | TIER_2 | 2 | — | _not analysed_ |
| GPUToolsPlayback | TIER_2 | 2 | — | _not analysed_ |
| GPUToolsTransport | TIER_2 | 2 | — | _not analysed_ |
| GRDBInternal | TIER_2 | 2 | — | _not analysed_ |
| GSSCred | TIER_2 | 2 | — | _not analysed_ |
| GameCenterOverlayService | TIER_2 | 2 | — | _not analysed_ |
| GameCenterUI | TIER_2 | 2 | — | _not analysed_ |
| GameCenterUICore | TIER_2 | 2 | — | _not analysed_ |
| GameControllerFoundation | TIER_2 | 2 | — | _not analysed_ |
| GameKit | TIER_2 | 2 | — | _not analysed_ |
| GameKitServices | TIER_2 | 2 | — | _not analysed_ |
| GamePolicy | TIER_2 | 2 | — | _not analysed_ |
| GameServices | TIER_2 | 2 | — | _not analysed_ |
| GameServicesCore | TIER_2 | 2 | — | _not analysed_ |
| GamepadHIDServiceFilter | TIER_2 | 2 | — | _not analysed_ |
| GeneralSettingsUI | TIER_2 | 2 | — | _not analysed_ |
| GenerativeAssistantActions | TIER_2 | 2 | — | _not analysed_ |
| GenerativeAssistantCommon | TIER_2 | 2 | — | _not analysed_ |
| GenerativeAssistantEnablementFlow | TIER_2 | 2 | — | _not analysed_ |
| GenerativeAssistantEnablementFlowPlugin | TIER_2 | 2 | — | _not analysed_ |
| GenerativeAssistantUI | TIER_2 | 2 | — | _not analysed_ |
| GenerativeExperiencesRuntime | TIER_2 | 2 | — | _not analysed_ |
| GenerativeFunctionsFoundation | TIER_2 | 2 | — | _not analysed_ |
| GenerativeFunctionsInstrumentation | TIER_2 | 2 | — | _not analysed_ |
| GenerativeModels | TIER_2 | 2 | — | _not analysed_ |
| GenericKextUpdaterService | TIER_2 | 2 | — | _not analysed_ |
| GeoAnalytics | TIER_2 | 2 | — | _not analysed_ |
| GeoFlowDelegatePlugin | TIER_2 | 2 | — | _not analysed_ |
| GeoServicesCore | TIER_2 | 2 | — | _not analysed_ |
| Geometry | TIER_2 | 2 | — | _not analysed_ |
| GeometryCompression | TIER_2 | 2 | — | _not analysed_ |
| GraphVisualizer | TIER_2 | 2 | — | _not analysed_ |
| GroupActivities | TIER_2 | 2 | — | _not analysed_ |
| GuidedAccess | TIER_2 | 2 | — | _not analysed_ |
| H16ISP.mediacapture | TIER_2 | 2 | — | _not analysed_ |
| HDSViewService | TIER_2 | 2 | — | _not analysed_ |
| HID | TIER_2 | 2 | — | _not analysed_ |
| HIDRMClientKit | TIER_2 | 2 | — | _not analysed_ |
| HIDRMKit | TIER_2 | 2 | — | _not analysed_ |
| HIDRMUI | TIER_2 | 2 | — | _not analysed_ |
| HMFoundation | TIER_2 | 2 | — | _not analysed_ |
| HSTouchHIDService | TIER_2 | 2 | — | _not analysed_ |
| Hands | TIER_2 | 2 | — | _not analysed_ |
| HangTracer | TIER_2 | 2 | — | _not analysed_ |
| HeadphoneManager | TIER_2 | 2 | — | _not analysed_ |
| HeadphoneProxService | TIER_2 | 2 | — | _not analysed_ |
| Health | TIER_2 | 2 | — | _not analysed_ |
| HealthAlgorithms | TIER_2 | 2 | — | _not analysed_ |
| HealthAppServices | TIER_2 | 2 | — | _not analysed_ |
| HealthArticles | TIER_2 | 2 | — | _not analysed_ |
| HealthArticlesGeneration | TIER_2 | 2 | — | _not analysed_ |
| HealthArticlesUI | TIER_2 | 2 | — | _not analysed_ |
| HealthBalanceAppPlugin | TIER_2 | 2 | — | _not analysed_ |
| HealthBalanceAppPluginBundle | TIER_2 | 2 | — | _not analysed_ |
| HealthBalanceDaemon | TIER_2 | 2 | — | _not analysed_ |
| HealthDaemonFoundation | TIER_2 | 2 | — | _not analysed_ |
| HealthDiagnosticExtensionCore | TIER_2 | 2 | — | _not analysed_ |
| HealthENBuddy | TIER_2 | 2 | — | _not analysed_ |
| HealthENLauncher | TIER_2 | 2 | — | _not analysed_ |
| HealthExperience | TIER_2 | 2 | — | _not analysed_ |
| HealthExperienceUI | TIER_2 | 2 | — | _not analysed_ |
| HealthFeaturesBridgeSetupPlugin | TIER_2 | 2 | — | _not analysed_ |
| HealthMedicationsExperience | TIER_2 | 2 | — | _not analysed_ |
| HealthMedicationsUI | TIER_2 | 2 | — | _not analysed_ |
| HealthMedicationsVisionUI | TIER_2 | 2 | — | _not analysed_ |
| HealthMedicationsWidgetUI | TIER_2 | 2 | — | _not analysed_ |
| HealthMobility | TIER_2 | 2 | — | _not analysed_ |
| HealthMobilityUI | TIER_2 | 2 | — | _not analysed_ |
| HealthOrchestration | TIER_2 | 2 | — | _not analysed_ |
| HealthPlatform | TIER_2 | 2 | — | _not analysed_ |
| HealthPlatformCore | TIER_2 | 2 | — | _not analysed_ |
| HealthPluginHost | TIER_2 | 2 | — | _not analysed_ |
| HealthPrivacyService | TIER_2 | 2 | — | _not analysed_ |
| HealthPrivacySettings | TIER_2 | 2 | — | _not analysed_ |
| HealthRecordServices | TIER_2 | 2 | — | _not analysed_ |
| HealthRecords | TIER_2 | 2 | — | _not analysed_ |
| HealthRecordsDaemon | TIER_2 | 2 | — | _not analysed_ |
| HealthRecordsExtraction | TIER_2 | 2 | — | _not analysed_ |
| HealthRecordsPlugin | TIER_2 | 2 | — | _not analysed_ |
| HealthRecordsUI | TIER_2 | 2 | — | _not analysed_ |
| HealthSettings | TIER_2 | 2 | — | _not analysed_ |
| HealthToolbox | TIER_2 | 2 | — | _not analysed_ |
| HealthUI | TIER_2 | 2 | — | _not analysed_ |
| HealthVisualization | TIER_2 | 2 | — | _not analysed_ |
| HearingAppPlugin | TIER_2 | 2 | — | _not analysed_ |
| HearingCore | TIER_2 | 2 | — | _not analysed_ |
| HearingMLHelperService | TIER_2 | 2 | — | _not analysed_ |
| HearingModeService | TIER_2 | 2 | — | _not analysed_ |
| HearingModeSettingsUI | TIER_2 | 2 | — | _not analysed_ |
| HearingTestUI | TIER_2 | 2 | — | _not analysed_ |
| HearingUI | TIER_2 | 2 | — | _not analysed_ |
| HearingUtilities | TIER_2 | 2 | — | _not analysed_ |
| Heart | TIER_2 | 2 | — | _not analysed_ |
| HeartHealth | TIER_2 | 2 | — | _not analysed_ |
| HeartHealthDaemon | TIER_2 | 2 | — | _not analysed_ |
| HeuristicInterpreter | TIER_2 | 2 | — | _not analysed_ |
| HighlightAlerts | TIER_2 | 2 | — | _not analysed_ |
| Highlights | TIER_2 | 2 | — | _not analysed_ |
| Home | TIER_2 | 2 | — | _not analysed_ |
| HomeAccessoryControlUI | TIER_2 | 2 | — | _not analysed_ |
| HomeAppIntents | TIER_2 | 2 | — | _not analysed_ |
| HomeAutomationFlowDelegatePlugin | TIER_2 | 2 | — | _not analysed_ |
| HomeAutomationInternal | TIER_2 | 2 | — | _not analysed_ |
| HomeAutomationSiriSuggestions | TIER_2 | 2 | — | _not analysed_ |
| HomeControlCenterModule | TIER_2 | 2 | — | _not analysed_ |
| HomeControlCenterSingleTileModule | TIER_2 | 2 | — | _not analysed_ |
| HomeDataModel | TIER_2 | 2 | — | _not analysed_ |
| HomeDeviceSetup | TIER_2 | 2 | — | _not analysed_ |
| HomeEnergyUI | TIER_2 | 2 | — | _not analysed_ |
| HomeKitBackingStore | TIER_2 | 2 | — | _not analysed_ |
| HomeKitDaemonFoundation | TIER_2 | 2 | — | _not analysed_ |
| HomeKitEvents | TIER_2 | 2 | — | _not analysed_ |
| HomeKitMatter | TIER_2 | 2 | — | _not analysed_ |
| HomeKitMetrics | TIER_2 | 2 | — | _not analysed_ |
| HomePodSettings | TIER_2 | 2 | — | _not analysed_ |
| HomeServices | TIER_2 | 2 | — | _not analysed_ |
| HomeSettings | TIER_2 | 2 | — | _not analysed_ |
| HomeUI | TIER_2 | 2 | — | _not analysed_ |
| HomeUI2 | TIER_2 | 2 | — | _not analysed_ |
| HoverTextUI | TIER_2 | 2 | — | _not analysed_ |
| IDS | TIER_2 | 2 | — | _not analysed_ |
| IDSBlastDoorService | TIER_2 | 2 | — | _not analysed_ |
| IDSCredentialsAgent | TIER_2 | 2 | — | _not analysed_ |
| IDSRemoteURLConnectionAgent | TIER_2 | 2 | — | _not analysed_ |
| IFFlowPlugin | TIER_2 | 2 | — | _not analysed_ |
| IMAVCore | TIER_2 | 2 | — | _not analysed_ |
| IMCore | TIER_2 | 2 | — | _not analysed_ |
| IMDMessageServicesAgent | TIER_2 | 2 | — | _not analysed_ |
| IMDebug | TIER_2 | 2 | — | _not analysed_ |
| IMRCSTransfer | TIER_2 | 2 | — | _not analysed_ |
| IMSharedUtilities | TIER_2 | 2 | — | _not analysed_ |
| IMTranscoderAgent | TIER_2 | 2 | — | _not analysed_ |
| IMTransferAgent | TIER_2 | 2 | — | _not analysed_ |
| IMTransferAgentClient | TIER_2 | 2 | — | _not analysed_ |
| IMTransferServices | TIER_2 | 2 | — | _not analysed_ |
| IO80211 | TIER_2 | 2 | — | _not analysed_ |
| IOAccelMemoryInfo | TIER_2 | 2 | — | _not analysed_ |
| IOAccessoryManager | TIER_2 | 2 | — | _not analysed_ |
| IOGameControllerFamily | TIER_2 | 2 | — | _not analysed_ |
| IOHIDEventProcessorFilter | TIER_2 | 2 | — | _not analysed_ |
| IOHIDEventServicePlugin | TIER_2 | 2 | — | _not analysed_ |
| IOHIDEventSystemStatistics | TIER_2 | 2 | — | _not analysed_ |
| IOHIDKeyboardFilter | TIER_2 | 2 | — | _not analysed_ |
| IOHIDLib | TIER_2 | 2 | — | _not analysed_ |
| IOHIDT8027USBSessionFilter | TIER_2 | 2 | — | _not analysed_ |
| IOKitten | TIER_2 | 2 | — | _not analysed_ |
| IOMFB_FDR_Loader | TIER_2 | 2 | — | _not analysed_ |
| IOMobileFramebuffer | TIER_2 | 2 | — | _not analysed_ |
| IOSurface | TIER_2 | 2 | — | _not analysed_ |
| IOUSBHost | TIER_2 | 2 | — | _not analysed_ |
| IOUSBLib | TIER_2 | 2 | — | _not analysed_ |
| IPConfiguration | TIER_2 | 2 | — | _not analysed_ |
| ISPExclaveKitServices | TIER_2 | 2 | — | _not analysed_ |
| IconServices | TIER_2 | 2 | — | _not analysed_ |
| Image Playground | TIER_2 | 2 | — | _not analysed_ |
| ImagePlayground | TIER_2 | 2 | — | _not analysed_ |
| InCallService | TIER_2 | 2 | — | _not analysed_ |
| InfoQueryPersonalizationFeatures | TIER_2 | 2 | — | _not analysed_ |
| InformationFlowPlugin | TIER_2 | 2 | — | _not analysed_ |
| InputAccessoriesSettings | TIER_2 | 2 | — | _not analysed_ |
| InputAnalytics | TIER_2 | 2 | — | _not analysed_ |
| InputAnalyticsServer | TIER_2 | 2 | — | _not analysed_ |
| IntelligenceEngine | TIER_2 | 2 | — | _not analysed_ |
| IntelligenceFlow | TIER_2 | 2 | — | _not analysed_ |
| IntelligenceFlowContextRuntime | TIER_2 | 2 | — | _not analysed_ |
| IntelligenceFlowPlannerRuntime | TIER_2 | 2 | — | _not analysed_ |
| IntelligenceFlowPlannerSupport | TIER_2 | 2 | — | _not analysed_ |
| IntelligenceFlowRuntime | TIER_2 | 2 | — | _not analysed_ |
| IntelligencePlatform | TIER_2 | 2 | — | _not analysed_ |
| IntelligencePlatformCore | TIER_2 | 2 | — | _not analysed_ |
| IntelligentRouting | TIER_2 | 2 | — | _not analysed_ |
| IntelligentRoutingDaemon | TIER_2 | 2 | — | _not analysed_ |
| Intents | TIER_2 | 2 | — | _not analysed_ |
| IntentsCore | TIER_2 | 2 | — | _not analysed_ |
| JSApp | TIER_2 | 2 | — | _not analysed_ |
| JetCore | TIER_2 | 2 | — | _not analysed_ |
| JetEngine | TIER_2 | 2 | — | _not analysed_ |
| JetPack | TIER_2 | 2 | — | _not analysed_ |
| JetUI | TIER_2 | 2 | — | _not analysed_ |
| JoinRequests | TIER_2 | 2 | — | _not analysed_ |
| Journal | TIER_2 | 2 | — | _not analysed_ |
| JournalDataclassOwner | TIER_2 | 2 | — | _not analysed_ |
| JournalSettings | TIER_2 | 2 | — | _not analysed_ |
| JournalShared | TIER_2 | 2 | — | _not analysed_ |
| JournalingSuggestions | TIER_2 | 2 | — | _not analysed_ |
| KnowledgeMonitor | TIER_2 | 2 | — | _not analysed_ |
| KoaMapper | TIER_2 | 2 | — | _not analysed_ |
| LLMCache | TIER_2 | 2 | — | _not analysed_ |
| LearnedFeatures | TIER_2 | 2 | — | _not analysed_ |
| LegalAndRegulatorySettingsSupport | TIER_2 | 2 | — | _not analysed_ |
| Lexicon | TIER_2 | 2 | — | _not analysed_ |
| LightweightCodeRequirements | TIER_2 | 2 | — | _not analysed_ |
| LimitAdTracking | TIER_2 | 2 | — | _not analysed_ |
| LimitedAccessPromptView | TIER_2 | 2 | — | _not analysed_ |
| LinkMetadata | TIER_2 | 2 | — | _not analysed_ |
| LinkPresentation | TIER_2 | 2 | — | _not analysed_ |
| LinkPresentationStyleSheetParsing | TIER_2 | 2 | — | _not analysed_ |
| LiveCommunicationKit | TIER_2 | 2 | — | _not analysed_ |
| LiveFS | TIER_2 | 2 | — | _not analysed_ |
| LiveTranscription | TIER_2 | 2 | — | _not analysed_ |
| LocalSpeechRecognitionBridge | TIER_2 | 2 | — | _not analysed_ |
| LocalStatusKit | TIER_2 | 2 | — | _not analysed_ |
| LocationSupport | TIER_2 | 2 | — | _not analysed_ |
| LockedCameraCapture | TIER_2 | 2 | — | _not analysed_ |
| LockedContentServices | TIER_2 | 2 | — | _not analysed_ |
| LoggingSupport | TIER_2 | 2 | — | _not analysed_ |
| LowPowerMode | TIER_2 | 2 | — | _not analysed_ |
| MCCFoundation | TIER_2 | 2 | — | _not analysed_ |
| MCCKitCategorization | TIER_2 | 2 | — | _not analysed_ |
| MDM | TIER_2 | 2 | — | _not analysed_ |
| MDMClientLibrary | TIER_2 | 2 | — | _not analysed_ |
| MIL | TIER_2 | 2 | — | _not analysed_ |
| MIME | TIER_2 | 2 | — | _not analysed_ |
| MLAssetIO | TIER_2 | 2 | — | _not analysed_ |
| MLRuntime | TIER_2 | 2 | — | _not analysed_ |
| MOVStreamIO | TIER_2 | 2 | — | _not analysed_ |
| MPSBenchmarkLoop | TIER_2 | 2 | — | _not analysed_ |
| MPSNDArray | TIER_2 | 2 | — | _not analysed_ |
| MPUFoundation | TIER_2 | 2 | — | _not analysed_ |
| MSMessageExtensionBalloonPlugin | TIER_2 | 2 | — | _not analysed_ |
| MSUEarlyBootTask | TIER_2 | 2 | — | _not analysed_ |
| MTLCompiler | TIER_2 | 2 | — | _not analysed_ |
| MTLCompilerService | TIER_2 | 2 | — | _not analysed_ |
| MTLReplayer | TIER_2 | 2 | — | _not analysed_ |
| MagnifierSupport | TIER_2 | 2 | — | _not analysed_ |
| MailCompositionService | TIER_2 | 2 | — | _not analysed_ |
| MailKit | TIER_2 | 2 | — | _not analysed_ |
| MailSupport | TIER_2 | 2 | — | _not analysed_ |
| MallocStackLogging | TIER_2 | 2 | — | _not analysed_ |
| ManagedAppDistribution | TIER_2 | 2 | — | _not analysed_ |
| ManagedAppsCore | TIER_2 | 2 | — | _not analysed_ |
| ManagedAppsInterface | TIER_2 | 2 | — | _not analysed_ |
| ManagedAppsSubscriber | TIER_2 | 2 | — | _not analysed_ |
| ManagedConfiguration | TIER_2 | 2 | — | _not analysed_ |
| ManagedConfigurationUEA | TIER_2 | 2 | — | _not analysed_ |
| ManagedConfigurationUI | TIER_2 | 2 | — | _not analysed_ |
| ManagedSettingsAgent | TIER_2 | 2 | — | _not analysed_ |
| ManagedSettingsObjC | TIER_2 | 2 | — | _not analysed_ |
| ManagedSettingsSupport | TIER_2 | 2 | — | _not analysed_ |
| MapKit | TIER_2 | 2 | — | _not analysed_ |
| MapsSettings | TIER_2 | 2 | — | _not analysed_ |
| MapsSuggestions | TIER_2 | 2 | — | _not analysed_ |
| MapsSupport | TIER_2 | 2 | — | _not analysed_ |
| MapsSync | TIER_2 | 2 | — | _not analysed_ |
| MapsUI | TIER_2 | 2 | — | _not analysed_ |
| MarketplaceKit | TIER_2 | 2 | — | _not analysed_ |
| MarkupUI | TIER_2 | 2 | — | _not analysed_ |
| Marrs | TIER_2 | 2 | — | _not analysed_ |
| MathTypesetting | TIER_2 | 2 | — | _not analysed_ |
| Matter | TIER_2 | 2 | — | _not analysed_ |
| MatterPlugin | TIER_2 | 2 | — | _not analysed_ |
| MatterSupport | TIER_2 | 2 | — | _not analysed_ |
| MechPasscode | TIER_2 | 2 | — | _not analysed_ |
| MechPearl | TIER_2 | 2 | — | _not analysed_ |
| MechPushButton | TIER_2 | 2 | — | _not analysed_ |
| MechTouchId | TIER_2 | 2 | — | _not analysed_ |
| MechanismBase | TIER_2 | 2 | — | _not analysed_ |
| Media | TIER_2 | 2 | — | _not analysed_ |
| MediaAnalysisServices | TIER_2 | 2 | — | _not analysed_ |
| MediaControl | TIER_2 | 2 | — | _not analysed_ |
| MediaControls | TIER_2 | 2 | — | _not analysed_ |
| MediaConversionService | TIER_2 | 2 | — | _not analysed_ |
| MediaCoreUI | TIER_2 | 2 | — | _not analysed_ |
| MediaLibraryCore | TIER_2 | 2 | — | _not analysed_ |
| MediaMiningKit | TIER_2 | 2 | — | _not analysed_ |
| MediaPlaybackCore | TIER_2 | 2 | — | _not analysed_ |
| MediaRemoteUI | TIER_2 | 2 | — | _not analysed_ |
| MediaRemoteUIService | TIER_2 | 2 | — | _not analysed_ |
| MediaServices | TIER_2 | 2 | — | _not analysed_ |
| MediaToolbox | TIER_2 | 2 | — | _not analysed_ |
| MedicalIDUI | TIER_2 | 2 | — | _not analysed_ |
| MedicationsHealthAppPlugin | TIER_2 | 2 | — | _not analysed_ |
| MenstrualAlgorithmsInternal | TIER_2 | 2 | — | _not analysed_ |
| MenstrualCyclesAppPlugin | TIER_2 | 2 | — | _not analysed_ |
| MentalHealthAppPlugin | TIER_2 | 2 | — | _not analysed_ |
| MentalHealthDaemon | TIER_2 | 2 | — | _not analysed_ |
| MergeBuddyProvisioningResponse | TIER_2 | 2 | — | _not analysed_ |
| MessageLegacy | TIER_2 | 2 | — | _not analysed_ |
| MessageProtection | TIER_2 | 2 | — | _not analysed_ |
| MessageUI | TIER_2 | 2 | — | _not analysed_ |
| Messages | TIER_2 | 2 | — | _not analysed_ |
| MessagesBlastDoorService | TIER_2 | 2 | — | _not analysed_ |
| MessagesCloudSync | TIER_2 | 2 | — | _not analysed_ |
| MessagesComplication | TIER_2 | 2 | — | _not analysed_ |
| MessagesFlowDelegatePlugin | TIER_2 | 2 | — | _not analysed_ |
| MessagesSupport | TIER_2 | 2 | — | _not analysed_ |
| MessagesUIPlugin | TIER_2 | 2 | — | _not analysed_ |
| MetadataUtilities | TIER_2 | 2 | — | _not analysed_ |
| Metal | TIER_2 | 2 | — | _not analysed_ |
| MetalFX | TIER_2 | 2 | — | _not analysed_ |
| MetricKitCore | TIER_2 | 2 | — | _not analysed_ |
| MetricKitServices | TIER_2 | 2 | — | _not analysed_ |
| MetricKitSource | TIER_2 | 2 | — | _not analysed_ |
| MetricMeasurement | TIER_2 | 2 | — | _not analysed_ |
| MicroLocation | TIER_2 | 2 | — | _not analysed_ |
| MicroLocationUtilities | TIER_2 | 2 | — | _not analysed_ |
| MindSettings | TIER_2 | 2 | — | _not analysed_ |
| MobileAccessoryUpdater | TIER_2 | 2 | — | _not analysed_ |
| MobileAsset | TIER_2 | 2 | — | _not analysed_ |
| MobileAssetExclaveServices | TIER_2 | 2 | — | _not analysed_ |
| MobileBackup | TIER_2 | 2 | — | _not analysed_ |
| MobileBackupUEA | TIER_2 | 2 | — | _not analysed_ |
| MobileCal | TIER_2 | 2 | — | _not analysed_ |
| MobileInBoxUpdate | TIER_2 | 2 | — | _not analysed_ |
| MobileInstallation | TIER_2 | 2 | — | _not analysed_ |
| MobileKeyBag | TIER_2 | 2 | — | _not analysed_ |
| MobileKeyBagLockState | TIER_2 | 2 | — | _not analysed_ |
| MobileMailSettings | TIER_2 | 2 | — | _not analysed_ |
| MobileMulticastTransfer | TIER_2 | 2 | — | _not analysed_ |
| MobileNotes | TIER_2 | 2 | — | _not analysed_ |
| MobileObliteration | TIER_2 | 2 | — | _not analysed_ |
| MobilePhone | TIER_2 | 2 | — | _not analysed_ |
| MobilePhoneSettings | TIER_2 | 2 | — | _not analysed_ |
| MobileSafari | TIER_2 | 2 | — | _not analysed_ |
| MobileSafariSettings | TIER_2 | 2 | — | _not analysed_ |
| MobileSafariUI | TIER_2 | 2 | — | _not analysed_ |
| MobileStorage | TIER_2 | 2 | — | _not analysed_ |
| MobileStoreDemoKit | TIER_2 | 2 | — | _not analysed_ |
| MobileStoreSettings | TIER_2 | 2 | — | _not analysed_ |
| MobileStoreUI | TIER_2 | 2 | — | _not analysed_ |
| MobileTimer | TIER_2 | 2 | — | _not analysed_ |
| MobileTimerSupport | TIER_2 | 2 | — | _not analysed_ |
| MobileWiFi | TIER_2 | 2 | — | _not analysed_ |
| MobilityAppPlugin | TIER_2 | 2 | — | _not analysed_ |
| ModelManagerServices | TIER_2 | 2 | — | _not analysed_ |
| ModuleBase | TIER_2 | 2 | — | _not analysed_ |
| Moments | TIER_2 | 2 | — | _not analysed_ |
| MomentsIntelligence | TIER_2 | 2 | — | _not analysed_ |
| MomentsIntelligenceService | TIER_2 | 2 | — | _not analysed_ |
| MomentsOnboardingAndSettings | TIER_2 | 2 | — | _not analysed_ |
| MomentsUIService | TIER_2 | 2 | — | _not analysed_ |
| Morpheus | TIER_2 | 2 | — | _not analysed_ |
| MorpheusExtensions | TIER_2 | 2 | — | _not analysed_ |
| MultitaskingAndGesturesSettings | TIER_2 | 2 | — | _not analysed_ |
| MultitouchHID | TIER_2 | 2 | — | _not analysed_ |
| Music | TIER_2 | 2 | — | _not analysed_ |
| MusicApplication | TIER_2 | 2 | — | _not analysed_ |
| MusicCarDisplayUI | TIER_2 | 2 | — | _not analysed_ |
| MusicKit | TIER_2 | 2 | — | _not analysed_ |
| MusicLibrary | TIER_2 | 2 | — | _not analysed_ |
| MusicRecognition | TIER_2 | 2 | — | _not analysed_ |
| MusicScriptUpdateService | TIER_2 | 2 | — | _not analysed_ |
| MusicSettings | TIER_2 | 2 | — | _not analysed_ |
| MusicUI | TIER_2 | 2 | — | _not analysed_ |
| MusicUIService | TIER_2 | 2 | — | _not analysed_ |
| NANDTaskScheduler | TIER_2 | 2 | — | _not analysed_ |
| NCLaunchStats | TIER_2 | 2 | — | _not analysed_ |
| NDOUI | TIER_2 | 2 | — | _not analysed_ |
| NFUIService | TIER_2 | 2 | — | _not analysed_ |
| NLP | TIER_2 | 2 | — | _not analysed_ |
| NPKCompanionAgent | TIER_2 | 2 | — | _not analysed_ |
| NPTKit | TIER_2 | 2 | — | _not analysed_ |
| NTKCustomization | TIER_2 | 2 | — | _not analysed_ |
| NanoClockBridgeSettings | TIER_2 | 2 | — | _not analysed_ |
| NanoClockBridgeSettingsPreferencesSyncCompanion | TIER_2 | 2 | — | _not analysed_ |
| NanoCompassComplications | TIER_2 | 2 | — | _not analysed_ |
| NanoHealthBalanceBridgeSettings | TIER_2 | 2 | — | _not analysed_ |
| NanoLeash | TIER_2 | 2 | — | _not analysed_ |
| NanoMailCompanionUI | TIER_2 | 2 | — | _not analysed_ |
| NanoMediaRemote | TIER_2 | 2 | — | _not analysed_ |
| NanoMenstrualCyclesCompanionSettings | TIER_2 | 2 | — | _not analysed_ |
| NanoMusicSync | TIER_2 | 2 | — | _not analysed_ |
| NanoPassKit | TIER_2 | 2 | — | _not analysed_ |
| NanoPassbookBridgeSettings | TIER_2 | 2 | — | _not analysed_ |
| NanoPreferencesSync | TIER_2 | 2 | — | _not analysed_ |
| NanoRegistry | TIER_2 | 2 | — | _not analysed_ |
| NanoResourceGrabber | TIER_2 | 2 | — | _not analysed_ |
| NanoSleepBridgeSetup | TIER_2 | 2 | — | _not analysed_ |
| NanoSleepComplication | TIER_2 | 2 | — | _not analysed_ |
| NanoSystemSettings | TIER_2 | 2 | — | _not analysed_ |
| NanoTimeKit | TIER_2 | 2 | — | _not analysed_ |
| NanoUniverse | TIER_2 | 2 | — | _not analysed_ |
| NanoWeatherComplicationsCompanion | TIER_2 | 2 | — | _not analysed_ |
| NanoWeatherKitUICompanion | TIER_2 | 2 | — | _not analysed_ |
| NaturalLanguage | TIER_2 | 2 | — | _not analysed_ |
| Navigation | TIER_2 | 2 | — | _not analysed_ |
| NearField | TIER_2 | 2 | — | _not analysed_ |
| NearFieldAccessory | TIER_2 | 2 | — | _not analysed_ |
| NearFieldPrivateServices | TIER_2 | 2 | — | _not analysed_ |
| NearbyInteraction | TIER_2 | 2 | — | _not analysed_ |
| NeighborhoodActivityConduit | TIER_2 | 2 | — | _not analysed_ |
| NetAppsUtilitiesUI | TIER_2 | 2 | — | _not analysed_ |
| Netrb | TIER_2 | 2 | — | _not analysed_ |
| NetworkRelay | TIER_2 | 2 | — | _not analysed_ |
| NetworkServiceProxy | TIER_2 | 2 | — | _not analysed_ |
| NeuralNetworks | TIER_2 | 2 | — | _not analysed_ |
| NotesEditor | TIER_2 | 2 | — | _not analysed_ |
| NotesSettings | TIER_2 | 2 | — | _not analysed_ |
| NotesShared | TIER_2 | 2 | — | _not analysed_ |
| NotesSiriUI | TIER_2 | 2 | — | _not analysed_ |
| NotesSupport | TIER_2 | 2 | — | _not analysed_ |
| NotesUI | TIER_2 | 2 | — | _not analysed_ |
| NowPlayingUI | TIER_2 | 2 | — | _not analysed_ |
| OSASubmissionClient | TIER_2 | 2 | — | _not analysed_ |
| OSAnalytics | TIER_2 | 2 | — | _not analysed_ |
| OSEligibility | TIER_2 | 2 | — | _not analysed_ |
| OSIntelligence | TIER_2 | 2 | — | _not analysed_ |
| OTACrashCopier | TIER_2 | 2 | — | _not analysed_ |
| OctagonTrust | TIER_2 | 2 | — | _not analysed_ |
| OfficeImport | TIER_2 | 2 | — | _not analysed_ |
| OmniSearch | TIER_2 | 2 | — | _not analysed_ |
| OmniSearchTypes | TIER_2 | 2 | — | _not analysed_ |
| OnDeviceStorage | TIER_2 | 2 | — | _not analysed_ |
| OnDeviceStorageInternal | TIER_2 | 2 | — | _not analysed_ |
| OxygenSaturationSettings | TIER_2 | 2 | — | _not analysed_ |
| PASViewService | TIER_2 | 2 | — | _not analysed_ |
| PBBridgeSupport | TIER_2 | 2 | — | _not analysed_ |
| PCViewService | TIER_2 | 2 | — | _not analysed_ |
| PacketFilter | TIER_2 | 2 | — | _not analysed_ |
| PairedDeviceRegistry | TIER_2 | 2 | — | _not analysed_ |
| PairedUnlockSettings | TIER_2 | 2 | — | _not analysed_ |
| ParavirtualizedANE | TIER_2 | 2 | — | _not analysed_ |
| PassKitCore | TIER_2 | 2 | — | _not analysed_ |
| PassKitUIFoundation | TIER_2 | 2 | — | _not analysed_ |
| Passbook | TIER_2 | 2 | — | _not analysed_ |
| PassbookSettings | TIER_2 | 2 | — | _not analysed_ |
| PassesLockScreenPlugin | TIER_2 | 2 | — | _not analysed_ |
| PasswordManagerUI | TIER_2 | 2 | — | _not analysed_ |
| Passwords | TIER_2 | 2 | — | _not analysed_ |
| PasswordsSettings | TIER_2 | 2 | — | _not analysed_ |
| Pasteboard | TIER_2 | 2 | — | _not analysed_ |
| PaymentUIBase | TIER_2 | 2 | — | _not analysed_ |
| PaymentsFlowDelegatePlugin | TIER_2 | 2 | — | _not analysed_ |
| Pegasus | TIER_2 | 2 | — | _not analysed_ |
| PegasusAPI | TIER_2 | 2 | — | _not analysed_ |
| PegasusConfiguration | TIER_2 | 2 | — | _not analysed_ |
| PegasusKit | TIER_2 | 2 | — | _not analysed_ |
| PencilKit | TIER_2 | 2 | — | _not analysed_ |
| People | TIER_2 | 2 | — | _not analysed_ |
| PeopleMessageService | TIER_2 | 2 | — | _not analysed_ |
| PeopleSuggester | TIER_2 | 2 | — | _not analysed_ |
| PeopleUI | TIER_2 | 2 | — | _not analysed_ |
| PeopleViewService | TIER_2 | 2 | — | _not analysed_ |
| PerfPowerServicesMetadata | TIER_2 | 2 | — | _not analysed_ |
| PerfPowerServicesReader | TIER_2 | 2 | — | _not analysed_ |
| PerformanceControlKit | TIER_2 | 2 | — | _not analysed_ |
| PerformanceTrace | TIER_2 | 2 | — | _not analysed_ |
| PeridotDepth | TIER_2 | 2 | — | _not analysed_ |
| PersonalizationPortrait | TIER_2 | 2 | — | _not analysed_ |
| PersonalizationPortraitInternals | TIER_2 | 2 | — | _not analysed_ |
| PersonalizedSensing | TIER_2 | 2 | — | _not analysed_ |
| PersonalizedSensingService | TIER_2 | 2 | — | _not analysed_ |
| PhotoFoundation | TIER_2 | 2 | — | _not analysed_ |
| PhotoImaging | TIER_2 | 2 | — | _not analysed_ |
| Photos | TIER_2 | 2 | — | _not analysed_ |
| PhotosFace | TIER_2 | 2 | — | _not analysed_ |
| PhotosFormats | TIER_2 | 2 | — | _not analysed_ |
| PhotosIntelligence | TIER_2 | 2 | — | _not analysed_ |
| PhotosIntelligenceCore | TIER_2 | 2 | — | _not analysed_ |
| PhotosPlayer | TIER_2 | 2 | — | _not analysed_ |
| PhotosSwiftUICore | TIER_2 | 2 | — | _not analysed_ |
| PhotosUI | TIER_2 | 2 | — | _not analysed_ |
| PhotosUIEdit | TIER_2 | 2 | — | _not analysed_ |
| PhotosUIPrivate | TIER_2 | 2 | — | _not analysed_ |
| PhotosensitivityProcessing | TIER_2 | 2 | — | _not analysed_ |
| PlatformSSOCore | TIER_2 | 2 | — | _not analysed_ |
| Plugins | TIER_2 | 2 | — | _not analysed_ |
| Podcasts | TIER_2 | 2 | — | _not analysed_ |
| PodcastsFoundation | TIER_2 | 2 | — | _not analysed_ |
| PodcastsKit | TIER_2 | 2 | — | _not analysed_ |
| PodcastsSettingsPlugin | TIER_2 | 2 | — | _not analysed_ |
| PodcastsTranscripts | TIER_2 | 2 | — | _not analysed_ |
| PodcastsUI | TIER_2 | 2 | — | _not analysed_ |
| PodcastsUsagePlugin | TIER_2 | 2 | — | _not analysed_ |
| Portrait | TIER_2 | 2 | — | _not analysed_ |
| PosterBoard | TIER_2 | 2 | — | _not analysed_ |
| PosterBoardUIServices | TIER_2 | 2 | — | _not analysed_ |
| PosterKit | TIER_2 | 2 | — | _not analysed_ |
| PosterPlatformSupportBundleService | TIER_2 | 2 | — | _not analysed_ |
| PowerLog | TIER_2 | 2 | — | _not analysed_ |
| PowerUI | TIER_2 | 2 | — | _not analysed_ |
| PowerlogCore | TIER_2 | 2 | — | _not analysed_ |
| PowerlogHelperdOperators | TIER_2 | 2 | — | _not analysed_ |
| PowerlogLiteOperators | TIER_2 | 2 | — | _not analysed_ |
| PreBoard | TIER_2 | 2 | — | _not analysed_ |
| PreboardService | TIER_2 | 2 | — | _not analysed_ |
| Preferences | TIER_2 | 2 | — | _not analysed_ |
| PreviewsFoundationOS | TIER_2 | 2 | — | _not analysed_ |
| PreviewsOSSupport | TIER_2 | 2 | — | _not analysed_ |
| PrimaryCloudCallingSettingsBundle | TIER_2 | 2 | — | _not analysed_ |
| Print Center | TIER_2 | 2 | — | _not analysed_ |
| PrintKitUI | TIER_2 | 2 | — | _not analysed_ |
| PrivacyAndSecuritySettings | TIER_2 | 2 | — | _not analysed_ |
| PrivacySettingsUI | TIER_2 | 2 | — | _not analysed_ |
| PrivateCloudCompute | TIER_2 | 2 | — | _not analysed_ |
| PrivateFederatedLearning | TIER_2 | 2 | — | _not analysed_ |
| PrivateMLClient | TIER_2 | 2 | — | _not analysed_ |
| PrivateMLClientInferenceProvider | TIER_2 | 2 | — | _not analysed_ |
| ProVideo | TIER_2 | 2 | — | _not analysed_ |
| ProactiveBlendingLayer_iOS | TIER_2 | 2 | — | _not analysed_ |
| ProactiveCDNDownloader | TIER_2 | 2 | — | _not analysed_ |
| ProactiveContextClient | TIER_2 | 2 | — | _not analysed_ |
| ProactiveEventTracker | TIER_2 | 2 | — | _not analysed_ |
| ProactiveExperiments | TIER_2 | 2 | — | _not analysed_ |
| ProactiveHarvesting | TIER_2 | 2 | — | _not analysed_ |
| ProactiveInputPredictionsInternals | TIER_2 | 2 | — | _not analysed_ |
| ProactiveMagicalMoments | TIER_2 | 2 | — | _not analysed_ |
| ProactiveSuggestionClientModel | TIER_2 | 2 | — | _not analysed_ |
| ProactiveSummarization | TIER_2 | 2 | — | _not analysed_ |
| ProactiveSupport | TIER_2 | 2 | — | _not analysed_ |
| ProductKit | TIER_2 | 2 | — | _not analysed_ |
| Profiles | TIER_2 | 2 | — | _not analysed_ |
| PromotedContent | TIER_2 | 2 | — | _not analysed_ |
| PromotedContentJetClient | TIER_2 | 2 | — | _not analysed_ |
| PromotedContentJetService | TIER_2 | 2 | — | _not analysed_ |
| PromotedContentJetSupport | TIER_2 | 2 | — | _not analysed_ |
| PromotedContentUI | TIER_2 | 2 | — | _not analysed_ |
| ProtectedCloudStorage | TIER_2 | 2 | — | _not analysed_ |
| ProximityAppleIDSetup | TIER_2 | 2 | — | _not analysed_ |
| ProximityAppleIDSetupUI | TIER_2 | 2 | — | _not analysed_ |
| ProximityReader | TIER_2 | 2 | — | _not analysed_ |
| ProximityReaderCore | TIER_2 | 2 | — | _not analysed_ |
| ProximityReaderDaemon | TIER_2 | 2 | — | _not analysed_ |
| QOSToolkit | TIER_2 | 2 | — | _not analysed_ |
| Quagga | TIER_2 | 2 | — | _not analysed_ |
| QueryParser | TIER_2 | 2 | — | _not analysed_ |
| QueryUnderstanding | TIER_2 | 2 | — | _not analysed_ |
| QuickSpeak | TIER_2 | 2 | — | _not analysed_ |
| RCS | TIER_2 | 2 | — | _not analysed_ |
| RapidResourceDelivery | TIER_2 | 2 | — | _not analysed_ |
| Rapport | TIER_2 | 2 | — | _not analysed_ |
| RawCamera | TIER_2 | 2 | — | _not analysed_ |
| RealityFusion | TIER_2 | 2 | — | _not analysed_ |
| RealityIO | TIER_2 | 2 | — | _not analysed_ |
| Recon3D | TIER_2 | 2 | — | _not analysed_ |
| RecoverDeviceUI | TIER_2 | 2 | — | _not analysed_ |
| RegulatoryDomain | TIER_2 | 2 | — | _not analysed_ |
| RelevanceEngine | TIER_2 | 2 | — | _not analysed_ |
| ReminderKit | TIER_2 | 2 | — | _not analysed_ |
| ReminderKitInternal | TIER_2 | 2 | — | _not analysed_ |
| RemindersSettings | TIER_2 | 2 | — | _not analysed_ |
| RemindersSiriUIPlugin | TIER_2 | 2 | — | _not analysed_ |
| RemindersUICore | TIER_2 | 2 | — | _not analysed_ |
| RemoteHID | TIER_2 | 2 | — | _not analysed_ |
| RemoteManagement | TIER_2 | 2 | — | _not analysed_ |
| RemoteManagementAgent | TIER_2 | 2 | — | _not analysed_ |
| RemoteManagementStore | TIER_2 | 2 | — | _not analysed_ |
| RemoteTextInput | TIER_2 | 2 | — | _not analysed_ |
| RemoteUI | TIER_2 | 2 | — | _not analysed_ |
| RenderBox | TIER_2 | 2 | — | _not analysed_ |
| ReplayKit | TIER_2 | 2 | — | _not analysed_ |
| ReplayKitAngel | TIER_2 | 2 | — | _not analysed_ |
| ReplayKitModule | TIER_2 | 2 | — | _not analysed_ |
| ReplicatorEngine | TIER_2 | 2 | — | _not analysed_ |
| RequestDispatcherBridges | TIER_2 | 2 | — | _not analysed_ |
| Required | TIER_2 | 2 | — | _not analysed_ |
| ResearchApp | TIER_2 | 2 | — | _not analysed_ |
| RespiratoryHealthAppPlugin | TIER_2 | 2 | — | _not analysed_ |
| ResponseGenerationUIPlugin | TIER_2 | 2 | — | _not analysed_ |
| RoomPlan | TIER_2 | 2 | — | _not analysed_ |
| RoseControllerLib | TIER_2 | 2 | — | _not analysed_ |
| RunningBoardServices | TIER_2 | 2 | — | _not analysed_ |
| SAObjects | TIER_2 | 2 | — | _not analysed_ |
| SBRendererService | TIER_2 | 2 | — | _not analysed_ |
| SDAPI | TIER_2 | 2 | — | _not analysed_ |
| SESUIServiceApp | TIER_2 | 2 | — | _not analysed_ |
| SEService | TIER_2 | 2 | — | _not analysed_ |
| SFSymbols | TIER_2 | 2 | — | _not analysed_ |
| SILManager | TIER_2 | 2 | — | _not analysed_ |
| SIMSetupUIService | TIER_2 | 2 | — | _not analysed_ |
| SMS | TIER_2 | 2 | — | _not analysed_ |
| SOS | TIER_2 | 2 | — | _not analysed_ |
| SOSBuddy | TIER_2 | 2 | — | _not analysed_ |
| SPIHelper-iOS | TIER_2 | 2 | — | _not analysed_ |
| SPOwner | TIER_2 | 2 | — | _not analysed_ |
| SPRCore | TIER_2 | 2 | — | _not analysed_ |
| STExtractionService.privileged | TIER_2 | 2 | — | _not analysed_ |
| STSXPCHelper | TIER_2 | 2 | — | _not analysed_ |
| SafariCore | TIER_2 | 2 | — | _not analysed_ |
| SafariFoundation | TIER_2 | 2 | — | _not analysed_ |
| SafariSafeBrowsing | TIER_2 | 2 | — | _not analysed_ |
| SafariServices | TIER_2 | 2 | — | _not analysed_ |
| SafariShared | TIER_2 | 2 | — | _not analysed_ |
| SafariSharedUI | TIER_2 | 2 | — | _not analysed_ |
| Safety | TIER_2 | 2 | — | _not analysed_ |
| SafetyMonitor | TIER_2 | 2 | — | _not analysed_ |
| SafetyMonitorUI | TIER_2 | 2 | — | _not analysed_ |
| Sage | TIER_2 | 2 | — | _not analysed_ |
| SampleAnalysis | TIER_2 | 2 | — | _not analysed_ |
| SatelliteSMS | TIER_2 | 2 | — | _not analysed_ |
| SavageUtil | TIER_2 | 2 | — | _not analysed_ |
| SceneIntelligence | TIER_2 | 2 | — | _not analysed_ |
| SceneKit | TIER_2 | 2 | — | _not analysed_ |
| SchoolTime | TIER_2 | 2 | — | _not analysed_ |
| ScreenReaderOutput | TIER_2 | 2 | — | _not analysed_ |
| ScreenSharingServer | TIER_2 | 2 | — | _not analysed_ |
| ScreenTime | TIER_2 | 2 | — | _not analysed_ |
| ScreenTimeAgent | TIER_2 | 2 | — | _not analysed_ |
| ScreenTimeCore | TIER_2 | 2 | — | _not analysed_ |
| ScreenTimeSettingsUI | TIER_2 | 2 | — | _not analysed_ |
| ScreenTimeSwift | TIER_2 | 2 | — | _not analysed_ |
| ScreenTimeUI | TIER_2 | 2 | — | _not analysed_ |
| ScreenshotServices | TIER_2 | 2 | — | _not analysed_ |
| ScreenshotServicesService | TIER_2 | 2 | — | _not analysed_ |
| Search | TIER_2 | 2 | — | _not analysed_ |
| SearchAds | TIER_2 | 2 | — | _not analysed_ |
| SearchFoundation | TIER_2 | 2 | — | _not analysed_ |
| SearchIndexer | TIER_2 | 2 | — | _not analysed_ |
| SearchOnDeviceAnalytics | TIER_2 | 2 | — | _not analysed_ |
| SearchToolUIPlugin | TIER_2 | 2 | — | _not analysed_ |
| SearchUI | TIER_2 | 2 | — | _not analysed_ |
| SecureCaptureKit | TIER_2 | 2 | — | _not analysed_ |
| SecureTransactionService | TIER_2 | 2 | — | _not analysed_ |
| SecureVoiceTriggerAssets | TIER_2 | 2 | — | _not analysed_ |
| Security | TIER_2 | 2 | — | _not analysed_ |
| Seeding | TIER_2 | 2 | — | _not analysed_ |
| SendLaterProvider | TIER_2 | 2 | — | _not analysed_ |
| SensingAlgsTouchButtonHost | TIER_2 | 2 | — | _not analysed_ |
| SensitiveContentAnalysisML | TIER_2 | 2 | — | _not analysed_ |
| SensitiveContentAnalysisUI | TIER_2 | 2 | — | _not analysed_ |
| SensorAccess | TIER_2 | 2 | — | _not analysed_ |
| SensorKit | TIER_2 | 2 | — | _not analysed_ |
| SensorKitALSHelper | TIER_2 | 2 | — | _not analysed_ |
| SensorKitLongTermStorageHelper | TIER_2 | 2 | — | _not analysed_ |
| SensorKitPrivacySettings | TIER_2 | 2 | — | _not analysed_ |
| SensorKitWriting | TIER_2 | 2 | — | _not analysed_ |
| SequoiaTranslator | TIER_2 | 2 | — | _not analysed_ |
| ServiceManagement | TIER_2 | 2 | — | _not analysed_ |
| SessionCore | TIER_2 | 2 | — | _not analysed_ |
| SessionFilterRecordingUpdater | TIER_2 | 2 | — | _not analysed_ |
| SessionTrackerAppSettings | TIER_2 | 2 | — | _not analysed_ |
| Settings | TIER_2 | 2 | — | _not analysed_ |
| SettingsCellular | TIER_2 | 2 | — | _not analysed_ |
| SettingsCellularUI | TIER_2 | 2 | — | _not analysed_ |
| SettingsCustomPlugin | TIER_2 | 2 | — | _not analysed_ |
| SettingsFlowDelegatePlugin | TIER_2 | 2 | — | _not analysed_ |
| SettingsFoundation | TIER_2 | 2 | — | _not analysed_ |
| SettingsHost | TIER_2 | 2 | — | _not analysed_ |
| SettingsUIKitPrivate | TIER_2 | 2 | — | _not analysed_ |
| SetupAssistant | TIER_2 | 2 | — | _not analysed_ |
| SetupAssistantSupport | TIER_2 | 2 | — | _not analysed_ |
| SetupAssistantSupportUI | TIER_2 | 2 | — | _not analysed_ |
| SetupAssistantUI | TIER_2 | 2 | — | _not analysed_ |
| SeymourClient | TIER_2 | 2 | — | _not analysed_ |
| SeymourClientServices | TIER_2 | 2 | — | _not analysed_ |
| SeymourCore | TIER_2 | 2 | — | _not analysed_ |
| SeymourMedia | TIER_2 | 2 | — | _not analysed_ |
| SeymourSessionServices | TIER_2 | 2 | — | _not analysed_ |
| SeymourUI | TIER_2 | 2 | — | _not analysed_ |
| ShaderGraph | TIER_2 | 2 | — | _not analysed_ |
| ShareSheet | TIER_2 | 2 | — | _not analysed_ |
| SharedUtils | TIER_2 | 2 | — | _not analysed_ |
| SharedWebCredentialViewService | TIER_2 | 2 | — | _not analysed_ |
| SharingViewService | TIER_2 | 2 | — | _not analysed_ |
| ShazamCore | TIER_2 | 2 | — | _not analysed_ |
| ShazamEvents | TIER_2 | 2 | — | _not analysed_ |
| ShazamEventsApp | TIER_2 | 2 | — | _not analysed_ |
| ShazamInsights | TIER_2 | 2 | — | _not analysed_ |
| ShazamKit | TIER_2 | 2 | — | _not analysed_ |
| ShazamKitUI | TIER_2 | 2 | — | _not analysed_ |
| ShazamUIPlugin | TIER_2 | 2 | — | _not analysed_ |
| ShelfKit | TIER_2 | 2 | — | _not analysed_ |
| ShelfKitCollectionViews | TIER_2 | 2 | — | _not analysed_ |
| ShellSceneKit | TIER_2 | 2 | — | _not analysed_ |
| ShimGameServices | TIER_2 | 2 | — | _not analysed_ |
| SidecarRelay | TIER_2 | 2 | — | _not analysed_ |
| SignpostSupport | TIER_2 | 2 | — | _not analysed_ |
| Silex | TIER_2 | 2 | — | _not analysed_ |
| SilexWeb | TIER_2 | 2 | — | _not analysed_ |
| SiriActivation | TIER_2 | 2 | — | _not analysed_ |
| SiriAnalytics | TIER_2 | 2 | — | _not analysed_ |
| SiriAppLaunchIntents | TIER_2 | 2 | — | _not analysed_ |
| SiriAppLaunchUIFramework | TIER_2 | 2 | — | _not analysed_ |
| SiriAppLaunchUIPlugin | TIER_2 | 2 | — | _not analysed_ |
| SiriAudioInternal | TIER_2 | 2 | — | _not analysed_ |
| SiriAudioSupport | TIER_2 | 2 | — | _not analysed_ |
| SiriAutoComplete | TIER_2 | 2 | — | _not analysed_ |
| SiriCalendarUI | TIER_2 | 2 | — | _not analysed_ |
| SiriContactsIntents | TIER_2 | 2 | — | _not analysed_ |
| SiriCrossDeviceArbitration | TIER_2 | 2 | — | _not analysed_ |
| SiriEntityMatcher | TIER_2 | 2 | — | _not analysed_ |
| SiriInference | TIER_2 | 2 | — | _not analysed_ |
| SiriInformationSearch | TIER_2 | 2 | — | _not analysed_ |
| SiriInformationTypes | TIER_2 | 2 | — | _not analysed_ |
| SiriInstrumentation | TIER_2 | 2 | — | _not analysed_ |
| SiriInteractive | TIER_2 | 2 | — | _not analysed_ |
| SiriKitRuntime | TIER_2 | 2 | — | _not analysed_ |
| SiriLinkFlowPlugin | TIER_2 | 2 | — | _not analysed_ |
| SiriLinkUIPlugin | TIER_2 | 2 | — | _not analysed_ |
| SiriMessageBus | TIER_2 | 2 | — | _not analysed_ |
| SiriMessageTypes | TIER_2 | 2 | — | _not analysed_ |
| SiriMessagesFlow | TIER_2 | 2 | — | _not analysed_ |
| SiriMessagesUI | TIER_2 | 2 | — | _not analysed_ |
| SiriNLUTypes | TIER_2 | 2 | — | _not analysed_ |
| SiriNaturalLanguageParsing | TIER_2 | 2 | — | _not analysed_ |
| SiriNetwork | TIER_2 | 2 | — | _not analysed_ |
| SiriNotebookUI | TIER_2 | 2 | — | _not analysed_ |
| SiriPlaybackControlIntents | TIER_2 | 2 | — | _not analysed_ |
| SiriPlaybackControlSupport | TIER_2 | 2 | — | _not analysed_ |
| SiriPrivateLearningInference | TIER_2 | 2 | — | _not analysed_ |
| SiriRemembers | TIER_2 | 2 | — | _not analysed_ |
| SiriSettingsSuggestionsPlugin | TIER_2 | 2 | — | _not analysed_ |
| SiriSettingsUI | TIER_2 | 2 | — | _not analysed_ |
| SiriSetup | TIER_2 | 2 | — | _not analysed_ |
| SiriSpeechSynthesis | TIER_2 | 2 | — | _not analysed_ |
| SiriSuggestions | TIER_2 | 2 | — | _not analysed_ |
| SiriSuggestionsBaseModel | TIER_2 | 2 | — | _not analysed_ |
| SiriSuggestionsBookkeepingService | TIER_2 | 2 | — | _not analysed_ |
| SiriSuggestionsFlowPlugin | TIER_2 | 2 | — | _not analysed_ |
| SiriSuggestionsInferenceBridge | TIER_2 | 2 | — | _not analysed_ |
| SiriSuggestionsKit | TIER_2 | 2 | — | _not analysed_ |
| SiriSuggestionsSKEBridge | TIER_2 | 2 | — | _not analysed_ |
| SiriSuggestionsSupport | TIER_2 | 2 | — | _not analysed_ |
| SiriTTS | TIER_2 | 2 | — | _not analysed_ |
| SiriTTSTraining | TIER_2 | 2 | — | _not analysed_ |
| SiriUIFoundation | TIER_2 | 2 | — | _not analysed_ |
| SiriVideoIntents | TIER_2 | 2 | — | _not analysed_ |
| SiriVideoUIFramework | TIER_2 | 2 | — | _not analysed_ |
| SiriVideoUIPlugin | TIER_2 | 2 | — | _not analysed_ |
| SleepDaemon | TIER_2 | 2 | — | _not analysed_ |
| SleepHealthAppPlugin | TIER_2 | 2 | — | _not analysed_ |
| SleepHealthDaemon | TIER_2 | 2 | — | _not analysed_ |
| SleepHealthUI | TIER_2 | 2 | — | _not analysed_ |
| SleepLockScreen | TIER_2 | 2 | — | _not analysed_ |
| SleepWidgetUI | TIER_2 | 2 | — | _not analysed_ |
| SnippetUI | TIER_2 | 2 | — | _not analysed_ |
| Social | TIER_2 | 2 | — | _not analysed_ |
| SocialLayer | TIER_2 | 2 | — | _not analysed_ |
| SocialServices | TIER_2 | 2 | — | _not analysed_ |
| SoftPosReader | TIER_2 | 2 | — | _not analysed_ |
| SoftwareUpdateBridge | TIER_2 | 2 | — | _not analysed_ |
| SoftwareUpdateCoreConnect | TIER_2 | 2 | — | _not analysed_ |
| SoftwareUpdateServices | TIER_2 | 2 | — | _not analysed_ |
| SoftwareUpdateServicesUI | TIER_2 | 2 | — | _not analysed_ |
| SoftwareUpdateServicesUIPlugin | TIER_2 | 2 | — | _not analysed_ |
| SoftwareUpdateSettingsUI | TIER_2 | 2 | — | _not analysed_ |
| SoftwareUpdateUIService | TIER_2 | 2 | — | _not analysed_ |
| SonicFoundation | TIER_2 | 2 | — | _not analysed_ |
| SonicKit | TIER_2 | 2 | — | _not analysed_ |
| SoundAnalysis | TIER_2 | 2 | — | _not analysed_ |
| SoundsAndHapticsSettings | TIER_2 | 2 | — | _not analysed_ |
| SpaceAttribution | TIER_2 | 2 | — | _not analysed_ |
| SpeakThis | TIER_2 | 2 | — | _not analysed_ |
| SpeakerRecognition | TIER_2 | 2 | — | _not analysed_ |
| SpeechDetector | TIER_2 | 2 | — | _not analysed_ |
| SpeechDictionary | TIER_2 | 2 | — | _not analysed_ |
| SpeechRecognitionCommandAndControl | TIER_2 | 2 | — | _not analysed_ |
| SpeechRecognitionCommandServices | TIER_2 | 2 | — | _not analysed_ |
| SpeechRecognitionCore | TIER_2 | 2 | — | _not analysed_ |
| Spotlight | TIER_2 | 2 | — | _not analysed_ |
| SpotlightDaemon | TIER_2 | 2 | — | _not analysed_ |
| SpotlightKnowledge | TIER_2 | 2 | — | _not analysed_ |
| SpotlightLinguistics | TIER_2 | 2 | — | _not analysed_ |
| SpotlightReceiver | TIER_2 | 2 | — | _not analysed_ |
| SpotlightResources | TIER_2 | 2 | — | _not analysed_ |
| SpotlightServices | TIER_2 | 2 | — | _not analysed_ |
| SpotlightUIInternal | TIER_2 | 2 | — | _not analysed_ |
| SpringBoardEducation | TIER_2 | 2 | — | _not analysed_ |
| SpringBoardFoundation | TIER_2 | 2 | — | _not analysed_ |
| SpringBoardServices | TIER_2 | 2 | — | _not analysed_ |
| SpringBoardUIServices | TIER_2 | 2 | — | _not analysed_ |
| SpriteKit | TIER_2 | 2 | — | _not analysed_ |
| StatusKit | TIER_2 | 2 | — | _not analysed_ |
| StatusKitAgent | TIER_2 | 2 | — | _not analysed_ |
| StatusKitAgentCore | TIER_2 | 2 | — | _not analysed_ |
| StickerPickerService | TIER_2 | 2 | — | _not analysed_ |
| Stickers | TIER_2 | 2 | — | _not analysed_ |
| Stocks | TIER_2 | 2 | — | _not analysed_ |
| StocksAnalytics | TIER_2 | 2 | — | _not analysed_ |
| StocksCore | TIER_2 | 2 | — | _not analysed_ |
| StocksKit | TIER_2 | 2 | — | _not analysed_ |
| StocksKitService | TIER_2 | 2 | — | _not analysed_ |
| StocksPersonalization | TIER_2 | 2 | — | _not analysed_ |
| StocksUI | TIER_2 | 2 | — | _not analysed_ |
| StoreDemoPlugin | TIER_2 | 2 | — | _not analysed_ |
| StoreDynamicUIPlugin | TIER_2 | 2 | — | _not analysed_ |
| StoreKit | TIER_2 | 2 | — | _not analysed_ |
| StoreKitUI | TIER_2 | 2 | — | _not analysed_ |
| StoreKitUIService | TIER_2 | 2 | — | _not analysed_ |
| StoreServices | TIER_2 | 2 | — | _not analysed_ |
| StreamingExtractor | TIER_2 | 2 | — | _not analysed_ |
| StreamingZip | TIER_2 | 2 | — | _not analysed_ |
| Summaries | TIER_2 | 2 | — | _not analysed_ |
| SummarizationKit | TIER_2 | 2 | — | _not analysed_ |
| SwiftCertificate | TIER_2 | 2 | — | _not analysed_ |
| SwiftData | TIER_2 | 2 | — | _not analysed_ |
| SymptomEvaluator | TIER_2 | 2 | — | _not analysed_ |
| SystemAppMigrator | TIER_2 | 2 | — | _not analysed_ |
| SystemConfiguration | TIER_2 | 2 | — | _not analysed_ |
| SystemExtensions | TIER_2 | 2 | — | _not analysed_ |
| SystemStatus | TIER_2 | 2 | — | _not analysed_ |
| SystemStatusUI | TIER_2 | 2 | — | _not analysed_ |
| SystemUIAnimationKit | TIER_2 | 2 | — | _not analysed_ |
| TCC | TIER_2 | 2 | — | _not analysed_ |
| TDGSharingViewService | TIER_2 | 2 | — | _not analysed_ |
| TSCharts | TIER_2 | 2 | — | _not analysed_ |
| TSPersistence | TIER_2 | 2 | — | _not analysed_ |
| TSReading | TIER_2 | 2 | — | _not analysed_ |
| TSText | TIER_2 | 2 | — | _not analysed_ |
| TSUtility | TIER_2 | 2 | — | _not analysed_ |
| TVMLKit | TIER_2 | 2 | — | _not analysed_ |
| TVPlayback | TIER_2 | 2 | — | _not analysed_ |
| TVRemoteCore | TIER_2 | 2 | — | _not analysed_ |
| TVRemoteUI | TIER_2 | 2 | — | _not analysed_ |
| TVSettings | TIER_2 | 2 | — | _not analysed_ |
| TailspinSymbolication | TIER_2 | 2 | — | _not analysed_ |
| Tamale | TIER_2 | 2 | — | _not analysed_ |
| TeaDB | TIER_2 | 2 | — | _not analysed_ |
| TeaTemplate | TIER_2 | 2 | — | _not analysed_ |
| TeaUI | TIER_2 | 2 | — | _not analysed_ |
| TelemetryDiskChecker | TIER_2 | 2 | — | _not analysed_ |
| TelephonyBlastDoorSupport | TIER_2 | 2 | — | _not analysed_ |
| TelephonyKit | TIER_2 | 2 | — | _not analysed_ |
| TelephonyPreferences | TIER_2 | 2 | — | _not analysed_ |
| TelephonyRPC | TIER_2 | 2 | — | _not analysed_ |
| TelephonyUtilities | TIER_2 | 2 | — | _not analysed_ |
| TelephonyXPCServer | TIER_2 | 2 | — | _not analysed_ |
| TemplateKit | TIER_2 | 2 | — | _not analysed_ |
| TemplateUI | TIER_2 | 2 | — | _not analysed_ |
| TestFlightCore | TIER_2 | 2 | — | _not analysed_ |
| TextInput | TIER_2 | 2 | — | _not analysed_ |
| TextInputCore | TIER_2 | 2 | — | _not analysed_ |
| TextInputTestingKit | TIER_2 | 2 | — | _not analysed_ |
| TextInputUI | TIER_2 | 2 | — | _not analysed_ |
| TextInput_ko | TIER_2 | 2 | — | _not analysed_ |
| TextInput_th | TIER_2 | 2 | — | _not analysed_ |
| TextRecognition | TIER_2 | 2 | — | _not analysed_ |
| TextToSpeechMauiSupport | TIER_2 | 2 | — | _not analysed_ |
| TextToSpeechVoiceBankingSupport | TIER_2 | 2 | — | _not analysed_ |
| TextUnderstandingShared | TIER_2 | 2 | — | _not analysed_ |
| ThreadNetwork | TIER_2 | 2 | — | _not analysed_ |
| Tightbeam | TIER_2 | 2 | — | _not analysed_ |
| TimeSync | TIER_2 | 2 | — | _not analysed_ |
| TipsCore | TIER_2 | 2 | — | _not analysed_ |
| TipsDaemon | TIER_2 | 2 | — | _not analysed_ |
| TipsTryIt | TIER_2 | 2 | — | _not analysed_ |
| TipsUI | TIER_2 | 2 | — | _not analysed_ |
| TirePressure | TIER_2 | 2 | — | _not analysed_ |
| TodayFeedConfigDecoder | TIER_2 | 2 | — | _not analysed_ |
| TokenGeneration | TIER_2 | 2 | — | _not analysed_ |
| TokenGenerationCore | TIER_2 | 2 | — | _not analysed_ |
| ToneKit | TIER_2 | 2 | — | _not analysed_ |
| ToolKit | TIER_2 | 2 | — | _not analysed_ |
| TrackingAvoidance | TIER_2 | 2 | — | _not analysed_ |
| Translation | TIER_2 | 2 | — | _not analysed_ |
| TranslationUI | TIER_2 | 2 | — | _not analysed_ |
| Transparency | TIER_2 | 2 | — | _not analysed_ |
| TransparencyUI | TIER_2 | 2 | — | _not analysed_ |
| Trial | TIER_2 | 2 | — | _not analysed_ |
| TrialServer | TIER_2 | 2 | — | _not analysed_ |
| Trip | TIER_2 | 2 | — | _not analysed_ |
| TrustedPeersHelper | TIER_2 | 2 | — | _not analysed_ |
| TuriCore | TIER_2 | 2 | — | _not analysed_ |
| UARPUpdaterServiceAFU | TIER_2 | 2 | — | _not analysed_ |
| UARPUpdaterServiceLegacyAudio | TIER_2 | 2 | — | _not analysed_ |
| UIAccessibility | TIER_2 | 2 | — | _not analysed_ |
| UIFoundation | TIER_2 | 2 | — | _not analysed_ |
| UIIntelligenceSupport | TIER_2 | 2 | — | _not analysed_ |
| UIIntelligenceSupportAgent | TIER_2 | 2 | — | _not analysed_ |
| UIKitServices | TIER_2 | 2 | — | _not analysed_ |
| USBHost | TIER_2 | 2 | — | _not analysed_ |
| USDKit | TIER_2 | 2 | — | _not analysed_ |
| UVFSService | TIER_2 | 2 | — | _not analysed_ |
| UnifiedMessagingKit | TIER_2 | 2 | — | _not analysed_ |
| UniversalHIDKit | TIER_2 | 2 | — | _not analysed_ |
| UrchinBridgeSettings | TIER_2 | 2 | — | _not analysed_ |
| UrchinKit | TIER_2 | 2 | — | _not analysed_ |
| UsageTracking | TIER_2 | 2 | — | _not analysed_ |
| UsageTrackingAgent | TIER_2 | 2 | — | _not analysed_ |
| UserFontManager | TIER_2 | 2 | — | _not analysed_ |
| UserManagement | TIER_2 | 2 | — | _not analysed_ |
| UserManagementLayout | TIER_2 | 2 | — | _not analysed_ |
| VDAF | TIER_2 | 2 | — | _not analysed_ |
| Vehicle | TIER_2 | 2 | — | _not analysed_ |
| ViceroyTrace | TIER_2 | 2 | — | _not analysed_ |
| VideoConferenceControlCenterModule | TIER_2 | 2 | — | _not analysed_ |
| VideoFlowDelegatePlugin | TIER_2 | 2 | — | _not analysed_ |
| VideoProcessing | TIER_2 | 2 | — | _not analysed_ |
| VideoSubscriberAccount | TIER_2 | 2 | — | _not analysed_ |
| VideoSubscriberAccountUI | TIER_2 | 2 | — | _not analysed_ |
| VideoToolbox | TIER_2 | 2 | — | _not analysed_ |
| VideoToolboxParavirtualizationSupport | TIER_2 | 2 | — | _not analysed_ |
| VideosUI | TIER_2 | 2 | — | _not analysed_ |
| VideosUICore | TIER_2 | 2 | — | _not analysed_ |
| VideosUIFramework | TIER_2 | 2 | — | _not analysed_ |
| VirtualGarage | TIER_2 | 2 | — | _not analysed_ |
| Visage | TIER_2 | 2 | — | _not analysed_ |
| VisionCompanion | TIER_2 | 2 | — | _not analysed_ |
| VisionCore | TIER_2 | 2 | — | _not analysed_ |
| VisionHealthAppPlugin | TIER_2 | 2 | — | _not analysed_ |
| VisionKitCore | TIER_2 | 2 | — | _not analysed_ |
| VisualGeneration | TIER_2 | 2 | — | _not analysed_ |
| VisualLocalization | TIER_2 | 2 | — | _not analysed_ |
| VisualLogger | TIER_2 | 2 | — | _not analysed_ |
| VisualUnderstanding | TIER_2 | 2 | — | _not analysed_ |
| VisualVoicemail | TIER_2 | 2 | — | _not analysed_ |
| VoiceActions | TIER_2 | 2 | — | _not analysed_ |
| VoiceControl | TIER_2 | 2 | — | _not analysed_ |
| VoiceMemos | TIER_2 | 2 | — | _not analysed_ |
| VoiceOverServices | TIER_2 | 2 | — | _not analysed_ |
| VoiceServices | TIER_2 | 2 | — | _not analysed_ |
| VoiceTrigger | TIER_2 | 2 | — | _not analysed_ |
| VoiceTriggerUI | TIER_2 | 2 | — | _not analysed_ |
| WPDaemon | TIER_2 | 2 | — | _not analysed_ |
| WalletPrivacySettings | TIER_2 | 2 | — | _not analysed_ |
| WatchControlSettings | TIER_2 | 2 | — | _not analysed_ |
| WatchFacesWallpaperSupport | TIER_2 | 2 | — | _not analysed_ |
| WatchListKit | TIER_2 | 2 | — | _not analysed_ |
| Weather | TIER_2 | 2 | — | _not analysed_ |
| WeatherAnalytics | TIER_2 | 2 | — | _not analysed_ |
| WeatherAppSupport | TIER_2 | 2 | — | _not analysed_ |
| WeatherComplications | TIER_2 | 2 | — | _not analysed_ |
| WeatherDaemon | TIER_2 | 2 | — | _not analysed_ |
| WeatherKit | TIER_2 | 2 | — | _not analysed_ |
| WeatherSettings | TIER_2 | 2 | — | _not analysed_ |
| WeatherUI | TIER_2 | 2 | — | _not analysed_ |
| WebBookmarks | TIER_2 | 2 | — | _not analysed_ |
| WebContentRestrictions | TIER_2 | 2 | — | _not analysed_ |
| WebCore | TIER_2 | 2 | — | _not analysed_ |
| WebGPU | TIER_2 | 2 | — | _not analysed_ |
| WebKitLegacy | TIER_2 | 2 | — | _not analysed_ |
| WebSheet | TIER_2 | 2 | — | _not analysed_ |
| WebUI | TIER_2 | 2 | — | _not analysed_ |
| WiFiAnalytics | TIER_2 | 2 | — | _not analysed_ |
| WiFiKit | TIER_2 | 2 | — | _not analysed_ |
| WiFiKitUI | TIER_2 | 2 | — | _not analysed_ |
| WiFiPeerToPeer | TIER_2 | 2 | — | _not analysed_ |
| WiFiPolicy | TIER_2 | 2 | — | _not analysed_ |
| WiFiSettings | TIER_2 | 2 | — | _not analysed_ |
| WidgetPreviewsShellPlugin | TIER_2 | 2 | — | _not analysed_ |
| WidgetRenderer | TIER_2 | 2 | — | _not analysed_ |
| WirelessCoexManager | TIER_2 | 2 | — | _not analysed_ |
| WirelessRadioManagerd | TIER_2 | 2 | — | _not analysed_ |
| WorkflowEditor | TIER_2 | 2 | — | _not analysed_ |
| WorkflowKit | TIER_2 | 2 | — | _not analysed_ |
| WorkflowResponsiveness | TIER_2 | 2 | — | _not analysed_ |
| WorkflowUI | TIER_2 | 2 | — | _not analysed_ |
| WorkflowUIServices | TIER_2 | 2 | — | _not analysed_ |
| WorkoutComplicationBundleCompanion | TIER_2 | 2 | — | _not analysed_ |
| WorkoutHealthPlugin | TIER_2 | 2 | — | _not analysed_ |
| WorkoutKit | TIER_2 | 2 | — | _not analysed_ |
| WorkoutKitXPCService | TIER_2 | 2 | — | _not analysed_ |
| WorkoutRemoteViewService | TIER_2 | 2 | — | _not analysed_ |
| WorkoutUI | TIER_2 | 2 | — | _not analysed_ |
| WorldClockComplications | TIER_2 | 2 | — | _not analysed_ |
| WritingToolsUI | TIER_2 | 2 | — | _not analysed_ |
| WritingToolsUIService | TIER_2 | 2 | — | _not analysed_ |
| XCTTargetBootstrap | TIER_2 | 2 | — | _not analysed_ |
| XOJIT | TIER_2 | 2 | — | _not analysed_ |
| XPCAcmeService | TIER_2 | 2 | — | _not analysed_ |
| YamahaUSBMIDIDriver | TIER_2 | 2 | — | _not analysed_ |
| YonkersUtil | TIER_2 | 2 | — | _not analysed_ |
| ZeoliteLanguage | TIER_2 | 2 | — | _not analysed_ |
| ZoomTouch | TIER_2 | 2 | — | _not analysed_ |
| ZoomWindow | TIER_2 | 2 | — | _not analysed_ |
| _GroupActivities_UIKit | TIER_2 | 2 | — | _not analysed_ |
| _JetEngine_SwiftUI | TIER_2 | 2 | — | _not analysed_ |
| _JetUI_SwiftUI | TIER_2 | 2 | — | _not analysed_ |
| _ManagedAppDistribution_SwiftUI | TIER_2 | 2 | — | _not analysed_ |
| _MusicKitInternal_MediaPlaybackCore | TIER_2 | 2 | — | _not analysed_ |
| _MusicKitInternal_MediaPlayer | TIER_2 | 2 | — | _not analysed_ |
| _MusicKitInternal_SwiftUI | TIER_2 | 2 | — | _not analysed_ |
| _MusicKit_SwiftUI | TIER_2 | 2 | — | _not analysed_ |
| _PassKit_SwiftUI | TIER_2 | 2 | — | _not analysed_ |
| _RealityKit_SwiftUI | TIER_2 | 2 | — | _not analysed_ |
| _SecureElementCredential_SwiftUI | TIER_2 | 2 | — | _not analysed_ |
| _SecureElementCredential_UIKit | TIER_2 | 2 | — | _not analysed_ |
| _SonicKit_MusicKit | TIER_2 | 2 | — | _not analysed_ |
| _SonicKit_MusicKit_Packages | TIER_2 | 2 | — | _not analysed_ |
| _SwiftData_SwiftUI | TIER_2 | 2 | — | _not analysed_ |
| absd | TIER_2 | 2 | — | _not analysed_ |
| accessoryd | TIER_2 | 2 | — | _not analysed_ |
| addressbooksyncd | TIER_2 | 2 | — | _not analysed_ |
| adid | TIER_2 | 2 | — | _not analysed_ |
| agx_a000 | TIER_2 | 2 | — | _not analysed_ |
| agx_a010 | TIER_2 | 2 | — | _not analysed_ |
| agx_b000 | TIER_2 | 2 | — | _not analysed_ |
| agx_b010 | TIER_2 | 2 | — | _not analysed_ |
| agx_b100 | TIER_2 | 2 | — | _not analysed_ |
| akd | TIER_2 | 2 | — | _not analysed_ |
| amfid | TIER_2 | 2 | — | _not analysed_ |
| amsaccountsd | TIER_2 | 2 | — | _not analysed_ |
| amsengagementd | TIER_2 | 2 | — | _not analysed_ |
| analyticsagent | TIER_2 | 2 | — | _not analysed_ |
| analyticsd | TIER_2 | 2 | — | _not analysed_ |
| aned | TIER_2 | 2 | — | _not analysed_ |
| anomalydetectiond | TIER_2 | 2 | — | _not analysed_ |
| apfs.util | TIER_2 | 2 | — | _not analysed_ |
| apfs_boot_util | TIER_2 | 2 | — | _not analysed_ |
| apfs_checkdigest | TIER_2 | 2 | — | _not analysed_ |
| apfs_iosd | TIER_2 | 2 | — | _not analysed_ |
| appinstallationmetricsd | TIER_2 | 2 | — | _not analysed_ |
| appleaccountd | TIER_2 | 2 | — | _not analysed_ |
| appleidsetupd | TIER_2 | 2 | — | _not analysed_ |
| appstored | TIER_2 | 2 | — | _not analysed_ |
| asd | TIER_2 | 2 | — | _not analysed_ |
| askpermissiond | TIER_2 | 2 | — | _not analysed_ |
| asktod | TIER_2 | 2 | — | _not analysed_ |
| assessmentagent | TIER_2 | 2 | — | _not analysed_ |
| assistantd | TIER_2 | 2 | — | _not analysed_ |
| assistivetouchd | TIER_2 | 2 | — | _not analysed_ |
| attributionkitd | TIER_2 | 2 | — | _not analysed_ |
| audioaccessoryd | TIER_2 | 2 | — | _not analysed_ |
| audioanalyticsd | TIER_2 | 2 | — | _not analysed_ |
| audioclocksyncd | TIER_2 | 2 | — | _not analysed_ |
| axassetsd | TIER_2 | 2 | — | _not analysed_ |
| axauditd | TIER_2 | 2 | — | _not analysed_ |
| backboardd | TIER_2 | 2 | — | _not analysed_ |
| backgroundassets.user | TIER_2 | 2 | — | _not analysed_ |
| biomesyncd | TIER_2 | 2 | — | _not analysed_ |
| biometrickitd | TIER_2 | 2 | — | _not analysed_ |
| bluetoothuserd | TIER_2 | 2 | — | _not analysed_ |
| bookdatastored | TIER_2 | 2 | — | _not analysed_ |
| bootpd | TIER_2 | 2 | — | _not analysed_ |
| budd | TIER_2 | 2 | — | _not analysed_ |
| businessservicesd | TIER_2 | 2 | — | _not analysed_ |
| callservicesd | TIER_2 | 2 | — | _not analysed_ |
| captiveagent | TIER_2 | 2 | — | _not analysed_ |
| caraccessoryd | TIER_2 | 2 | — | _not analysed_ |
| carkitd | TIER_2 | 2 | — | _not analysed_ |
| catutil | TIER_2 | 2 | — | _not analysed_ |
| caulk | TIER_2 | 2 | — | _not analysed_ |
| cc_fips_test | TIER_2 | 2 | — | _not analysed_ |
| ciphermld | TIER_2 | 2 | — | _not analysed_ |
| cloudd | TIER_2 | 2 | — | _not analysed_ |
| cloudphotod | TIER_2 | 2 | — | _not analysed_ |
| codecctl | TIER_2 | 2 | — | _not analysed_ |
| com.apple.AppleKeyStoreEvents | TIER_2 | 2 | — | _not analysed_ |
| com.apple.CallKit.CallDirectory | TIER_2 | 2 | — | _not analysed_ |
| com.apple.CallKit.CallDirectoryMaintenance | TIER_2 | 2 | — | _not analysed_ |
| com.apple.DocumentManagerCore.Rename | TIER_2 | 2 | — | _not analysed_ |
| com.apple.DriverKit-AppleEthernetE1000 | TIER_2 | 2 | — | _not analysed_ |
| com.apple.DriverKit-AppleEthernetIXL | TIER_2 | 2 | — | _not analysed_ |
| com.apple.EXBrightKext | TIER_2 | 2 | — | _not analysed_ |
| com.apple.FTLivePhotoService | TIER_2 | 2 | — | _not analysed_ |
| com.apple.FontServices.FontProviderLoader | TIER_2 | 2 | — | _not analysed_ |
| com.apple.MobileSoftwareUpdate.CleanupPreparePathService | TIER_2 | 2 | — | _not analysed_ |
| com.apple.NeighborhoodActivityConduitService | TIER_2 | 2 | — | _not analysed_ |
| com.apple.PerformanceTrace.PerformanceTraceService | TIER_2 | 2 | — | _not analysed_ |
| com.apple.PrintKit.PrinterTool | TIER_2 | 2 | — | _not analysed_ |
| com.apple.SharePlay.NearbyInvitationsService | TIER_2 | 2 | — | _not analysed_ |
| com.apple.SpeechRecognitionCore.brokerd | TIER_2 | 2 | — | _not analysed_ |
| com.apple.SpeechRecognitionCore.speechrecognitiond | TIER_2 | 2 | — | _not analysed_ |
| com.apple.StreamingUnzipService.privileged | TIER_2 | 2 | — | _not analysed_ |
| com.apple.accessoryd.matching | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleARMPlatform | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleBasebandM20 | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleBasebandPCIMAVControl | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleBasebandPCIMAVPDP | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleDiskImages2 | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleDisplayCrossbar | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleEmbeddedAudioLibs | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleEmbeddedUSBHost | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleFirmwareKit | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleGenericMultitouch | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleHIDTransport | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleHIDTransportFIFO | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleHPM | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleHapticsSupportLEAP | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleJPEGDriver | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleLockdownMode | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleM68Buttons | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleMobileApNonce | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleMobileDispH17P-DCP | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleMultitouchDriver | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleMultitouchSPI | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.ApplePMGR | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.ApplePPMCPMS | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.ApplePearlSEPDriver | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleProcessorTrace | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleSARService | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleSEPCredentialManager | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleSEPManager | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleSPMI | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleSPU | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleUSBAudio | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleUSBLightningAdapter | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AudioDMAController-T8140 | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.ExclavesAudioKext | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.IOPAudioVoiceTriggerDevice | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.RTBuddy | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.SecureRTBuddyProxy | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.corecapture | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.usb.AppleSynopsysUSB40XHCI | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.usb.AppleUSBHub | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.usb.AppleUSBXHCI | TIER_2 | 2 | — | _not analysed_ |
| com.apple.filesystems.lifs | TIER_2 | 2 | — | _not analysed_ |
| com.apple.health.records.legacy-ingestion | TIER_2 | 2 | — | _not analysed_ |
| com.apple.iokit.IOAVFamily | TIER_2 | 2 | — | _not analysed_ |
| com.apple.iokit.IOAccessoryManager | TIER_2 | 2 | — | _not analysed_ |
| com.apple.iokit.IOBiometricFamily | TIER_2 | 2 | — | _not analysed_ |
| com.apple.iokit.IODisplayPortFamily | TIER_2 | 2 | — | _not analysed_ |
| com.apple.iokit.IOGPUFamily | TIER_2 | 2 | — | _not analysed_ |
| com.apple.iokit.IOGameControllerFamily | TIER_2 | 2 | — | _not analysed_ |
| com.apple.iokit.IOMobileGraphicsFamily | TIER_2 | 2 | — | _not analysed_ |
| com.apple.iokit.IOMobileGraphicsFamily-DCP | TIER_2 | 2 | — | _not analysed_ |
| com.apple.iokit.IOSkywalkFamily | TIER_2 | 2 | — | _not analysed_ |
| com.apple.iokit.IOThunderboltFamily | TIER_2 | 2 | — | _not analysed_ |
| com.apple.iokit.IOTimeSyncFamily | TIER_2 | 2 | — | _not analysed_ |
| com.apple.iokit.IOUSBHostFamily | TIER_2 | 2 | — | _not analysed_ |
| com.apple.kec.corecrypto | TIER_2 | 2 | — | _not analysed_ |
| com.apple.photos.ImageConversionService | TIER_2 | 2 | — | _not analysed_ |
| com.apple.photos.VideoConversionService | TIER_2 | 2 | — | _not analysed_ |
| com.apple.siri.embeddedspeech | TIER_2 | 2 | — | _not analysed_ |
| com.apple.telemetry | TIER_2 | 2 | — | _not analysed_ |
| com.apple.weather.appremoval | TIER_2 | 2 | — | _not analysed_ |
| com.apple.weatherkit.authservice | TIER_2 | 2 | — | _not analysed_ |
| companioncamerad | TIER_2 | 2 | — | _not analysed_ |
| companiond | TIER_2 | 2 | — | _not analysed_ |
| configd | TIER_2 | 2 | — | _not analysed_ |
| contactsd | TIER_2 | 2 | — | _not analysed_ |
| continuitycaptured | TIER_2 | 2 | — | _not analysed_ |
| coreauthd | TIER_2 | 2 | — | _not analysed_ |
| corecaptured | TIER_2 | 2 | — | _not analysed_ |
| corerepaird | TIER_2 | 2 | — | _not analysed_ |
| coresymbolicationd | TIER_2 | 2 | — | _not analysed_ |
| crash_mover | TIER_2 | 2 | — | _not analysed_ |
| csfdiagnose | TIER_2 | 2 | — | _not analysed_ |
| ctkd | TIER_2 | 2 | — | _not analysed_ |
| dasd | TIER_2 | 2 | — | _not analysed_ |
| deleted | TIER_2 | 2 | — | _not analysed_ |
| demod_helper | TIER_2 | 2 | — | _not analysed_ |
| deviceaccessd | TIER_2 | 2 | — | _not analysed_ |
| devicecheckd | TIER_2 | 2 | — | _not analysed_ |
| devicedataresetd | TIER_2 | 2 | — | _not analysed_ |
| dhcp6d | TIER_2 | 2 | — | _not analysed_ |
| dietappleh16camerad | TIER_2 | 2 | — | _not analysed_ |
| diskarbitrationd | TIER_2 | 2 | — | _not analysed_ |
| diskimagesiod | TIER_2 | 2 | — | _not analysed_ |
| dockaccessoryd | TIER_2 | 2 | — | _not analysed_ |
| eligibilityd | TIER_2 | 2 | — | _not analysed_ |
| eventkitsyncd | TIER_2 | 2 | — | _not analysed_ |
| exfat.util | TIER_2 | 2 | — | _not analysed_ |
| facetimemessagestored | TIER_2 | 2 | — | _not analysed_ |
| fairplayd.H2 | TIER_2 | 2 | — | _not analysed_ |
| fileproviderctl | TIER_2 | 2 | — | _not analysed_ |
| findmydeviced | TIER_2 | 2 | — | _not analysed_ |
| fitcored | TIER_2 | 2 | — | _not analysed_ |
| fitcoresessiond | TIER_2 | 2 | — | _not analysed_ |
| fmflocatord | TIER_2 | 2 | — | _not analysed_ |
| fontservicesd | TIER_2 | 2 | — | _not analysed_ |
| footprint | TIER_2 | 2 | — | _not analysed_ |
| fsck_exfat | TIER_2 | 2 | — | _not analysed_ |
| fskitd | TIER_2 | 2 | — | _not analysed_ |
| gamed | TIER_2 | 2 | — | _not analysed_ |
| gamepolicyd | TIER_2 | 2 | — | _not analysed_ |
| geocorrectiond | TIER_2 | 2 | — | _not analysed_ |
| geod | TIER_2 | 2 | — | _not analysed_ |
| gputoolsserviced | TIER_2 | 2 | — | _not analysed_ |
| griddatad | TIER_2 | 2 | — | _not analysed_ |
| handwritingd | TIER_2 | 2 | — | _not analysed_ |
| hangreporter | TIER_2 | 2 | — | _not analysed_ |
| hangtracerd | TIER_2 | 2 | — | _not analysed_ |
| healthappd | TIER_2 | 2 | — | _not analysed_ |
| healthd | TIER_2 | 2 | — | _not analysed_ |
| hpmdiagnose | TIER_2 | 2 | — | _not analysed_ |
| iBooksSettings | TIER_2 | 2 | — | _not analysed_ |
| iCloud | TIER_2 | 2 | — | _not analysed_ |
| iCloudMailAccountUI | TIER_2 | 2 | — | _not analysed_ |
| iCloudQuota | TIER_2 | 2 | — | _not analysed_ |
| iCloudQuotaUI | TIER_2 | 2 | — | _not analysed_ |
| iCloudSettings | TIER_2 | 2 | — | _not analysed_ |
| iCloudSubscriptionOptimizerDaemon | TIER_2 | 2 | — | _not analysed_ |
| iMessage | TIER_2 | 2 | — | _not analysed_ |
| iMessageLite | TIER_2 | 2 | — | _not analysed_ |
| iOSDiagnostics | TIER_2 | 2 | — | _not analysed_ |
| iOSScreenSharing | TIER_2 | 2 | — | _not analysed_ |
| iTunesCloud | TIER_2 | 2 | — | _not analysed_ |
| iTunesStoreUI | TIER_2 | 2 | — | _not analysed_ |
| iWorkFileFormat | TIER_2 | 2 | — | _not analysed_ |
| iaptransportd | TIER_2 | 2 | — | _not analysed_ |
| icloudMCCKit | TIER_2 | 2 | — | _not analysed_ |
| icloudMailSettings | TIER_2 | 2 | — | _not analysed_ |
| icloudmailagent | TIER_2 | 2 | — | _not analysed_ |
| iconservicesagent | TIER_2 | 2 | — | _not analysed_ |
| idcredd | TIER_2 | 2 | — | _not analysed_ |
| imagent | TIER_2 | 2 | — | _not analysed_ |
| inboxupdaterd | TIER_2 | 2 | — | _not analysed_ |
| ind | TIER_2 | 2 | — | _not analysed_ |
| installd | TIER_2 | 2 | — | _not analysed_ |
| itunescloudd | TIER_2 | 2 | — | _not analysed_ |
| itunesstored | TIER_2 | 2 | — | _not analysed_ |
| libAHTRestore.dylib | TIER_2 | 2 | — | _not analysed_ |
| libANGLE-shared.dylib | TIER_2 | 2 | — | _not analysed_ |
| libARIServer.dylib | TIER_2 | 2 | — | _not analysed_ |
| libATCommandStudioDynamic.dylib | TIER_2 | 2 | — | _not analysed_ |
| libAccessibility.dylib | TIER_2 | 2 | — | _not analysed_ |
| libAppleArchive.dylib | TIER_2 | 2 | — | _not analysed_ |
| libAppleTCONUpdater.dylib | TIER_2 | 2 | — | _not analysed_ |
| libAppletTranslationLibrary.dylib | TIER_2 | 2 | — | _not analysed_ |
| libAudioToolboxUtility.dylib | TIER_2 | 2 | — | _not analysed_ |
| libBKDM2.dylib | TIER_2 | 2 | — | _not analysed_ |
| libBasebandCommandDriversMIPC.dylib | TIER_2 | 2 | — | _not analysed_ |
| libBasebandCommandDriversQMI.dylib | TIER_2 | 2 | — | _not analysed_ |
| libBasebandManager.dylib | TIER_2 | 2 | — | _not analysed_ |
| libBasebandManagerDAL.dylib | TIER_2 | 2 | — | _not analysed_ |
| libBasebandManagerICE.dylib | TIER_2 | 2 | — | _not analysed_ |
| libCommCenterBase.dylib | TIER_2 | 2 | — | _not analysed_ |
| libCommCenterCommandDrivers.dylib | TIER_2 | 2 | — | _not analysed_ |
| libCommCenterKCommandDrivers.dylib | TIER_2 | 2 | — | _not analysed_ |
| libCommCenterMCommandDrivers.dylib | TIER_2 | 2 | — | _not analysed_ |
| libCoreEntitlements_V2.dylib | TIER_2 | 2 | — | _not analysed_ |
| libCoreFP.dylib | TIER_2 | 2 | — | _not analysed_ |
| libCoreKE.dylib | TIER_2 | 2 | — | _not analysed_ |
| libCoreLSKD.dylib | TIER_2 | 2 | — | _not analysed_ |
| libEDR | TIER_2 | 2 | — | _not analysed_ |
| libETLDynamic.dylib | TIER_2 | 2 | — | _not analysed_ |
| libEmbeddedSystemAUs.dylib | TIER_2 | 2 | — | _not analysed_ |
| libFDR.dylib | TIER_2 | 2 | — | _not analysed_ |
| libFontParser.dylib | TIER_2 | 2 | — | _not analysed_ |
| libGPUCompilerImpl.dylib | TIER_2 | 2 | — | _not analysed_ |
| libGPUCompilerImplLazy.dylib | TIER_2 | 2 | — | _not analysed_ |
| libHSFilerDynamic.dylib | TIER_2 | 2 | — | _not analysed_ |
| libIOABP.dylib | TIER_2 | 2 | — | _not analysed_ |
| libIOACIPC.dylib | TIER_2 | 2 | — | _not analysed_ |
| libIOACIPCBB.dylib | TIER_2 | 2 | — | _not analysed_ |
| libIPTelephony.dylib | TIER_2 | 2 | — | _not analysed_ |
| libInFieldCollection.dylib | TIER_2 | 2 | — | _not analysed_ |
| libMIPCSdk.dylib | TIER_2 | 2 | — | _not analysed_ |
| libMemoryResourceException.dylib | TIER_2 | 2 | — | _not analysed_ |
| libMobileGestalt.dylib | TIER_2 | 2 | — | _not analysed_ |
| libMobileGestaltExtensions.dylib | TIER_2 | 2 | — | _not analysed_ |
| libNFC_HAL.dylib | TIER_2 | 2 | — | _not analysed_ |
| libPN548_API.dylib | TIER_2 | 2 | — | _not analysed_ |
| libPPM.dylib | TIER_2 | 2 | — | _not analysed_ |
| libRoseBooter.dylib | TIER_2 | 2 | — | _not analysed_ |
| libRoseUpdater.dylib | TIER_2 | 2 | — | _not analysed_ |
| libSCLM.dylib | TIER_2 | 2 | — | _not analysed_ |
| libSESShared.dylib | TIER_2 | 2 | — | _not analysed_ |
| libSEUpdater.dylib | TIER_2 | 2 | — | _not analysed_ |
| libSLAMDynamic.dylib | TIER_2 | 2 | — | _not analysed_ |
| libSavageRestoreInfo_iOS.dylib | TIER_2 | 2 | — | _not analysed_ |
| libSavageUpdater_iOS.dylib | TIER_2 | 2 | — | _not analysed_ |
| libSecureMAHelper.dylib | TIER_2 | 2 | — | _not analysed_ |
| libSessionUtility.dylib | TIER_2 | 2 | — | _not analysed_ |
| libSoftwareUpdateSSO.dylib | TIER_2 | 2 | — | _not analysed_ |
| libSparse.dylib | TIER_2 | 2 | — | _not analysed_ |
| libSystemDetermination.dylib | TIER_2 | 2 | — | _not analysed_ |
| libSystemHealth.dylib | TIER_2 | 2 | — | _not analysed_ |
| libTLE.dylib | TIER_2 | 2 | — | _not analysed_ |
| libTelephonyCapabilities.dylib | TIER_2 | 2 | — | _not analysed_ |
| libTelephonyIOKitDynamic.dylib | TIER_2 | 2 | — | _not analysed_ |
| libValidationCapsule.dylib | TIER_2 | 2 | — | _not analysed_ |
| libVinylNonUpdater.dylib | TIER_2 | 2 | — | _not analysed_ |
| libVinylUpdater.dylib | TIER_2 | 2 | — | _not analysed_ |
| libafc.dylib | TIER_2 | 2 | — | _not analysed_ |
| libamsupport.dylib | TIER_2 | 2 | — | _not analysed_ |
| libboringssl.dylib | TIER_2 | 2 | — | _not analysed_ |
| libc++.1.dylib | TIER_2 | 2 | — | _not analysed_ |
| libcorecrypto.dylib | TIER_2 | 2 | — | _not analysed_ |
| libcorecrypto_noasm.dylib | TIER_2 | 2 | — | _not analysed_ |
| libcorecrypto_trace.dylib | TIER_2 | 2 | — | _not analysed_ |
| libcoreroutine.dylib | TIER_2 | 2 | — | _not analysed_ |
| libcryptex.dylib | TIER_2 | 2 | — | _not analysed_ |
| libcryptex_core.dylib | TIER_2 | 2 | — | _not analysed_ |
| libcryptex_interface.dylib | TIER_2 | 2 | — | _not analysed_ |
| libcryptex_trampoline.dylib | TIER_2 | 2 | — | _not analysed_ |
| libdns_services.dylib | TIER_2 | 2 | — | _not analysed_ |
| libdyld.dylib | TIER_2 | 2 | — | _not analysed_ |
| libfire7.dylib | TIER_2 | 2 | — | _not analysed_ |
| libhwtrace.dylib | TIER_2 | 2 | — | _not analysed_ |
| libindus.dylib | TIER_2 | 2 | — | _not analysed_ |
| liblog_location.dylib | TIER_2 | 2 | — | _not analysed_ |
| libmdns.dylib | TIER_2 | 2 | — | _not analysed_ |
| libmecab.dylib | TIER_2 | 2 | — | _not analysed_ |
| libmecabra.dylib | TIER_2 | 2 | — | _not analysed_ |
| libmorphun.dylib | TIER_2 | 2 | — | _not analysed_ |
| libnfrestore.dylib | TIER_2 | 2 | — | _not analysed_ |
| libnfshared.dylib | TIER_2 | 2 | — | _not analysed_ |
| libnwswifttls.dylib | TIER_2 | 2 | — | _not analysed_ |
| libobjc.A.dylib | TIER_2 | 2 | — | _not analysed_ |
| libpartition2_dynamic.dylib | TIER_2 | 2 | — | _not analysed_ |
| libpmenergy.dylib | TIER_2 | 2 | — | _not analysed_ |
| libquic.dylib | TIER_2 | 2 | — | _not analysed_ |
| libramrod.dylib | TIER_2 | 2 | — | _not analysed_ |
| libskit.dylib | TIER_2 | 2 | — | _not analysed_ |
| libswiftAVFoundation.dylib | TIER_2 | 2 | — | _not analysed_ |
| libswiftAccelerate.dylib | TIER_2 | 2 | — | _not analysed_ |
| libswiftAppleArchive.dylib | TIER_2 | 2 | — | _not analysed_ |
| libswiftCoreMedia.dylib | TIER_2 | 2 | — | _not analysed_ |
| libswiftCryptoTokenKit.dylib | TIER_2 | 2 | — | _not analysed_ |
| libswiftDarwin.dylib | TIER_2 | 2 | — | _not analysed_ |
| libswiftDispatch.dylib | TIER_2 | 2 | — | _not analysed_ |
| libswiftMetal.dylib | TIER_2 | 2 | — | _not analysed_ |
| libswiftObservation.dylib | TIER_2 | 2 | — | _not analysed_ |
| libswiftPrespecialized.dylib | TIER_2 | 2 | — | _not analysed_ |
| libswiftRemoteMirror.dylib | TIER_2 | 2 | — | _not analysed_ |
| libswiftSwiftOnoneSupport.dylib | TIER_2 | 2 | — | _not analysed_ |
| libswiftXPC.dylib | TIER_2 | 2 | — | _not analysed_ |
| libswift_Concurrency.dylib | TIER_2 | 2 | — | _not analysed_ |
| libswift_StringProcessing.dylib | TIER_2 | 2 | — | _not analysed_ |
| libswiftos.dylib | TIER_2 | 2 | — | _not analysed_ |
| libsystem_c.dylib | TIER_2 | 2 | — | _not analysed_ |
| libsystem_c_debug.dylib | TIER_2 | 2 | — | _not analysed_ |
| libsystem_coreservices.dylib | TIER_2 | 2 | — | _not analysed_ |
| libsystem_info.dylib | TIER_2 | 2 | — | _not analysed_ |
| libsystem_kernel.dylib | TIER_2 | 2 | — | _not analysed_ |
| libsystem_platform.dylib | TIER_2 | 2 | — | _not analysed_ |
| libsystem_platform_debug.dylib | TIER_2 | 2 | — | _not analysed_ |
| libsystem_sanitizers.dylib | TIER_2 | 2 | — | _not analysed_ |
| libsystem_trace.dylib | TIER_2 | 2 | — | _not analysed_ |
| libsystem_trace_debug.dylib | TIER_2 | 2 | — | _not analysed_ |
| libusrtcp.dylib | TIER_2 | 2 | — | _not analysed_ |
| libvoiced_tts.dylib | TIER_2 | 2 | — | _not analysed_ |
| libwebrtc.dylib | TIER_2 | 2 | — | _not analysed_ |
| libxpc.dylib | TIER_2 | 2 | — | _not analysed_ |
| lifs | TIER_2 | 2 | — | _not analysed_ |
| linkd | TIER_2 | 2 | — | _not analysed_ |
| localspeechrecognition | TIER_2 | 2 | — | _not analysed_ |
| lockdownmoded | TIER_2 | 2 | — | _not analysed_ |
| lskdd | TIER_2 | 2 | — | _not analysed_ |
| mDNSResponder | TIER_2 | 2 | — | _not analysed_ |
| maild | TIER_2 | 2 | — | _not analysed_ |
| maphelperservice | TIER_2 | 2 | — | _not analysed_ |
| mapssyncd | TIER_2 | 2 | — | _not analysed_ |
| mediaanalysisd | TIER_2 | 2 | — | _not analysed_ |
| mediaanalysisd-service | TIER_2 | 2 | — | _not analysed_ |
| medialibraryd | TIER_2 | 2 | — | _not analysed_ |
| migrationd | TIER_2 | 2 | — | _not analysed_ |
| milod | TIER_2 | 2 | — | _not analysed_ |
| misd | TIER_2 | 2 | — | _not analysed_ |
| mlruntimed | TIER_2 | 2 | — | _not analysed_ |
| mmaintenanced | TIER_2 | 2 | — | _not analysed_ |
| mobile_diagnostics_relay | TIER_2 | 2 | — | _not analysed_ |
| mobile_obliterator | TIER_2 | 2 | — | _not analysed_ |
| mobile_storage_proxy | TIER_2 | 2 | — | _not analysed_ |
| mobileactivationd | TIER_2 | 2 | — | _not analysed_ |
| mobileassetd | TIER_2 | 2 | — | _not analysed_ |
| mobilerepaird | TIER_2 | 2 | — | _not analysed_ |
| modelcatalogd | TIER_2 | 2 | — | _not analysed_ |
| modelcatalogdump | TIER_2 | 2 | — | _not analysed_ |
| modelmanagerd | TIER_2 | 2 | — | _not analysed_ |
| momentsd | TIER_2 | 2 | — | _not analysed_ |
| motiontrackingd | TIER_2 | 2 | — | _not analysed_ |
| mscamerad-xpc | TIER_2 | 2 | — | _not analysed_ |
| nanomapscd | TIER_2 | 2 | — | _not analysed_ |
| nanotimekitcompaniond | TIER_2 | 2 | — | _not analysed_ |
| navd | TIER_2 | 2 | — | _not analysed_ |
| ndoagent | TIER_2 | 2 | — | _not analysed_ |
| networkserviceproxy | TIER_2 | 2 | — | _not analysed_ |
| nsurlsessiond | TIER_2 | 2 | — | _not analysed_ |
| ospredictiond | TIER_2 | 2 | — | _not analysed_ |
| otctl | TIER_2 | 2 | — | _not analysed_ |
| parsec-fbf | TIER_2 | 2 | — | _not analysed_ |
| parsecd | TIER_2 | 2 | — | _not analysed_ |
| passcodenagd | TIER_2 | 2 | — | _not analysed_ |
| passwordbreachd | TIER_2 | 2 | — | _not analysed_ |
| pasted | TIER_2 | 2 | — | _not analysed_ |
| pcapd | TIER_2 | 2 | — | _not analysed_ |
| peakpowermanagerd | TIER_2 | 2 | — | _not analysed_ |
| peopled | TIER_2 | 2 | — | _not analysed_ |
| perfdata | TIER_2 | 2 | — | _not analysed_ |
| photoanalysisd | TIER_2 | 2 | — | _not analysed_ |
| photosfaced | TIER_2 | 2 | — | _not analysed_ |
| pointeruid | TIER_2 | 2 | — | _not analysed_ |
| powerd | TIER_2 | 2 | — | _not analysed_ |
| powerexperienced | TIER_2 | 2 | — | _not analysed_ |
| pppd | TIER_2 | 2 | — | _not analysed_ |
| privatecloudcomputed | TIER_2 | 2 | — | _not analysed_ |
| profiled | TIER_2 | 2 | — | _not analysed_ |
| promotedcontentd | TIER_2 | 2 | — | _not analysed_ |
| proximitycontrold | TIER_2 | 2 | — | _not analysed_ |
| ptpd | TIER_2 | 2 | — | _not analysed_ |
| racoon | TIER_2 | 2 | — | _not analysed_ |
| rapportd | TIER_2 | 2 | — | _not analysed_ |
| remindd | TIER_2 | 2 | — | _not analysed_ |
| remoted | TIER_2 | 2 | — | _not analysed_ |
| remotemanagementd | TIER_2 | 2 | — | _not analysed_ |
| restoreserviced | TIER_2 | 2 | — | _not analysed_ |
| retimerd | TIER_2 | 2 | — | _not analysed_ |
| rtadvd | TIER_2 | 2 | — | _not analysed_ |
| rtcreportingd | TIER_2 | 2 | — | _not analysed_ |
| safetyalertsd | TIER_2 | 2 | — | _not analysed_ |
| searchpartyd | TIER_2 | 2 | — | _not analysed_ |
| security-sysdiagnose | TIER_2 | 2 | — | _not analysed_ |
| securityuploadd | TIER_2 | 2 | — | _not analysed_ |
| seld | TIER_2 | 2 | — | _not analysed_ |
| sensorkitd | TIER_2 | 2 | — | _not analysed_ |
| sharingd | TIER_2 | 2 | — | _not analysed_ |
| shazamd | TIER_2 | 2 | — | _not analysed_ |
| siriactionsd | TIER_2 | 2 | — | _not analysed_ |
| siriinferenced | TIER_2 | 2 | — | _not analysed_ |
| slurpAPFSMeta | TIER_2 | 2 | — | _not analysed_ |
| sm_stats | TIER_2 | 2 | — | _not analysed_ |
| softposreaderd | TIER_2 | 2 | — | _not analysed_ |
| spindump | TIER_2 | 2 | — | _not analysed_ |
| spindump_fileparser | TIER_2 | 2 | — | _not analysed_ |
| sportsd | TIER_2 | 2 | — | _not analysed_ |
| spotlightknowledged | TIER_2 | 2 | — | _not analysed_ |
| sptm.t8140.release.im4p | TIER_2 | 2 | — | _not analysed_ |
| storekitd | TIER_2 | 2 | — | _not analysed_ |
| swcagent | TIER_2 | 2 | — | _not analysed_ |
| swcd | TIER_2 | 2 | — | _not analysed_ |
| swcutil | TIER_2 | 2 | — | _not analysed_ |
| swtransparencyd | TIER_2 | 2 | — | _not analysed_ |
| sysdiagnose | TIER_2 | 2 | — | _not analysed_ |
| sysdiagnose_helper | TIER_2 | 2 | — | _not analysed_ |
| sysdiagnosed | TIER_2 | 2 | — | _not analysed_ |
| sysstatuscheck | TIER_2 | 2 | — | _not analysed_ |
| tailspind | TIER_2 | 2 | — | _not analysed_ |
| taskinfo | TIER_2 | 2 | — | _not analysed_ |
| tccd | TIER_2 | 2 | — | _not analysed_ |
| terminusd | TIER_2 | 2 | — | _not analysed_ |
| teslad | TIER_2 | 2 | — | _not analysed_ |
| textcontextd | TIER_2 | 2 | — | _not analysed_ |
| textunderstandingd | TIER_2 | 2 | — | _not analysed_ |
| thermalmonitord | TIER_2 | 2 | — | _not analysed_ |
| timed | TIER_2 | 2 | — | _not analysed_ |
| tipsd | TIER_2 | 2 | — | _not analysed_ |
| transparencyd | TIER_2 | 2 | — | _not analysed_ |
| trustd | TIER_2 | 2 | — | _not analysed_ |
| uarppersonalizationd | TIER_2 | 2 | — | _not analysed_ |
| umtool | TIER_2 | 2 | — | _not analysed_ |
| usbctelemetryd | TIER_2 | 2 | — | _not analysed_ |
| usbsmartcardreaderd | TIER_2 | 2 | — | _not analysed_ |
| usermanagerd | TIER_2 | 2 | — | _not analysed_ |
| videosubscriptionsd | TIER_2 | 2 | — | _not analysed_ |
| visioncompaniond | TIER_2 | 2 | — | _not analysed_ |
| vmd | TIER_2 | 2 | — | _not analysed_ |
| voicebankingd | TIER_2 | 2 | — | _not analysed_ |
| voicememod | TIER_2 | 2 | — | _not analysed_ |
| vot | TIER_2 | 2 | — | _not analysed_ |
| wapic | TIER_2 | 2 | — | _not analysed_ |
| watchlistd | TIER_2 | 2 | — | _not analysed_ |
| weatherd | TIER_2 | 2 | — | _not analysed_ |
| webbookmarksd | TIER_2 | 2 | — | _not analysed_ |
| wifid | TIER_2 | 2 | — | _not analysed_ |
| wifivelocityd | TIER_2 | 2 | — | _not analysed_ |
| xpcproxy | TIER_2 | 2 | — | _not analysed_ |
| zprint | TIER_2 | 2 | — | _not analysed_ |

</details>

## HIGH_SIGNAL — excluded, low/no security relevance (2050)

<details><summary>Show 2050 components</summary>

- AAAFoundationSwift
- AAUIViewService
- ACCAppLinksIconService
- ACCFeatureAudioProductService
- AGXCompilerConnection-S2A8
- AGXCompilerCore-S2A8
- AHTUserEventAgent
- AIMLInstrumentationStreams
- ALDataTypes.dylib
- AMPCoreUI
- ARKit
- ARKitUI
- ARTraceModule
- ASIOKit
- AUHostingServiceXPC_arrow
- AV1SW.videodecoder
- AVAudioDeviceTestService
- AVFoundation
- AXActionSheetUIServer
- AXAggregateStatisticsServer
- AXAssetAndDataServer
- AXAssetLoader
- AXAuditAXUIService
- AXBuddyBundle
- AXElementInteraction
- AXFeatureOverrideServer
- AXFrontBoardUtils
- AXHapticMusicServer
- AXIDSServer
- AXIDSServices
- AXMediaUtilities
- AXMotionCuesServices
- AXNTKUtilities
- AXRuntime
- AXSoundDetection
- AXSpringBoardServerInstance
- AXUIViewService
- AXUltronPluginService
- AXWatchRemoteScreenServices
- AXWatchRemoteScreenUI
- AXWatchRemoteScreenUIServer
- AccessibilityAudit
- AccessibilityBridgeSetup
- AccessibilityDataMigration
- AccessibilityFocusEngine
- AccessibilityHeadphoneLevelsControlCenterModule
- AccessibilityLiveListenControlCenterModule
- AccessibilityMotionCuesControlCenterModule
- AccessibilityPhysicalInteraction
- AccessibilitySettingsLoader
- AccessibilitySettingsUI
- AccessibilityShorcutsModule
- AccessibilitySoundDetectionControlCenterModule
- AccessibilityTextSizeModule
- AccessibilityUI
- AccessibilityUIServer
- AccessoryNowPlaying
- AccessoryTimeSync
- AccessoryiAP2Shim
- AccountSettingsUI
- AcousticId-Assistant
- AcousticMaterials
- ActivityAwardsClient
- ActivityAwardsCore
- ActivityAwardsPlugin
- ActivityAwardsServices
- ActivityBridgeSetup
- ActivityComplicationBundleCompanion
- ActivityDigitalSeparation
- ActivityProgressKit
- ActivityRingsUI
- ActivitySharing
- ActivitySharingClient
- ActivitySharingUI
- ActivityUIServices
- AdAttributionKitDeveloperSettings
- AdCore
- AdID
- AddressBook-Assistant
- AddressBookUIFramework
- AegirProxyApp
- AirDrop
- AirDropSettings
- AirDropSettingsSupport
- AirDropUI
- AirFair2
- AirPlayAndHandoffSettings
- AirPlayAndHandoffSettingsSupport
- AirPlayKit
- AirPlayMirroringModule
- AirPlayReceiverKit
- AirPlaySenderKit
- AirPlaySenderUIApp
- AirPortAssistant
- AirPortSettings
- AirTraffic
- AirTrafficSettings
- AlarmFlowPlugin
- AlarmUIFramework
- AlarmUIPlugin
- AltruisticBodyPoseKit
- AmbientSettings
- AmbientUI
- Animoji
- AnnotationKit
- Announce
- AppConduit
- AppDeletionUIHost
- AppInstallExtension
- AppInstallation
- AppInstallationMetrics
- AppPredictionIntentsHelperService
- AppPredictionToolsInternal
- AppProtectionDaemon
- AppProtectionUIHost
- AppSSODaemon
- AppSSOUI
- AppStoreFoundation
- AppStoreOverlays
- AppStoreUtilities
- AppSupportUI
- AppSystemSettings
- AppUserDataMigrator
- AppearanceModule
- AppleAOPAudioPlugin
- AppleBasebandManager
- AppleBasebandServices
- AppleBrailleTranslator
- AppleCV3DMOVKit
- AppleCV3DModels
- AppleCVA
- AppleCVAPhoto
- AppleDepthCore
- AppleDeviceManagementHIDFilter
- AppleEthernetSettingsPreferences
- AppleFSCompression
- AppleFlatBuffers
- AppleH15MCD
- AppleJPEG
- AppleJPEGXL
- AppleMIDIRTPDriver
- AppleMetalGLRenderer
- AppleProResSWDecoder.videodecoder
- AppleProResSWEncoder.videoencoder
- AppleSPUHIDStatistics
- AppleSauce
- AppleServiceToolkit
- AppleT6030
- AppleT8122
- AppleTimeSyncAudioClock
- AppleTopCaseHIDEventDriver
- AppleUSBTopCaseDriver
- Applications
- Arcade
- Archetype
- ArchiveService
- ArgumentParserInternal
- AskPermission
- AskPermissionUI
- AssetCacheServices
- AssetsLibrary
- Assignables
- AssistantBridgeSettings
- AssistantSettings
- AssistantSettingsFoundation
- AssistantUI
- AssistiveTouch
- AssistiveTouchUI
- AtomicsInternal
- AttributionWeeApp
- AudioAnalytics
- AudioAnalyticsBase
- AudioAnalyticsExternal
- AudioConferenceControlCenterModule
- AudioDataAnalysis
- AudioMessagesExtension
- AudioPasscode
- AudioServerDriverTransports_IOA2
- AudiogramIngestion
- AutoFillHelper
- AutoLoop
- AutomatedDeviceEnrollment
- AutomaticAssessmentConfiguration
- AvailabilityKit
- AvatarPickerMemojiPicker
- AvatarPoster
- BKAudiobooks
- BPSStingSetup
- BTAvrcp
- BTD2DPlugin
- BTMap
- BackgroundSoundsCCModule
- BackgroundSystemTasks
- BacklightServices
- BacklightServicesHost
- BacklinkIndicator
- BarcodeScanner
- BasebandVoice
- Batteries
- BatteryCenterUI
- BatteryWidget
- BiomeDSL
- BiomePubSub
- BlastDoorPosterArchiveBridging
- BlissReader
- BlocklistSettings
- Bom
- BookEPUBWebProcessPlugin
- BookLibrary
- BooksPersonalization
- BrailleSymbology
- BreathingAlgorithms
- BridgeHealthSettings
- BridgeLiveActivity
- BridgeRemoteAccounts
- BridgeStoreExtension
- BrightnessControl
- BrookBridgeSettings
- BrookServices
- BrowserEngineCore
- BrowserEngineKit.Intermediary
- BrowserSupportKit
- BuiltinAudioPlugin
- Business
- BusinessChat
- BusinessChatFramework
- BusinessServices
- BusinessServicesUI
- C2
- CAMRootFlowPlugin
- CARDNDUI
- CBORLibrary
- CFNetworkAgent
- CGPDFService
- CIBarcode
- CIInpainting
- CIPassThrough
- CLKCompanionWatchFaceLibraryService
- CMCaptureDevice
- CPAnalytics
- CPUTrace
- CSExattrCrypto
- CSExattrCryptoService
- CSLCompanionLiveActivitiesSettings
- CTNotifyUIService
- CTParser
- CTParserService
- CVNLP
- CacheDeleteAppContainerCaches
- Calendar
- Calendar-Assistant
- CalendarFlowDelegatePlugin
- CalendarIntegrationSupport
- CalendarLink
- CalendarMigration
- CalendarSuggestions
- CalendarUIKitInternal
- CalendarUIPlugin
- CalendarWidget
- CallFiltering
- CallRecordingSettingsBundle
- CallScreeningSettingsBundle
- CameraEditKitFramework
- CameraKit
- CameraOverlayServices
- CarAssetUtils
- CarCommandsUIFramework
- CarKey
- CarModeModule
- CarPlayHalogen
- CarPlayServices
- CarPlaySetup
- CarPlaySplashScreen
- CarPlayTemplateUIHost
- CarPlayWallpaper
- CardKit
- Cards
- CarouselAppViewSettings
- CarouselLayoutSettings
- CarrierBundleUtilities.dylib
- CarrierSettings
- Catalyst
- Categories
- CategoriesService
- CellularBridgeSettings
- CellularSource
- CertInfo
- Charge
- ChargingViewService
- ChatKitAssistant
- ChatKitAssistantUI-Assistant
- ChatKitFramework
- CheckerBoardServices
- Cinematic
- CinematicFraming
- ClarityBoardFoundation
- ClarityCamera
- ClarityFoundation
- ClarityPhotos
- ClarityUIMessagesSettings
- ClarityUIMusicSettings
- ClarityUIPhoneFaceTimeSettings
- ClarityUIPhotosSettings
- ClassKitSettings
- ClassKitUI
- ClassroomKit
- ClassroomUIKit
- ClipServicesSettings
- ClipUIServices
- ClockAngel
- ClockFlowPlugin
- ClockPoster
- ClockUIFramework
- CloudDocsUI
- CloudKitCode
- CloudKitCodeProtobuf
- CloudKitDistributedSync
- CloudPhotoServices
- CloudSharingUI
- CloudTelemetry
- CognitiveHealth
- CollectionViewCore
- CollectionsInternal
- ColorPickerUIService
- ColourSensorFilterPlugin
- Combine
- CommCenterMobileHelper
- CommandAndControl
- CommandAndControlUI
- CommunicationSafetySettings
- CommunicationSafetySettingsUI
- Communications-iOS
- CommunicationsFilter
- CompanionAppBacklightPrivacySettings
- CompanionAppViewSetup
- CompanionAutoLaunchSettings
- CompanionBARSettings
- CompanionHealthDaemon
- CompanionHealthPlugin
- CompanionInternationalSettings
- CompanionReturnToClockSettings
- CompanionStingSettings
- CompanionSync
- CompanionWakeSettings
- Compass
- CompassSettings
- CompassViewCalibrationService
- ComplicationDisplay
- ConferenceRegistrationSettings
- ConfigurationEngineModel
- ConnectivityModule
- ContactPhotoCarouselRemoteAlert
- ContactProvider
- ContactsAutocomplete
- ContactsBackgroundColorService
- ContactsButtonXPCService
- ContactsFlowDelegatePlugin
- ContactsFlowUIPlugin
- ContactsSettings
- ContactsWidgetUI
- ContextService
- ContextSync
- ContextualUnderstanding
- ContinuityCaptureAgent
- ContinuityDisplay
- ControlCenterServices
- ControlCenterSettings
- ControlCenterUIServices
- CookingData
- CookingSupport
- CoordinationCore
- CoreAnalytics
- CoreAutoLayout
- CoreCDPUIInternal
- CoreCaptureControl
- CoreDAV
- CoreDuetContext
- CoreGEM.dylib
- CoreHID
- CoreIDVPAD
- CoreIndoor
- CoreLocationProtobuf
- CoreLocationUI
- CoreMLModelSecurityService
- CoreMaterial
- CoreMotionAlgorithms
- CoreNavigation
- CoreOCModules
- CoreOptimization
- CorePhoneNumbers
- CorePrediction
- CoreRCPlugin
- CoreRepairCoreXPCService
- CoreRoutineSettings
- CoreSVG
- CoreServicesInternal
- CoreServicesStore
- CoreSpeechXPC
- CoreSuggestionsML
- CoreText
- CoreThemeDefinition
- CoreThreadRadio
- CoreTime
- CoreTransferable
- CoreUtilsExtras
- CoreUtilsUI
- CoreVideo
- CosmeticAssessment
- Cosmo
- CreateMLComponents
- CredentialSharingUIViewService
- CrisisResources
- CryptoKitCBridging
- CustomizeYourWatchPlugin
- DAAccountAuthenticator
- DACardDAV
- DADaemonCardDAV
- DADaemonEAS
- DADaemonSubCal
- DASubCal
- DDActionsService
- DSContinuityPairing
- DSNotesPlugin
- DSRemotePairing
- DVTInstrumentsUtilities
- DarwinDirectory
- DarwinDirectoryInternal
- DarwinDirectoryQuery
- DataAccessExpress
- DataDeliveryServices
- DataDetection
- DataFlow
- DataMigration
- DayStreamProcessorService
- DebugHierarchyKit
- DeepThought
- DeepVideoProcessingCore
- DefaultAppsSettings
- DefaultAppsSettingsUI
- DefaultContactlessAppSettingsUIPlugin
- DepthCompanionSettings
- DepthCompanionSetup
- DepthComplicationBundleCompanion
- DepthCore
- DesktopServicesHelper
- DeveloperToolsSupport
- DeviceDiscoveryExtension
- DeviceOMatic
- DeviceSharingServices
- DeviceSharingServicesCore
- DeviceSharingUI
- DeviceTreeKit
- DiagnosticsKit
- DiagnosticsReporter
- DiagnosticsService
- DiagnosticsSessionAvailabilityService
- DiagnosticsSupport
- DictionaryServices
- DictionarySettings
- DictionaryUI
- DigitalSeparationBundle
- DigitalSeparationSettings
- DigitalTouchBalloonProvider
- DigitalTouchShared
- Disembark
- DisplayFilterUIServer
- DisplayModule
- DistributedTimers
- DistributedTimersDaemon
- DoNotDisturb
- DoNotDisturbKit
- DoNotDisturbModule
- DoNotDisturbSettings
- DockKit
- DonationAccountWatcher
- DoseSettings
- DoubleAgent
- DrawingKit
- DriverKit
- DriverKitSettings
- DriverManagement
- DropIn
- DropInCore
- DropletUI
- DualSenseHIDServicePlugin
- DualShock4HIDServicePlugin
- DurianUpdaterService
- Duxbury
- EAGLReplayControllerSupport
- EAP8021X
- EAPOLController
- EDPSecurity
- ESAccountAuthenticator
- ESDaemonSupport
- EdutainmentFlowPlugin
- EmailAddressing
- EmergencyAlerts
- EmergencyFlowPlugin
- EmojiKit
- EmojiPoster
- EncoreXPCService
- EquationKit
- EventKitSyncServices
- EventKitTCCUI
- EventKitUIFramework
- ExchangeSync
- ExchangeSyncExpress
- ExclaveFDRDecode
- ExternalAccessory
- EyeReliefUI
- Eyedropper
- FMFUI
- FMNetworking
- FPCKService
- FSEvents
- FaceTimeFeatureControl
- FacebookSettings
- Family
- FamilyControls
- FamilyControlsAgent
- FeatureFlagsSupport
- Feedback
- Feedback Assistant iOS
- FeedbackRemoteView
- FeedbackService
- FileProviderOverride
- FileProviderUI
- FinHealth
- FinanceImageProcessingService
- FinanceStub
- FindMyDaemonSupport
- FindMyDeviceBTDiscoveryXPCService
- FindMyDeviceEmergencyCallInfoPublisherXPCService
- FindMyDeviceEraseXPCService
- FindMyDeviceIdentityXPCService
- FindMyDeviceSharedConfigurationXPCService
- FindMyFlowPlugin
- FindMyItemsDigitalSeparation
- FindMyLocate
- FindMyLocateObjCWrapper
- FindMyMessagesApp
- FindMyMessaging
- FindMyPeopleDigitalSeparation
- FindMyStorage
- FindMyUIPlugin
- FindMyUnsafeAsyncBridging
- FitnessApp
- FitnessAppRoot
- FitnessCoaching
- FitnessCoachingCore
- FitnessCoachingHealthServices
- FitnessCoreUI
- FitnessForYou
- FitnessRemoteBrowsing
- FitnessSharePlaySession
- FitnessSiriSession
- FitnessTrainerTips
- FitnessUtilities
- FlashlightModule
- FlightUtilities
- FlowFrameKit
- FocusUIModule
- FontPicker
- FontPickerUIService
- FontServices
- FramePacing
- FreeformSettings
- FullKeyboardAccess
- FusionTracker
- Futhark
- GAXApp
- GKSPerformance
- GLTools
- GLToolsCore
- GNSSLocationService
- GPUToolsiOS
- GSS
- Game Center
- GameCenterDashboardExtension
- GameCenterPrivateUIFramework
- GameCenterServerClient
- GameCenterSettings
- GameCenterUIFramework
- GameCenterUIService
- GameCenterWidgets
- GameControllerSettings
- GameControlleriOSSettings
- GameKitFramework
- GameplayKit
- GeneralKnowledge-Assistant
- GenerativeAssistantUIPlugin
- GenerativeExperiences
- GenerativeExperiencesUI
- GenerativeFunctions
- GenericGamepadHIDServicePlugin
- GenericHID
- GeoUIFramework
- GeoUIPlugin
- GradientPoster
- GraphicsServices
- GroupSessionService
- GuestUserHandoverSetup
- H10ISPServices
- H16ISPServices
- H264H8.videodecoder
- H264SW.videocodec
- HIDRMServiceFilter
- HIDRMSessionFilter
- HMAssistant
- HTTPTypesInternal
- HandwritingProvider
- HangHUD
- HangTracerSettingsClient
- Haptics
- HashtagImagesExtension
- HeadGestures
- HeadphoneAccommodationsCCModule
- HeadphoneConfigs
- HeadphoneProxFeatureService
- HeadphoneSettings
- HealthActivityCache
- HealthAndFitnessPlugin
- HealthAppDiagnosticExtensionPlugin
- HealthAppsSettings
- HealthBalance
- HealthBalanceDaemonPlugin
- HealthBalanceUI
- HealthBridgePrivacySettings
- HealthBridgeSetupPlugin
- HealthDaemonFeatures
- HealthDaemonFeaturesPlugin
- HealthDomainsTools
- HealthFeatures
- HealthFlowDelegatePlugin
- HealthHearing
- HealthHearingDaemon
- HealthKitAdditions
- HealthKitUI
- HealthMedications
- HealthMedicationsDaemonPlugin
- HealthMedicationsVision
- HealthMenstrualCycles
- HealthMenstrualCyclesDaemon
- HealthMenstrualCyclesUI
- HealthMenstrualCyclesWidgetUI
- HealthMobilityDaemon
- HealthRecordsSettings
- HealthRecordsWalletSupport
- HealthSafety
- HearingAidUIServer
- HearingAidsModule
- HearingApp
- HearingDevicesCCModule
- HearingMLHelper
- HearingModeService_Private
- HearingModeUI
- HearingSettings
- HeartRateBridgePlugin
- HeartRateSettings
- HeartRhythmUI
- Heimdal
- HelpKit
- HeroDataClient
- HistoricalAnalyzerService
- HomeAI
- HomeAutomationUIFramework
- HomeCaptiveViewService
- HomeCommunicationFlowDelegatePlugin
- HomeCommunicationUIFramework
- HomeCommunicationUIPlugin
- HomeControlCenterCompactModule
- HomeControlService
- HomeKitCore
- HomeKitEventRouter
- HomeMessagingUtils
- HomePlatformSettingsUI
- HomeRecommendationEngine
- HomeScreenSettings
- HomeSharing
- HomeUICommon
- HomeUIService
- HomeUtilityServices
- HomeWidgetIntents
- HoverTextServices
- HoverTextUIServer
- HumanUnderstandingEvidence
- HumanUnderstandingFoundation
- ICBSettingsBundle
- ICSSettingsBundle
- IDEDebugGaugeDataProviders
- IDSBlastDoorSupport
- IDSHashPersistence
- IDSKVStore
- IMAssistantCore
- IMAutomaticHistoryDeletionAgent
- IMCorePipeline
- IMDPersistenceAgent
- IMSharedUI
- IMTranscoding
- IOAccelMemoryInfoCollector
- IOAnalytics
- IOHIDPointerScrollFilter
- IOHIDSensorPowerLoggingFilter
- IOMFB_bics_daemon
- IOSurfaceAccelerator
- IOUIAngel
- ITMLKit
- IdentityFlowPlugin
- IdentityLookup
- IdleTimerServices
- ImageHarmonizationKit
- InCallLockScreen
- IncomingCall
- InertiaCam
- InputToolKit
- InputToolKitUI
- InputTranscoder
- InputUI
- InstalledApps
- IntelligenceFlowAppIntentsPreviewToolSupport
- IntelligenceFlowContext
- IntelligenceFlowFeedbackDataCollector
- IntelligenceFlowShared
- IntelligencePlatformCompute
- IntelligencePlatformComputeService
- IntelligentLight
- IntelligentRoutingMediaBundles
- IntelligentRoutingServices
- IntelligentTrackingCore
- IntentsServices
- IntentsUI
- InteractiveLegacyProfilesSubscriber
- InternalSwiftProtobuf
- InternationalSettings
- InternationalSupport
- IntlPreferences
- IntlPreferencesUI
- InvertColorsManager
- IsolatedCoreAudioClient
- JPEGH1.videodecoder
- JPEGH1.videoencoder
- Jet
- JoyConHIDServicePlugin
- KRExperiments
- KeyboardArbiter
- KeyboardMigrator
- KeyboardServices
- KeyboardSettings
- Keyboards
- KeychainDataclassOwner
- KeynoteQuicklook
- KnowledgeGraphKit
- Koa
- LACC
- LanguageModeling
- LatentSemanticMapping
- LeakAgent
- LegacyProfilesSubscriber
- LegalAndRegulatorySettings
- LiblouisBrailleTranslator
- LiftUI
- LighthouseAV
- LighthouseBitacoraFramework
- LighthouseDataProcessor
- LighthouseQuartz
- LighthouseServicesAnalyticsFramework
- LinguisticData
- LinkSource
- LiveExecutionResultsFoundation
- LiveExecutionResultsProbe
- LiveFSFPHelper
- LiveSpeechServices
- LiveSpeechUI
- LiveSpeechUIService
- LiveTranscriptionUI
- LockdownMode
- Logging
- LoginUI
- LoginUILogViewer
- LunaHIDServicePlugin
- MBATCPlugin
- MBHelperApp
- MBHelperService
- MCProfile
- MFAANetwork
- MIBULoopbackServerHelper
- MLCompilerOSXPC
- MLCompilerRuntime
- MLCompilerServices
- MLCompute
- MLKit
- MLModelSpecification
- MMCS
- MMCSServices
- MP4VH8.videodecoder
- MPSCore
- MPSImage
- MPSMatrix
- MPSNeuralNetwork
- MPSRayIntersector
- MSUDataAccessor
- MTLAssetUpgraderD
- MTLSpline
- MTLToolsDeviceSupport
- Magnifier
- MagnifierAngel
- MagnifierServices
- Mail
- Mail-Assistant
- MailAccountSettings
- MailAttachmentPlugin
- MailFlowDelegatePlugin
- MailServices
- MailVIPWidget
- ManagedApp
- ManagedOrganizationContacts
- ManagedSettings
- ManagedSettingsSubscriber
- ManagedSettingsUI
- ManifestStorageService
- MapKitFramework
- MapKitSwiftUI
- Maps-Assistant
- MapsDigitalSeparation
- MaterialKit
- MeasureFoundation
- MeasureSettings
- MediaAccessibility
- MediaAnalysisBlastDoorService
- MediaAnalysisBlastDoorSupport
- MediaAnalysisPhotosServices
- MediaControlSender
- MediaControlsAudioModule
- MediaControlsModule
- MediaFoundation
- MediaMLServices
- MediaPlayerFramework
- MediaPlayerUIFramework
- MediaSafetyNet
- MediaStream
- Memories
- MentalHealth
- MentalHealthUI
- MentalHealthWidgetUI
- MessageSecurity
- MessageUIFramework
- MessagesAirlockService
- MessagesBlastDoorSupport
- MessagesBridgeSettings
- MessagesPairingRegistration
- MessagesSettingsUI
- MetalKit
- MetricMeasurementHelper
- MilAneflow
- MindComplicationBundleCompanion
- MindRelevanceEngineDataSource
- MobileActivation
- MobileActivationMigrator
- MobileBackupCacheDeleteService
- MobileCalSettings
- MobileIdentityServiceUI
- MobileSMS
- MobileSafariFramework
- MobileSlideShow
- MobileSlideShowSettings
- MobileSoftwareUpdate
- MobileStore
- MobileStoreDemoSetupUI
- MobileTimer-Assistant
- MobileTimerFramework
- MobileTimerUI
- MobileTimerUIFramework
- ModalityXObjects
- ModelIO
- ModelMonitoringLighthouse
- MomentsUIServiceCore
- MonogramPoster
- MonogramPosterExtension
- Montreal
- MorphunAssets
- MorphunSwift
- MotionSensorLogging
- Movies-Assistant
- MultitouchSupport
- MusicKitPlaybackSupport
- MusicMessagesApp
- MusicSettingsSupport
- MusicStoreUI
- MusicUsage
- MuteModule
- NDOAPI
- NFC
- NFCControlCenterModule
- NLPLearner
- NTKCTritiumSettings
- NTKCellularConnectivityCompanionComplicationBundle
- NTKFaceSnapshotService
- NTKTimelyComplications
- NTKTimerComplicationBundle
- NTKUltraCubeFaceBundleCompanion
- NanoAudioControl
- NanoBedtimeBridgeSettings
- NanoBooksBridgeSettings
- NanoCalendarBridgeSettings
- NanoCalendarComplicationsCompanion
- NanoCalendarPingSubscriber
- NanoContactsBridgeSettingsOther
- NanoContactsBridgeSettingsPaired
- NanoHomeIntents
- NanoHomeScreenServices
- NanoHomeScreenUIServices
- NanoMailKitServer
- NanoMapsBridgeSettings
- NanoMediaAPI
- NanoMediaBridgeUI
- NanoMenstrualCyclesComplication
- NanoMusicBridgeSettings
- NanoNetAppsUI
- NanoPeopleBridgeSettings
- NanoPhotosBridgeSettings
- NanoPhotosCore
- NanoRemindersComplication
- NanoTimeKitCompanion
- NanoTipsBridgeSettings
- Nearby
- NearbySessions
- NetworkStatistics
- NetworkUplinkClock
- Nexus
- NexusDaemon
- NotebookFlowPlugin
- NotebookUIPlugin
- NotesAnalytics
- NotesPreviewKit
- NotesUIServices
- NowPlaying-iOS
- NumberAdder
- NumberAdderService
- NumbersQuicklook
- ODCurareAnalysis
- ODCurareEvaluationAndReporting
- ODDIFramework
- OOBBTPairing-iOS
- OSLog
- OTEAutomationTest
- OTSVG
- ObjectUnderstanding
- OctaviaHalogen
- OnBoardingKit
- OpenAL
- OpenAPIRuntimeInternal
- OpenAPIURLSessionInternal
- OpusKit
- OrientationLockModule
- Osprey
- OverlayUI
- PCSReadingFlowDelegatePlugin
- PDSAgent
- PIRGeoProtos
- POP
- PPPController
- PagesQuicklook
- PairedSync
- PairingProximity
- PaperKit
- ParsecModel
- ParsecSubscriptionServiceSupport
- ParsingInternal
- PassKitFramework
- PassKitServices
- PassbookDataclassOwnerPlugin
- PassbookSecureUIService
- PassbookUISceneService
- PassbookUIService
- PasscodeSettingsSubscriber
- PaymentContactlessSettingsUIPlugin
- PaymentUI
- PearlEventFilter
- PeerPaymentMessagesExtension
- PegasusPersistence
- PencilPairingUI
- PerfPowerServicesEventListenerPlugin
- PerfPowerServicesSignpostReader
- PerfPowerTelemetryClientRegistrationService
- PerformanceTraceModule
- PersonaUI
- PersonalAudio
- PersonalIntelligenceCore
- Phoenix
- PhoneBridgeSettings
- PhoneNumberResolver
- PhoneSnippetUI
- PhoneSuggestions
- PhoneUIPlugin
- Photo Booth
- PhotoEditing
- PhotoLibrary
- PhotoLibraryFramework
- PhotoSharingPlugin
- PhotosCloudRecommendations
- PhotosEditUI
- PhotosFaceCore
- PhotosFaceLayout
- PhotosFramework
- PhotosImagingFoundation
- PhotosKnowledgeGraph
- PhotosMediaFoundation
- PhotosSearchClient
- PhotosSeparation
- PhotosStorageManagementSettings
- PhotosUIFramework
- PhotosUIService
- PhysicsKit
- PictureInPictureSettings
- PingMyWatchControlCenterUI
- Planks
- PlatterKit
- PlaybackControlsSuggestionsPlugin
- PlugInKit
- PlugInKitDaemon
- PnROnDeviceFramework
- PodcastsBridgeSettings
- PodcastsPodcastsTodayExtension
- PointerUIServices
- PoirotBlocks
- PoirotSchematizer
- PoirotUDFs
- PortraitFilters
- PostSiriEngagement
- PosterBoardFramework
- PosterPlatformSupport
- PowerExperience
- PowerlogAccounting
- PreferencesExtended
- PreferencesFramework
- PreferencesMigrator
- PreferencesUI
- PreviewShell
- PreviewShellKit
- PreviewUI
- PreviewsInjection
- PreviewsMessagingOS
- PreviewsOSSupportUI
- PreviewsServices
- PreviewsServicesUI
- PrintKit
- PrivacyAccounting
- PrivacyDisclosureUI
- PrivateSearchClient
- PrivateSearchCore
- PrivateSearchProtocols
- ProactiveDaemonSupport
- ProactiveInputPredictions
- ProactiveML
- ProactiveSummarizationClient
- ProactiveSupportStubs
- ProductKitViewer
- ProductPageExtension
- ProgressUI
- PromotedContentPrediction
- PromptKit
- ProofReader
- ProtoDataExtractor
- ProtocolBuffer
- PrototypeTools
- PrototypeToolsUI
- ProxCardKit
- Proximity
- ProximityControl
- ProximityReaderSceneUI
- ProximityReaderUIService
- ProximityUI
- QLCharts
- QuickTime Plugin
- RTBuddyCrashlogDecoder
- RTCReporting
- RTTUI
- RTTUtilities
- Radio
- RapportUI
- ReaderFlowPlugin
- RealityKit
- RealityKitInspection
- Recap
- RecapPerformanceTesting
- RecentlyPlayedTodayExtension
- RecentsAvocado
- Recount
- ReflectionInternal
- RelativeMotion
- RelevanceEngineReminders
- RelevanceEngineUI
- RemindersAppIntents
- RemindersDES
- RemindersDataclassOwnerPlugin
- RemindersIntentsFramework
- RemoteConfiguration
- RemoteManagementModel
- RemoteMediaServices
- RemotePairingDevice
- RemotePaymentPassActionsService
- RemoteServiceDiscovery
- RemoteUIFramework
- RemoteXPC
- ReplyWithMessageSettings
- ReportMemoryException
- ReportSystemMemory
- RespiratoryHealth
- RespiratoryHealthDaemon
- RespiratoryHealthSetupPlugin
- RespiratoryHealthUI
- ResponseKit
- ResponseUI
- Restaurants-Assistant
- RestorePostProcess
- RichLinkProvider
- RoomScanCore
- RuntimeInternal
- SAExtensionOrchestrator
- SAHelper
- SAML
- SCHelper
- SMBClientEngine
- SMSPreferences
- SOSSettings
- SOSUI
- SPFinder
- SPShared
- STAEAExtractionPlugin
- STSXPCHelperClient
- SafariBookmarksSyncAgent
- SafariUsageBundle
- SafetyAlerts
- SafetyKit
- SafetyMonitorApp
- SafetyMonitorMessages
- SafetyMonitorSeparation
- SafetyServiceFilter
- SafetySessionFlowPlugin
- SatelliteModule
- SaveToFiles
- SchoolTimeSettingsUI
- Screen Time
- ScreenContinuityServices
- ScreenContinuityShell
- ScreenReaderBrailleDriver
- ScreenReaderCore
- ScreenSharing
- ScreenSharingAccessibilityServer
- ScreenSharingAccessibilityService
- ScreenSharingKit
- ScreenSharingViewService
- ScreenTimeUICore
- ScreenTimeUnlock
- ScreenshotServicesFramework
- SearchAssets
- SearchSettings
- SearchToShareCore
- SearchUICardKitProviderSupport
- SecondaryCloudCallingSettingsBundle
- SecureElementCredential
- SecuritySubscriber
- SecurityUI
- SecurityUICore
- SemanticPerception
- SensingAlgsService
- SensingPredictXPCService
- SensorKitDataExport
- SensorKitHelper
- SensorKitSupport
- SentencePiece
- SentencePieceInternal
- SeparationAlerts
- ServiceExtensions
- ServiceExtensionsCore
- SessionAlert
- SessionAssertion
- SessionFilterPreferenceProvider
- SessionFoundation
- SessionSQL
- SessionSyncEngine
- Settings-Assistant
- SettingsHostUI
- SetupKit
- SeymourAwardsPlugin
- SeymourServerProtocol
- SeymourServicesCore
- SharePlaySettings
- SharedWebCredentials
- SharedWithYou
- SharedWithYouCore
- SharedWithYouFramework
- SharingHUDService
- SharingUIService
- Sidecar
- SidecarCore
- SignalCompression
- SignpostCollection
- SilenceCallsSettingBundle
- SilexVideo
- SimpleKeyExchange
- SiriAppResolution
- SiriAudioIntentUtils
- SiriAudioSnippetKit
- SiriAutoCompleteAPI
- SiriCalendarIntents
- SiriCarCommandsIntents
- SiriCloudKitAccountsNotifier
- SiriContactsCommon
- SiriContactsUI
- SiriCore
- SiriCoreMetrics
- SiriCorrections
- SiriCrossDeviceArbitrationFeedback
- SiriDailyBriefingInternal
- SiriDialogEngine
- SiriEmergencyIntents
- SiriExpanseInternal
- SiriExpanseInternalUI
- SiriExpanseInternalUIPlugin
- SiriFindMy
- SiriFindMyBundle
- SiriFindMyUI
- SiriFlowEnvironment
- SiriGeo
- SiriGeoSuggestions
- SiriGestureBridge
- SiriHeadlessService
- SiriIdentityInternal
- SiriInCall
- SiriInferenceFlow
- SiriInferenceFlowsUIPlugin
- SiriInferenceIntents
- SiriInformationSuggestionsPlugin
- SiriInformationUIPlugin
- SiriIntentEvents
- SiriKitFlow
- SiriKitFlowSnippetUIPlugin
- SiriKitInvocation
- SiriKitUIPlugin
- SiriLiminal
- SiriLinkSuggestionsPlugin
- SiriMASPFLTraining
- SiriMailInternal
- SiriMailOntology
- SiriMailUI
- SiriMailUIModel
- SiriMailUIPlugin
- SiriMessagesCommon
- SiriMessagesSettings
- SiriMessagesSuggestions
- SiriMetricsBugReporter
- SiriNLUOverrides
- SiriNaturalLanguageGeneration
- SiriNotebook
- SiriNotebookSuggestionsPlugin
- SiriOntology
- SiriOntologyProtobuf
- SiriPaymentsUIPlugin
- SiriPhoneIntents
- SiriPowerInstrumentation
- SiriPrivateLearningAnalytics
- SiriPrivateLearningInferencePlugin
- SiriPrivateLearningLogging
- SiriPrivateLearningPatternExtractionPlugin
- SiriPrivateLearningTTSMispronunciationPlugin
- SiriReaderIntents
- SiriReferenceResolution
- SiriReferenceResolutionDataModel
- SiriReferenceResolutionMetricsPlugin
- SiriReferenceResolver
- SiriRequestDispatcher
- SiriSignals
- SiriSocialConversation
- SiriSocialConversationUIPlugin
- SiriStates
- SiriSuggestionsAPI
- SiriSuggestionsIntelligence
- SiriSuggestionsUIPlugin
- SiriSystemCommandsIntents
- SiriTaskEngagement
- SiriTasksEvaluation
- SiriTimeAlarmInternal
- SiriTimeInternal
- SiriTimeSuggestionsPlugin
- SiriTimeTimerInternal
- SiriTranslationIntents
- SiriTranslationUI
- SiriTranslationUIPlugin
- SiriTurnRestatement
- SiriTurnTakingManager
- SiriUI
- SiriUIActivation
- SiriUIBridge
- SiriUICardKitProviderSupport
- SiriUICore
- SiriUserSegments
- SiriUtilities
- SiriVOX
- SiriVirtualDeviceResolution
- SiriWatchPairingSetup
- SiriXShimTools
- Siriland
- Sleep
- SleepHealth
- SmartIOFirmware_ASCv7.im4p
- SmartReplies
- SmartRepliesServer
- SmartRepliesUI
- SnippetCommands
- SnippetKit
- SnippetUI_Proto
- SocialFramework
- SocialWeeApp
- SoftwareUpdateController
- SoftwareUpdateCoreSupport
- SoftwareUpdateSettings
- SoftwareUpdateSubscriber
- SoundBoardServices
- SoundScapesUtility
- SpatialInspectorFoundation
- SpeakServer
- SpeakThisServices
- SpeechRecognitionSharedSupport
- SplashBoard
- Sports-Assistant
- SportsKit
- SpotlightEmbedding
- SpotlightRecommendation
- SpotlightSetting
- SpotlightSettingsSupport
- SpotlightUI
- SpotlightUIInternalFramework
- SpringBoardDisplay
- SpringBoardDisplayServices
- SpringBoardIntents
- SpringBoardUI
- Stateful
- StickerFoundationInternal
- StickersUI
- Stocks-Assistant
- StocksBridgeSettings
- StocksDataclassOwner
- StocksFramework
- StocksSettings
- StocksWidget
- StorageSettings
- StorageSettingsFramework
- StorageUI
- StoreBookkeeper
- StoreDemoViewService
- StoreKitFramework
- StrokeAnimation
- SubscribePageExtension
- SuggestionsSpotlightMetrics
- SummariesHealthDaemon
- SwiftASN1
- SwiftASN1Internal
- SwiftUIAccessibility
- Symbols
- SymptomAnalytics
- SymptomDiagnosticReporter
- SymptomLinkAdvisory
- SymptomPresentationFeed
- SymptomPresentationLite
- Synapse
- SyncedModels
- System-Assistant
- SystemActions
- SystemApertureUI
- SystemCommandsFlowDelegatePlugin
- SystemCommandsSuggestionsPlugin
- SystemPlugin
- SystemStatusServer
- TQQuicklook
- TSApplication
- TSCollaborationKit
- TSDrawables
- TSKit
- TSStyles
- TV
- TVLatency
- TVRemoteModule
- TVRemoteUIService
- TVSetupUIService
- TVUIKit
- Tabi
- TabularData
- TailspinSymbolicationServer
- TeaBreeze
- TeaCharts
- TeaFoundation
- TeaSettings
- TeaSnappy
- TelephonyBlastDoorService
- TelephonyUI
- TelephonyUIFramework
- TelephonyXPCClient
- TextFormattingUI
- TextGeneration
- TextGenerationInference
- TextInputCJK
- TextInput_cs
- TextInput_de
- TextInput_el
- TextInput_es
- TextInput_fr
- TextInput_haw
- TextInput_hi
- TextInput_ja
- TextInput_mr
- TextInput_nl
- TextInput_pa
- TextInput_sk
- TextInput_ta
- TextInput_tr
- TextInput_vi
- TextSettingsBridgeSetup
- TextToSpeechVoiceBankingUI
- ThirdPartyApplicationSettings
- TilesService
- TimerFlowDelegatePlugin
- TimerModule
- TimerUIPlugin
- TinCanSettings
- TipKitServices
- Tips
- TipsApp
- TipsWidgetExtension
- ToneLibrary
- TouchAccommodations
- TouchML
- TouchRemote
- TouchSensitiveButtonHIDService
- Translate
- TranslationAPISupport
- TranslationFlowDelegatePlugin
- TranslationPersistence
- TranslationUIProvider
- Transliteration
- TransparencyDetailsView
- TrialArchivingService
- TrialProto
- TrustedPeers
- TwitterFramework
- TypingDESPlugin
- TypistFramework
- UIIntelligenceIntents
- UITriggerVC
- UIUnderstanding
- URLCompression
- URLFormatting
- USDLib_FormatLoader
- UniformTypeIdentifiers
- UniversalDrag
- UniversalHID
- UpNext
- UsageSettings
- UserActivity
- UserFS
- UserFontServices
- UserSafetyUI
- VCH263.videodecoder
- VCH263.videoencoder
- VCPHEVC.videocodec
- VCPMP4V.videodecoder
- VFXAssets
- VectorSearch
- VictoriaSettings
- VideoEffect
- VideoSubscriberAccountSettings
- VideoSuggestionsPlugin
- Videos
- VideosExtrasFramework
- ViewHierarchyAgent
- VisionCompanionServices
- VisionCompanionSettings
- VisionHWAccelerationServices
- VisionKit
- VisualAlert
- VoiceControlSettings
- VoiceControlUI
- VoiceDial
- VoiceMemosSettings
- VoiceOver
- VolumeLimitSettings
- WAAnswer-Assistant
- WACEAService
- WGAEltonPhoneBuddyFlowPanel
- WGAEltonUsersSettingsPhone
- WalletBlastDoorService
- WalletBlastDoorSupport
- Wallpaper
- WallpaperKit
- WallpaperSettings
- WatchConnectivity
- WatchKit
- WatchQuickActionsServices
- WatchdogClient
- WeatherData
- WeatherExtensionBridgeSettings
- WebApp
- WebBookmarksSwift
- WebInspector
- WebPrivacy
- WebProcess
- WebProcessLoader
- WelcomeKitCore
- WelcomeKitUI
- WellnessFlowPlugin
- WellnessUI
- WiFiCloudAssetsXPCService
- WiFiDataMigrator
- WiFiVelocity
- WidgetConfigurationExtension
- WidgetPreviewsExtensionAgent
- WidgetPreviewsSupport
- WidgetRenderer_CarPlay
- WidgetRenderer_Default
- Widgets
- WirelessDiagnostics
- WirelessModemSettings
- WirelessProximity
- WorkflowUICore
- WorkoutAnnouncements
- WorkoutHealthBridge
- WorkoutKitServices
- WorkoutKitUI
- WritingTools
- XGBoostFramework
- XOJITExecutor
- XavierCore
- XboxGamepadHIDServicePlugin
- XboxOneHIDServicePlugin
- ZeoliteFramework
- ZoomServices
- _AVKit_SwiftUI
- _AdAttributionKit_StoreKit
- _AppIntentsServices_AppIntents
- _AppIntents_SwiftUI
- _AppIntents_UIKit
- _Coherence_CloudKit_Private
- _CoreData_CloudKit
- _CoreLocationUI_SwiftUI
- _CoreNFC_UIKit
- _DeviceActivity_SwiftUI
- _GameController_SwiftUI
- _HomeKit_SwiftUI
- _IconServices_SwiftUI
- _Intents_TipKit
- _MapKit_SwiftUI
- _MarketplaceKit_UIKit
- _PhotosUI_SwiftUI
- _SceneKit_SwiftUI
- _SpriteKit_SwiftUI
- _SwiftData_CoreData
- _Translation_SwiftUI
- _WorkoutKit_SwiftUI
- abm-helper
- abmlite
- acdiagnose
- activity-widget
- activityawardsd
- activitysharingd
- addaily
- afktool
- announced
- appconduitd
- appleh16camerad
- applicensedeliveryd
- appplaceholdersyncd
- arkitd
- assetsd
- assistant_cdmd
- assistant_service
- audiomxd
- automationmode-writer
- batterytrapd
- biomed
- bookassetd
- brctl
- cdpd
- chronod
- chs.dylib
- cht.dylib
- com.apple.AppleFSCompression.AppleFSCompressionTypeZlib
- com.apple.CloudDocsUI.CloudSharing-AppExtension
- com.apple.DiagnosticsSessionAvailibility
- com.apple.DictionaryServiceHelper
- com.apple.DocumentManager.Service-AppExtension
- com.apple.DocumentManagerCore.Downloads
- com.apple.DriverKit-AppleEthernetIXGBE
- com.apple.DriverKit-AppleEthernetMLX5
- com.apple.ExclaveKextClient
- com.apple.FaceTime.FTConversationService
- com.apple.GeoServices.MapsOfflineServices
- com.apple.IdentityLookup.MessageFilter
- com.apple.Maps.appremoval
- com.apple.Photos.CPLDiagnose
- com.apple.Safari.SearchHelper
- com.apple.SiriTTSService.TrialProxy
- com.apple.Translate.appremoval
- com.apple.UIKit.KeyboardManagement
- com.apple.accessibility.mediaaccessibilityd
- com.apple.cloudsettings.international
- com.apple.cts
- com.apple.datamigrator
- com.apple.dispatch.vfs
- com.apple.driver.AOPAudio2
- com.apple.driver.AOPTouchKext
- com.apple.driver.ASIOKit
- com.apple.driver.AppleA7IOP
- com.apple.driver.AppleALSColorSensor
- com.apple.driver.AppleARMPMU
- com.apple.driver.AppleActuatorDriver
- com.apple.driver.AppleAuthCP
- com.apple.driver.AppleBasebandPCI
- com.apple.driver.AppleC26Charger
- com.apple.driver.AppleCS42L79Audio
- com.apple.driver.AppleCallbackPowerSource
- com.apple.driver.AppleDCP
- com.apple.driver.AppleDCPDPTXProxy
- com.apple.driver.AppleEmbeddedAudio
- com.apple.driver.AppleEmbeddedLightSensor
- com.apple.driver.AppleEmbeddedMikeyBus
- com.apple.driver.AppleEmbeddedPCIE
- com.apple.driver.AppleHIDTransportSPI
- com.apple.driver.AppleHapticsSupportNVM
- com.apple.driver.AppleIDV
- com.apple.driver.AppleIOPADMAStream
- com.apple.driver.AppleInputDeviceSupport
- com.apple.driver.AppleInterruptControllerV3
- com.apple.driver.AppleMultiFunctionManager
- com.apple.driver.AppleOnboardSerial
- com.apple.driver.ApplePMP
- com.apple.driver.ApplePMPFirmware
- com.apple.driver.ApplePTD
- com.apple.driver.ApplePhoneBTM
- com.apple.driver.AppleProResHW
- com.apple.driver.AppleS5L8920XPWM
- com.apple.driver.AppleS5L8940XI2C
- com.apple.driver.AppleSMC
- com.apple.driver.AppleSMCWirelessCharger
- com.apple.driver.AppleSPIMC
- com.apple.driver.AppleSPMIPMU
- com.apple.driver.AppleSSE
- com.apple.driver.AppleSmartBatteryManagerEmbedded
- com.apple.driver.AppleStockholmControl
- com.apple.driver.AppleT6020PCIePIODMA
- com.apple.driver.AppleT8103TypeCPhy
- com.apple.driver.AppleT8110DART
- com.apple.driver.AppleT8130TypeCPhy
- com.apple.driver.AppleT8140ANEHAL
- com.apple.driver.AppleT8140CLPC
- com.apple.driver.AppleT8140MCC
- com.apple.driver.AppleT8140PMGR
- com.apple.driver.AppleThunderboltDPOutAdapter
- com.apple.driver.AppleThunderboltNHI
- com.apple.driver.AppleThunderboltUSBUpAdapter
- com.apple.driver.AppleTopCaseHIDEventDriver
- com.apple.driver.AppleTypeCPhy
- com.apple.driver.AppleTypeCPhyAUSBC
- com.apple.driver.AppleUSBDeviceNCM
- com.apple.driver.AppleUSBXDCI
- com.apple.driver.AppleUSBXDCIARM
- com.apple.driver.AudioDMAFamily
- com.apple.driver.AudioSharedDARTMapperProxy
- com.apple.driver.DCPAVFamilyProxy
- com.apple.driver.DMAChannelProxy
- com.apple.driver.DiskImages
- com.apple.driver.DiskImages.UDIFDiskImage
- com.apple.driver.EXDisplayPipeH17P
- com.apple.driver.ExclaveSEPManagerProxy
- com.apple.driver.IODARTFamily
- com.apple.driver.IOPAudioClientManagerDevice
- com.apple.driver.usb.AppleSynopsysUSBXHCI
- com.apple.driver.usb.AppleUSBHostBillboardDevice
- com.apple.driver.usb.AppleUSBHostCompositeDevice
- com.apple.dt.DTMLModelRunnerService
- com.apple.dt.instruments.dtsecurity
- com.apple.finddevices.complications
- com.apple.finditems.complications
- com.apple.findpeople.complications
- com.apple.freeform.appremoval
- com.apple.iokit.IOHDCPFamily
- com.apple.iokit.IONetworkFamily
- com.apple.iokit.IOPAudioDriverFamily
- com.apple.iokit.IOSCSIArchitectureModelFamily
- com.apple.iokit.IOSerialFamily
- com.apple.iokit.IOStorageFamily
- com.apple.iokit.IOUSBDeviceFamily
- com.apple.iokit.IOUSBMassStorageDriver
- com.apple.migrationpluginwrapper
- com.apple.mobilenotes.NotesImporter
- com.apple.podcasts.appremoval
- com.apple.printactivityservice
- com.apple.siri.acousticsignature
- com.apple.spotlight.IndexAgent
- companionappd
- companionfindlocallyd
- companionmessagesd
- contactsdonationagent
- corebrightnessdiag
- coreduetd
- corercd
- countryd
- destinationd
- deu.dylib
- devicesharingd
- diagnosticd
- diagnosticservicesd
- diagnosticspushd
- dietapplecamerad
- dmd
- druid
- dtfetchsymbolsd
- eapolclient
- ecosystemanalyticsd
- eedmediaservice
- eng.dylib
- enu.dylib
- esm.dylib
- esp.dylib
- exclave_kernel
- eyereliefd
- facemetricsd
- fairplaydeviceidentityd
- familynotificationd
- feedbackd
- fileproviderd
- fin.dylib
- findmybeaconingd
- finhealth_client
- fitnesscoachingd
- followupd
- fra.dylib
- frc.dylib
- fsck_msdos
- fseventsd
- fskit_helper
- gamecontrollerd
- generativeexperiencesd
- geoanalyticsd
- get-network-info
- gputoolsd
- hangtelemetryd
- healthappworkd
- healthrecordsd
- homed
- homeenergyd
- homerecommendationutil
- hostapd
- iAdFramework
- iCalendar
- iCloud+
- iCloudCalendarUnifiedSettings
- iCloudDriveApp
- iCloudDriveFileProviderOverride
- iCloudMailUnifiedSettings
- iCloudSubscriptionOptimizerClient
- iCloudSubscriptionOptimizerCore
- iCloudSubscriptionOptimizerLighthouse
- iCloudSubscriptionOptimizerPFLTraining
- iMessageApps
- iTunesStore
- iTunesStoreUIFramework
- iWorkImport
- iapd
- icloudCalendarSettings
- icloudsubscriptionoptimizerd
- ifconfig
- init_exclavekit
- intelligencecontextd
- intelligenceflowd
- intelligenceplatformd
- iosdiagnosticsd
- ioupsd
- ita.dylib
- jetsam_priority
- jpn.dylib
- kbd
- kbdebug
- keychainsharingmessagingd
- knowledgeconstructiond
- kor.dylib
- kperf
- kperfdata
- ktrace
- languageassetd
- libAWDProtobufFacetime.dylib
- libAWDProtobufGCK.dylib
- libAWDProtobufLocation.dylib
- libAWDSupport.dylib
- libAWDSupportFramework.dylib
- libAXSafeCategoryBundle.dylib
- libAppleEXR.dylib
- libAudioDSPCore.dylib
- libAudioIssueDetector.dylib
- libAudioStatistics.dylib
- libBLAS.dylib
- libBasebandCommandDrivers.dylib
- libBasebandCommandDriversARI.dylib
- libBasebandDiagnostics.dylib
- libBasebandSharedServices.dylib
- libCGInterfaces.dylib
- libCRFSuite.dylib
- libCTGreenTeaLogger.dylib
- libCellularDecoders.dylib
- libChineseTokenizer.dylib
- libCommCenterAWDMetrics.dylib
- libCommCenterCNTargetData.dylib
- libComposeFilters.dylib
- libCoreEntitlements.dylib
- libETLDIAGLoggingDynamic.dylib
- libETLDLOADDynamic.dylib
- libETLDMCDynamic.dylib
- libETLEFSDumpDynamic.dylib
- libETLSAHDynamic.dylib
- libFDRDecode.dylib
- libGLProgrammability.dylib
- libGLVMPlugin.dylib
- libGPUCompiler.dylib
- libGPUCompilerUtils.dylib
- libGSFont.dylib
- libGSFontCache.dylib
- libICEClient.dylib
- libKTLDynamic.dylib
- libLAPACK.dylib
- libLinearAlgebra.dylib
- libLogRedirect.dylib
- libMTLCompilerHelper.dylib
- libPPMDataModel.dylib
- libParallelCompression.dylib
- libQMIParserDynamic.dylib
- libRPAC.dylib
- libRemoteTelephonyTransport.dylib
- libRosetta.dylib
- libSTS-N.dylib
- libSparseBLAS.dylib
- libTelephonyBasebandDynamic.dylib
- libTelephonyDebugDynamic.dylib
- libTelephonyUtilDynamic.dylib
- libThaiTokenizer.dylib
- libVibeSynthEngine.dylib
- libViewDebuggerSupport.dylib
- libWISSupport.dylib
- libWirelessAudioIPC.dylib
- libacmobileshim.dylib
- libapple_nghttp2.dylib
- libarchive.2.dylib
- libate.dylib
- libc++abi.dylib
- libchannel.dylib
- libcmark-gfm.dylib
- libcompression.dylib
- libcopyfile.dylib
- libcupolicy.dylib
- libdscsym.dylib
- libedit.3.dylib
- libexslt.0.dylib
- libfaceCore.dylib
- libglInterpose.dylib
- libhvf.dylib
- libicucore.A.dylib
- libllvm-flatbuffers.dylib
- liblockdown.dylib
- liblog_coreacc.dylib
- liblog_geo.dylib
- liblog_mdns.dylib
- liblog_mdnsresponder.dylib
- liblog_srp.dylib
- libmacho.dylib
- libmarisa.dylib
- libmav_ipc_router_dynamic.dylib
- libmrc.dylib
- libnfstorage.dylib
- liboah.dylib
- liboainject.dylib
- libolaf.dylib
- libpcap.A.dylib
- libprotobuf-lite.dylib
- libprotobuf.dylib
- libsandbox.1.dylib
- libspindump.dylib
- libstdc++.6.0.9.dylib
- libswiftARKit.dylib
- libswiftAssetsLibrary.dylib
- libswiftCallKit.dylib
- libswiftCarPlay.dylib
- libswiftCompression.dylib
- libswiftContacts.dylib
- libswiftCoreAudio.dylib
- libswiftCoreFoundation.dylib
- libswiftCoreImage.dylib
- libswiftCoreLocation.dylib
- libswiftCoreMIDI.dylib
- libswiftCoreML.dylib
- libswiftCoreNFC.dylib
- libswiftDataDetection.dylib
- libswiftDemangle.dylib
- libswiftDistributed.dylib
- libswiftExtensionFoundation.dylib
- libswiftExtensionKit.dylib
- libswiftGLKit.dylib
- libswiftGameplayKit.dylib
- libswiftIntents.dylib
- libswiftMLCompute.dylib
- libswiftMapKit.dylib
- libswiftMetalKit.dylib
- libswiftMetricKit.dylib
- libswiftModelIO.dylib
- libswiftNaturalLanguage.dylib
- libswiftOSLog.dylib
- libswiftObjectiveC.dylib
- libswiftPassKit.dylib
- libswiftQuartzCore.dylib
- libswiftRegexBuilder.dylib
- libswiftSceneKit.dylib
- libswiftSpatial.dylib
- libswiftSpriteKit.dylib
- libswiftSynchronization.dylib
- libswiftSystem.dylib
- libswiftSystem_Foundation.dylib
- libswiftUniformTypeIdentifiers.dylib
- libswiftVideoToolbox.dylib
- libswiftVision.dylib
- libswiftWatchKit.dylib
- libswift_Builtin_float.dylib
- libswift_Differentiation.dylib
- libswift_RegexParser.dylib
- libswift_errno.dylib
- libswift_math.dylib
- libswift_signal.dylib
- libswift_stdio.dylib
- libswift_time.dylib
- libswiftsimd.dylib
- libswiftsys_time.dylib
- libswiftunistd.dylib
- libsysdiagnose.dylib
- libsystem_asl.dylib
- libsystem_dnssd.dylib
- libsystem_eligibility.dylib
- libsystem_featureflags.dylib
- libsystem_pthread.dylib
- libsystem_pthread_debug.dylib
- libtailspin.dylib
- libtidy.A.dylib
- libutil.dylib
- libvDSP.dylib
- libxml2.2.dylib
- libxo.dylib
- libxslt.1.dylib
- lighthouse_runtime
- liveactivitiesd
- livefiles_hfs.dylib
- livefiles_msdos.dylib
- livefiles_ntfs.dylib
- localizationswitcherd
- locationaccessstored
- locationpushd
- logd_helper
- logd_reporter
- mDNSResponderHelper
- magicswitchd
- managedappsd
- managedsettingsdiagnoticstool
- mapinspectord
- mapspushd
- mediamlxpc
- mediaplaybackd
- mediasetupd
- merchantd
- meshnetd
- modelmanagerdump
- mount
- mstreamd
- nanoappregistryd
- nanobackupd
- nanomediaremotelinkagent
- nanoprefsyncd
- nanosystemsettingsd
- nanoweatherprefsd
- ndp
- netstat
- nexusd
- nfsstat
- nptocompaniond
- otpaird
- pairedsyncd
- pairedunlockd
- pcsstatus
- perfdiagsselfenabled
- pfd
- pipelined
- pmudiagnose
- previewsd
- printbandservice
- progressd
- prototyped
- ptb.dylib
- recentsd
- relatived
- remoteappintentsd
- remotectl
- remotepairingdeviced
- replicatord
- resourcegrabberd
- routined
- safarifetcherd
- scrod
- searchd
- securem3fw-d9x.im4p
- seputil
- shared_cache_page_prewarming
- signpost_reporter
- siriinference-dodml-plugin
- sirireaderd
- sirittsd
- skywalkctl
- smbclientd
- softwareupdateservicesd
- sosd
- soundanalysisd
- speechmodeltrainingd
- stickersd
- suggestd
- swift-inspect
- swtransparency-sysdiagnose
- symptomsd
- symptomsd-helper
- t8140pmp.im4p
- transitd
- transparencyStaticKey
- tursd
- tvremoted
- tzd
- tzinit
- usbaudiodxpc
- useractivityd
- usernotificationsd
- vCard
- vImage
- videocodecd
- voiced
- watchdogd
- watchpresenced
- wcd
- webinspectord
- webprivacyd
- xpcroleaccountd

</details>

## LOW_SIGNAL — excluded (1053, metadata/timestamp churn only)

<details><summary>Show 1053 components</summary>

- AACDependencies
- ACIAdapter
- ACICVPInterface
- ACICamera
- ACICoreKit
- ACIObjCCoreKit
- ACIPCBTLib.dylib
- ADEventListenerPlugin
- AGXCompilerService-S2A8
- AGXGPURawCounterBundle
- ANEClientSignals
- ARKitFoundation
- ASDAccountNotficationPlugin
- ASOctaneSupport
- AV1SW.videoencoder
- AVKitSettings
- AXAVSPluginService
- AXAggregateStatisticsServices
- AXContainerServices
- AXGuestPassServices
- AXLocalizationCaptionService
- AXSpeakFingerManager
- Accelerate
- AccessibilityReaderData
- AccessibilityReaderServices
- AccessibilityReadingUI
- AccessibilityRemoteServices
- AccessibilityRemoteUIServices
- AccessibilityUIShared
- AccessibilityUIViewServices
- Accessory
- AccessoryAssistiveTouch
- AccessoryAudio
- AccessoryBLEPairing
- AccessoryCommunications
- AccessoryFirmwareUpdate
- AccessoryHID
- AccessoryMediaLibrary
- AccessoryNavigation
- AccessoryOOBBTPairing
- AccessorySensorManagerExclaveDaemon
- AccessorySensorManagerServices
- AccessorySensorManager_Private
- AccessoryVoiceOver
- AccountsUISupport
- AccountsUISupportShared
- ActivityAchievementsPlugin
- ActivitySharingAwardsPlugin
- ActivitySharingPlugin
- AdPlatformsCommonUI
- AdPlatformsInternal
- AdServices
- AdaptiveMesh
- AddressBook
- AddressBookUI
- AirFair
- AirPlayRoutePrediction
- AirPlaySenderUI
- Airship
- AirshipCentauriHelper
- AlarmKit
- AlarmKitCore
- AlarmKitFoundation
- AlarmModule
- AlchemistBase
- AlchemistService
- AlgorithmsInternal
- AlgosScoreFramework
- AltimeterHarvest
- AlwaysOnExclavesServices
- Ambient
- AmbientSceneScope
- AmbientUIKit
- AmbientUIServices
- AnnounceSiriExtensions
- AppClip
- AppGenius
- AppSSOConfigPlugin_iOS
- AppSSOLocatePlugin_iOS
- AppSSOReplacePlugin_iOS
- AppStoreComponentsDaemonKit
- AppStoreEvalLighthouseUtils
- AppStoreUI
- AppSupport
- AppTrackingTransparency
- AppleEmbeddedDisplayServices
- AppleHDQGasGauge
- AppleHDQGasGaugeHID
- AppleHIDALS
- AppleIntelligenceReporting
- AppleIntelligenceReportingProcessing
- AppleLDAP
- AppleMSG
- AppleNVMe
- ApplePMUFirmwareDriver
- Apps
- AsenAOP2TightbeamService.dylib
- AskToUI
- AssertionServices
- AssetCacheServicesExtensions
- AssistantCardServiceSupport
- AssistantTTSPlugin
- AssistiveTouch-iOS
- AsyncAlgorithmsInternal
- AttentionAwarenessFilter
- AudioAccessoryAssetManagement
- AudioAppleSiriRemoteInput
- AudioDSPAnalysis
- AudioDiagnosticExtensionCore
- AudioTransportCommon
- AuthBrokerAgent
- AutomationMode
- BLEPairing-iOS
- BackBoardHIDEventProcessors
- BagKit
- BehaviorMiner
- BiomeFlexibleStorage
- BiomeSync
- BookCoverUtility
- BookUtility
- BootCampFormatter
- BrailleNBSC
- BridgeCommons
- BridgeReporting
- BrookDataCollection
- BrowserKit
- BubbleKit
- CDDataAccessExpress
- CTCarrierSpace
- CalDAV
- CalculatorModule
- CallIntelligence
- CallsAppServices
- CallsAppUI
- CallsDialer
- CallsPersistence
- CallsSearch
- CallsUtilities
- CallsXPC
- CameraModule
- CarAccessoryDaemon
- CarKitNavigation
- CarPlayArtwork
- CardServices
- CardioHealth
- CascadingFilters
- Centauri
- CentauriAlphaPatchBay
- CentauriBetaPatchBay
- CentauriBooter
- CentauriController
- CentauriDiagnostic
- CertUI
- ChunkingLibrary
- ClockAppIntentsSupport
- ClockComplications
- CloudAssetDaemon
- CloudAssetsCommons
- CloudAssetsDaemon
- CloudCoreInternal
- CloudDocsDataclassOwnerPlugin
- CloudDocsFileProvider
- CloudKitAccessPlugin
- CloudMediaServicesInterfaceKit
- CodesignKit
- CombineCocoa
- CommonAuth
- CommonUtilities
- CommunicationDetails
- CommunicationTrust
- CompanionInferenceCore
- CompanionViewService
- CompassCalibration
- CompassUI
- ConnectedMode
- ConstantClasses
- ContactsAssistantServices
- ContactsDonation
- ContactsDonationFeedback
- ContactsMetrics
- ContainerManagerSystem
- ContainerManagerUser
- ContainerMetadataExtractor
- ContainerMigrator
- ContextKit
- ContextKitCore
- ContextKitExtraction
- ContextKitPrediction
- ContextualActionsClient
- ContinuityCapture
- ContinuitySing
- ContinuousDialogManagerService
- Coordination
- CopyHFSMeta
- CoreAccessoriesFeatures
- CoreAudioOrchestration
- CoreCapture
- CoreDuetDaemonProtocol
- CoreDuetSync
- CoreGPS
- CoreGPS.dylib
- CoreGPSTest
- CoreGPSTest.dylib
- CoreGlyphsPrivate
- CoreLocationSync
- CoreMLOdie
- CoreMotionFDNML
- CoreMotionModels
- CoreNameParser
- CorePrescription
- CorePrescriptionLite
- CoreRE3DGSFoundation
- CoreServicesUI
- CoreSpeechDataAnalytics
- CoreThread
- Cornobble
- CorrectionsProfilesSync
- CredentialProviderExtensionHelper
- DAAPKit
- DAAccount
- DAAccountNotifier
- DACoreDAVGlue
- DAIMAPNotes
- DALDAP
- DASDaemon
- DASDelegate
- DMCTools
- DMCToolsUIUtilities
- DOT
- DRMFoundation
- DTServiceHub
- DailyBriefingCommon
- DataAccessUI
- DataActivation
- DataCollector
- DataCollectorLibrary
- DataDetectorsNaturalLanguage
- DataDetectorsRemoteScanner
- DataRelay
- DataRelay_Private
- DateAndTimeSupport
- DeclaredAgeRange
- DeepBreathingSettings
- DefaultAccessPlugin
- DendriteIngest
- DesignLibrary
- DesktopServicesUI
- DeviceActivityConductor
- DeviceDiscoveryUI
- DevicePresence
- DeviceProximityDetection
- DeviceRecovery
- DeviceSharingEnrollmentServices
- DeviceSharingEnterpriseServices
- DeviceToDeviceManager
- DiagnosticExtensions
- DiagnosticLogCollection
- DiagnosticsSessionAvailability
- DiskImages
- DiskSpaceDiagnostics
- DoNotDisturbAssistant
- DoNotDisturbSettingsSync
- DragUI
- DuetActivitySchedulerDaemon
- EDGESettings
- ESAccountNotifier
- EasyConfig
- EchoRelay
- EnergyKit
- EnergyKitInternal
- Engram
- EnhancedLogging
- EventKitUICore
- ExclavePolarisBufferService
- EyeRelief
- FMCore
- FMCoreLite
- FMCoreUI
- FMF
- FMFMapXPCService
- FSTaskScheduler
- FTAWD
- FTClientServices
- FaceTimeMigrator
- FaceTimeNameUtility
- FamilyControlsObjC
- FeatureFlags
- FeedbackAssistantModule
- FileIndexerDaemon
- FileProviderResolver
- FileProviderTelemetry
- FilesActionsUI
- FindMyDeviceUI
- FitnessDispatch
- FitnessIntelligence
- FitnessIntelligenceDaemonCore
- FitnessIntelligenceFeedback
- FitnessIntelligenceInference
- FitnessIntelligenceSnapshotting
- FitnessSampleContent
- FitnessSummary
- FitnessSync
- FlexMusicKit
- Fluid
- Focus
- FoundInAppsPlugins
- FoundationModels
- FoundationODR
- FriendKit
- GCCloudServiceOwner
- GEO
- GLEngine
- GLKit
- GPUToolsDeviceServices
- GPUToolsReplay
- GRPCCoreInternal
- GRPCInProcessTransportInternal
- GRPCProtobufInternal
- GRPCURLSessionTransportInternal
- Game
- GameControllerUI
- GamePolicyServices
- GameSave
- GameStoreKit
- GenerationalStorage
- GenerativePartnerService
- GenerativePartnerServiceUI
- GenericAddressHandler
- GeoToolbox
- Gestures
- GridDataServices
- GridZero
- GroupKitCrypto
- HAENDataMigrator
- HIDAnalytics
- HIDDisplay
- HIDPreferences
- HWAdapter
- HardwareDiagnostics
- HeadphoneCommonUIKit
- HealthAppPlugin
- HealthCategories
- HealthCharts
- HealthChartsCore
- HealthContent
- HealthContentDaemon
- HealthContentDaemonPlugin
- HealthContentGeneration
- HealthDataclassOwnerPlugin
- HealthDomains
- HealthDomainsDaemon
- HealthDomainsUI
- HealthExpressions
- HealthHeartRateStream
- HealthIntents
- HealthLEHeartRate
- HealthOntologyKit
- HealthRecordsConceptsSupport
- HealthSettingsUI
- HealthTopics
- HealthTopicsCore
- HealthTopicsDaemon
- HealthTopicsDaemonPlugin
- HeartDaemonPlugin
- HeartHealthUI
- HeartRateCoordinator
- HomeAutomationUIPlugin
- HomeKitDaemonShared
- HomeKitFeatures
- Human
- HumanUI
- ICE
- IMDMessageServices
- IOAccelerator
- IOFastPath
- IOHIDMotionEventSessionFilter
- IOUSBDeviceLib
- IPConfigurationHelper
- IXATestAppRelay
- IconRendering
- IdentityDocumentServices
- IdentityDocumentServicesUI
- IdentityLookupUI
- IdleTimerHosting
- Image
- InAppMessages
- InAppMessagesCore
- IncomingCallFilter
- InputContext
- IntelligencePlatformDataActions
- IntelligencePlatformQuery
- IntelligenceSimulation
- IntelligenceTasks
- IntelligenceTasksEngine
- IntentRecommend
- IntentRecommendRuntime
- IntentRecommendShared
- IntentsFoundation
- IntentsUICardKitProviderSupport
- InternationalSupportMigrator
- InternationalTextSearch
- IonosphereHarvest
- JarvisPlugin
- JetsamProperties
- JournalUI
- KernelManagerLibrary
- KeyboardBrightnessModule
- KeyboardSettingsFeedback
- L2TP
- LegacyGameKit
- LegacyHandle
- LightSourceSupport
- LighthouseCoreMLFeatureStore
- LighthouseDictation
- LocaleSettings
- LocationAccessStore
- LocationFenceSync
- LocationHarvest
- LocationLogEncryption
- LocationPromptUI
- LockoutUI
- LoginKit
- LoginPerformanceKit
- LowPowerModule
- MIDI
- MIDIServer
- MPSFunctions
- MSGExternalSync
- MXI
- MXUIService
- MXUIServiceClient
- MagnifierModule
- MailWebProcessSupport
- ManagedAssets
- ManagedBackgroundAssets
- ManagedBackgroundAssetsHelper
- ManagedBackgroundAssetsHelperFetching
- ManagedBackgroundAssetsXPC
- ManagedEvent
- MapKitSwiftBridge
- MapsDesign
- MapsIntelligence
- Marco
- MediaAnalysisGeneration
- MediaContinuityKit
- MediaControlReceiver
- MediaControlUI
- MediaGroups
- MediaGroupsDaemon
- MediaIntents
- MediaKit
- MediaLibrary-iOS
- MediaPlatform
- MediaPlayerUI
- MediaRemoteDaemonServices
- MediaServicesBroker
- MediaSetup
- MediaSuggester
- MediaTokens
- MedicalIDDaemon
- MemoryAccounting
- MemoryDiagnostics
- MenstrualCyclesDaemonPlugin
- MentalHealthDaemonPlugin
- MessageSupport
- MessagesDataKeyboardPlugin
- MessagesDataMigrator
- MetalPerformancePrimitives
- MetalPerformanceShaders
- MetricsKit
- MicroFindMy
- MobileAssetUpdater
- MobileContainerManager
- MobileCoreServices
- MobileDeviceLink
- MobileDevices-0001
- MobileDevices-0003
- MobileDevices-0004
- MobileGestaltHelper
- MobileIcons
- MobileLookup
- MobileSync
- MobileSystemServices
- MobileTimerUISupport
- MomentsData
- MomentsUI
- MotionCalibration
- MotionHealthAlgorithms
- MultipeerConnectivity
- MultitouchSessionFilterSupport
- NFRadioPowerSwitch
- NFRestoreService
- NRDUpdated
- NameRecognition
- NanoAppRegistry
- NanoBackup
- NanoContactsBridgeSetup
- NanoControlCenter
- NanoFaceGallery
- NanoMapsComplications
- NanoMapsNavigationCompanionDataSource
- NanoMapsSampleDataSource
- NanoPassKitUI
- NanoSmartStackControlUI
- NanoSmartStackProactiveSuggestions
- Navigation-iOS
- NearFieldUI
- NeighborhoodActivityConduitIntents
- NetAppsUtilities
- NetworkQuality
- NetworkQualityServices
- NetworkScore
- NewDeviceOutreach
- NewDeviceOutreachUI
- NewDeviceSetupUIService
- News
- NewsAds
- NewsAnalytics
- NewsAnalyticsUpload
- NewsArticles
- NewsCore
- NewsDaemon
- NewsEngagement
- NewsEngagementCollector
- NewsFeed
- NewsFoundation
- NewsKit
- NewsLiveActivitiesCore
- NewsPersonalization
- NewsScoringService
- NewsServices
- NewsServicesInternal
- NewsSettings
- NewsSubscription
- NewsToday
- NewsTransport
- NewsUI
- NewsUI2
- NewsURLBucket
- NewsURLResolution
- OAuth
- ODIE
- OSAServicesClient
- OSASyncProxyClient
- OmniSearchClient
- OpenGLES
- OpusFoundation
- OpusOrigamiProducer
- PDS
- PLAMonitor
- PLSnapshot
- PacketFilter-embedded
- PacketParser
- PairedUnlock
- PanicHelper
- PassKit
- PassbookUsageBundle
- PasscodeAndBiometricsSettings
- PasswordsDigitalSeparation
- PeopleSuggesterLighthouse
- PeopleSuggesterMetrics
- PeopleUIInternal
- PerfPowerTelemetryReaderService
- PermissionKit
- PersonaKit
- PersonalSearch
- PersonalSearchService
- PersonalSearchTypes
- Phone
- PhoneAppIntents
- PhoneKit
- PhoneNumbers
- Photo
- PhotoBoothEffects
- PhotosFaceLayoutCore
- PhotosSpatialMedia
- PhotosSpatialMediaCore
- PointerUISystemServices
- Polaris
- PolarisBufferService
- PolarisExclaveSupport
- PolarisGraph
- PolarisRuntime
- PolarisSwift
- PolarisSystemGraph
- PortraitCore
- PosterBoardUI
- PosterFuturesKit
- PosterLegibilityKit
- PosterModel
- PowerlogControl
- PowerlogDatabaseReader
- PowerlogFullOperators
- PredictedContextAlgorithms
- PreferencesAssistant
- PriMLETL
- Print
- PrivacyDisclosureCore
- ProDisplayLibrary
- ProactiveExperimentsInternals
- ProactivePredictionClient
- ProceduralWallpapers
- ProfileValidatedAppIdentity
- PromotedContentProxy
- PromotedContentSupport
- PushKit
- PushToTalk
- QRCodeModule
- QuickNoteModule
- QuickTime
- RawCameraSupport
- RecencyService
- RelevanceEngineHome
- RelevanceEngineSolar
- RelevanceEngineWeather
- RelevanceKit
- RelevanceServicesCompanion
- ReminderKitUI
- RemoteInjectionAgent
- RemoteManagementProtocol
- RemoteManagementUI
- RemoteSoftwareUpdate
- RemoteStateDumpKit
- ReportingPlugin
- RespiratoryHealthDaemonPlugin
- RevealCore
- Rewind
- Rhine
- Routine
- Rules
- SADSupport
- SANovaGestureRecognizers
- SESUIService
- SESUIServiceCore
- SIDFitness
- SIMToolkitUI
- SLOM
- SMBClientProvider
- SMBSearch
- SMCT
- SavageCameraInterface
- Screen
- SearchIntrospectionKit
- SecureControlService
- SecureMessaging
- SecureMessagingAgentCore
- SensingPredictExclaveDaemon
- SensingPredictServices
- SensorKitUI
- Sentry
- ServiceShared
- ServicesIntelligence
- SharingHUD
- SharingXPCHelper
- SharingXPCServices
- ShazamModule
- SidecarUI
- SignpostMetrics
- SiriActivationFoundation
- SiriGlobalConfiguration
- SiriHomeAccessoryFramework
- SiriInferredHelpfulness
- SiriInstrumentationManifest
- SiriInvocationAnalytics
- SiriLocalization
- SiriModes
- SiriObservation
- SiriReaderServices
- SiriSystemCommandsUIFramework
- SiriTasks
- SleepHealthDaemonPlugin
- SlideshowKit
- SmartStackFoundation
- SmartStackSettings
- SmartStackSettingsUI
- SoftLinking
- SoftwareUpdateUIFoundation
- SoftwareUpdateUIKit
- SoftwareUpdateUIMobile
- SpatialAudioProfile
- SpatialAudioServices
- SpeakTypingServices
- SpeechTranslation
- SpotlightFoundation
- SpotlightKnowledgeDaemon
- SpotlightUIServices
- StandaloneHIDAudService
- StickerFoundation
- StickerKitInternal
- StopwatchModule
- StorageContainersPrivate
- StorageData
- StoreBookkeeperClient
- SubcredentialUIService
- SubscribedCalendarSettings
- SummariesHealthDaemonPlugin
- SupportFlowCore
- SupportFlowUI
- SupportServices
- SwiftCRLite
- SwiftMLS
- SwiftTLS
- SwiftUITracingSupport
- SymptomDistribution
- SymptomNetworkDiagnostics
- SymptomNetworkDiagnosticsCore
- SymptomReporter
- SymptomShared
- SynapseSyncPlugin
- SystemAperture
- SystemCustomization
- SystemIntentsSupport
- SystemPaperPresentation
- SystemUISecureFlipBookUtilities
- SystemUIWindowingKit
- SystemWake
- TCCSystemMigration
- TSCalculationEngine
- TeaState
- TelephonyMessagingKit
- TerminalToolKit
- TextAnimationSupport
- TextEffectsCatalog
- TextInput_ar
- TextInput_bn
- TextInput_bo
- TextInput_ca
- TextInput_chr
- TextInput_emoji
- TextInput_en
- TextInput_he
- TextInput_intl
- TextInput_mul
- TextInput_my
- TextInput_pt
- TextInput_si
- TextInput_sl
- TextInput_ug
- TextInput_yue
- TextInput_zh
- TextToSpeechKonaSupport
- TextUnderstanding
- TextUnderstandingFoundation
- TextUnderstandingRuntime
- TextureIO
- TimeAppServices
- TimeZone
- Timeline
- TinCanShared
- TouchController
- Traffic
- TraitsArbiter
- TranslationUIServices
- TypologyAccess
- UARPAssetManager
- UARPKit
- UARPUpdaterService
- UIGrounding
- UIIntelligenceInteraction
- UIKitSwiftUIComponents
- UINavigationKit
- UIUtilities
- ULPNHeuristicsClientFramework
- USBCAccessoryUpdaterService
- USDLib_FormatLoaderProxy
- UVFSXPCService
- UnblockClient
- UnblockService
- UnityPoster
- UpdateCycle
- UpdateCycleSupport
- UserAlerts
- UserDomainConceptsSupport
- UserEventAgent
- UserManagementUI
- UserSafety
- VPNPreferences
- VideoIntelligence
- VisionKitInternal
- VisualActionPrediction
- VisualActionPredictionCore
- VisualActionPredictionSupport
- VisualIntelligence
- VisualIntelligenceCore
- VisualIntelligenceCoreDDSupport
- VisualIntelligenceUI
- VisualLookUp
- VisualMappingKit
- VisualPairing
- VoiceMemosModule
- VoicemailStore
- WalletModule
- WatchControlAssets
- WatchdogServiceManagement
- WeatherFoundation
- WeatherResources
- Weave
- WebContentAnalysis
- Welcome
- WelcomeKit
- WellnessUIPlugin
- WiFiAware
- WiFiCloudSyncEngine
- WiFiLogCapture
- WiFiSettingsKit
- WiFiSharing
- WirelessInsights
- XPCDistributed
- XavierNews
- YelpAccessPlugin
- ZhuGeSupport
- _AppIntentsServices_ToolKit
- _CommunicationsUICore_PosterBoardServices
- _DeviceDiscoveryUI_SwiftUI
- _GeoServices_GeoToolbox
- _GeoToolbox_AppIntents
- _GeoToolbox_CoreLocation
- _LocationEssentials
- _MediaPlayer_AppIntents
- _OnDeviceStorage_JavaScriptCore
- _PermissionKit_SwiftUI
- _PermissionKit_UIKit
- _PhotosUI_WidgetKit
- _RelevanceKit_MapKit
- _ToneKit_SwiftUI
- _WebKit_SwiftUI
- accountsd
- activity
- addNetworkInterface
- apfs_boot_mount
- arp
- aslmanager
- bird
- brookcompaniond
- cameracaptured
- checkpointd
- chsrom.dylib
- chtrom.dylib
- ckdiscretionaryd
- com.apple.BackgroundTaskAgentPlugin
- com.apple.MapKit.SnapshotService
- com.apple.NDO.FollowUp
- com.apple.alarm
- com.apple.bonjour
- com.apple.cloudsettings.keyboard
- com.apple.corelocation.locationUI
- com.apple.datadetectors.AddToRecentsService
- com.apple.donotdisturb
- com.apple.donotdisturb.private.driving-trigger
- com.apple.donotdisturb.private.hearing-trigger
- com.apple.donotdisturb.private.intents.preload
- com.apple.donotdisturb.private.intents.user-interactive.preload
- com.apple.donotdisturb.private.schedule
- com.apple.donotdisturb.private.sleeping-trigger
- com.apple.donotdisturb.private.workout-trigger
- com.apple.driver.AppleAOPAudio
- com.apple.driver.AppleSmartIO2
- com.apple.driver.AppleUSBDeviceMux
- com.apple.fsevents.matching
- com.apple.iCloud.FollowUp
- com.apple.netsvcproxy
- com.apple.quicklook.ThumbnailsAgent
- com.apple.systemconfiguration
- com.apple.tailspin
- companion_proxy
- containermanagerd
- df
- diagnosticextensionsd
- dirs_cleaner
- donotdisturbd
- duetexpertd
- eci.dylib
- fdrhelper
- filecoordinationd
- iCloudDriveService
- iCloudMailAssistant
- iCloudQuotaNetworking
- iCloudQuotaNetworkingCore
- iTunesStoreFramework
- iWorkXPC
- init_featureflags
- intents_helper
- jpnrom.dylib
- korrom.dylib
- libAONConnection.dylib
- libAXSpeechManager.dylib
- libAmber.dylib
- libAppleDeviceQueryArmory.dylib
- libAppleDeviceQueryRoster.dylib
- libAppleSSE.dylib
- libAppleSSEExt.dylib
- libAppleTconUARPUpdater.dylib
- libBASupport.dylib
- libBBUpdaterDynamic_stubs.dylib
- libBIG5.dylib
- libCVMSPluginSupport.dylib
- libCentauriUpdater.dylib
- libCoreFSCache.dylib
- libCoreVMClient.dylib
- libDECHanyu.dylib
- libDECKanji.dylib
- libDHCPServer.A.dylib
- libETLDLFDynamic.dylib
- libETLDLOADCoreDumpDynamic.dylib
- libEUC.dylib
- libEUCTW.dylib
- libFosl_dynamic.dylib
- libGBK2K.dylib
- libGFXShared.dylib
- libGLImage.dylib
- libGPUSupportMercury.dylib
- libHDLCDynamic.dylib
- libHZ.dylib
- libIOAccessoryManager.dylib
- libIOReport.dylib
- libISO2022.dylib
- libJOHAB.dylib
- libMSKanji.dylib
- libMTLHud.dylib
- libMatch.1.dylib
- libODIECompiler.dylib
- libQuadrature.dylib
- libReverseProxyDevice.dylib
- libSMC.dylib
- libSpatial.dylib
- libSystem.B.dylib
- libSystem.B_asan.dylib
- libTelephonyUSBDynamic.dylib
- libType1Scaler.dylib
- libUES.dylib
- libUTF1632.dylib
- libUTF7.dylib
- libUTF8.dylib
- libUTF8MAC.dylib
- libVIQR.dylib
- libWAPI.dylib
- libZW.dylib
- libZhuGeArmory.dylib
- libZhuGeRoster.dylib
- libapp_launch_measurement.dylib
- libbsm.0.dylib
- libbz2.1.0.dylib
- libcache.dylib
- libcharset.1.dylib
- libcmph.dylib
- libcommonCrypto.dylib
- libcompiler_rt.dylib
- libcoretls.dylib
- libexpat.1.dylib
- libform.5.4.dylib
- libgermantok.dylib
- libheimdal-asn1.dylib
- libheimdalasn1.dylib
- libiconv.2.dylib
- libiconv_none.dylib
- libiconv_std.dylib
- libktrace.dylib
- liblaunch.dylib
- liblivefiles.plugin.dummy.dylib
- libllvm-lmdb.dylib
- liblog_SystemConfiguration.dylib
- liblog_network.dylib
- liblog_signpost.description.dylib
- liblog_signpost.dylib
- liblog_signpost.telemetry.dylib
- liblog_sonic.dylib
- liblzma.5.dylib
- libmapper_646.dylib
- libmapper_none.dylib
- libmapper_parallel.dylib
- libmapper_serial.dylib
- libmapper_std.dylib
- libmapper_zone.dylib
- libncurses.5.4.dylib
- libnetquality.dylib
- libnetwork.dylib
- libobjc-trampolines.dylib
- libperfcheck.dylib
- libpmsample.dylib
- libprequelite.dylib
- librealtime_safety.dylib
- libremovefile.dylib
- libresolv.9.dylib
- libsbuf.dylib
- libsp.dylib
- libswiftCoreAudio_Private.dylib
- libswiftFileProvider.dylib
- libswiftHealthKit.dylib
- libswiftMediaPlayer.dylib
- libswiftNearbyInteraction.dylib
- libswiftNetwork.dylib
- libswiftPhotos.dylib
- libswiftPhotosUI.dylib
- libswiftUIKit.dylib
- libswift_DarwinFoundation1.dylib
- libswift_DarwinFoundation2.dylib
- libswift_DarwinFoundation3.dylib
- libswift_Volatile.dylib
- libsysmon.dylib
- libsystem_blocks.dylib
- libsystem_blocks_debug.dylib
- libsystem_blocks_profile.dylib
- libsystem_collections.dylib
- libsystem_configuration.dylib
- libsystem_darwin.dylib
- libsystem_darwindirectory.dylib
- libsystem_m.dylib
- libsystem_notify.dylib
- libsystem_symptoms.dylib
- libsystem_trial.dylib
- libsystemstats.dylib
- libunwind.dylib
- libvMisc.dylib
- libxpc_datastores.dylib
- libz.1.dylib
- livefiles_cs.dylib
- locationd.events
- ltop
- mediaartworkd
- microstackshot
- model.dylib
- mount_hfs
- mount_nfs
- msdos.util
- newfs_apfs
- newfs_exfat
- newfs_hfs
- newfs_msdos
- newsd
- notifyd
- oncrpc
- powerdatad
- powerlogHelperd
- ps
- reversetemplated
- revisiond
- route
- screenshotsyncd
- siriknowledged
- sleepd
- snatmap
- softwareupdated
- splashboardd
- streaming_zip_conduit
- syslogd
- tightbeam_stub
- triald
- triald_system
- truncate
- umount
- userfsd
- vecLib
- vm_stat

</details>
