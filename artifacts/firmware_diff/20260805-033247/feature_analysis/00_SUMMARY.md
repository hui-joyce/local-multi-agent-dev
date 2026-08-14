# Feature Analysis Summary -- iOS 26.6

- **Total components in diff**: 3853  (**HIGH_SIGNAL**: 1961, **LOW_SIGNAL**: 1892)
- **Analysed** (report written): 100  |  **Apple Security Notes matches**: 175  |  **Suppressed TIER_3**: 0  |  **HIGH_SIGNAL not analysed** (budget/security filter): 1861

Tier shown is the LLM-assigned tier for analysed components, otherwise a deterministic estimate from the security score (4=Apple Security Notes, 3=hard indicator, 2=security vocabulary, 1=code change, 0=asset/UI/log).

## Apple Security Notes matches -- highest priority

<details><summary>Show 175 components</summary>

| Component | Tier | Sec score | Apple Security Notes | Report |
|---|---|---|---|---|
| +com.apple.driver.AppleProResHW (550.49) | TIER_1 | 4 | `Pro Res` | _not analysed_ |
| -com.apple.driver.AppleProResHW (550.48) | TIER_1 | 4 | `Pro Res` | _not analysed_ |
| AMSAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | [report](AMSAccountNotificationPlugin_analysis.md) |
| AXFrontBoardUtils | TIER_1 | 4 | `FrontBoard` | [report](AXFrontBoardUtils_analysis.md) |
| Accessibility | TIER_1 | 4 | `Accessibility` | [report](Accessibility_analysis.md) |
| AccessibilityFocusEngine | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityHeadphoneLevelsControlCenterModule | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityLiveListenControlCenterModule | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityMotionCuesControlCenterModule | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityPhysicalInteraction | TIER_1 | 4 | `Accessibility` | [report](AccessibilityPhysicalInteraction_analysis.md) |
| AccessibilityPlatformTranslation | TIER_1 | 4 | `Accessibility` | [report](AccessibilityPlatformTranslation_analysis.md) |
| AccessibilityReaderData | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityReaderServices | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityReadingUI | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityRemoteServices | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityRemoteUIServices | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilitySettings | TIER_1 | 4 | `Accessibility` | [report](AccessibilitySettings_analysis.md) |
| AccessibilitySettingsLoader | TIER_1 | 4 | `Accessibility` | [report](AccessibilitySettingsLoader_analysis.md) |
| AccessibilitySettingsUI | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilitySharedSupport | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityShorcutsModule | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilitySoundDetectionControlCenterModule | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityTextSizeModule | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityUI | TIER_1 | 4 | `Accessibility` | [report](AccessibilityUI_analysis.md) |
| AccessibilityUIService | TIER_1 | 4 | `Accessibility` | [report](AccessibilityUIService_analysis.md) |
| AccessibilityUIShared | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityUIUtilities | TIER_1 | 4 | `Accessibility` | [report](AccessibilityUIUtilities_analysis.md) |
| AccessibilityUIViewServices | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityUtilities | TIER_1 | 4 | `Accessibility` | [report](AccessibilityUtilities_analysis.md) |
| Accounts | TIER_1 | 4 | `Accounts Framework` | [report](Accounts_analysis.md) |
| AccountsDaemon | TIER_1 | 4 | `Accounts Framework` | [report](AccountsDaemon_analysis.md) |
| AccountsUISupport | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| AccountsUISupportShared | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| AppStore | TIER_1 | 4 | `App Store` | [report](AppStore_analysis.md) |
| AppleAccount | TIER_1 | 4 | `Accounts Framework` | [report](AppleAccount_analysis.md) |
| AppleAccountSettings | TIER_1 | 4 | `Accounts Framework` | [report](AppleAccountSettings_analysis.md) |
| AppleAccountTransparency | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| AppleAccountUI | TIER_1 | 4 | `Accounts Framework` | [report](AppleAccountUI_analysis.md) |
| AppleNeuralEngine | TIER_1 | 4 | `Apple Neural Engine` | [report](AppleNeuralEngine_analysis.md) |
| AppleProResHWDecoder.videodecoder | TIER_1 | 4 | `Pro Res` | _not analysed_ |
| AppleProResHWEncoder.videoencoder | TIER_1 | 4 | `Pro Res` | _not analysed_ |
| AuthKit | TIER_1 | 4 | `AuthKit` | [report](AuthKit_analysis.md) |
| BackgroundAssets | TIER_1 | 4 | `BackgroundAssets` | [report](BackgroundAssets_analysis.md) |
| Books | TIER_1 | 4 | `Books` | [report](Books_analysis.md) |
| ClassKitAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | [report](ClassKitAccountNotificationPlugin_analysis.md) |
| CloudAttestation | TIER_1 | 4 | `CloudAttestation` | [report](CloudAttestation_analysis.md) |
| ContactProvider | TIER_1 | 4 | `Contacts` | _not analysed_ |
| Contacts | TIER_1 | 4 | `Contacts` | [report](Contacts_analysis.md) |
| ContactsAutocomplete | TIER_1 | 4 | `Contacts` | _not analysed_ |
| ContactsAutocompleteUI | TIER_1 | 4 | `Contacts` | [report](ContactsAutocompleteUI_analysis.md) |
| ContactsDonation | TIER_1 | 4 | `Contacts` | _not analysed_ |
| ContactsDonationFeedback | TIER_1 | 4 | `Contacts` | _not analysed_ |
| ContactsFoundation | TIER_1 | 4 | `Contacts` | [report](ContactsFoundation_analysis.md) |
| ContactsMetrics | TIER_1 | 4 | `Contacts` | _not analysed_ |
| ContactsUI | TIER_1 | 4 | `Contacts` | [report](ContactsUI_analysis.md) |
| ContactsUICore | TIER_1 | 4 | `Contacts` | [report](ContactsUICore_analysis.md) |
| ContactsWidgetUI | TIER_1 | 4 | `Contacts` | _not analysed_ |
| CoreAudio | TIER_1 | 4 | `CoreAudio` | _not analysed_ |
| CoreMedia | TIER_1 | 4 | `CoreMedia` | [report](CoreMedia_analysis.md) |
| CoreWiFi | TIER_1 | 4 | `Wi-Fi` | [report](CoreWiFi_analysis.md) |
| DAAccount | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| DriverKit | TIER_1 | 4 | `DriverKit` | _not analysed_ |
| FitnessWorkoutPlan | TIER_1 | 4 | `WorkoutKit` | _not analysed_ |
| Foundation | TIER_1 | 4 | `Foundation` | [report](Foundation_analysis.md) |
| FrontBoard | TIER_1 | 4 | `FrontBoard` | [report](FrontBoard_analysis.md) |
| FrontBoardServices | TIER_1 | 4 | `FrontBoard` | _not analysed_ |
| GameCenterDashboardExtension | TIER_1 | 4 | `Game Center` | [report](GameCenterDashboardExtension_analysis.md) |
| GameCenterFoundation | TIER_1 | 4 | `Game Center` | [report](GameCenterFoundation_analysis.md) |
| GameCenterOverlayService | TIER_1 | 4 | `Game Center` | _not analysed_ |
| GameCenterServerClient | TIER_1 | 4 | `Game Center` | _not analysed_ |
| GameCenterUICore | TIER_1 | 4 | `Game Center` | _not analysed_ |
| GameCenterUIFramework | TIER_1 | 4 | `Game Center` | [report](GameCenterUIFramework_analysis.md) |
| HealthKitAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| IDSAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| IMAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| IOKit | TIER_1 | 4 | `IOKit` | [report](IOKit_analysis.md) |
| ImageIO | TIER_1 | 4 | `ImageIO` | [report](ImageIO_analysis.md) |
| KeychainSyncAccountNotification | TIER_1 | 4 | `Accounts Framework` | [report](KeychainSyncAccountNotification_analysis.md) |
| LockdownModeAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| MailAccountSettings | TIER_1 | 4 | `Accounts Framework` | [report](MailAccountSettings_analysis.md) |
| Managed Background Assets Processing Pipeline | TIER_1 | 4 | `BackgroundAssets` | [report](Managed_Background_Assets_Processing_Pipeline_analysis.md) |
| ManagedBackgroundAssets | TIER_1 | 4 | `BackgroundAssets` | [report](ManagedBackgroundAssets_analysis.md) |
| ManagedBackgroundAssetsHelper | TIER_1 | 4 | `BackgroundAssets` | [report](ManagedBackgroundAssetsHelper_analysis.md) |
| ManagedBackgroundAssetsHelperFetching | TIER_1 | 4 | `BackgroundAssets` | [report](ManagedBackgroundAssetsHelperFetching_analysis.md) |
| ManagedBackgroundAssetsRelay | TIER_1 | 4 | `BackgroundAssets` | _not analysed_ |
| ManagedBackgroundAssetsXPC | TIER_1 | 4 | `BackgroundAssets` | [report](ManagedBackgroundAssetsXPC_analysis.md) |
| ManagedConfiguration | TIER_1 | 4 | `Managed Configuration` | [report](ManagedConfiguration_analysis.md) |
| ManagedOrganizationContacts | TIER_1 | 4 | `Contacts` | _not analysed_ |
| MediaRemote | TIER_1 | 4 | `MediaRemote` | [report](MediaRemote_analysis.md) |
| MediaRemoteDaemonServices | TIER_1 | 4 | `MediaRemote` | _not analysed_ |
| MessageAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| MobileSyncAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| MobileWiFi | TIER_1 | 4 | `Wi-Fi` | _not analysed_ |
| NanoMediaRemote | TIER_1 | 4 | `MediaRemote` | _not analysed_ |
| NotesAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| PCSAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| PassbookAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| PhotosAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| RPAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| RemindersAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| RemoteMediaServices | TIER_1 | 4 | `MediaRemote` | _not analysed_ |
| SceneKit | TIER_1 | 4 | `SceneKit` | [report](SceneKit_analysis.md) |
| SearchPartyAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| ServicesAccountLinking | TIER_1 | 4 | `Accounts Framework` | [report](ServicesAccountLinking_analysis.md) |
| ServicesAccountLinkingService | TIER_1 | 4 | `Accounts Framework` | [report](ServicesAccountLinkingService_analysis.md) |
| SharingAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| ShortcutsCloudKitAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| Siri | TIER_1 | 4 | `Siri` | [report](Siri_analysis.md) |
| SiriCloudKitAccountsNotifier | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| SiriContactsCommon | TIER_1 | 4 | `Contacts` | _not analysed_ |
| SiriContactsIntents | TIER_1 | 4 | `Contacts` | _not analysed_ |
| SiriContactsUI | TIER_1 | 4 | `Contacts` | _not analysed_ |
| SwiftUIAccessibility | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| UIAccessibility | TIER_1 | 4 | `Accessibility` | [report](UIAccessibility_analysis.md) |
| VideoSubscriberAccount | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| VideoSubscriberAccountUI | TIER_1 | 4 | `Accounts Framework` | [report](VideoSubscriberAccountUI_analysis.md) |
| WiFiAnalytics | TIER_1 | 4 | `Wi-Fi` | [report](WiFiAnalytics_analysis.md) |
| WiFiAware | TIER_1 | 4 | `Wi-Fi` | [report](WiFiAware_analysis.md) |
| WiFiCloudAssetsXPCService | TIER_1 | 4 | `Wi-Fi` | [report](WiFiCloudAssetsXPCService_analysis.md) |
| WiFiCloudSyncEngine | TIER_1 | 4 | `Wi-Fi` | [report](WiFiCloudSyncEngine_analysis.md) |
| WiFiInfrastructure | TIER_1 | 4 | `Wi-Fi` | [report](WiFiInfrastructure_analysis.md) |
| WiFiKit | TIER_1 | 4 | `Wi-Fi` | [report](WiFiKit_analysis.md) |
| WiFiKitUI | TIER_1 | 4 | `Wi-Fi` | [report](WiFiKitUI_analysis.md) |
| WiFiLogCapture | TIER_1 | 4 | `Wi-Fi` | _not analysed_ |
| WiFiPeerToPeer | TIER_1 | 4 | `Wi-Fi` | _not analysed_ |
| WiFiPolicy | TIER_1 | 4 | `Wi-Fi` | [report](WiFiPolicy_analysis.md) |
| WiFiSettingsKit | TIER_1 | 4 | `Wi-Fi` | _not analysed_ |
| WiFiSharing | TIER_1 | 4 | `Wi-Fi` | _not analysed_ |
| WiFiVelocity | TIER_1 | 4 | `Wi-Fi` | _not analysed_ |
| WorkoutCore | TIER_1 | 4 | `WorkoutKit` | [report](WorkoutCore_analysis.md) |
| WorkoutHealthBridge | TIER_1 | 4 | `WorkoutKit` | _not analysed_ |
| WorkoutKit | TIER_1 | 4 | `WorkoutKit` | _not analysed_ |
| WorkoutKitServices | TIER_1 | 4 | `WorkoutKit` | [report](WorkoutKitServices_analysis.md) |
| WorkoutKitUI | TIER_1 | 4 | `WorkoutKit` | _not analysed_ |
| WorkoutKitXPCService | TIER_1 | 4 | `WorkoutKit` | [report](WorkoutKitXPCService_analysis.md) |
| WorkoutUI | TIER_1 | 4 | `WorkoutKit` | [report](WorkoutUI_analysis.md) |
| _WorkoutKit_SwiftUI | TIER_1 | 4 | `WorkoutKit` | _not analysed_ |
| com.apple.askpermission.AccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| com.apple.driver.AppleProResHW | TIER_1 | 4 | `Pro Res` | _not analysed_ |
| com.apple.kernel | TIER_1 | 4 | `Kernel` | [report](com.apple.kernel_analysis.md) |
| libAccessibility.dylib | TIER_1 | 4 | `Accessibility` | [report](libAccessibility.dylib_analysis.md) |
| libarchive.2.dylib | TIER_1 | 4 | `libarchive` | [report](libarchive.2.dylib_analysis.md) |
| mDNSResponder | TIER_1 | 4 | `mDNSResponder` | [report](mDNSResponder_analysis.md) |
| AAAccountNotificationPlugin | TIER_2 | 4 | `Accounts Framework` | [report](AAAccountNotificationPlugin_analysis.md) |
| AAIDMSAccountNotificationPlugin | TIER_2 | 4 | `Accounts Framework` | [report](AAIDMSAccountNotificationPlugin_analysis.md) |
| ADAccountsNotificationPlugin | TIER_2 | 4 | `Accounts Framework` | [report](ADAccountsNotificationPlugin_analysis.md) |
| AISAccountNotificationPlugin | TIER_2 | 4 | `Accounts Framework` | [report](AISAccountNotificationPlugin_analysis.md) |
| AKAccountNotificationPlugin | TIER_2 | 4 | `Accounts Framework` | [report](AKAccountNotificationPlugin_analysis.md) |
| AMSAccountAuthenticationPlugin | TIER_2 | 4 | `Accounts Framework` | [report](AMSAccountAuthenticationPlugin_analysis.md) |
| AMSAccountSyncNotificationPlugin | TIER_2 | 4 | `Accounts Framework` | [report](AMSAccountSyncNotificationPlugin_analysis.md) |
| AccountsUI | TIER_2 | 4 | `Accounts Framework` | [report](AccountsUI_analysis.md) |
| CDPAccountNotificationPlugin_IOS | TIER_2 | 4 | `Accounts Framework` | [report](CDPAccountNotificationPlugin_IOS_analysis.md) |
| DAAccountAuthenticator | TIER_2 | 4 | `Accounts Framework` | [report](DAAccountAuthenticator_analysis.md) |
| DAAccountNotifier | TIER_2 | 4 | `Accounts Framework` | [report](DAAccountNotifier_analysis.md) |
| FMFLocatorAccountNotificationPlugin | TIER_2 | 4 | `Accounts Framework` | [report](FMFLocatorAccountNotificationPlugin_analysis.md) |
| FindMyDeviceAccountNotificationPlugin | TIER_2 | 4 | `Accounts Framework` | [report](FindMyDeviceAccountNotificationPlugin_analysis.md) |
| GameCenterPrivateUIFramework | TIER_2 | 4 | `Game Center` | [report](GameCenterPrivateUIFramework_analysis.md) |
| GameCenterUI | TIER_2 | 4 | `Game Center` | [report](GameCenterUI_analysis.md) |
| GameCenterUIService | TIER_2 | 4 | `Game Center` | [report](GameCenterUIService_analysis.md) |
| Heimdal | TIER_2 | 4 | `Heimdal` | [report](Heimdal_analysis.md) |
| Managed Background Assets Helper Service | TIER_2 | 4 | `BackgroundAssets` | [report](Managed_Background_Assets_Helper_Service_analysis.md) |
| ManagedConfigurationUI | TIER_2 | 4 | `Managed Configuration` | [report](ManagedConfigurationUI_analysis.md) |
| WebKit | TIER_2 | 4 | `WebKit` | [report](WebKit_analysis.md) |
| ASDAccountNotficationPlugin | TIER_3 | 4 | `Accounts Framework` | [report](ASDAccountNotficationPlugin_analysis.md) |
| AccessibilitySharedUISupport | TIER_3 | 4 | `Accessibility` | [report](AccessibilitySharedUISupport_analysis.md) |
| BTCloudPairingAccountNotificationPlugin | TIER_3 | 4 | `Accounts Framework` | [report](BTCloudPairingAccountNotificationPlugin_analysis.md) |
| CoreLocationAccountNotificationPlugin | TIER_3 | 4 | `Accounts Framework` | [report](CoreLocationAccountNotificationPlugin_analysis.md) |
| CoreRecentsAccountNotificationPlugin | TIER_3 | 4 | `Accounts Framework` | [report](CoreRecentsAccountNotificationPlugin_analysis.md) |
| DonationAccountWatcher | TIER_3 | 4 | `Accounts Framework` | [report](DonationAccountWatcher_analysis.md) |
| Game Center | TIER_3 | 4 | `Game Center` | [report](Game_Center_analysis.md) |
| GameCenterAccountNotificationPlugin | TIER_3 | 4 | `Game Center` | [report](GameCenterAccountNotificationPlugin_analysis.md) |
| Managed Background Assets Helper Fetching Service | TIER_3 | 4 | `BackgroundAssets` | [report](Managed_Background_Assets_Helper_Fetching_Service_analysis.md) |
| MediaAccessibility | TIER_3 | 4 | `Accessibility` | [report](MediaAccessibility_analysis.md) |
| MessageAccountAuthenticationPlugin | TIER_3 | 4 | `Accounts Framework` | [report](MessageAccountAuthenticationPlugin_analysis.md) |
| iCloudMailAccountUI | TIER_3 | 4 | `Accounts Framework` | [report](iCloudMailAccountUI_analysis.md) |

</details>

## Analysed components (reports written)

<details><summary>Show 100 components</summary>

| Component | Tier | Sec score | Apple Security Notes | Report |
|---|---|---|---|---|
| AMSAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | [report](AMSAccountNotificationPlugin_analysis.md) |
| AXFrontBoardUtils | TIER_1 | 4 | `FrontBoard` | [report](AXFrontBoardUtils_analysis.md) |
| Accessibility | TIER_1 | 4 | `Accessibility` | [report](Accessibility_analysis.md) |
| AccessibilityPhysicalInteraction | TIER_1 | 4 | `Accessibility` | [report](AccessibilityPhysicalInteraction_analysis.md) |
| AccessibilityPlatformTranslation | TIER_1 | 4 | `Accessibility` | [report](AccessibilityPlatformTranslation_analysis.md) |
| AccessibilitySettings | TIER_1 | 4 | `Accessibility` | [report](AccessibilitySettings_analysis.md) |
| AccessibilitySettingsLoader | TIER_1 | 4 | `Accessibility` | [report](AccessibilitySettingsLoader_analysis.md) |
| AccessibilityUI | TIER_1 | 4 | `Accessibility` | [report](AccessibilityUI_analysis.md) |
| AccessibilityUIService | TIER_1 | 4 | `Accessibility` | [report](AccessibilityUIService_analysis.md) |
| AccessibilityUIUtilities | TIER_1 | 4 | `Accessibility` | [report](AccessibilityUIUtilities_analysis.md) |
| AccessibilityUtilities | TIER_1 | 4 | `Accessibility` | [report](AccessibilityUtilities_analysis.md) |
| Accounts | TIER_1 | 4 | `Accounts Framework` | [report](Accounts_analysis.md) |
| AccountsDaemon | TIER_1 | 4 | `Accounts Framework` | [report](AccountsDaemon_analysis.md) |
| AppStore | TIER_1 | 4 | `App Store` | [report](AppStore_analysis.md) |
| AppleAccount | TIER_1 | 4 | `Accounts Framework` | [report](AppleAccount_analysis.md) |
| AppleAccountSettings | TIER_1 | 4 | `Accounts Framework` | [report](AppleAccountSettings_analysis.md) |
| AppleAccountUI | TIER_1 | 4 | `Accounts Framework` | [report](AppleAccountUI_analysis.md) |
| AppleNeuralEngine | TIER_1 | 4 | `Apple Neural Engine` | [report](AppleNeuralEngine_analysis.md) |
| AuthKit | TIER_1 | 4 | `AuthKit` | [report](AuthKit_analysis.md) |
| BackgroundAssets | TIER_1 | 4 | `BackgroundAssets` | [report](BackgroundAssets_analysis.md) |
| Books | TIER_1 | 4 | `Books` | [report](Books_analysis.md) |
| ClassKitAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | [report](ClassKitAccountNotificationPlugin_analysis.md) |
| CloudAttestation | TIER_1 | 4 | `CloudAttestation` | [report](CloudAttestation_analysis.md) |
| Contacts | TIER_1 | 4 | `Contacts` | [report](Contacts_analysis.md) |
| ContactsAutocompleteUI | TIER_1 | 4 | `Contacts` | [report](ContactsAutocompleteUI_analysis.md) |
| ContactsFoundation | TIER_1 | 4 | `Contacts` | [report](ContactsFoundation_analysis.md) |
| ContactsUI | TIER_1 | 4 | `Contacts` | [report](ContactsUI_analysis.md) |
| ContactsUICore | TIER_1 | 4 | `Contacts` | [report](ContactsUICore_analysis.md) |
| CoreMedia | TIER_1 | 4 | `CoreMedia` | [report](CoreMedia_analysis.md) |
| CoreWiFi | TIER_1 | 4 | `Wi-Fi` | [report](CoreWiFi_analysis.md) |
| Foundation | TIER_1 | 4 | `Foundation` | [report](Foundation_analysis.md) |
| FrontBoard | TIER_1 | 4 | `FrontBoard` | [report](FrontBoard_analysis.md) |
| GameCenterDashboardExtension | TIER_1 | 4 | `Game Center` | [report](GameCenterDashboardExtension_analysis.md) |
| GameCenterFoundation | TIER_1 | 4 | `Game Center` | [report](GameCenterFoundation_analysis.md) |
| GameCenterUIFramework | TIER_1 | 4 | `Game Center` | [report](GameCenterUIFramework_analysis.md) |
| IOKit | TIER_1 | 4 | `IOKit` | [report](IOKit_analysis.md) |
| ImageIO | TIER_1 | 4 | `ImageIO` | [report](ImageIO_analysis.md) |
| KeychainSyncAccountNotification | TIER_1 | 4 | `Accounts Framework` | [report](KeychainSyncAccountNotification_analysis.md) |
| MailAccountSettings | TIER_1 | 4 | `Accounts Framework` | [report](MailAccountSettings_analysis.md) |
| Managed Background Assets Processing Pipeline | TIER_1 | 4 | `BackgroundAssets` | [report](Managed_Background_Assets_Processing_Pipeline_analysis.md) |
| ManagedBackgroundAssets | TIER_1 | 4 | `BackgroundAssets` | [report](ManagedBackgroundAssets_analysis.md) |
| ManagedBackgroundAssetsHelper | TIER_1 | 4 | `BackgroundAssets` | [report](ManagedBackgroundAssetsHelper_analysis.md) |
| ManagedBackgroundAssetsHelperFetching | TIER_1 | 4 | `BackgroundAssets` | [report](ManagedBackgroundAssetsHelperFetching_analysis.md) |
| ManagedBackgroundAssetsXPC | TIER_1 | 4 | `BackgroundAssets` | [report](ManagedBackgroundAssetsXPC_analysis.md) |
| ManagedConfiguration | TIER_1 | 4 | `Managed Configuration` | [report](ManagedConfiguration_analysis.md) |
| MediaRemote | TIER_1 | 4 | `MediaRemote` | [report](MediaRemote_analysis.md) |
| SceneKit | TIER_1 | 4 | `SceneKit` | [report](SceneKit_analysis.md) |
| ServicesAccountLinking | TIER_1 | 4 | `Accounts Framework` | [report](ServicesAccountLinking_analysis.md) |
| ServicesAccountLinkingService | TIER_1 | 4 | `Accounts Framework` | [report](ServicesAccountLinkingService_analysis.md) |
| Siri | TIER_1 | 4 | `Siri` | [report](Siri_analysis.md) |
| UIAccessibility | TIER_1 | 4 | `Accessibility` | [report](UIAccessibility_analysis.md) |
| VideoSubscriberAccountUI | TIER_1 | 4 | `Accounts Framework` | [report](VideoSubscriberAccountUI_analysis.md) |
| WiFiAnalytics | TIER_1 | 4 | `Wi-Fi` | [report](WiFiAnalytics_analysis.md) |
| WiFiAware | TIER_1 | 4 | `Wi-Fi` | [report](WiFiAware_analysis.md) |
| WiFiCloudAssetsXPCService | TIER_1 | 4 | `Wi-Fi` | [report](WiFiCloudAssetsXPCService_analysis.md) |
| WiFiCloudSyncEngine | TIER_1 | 4 | `Wi-Fi` | [report](WiFiCloudSyncEngine_analysis.md) |
| WiFiInfrastructure | TIER_1 | 4 | `Wi-Fi` | [report](WiFiInfrastructure_analysis.md) |
| WiFiKit | TIER_1 | 4 | `Wi-Fi` | [report](WiFiKit_analysis.md) |
| WiFiKitUI | TIER_1 | 4 | `Wi-Fi` | [report](WiFiKitUI_analysis.md) |
| WiFiPolicy | TIER_1 | 4 | `Wi-Fi` | [report](WiFiPolicy_analysis.md) |
| WorkoutCore | TIER_1 | 4 | `WorkoutKit` | [report](WorkoutCore_analysis.md) |
| WorkoutKitServices | TIER_1 | 4 | `WorkoutKit` | [report](WorkoutKitServices_analysis.md) |
| WorkoutKitXPCService | TIER_1 | 4 | `WorkoutKit` | [report](WorkoutKitXPCService_analysis.md) |
| WorkoutUI | TIER_1 | 4 | `WorkoutKit` | [report](WorkoutUI_analysis.md) |
| com.apple.kernel | TIER_1 | 4 | `Kernel` | [report](com.apple.kernel_analysis.md) |
| libAccessibility.dylib | TIER_1 | 4 | `Accessibility` | [report](libAccessibility.dylib_analysis.md) |
| libarchive.2.dylib | TIER_1 | 4 | `libarchive` | [report](libarchive.2.dylib_analysis.md) |
| mDNSResponder | TIER_1 | 4 | `mDNSResponder` | [report](mDNSResponder_analysis.md) |
| AAAccountNotificationPlugin | TIER_2 | 4 | `Accounts Framework` | [report](AAAccountNotificationPlugin_analysis.md) |
| AAIDMSAccountNotificationPlugin | TIER_2 | 4 | `Accounts Framework` | [report](AAIDMSAccountNotificationPlugin_analysis.md) |
| ADAccountsNotificationPlugin | TIER_2 | 4 | `Accounts Framework` | [report](ADAccountsNotificationPlugin_analysis.md) |
| AISAccountNotificationPlugin | TIER_2 | 4 | `Accounts Framework` | [report](AISAccountNotificationPlugin_analysis.md) |
| AKAccountNotificationPlugin | TIER_2 | 4 | `Accounts Framework` | [report](AKAccountNotificationPlugin_analysis.md) |
| AMSAccountAuthenticationPlugin | TIER_2 | 4 | `Accounts Framework` | [report](AMSAccountAuthenticationPlugin_analysis.md) |
| AMSAccountSyncNotificationPlugin | TIER_2 | 4 | `Accounts Framework` | [report](AMSAccountSyncNotificationPlugin_analysis.md) |
| AccountsUI | TIER_2 | 4 | `Accounts Framework` | [report](AccountsUI_analysis.md) |
| CDPAccountNotificationPlugin_IOS | TIER_2 | 4 | `Accounts Framework` | [report](CDPAccountNotificationPlugin_IOS_analysis.md) |
| DAAccountAuthenticator | TIER_2 | 4 | `Accounts Framework` | [report](DAAccountAuthenticator_analysis.md) |
| DAAccountNotifier | TIER_2 | 4 | `Accounts Framework` | [report](DAAccountNotifier_analysis.md) |
| FMFLocatorAccountNotificationPlugin | TIER_2 | 4 | `Accounts Framework` | [report](FMFLocatorAccountNotificationPlugin_analysis.md) |
| FindMyDeviceAccountNotificationPlugin | TIER_2 | 4 | `Accounts Framework` | [report](FindMyDeviceAccountNotificationPlugin_analysis.md) |
| GameCenterPrivateUIFramework | TIER_2 | 4 | `Game Center` | [report](GameCenterPrivateUIFramework_analysis.md) |
| GameCenterUI | TIER_2 | 4 | `Game Center` | [report](GameCenterUI_analysis.md) |
| GameCenterUIService | TIER_2 | 4 | `Game Center` | [report](GameCenterUIService_analysis.md) |
| Heimdal | TIER_2 | 4 | `Heimdal` | [report](Heimdal_analysis.md) |
| Managed Background Assets Helper Service | TIER_2 | 4 | `BackgroundAssets` | [report](Managed_Background_Assets_Helper_Service_analysis.md) |
| ManagedConfigurationUI | TIER_2 | 4 | `Managed Configuration` | [report](ManagedConfigurationUI_analysis.md) |
| WebKit | TIER_2 | 4 | `WebKit` | [report](WebKit_analysis.md) |
| ASDAccountNotficationPlugin | TIER_3 | 4 | `Accounts Framework` | [report](ASDAccountNotficationPlugin_analysis.md) |
| AccessibilitySharedUISupport | TIER_3 | 4 | `Accessibility` | [report](AccessibilitySharedUISupport_analysis.md) |
| BTCloudPairingAccountNotificationPlugin | TIER_3 | 4 | `Accounts Framework` | [report](BTCloudPairingAccountNotificationPlugin_analysis.md) |
| CoreLocationAccountNotificationPlugin | TIER_3 | 4 | `Accounts Framework` | [report](CoreLocationAccountNotificationPlugin_analysis.md) |
| CoreRecentsAccountNotificationPlugin | TIER_3 | 4 | `Accounts Framework` | [report](CoreRecentsAccountNotificationPlugin_analysis.md) |
| DonationAccountWatcher | TIER_3 | 4 | `Accounts Framework` | [report](DonationAccountWatcher_analysis.md) |
| Game Center | TIER_3 | 4 | `Game Center` | [report](Game_Center_analysis.md) |
| GameCenterAccountNotificationPlugin | TIER_3 | 4 | `Game Center` | [report](GameCenterAccountNotificationPlugin_analysis.md) |
| Managed Background Assets Helper Fetching Service | TIER_3 | 4 | `BackgroundAssets` | [report](Managed_Background_Assets_Helper_Fetching_Service_analysis.md) |
| MediaAccessibility | TIER_3 | 4 | `Accessibility` | [report](MediaAccessibility_analysis.md) |
| MessageAccountAuthenticationPlugin | TIER_3 | 4 | `Accounts Framework` | [report](MessageAccountAuthenticationPlugin_analysis.md) |
| iCloudMailAccountUI | TIER_3 | 4 | `Accounts Framework` | [report](iCloudMailAccountUI_analysis.md) |

</details>

## HIGH_SIGNAL -- flagged security-relevant but not analysed (605, over budget)

<details><summary>Show 605 components</summary>

| Component | Tier | Sec score | Apple Security Notes | Report |
|---|---|---|---|---|
| +com.apple.driver.AppleProResHW (550.49) | TIER_1 | 4 | `Pro Res` | _not analysed_ |
| -com.apple.driver.AppleProResHW (550.48) | TIER_1 | 4 | `Pro Res` | _not analysed_ |
| AccessibilityFocusEngine | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityHeadphoneLevelsControlCenterModule | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityLiveListenControlCenterModule | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityMotionCuesControlCenterModule | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityReaderData | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityReaderServices | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityReadingUI | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityRemoteServices | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityRemoteUIServices | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilitySettingsUI | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilitySharedSupport | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityShorcutsModule | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilitySoundDetectionControlCenterModule | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityTextSizeModule | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityUIShared | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccessibilityUIViewServices | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| AccountsUISupport | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| AccountsUISupportShared | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| AppleAccountTransparency | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| AppleProResHWDecoder.videodecoder | TIER_1 | 4 | `Pro Res` | _not analysed_ |
| AppleProResHWEncoder.videoencoder | TIER_1 | 4 | `Pro Res` | _not analysed_ |
| ContactProvider | TIER_1 | 4 | `Contacts` | _not analysed_ |
| ContactsAutocomplete | TIER_1 | 4 | `Contacts` | _not analysed_ |
| ContactsDonation | TIER_1 | 4 | `Contacts` | _not analysed_ |
| ContactsDonationFeedback | TIER_1 | 4 | `Contacts` | _not analysed_ |
| ContactsMetrics | TIER_1 | 4 | `Contacts` | _not analysed_ |
| ContactsWidgetUI | TIER_1 | 4 | `Contacts` | _not analysed_ |
| CoreAudio | TIER_1 | 4 | `CoreAudio` | _not analysed_ |
| DAAccount | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| DriverKit | TIER_1 | 4 | `DriverKit` | _not analysed_ |
| FitnessWorkoutPlan | TIER_1 | 4 | `WorkoutKit` | _not analysed_ |
| FrontBoardServices | TIER_1 | 4 | `FrontBoard` | _not analysed_ |
| GameCenterOverlayService | TIER_1 | 4 | `Game Center` | _not analysed_ |
| GameCenterServerClient | TIER_1 | 4 | `Game Center` | _not analysed_ |
| GameCenterUICore | TIER_1 | 4 | `Game Center` | _not analysed_ |
| HealthKitAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| IDSAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| IMAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| LockdownModeAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| ManagedBackgroundAssetsRelay | TIER_1 | 4 | `BackgroundAssets` | _not analysed_ |
| ManagedOrganizationContacts | TIER_1 | 4 | `Contacts` | _not analysed_ |
| MediaRemoteDaemonServices | TIER_1 | 4 | `MediaRemote` | _not analysed_ |
| MessageAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| MobileSyncAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| MobileWiFi | TIER_1 | 4 | `Wi-Fi` | _not analysed_ |
| NanoMediaRemote | TIER_1 | 4 | `MediaRemote` | _not analysed_ |
| NotesAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| PCSAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| PassbookAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| PhotosAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| RPAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| RemindersAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| RemoteMediaServices | TIER_1 | 4 | `MediaRemote` | _not analysed_ |
| SearchPartyAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| SharingAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| ShortcutsCloudKitAccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| SiriCloudKitAccountsNotifier | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| SiriContactsCommon | TIER_1 | 4 | `Contacts` | _not analysed_ |
| SiriContactsIntents | TIER_1 | 4 | `Contacts` | _not analysed_ |
| SiriContactsUI | TIER_1 | 4 | `Contacts` | _not analysed_ |
| SwiftUIAccessibility | TIER_1 | 4 | `Accessibility` | _not analysed_ |
| VideoSubscriberAccount | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| WiFiLogCapture | TIER_1 | 4 | `Wi-Fi` | _not analysed_ |
| WiFiPeerToPeer | TIER_1 | 4 | `Wi-Fi` | _not analysed_ |
| WiFiSettingsKit | TIER_1 | 4 | `Wi-Fi` | _not analysed_ |
| WiFiSharing | TIER_1 | 4 | `Wi-Fi` | _not analysed_ |
| WiFiVelocity | TIER_1 | 4 | `Wi-Fi` | _not analysed_ |
| WorkoutHealthBridge | TIER_1 | 4 | `WorkoutKit` | _not analysed_ |
| WorkoutKit | TIER_1 | 4 | `WorkoutKit` | _not analysed_ |
| WorkoutKitUI | TIER_1 | 4 | `WorkoutKit` | _not analysed_ |
| _WorkoutKit_SwiftUI | TIER_1 | 4 | `WorkoutKit` | _not analysed_ |
| com.apple.askpermission.AccountNotificationPlugin | TIER_1 | 4 | `Accounts Framework` | _not analysed_ |
| com.apple.driver.AppleProResHW | TIER_1 | 4 | `Pro Res` | _not analysed_ |
| APFS | TIER_1 | 3 | -- | _not analysed_ |
| AVConference | TIER_1 | 3 | -- | _not analysed_ |
| AppSubscriptions | TIER_1 | 3 | -- | _not analysed_ |
| AppleCIOFusion | TIER_1 | 3 | -- | _not analysed_ |
| CacheDelete | TIER_1 | 3 | -- | _not analysed_ |
| CallHistory | TIER_1 | 3 | -- | _not analysed_ |
| ChatKit | TIER_1 | 3 | -- | _not analysed_ |
| CommCenter | TIER_1 | 3 | -- | _not analysed_ |
| CoreBrightness | TIER_1 | 3 | -- | _not analysed_ |
| CoreCDPInternal | TIER_1 | 3 | -- | _not analysed_ |
| CoreDiagnostics | TIER_1 | 3 | -- | _not analysed_ |
| CoreServices | TIER_1 | 3 | -- | _not analysed_ |
| CryptexServer | TIER_1 | 3 | -- | _not analysed_ |
| DeviceIdentity | TIER_1 | 3 | -- | _not analysed_ |
| FSKit | TIER_1 | 3 | -- | _not analysed_ |
| GameKitServices | TIER_1 | 3 | -- | _not analysed_ |
| HDRProcessing | TIER_1 | 3 | -- | _not analysed_ |
| ICE | TIER_1 | 3 | -- | _not analysed_ |
| IMCore | TIER_1 | 3 | -- | _not analysed_ |
| IconServices | TIER_1 | 3 | -- | _not analysed_ |
| KeychainCircle | TIER_1 | 3 | -- | _not analysed_ |
| Maps | TIER_1 | 3 | -- | _not analysed_ |
| Measure | TIER_1 | 3 | -- | _not analysed_ |
| MigrationKit | TIER_1 | 3 | -- | _not analysed_ |
| MobileActivationMigrator | TIER_1 | 3 | -- | _not analysed_ |
| Morpheus | TIER_1 | 3 | -- | _not analysed_ |
| NeutrinoKit | TIER_1 | 3 | -- | _not analysed_ |
| PhoneCallFlowDelegatePlugin | TIER_1 | 3 | -- | _not analysed_ |
| Rules | TIER_1 | 3 | -- | _not analysed_ |
| SearchPersonalization | TIER_1 | 3 | -- | _not analysed_ |
| Security | TIER_1 | 3 | -- | _not analysed_ |
| Setup | TIER_1 | 3 | -- | _not analysed_ |
| SpotlightDaemon | TIER_1 | 3 | -- | _not analysed_ |
| Translation | TIER_1 | 3 | -- | _not analysed_ |
| accessoryd | TIER_1 | 3 | -- | _not analysed_ |
| apfs_checkseal | TIER_1 | 3 | -- | _not analysed_ |
| apfs_condenser | TIER_1 | 3 | -- | _not analysed_ |
| apfs_vol_converter | TIER_1 | 3 | -- | _not analysed_ |
| com.apple.AGXG18P | TIER_1 | 3 | -- | _not analysed_ |
| com.apple.driver.AppleAVE2 | TIER_1 | 3 | -- | _not analysed_ |
| com.apple.driver.AppleJPEGDriver | TIER_1 | 3 | -- | _not analysed_ |
| com.apple.driver.ApplePMGR | TIER_1 | 3 | -- | _not analysed_ |
| com.apple.filesystems.apfs | TIER_1 | 3 | -- | _not analysed_ |
| com.apple.iokit.IOSurface | TIER_1 | 3 | -- | _not analysed_ |
| destinationd | TIER_1 | 3 | -- | _not analysed_ |
| exclave_roottask | TIER_1 | 3 | -- | _not analysed_ |
| exclave_sharedcache | TIER_1 | 3 | -- | _not analysed_ |
| fsck_apfs | TIER_1 | 3 | -- | _not analysed_ |
| iCloudDriveCore | TIER_1 | 3 | -- | _not analysed_ |
| libBNNS.dylib | TIER_1 | 3 | -- | _not analysed_ |
| libcryptex_core.dylib | TIER_1 | 3 | -- | _not analysed_ |
| libmalloc_exclaves_introspector | TIER_1 | 3 | -- | _not analysed_ |
| libsystem_malloc.dylib | TIER_1 | 3 | -- | _not analysed_ |
| libsystem_malloc_debug.dylib | TIER_1 | 3 | -- | _not analysed_ |
| libusd_ms.dylib | TIER_1 | 3 | -- | _not analysed_ |
| livefiles_apfs.dylib | TIER_1 | 3 | -- | _not analysed_ |
| misd | TIER_1 | 3 | -- | _not analysed_ |
| securityd | TIER_1 | 3 | -- | _not analysed_ |
| slurpAPFSMeta | TIER_1 | 3 | -- | _not analysed_ |
| sm_stats | TIER_1 | 3 | -- | _not analysed_ |
| spaceattributiond | TIER_1 | 3 | -- | _not analysed_ |
| threadradiod | TIER_1 | 3 | -- | _not analysed_ |
| trustd | TIER_1 | 3 | -- | _not analysed_ |
| vm_stat | TIER_1 | 3 | -- | _not analysed_ |
| AAAFoundation | TIER_2 | 2 | -- | _not analysed_ |
| ANECompilerService | TIER_2 | 2 | -- | _not analysed_ |
| APFoundation | TIER_2 | 2 | -- | _not analysed_ |
| ASOctaneSupportXPCService | TIER_2 | 2 | -- | _not analysed_ |
| AVKit | TIER_2 | 2 | -- | _not analysed_ |
| AccessoryNotifications | TIER_2 | 2 | -- | _not analysed_ |
| AccessorySetupKit | TIER_2 | 2 | -- | _not analysed_ |
| AccessorySetupUI | TIER_2 | 2 | -- | _not analysed_ |
| AccessoryTransportExtension | TIER_2 | 2 | -- | _not analysed_ |
| ActionKit | TIER_2 | 2 | -- | _not analysed_ |
| ActivityKit | TIER_2 | 2 | -- | _not analysed_ |
| ActivitySharingDaemonCore | TIER_2 | 2 | -- | _not analysed_ |
| AdCore | TIER_2 | 2 | -- | _not analysed_ |
| AdID | TIER_2 | 2 | -- | _not analysed_ |
| AdPlatformsCommon | TIER_2 | 2 | -- | _not analysed_ |
| AddressBookLegacy | TIER_2 | 2 | -- | _not analysed_ |
| Anvil | TIER_2 | 2 | -- | _not analysed_ |
| AppAttestInternal | TIER_2 | 2 | -- | _not analysed_ |
| AppDistributionLaunchAngel | TIER_2 | 2 | -- | _not analysed_ |
| AppRemoteAssets | TIER_2 | 2 | -- | _not analysed_ |
| AppSSODaemon | TIER_2 | 2 | -- | _not analysed_ |
| AppSSOKerberos | TIER_2 | 2 | -- | _not analysed_ |
| AppStoreComponents | TIER_2 | 2 | -- | _not analysed_ |
| AppStoreDaemon | TIER_2 | 2 | -- | _not analysed_ |
| AppleCIOFusionConfig | TIER_2 | 2 | -- | _not analysed_ |
| AppleDeviceQueryService | TIER_2 | 2 | -- | _not analysed_ |
| AppleFirmwareUpdate | TIER_2 | 2 | -- | _not analysed_ |
| AppleIDAMDriver | TIER_2 | 2 | -- | _not analysed_ |
| AppleIDSetup | TIER_2 | 2 | -- | _not analysed_ |
| AppleIDSetupDaemon | TIER_2 | 2 | -- | _not analysed_ |
| AppleIDSetupUI | TIER_2 | 2 | -- | _not analysed_ |
| AppleIntelligenceReporting | TIER_2 | 2 | -- | _not analysed_ |
| AppleIntelligenceReportingProcessing | TIER_2 | 2 | -- | _not analysed_ |
| AppleIntelligenceReportingProcessingService | TIER_2 | 2 | -- | _not analysed_ |
| AppleKeyStore | TIER_2 | 2 | -- | _not analysed_ |
| AppleLockdownMode | TIER_2 | 2 | -- | _not analysed_ |
| AppleMCTF | TIER_2 | 2 | -- | _not analysed_ |
| AppleMIDIUSBDriver | TIER_2 | 2 | -- | _not analysed_ |
| AppleMediaServices | TIER_2 | 2 | -- | _not analysed_ |
| AppleMediaServicesUI | TIER_2 | 2 | -- | _not analysed_ |
| AppleMediaServicesUIKitInternal | TIER_2 | 2 | -- | _not analysed_ |
| AppleServiceToolkit | TIER_2 | 2 | -- | _not analysed_ |
| AppleVideoEncoder | TIER_2 | 2 | -- | _not analysed_ |
| ArchiveService | TIER_2 | 2 | -- | _not analysed_ |
| AssetsLibrary | TIER_2 | 2 | -- | _not analysed_ |
| AssistantServices | TIER_2 | 2 | -- | _not analysed_ |
| AudioSession | TIER_2 | 2 | -- | _not analysed_ |
| AudioToolboxCore | TIER_2 | 2 | -- | _not analysed_ |
| AuthKitUI | TIER_2 | 2 | -- | _not analysed_ |
| AuthenticationServices | TIER_2 | 2 | -- | _not analysed_ |
| AuthenticationServicesAgent | TIER_2 | 2 | -- | _not analysed_ |
| AuthenticationServicesCore | TIER_2 | 2 | -- | _not analysed_ |
| AutoBugCaptureCore | TIER_2 | 2 | -- | _not analysed_ |
| BTLEServer | TIER_2 | 2 | -- | _not analysed_ |
| BackBoardServices | TIER_2 | 2 | -- | _not analysed_ |
| BackgroundShortcutRunner | TIER_2 | 2 | -- | _not analysed_ |
| BannerKit | TIER_2 | 2 | -- | _not analysed_ |
| BiomeFoundation | TIER_2 | 2 | -- | _not analysed_ |
| BiomeStorage | TIER_2 | 2 | -- | _not analysed_ |
| BlastDoor | TIER_2 | 2 | -- | _not analysed_ |
| BooksUI | TIER_2 | 2 | -- | _not analysed_ |
| CAFUI | TIER_2 | 2 | -- | _not analysed_ |
| CDMFoundation | TIER_2 | 2 | -- | _not analysed_ |
| CMCapture | TIER_2 | 2 | -- | _not analysed_ |
| CTLazuliSupport | TIER_2 | 2 | -- | _not analysed_ |
| CallsDialer | TIER_2 | 2 | -- | _not analysed_ |
| CarAccessoryFramework | TIER_2 | 2 | -- | _not analysed_ |
| CarKit | TIER_2 | 2 | -- | _not analysed_ |
| CarPlayAssetUI | TIER_2 | 2 | -- | _not analysed_ |
| CarPlayUIServices | TIER_2 | 2 | -- | _not analysed_ |
| CascadeSets | TIER_2 | 2 | -- | _not analysed_ |
| CentauriController | TIER_2 | 2 | -- | _not analysed_ |
| CheckerBoard | TIER_2 | 2 | -- | _not analysed_ |
| ChronoCore | TIER_2 | 2 | -- | _not analysed_ |
| ChronoKit | TIER_2 | 2 | -- | _not analysed_ |
| ChronoServices | TIER_2 | 2 | -- | _not analysed_ |
| CipherML | TIER_2 | 2 | -- | _not analysed_ |
| CloudKit | TIER_2 | 2 | -- | _not analysed_ |
| CloudPhotoLibrary | TIER_2 | 2 | -- | _not analysed_ |
| CloudServices | TIER_2 | 2 | -- | _not analysed_ |
| CommCenterMobileHelper | TIER_2 | 2 | -- | _not analysed_ |
| CommunicationsSetupUI | TIER_2 | 2 | -- | _not analysed_ |
| CompanionServices | TIER_2 | 2 | -- | _not analysed_ |
| CompanionSetup | TIER_2 | 2 | -- | _not analysed_ |
| CompanionSetupKit | TIER_2 | 2 | -- | _not analysed_ |
| ContainerManagerCommon | TIER_2 | 2 | -- | _not analysed_ |
| ContentKit | TIER_2 | 2 | -- | _not analysed_ |
| CoreAudioKit | TIER_2 | 2 | -- | _not analysed_ |
| CoreCDP | TIER_2 | 2 | -- | _not analysed_ |
| CoreCDPUI | TIER_2 | 2 | -- | _not analysed_ |
| CoreCaptureDaemon | TIER_2 | 2 | -- | _not analysed_ |
| CoreDAV | TIER_2 | 2 | -- | _not analysed_ |
| CoreEmbeddedSpeechRecognition | TIER_2 | 2 | -- | _not analysed_ |
| CoreFoundation | TIER_2 | 2 | -- | _not analysed_ |
| CoreHAP | TIER_2 | 2 | -- | _not analysed_ |
| CoreMediaStream | TIER_2 | 2 | -- | _not analysed_ |
| CoreNFC | TIER_2 | 2 | -- | _not analysed_ |
| CoreSceneUnderstanding | TIER_2 | 2 | -- | _not analysed_ |
| CoreSpeech | TIER_2 | 2 | -- | _not analysed_ |
| CoreSpeechFoundation | TIER_2 | 2 | -- | _not analysed_ |
| CoreSpotlight | TIER_2 | 2 | -- | _not analysed_ |
| CoreSymbolication | TIER_2 | 2 | -- | _not analysed_ |
| CoreTransparency | TIER_2 | 2 | -- | _not analysed_ |
| CoreUtils | TIER_2 | 2 | -- | _not analysed_ |
| CoreUtilsExtras | TIER_2 | 2 | -- | _not analysed_ |
| CryptexKit | TIER_2 | 2 | -- | _not analysed_ |
| CryptoKit | TIER_2 | 2 | -- | _not analysed_ |
| CryptoTokenKit | TIER_2 | 2 | -- | _not analysed_ |
| DADaemonCardDAV | TIER_2 | 2 | -- | _not analysed_ |
| DMCEnrollmentLibrary | TIER_2 | 2 | -- | _not analysed_ |
| DMCEnrollmentProvider | TIER_2 | 2 | -- | _not analysed_ |
| DMCUtilities | TIER_2 | 2 | -- | _not analysed_ |
| DashBoard | TIER_2 | 2 | -- | _not analysed_ |
| DeviceAccess | TIER_2 | 2 | -- | _not analysed_ |
| Diagnostics | TIER_2 | 2 | -- | _not analysed_ |
| DigitalSeparationUI | TIER_2 | 2 | -- | _not analysed_ |
| DiskImages2 | TIER_2 | 2 | -- | _not analysed_ |
| DistributedTimers | TIER_2 | 2 | -- | _not analysed_ |
| DistributedTimersDaemon | TIER_2 | 2 | -- | _not analysed_ |
| DocumentManager | TIER_2 | 2 | -- | _not analysed_ |
| Email | TIER_2 | 2 | -- | _not analysed_ |
| EmailCore | TIER_2 | 2 | -- | _not analysed_ |
| EmailDaemon | TIER_2 | 2 | -- | _not analysed_ |
| EnergyKitInternal | TIER_2 | 2 | -- | _not analysed_ |
| EscrowSecurityAlert | TIER_2 | 2 | -- | _not analysed_ |
| FTServices | TIER_2 | 2 | -- | _not analysed_ |
| FamilyCircle | TIER_2 | 2 | -- | _not analysed_ |
| FamilyCircleUI | TIER_2 | 2 | -- | _not analysed_ |
| FileProvider | TIER_2 | 2 | -- | _not analysed_ |
| FileProviderDaemon | TIER_2 | 2 | -- | _not analysed_ |
| FinanceDaemon | TIER_2 | 2 | -- | _not analysed_ |
| FinanceKit | TIER_2 | 2 | -- | _not analysed_ |
| FinanceKitUI | TIER_2 | 2 | -- | _not analysed_ |
| FocusSettingsUI | TIER_2 | 2 | -- | _not analysed_ |
| GAXBackboardServer | TIER_2 | 2 | -- | _not analysed_ |
| GAXClient | TIER_2 | 2 | -- | _not analysed_ |
| GPUToolsCapture | TIER_2 | 2 | -- | _not analysed_ |
| GPUToolsReplay | TIER_2 | 2 | -- | _not analysed_ |
| GameOverlayUI | TIER_2 | 2 | -- | _not analysed_ |
| GamePolicy | TIER_2 | 2 | -- | _not analysed_ |
| GameSave | TIER_2 | 2 | -- | _not analysed_ |
| GameServicesCore | TIER_2 | 2 | -- | _not analysed_ |
| GameStoreKit | TIER_2 | 2 | -- | _not analysed_ |
| GeoAnalytics | TIER_2 | 2 | -- | _not analysed_ |
| GeoServices | TIER_2 | 2 | -- | _not analysed_ |
| GeoServicesCore | TIER_2 | 2 | -- | _not analysed_ |
| H264H9.videoencoder | TIER_2 | 2 | -- | _not analysed_ |
| H9.videoencoder | TIER_2 | 2 | -- | _not analysed_ |
| HMFoundation | TIER_2 | 2 | -- | _not analysed_ |
| HangTracer | TIER_2 | 2 | -- | _not analysed_ |
| Health | TIER_2 | 2 | -- | _not analysed_ |
| HealthDaemon | TIER_2 | 2 | -- | _not analysed_ |
| HealthKit | TIER_2 | 2 | -- | _not analysed_ |
| HealthRecordsPlugin | TIER_2 | 2 | -- | _not analysed_ |
| HealthUI | TIER_2 | 2 | -- | _not analysed_ |
| HomeDeviceSetup | TIER_2 | 2 | -- | _not analysed_ |
| HomeEnergyDaemon | TIER_2 | 2 | -- | _not analysed_ |
| HomeKit | TIER_2 | 2 | -- | _not analysed_ |
| HomeKitDaemon | TIER_2 | 2 | -- | _not analysed_ |
| HomeKitDaemonLegacy | TIER_2 | 2 | -- | _not analysed_ |
| HomeKitEvents | TIER_2 | 2 | -- | _not analysed_ |
| IDS | TIER_2 | 2 | -- | _not analysed_ |
| IMDPersistence | TIER_2 | 2 | -- | _not analysed_ |
| IMDaemonCore | TIER_2 | 2 | -- | _not analysed_ |
| IMRCSTransfer | TIER_2 | 2 | -- | _not analysed_ |
| IMSharedUtilities | TIER_2 | 2 | -- | _not analysed_ |
| IMTransferAgent | TIER_2 | 2 | -- | _not analysed_ |
| IMTransferAgentClient | TIER_2 | 2 | -- | _not analysed_ |
| InCallService | TIER_2 | 2 | -- | _not analysed_ |
| InputAnalytics | TIER_2 | 2 | -- | _not analysed_ |
| InstalledContentLibrary | TIER_2 | 2 | -- | _not analysed_ |
| IntelligenceFlow | TIER_2 | 2 | -- | _not analysed_ |
| IntelligenceFlowContextRuntime | TIER_2 | 2 | -- | _not analysed_ |
| IntelligenceFlowPlannerSupport | TIER_2 | 2 | -- | _not analysed_ |
| IntelligencePlatformLibrary | TIER_2 | 2 | -- | _not analysed_ |
| Intents | TIER_2 | 2 | -- | _not analysed_ |
| JavaScriptCore | TIER_2 | 2 | -- | _not analysed_ |
| LinkPresentation | TIER_2 | 2 | -- | _not analysed_ |
| LinkServices | TIER_2 | 2 | -- | _not analysed_ |
| LocalAuthenticationCore | TIER_2 | 2 | -- | _not analysed_ |
| LocalAuthenticationUIService | TIER_2 | 2 | -- | _not analysed_ |
| LowPowerMode | TIER_2 | 2 | -- | _not analysed_ |
| MPSNDArray | TIER_2 | 2 | -- | _not analysed_ |
| MTLCompilerService | TIER_2 | 2 | -- | _not analysed_ |
| ManagedSettings | TIER_2 | 2 | -- | _not analysed_ |
| ManagedSettingsAgent | TIER_2 | 2 | -- | _not analysed_ |
| MapKit | TIER_2 | 2 | -- | _not analysed_ |
| MapsDesign | TIER_2 | 2 | -- | _not analysed_ |
| MapsSuggestions | TIER_2 | 2 | -- | _not analysed_ |
| MapsSupport | TIER_2 | 2 | -- | _not analysed_ |
| MapsUI | TIER_2 | 2 | -- | _not analysed_ |
| MediaAnalysis | TIER_2 | 2 | -- | _not analysed_ |
| MediaPlaybackCore | TIER_2 | 2 | -- | _not analysed_ |
| MediaSetup | TIER_2 | 2 | -- | _not analysed_ |
| MessageProtection | TIER_2 | 2 | -- | _not analysed_ |
| MessageSecurity | TIER_2 | 2 | -- | _not analysed_ |
| MessagesBlastDoorService | TIER_2 | 2 | -- | _not analysed_ |
| MetadataUtilities | TIER_2 | 2 | -- | _not analysed_ |
| MetalTools | TIER_2 | 2 | -- | _not analysed_ |
| MetricMeasurement | TIER_2 | 2 | -- | _not analysed_ |
| MobileAssetDaemon | TIER_2 | 2 | -- | _not analysed_ |
| MobileInstallation | TIER_2 | 2 | -- | _not analysed_ |
| MobilePhone | TIER_2 | 2 | -- | _not analysed_ |
| MobileSafari | TIER_2 | 2 | -- | _not analysed_ |
| MobileSafariUI | TIER_2 | 2 | -- | _not analysed_ |
| ModelManagerServices | TIER_2 | 2 | -- | _not analysed_ |
| MomentsUIService | TIER_2 | 2 | -- | _not analysed_ |
| MusicKit | TIER_2 | 2 | -- | _not analysed_ |
| MusicLibrary | TIER_2 | 2 | -- | _not analysed_ |
| NFCUISceneService | TIER_2 | 2 | -- | _not analysed_ |
| NanoTimeKit | TIER_2 | 2 | -- | _not analysed_ |
| NearField | TIER_2 | 2 | -- | _not analysed_ |
| NearFieldPrivateServices | TIER_2 | 2 | -- | _not analysed_ |
| Network | TIER_2 | 2 | -- | _not analysed_ |
| NetworkExtension | TIER_2 | 2 | -- | _not analysed_ |
| NetworkInfo | TIER_2 | 2 | -- | _not analysed_ |
| NexusDaemon | TIER_2 | 2 | -- | _not analysed_ |
| NotesShared | TIER_2 | 2 | -- | _not analysed_ |
| OSAnalytics | TIER_2 | 2 | -- | _not analysed_ |
| OmniSearch | TIER_2 | 2 | -- | _not analysed_ |
| OmniSearchClient | TIER_2 | 2 | -- | _not analysed_ |
| PDFKit | TIER_2 | 2 | -- | _not analysed_ |
| PacketFilter | TIER_2 | 2 | -- | _not analysed_ |
| PacketFilter-embedded | TIER_2 | 2 | -- | _not analysed_ |
| ParavirtualizedANE | TIER_2 | 2 | -- | _not analysed_ |
| PassKitCore | TIER_2 | 2 | -- | _not analysed_ |
| PassKitUI | TIER_2 | 2 | -- | _not analysed_ |
| PasscodeAndBiometricsSettings | TIER_2 | 2 | -- | _not analysed_ |
| PasscodeSettingsSubscriber | TIER_2 | 2 | -- | _not analysed_ |
| PasswordManagerUI | TIER_2 | 2 | -- | _not analysed_ |
| PaymentUIBase | TIER_2 | 2 | -- | _not analysed_ |
| PerfPowerServicesSignpostService | TIER_2 | 2 | -- | _not analysed_ |
| PhotoLibraryServices | TIER_2 | 2 | -- | _not analysed_ |
| PhotoLibraryServicesCore | TIER_2 | 2 | -- | _not analysed_ |
| Photos | TIER_2 | 2 | -- | _not analysed_ |
| PhotosGraph | TIER_2 | 2 | -- | _not analysed_ |
| PhotosIntelligence | TIER_2 | 2 | -- | _not analysed_ |
| PhotosUICore | TIER_2 | 2 | -- | _not analysed_ |
| PhotosUIFoundation | TIER_2 | 2 | -- | _not analysed_ |
| PhotosUIPrivate | TIER_2 | 2 | -- | _not analysed_ |
| PlatformSSO | TIER_2 | 2 | -- | _not analysed_ |
| PlatformSSOCore | TIER_2 | 2 | -- | _not analysed_ |
| PowerLog | TIER_2 | 2 | -- | _not analysed_ |
| PowerlogCore | TIER_2 | 2 | -- | _not analysed_ |
| PriMLETL | TIER_2 | 2 | -- | _not analysed_ |
| PrivateMLClient | TIER_2 | 2 | -- | _not analysed_ |
| ProductKitCore | TIER_2 | 2 | -- | _not analysed_ |
| PromotedContent | TIER_2 | 2 | -- | _not analysed_ |
| PromotedContentUI | TIER_2 | 2 | -- | _not analysed_ |
| ProtectedCloudStorage | TIER_2 | 2 | -- | _not analysed_ |
| QuartzCore | TIER_2 | 2 | -- | _not analysed_ |
| RCS | TIER_2 | 2 | -- | _not analysed_ |
| Rapport | TIER_2 | 2 | -- | _not analysed_ |
| Reminders | TIER_2 | 2 | -- | _not analysed_ |
| RemoteConfiguration | TIER_2 | 2 | -- | _not analysed_ |
| RemoteUI | TIER_2 | 2 | -- | _not analysed_ |
| SESShared | TIER_2 | 2 | -- | _not analysed_ |
| SEService | TIER_2 | 2 | -- | _not analysed_ |
| SMS | TIER_2 | 2 | -- | _not analysed_ |
| SafariBookmarksSyncAgent | TIER_2 | 2 | -- | _not analysed_ |
| SafariCore | TIER_2 | 2 | -- | _not analysed_ |
| SafariServices | TIER_2 | 2 | -- | _not analysed_ |
| SafariShared | TIER_2 | 2 | -- | _not analysed_ |
| SafariSharedUI | TIER_2 | 2 | -- | _not analysed_ |
| SatelliteSMS | TIER_2 | 2 | -- | _not analysed_ |
| ScreenTimeAgent | TIER_2 | 2 | -- | _not analysed_ |
| ScreenTimeCore | TIER_2 | 2 | -- | _not analysed_ |
| SecureElementCredential | TIER_2 | 2 | -- | _not analysed_ |
| SecureMessaging | TIER_2 | 2 | -- | _not analysed_ |
| SecureMessagingAgent | TIER_2 | 2 | -- | _not analysed_ |
| SecureMessagingAgentCore | TIER_2 | 2 | -- | _not analysed_ |
| Seeding | TIER_2 | 2 | -- | _not analysed_ |
| SessionCore | TIER_2 | 2 | -- | _not analysed_ |
| SharedWebCredentials | TIER_2 | 2 | -- | _not analysed_ |
| Sharing | TIER_2 | 2 | -- | _not analysed_ |
| ShazamKit | TIER_2 | 2 | -- | _not analysed_ |
| ShimGameServices | TIER_2 | 2 | -- | _not analysed_ |
| SiriLinkFlowPlugin | TIER_2 | 2 | -- | _not analysed_ |
| SoftwareUpdateCore | TIER_2 | 2 | -- | _not analysed_ |
| SoftwareUpdateServices | TIER_2 | 2 | -- | _not analysed_ |
| SoftwareUpdateServicesUI | TIER_2 | 2 | -- | _not analysed_ |
| SoftwareUpdateSettingsUI | TIER_2 | 2 | -- | _not analysed_ |
| SpeakerRecognition | TIER_2 | 2 | -- | _not analysed_ |
| Speech | TIER_2 | 2 | -- | _not analysed_ |
| SpotlightIndex | TIER_2 | 2 | -- | _not analysed_ |
| SpotlightKnowledgeDaemon | TIER_2 | 2 | -- | _not analysed_ |
| SpotlightResources | TIER_2 | 2 | -- | _not analysed_ |
| SpotlightServices | TIER_2 | 2 | -- | _not analysed_ |
| SpringBoard | TIER_2 | 2 | -- | _not analysed_ |
| SpringBoardUIServices | TIER_2 | 2 | -- | _not analysed_ |
| StatusKit | TIER_2 | 2 | -- | _not analysed_ |
| StatusKitAgent | TIER_2 | 2 | -- | _not analysed_ |
| StatusKitAgentCore | TIER_2 | 2 | -- | _not analysed_ |
| StocksPersonalization | TIER_2 | 2 | -- | _not analysed_ |
| StoreKit | TIER_2 | 2 | -- | _not analysed_ |
| SwiftMLS | TIER_2 | 2 | -- | _not analysed_ |
| SwiftUI | TIER_2 | 2 | -- | _not analysed_ |
| Symbolication | TIER_2 | 2 | -- | _not analysed_ |
| T8150_CoreAAClientKit_asan | TIER_2 | 2 | -- | _not analysed_ |
| T8150_ExclaveISPSharedLib_exclavekit_asan | TIER_2 | 2 | -- | _not analysed_ |
| T8150_IR_ISP_EK_Component_asan | TIER_2 | 2 | -- | _not analysed_ |
| T8150_RGB_ISP_EK_Component_asan | TIER_2 | 2 | -- | _not analysed_ |
| TSUtility | TIER_2 | 2 | -- | _not analysed_ |
| TVRemoteCore | TIER_2 | 2 | -- | _not analysed_ |
| TVRemoteUI | TIER_2 | 2 | -- | _not analysed_ |
| TelephonyBlastDoorSupport | TIER_2 | 2 | -- | _not analysed_ |
| TelephonyKit | TIER_2 | 2 | -- | _not analysed_ |
| TelephonyMessagingKit | TIER_2 | 2 | -- | _not analysed_ |
| TextInput | TIER_2 | 2 | -- | _not analysed_ |
| TextInputUI | TIER_2 | 2 | -- | _not analysed_ |
| Tips | TIER_2 | 2 | -- | _not analysed_ |
| TokenGenerationInference | TIER_2 | 2 | -- | _not analysed_ |
| TranslationDaemon | TIER_2 | 2 | -- | _not analysed_ |
| Transparency | TIER_2 | 2 | -- | _not analysed_ |
| TrustKit | TIER_2 | 2 | -- | _not analysed_ |
| TrustedPeers | TIER_2 | 2 | -- | _not analysed_ |
| TrustedPeersHelper | TIER_2 | 2 | -- | _not analysed_ |
| UARPUpdaterServiceHID | TIER_2 | 2 | -- | _not analysed_ |
| UIKitServices | TIER_2 | 2 | -- | _not analysed_ |
| UnifiedAssetFramework | TIER_2 | 2 | -- | _not analysed_ |
| UnifiedMessagingKit | TIER_2 | 2 | -- | _not analysed_ |
| UserNotificationsCore | TIER_2 | 2 | -- | _not analysed_ |
| VectorKit | TIER_2 | 2 | -- | _not analysed_ |
| VideosUI | TIER_2 | 2 | -- | _not analysed_ |
| VoiceServices | TIER_2 | 2 | -- | _not analysed_ |
| VoiceShortcutClient | TIER_2 | 2 | -- | _not analysed_ |
| VoiceShortcuts | TIER_2 | 2 | -- | _not analysed_ |
| VoiceTrigger | TIER_2 | 2 | -- | _not analysed_ |
| WeatherKit | TIER_2 | 2 | -- | _not analysed_ |
| WebContentRestrictions | TIER_2 | 2 | -- | _not analysed_ |
| WebCore | TIER_2 | 2 | -- | _not analysed_ |
| WebGPU | TIER_2 | 2 | -- | _not analysed_ |
| WebKitLegacy | TIER_2 | 2 | -- | _not analysed_ |
| WebUI | TIER_2 | 2 | -- | _not analysed_ |
| WorkflowKit | TIER_2 | 2 | -- | _not analysed_ |
| WorkflowResponsiveness | TIER_2 | 2 | -- | _not analysed_ |
| YamahaUSBMIDIDriver | TIER_2 | 2 | -- | _not analysed_ |
| _GroupActivities_UIKit | TIER_2 | 2 | -- | _not analysed_ |
| _StoreKit_SwiftUI | TIER_2 | 2 | -- | _not analysed_ |
| akd | TIER_2 | 2 | -- | _not analysed_ |
| amsaccountsd | TIER_2 | 2 | -- | _not analysed_ |
| amsengagementd | TIER_2 | 2 | -- | _not analysed_ |
| aned | TIER_2 | 2 | -- | _not analysed_ |
| apfs_boot_util | TIER_2 | 2 | -- | _not analysed_ |
| appleaccountd | TIER_2 | 2 | -- | _not analysed_ |
| applekeystored | TIER_2 | 2 | -- | _not analysed_ |
| appstored | TIER_2 | 2 | -- | _not analysed_ |
| askpermissiond | TIER_2 | 2 | -- | _not analysed_ |
| attributionkitd | TIER_2 | 2 | -- | _not analysed_ |
| audioaccessoryd | TIER_2 | 2 | -- | _not analysed_ |
| backgroundassets.user | TIER_2 | 2 | -- | _not analysed_ |
| bluetoothd | TIER_2 | 2 | -- | _not analysed_ |
| callservicesd | TIER_2 | 2 | -- | _not analysed_ |
| caraccessoryd | TIER_2 | 2 | -- | _not analysed_ |
| carkitd | TIER_2 | 2 | -- | _not analysed_ |
| caulk | TIER_2 | 2 | -- | _not analysed_ |
| com.apple.MobileAsset.DownloadService.Builtin | TIER_2 | 2 | -- | _not analysed_ |
| com.apple.MobileInstallationHelperService | TIER_2 | 2 | -- | _not analysed_ |
| com.apple.driver.AppleH16ANEInterface | TIER_2 | 2 | -- | _not analysed_ |
| com.apple.driver.ApplePearlSEPDriver | TIER_2 | 2 | -- | _not analysed_ |
| com.apple.driver.AppleSEPKeyStore | TIER_2 | 2 | -- | _not analysed_ |
| com.apple.driver.AppleT8150MCC | TIER_2 | 2 | -- | _not analysed_ |
| com.apple.filesystems.hfs.kext | TIER_2 | 2 | -- | _not analysed_ |
| com.apple.iokit.IOGPUFamily | TIER_2 | 2 | -- | _not analysed_ |
| com.apple.iokit.IOTimeSyncFamily | TIER_2 | 2 | -- | _not analysed_ |
| com.apple.sbd | TIER_2 | 2 | -- | _not analysed_ |
| contactsd | TIER_2 | 2 | -- | _not analysed_ |
| coreidvd | TIER_2 | 2 | -- | _not analysed_ |
| coresymbolicationd | TIER_2 | 2 | -- | _not analysed_ |
| cryptexd | TIER_2 | 2 | -- | _not analysed_ |
| dasd | TIER_2 | 2 | -- | _not analysed_ |
| deleted | TIER_2 | 2 | -- | _not analysed_ |
| deviceaccessd | TIER_2 | 2 | -- | _not analysed_ |
| diskimagescontroller | TIER_2 | 2 | -- | _not analysed_ |
| diskimagesiod | TIER_2 | 2 | -- | _not analysed_ |
| dyld | TIER_2 | 2 | -- | _not analysed_ |
| eligibilityd | TIER_2 | 2 | -- | _not analysed_ |
| familycircled | TIER_2 | 2 | -- | _not analysed_ |
| frauddefensed | TIER_2 | 2 | -- | _not analysed_ |
| fskitd | TIER_2 | 2 | -- | _not analysed_ |
| gamed | TIER_2 | 2 | -- | _not analysed_ |
| gamepolicyd | TIER_2 | 2 | -- | _not analysed_ |
| gpsd | TIER_2 | 2 | -- | _not analysed_ |
| homeenergyd | TIER_2 | 2 | -- | _not analysed_ |
| iCloudQuotaUI | TIER_2 | 2 | -- | _not analysed_ |
| iCloudSettings | TIER_2 | 2 | -- | _not analysed_ |
| iMessage | TIER_2 | 2 | -- | _not analysed_ |
| iMessageLite | TIER_2 | 2 | -- | _not analysed_ |
| iTunesCloud | TIER_2 | 2 | -- | _not analysed_ |
| iTunesStoreUI | TIER_2 | 2 | -- | _not analysed_ |
| icloudwebd | TIER_2 | 2 | -- | _not analysed_ |
| identityservicesd | TIER_2 | 2 | -- | _not analysed_ |
| imagent | TIER_2 | 2 | -- | _not analysed_ |
| installd | TIER_2 | 2 | -- | _not analysed_ |
| jetpackassetd | TIER_2 | 2 | -- | _not analysed_ |
| keybagd | TIER_2 | 2 | -- | _not analysed_ |
| launchd | TIER_2 | 2 | -- | _not analysed_ |
| libANGLE-shared.dylib | TIER_2 | 2 | -- | _not analysed_ |
| libAudioDSP.dylib | TIER_2 | 2 | -- | _not analysed_ |
| libBKDM2.dylib | TIER_2 | 2 | -- | _not analysed_ |
| libIPTelephony.dylib | TIER_2 | 2 | -- | _not analysed_ |
| libMobileGestalt.dylib | TIER_2 | 2 | -- | _not analysed_ |
| libSecureMAHelper.dylib | TIER_2 | 2 | -- | _not analysed_ |
| libSparse.dylib | TIER_2 | 2 | -- | _not analysed_ |
| libT200Updater.dylib | TIER_2 | 2 | -- | _not analysed_ |
| libauthinstall.dylib | TIER_2 | 2 | -- | _not analysed_ |
| libaxis.dylib | TIER_2 | 2 | -- | _not analysed_ |
| libboringssl.dylib | TIER_2 | 2 | -- | _not analysed_ |
| libcryptex.dylib | TIER_2 | 2 | -- | _not analysed_ |
| libcryptex_interface.dylib | TIER_2 | 2 | -- | _not analysed_ |
| libcryptex_trampoline.dylib | TIER_2 | 2 | -- | _not analysed_ |
| libdyld.dylib | TIER_2 | 2 | -- | _not analysed_ |
| libimage4.dylib | TIER_2 | 2 | -- | _not analysed_ |
| libnfshared.dylib | TIER_2 | 2 | -- | _not analysed_ |
| libswiftPrespecialized.dylib | TIER_2 | 2 | -- | _not analysed_ |
| libswiftXPC.dylib | TIER_2 | 2 | -- | _not analysed_ |
| libsystem_c_debug.dylib | TIER_2 | 2 | -- | _not analysed_ |
| libsystem_containermanager.dylib | TIER_2 | 2 | -- | _not analysed_ |
| libsystem_networkextension.dylib | TIER_2 | 2 | -- | _not analysed_ |
| libsystem_sandbox.dylib | TIER_2 | 2 | -- | _not analysed_ |
| libsystem_trace.dylib | TIER_2 | 2 | -- | _not analysed_ |
| libxpc.dylib | TIER_2 | 2 | -- | _not analysed_ |
| lifs | TIER_2 | 2 | -- | _not analysed_ |
| linkd | TIER_2 | 2 | -- | _not analysed_ |
| livefiles_hfs.dylib | TIER_2 | 2 | -- | _not analysed_ |
| locationd | TIER_2 | 2 | -- | _not analysed_ |
| logd | TIER_2 | 2 | -- | _not analysed_ |
| managedappdistributiond | TIER_2 | 2 | -- | _not analysed_ |
| mediaremoted | TIER_2 | 2 | -- | _not analysed_ |
| migrationd | TIER_2 | 2 | -- | _not analysed_ |
| mmaintenanced | TIER_2 | 2 | -- | _not analysed_ |
| mobile_obliterator | TIER_2 | 2 | -- | _not analysed_ |
| mobileactivationd | TIER_2 | 2 | -- | _not analysed_ |
| nehelper | TIER_2 | 2 | -- | _not analysed_ |
| nesessionmanager | TIER_2 | 2 | -- | _not analysed_ |
| networkserviceproxy | TIER_2 | 2 | -- | _not analysed_ |
| nfcd | TIER_2 | 2 | -- | _not analysed_ |
| otctl | TIER_2 | 2 | -- | _not analysed_ |
| passd | TIER_2 | 2 | -- | _not analysed_ |
| pppd | TIER_2 | 2 | -- | _not analysed_ |
| profiled | TIER_2 | 2 | -- | _not analysed_ |
| promotedcontentd | TIER_2 | 2 | -- | _not analysed_ |
| proximitycontrold | TIER_2 | 2 | -- | _not analysed_ |
| rapportd | TIER_2 | 2 | -- | _not analysed_ |
| remoted | TIER_2 | 2 | -- | _not analysed_ |
| replayd | TIER_2 | 2 | -- | _not analysed_ |
| revisiond | TIER_2 | 2 | -- | _not analysed_ |
| searchd | TIER_2 | 2 | -- | _not analysed_ |
| seld | TIER_2 | 2 | -- | _not analysed_ |
| seserviced | TIER_2 | 2 | -- | _not analysed_ |
| sharingd | TIER_2 | 2 | -- | _not analysed_ |
| shazamd | TIER_2 | 2 | -- | _not analysed_ |
| sportsd | TIER_2 | 2 | -- | _not analysed_ |
| sptm.t8150.release.im4p | TIER_2 | 2 | -- | _not analysed_ |
| storekitd | TIER_2 | 2 | -- | _not analysed_ |
| swtransparencyd | TIER_2 | 2 | -- | _not analysed_ |
| tailspind | TIER_2 | 2 | -- | _not analysed_ |
| transparencyd | TIER_2 | 2 | -- | _not analysed_ |
| tvremoted | TIER_2 | 2 | -- | _not analysed_ |
| txm.iphoneos.release.im4p | TIER_2 | 2 | -- | _not analysed_ |
| uarpassetmanagerd | TIER_2 | 2 | -- | _not analysed_ |
| usermanagerd | TIER_2 | 2 | -- | _not analysed_ |
| vot | TIER_2 | 2 | -- | _not analysed_ |
| wifip2pd | TIER_2 | 2 | -- | _not analysed_ |
| wirelessinsightsd | TIER_2 | 2 | -- | _not analysed_ |
| xpcproxy | TIER_2 | 2 | -- | _not analysed_ |

</details>

## HIGH_SIGNAL -- excluded, low/no security relevance (1256)

<details><summary>Show 1256 components</summary>

- AACDependencies
- ACCBaker
- ACCHWComponentAuthService
- ACTFramework
- AGXCompilerCore
- AGXMetalG18P
- AIMLInstrumentationStreams
- APConfigurationSystem
- APTransport
- ARKit
- ARTraceModule
- ASEProcessing
- ASIOKit
- ASMessagesProvider
- ASPCarryLog
- ASRBridge
- AVD.videodecoder
- AVFCapture
- AVFCore
- AVFoundation
- AXAVSPluginService
- AXActionSheetUIServer
- AXAssetLoader
- AXElementInteraction
- AXGuestPassServer
- AXGuestPassServices
- AXIDSServices
- AXMediaUtilities
- AXMotionCuesServer
- AXNTKUtilities
- AXRuntime
- AXSoundDetectionUI
- AXSpeechAssetServices
- AXSpringBoardServerInstance
- AXTapToSpeakTime
- Accessory Updater Service
- AccessoryComponentAuth
- AccessoryDeveloperSettings
- AccessoryNotificationsSourceSelection
- AccessorySetupDeveloperSettings
- AccessorySetupKitCore
- AcousticId-Assistant
- ActionButtonConfigurationUI
- ActionButtonSelector
- ActionKitUI
- ActiveSyncSettings
- ActivityAchievements
- ActivityAchievementsDaemon
- ActivityAchievementsUI
- ActivityAwardsClient
- ActivityAwardsServices
- ActivitySettings
- ActivitySharing
- ActivitySharingUI
- ActivityUIServices
- AdaptiveMusic
- AdaptiveVoiceShortcuts
- AddressBook
- AddressBook-Assistant
- AddressBookUIFramework
- AfibBurden
- AirDrop
- AirDropUI
- AirPlayKit
- AirPlayMirroringModule
- AirPlayOverlaysServer
- AirPlayReceiver
- AirPlayReceiverKit
- AirPlaySender
- AirPlaySupport
- AirPortSettings
- AirTrafficSettings
- AmbientUI
- Animoji
- AnnotationKit
- AppAnalytics
- AppDistribution
- AppDistributionUI
- AppInstallExtension
- AppInstallation
- AppInstallationSettings
- AppIntents
- AppMigrationKit
- AppPredictionClient
- AppPredictionInternal
- AppPredictionUI
- AppPredictionUIWidget
- AppState
- AppStoreKit
- AppSystemSettingsUI
- AppearanceModule
- AppleAVE2FW_H18.im4p
- AppleBasebandManager
- AppleBasebandServices
- AppleConvergedFirmwareUpdater
- AppleDeviceQuerySupport
- AppleIDSetupUIService
- AppleMIDINetworkDriver
- AppleMediaServicesKitInternal
- AppleMediaServicesUIDynamic
- AppleMediaServicesUIPaymentSheets
- AppleProxServiceFilter
- AppleTV
- Arcade
- AskToDaemon
- AskToUI
- AssetExplorer
- AssetViewer
- AssistantUI
- AttributionWeeApp
- Audio-QuickLook
- AudioAccessoryKit
- AudioAccessoryServices
- AudioAnalyticsBase
- AudioAnalyticsExternal
- AudioCodecs
- AudioConferenceControlCenterModule
- AudioDSPManager
- AudioServerDriver
- AudioToolbox
- AudiogramIngestion
- AvatarKit
- AvatarPickerMemojiPicker
- AvatarUI
- BPSStingSetup
- BTAudioHALPlugin
- BackBoard
- BackBoardHIDEventFoundation
- BackgroundSecurityImprovement
- BacklightServicesHost
- BackupAgent2
- BarcodeScanner
- BaseBoardUI
- BatteryCenterUI
- BatteryUsageUI
- BatteryWidget
- BiomeLibrary
- BiomeStreams
- BiometricKitUI
- BiometricSupport
- Blackbeard
- BlissReader
- BluetoothFirmware
- BluetoothSettings
- BookStoreUI
- Bridge
- BridgePreferences
- BridgeStoreExtension
- BulletinDistributorCompanion
- Business
- BusinessChatFramework
- BusinessChatService
- BusinessServicesUI
- CAFCombine
- CARDNDUI
- CFNetwork
- CMCaptureCore
- CMFSyncAgent
- Calculate
- Calculator
- Calendar-Assistant
- CalendarDatabase
- CallHistorySyncHelper
- CallIntelligence
- CallsAppServices
- CallsAppUI
- CallsSearch
- Camera
- CameraEditKitFramework
- CameraEffectsKit
- CameraKit
- CameraOverlayAngel
- CameraUI
- CaptiveNetworkSupport
- CarAssetUtils
- CarKey
- CarKitNavigation
- CarKitSettings
- CarModeModule
- CarPlay
- CarPlayDisplayUtils
- CarPlayServices
- CarPlaySettings
- CarPlaySetup
- CarPlaySupport
- CarPlayTemplateUIHost
- CarPlayUI
- CarPlayWallpaper
- CardKit
- CarouselAppViewSettings
- CarouselLayoutSettings
- CascadeEngine
- CellularBridgeUI
- CertInfo
- Charge
- ChargingViewService
- ChatKitAssistantUI-Assistant
- ChatKitFramework
- ChronoUIServices
- Cinematic
- ClassKitNotificationUI
- Climate
- ClipServices
- ClipUIServices
- ClockKit
- ClockPoster
- CloudDocs
- CloudMediaServicesInterfaceKit
- Coherence
- CommunicationDetails
- CommunicationsUI
- CommunicationsUICore
- CompanionAppViewSetup
- CompanionHealthDaemon
- CompanionNotificationSettings
- CompanionStingSettings
- CompanionSync
- Compass
- CompassViewCalibrationService
- ComplicationDisplay
- ComputationalGraph
- ConferenceRegistrationSettings
- ConnectivityModule
- ContextSync
- ContextualSuggestionClient
- ContinuityCapture
- ContinuityDisplay
- ContinuousExposeModule
- ControlCenterUI
- ControlCenterUIKit
- ConversationKit
- CookingKit
- CookingSupport
- CoreAuthUI
- CoreBluetooth
- CoreDuet
- CoreDynamicUIPlugin
- CoreEmoji
- CoreFollowUp
- CoreGEM.dylib
- CoreGPSTest.dylib
- CoreGraphics
- CoreIDVRGBLiveness
- CoreIDVUI
- CoreIndoor
- CoreLocation
- CoreLocationProtobuf
- CoreMotion
- CoreMotionAlgorithms
- CoreNavigation
- CoreParsec
- CorePhotogrammetry
- CorePrescription
- CoreRealityIO
- CoreRecognition
- CoreRepairCore
- CoreRoutineHelperService
- CoreServicesInternal
- CoreSuggestionsInternals
- CoreSuggestionsUI
- CoreTelephony
- CoreUARP
- CoreUI
- CoreUtilsShims
- CoreUtilsSwift
- CoreVideo
- CoverSheet
- CoverSheetKit
- DACardDAV
- DADaemonSupport
- DDActionsService
- DMCTools
- DaemonUtils
- DataDeliveryServices
- DataDetectorsCore
- DeepVideoProcessingCore
- DefaultMediaPlayer-QuickLook
- DefaultMessagingAppsSettings
- DesktopServicesPriv
- DeviceCheckInternal
- DeviceDiscoveryUI
- DeviceDiscoveryUICore
- DeviceManagementTools
- DiagnosticsKit
- DiagnosticsSessionAvailabilityService
- DialogEngine
- DictionarySettings
- DictionaryUI
- DigitalAccess
- DigitalSeparation
- DigitalSeparationSettings
- DigitalTouchBalloonProvider
- DigitalTouchShared
- DisplayAndBrightnessSettings
- DisplayModule
- DoNotDisturb
- DoNotDisturbKit
- DoNotDisturbModule
- DoNotDisturbServer
- DoNotDisturbSettings
- DockFolderViewService
- DocumentCamera
- DocumentManagerExecutables
- DocumentManagerUICore
- DrawingKit
- DuetActivityScheduler
- Dyld
- DynamicPrefetching
- EAUpdaterService
- EmbeddedAcousticRecognition
- EmojiKit
- EventKit
- EventKitUIFramework
- ExposureNotificationSettingsUI
- ExtensionFoundation
- FMFCore
- FMFindingUI
- FMIPCore
- FTMInternal
- FaceTime
- FaceTimeMessageStore
- FacebookSettings
- Family
- FamilyControlsAgent
- FamilyExtensionHost
- FedStatsPluginCore
- FeedbackLogger
- Files
- FilesystemMetadataSnapshotService
- FinanceUIService
- FindMy
- FindMyDevice
- FindMyLocate
- Fitness
- FitnessCoachingCore
- FitnessCoachingHealthServices
- FitnessCoachingServices
- FitnessIntelligence
- FitnessIntelligencePlugin
- FitnessMachineServices
- FitnessSettings
- FitnessUI
- FlashlightModule
- FlightUtilities
- FocusUI
- FocusUIModule
- FontPicker
- FontServices
- FontSettings
- FoundationModels
- Freeform
- FreeformDataclassOwner
- FullKeyboardAccess
- GAXSpringboardServer
- GCoreFramework
- GPUToolsReplayService
- GPUToolsTransport
- GameController
- GameControllerFoundation
- GameKitFramework
- GameServices
- Games
- GeneralKnowledge-Assistant
- GeneralSettingsUI
- GenerationalStorage
- GenerativeModels
- Gif-QuickLook
- GuidedAccess
- H16ISP.mediacapture
- H264SW.videocodec
- HAENotifications
- HDSViewService
- HSTouchHIDService
- HandwritingProvider
- HangHUD
- Haptics
- HashtagImagesExtension
- HeadphoneCommonUIKit
- HeadphoneConfigs
- HeadphoneManager
- HeadphoneProxService
- HeadphoneSettings
- HeadphoneSettingsUI
- HealthActivityCache
- HealthAppHealthDaemon
- HealthArticles
- HealthArticlesGeneration
- HealthArticlesUI
- HealthBalanceAppPluginBundle
- HealthBluetoothPeripheral
- HealthCategories
- HealthDaemonFeatures
- HealthDaemonFoundation
- HealthDiagnosticExtensionCore
- HealthExperienceUI
- HealthExposureNotificationUI
- HealthFeaturesBridgeSetupPlugin
- HealthHearingDaemon
- HealthIntents
- HealthKitUI
- HealthMedications
- HealthMedicationsDaemonPlugin
- HealthMedicationsExperience
- HealthMedicationsUI
- HealthMedicationsVision
- HealthMedicationsVisionUI
- HealthMenstrualCycles
- HealthMenstrualCyclesDaemon
- HealthMobility
- HealthMobilityDaemon
- HealthMobilityUI
- HealthOntologyDaemon
- HealthPlatform
- HealthPlatformCatalogUI
- HealthRecordServices
- HealthRecords
- HealthRecordsExtraction
- HealthRecordsUI
- HealthSafety
- HealthSettings
- HealthSettingsUI
- HealthToolbox
- HealthVisualization
- HearingAidUIServer
- HearingAppPlugin
- HearingModeService
- HearingModeService_Private
- HearingModeSettingsUI
- HearingModeUI
- HearingTestUI
- HearingUI
- HearingUtilities
- Heart
- HeartHealth
- HeartHealthDaemon
- HeartRhythmUI
- HelpKit
- HighlightAlerts
- Highlights
- Home
- HomeAI
- HomeAccessoryControlUI
- HomeControlCenterCompactModule
- HomeControlCenterModule
- HomeControlService
- HomeDataModel
- HomeKitDaemonShared
- HomeKitMatter
- HomeKitMetrics
- HomePodSettings
- HomeUI
- HomeUIService
- HoverTextUI
- HubbleBlastDoorService
- IDSFoundation
- IMAssistantCore
- IMCorePipeline
- IMDMessageServicesAgent
- IMTranscoderAgent
- IO80211
- IconRendering
- Image-QuickLook
- ImagePlaygroundInternal
- InAppFeedback
- InCallLockScreen
- IncomingCall
- InformationFlowPlugin
- InputUI
- IntelligenceFlowContext
- IntelligenceFlowFeedbackDataCollector
- IntelligenceFlowPlannerRuntime
- IntelligenceFlowRuntime
- IntelligenceFlowShared
- IntelligencePlatform
- IntelligencePlatformCore
- IntelligenceTasksEngine
- IntelligentCallScreeningSettingsBundle
- IntelligentRoutingDaemon
- IntelligentRoutingDaemonLLMService
- IntentRecommend
- IntentsCore
- IntentsUI
- InternationalSettings
- Journal
- JournalSettings
- KeyboardSettings
- Lexicon
- LiveTranscription
- LiveTranscriptionUI
- LocalAuthentication
- LocalAuthenticationCoreUI
- LocalAuthenticationPrivateUI
- LocalAuthenticationRGBCapture
- LocalAuthenticationUI
- LocalSpeechRecognitionBridge
- LoginUI
- MDM
- MDMClientLibrary
- MFAAuthentication
- MTLAssetUpgraderD
- MTLReplayer
- MagnifierSupport
- Mail-Assistant
- MailAttachmentPlugin
- MailSupport
- MailUI
- MailVIPWidget
- ManagedAppsSubscriber
- ManagedDevice
- MapKitFramework
- MapKitSwiftUI
- Maps-Assistant
- MapsSettings
- MapsSync
- MarketplaceKit
- MarkupUI
- Matter
- MatterPlugin
- MechanismBase
- Media
- MediaAnalysisBlastDoorService
- MediaAnalysisServices
- MediaControls
- MediaCoreUI
- MediaExperience
- MediaPlayer
- MediaPlayerFramework
- MediaPlayerUIFramework
- MediaServices
- MediaSuggester
- MediaToolbox
- MedicalIDUI
- MedicationsHealthAppPlugin
- MedicationsHealthAppPluginBundle
- Memories
- MenstrualCyclesAppPlugin
- MentalHealth
- MentalHealthDaemon
- Mercury
- Message
- MessageUI
- MessageUIFramework
- Messages
- MessagesAirlockService
- MessagesBlastDoorSupport
- MessagesCloudSync
- MessagesDataMigrator
- MessagesFlowDelegatePlugin
- MessagesPolls
- MessagesSettingsUI
- MessagesSupport
- Metal
- MetalPerformanceShadersGraph
- MicroLocationDaemon
- MobileActivation
- MobileAsset
- MobileCal
- MobileInBoxUpdate
- MobileMail
- MobileMailSettings
- MobileMailUI
- MobileNotes
- MobileSMS
- MobileSafariFramework
- MobileSafariSettings
- MobileSlideShow
- MobileStore
- MobileStoreDemoKit
- MobileStoreUI
- MobileTimer
- MobileTimer-Assistant
- MobileTimerFramework
- MobileTimerUI
- MobileTimerUIFramework
- MobilityAppPlugin
- ModelCatalog
- ModelCatalogRuntime
- ModelIO
- Moments
- MomentsUI
- MomentsUIServiceCore
- MonogramPosterExtension
- MorpheusExtensions
- MorphunAssets
- Movie-QuickLook
- Movies-Assistant
- MultitouchSupport
- Music
- MusicApplication
- MusicCarDisplayUI
- MusicKitInternal
- MusicMessagesApp
- MusicRecognition
- MusicScriptUpdateService
- MusicSettings
- MusicUI
- MusicUsage
- MuteModule
- NANDTaskScheduler
- NDOAPI
- NFC
- NFCControlCenterModule
- NFStorageServer
- NFUIService
- NTKCustomization
- NTKUltraCubeFaceBundleCompanion
- NanoCalendarBridgeSettings
- NanoCalendarComplicationsCompanion
- NanoCalendarPingSubscriber
- NanoCompassComplications
- NanoControlCenter
- NanoHealthBalanceBridgeSettings
- NanoMenstrualCyclesCompanionSettings
- NanoPassKit
- NanoPassKitUI
- NanoRegistry
- NanoTimeKitCompanion
- NaturalLanguage
- Navigation
- Nearby
- NetworkQuality
- Nexus
- NotesAnalytics
- NotesEditor
- NotesSupport
- NotesUI
- NotificationCenter
- NotificationsSettings
- NowPlayingUI
- OSEligibility
- OctagonTrust
- OnBoardingKit
- OpusKit
- OrientationLockModule
- OxygenSaturationSettings
- PBBridgeSupport
- PCViewService
- PairedDeviceRegistry
- PaperBoardUI
- PaperKit
- PassKitFramework
- PassKitUIFoundation
- PassKitWrapperXPCServiceUI
- PassbookSettings
- PassesLockScreenPlugin
- PasswordsSettings
- PeerPaymentMessagesExtension
- Pegasus
- PegasusConfiguration
- PegasusKit
- PencilKit
- PeopleMessageService
- PeopleSuggester
- PerfPowerMetricMonitor
- PerfPowerServicesMetadata
- PerfPowerTelemetryClientRegistrationService
- PerformanceTraceModule
- PersonalSearchService
- PhoneKit
- Photo Booth
- PhotoLibrary
- PhotoLibraryFramework
- PhotosEditUI
- PhotosFormats
- PhotosFramework
- PhotosUI
- PhotosUIFramework
- PlatterKit
- PlugInKitDaemon
- Podcasts
- PodcastsFoundation
- PodcastsPodcastsTodayExtension
- PodcastsTranscripts
- PodcastsUI
- PosterBoard
- PosterBoardFramework
- PosterFuturesKit
- PosterKit
- PosterUIFoundation
- PowerUI
- PowerlogHelperdOperators
- PowerlogLiteOperators
- PreBoard
- Preferences
- PreferencesFramework
- PreferencesUI
- Preview
- PreviewUI
- PrintKitUI
- PrivacyAndSecuritySettings
- PrivacySettingsUI
- PrivateCloudComputeDaemon
- PrivateMLClientInferenceProvider
- ProVideo
- ProactiveSupport
- ProductKit
- ProductKitService
- ProductPageExtension
- Profiles
- PromotedContentJetClient
- PromotedContentJetSupport
- PromotedContentPrediction
- PromotedContentProxy
- ProxCardKit
- ProximityReader
- ProximityReaderDaemon
- QueryParser
- QuickLook
- QuickLookThumbnailingDaemon
- QuickSpeak
- QuickTime Plugin
- RTTUI
- RTTUtilities
- RapidResourceDelivery
- RawCamera
- RealityFoundation
- RealityKit
- RecentlyPlayedTodayExtension
- RecentsAvocado
- Recon3D
- RelevanceEngine
- ReminderKit
- ReminderKitInternal
- RemindersSettings
- RemindersUICore
- RemoteManagementStore
- RemotePairingDevice
- RemoteServiceDiscovery
- RemoteUIFramework
- ReplayKit
- ReplayKitModule
- ReportCrash
- ReportMemoryException
- RequestDispatcherBridges
- RespiratoryHealthAppPlugin
- RespiratoryHealthDaemon
- Restaurants-Assistant
- Rhine
- RichLinkProvider
- RunningBoard
- RunningBoardServices
- SESUIServiceApp
- SIMSetupSupport
- SIMSetupUIService
- SMSPreferences
- SOS
- SOSSettings
- SafariFoundation
- Safety
- SafetyMonitor
- SaveToFiles
- ScreenReaderOutput
- ScreenTime
- ScreenTimeSettingsUI
- ScreenTimeSwift
- ScreenTimeUI
- ScreenshotServices
- ScreenshotServicesFramework
- ScreenshotServicesService
- SearchAds
- SearchAssets
- SearchFoundation
- SearchOnDeviceAnalytics
- SearchSettings
- SearchToShareCore
- SearchUI
- SecureAudioPasscodeComponent
- SecurePairing
- SensingAlgsPadHostServiceJ8xx
- SensingAlgsService
- SensingAlgsTouchButtonHost
- SensitiveContentAnalysis
- SensitiveContentAnalysisUI
- SequoiaTranslator
- SessionAlert
- SessionSyncEngine
- Settings-Assistant
- SettingsCellularUI
- SetupAssistant
- SetupAssistantSupport
- SetupAssistantUI
- SetupKit
- SeymourClient
- SeymourServices
- SeymourServicesCore
- SeymourUI
- ShareSheet
- SharedWithYou
- SharedWithYouCore
- SharedWithYouFramework
- SharingUI
- SharingUIService
- SharingViewService
- ShazamCore
- ShazamKitUI
- ShelfKit
- ShelfKitCollectionViews
- Shortcuts
- ShortcutsSettings
- ShortcutsUI
- SidebarFileDispatcher
- SidebarFileDispatcherService
- Sidecar
- Silex
- SilexVideo
- SilexWeb
- SiriActivation
- SiriAudioSupport
- SiriAutoComplete
- SiriFindMy
- SiriGestureBridge
- SiriHeadlessService
- SiriInference
- SiriInformationSearch
- SiriKitRuntime
- SiriMessageBus
- SiriMessagesFlowCommon
- SiriMessagesUI
- SiriMessagesUICommon
- SiriNaturalLanguageParsing
- SiriPlaybackControlIntents
- SiriRequestDispatcher
- SiriSettingsIntents
- SiriSetup
- SiriSharedUI
- SiriTTS
- SiriTTSService
- SiriUI
- SiriUIBridge
- SiriUICore
- Siriland
- Sleep
- SleepDaemon
- SleepHealth
- SleepHealthAppPlugin
- SleepHealthDaemon
- SleepHealthUI
- SmartIOFirmware_ASCv7.im4p
- SnippetKit
- SnippetUI
- SocialFramework
- SocialLayer
- SocialWeeApp
- SoftwareUpdateBridge
- SoftwareUpdateController
- SoftwareUpdateCoreSupport
- SoftwareUpdateServicesUIPlugin
- SoftwareUpdateSettings
- SoftwareUpdateUIFoundation
- SoftwareUpdateUIKit
- SoftwareUpdateUIMobile
- SoftwareUpdateUIMobileSettingsPlugin
- SoftwareUpdateUIService
- SoundAnalysis
- SoundBoardServices
- SoundsAndHapticsSettings
- SpaceAttribution
- SpeakThis
- SpeakThisServices
- SpeechRecognitionCommandAndControl
- Sports-Assistant
- Spotlight
- SpotlightDiagnostics
- SpotlightEmbedding
- SpotlightKnowledge
- SpotlightLinguistics
- SpotlightUIInternalFramework
- SpringBoardFoundation
- SpringBoardHome
- SpringBoardUI
- SpriteKit
- StickerKit
- StickerPickerService
- Stickers
- StickersUI
- Stocks
- Stocks-Assistant
- StocksAnalytics
- StocksCore
- StocksFramework
- StocksUI
- StocksWidget
- StorageKit
- StorageSettings
- StorageSettingsFramework
- StoreDynamicUIPlugin
- StoreKitFramework
- StoreKitUI
- StoreKitUISceneService
- StoreKitUIService
- SubscribePageExtension
- SupportFlow
- SymptomDiagnosticReporter
- SymptomEvaluator
- System-Assistant
- SystemApertureUI
- SystemAppMigrator
- SystemConfiguration
- SystemPlugin
- SystemStatusServer
- SystemStatusUI
- SystemUIWindowingKit
- TCC
- TSImageGeneration
- TSMediaLibrary
- TV
- TVAppServices
- TVMLKit
- TVPlayback
- TVRemoteModule
- TVRemoteUIService
- TVSettings
- TeaBreeze
- TeaUI
- TelephonyPreferences
- TelephonyUI
- TelephonyUIFramework
- TelephonyUtilities
- TemplateKit
- TextComposer
- TextInput_cs
- TextInput_sk
- TextUnderstandingRuntime
- ThumbnailsBlastDoorService
- TimerModule
- TinCanShared
- TipKit
- TipKitCore
- TipsApp
- TipsCore
- TipsDaemon
- TipsNotificationExtension
- TipsWidgetExtension
- TirePressure
- ToneKit
- ToneLibrary
- ToolKit
- TouchSensitiveButtonHIDService
- Transfer to Android
- Translate
- TransparencyDetailsView
- Trial
- TrialServer
- Trip
- TuriCore
- TwitterFramework
- TypistFramework
- UARPUpdaterServiceLegacyAudio
- UARPiCloud
- UIKit
- UIKitCore
- USDObjCKit
- UniformTypeIdentifiers
- UnilogTelemetry
- UpNext
- UsageSettings
- UsageTrackingAgent
- UserNotificationsKit
- UserNotificationsServer
- UserNotificationsSettings
- UserNotificationsUI
- UserNotificationsUIKit
- VFX
- VPNPreferences
- Vehicle
- ViceroyTrace
- VictoriaSettings
- VideoConferenceControlCenterModule
- VideoEffect
- VideoToolbox
- Videos
- VideosExtrasFramework
- VideosUICore
- VideosUIFramework
- VirtualAudio
- Visage
- VisionHWAccelerationServices
- VisionHealthAppPlugin
- VisionKitCore
- VisualAlert
- VisualIntelligenceCore
- VisualIntelligenceUI
- VisualLocalization
- VisualLogger
- VisualLookUp
- VoiceControlSettings
- VoiceMemos
- VoiceOverServices
- VoiceProcessor
- VoiceShortcutsUI
- VoiceTriggerUI
- VolumeLimitSettings
- WAAnswer-Assistant
- WPDaemon
- WalletPrivacySettings
- Wallpaper
- WallpaperKit
- WallpaperSettings
- WatchControlSettings
- WatchFacesWallpaperSupport
- WatchKit
- WatchListKit
- WatchQuickActionsServices
- Weather
- WeatherCore
- WebBookmarks
- WebContentRestrictionsUI
- WebInspector
- WebProcess
- WebProcessLoader
- WelcomeKitUI
- WidgetConfigurationExtension
- WidgetKit
- WidgetRenderer
- Widgets
- WirelessModemSettings
- WirelessRadioManagerd
- WorkflowEditor
- WorkflowUI
- WorkflowUICore
- WorkflowUIServices
- WritingToolsUI
- WritingToolsUIService
- ZoomServices
- ZoomWindow
- _JetEngine_SwiftUI
- _MapKit_SwiftUI
- _PermissionKit_SwiftUI
- adc-silenus-v5x.im4p
- afktool
- agx_a000
- agx_a010
- agx_b000
- analyticsagent
- ansf.t8150.release.im4p
- aonsensed
- appinstallationmetricsd
- apsd
- asd
- asktod
- assetsd
- assistantd
- assistivetouchd
- audioanalyticsd
- backupd
- bookassetd
- businessservicesd
- captiveagent
- catutil
- centaurid
- chs.dylib
- chsrom.dylib
- cht.dylib
- chtrom.dylib
- com.apple.CloudDocsUI.CloudSharing-AppExtension
- com.apple.DiagnosticsSessionAvailibility
- com.apple.DocumentManager.Service-AppExtension
- com.apple.DriverKit-AppleBCMWLAN
- com.apple.DriverKit-AppleEthernetE1000
- com.apple.MobileSoftwareUpdate.CleanupPreparePathService
- com.apple.NeighborhoodActivityConduitService
- com.apple.Safari.SearchHelper
- com.apple.SpeechRecognitionCore.speechrecognitiond
- com.apple.accessoryd.matching
- com.apple.driver.AppleBasebandM20
- com.apple.driver.AppleHIDTransportSPI
- com.apple.driver.AppleM2ScalerCSCDriver
- com.apple.driver.AppleMobileFileIntegrity
- com.apple.driver.AppleProcessorTrace
- com.apple.driver.AppleProxDriver
- com.apple.driver.AppleSARService
- com.apple.driver.AppleSEPManager
- com.apple.driver.AppleSPMIPMU
- com.apple.driver.AppleT8150CLPC
- com.apple.driver.corecapture
- com.apple.iokit.IOHIDFamily
- com.apple.iokit.IOMobileGraphicsFamily-DCP
- com.apple.iokit.IOThunderboltFamily
- com.apple.iokit.IOUSBHostFamily
- com.apple.security.AKSAnalytics
- com.apple.security.AppleImage4
- com.apple.security.sandbox
- companiond
- configd
- coreauthd
- corespeechd
- deleted_helper
- demod
- demod_helper
- deu.dylib
- devicerecoveryd
- diskarbitrationd
- eci.dylib
- eng.dylib
- enu.dylib
- esm.dylib
- esp.dylib
- exclave_kernel
- exclave_pmm_exclave
- familynotificationd
- filecoordinationd
- fileproviderctl
- fin.dylib
- findmydeviced
- footprint
- fra.dylib
- frc.dylib
- gamesaved
- geoanalyticsd
- get-network-info
- gputoolsserviced
- hangreporter
- hangtracerd
- homeeventsd
- iAdFramework
- iCloudDriveApp
- iCloudSubscriptionOptimizerCore
- iCloudSubscriptionOptimizerDaemon
- iCloudWebData
- iCloudWebUI
- iOSDiagnostics
- iTunesStoreUIFramework
- icloudmailagent
- iconservicesagent
- inboxupdaterd
- ita.dylib
- itunescloudd
- jpn.dylib
- jpnrom.dylib
- kor.dylib
- korrom.dylib
- languageassetd
- latticed
- libAONConnection.dylib
- libAppletTranslationLibrary.dylib
- libAudioIssueDetector.dylib
- libBBUpdaterDynamic.dylib
- libBasebandCommandDrivers.dylib
- libBasebandCommandDriversARI.dylib
- libBasebandCommandDriversMIPC.dylib
- libBasebandCommandDriversQMI.dylib
- libBasebandManager.dylib
- libBasebandManagerDAL.dylib
- libBasebandManagerICE.dylib
- libCommCenterAWDMetrics.dylib
- libCommCenterBase.dylib
- libCommCenterKCommandDrivers.dylib
- libCoreFSCache.dylib
- libEmbeddedSystemAUs.dylib
- libFontParser.dylib
- libGPUCompilerImpl.dylib
- libGPUCompilerImplLazy.dylib
- libGPUCompilerUtils.dylib
- libGSFont.dylib
- libHSFilerDynamic.dylib
- libKTLDynamic.dylib
- libLLVM.dylib
- libMTLHud.dylib
- libMemoryResourceException.dylib
- libPN548_API.dylib
- libRPAC.dylib
- libRoseBooter.dylib
- libSEUpdater.dylib
- libSparseBLAS.dylib
- libSystemDetermination.dylib
- libVinylNonUpdater.dylib
- libVinylUpdater.dylib
- libafc.dylib
- libcompression.dylib
- libcopyfile.dylib
- libcorecrypto.dylib
- libcorecrypto_noasm.dylib
- libcorecrypto_trace.dylib
- libcoreroutine.dylib
- libexpat.1.dylib
- libfire7.dylib
- libmis.dylib
- libnetworkextension.dylib
- libnfstorage.dylib
- libquic.dylib
- libramrod.dylib
- libsandbox.1.dylib
- libsystem_c.dylib
- libsystem_eligibility.dylib
- libsystem_kernel.dylib
- libsystem_notify.dylib
- libsystemstats.dylib
- libwebrtc.dylib
- libxml2.2.dylib
- libxslt.1.dylib
- lockdownd
- magicswitchd
- maild
- manageddeviced
- mapssyncd
- mediaanalysisd
- mediaanalysisd-generation
- mediaanalysisd-service
- mediamlxpc
- mobile_storage_proxy
- mobileassetd
- model.dylib
- modelmanagerd
- momentsd
- nanobackupd
- nanoprefsyncd
- nanoregistryd
- nanosystemsettingsd
- ndoagent
- nearbyd
- notifyd
- online-auth-agent
- osanalyticshelper
- parsec-fbf
- parsecd
- pasted
- pcsstatus
- perfdiagsselfenabled
- pfd
- pipelined
- powerd
- powerdatad
- ptb.dylib
- rans.t8150.release.im4p
- remindd
- remotepairingdeviced
- safetycheckd
- searchdiagnose
- searchpartyd
- security-sysdiagnose
- sensingpredictd
- sirittsd
- snatmap
- softposreaderd
- spindump
- spindump_fileparser
- srp-mdns-proxy
- storagekitd
- swiftuitraced
- swtransparency-sysdiagnose
- sysdiagnose_helper
- sysdiagnosed
- t8150.msrf.im4p
- t8150.rmsr.im4p
- t8150pmp.im4p
- tccd
- terminusd
- usbaudiod
- usernotificationsd
- vCard
- watchdogd
- webbookmarksd
- webprivacyd
- wifianalyticsd
- wifid
- xpcroleaccountd

</details>

## LOW_SIGNAL -- excluded (1892, metadata/timestamp churn only)

<details><summary>Show 1892 components</summary>

- +com.apple.AGXFirmwareKextRTBuddy64 (353.14)
- +com.apple.AGXG18P (353.14)
- +com.apple.driver.ASIOKit (26.5.0)
- +com.apple.driver.AppleAVD (962)
- +com.apple.driver.AppleAVE2 (905.40.1)
- +com.apple.driver.AppleActuatorDriver (9160.1)
- +com.apple.driver.AppleDiskImages2 (524.160.11)
- +com.apple.driver.AppleGameControllerPersonality (13.6.2)
- +com.apple.driver.AppleH16ANEInterface (9.512.0)
- +com.apple.driver.AppleH16CameraInterface (5.604)
- +com.apple.driver.AppleIDV (8.601)
- +com.apple.driver.AppleJPEGDriver (8.1.3)
- +com.apple.driver.AppleMultitouchDriver (9160.1)
- +com.apple.driver.AppleMultitouchSPI (9160.1)
- +com.apple.driver.AppleProxDriver (49.5.6)
- +com.apple.driver.AppleT8150ANEHAL (9.512.0)
- +com.apple.driver.AppleUSBAudio (850.5)
- +com.apple.driver.AppleUSBDeviceAudioController (850.5)
- +com.apple.filesystems.apfs (2811.160.7)
- +com.apple.filesystems.hfs.kext (715.160.9)
- +com.apple.iokit.IOGPUFamily (130.16.4)
- +com.apple.iokit.IOGameControllerFamily (13.6.2)
- +com.apple.iokit.IOSurface (393.5.8)
- +com.apple.iokit.IOTimeSyncFamily (1460.2)
- +com.apple.kpi.bsd (25.6.0)
- +com.apple.kpi.dsep (25.6.0)
- +com.apple.kpi.iokit (25.6.0)
- +com.apple.kpi.libkern (25.6.0)
- +com.apple.kpi.mach (25.6.0)
- +com.apple.kpi.private (25.6.0)
- +com.apple.kpi.unsupported (25.6.0)
- +com.apple.plugin.IOgPTPPlugin (1460.2)
- -com.apple.AGXFirmwareKextRTBuddy64 (350.37)
- -com.apple.AGXG18P (350.37)
- -com.apple.driver.ASIOKit (26.4.8)
- -com.apple.driver.AppleAVD (960)
- -com.apple.driver.AppleAVE2 (905.36.1)
- -com.apple.driver.AppleActuatorDriver (9140.5)
- -com.apple.driver.AppleDiskImages2 (524.100.22)
- -com.apple.driver.AppleGameControllerPersonality (13.4.9)
- -com.apple.driver.AppleH16ANEInterface (9.511.2)
- -com.apple.driver.AppleH16CameraInterface (5.408)
- -com.apple.driver.AppleIDV (8.420.1)
- -com.apple.driver.AppleJPEGDriver (7.7.9)
- -com.apple.driver.AppleMultitouchDriver (9140.5)
- -com.apple.driver.AppleMultitouchSPI (9140.5)
- -com.apple.driver.AppleProxDriver (49.5.1)
- -com.apple.driver.AppleT8150ANEHAL (9.511.0)
- -com.apple.driver.AppleUSBAudio (841.2)
- -com.apple.driver.AppleUSBDeviceAudioController (841.2)
- -com.apple.filesystems.apfs (2811.102.1)
- -com.apple.filesystems.hfs.kext (715.100.10)
- -com.apple.iokit.IOGPUFamily (130.13)
- -com.apple.iokit.IOGameControllerFamily (13.4.9)
- -com.apple.iokit.IOSurface (393.5.7)
- -com.apple.iokit.IOTimeSyncFamily (1440.24)
- -com.apple.kpi.bsd (25.4.0)
- -com.apple.kpi.dsep (25.4.0)
- -com.apple.kpi.iokit (25.4.0)
- -com.apple.kpi.libkern (25.4.0)
- -com.apple.kpi.mach (25.4.0)
- -com.apple.kpi.private (25.4.0)
- -com.apple.kpi.unsupported (25.4.0)
- -com.apple.plugin.IOgPTPPlugin (1440.24)
- AAAFoundationSwift
- AAAFoundationUI
- AACClient
- AACCore
- AADataclassEnableNotificationPlugin
- ABMHelper
- ACDatabaseBackupNotificationPlugin
- ACIAdapter
- AFKUser
- AGXGPURawCounter
- AGXGPURawCounterBundle
- ALDataTypes.dylib
- ALUtil.dylib
- AMPCoreUI
- AMSEngagementViewService
- ANEClientSignals
- ANEServices
- AONSense.dylib
- AONVL
- ASOctaneSupport
- ATFoundation
- AUDeveloperSettings
- AUSettings
- AVKitSettings
- AVRouting
- AXAggregateStatisticsServices
- AXContainerServices
- AXCoreUtilities
- AXFlashScreenUIServices
- AXLocalizationCaptionService
- AXMotionCuesServices
- AXSoundDetection
- AXSpeakFingerManager
- AXWatchRemoteScreenServices
- AXWatchRemoteScreenUI
- Accelerate
- Accessory
- AccessoryAssistiveTouch
- AccessoryAudio
- AccessoryBLEPairing
- AccessoryCommunications
- AccessoryHID
- AccessoryLiveActivities
- AccessoryLiveActivitiesUI
- AccessoryMediaLibrary
- AccessoryNavigation
- AccessoryNowPlaying
- AccessoryOOBBTPairing
- AccessoryVoiceOver
- AccessoryiAP2Shim
- ActionPredictionHeuristics
- ActionPredictionHeuristicsInternal
- ActivityAwardsCore
- ActivityAwardsPlugin
- ActivityProgressKit
- ActivitySharingAwardsPlugin
- ActivitySharingClient
- ActivitySharingHealthDaemon
- ActivitySharingPlugin
- ActivitySharingServices
- ActivityUI
- AdAttributionKit
- AdPlatforms
- AdPlatformsCommonUI
- AdPlatformsInternal
- AdServices
- AddressBookUI
- AeroML
- AirDropSettingsSupport
- AirFair
- AirPlayAndHandoffSettingsSupport
- AirPlayOverlays
- AirPlayRoutePrediction
- AirPlaySenderKit
- AirPlaySenderUI
- AirTraffic
- AirTrafficDevice
- AlarmKit
- AlarmKitCore
- AlarmKitFoundation
- AlarmModule
- AlarmUIFramework
- AlgorithmsInternal
- AltimeterHarvest
- AppClip
- AppGenius
- AppIntentSchemas
- AppIntentsIndex
- AppIntentsServices
- AppIntentsTypeSupport
- AppNotificationsLoggingClient
- AppPredictionFoundation
- AppPredictionIntentsHelperService
- AppPredictionToolsInternal
- AppPredictionUIFoundation
- AppRecommendations
- AppSSO
- AppSSOCore
- AppSSOUI
- AppServerSupport
- AppStoreComponentsDaemonKit
- AppStoreFoundation
- AppStoreOverlays
- AppStoreUI
- AppStoreUtilities
- AppSystemSettings
- AppleAOPAudioPlugin
- AppleBasebandLink
- AppleCV3D
- AppleCV3DMOVKit
- AppleCV3DModels
- AppleCVHWA
- AppleFSCompression
- AppleIDAuthentication
- AppleIDSSOAuthentication
- AppleIDSSOAuthenticationPlugin
- AppleIDSSONotificationPlugin
- AppleJPEGXL
- AppleLatticeSupport
- AppleMediaServicesKitSupport
- AppleMipcRouter
- AppleMobileFileIntegrity
- AppleNVMe
- ApplePushService
- AppleSARHelper
- AppleSMCFirmware.bin
- AppleTracingSupportSymbolication
- Artwork
- Asen.dylib
- AskPermission
- AskPermissionUI
- AskTo
- AskToCore
- AssertionServices
- AssetCacheServices
- AssetCacheServicesExtensions
- AssistantCardServiceSupport
- AssistantSettingsFoundation
- AssistantSettingsSupport
- AssistiveTouch-iOS
- AssistiveTouchUI
- AsyncAlgorithmsInternal
- AtomicsInternal
- AudioAccessoryAssetManagement
- AudioAnalytics
- AudioDataAnalysis
- AudioServerApplication
- AudioSessionServer
- AutomatedDeviceEnrollment
- AutomaticAssessmentConfiguration
- AvailabilityKit
- BLEPairing-iOS
- BNNSGraphPCC
- BNNSOdieDelegate
- BackBoardHIDEventProcessors
- BackgroundSoundsCCModule
- BackgroundSystemTasks
- BackgroundTasks
- BacklightServices
- BagKit
- BarcodeSupport
- BasebandTraceHelper
- BatteryCenter
- BinaryParsingInternal
- BiomeDSL
- BiomePubSub
- BiomeSync
- BlueTool
- BluetoothAudio
- BluetoothManager
- BluetoothServices
- BluetoothServicesUI
- BluetoothUIService
- Bom
- BookCoverUtility
- BookDataStore
- BookFoundation
- BookLibrary
- BookLibraryCore
- BookUtility
- BoundingPathData
- BrailleSymbology
- BrailleTranslation
- BridgeCommons
- BridgeLiveActivity
- BridgeReporting
- BrightnessControl
- BrowserEngineCore
- BrowserEngineKit
- BrowserKit
- BrowserSupportKit
- BubbleKit
- BulletinBoard
- BusinessChat
- BusinessFoundation
- BusinessServices
- ByteMatrixVerification
- C2
- CDDataAccess
- CDDataAccessExpress
- CMCaptureDevice
- CMContinuityCaptureCore
- CMImaging
- CMPhoto
- CPAnalytics
- CSExattrCrypto
- CTBlastDoorSupport
- CTCarrierSpace
- CTParser
- CalculateUI
- CalculatorModule
- CalendarDaemon
- CalendarIntegrationSupport
- CallKit
- CallsPersistence
- CallsUtilities
- CallsXPC
- CameraColorProcessing
- CameraEditKit
- CameraModule
- CameraOverlayServices
- CaptiveNetwork
- CarAccessoryDaemon
- CarCommandsFlowDelegatePlugin
- CarCommandsUIFramework
- CarPlayArtwork
- CardioHealth
- CarouselPreferenceServices
- CarrierSettings
- Celestial
- CellularPlanManager
- Centauri
- CentauriAlphaPatchBay
- CentauriBetaPatchBay
- CentauriDiagnostic
- CheckerBoardServices
- Chirp
- CinematicFraming
- ClarityFoundation
- ClassKit
- ClassKitDeveloperSettings
- ClassKitSettings
- ClassKitUI
- ClockAppIntentsSupport
- ClockComplications
- ClockKitUI
- ClockUIFramework
- CloudAsset
- CloudCoreInternal
- CloudKitAccessPlugin
- CloudKitAuthenticationPlugin
- CloudKitCode
- CloudKitCodeProtobuf
- CloudKitDaemon
- CloudKitDistributedSync
- CloudKitNotificationPlugin
- CloudKitSettings
- CloudPhotoServices
- CloudSubscriptionFeatures
- CollectionViewCore
- CollectionsInternal
- ColorSync
- CommandAndControlUI
- CommonAuth
- CommunicationTrust
- Communications-iOS
- CommunicationsFilter
- CompanionHealthPlugin
- CompassCalibration
- CompassUI
- ContactlessReaderUI
- ContainerManagerSystem
- ContainerManagerUser
- ContextualUnderstanding
- ContinuitySing
- ContinuousDialogManagerService
- ControlCenterServices
- ControlCenterUIServices
- CookingData
- Coordination
- CoordinationCore
- CopresenceCore
- CopyHFSMeta
- CoreAUC
- CoreAccessories
- CoreAccessoriesFeatures
- CoreAnalytics
- CoreBluetoothUI
- CoreCDPUIInternal
- CoreCapture
- CoreCaptureControl
- CoreDuetContext
- CoreDuetDaemonProtocol
- CoreDuetSync
- CoreFollowUpUI
- CoreHID
- CoreIDCred
- CoreIDCredBuilder
- CoreIDV
- CoreIDVDaemonSupport
- CoreIDVShared
- CoreImage
- CoreLocationReplay
- CoreLocationSync
- CoreLocationTiles
- CoreLocationUI
- CoreMIDI
- CoreML
- CoreMLModelSecurityService
- CorePhoneNumbers
- CoreRE
- CoreRecents
- CoreRepairKit
- CoreRepairLite
- CoreRepairUI
- CoreRoutine
- CoreServicesStore
- CoreSpeechDataAnalytics
- CoreSpeechExclave
- CoreSpeechUtils
- CoreSuggestions
- CoreText
- CoreThread
- CoreThreadCommissionerServiced
- CoreThreadRadio
- CoreUtilsUI
- CorrectionsProfilesSync
- CosmeticAssessment
- CredentialProviderExtensionHelper
- CryptoKitCBridging
- CryptoKitPrivate
- DACalDAV
- DACoreDAVGlue
- DAIMAPNotes
- DALDAP
- DANECPWrapper
- DASDaemon
- DASDelegate
- DASubCal
- DEPClientLibrary
- DMCApps
- DMCToolsUIUtilities
- DRMFoundation
- DSContinuityPairing
- DSRemotePairing
- DataAccess
- DataAccessExpress
- DataAccessUI
- DataActivation
- DataCollector
- DataCollectorLibrary
- DataDetection
- DataRelay
- DataRelay_Private
- DateAndTimeSupport
- DeclaredAgeRange
- DefaultAccessPlugin
- DesignLibrary
- DesktopServicesUI
- DeviceActivity
- DeviceCheck
- DeviceDiscoveryExtension
- DeviceExpertIntents
- DeviceExpertUI
- DeviceTreeKit
- DiagnosticExtensionsDaemon
- DiagnosticLogCollection
- DiagnosticRequest
- DiagnosticRequestService
- DiagnosticsReporterServices
- DiagnosticsSessionAvailability
- DiagnosticsSupport
- DictionaryServices
- DifferentialPrivacy
- DiskArbitration
- DiskImages
- DiskSpaceDiagnostics
- DistributedEvaluation
- DocumentManagerCore
- DocumentUnderstanding
- DocumentUnderstandingClient
- DoubleAgent
- DumpPanic
- EAFirmwareUpdater
- EAP8021X
- EXDisplayPipe
- EasyConfig
- EchoRelay
- EmailAddressing
- EmailFoundation
- EmbeddingService
- EncoreXPCService
- EnergyKit
- EnergyKitFoundation
- Engram
- EnhancedLoggingState
- Espresso
- EventKitUI
- EventKitUICore
- ExclaveFDRDecode
- ExposureNotification
- ExposureNotificationDaemon
- ExtensionKit
- FMCore
- FMCoreLite
- FMCoreUI
- FMF
- FMFUI
- FMNetworking
- FSEvents
- FTAWD
- FTClientServices
- FaceTimeFeatureControl
- FaceTimeMigrator
- FaceTimeNameUtility
- FaceTimeNotificationCore
- FaceTimeNotificationUI
- FamilyControls
- FamilyControlsObjC
- FamilyControlsSlotSupport
- FamilyNotification
- FedStats
- FeedbackAssistantModule
- FileIndexerDaemon
- FileProviderOverride
- FileProviderResolver
- FileProviderTelemetry
- FilterAsNewCallersSettingsBundle
- FindMyBase
- FindMyBluetooth
- FindMyCloudKit
- FindMyCommon
- FindMyCore
- FindMyCrypto
- FindMyDaemonSupport
- FindMyDeviceUI
- FindMyLocateObjCWrapper
- FindMyMessaging
- FindMyPairing
- FindMyServerInteraction
- FindMyStorage
- FindMyUICore
- FindMyUnsafeAsyncBridging
- FitnessActions
- FitnessAppRoot
- FitnessAsset
- FitnessAwards
- FitnessBrowsing
- FitnessCanvas
- FitnessCanvasUI
- FitnessCoreUI
- FitnessDispatch
- FitnessFiltering
- FitnessForYou
- FitnessIntelligenceDaemonCore
- FitnessIntelligenceFeedback
- FitnessIntelligenceInference
- FitnessIntelligenceSnapshotting
- FitnessLibrary
- FitnessMarketing
- FitnessOnboarding
- FitnessProductDetail
- FitnessRemoteBrowsing
- FitnessSampleContent
- FitnessSearch
- FitnessSharePlaySession
- FitnessSiriSession
- FitnessSummary
- FitnessTrainerTips
- FitnessUtilities
- FlowFrameKit
- Focus
- FocusEngine
- FoundationODR
- FramePacing
- FusionTracker
- GEO
- GKSPerformance
- GPUToolsDeviceServices
- GSS
- Game
- GameControllerIO
- GameControllerSettings
- GameControllerUI
- GameKit
- GamePolicyFoundation
- GamePolicyServices
- GameplayKit
- GenerativeAssistantActions
- GenerativeAssistantCommon
- GenerativeAssistantEnablementFlow
- GenerativeAssistantSettings
- GenerativeAssistantUI
- GenerativeExperiences
- GenerativeExperiencesRuntime
- GenerativeExperiencesUI
- GenerativeFunctions
- GenerativeFunctionsFoundation
- GenerativeFunctionsInstrumentation
- GenerativeModelsFoundation
- GenerativePartnerService
- GenerativePartnerServiceUI
- GenericGamepadHIDServicePlugin
- GeoToolbox
- GeoUIFramework
- GridZero
- GroupActivities
- H16ISPServices
- HID
- HIDAnalytics
- HIDDisplay
- HIDPreferences
- HIDRMClientKit
- HIDRMKit
- HMAssistant
- HRTFEnrollment
- HSAAuthentication
- HTTPTypesInternal
- HWAdapter
- HangTracerSettingsClient
- HeadphoneAccommodationsCCModule
- HeadphoneAssets
- HeadphoneProxFeatureService
- HealthAppHealthDaemonSupport
- HealthAppPlugin
- HealthAppServices
- HealthBalance
- HealthBalanceAppPlugin
- HealthBalanceDaemon
- HealthBalanceUI
- HealthCharts
- HealthChartsCore
- HealthCoaching
- HealthDomains
- HealthDomainsDaemon
- HealthDomainsUI
- HealthEventsDaemonImplementation
- HealthExperience
- HealthExpressions
- HealthFeatures
- HealthHearing
- HealthHeartRateStream
- HealthKitAdditions
- HealthKitOrchestrationAdditions
- HealthLEHeartRate
- HealthMedicationsWidgetUI
- HealthMenstrualCyclesUI
- HealthMenstrualCyclesWidgetUI
- HealthOntologyDaemonPlugin
- HealthOntologyKit
- HealthOrchestration
- HealthPlatformCore
- HealthPlatformFoundation
- HealthPluginHost
- HealthRecordsDaemon
- HealthRecordsWalletSupport
- HealthTopics
- HealthTopicsCore
- HealthTopicsDaemon
- HealthTopicsDaemonPlugin
- HearingAidsModule
- HearingCore
- HearingDevicesCCModule
- HearingMLHelper
- HeartDaemonPlugin
- HeartHealthUI
- HeroDataClient
- HeuristicInterpreter
- HomeAppIntents
- HomeAutomationInternal
- HomeAutomationUIFramework
- HomeCommunicationUIFramework
- HomeControlCenterSingleTileModule
- HomeEnergyUI
- HomeKitBackingStore
- HomeKitClips
- HomeKitCore
- HomeKitDaemonFoundation
- HomeKitEventRouter
- HomeKitFeatures
- HomePlatformSettingsUI
- HomeRecommendationEngine
- HomeServices
- HomeUI2
- HomeUICommon
- HomeUtilityServices
- HomeWidgetIntents
- HoverTextServices
- HumanUnderstandingEvidence
- HumanUnderstandingFoundation
- IDEDebugGaugeDataProviders
- IDSBlastDoorService
- IDSBlastDoorSupport
- IDSHashPersistence
- IDSKVStore
- IMAP
- IMDMessageServices
- IMFoundation
- IMSharedUI
- IMTranscoding
- IMTransferServices
- IOAccessoryManager
- IOFastPath
- IOGPU
- IOHIDEventProcessorFilter
- IOHIDEventSystemStatistics
- IOHIDKeyboardFilter
- IOHIDLib
- IOHIDPointerScrollFilter
- IOHIDT8027USBSessionFilter
- IOMobileFramebuffer
- IOSurface
- IOSurfaceAccelerator
- IOUSBHost
- IOUSBLib
- IPConfiguration
- ISPExclaveKitServices
- ITMLKit
- IXATestAppRelay
- IconFoundation
- IdentityDocumentServices
- IdentityDocumentServicesUI
- IdentityLookup
- IdentityLookupUI
- ImageHarmonizationKit
- ImagePlayground
- InAppMessages
- InAppMessagesCore
- IncomingCallFilter
- InertiaCam
- InfoQueryPersonalizationFeatures
- InputAnalyticsServer
- InstallCoordination
- IntelligenceFlowAppIntentsPreviewToolSupport
- IntelligencePlatformCompute
- IntelligencePlatformComputeService
- IntelligencePlatformDataActions
- IntelligencePlatformQuery
- IntelligenceTasks
- IntelligentRouting
- IntelligentRoutingMediaBundles
- IntelligentRoutingServices
- IntentRecommendRuntime
- IntentRecommendShared
- IntentsFoundation
- IntentsServices
- InternationalTextSearch
- IonosphereHarvest
- JPEGH1.videodecoder
- JPEGH1.videoencoder
- JarvisPlugin
- JetCore
- JetEngine
- JetPack
- JetUI
- JetsamProperties
- JoinRequests
- JournalShared
- JournalUI
- KerberosAuthenticationPlugin
- KernelManagerLibrary
- KeyboardArbiter
- KeyboardBrightnessModule
- KeyboardSettingsFeedback
- KnowledgeGraphKit
- LanguageModeling
- LearnedFeatures
- LegacyGameKit
- LegacyHandle
- LegalAndRegulatorySettingsSupport
- LighthouseBitacoraFramework
- LimitAdTracking
- LinkMetadata
- LinkPresentationStyleSheetParsing
- LiveCommunicationKit
- LiveFS
- LiveFSFPHelper
- LiveSpeechServices
- LiveSpeechUI
- LocalAuthenticationCredentialServices
- LocalAuthenticationEmbeddedUI
- LocalAuthenticationPreboard
- LocalStatusKit
- LocaleSettings
- LocationAccessStore
- LocationFenceSync
- LocationHarvest
- LocationLogEncryption
- LocationPromptUI
- LocationSupport
- LockdownMode
- LoggingSupport
- LowPowerModule
- MIDI
- MIME
- MMCSServices
- MPSBenchmarkLoop
- MPSCore
- MPSFunctions
- MPSHost
- MPSImage
- MPSMatrix
- MPSNeuralNetwork
- MPSRayIntersector
- MPUFoundation
- MSMessageExtensionBalloonPlugin
- MSUDataAccessor
- MTInferenceToolLib
- MTLCompiler
- MXI
- MXUIService
- MXUIServiceClient
- MagnifierModule
- MagnifierServices
- MailKit
- MailServices
- MailWebProcessSupport
- MallocStackLogging
- Managed
- ManagedApp
- ManagedAppDistribution
- ManagedAppsCore
- ManagedAppsInterface
- ManagedEvent
- ManagedSettingsObjC
- ManagedSettingsSupport
- ManagedSettingsUI
- ManifestStorageService
- MapKitSwiftBridge
- MapsBlastDoorSupport
- MapsIntelligence
- Marco
- MatterSupport
- MechTouchId
- MediaAnalysisBlastDoorSupport
- MediaAnalysisGeneration
- MediaAnalysisPhotosServices
- MediaControl
- MediaControlReceiver
- MediaControlSender
- MediaControlUI
- MediaControlsAudioModule
- MediaControlsModule
- MediaConversionService
- MediaGroups
- MediaGroupsDaemon
- MediaLibrary-iOS
- MediaMiningKit
- MediaPlatform
- MediaPlayerUI
- MediaServicesBroker
- MediaStream
- MediaTokens
- MedicalIDDaemon
- MemoryDiagnostics
- MenstrualCyclesDaemonPlugin
- MentalHealthAppPlugin
- MentalHealthUI
- MentalHealthWidgetUI
- MessageSupport
- MessagesComplication
- MetalPerformancePrimitives
- MetalPerformanceShaders
- MetricKit
- MetricKitCore
- MetricKitServices
- MetricKitSource
- MetricsFramework
- MicroFindMy
- MicroLocation
- MicroLocationKit
- MicroLocationUtilities
- MobileAccessoryUpdater
- MobileAssetExclaveServices
- MobileAssetUpdater
- MobileBackup
- MobileBluetooth
- MobileContainerManager
- MobileCoreServices
- MobileIcons
- MobileIdentityServiceUI
- MobileKeyBag
- MobileMulticastTransfer
- MobileObliteration
- MobilePhoneSettings
- MobileSoftwareUpdate
- MobileStorage
- MobileStorageMounter
- MobileStoreDemoSetupUI
- MobileSync
- MobileTimerSupport
- MobileTimerUISupport
- ModelMonitoringLighthouse
- ModuleBase
- MonogramPoster
- MotionCalibration
- MotionSensorLogging
- MultipeerConnectivity
- MultitouchHID
- MultitouchSessionFilterSupport
- MusicKitPlaybackSupport
- MusicSettingsSupport
- MusicStoreUI
- NCLaunchStats
- NDOUI
- NRDUpdated
- NameRecognition
- NanoAudioControl
- NanoFaceGallery
- NanoLeash
- NanoMailKitServer
- NanoMediaAPI
- NanoMediaBridgeUI
- NanoMenstrualCyclesComplication
- NanoMusicSync
- NanoSleepComplication
- NanoSystemSettings
- Navigation-iOS
- NearFieldAccessory
- NearFieldUI
- NearbySessions
- NeighborhoodActivityConduit
- NeighborhoodActivityConduitIntents
- Netrb
- NetworkQualityXPC
- NetworkRelay
- NetworkServiceProxy
- NetworkStatistics
- NeutrinoCore
- NewDeviceOutreach
- NewDeviceOutreachUI
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
- NewsNotificationPlugin
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
- NewsUserEvents
- Notes
- NotesPreviewKit
- NotesSiriUI
- NotesUIServices
- NowPlaying-iOS
- ODCurareEvaluationAndReporting
- ODDAnalytics
- ODDIFramework
- OOBBTPairing-iOS
- OSAServicesClient
- OSASubmissionClient
- OSASyncProxyClient
- OSAnalyticsPrivate
- OSIntelligence
- OSLog
- OTSVG
- OfficeImport
- OmniSearchTypes
- OnDeviceStorage
- OnDeviceStorageCore
- OnDeviceStorageInternal
- PDS
- PDSAgent
- PIRGeoProtos
- PLAMonitor
- PLSnapshot
- POP
- PairingProximity
- PanicHelper
- ParsecModel
- ParsecSubscriptionServiceSupport
- ParsingInternal
- PartnerVisualSearch
- PassKit
- PassKitServices
- PasswordsDigitalSeparation
- Pasteboard
- PaymentUI
- PearlEventFilter
- PegasusAPI
- PegasusPersistence
- People
- PeopleUI
- PeopleUIInternal
- PerfPowerServicesReader
- PerformanceControlKit
- PerformanceTrace
- PermissionKit
- PersonaKit
- PersonaUI
- PersonalAudio
- PersonalSearch
- PersonalSearchTypes
- PersonalizationPortraitInternals
- Phoenix
- Phone
- PhoneAppIntents
- PhoneNumbers
- PhoneSnippetUI
- Photo
- PhotoAnalysis
- PhotoEditing
- PhotoFoundation
- PhotoImaging
- PhotosImagingFoundation
- PhotosIntelligenceCore
- PhotosKnowledgeGraph
- PhotosMediaFoundation
- PhotosPlayer
- PhotosSearchClient
- PhotosSpatialMedia
- PhotosSpatialMediaCore
- PhotosSwiftUICore
- PhotosUIEdit
- Platform-Bluetooth
- PlugInKit
- PnROnDeviceFramework
- PodcastsKit
- PoirotAnalytics
- PoirotBlocks
- PoirotSQLite
- PoirotSchematizer
- PoirotUDFs
- PolarisBufferService
- Portrait
- PortraitCore
- PostSiriEngagement
- PosterBoardServices
- PosterBoardUI
- PosterBoardUIServices
- PosterFoundation
- PosterLegibilityKit
- PosterModel
- PosterPlatformSupport
- PowerlogAccounting
- PowerlogControl
- PowerlogDatabaseReader
- PowerlogFullOperators
- PredictedContextAlgorithms
- PreviewShellKit
- PreviewsFoundationOS
- PreviewsInjection
- PreviewsMessagingOS
- PreviewsOSSupport
- PreviewsOSSupportUI
- PreviewsServices
- PreviewsServicesUI
- PrivacyAccounting
- PrivateCloudCompute
- ProactiveBlendingLayer_iOS
- ProactiveCDNDownloader
- ProactiveContextClient
- ProactiveDaemonSupport
- ProactiveEventTracker
- ProactiveExperiments
- ProactiveHarvesting
- ProactiveInputPredictionsInternals
- ProactiveML
- ProactiveMagicalMoments
- ProactivePredictionClient
- ProactivePredictionFoundation
- ProactiveSuggestionClientModel
- ProfileValidatedAppIdentity
- PromotedContentJetService
- PromotedContentSupport
- PromptKit
- ProofReader
- ProtocolBuffer
- ProximityAppleIDSetup
- ProximityAppleIDSetupUI
- ProximityControl
- ProximityReaderCore
- PushToTalk
- QLCharts
- QRCodeModule
- QueryUnderstanding
- QuickLookSupport
- QuickLookThumbnailGeneration
- QuickLookThumbnailing
- QuickLookUICore
- QuickNoteModule
- QuickTime
- RESync
- RTBuddyCrashlogDecoder
- RTKit.bin
- RapportUI
- RealityFusion
- Recap
- RecencyService
- ReflectionInternal
- ReminderKitUI
- RemindersAppIntents
- RemindersIntentsFramework
- RemoteManagement
- RemoteManagementModel
- RemoteManagementProtocol
- RemoteManagementUI
- RemoteStateDumpKit
- RemoteXPC
- ReplicatorCore
- ReplicatorEngine
- ReplicatorServices
- ResearchApp
- RespiratoryHealth
- RespiratoryHealthDaemonPlugin
- RespiratoryHealthUI
- Rewind
- Routine
- RuntimeInternal
- SADSupport
- SAML
- SAObjects
- SCSharingReminders
- SDAPI
- SESUIService
- SESUIServiceCore
- SMBClientProvider
- SMBSearch
- SOSUI
- SPFinder
- SPOwner
- SPRCore
- SPShared
- STExtractionService
- STExtractionService.privileged
- Safari
- SafariSafeBrowsing
- SafetyAlerts
- SafetyKit
- SafetyMonitorUI
- Sage
- SchoolTime
- ScreenReaderBrailleDriver
- ScreenTimeUICore
- Search
- SearchIntrospectionKit
- SecureBackupNotification
- SecureControlService
- SecureVectorStorage
- SensitiveContentAnalysisML
- SensorAccess
- ServiceExtensions
- ServiceExtensionsCore
- ServiceManagement
- ServiceShared
- SessionAssertion
- SessionFoundation
- SessionPushNotifications
- SessionSQL
- SettingsCellular
- SettingsFoundation
- SetupAssistantSoftwareUpdateUI
- SeymourAwardsPlugin
- SeymourClientServices
- SeymourCore
- SeymourMedia
- SeymourServerProtocol
- SeymourSessionServices
- SharedUtils
- SharingHUD
- SharingXPCServices
- ShazamInsights
- ShazamModule
- ShortcutUIKit
- SidecarCore
- SidecarRelay
- SidecarUI
- SimpleKeyExchange
- SiriActivationFoundation
- SiriAnalytics
- SiriAnalyticsRuntime
- SiriAnalyticsToolKitSupport
- SiriAppResolution
- SiriAudioIntentUtils
- SiriAudioInternal
- SiriAudioSnippetKit
- SiriAutoCompleteAPI
- SiriCarCommandsIntents
- SiriEntityMatcher
- SiriFindMyUI
- SiriGeo
- SiriGlobalConfiguration
- SiriHomeAccessoryFramework
- SiriInferenceFlow
- SiriInformationTypes
- SiriInstrumentation
- SiriInstrumentationManifest
- SiriIntentEvents
- SiriInteractive
- SiriKitFlow
- SiriLiminal
- SiriLocalization
- SiriMASPFLTraining
- SiriMessageTypes
- SiriMessagesFlow
- SiriMetricsBugReporter
- SiriNLUOverrides
- SiriNLUTypes
- SiriNotebook
- SiriNotebookUI
- SiriObservation
- SiriPhoneCATs
- SiriPhoneIntents
- SiriPlaybackControlSupport
- SiriPowerInstrumentation
- SiriReaderServices
- SiriReferenceResolution
- SiriReferenceResolutionMetricsPlugin
- SiriRemembers
- SiriSchemaRegistry
- SiriSettingsUI
- SiriSignals
- SiriSpeechSynthesis
- SiriSuggestions
- SiriSuggestionsAPI
- SiriSuggestionsBaseModel
- SiriSuggestionsIntelligence
- SiriSuggestionsKit
- SiriSuggestionsSupport
- SiriSystemCommandsIntents
- SiriSystemCommandsUIFramework
- SiriTaskEngagement
- SiriTasks
- SiriTasksEvaluation
- SiriTimeAlarmInternal
- SiriTimeInternal
- SiriTimeTimerInternal
- SiriTurnRestatement
- SiriUIActivation
- SiriUICardKitProviderSupport
- SiriUIFoundation
- SiriVideoIntents
- SiriVideoUIFramework
- SleepHealthDaemonPlugin
- SleepWidgetUI
- SmartReplies
- SmartRepliesServer
- SmartRepliesUI
- SnippetCommands
- SnippetUI_Proto
- SoftPosReader
- SoftwareUpdateCoreConnect
- SonicFoundation
- SonicKit
- SoundScapesUtility
- SpatialAudioProfile
- SpeakTypingServices
- SpeechDetector
- SpeechRecognitionCommandServices
- SpeechRecognitionCore
- SpeechRecognitionSharedSupport
- SpeechTranslation
- SpokenNotificationsModule
- SportsKit
- SpotlightFoundation
- SpotlightReceiver
- SpotlightRecommendation
- SpringBoardIntents
- SpringBoardServices
- StickerFoundation
- StickerFoundationInternal
- StickerKitInternal
- StocksKit
- StopwatchModule
- StorageContainersPrivate
- StorageUI
- StoreServices
- StreamingAppleTrace
- StreamingExtractor
- Summaries
- SummariesHealthDaemon
- SwiftCertificate
- SwiftSQLite
- SwiftUICore
- SymptomAnalytics
- SymptomDistribution
- SymptomLinkAdvisory
- SymptomNetworkDiagnostics
- SymptomNetworkDiagnosticsCommon
- SymptomNetworkDiagnosticsCore
- SymptomPresentationFeed
- SymptomPresentationLite
- SymptomReporter
- SymptomShared
- SynapseSyncPlugin
- System
- SystemCustomization
- SystemPaperPresentation
- SystemStatus
- SystemVoiceAssistantServices
- TCCAuthorizationService
- TSApplication
- TSReading
- TVLatency
- TVUIKit
- TailspinSymbolication
- TailspinSymbolicationServer
- Tamale
- TeaCharts
- TeaDB
- TeaFoundation
- TeaSettings
- TeaSnappy
- TeaState
- TeaTemplate
- TelephonyRPC
- TelephonyTransferService
- TerminalToolKit
- TextEffectsCatalog
- TextFormattingUI
- TextInputCJK
- TextInputCore
- TextInputTestingKit
- TextInput_ar
- TextInput_bn
- TextInput_bo
- TextInput_ca
- TextInput_chr
- TextInput_de
- TextInput_el
- TextInput_emoji
- TextInput_en
- TextInput_es
- TextInput_fr
- TextInput_haw
- TextInput_he
- TextInput_hi
- TextInput_intl
- TextInput_ja
- TextInput_ko
- TextInput_mr
- TextInput_mul
- TextInput_my
- TextInput_nl
- TextInput_pa
- TextInput_pt
- TextInput_si
- TextInput_sl
- TextInput_ta
- TextInput_th
- TextInput_tr
- TextInput_ug
- TextInput_vi
- TextInput_yue
- TextInput_zh
- TextRecognition
- TextToSpeech
- TextToSpeechBundleSupport
- TextToSpeechKonaSupport
- TextToSpeechMauiSupport
- TextToSpeechVoiceBankingSupport
- TextToSpeechVoiceBankingUI
- TextUnderstanding
- TextUnderstandingFoundation
- TextUnderstandingShared
- ThreadNetwork
- ThumbnailsBlastDoorSupport
- TimeSync
- TimeZone
- TipKitServices
- TipsTryIt
- TipsUI
- TokenGeneration
- TokenGenerationCore
- TouchRemote
- Traffic
- Transfer
- TranslationAPISupport
- TranslationInference
- TranslationPersistence
- TranslationUI
- TranslationUIProvider
- TranslationUIServices
- TransparencyUI
- TrialProto
- Tungsten
- TypologyAccess
- UARPAssetManager
- UARPKit
- UARPUpdaterService
- UARPUpdaterServiceUSBPD
- UIFoundation
- UITriggerVC
- UIUtilities
- ULPNHeuristicsClientFramework
- URLFormatting
- USBHost
- USDLib_FormatLoaderProxy
- UnilogCoordination
- UnilogIngestion
- UnilogStreamAlgorithms
- UsageTracking
- UserActivity
- UserDomainConceptsSupport
- UserNotifications
- UserNotificationsServices
- UserNotificationsTranslation
- UserProfilesCore
- UserSafety
- UserSafetyUI
- VCH263.videodecoder
- VCH263.videoencoder
- VCPHEVC.videocodec
- VideoIntelligence
- VideoProcessing
- VirtualGarage
- VisualActionPrediction
- VisualActionPredictionCore
- VisualActionPredictionSupport
- VisualIntelligence
- VisualIntelligenceCoreDDSupport
- VisualMappingKit
- VisualVoicemail
- VoiceControl
- VoiceControlUI
- VoiceDial
- VoiceMemosModule
- VoiceShortcutsUICardKitProviderSupport
- WalletBlastDoorSupport
- WalletModule
- WatchConnectivity
- WatchControlAssets
- WebApp
- WebBookmarksNotificationPlugin
- WebBookmarksSwift
- WebSheet
- WelcomeKit
- WelcomeKitCore
- WidgetPreviewsExtensionAgent
- WidgetPreviewsShellPlugin
- WidgetPreviewsSupport
- WirelessCoexManager
- WirelessInsights
- WirelessProximity
- WritingTools
- XCTTargetBootstrap
- XPCDistributed
- XavierCore
- XavierNews
- YelpAccessPlugin
- \ No newline at end of file
- _AVKit_SwiftUI
- _AdAttributionKit_StoreKit
- _AppIntentsServices_AppIntents
- _AppIntentsServices_ToolKit
- _AppIntents_SwiftUI
- _AppIntents_UIKit
- _AuthenticationServices_SwiftUI
- _Coherence_CloudKit_Private
- _CommunicationsUICore_PosterBoardServices
- _CoreLocationUI_SwiftUI
- _CoreNFC_UIKit
- _DeviceActivity_SwiftUI
- _DeviceDiscoveryUI_SwiftUI
- _DeviceExpertIntents_AppIntents
- _GameController_SwiftUI
- _GeoServices_GeoToolbox
- _GeoToolbox_AppIntents
- _GeoToolbox_CoreLocation
- _HomeKit_SwiftUI
- _IconServices_SwiftUI
- _Intents_TipKit
- _JetUI_SwiftUI
- _LinkPresentation_AppIntents
- _LocationEssentials
- _MarketplaceKit_UIKit
- _MediaPlayer_AppIntents
- _MusicKitInternal_MediaPlaybackCore
- _MusicKitInternal_MediaPlayer
- _MusicKitInternal_SwiftUI
- _MusicKit_SwiftUI
- _OnDeviceStorage_JetEngine
- _PassKit_SwiftUI
- _PermissionKit_UIKit
- _PhotosUIPrivate_SwiftUI
- _PhotosUI_SwiftUI
- _PhotosUI_WidgetKit
- _Photos_AppIntents
- _QuickLook_SwiftUI
- _RealityKit_SwiftUI
- _SceneKit_SwiftUI
- _SecureElementCredential_SwiftUI
- _SecureElementCredential_UIKit
- _SonicKit_MusicKit
- _SonicKit_MusicKit_Packages
- _ToneKit_SwiftUI
- _ToolKit_AppIntents
- _Translation_SwiftUI
- _WebKit_SwiftUI
- accessoryupdaterd
- addressbooksyncd
- afcd
- amfid
- amsondevicestoraged
- anomalydetectiond
- apfs_boot_mount
- apfs_iosd
- appconduitd
- appleh16camerad
- audioclocksyncd
- backboardd
- biomesyncd
- bookdatastored
- cfprefsd
- ckdiscretionaryd
- cloudd
- cloudphotod
- com.apple.AGXFirmwareKextG18PRTBuddy (1)
- com.apple.AUC (1.0)
- com.apple.AppleFSCompression.AppleFSCompressionTypeZlib (1.0.0)
- com.apple.CallKit.CallDirectory
- com.apple.CallKit.CallDirectoryMaintenance
- com.apple.DeviceRecoveryBuiltinBrain
- com.apple.EXBrightCalibrationConsumer (1.0.0)
- com.apple.IOTextEncryptionFamily (1.0.0)
- com.apple.Siri.ActionPredictionNotifications
- com.apple.StreamingUnzipService
- com.apple.StreamingUnzipService.privileged
- com.apple.UIKit.KeyboardManagement
- com.apple.corelocation.locationUI
- com.apple.datamigrator
- com.apple.donotdisturb.private.smart-trigger
- com.apple.driver.AOPAudio2 (340.1)
- com.apple.driver.AOPTouchKext (313)
- com.apple.driver.ASIOKit
- com.apple.driver.AppleA7IOP (1.0.2)
- com.apple.driver.AppleA7IOP-ASCWrap-v6 (1.0.2)
- com.apple.driver.AppleALSColorSensor (1.0.0d1)
- com.apple.driver.AppleAOPAudio
- com.apple.driver.AppleARMPMU (1.0)
- com.apple.driver.AppleARMPlatform (1.0.2)
- com.apple.driver.AppleARMWatchdogTimer (1)
- com.apple.driver.AppleAVD
- com.apple.driver.AppleAstrisGpioProbe (1.0.1)
- com.apple.driver.AppleAudioClockLibs (540.3)
- com.apple.driver.AppleAuthCP (1.0.0)
- com.apple.driver.AppleDCPDPTXProxy (1.0.0)
- com.apple.driver.AppleDiagnosticDataAccessReadOnly (1.0.0)
- com.apple.driver.AppleDialogPMU (1.0.1)
- com.apple.driver.AppleDiskImages2
- com.apple.driver.AppleDisplayCrossbar (1.0.0)
- com.apple.driver.AppleDockChannel (1)
- com.apple.driver.AppleEffaceableBlockDevice (1.0)
- com.apple.driver.AppleEmbeddedLightSensor
- com.apple.driver.AppleFirmwareUpdateKext (1)
- com.apple.driver.AppleGPIOCanary (1.0.0)
- com.apple.driver.AppleGPIOICController (1.0.2)
- com.apple.driver.AppleGenericMultitouch (26.3)
- com.apple.driver.AppleH10PearlCameraInterface (22.303.0)
- com.apple.driver.AppleH16CameraInterface
- com.apple.driver.AppleH16PhotonDetector (1.0)
- com.apple.driver.AppleHIDALSService (1)
- com.apple.driver.AppleHIDKeyboard (9140.2)
- com.apple.driver.AppleHapticsSupportLEAP (10.16)
- com.apple.driver.AppleHapticsSupportNVM (10.16)
- com.apple.driver.AppleIDAMInterface (1)
- com.apple.driver.AppleIDV
- com.apple.driver.AppleIISController (540.4)
- com.apple.driver.AppleIOPADMAStream (340.7)
- com.apple.driver.AppleIPAppender (1.0)
- com.apple.driver.AppleInputDeviceSupport (9140.6)
- com.apple.driver.AppleInterruptControllerV3 (1.0.0d1)
- com.apple.driver.AppleLockdownMode (1)
- com.apple.driver.AppleM2ScalerCSCDriver (265.0.0)
- com.apple.driver.AppleM68Buttons (1.0.0d1)
- com.apple.driver.AppleMSG
- com.apple.driver.AppleMobileApNonce (1)
- com.apple.driver.AppleMobileDispH18P-DCP
- com.apple.driver.AppleMobileDispH18P-DCP (140.0)
- com.apple.driver.AppleMobileFileIntegrity (1.0.5)
- com.apple.driver.AppleNANDConfigAccess (1.0.0)
- com.apple.driver.AppleOnboardSerial (1.0)
- com.apple.driver.ApplePIODMA (1)
- com.apple.driver.ApplePearlSEPDriver (1)
- com.apple.driver.ApplePhoneBTM (1.0.1)
- com.apple.driver.ApplePhotonDetector (1.0)
- com.apple.driver.AppleProcessorTrace (1.0.0)
- com.apple.driver.AppleS5L8920XPWM (1.0.0d1)
- com.apple.driver.AppleS5L8940XI2C (1.0.0d2)
- com.apple.driver.AppleS5L8960XNCO (1)
- com.apple.driver.AppleSMC
- com.apple.driver.AppleSmartIO2
- com.apple.driver.AppleT8110DART (1)
- com.apple.driver.AppleT8130TypeCPhy (1)
- com.apple.driver.AppleT8150 (1)
- com.apple.driver.AppleT8150CLPC (1)
- com.apple.driver.AppleT8150MCC (1)
- com.apple.driver.AppleT8150PCIe (1)
- com.apple.driver.AppleThunderboltNHI
- com.apple.driver.AppleTriStar (1.0.0)
- com.apple.driver.AppleTypeCPhy (1)
- com.apple.driver.AppleTypeCPhyAUSBC (1)
- com.apple.driver.AppleUSBCardReader (562)
- com.apple.driver.AppleUSBDeviceMux
- com.apple.driver.AppleUSBDeviceMux (1.0.0d1)
- com.apple.driver.AppleUSBDeviceNCM (5.0.0)
- com.apple.driver.AppleUSBEthernetDevice (7.0)
- com.apple.driver.AudioDMACLLTEscalationDetector-T8150
- com.apple.driver.AudioDMAController-T8150
- com.apple.driver.AudioDMAFamily
- com.apple.driver.DiskImages
- com.apple.driver.DiskImages.UDIFDiskImage
- com.apple.driver.FairPlayIOKit
- com.apple.driver.IODARTFamily
- com.apple.driver.IOPAudioVoiceTriggerDevice
- com.apple.driver.RTBuddy
- com.apple.driver.usb.cdc.ncm (5.0.0)
- com.apple.driver.usb.ethernet.asix (5.0.0)
- com.apple.driver.usb.networking (5.0.0)
- com.apple.filesystems.lifs
- com.apple.filesystems.lifs (1)
- com.apple.filesystems.tmpfs (1)
- com.apple.iokit.AppleARMIISAudio (540.16)
- com.apple.iokit.IOAccessoryManager
- com.apple.iokit.IOCECFamily (1)
- com.apple.iokit.IOCryptoAcceleratorFamily (1.0.1)
- com.apple.iokit.IODisplayPortFamily (1.0.0)
- com.apple.iokit.IOHDCPFamily (1.0.0)
- com.apple.iokit.IOHIDEventDriver (2.0.0)
- com.apple.iokit.IOHIDEventDriverSafeBoot (2.0.0)
- com.apple.iokit.IONetworkingFamily
- com.apple.iokit.IOPCIFamily
- com.apple.iokit.IOSkywalkFamily
- com.apple.iokit.IOSlowAdaptiveClockingFamily (1.0.0)
- com.apple.iokit.IOStorageFamily
- com.apple.iokit.IOStorageFamily (2.1)
- com.apple.iokit.IOStreamFamily (1.1.0)
- com.apple.iokit.IOThunderboltFamily (9.3.3)
- com.apple.iokit.IOUSBDeviceFamily (2.0.0)
- com.apple.iokit.IOUSBHostFamily (1.2)
- com.apple.iokit.IOUSBMassStorageDriver (280)
- com.apple.kec.corecrypto
- com.apple.kec.pthread (1)
- com.apple.kext.AppleMatch (1.0.0d1)
- com.apple.kext.CoreTrust
- com.apple.kext.CoreTrust (1)
- com.apple.nke.l2tp
- com.apple.nke.l2tp (1.9)
- com.apple.nke.ppp (1.9)
- com.apple.security.AKSAnalytics (1)
- com.apple.security.AppleImage4 (7.0.0)
- com.apple.security.sandbox (300.0)
- companion_proxy
- companionappd
- companioncamerad
- companionmessagesd
- containermanagerd_system
- corerepaird
- dietappleh16camerad
- distnoted
- duetexpertd
- eapolclient
- eventkitsyncd
- fairplayd.H2
- fsck_exfat
- fsck_hfs
- geocorrectiond
- geod
- h18_ane_fw_apollo_v5x.im4p
- iCloud
- iCloudDriveFileProviderOverride
- iCloudDriveService
- iCloudSubscriptionOptimizerClient
- iCloudSubscriptionOptimizerLighthouse
- iCloudSubscriptionOptimizerPFLTraining
- iCloudWebSupport
- iMessageApps
- iTunesStore
- iTunesStoreFramework
- iboot_blob29.bin
- iboot_blob30.bin
- iboot_blob32.bin
- iboot_blob45.bin
- iboot_blob46.bin
- installcoordination_proxy
- installcoordinationd
- intelligenceplatformd
- itunesstored
- libATCommandStudioDynamic.dylib
- libAWDSupportFramework.dylib
- libAXSafeCategoryBundle.dylib
- libAXSpeechManager.dylib
- libAce3Updater.dylib
- libAppPatch.dylib
- libAppleArchive.dylib
- libAppleEXR.dylib
- libAppleTconUARPUpdater.dylib
- libAudioDSPCore.dylib
- libAudioStatistics.dylib
- libAudioToolboxUtility.dylib
- libBASupport.dylib
- libBBUpdaterDynamic_stubs.dylib
- libBIG5.dylib
- libBLAS.dylib
- libBasebandDiagnostics.dylib
- libBasebandSharedServices.dylib
- libCGInterfaces.dylib
- libCTGreenTeaLogger.dylib
- libCellularDecoders.dylib
- libCommCenterCNTargetData.dylib
- libCommCenterCommandDrivers.dylib
- libCommCenterMCommandDrivers.dylib
- libComposeFilters.dylib
- libCoreFP.dylib
- libCoreVMClient.dylib
- libDECHanyu.dylib
- libDECKanji.dylib
- libDHCPServer.A.dylib
- libETLDIAGLoggingDynamic.dylib
- libETLDLFDynamic.dylib
- libETLDLOADCoreDumpDynamic.dylib
- libETLDLOADDynamic.dylib
- libETLDMCDynamic.dylib
- libETLDynamic.dylib
- libETLEFSDumpDynamic.dylib
- libETLSAHDynamic.dylib
- libEUC.dylib
- libEUCTW.dylib
- libFDR.dylib
- libFDRDecode.dylib
- libGBK2K.dylib
- libGLProgrammability.dylib
- libGPUCompiler.dylib
- libHDLCDynamic.dylib
- libHZ.dylib
- libIOAccessoryManager.dylib
- libISO2022.dylib
- libJOHAB.dylib
- libLAPACK.dylib
- libLinearAlgebra.dylib
- libMSKanji.dylib
- libMTLCompilerHelper.dylib
- libMobileGestaltExtensions.dylib
- libNFC_Comet.dylib
- libNFC_HAL.dylib
- libPPMDataModel.dylib
- libPS190Updater.dylib
- libParallelCompression.dylib
- libQMIParserDynamic.dylib
- libReverseProxyDevice.dylib
- libSCLM.dylib
- libSLAMDynamic.dylib
- libSTS-N.dylib
- libSessionUtility.dylib
- libSoftwareUpdateSSO.dylib
- libSystemHealth.dylib
- libUES.dylib
- libUTF1632.dylib
- libUTF7.dylib
- libUTF8.dylib
- libUTF8MAC.dylib
- libVIQR.dylib
- libValidationCapsule.dylib
- libVibeSynthEngine.dylib
- libWISSupport.dylib
- libWebKitSwift.dylib
- libZW.dylib
- libZhuGeArmory.dylib
- libZhuGeRoster.dylib
- libamsupport.dylib
- libapple_nghttp2.dylib
- libbz2.1.0.dylib
- libccan.dylib
- libcharset.1.dylib
- libcupolicy.dylib
- libdispatch.dylib
- libdns_services.dylib
- libexslt.0.dylib
- libheimdal-asn1.dylib
- libibmad.dylib
- libibumad.dylib
- libibverbs.dylib
- libiconv.2.dylib
- libiconv_none.dylib
- libiconv_std.dylib
- libicucore.A.dylib
- libindus.dylib
- liblaunch.dylib
- libllvm-flatbuffers.dylib
- libllvm-lmdb.dylib
- liblockdown.dylib
- liblog_IOHIDFamily.dylib
- liblog_SystemConfiguration.dylib
- liblog_coreacc.dylib
- liblog_geo.dylib
- liblog_location.dylib
- liblog_mdns.dylib
- liblog_mdnsresponder.dylib
- liblog_network.dylib
- liblog_sonic.dylib
- liblog_srp.dylib
- libmacho.dylib
- libmapper_646.dylib
- libmapper_none.dylib
- libmapper_parallel.dylib
- libmapper_serial.dylib
- libmapper_std.dylib
- libmapper_zone.dylib
- libmav_ipc_router_dynamic.dylib
- libmdns.dylib
- libmecab.dylib
- libmecabra.dylib
- libmlx5.dylib
- libmrc.dylib
- libnfrestore.dylib
- libolaf.dylib
- libpartition2_dynamic.dylib
- libpmenergy.dylib
- libpmsample.dylib
- librxe.dylib
- libspindump.dylib
- libsqlite3.dylib
- libswiftAVFoundation.dylib
- libswiftAppleArchive.dylib
- libswiftAssetsLibrary.dylib
- libswiftCarPlay.dylib
- libswiftCore.dylib
- libswiftCoreAudio.dylib
- libswiftCoreAudio_Private.dylib
- libswiftCoreMedia.dylib
- libswiftCryptoTokenKit.dylib
- libswiftDarwin.dylib
- libswiftDataDetection.dylib
- libswiftDemangle.dylib
- libswiftDispatch.dylib
- libswiftDistributed.dylib
- libswiftExtensionFoundation.dylib
- libswiftExtensionKit.dylib
- libswiftFileProvider.dylib
- libswiftHealthKit.dylib
- libswiftMapKit.dylib
- libswiftMediaPlayer.dylib
- libswiftMetal.dylib
- libswiftObservation.dylib
- libswiftPassKit.dylib
- libswiftPhotos.dylib
- libswiftPhotosUI.dylib
- libswiftRegexBuilder.dylib
- libswiftSwiftOnoneSupport.dylib
- libswiftSynchronization.dylib
- libswiftSystem_Foundation.dylib
- libswiftUIKit.dylib
- libswiftUniformTypeIdentifiers.dylib
- libswiftVideoToolbox.dylib
- libswift_Builtin_float.dylib
- libswift_Concurrency.dylib
- libswift_DarwinFoundation1.dylib
- libswift_DarwinFoundation2.dylib
- libswift_DarwinFoundation3.dylib
- libswift_RegexParser.dylib
- libswift_StringProcessing.dylib
- libswift_Volatile.dylib
- libswift_errno.dylib
- libswift_math.dylib
- libswift_signal.dylib
- libswift_stdio.dylib
- libswift_time.dylib
- libswiftsys_time.dylib
- libswiftunistd.dylib
- libsysdiagnose.dylib
- libsystem_collections.dylib
- libsystem_configuration.dylib
- libsystem_coreservices.dylib
- libsystem_darwin.dylib
- libsystem_dnssd.dylib
- libsystem_platform.dylib
- libsystem_platform_debug.dylib
- libsystem_sanitizers.dylib
- libsystem_symptoms.dylib
- libsystem_trace_debug.dylib
- libsystem_trial.dylib
- libtailspin.dylib
- libtailspin_internal.dylib
- libusrtcp.dylib
- libvDSP.dylib
- libvMisc.dylib
- libxpc_datastores.dylib
- libz.1.dylib
- livefiles_cs.dylib
- livefiles_exfat.dylib
- locationd.events
- lockdownmoded
- logd_reporter
- mapspushd
- microstackshot
- nanoappregistryd
- nanomapscd
- nanomediaremotelinkagent
- navd
- newfs_apfs
- newsd
- nptocompaniond
- nsurlsessiond
- ospredictiond
- pairedunlockd
- peakpowermanagerd
- polarisd
- progressd
- resourcegrabberd
- securem3fw-v5x.im4p
- securityuploadd
- softwareupdated
- thermalmonitord
- uarpd
- useractivityd
- vImage
- vecLib
- vmd
- watchlistd
- wcd

</details>
