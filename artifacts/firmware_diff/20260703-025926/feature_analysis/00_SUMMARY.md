# Feature Analysis Summary — iOS 17.1

- **Total components in diff**: 3160  (**HIGH_SIGNAL**: 1876, **LOW_SIGNAL**: 1284)
- **Analysed** (report written): 98  |  **Apple Security Notes matches**: 58  |  **Suppressed TIER_3**: 2  |  **HIGH_SIGNAL not analysed** (budget/security filter): 1776

Tier shown is the LLM-assigned tier for analysed components, otherwise a deterministic estimate from the security score (4=Apple Security Notes, 3=hard indicator, 2=security vocabulary, 1=code change, 0=asset/UI/log).

## 🔴 Apple Security Notes matches — highest priority

| Component | Tier | Sec score | Apple Security Notes | Report |
|---|---|---|---|---|
| AppleProResHWDecoder.videodecoder | TIER_1 | 4 | `Pro Res` | [report](AppleProResHWDecoder.videodecoder_analysis.md) |
| AppleProResHWEncoder.videoencoder | TIER_1 | 4 | `Pro Res` | [report](AppleProResHWEncoder.videoencoder_analysis.md) |
| ContactsAutocomplete | TIER_1 | 4 | `Contacts` | [report](ContactsAutocomplete_analysis.md) |
| ContactsBackgroundColorService | TIER_1 | 4 | `Contacts` | [report](ContactsBackgroundColorService_analysis.md) |
| ContactsDonationFeedback | TIER_1 | 4 | `Contacts` | [report](ContactsDonationFeedback_analysis.md) |
| ContactsFlowDelegatePlugin | TIER_1 | 4 | `Contacts` | [report](ContactsFlowDelegatePlugin_analysis.md) |
| ContactsSettings | TIER_1 | 4 | `Contacts` | [report](ContactsSettings_analysis.md) |
| ContactsUI | TIER_1 | 4 | `Contacts` | [report](ContactsUI_analysis.md) |
| ContactsWidgetUI | TIER_1 | 4 | `Contacts` | [report](ContactsWidgetUI_analysis.md) |
| GameCenterAccountNotificationPlugin | TIER_1 | 4 | `Game Center` | [report](GameCenterAccountNotificationPlugin_analysis.md) |
| GameCenterUI | TIER_1 | 4 | `Game Center` | [report](GameCenterUI_analysis.md) |
| GameCenterUICore | TIER_1 | 4 | `Game Center` | [report](GameCenterUICore_analysis.md) |
| ImageIO | TIER_1 | 4 | `ImageIO` | [report](ImageIO_analysis.md) |
| NanoWeatherComplicationsCompanion | TIER_1 | 4 | `Weather` | [report](NanoWeatherComplicationsCompanion_analysis.md) |
| ProactiveShareSheetDataHarvestingLighthouse | TIER_1 | 4 | `Share Sheet` | [report](ProactiveShareSheetDataHarvestingLighthouse_analysis.md) |
| WeatherCore | TIER_1 | 4 | `Weather` | [report](WeatherCore_analysis.md) |
| WeatherKit | TIER_1 | 4 | `Weather` | [report](WeatherKit_analysis.md) |
| WeatherMaps | TIER_1 | 4 | `Weather` | [report](WeatherMaps_analysis.md) |
| com.apple.IOTextEncryptionFamily | TIER_1 | 4 | `IOTextEncryptionFamily` | [report](com.apple.IOTextEncryptionFamily_analysis.md) |
| com.apple.driver.AppleProResHW | TIER_1 | 4 | `Pro Res` | [report](com.apple.driver.AppleProResHW_analysis.md) |
| com.apple.kernel | TIER_1 | 4 | `Kernel` | [report](com.apple.kernel_analysis.md) |
| com.apple.security.sandbox | TIER_1 | 4 | `Sandbox` | [report](com.apple.security.sandbox_analysis.md) |
| libsystem_sandbox.dylib | TIER_1 | 4 | `Sandbox` | [report](libsystem_sandbox.dylib_analysis.md) |
| AutomationMode | TIER_2 | 4 | `Automation` | [report](AutomationMode_analysis.md) |
| ContactPhotoCarouselRemoteAlert | TIER_2 | 4 | `Contacts` | [report](ContactPhotoCarouselRemoteAlert_analysis.md) |
| Contacts | TIER_2 | 4 | `Contacts` | [report](Contacts_analysis.md) |
| ContactsFoundation | TIER_2 | 4 | `Contacts` | [report](ContactsFoundation_analysis.md) |
| ContactsUICore | TIER_2 | 4 | `Contacts` | [report](ContactsUICore_analysis.md) |
| FindMy | TIER_2 | 4 | `Find My` | [report](FindMy_analysis.md) |
| Game Center | TIER_2 | 4 | `Game Center` | [report](Game_Center_analysis.md) |
| GameCenterFoundation | TIER_2 | 4 | `Game Center` | [report](GameCenterFoundation_analysis.md) |
| GameCenterRemoteAlert | TIER_2 | 4 | `Game Center` | [report](GameCenterRemoteAlert_analysis.md) |
| HomeAutomationInternal | TIER_2 | 4 | `Automation` | [report](HomeAutomationInternal_analysis.md) |
| Photos | TIER_2 | 4 | `Photos` | [report](Photos_analysis.md) |
| RelevanceEngineWeather | TIER_2 | 4 | `Weather` | [report](RelevanceEngineWeather_analysis.md) |
| ShareSheet | TIER_2 | 4 | `Share Sheet` | [report](ShareSheet_analysis.md) |
| Siri | TIER_2 | 4 | `Siri` | [report](Siri_analysis.md) |
| SiriContactsIntents | TIER_2 | 4 | `Contacts` | [report](SiriContactsIntents_analysis.md) |
| Weather | TIER_2 | 4 | `Weather` | [report](Weather_analysis.md) |
| WeatherAnalytics | TIER_2 | 4 | `Weather` | [report](WeatherAnalytics_analysis.md) |
| WeatherDaemon | TIER_2 | 4 | `Weather` | [report](WeatherDaemon_analysis.md) |
| WeatherUI | TIER_2 | 4 | `Weather` | [report](WeatherUI_analysis.md) |
| libxpc.dylib | TIER_2 | 4 | `libxpc` | [report](libxpc.dylib_analysis.md) |
| mDNSResponder | TIER_2 | 4 | `mDNSResponder` | [report](mDNSResponder_analysis.md) |
| ContactsAutocompleteUI | TIER_3 | 4 | `Contacts` | [report](ContactsAutocompleteUI_analysis.md) |
| ContactsDonation | TIER_3 | 4 | `Contacts` | [report](ContactsDonation_analysis.md) |
| ContactsMetrics | TIER_3 | 4 | `Contacts` | [report](ContactsMetrics_analysis.md) |
| CoreRecents | TIER_3 | 4 | `Core Recents` | [report](CoreRecents_analysis.md) |
| GameCenterDashboardExtension | TIER_3 | 4 | `Game Center` | [report](GameCenterDashboardExtension_analysis.md) |
| GameCenterPrivateUIFramework | TIER_3 | 4 | `Game Center` | [report](GameCenterPrivateUIFramework_analysis.md) |
| GameCenterUIFramework | TIER_3 | 4 | `Game Center` | [report](GameCenterUIFramework_analysis.md) |
| GameCenterUIService | TIER_3 | 4 | `Game Center` | [report](GameCenterUIService_analysis.md) |
| NanoWeatherKitUICompanion | TIER_3 | 4 | `Weather` | [report](NanoWeatherKitUICompanion_analysis.md) |
| Safari | TIER_3 | 4 | `Safari` | [report](Safari_analysis.md) |
| SetupAssistant | TIER_3 | 4 | `Setup Assistant` | [report](SetupAssistant_analysis.md) |
| SetupAssistantUI | TIER_3 | 4 | `Setup Assistant` | [report](SetupAssistantUI_analysis.md) |
| WeatherComplications | TIER_3 | 4 | `Weather` | [report](WeatherComplications_analysis.md) |
| WebKit | TIER_3 | 4 | `WebKit` | [report](WebKit_analysis.md) |

## Analysed components (reports written)

<details><summary>Show 98 components</summary>

| Component | Tier | Sec score | Apple Security Notes | Report |
|---|---|---|---|---|
| AppleProResHWDecoder.videodecoder | TIER_1 | 4 | `Pro Res` | [report](AppleProResHWDecoder.videodecoder_analysis.md) |
| AppleProResHWEncoder.videoencoder | TIER_1 | 4 | `Pro Res` | [report](AppleProResHWEncoder.videoencoder_analysis.md) |
| ContactsAutocomplete | TIER_1 | 4 | `Contacts` | [report](ContactsAutocomplete_analysis.md) |
| ContactsBackgroundColorService | TIER_1 | 4 | `Contacts` | [report](ContactsBackgroundColorService_analysis.md) |
| ContactsDonationFeedback | TIER_1 | 4 | `Contacts` | [report](ContactsDonationFeedback_analysis.md) |
| ContactsFlowDelegatePlugin | TIER_1 | 4 | `Contacts` | [report](ContactsFlowDelegatePlugin_analysis.md) |
| ContactsSettings | TIER_1 | 4 | `Contacts` | [report](ContactsSettings_analysis.md) |
| ContactsUI | TIER_1 | 4 | `Contacts` | [report](ContactsUI_analysis.md) |
| ContactsWidgetUI | TIER_1 | 4 | `Contacts` | [report](ContactsWidgetUI_analysis.md) |
| GameCenterAccountNotificationPlugin | TIER_1 | 4 | `Game Center` | [report](GameCenterAccountNotificationPlugin_analysis.md) |
| GameCenterUI | TIER_1 | 4 | `Game Center` | [report](GameCenterUI_analysis.md) |
| GameCenterUICore | TIER_1 | 4 | `Game Center` | [report](GameCenterUICore_analysis.md) |
| ImageIO | TIER_1 | 4 | `ImageIO` | [report](ImageIO_analysis.md) |
| NanoWeatherComplicationsCompanion | TIER_1 | 4 | `Weather` | [report](NanoWeatherComplicationsCompanion_analysis.md) |
| ProactiveShareSheetDataHarvestingLighthouse | TIER_1 | 4 | `Share Sheet` | [report](ProactiveShareSheetDataHarvestingLighthouse_analysis.md) |
| WeatherCore | TIER_1 | 4 | `Weather` | [report](WeatherCore_analysis.md) |
| WeatherKit | TIER_1 | 4 | `Weather` | [report](WeatherKit_analysis.md) |
| WeatherMaps | TIER_1 | 4 | `Weather` | [report](WeatherMaps_analysis.md) |
| com.apple.IOTextEncryptionFamily | TIER_1 | 4 | `IOTextEncryptionFamily` | [report](com.apple.IOTextEncryptionFamily_analysis.md) |
| com.apple.driver.AppleProResHW | TIER_1 | 4 | `Pro Res` | [report](com.apple.driver.AppleProResHW_analysis.md) |
| com.apple.kernel | TIER_1 | 4 | `Kernel` | [report](com.apple.kernel_analysis.md) |
| com.apple.security.sandbox | TIER_1 | 4 | `Sandbox` | [report](com.apple.security.sandbox_analysis.md) |
| libsystem_sandbox.dylib | TIER_1 | 4 | `Sandbox` | [report](libsystem_sandbox.dylib_analysis.md) |
| ApplePencilDMServicePlugin | TIER_1 | 3 | — | [report](ApplePencilDMServicePlugin_analysis.md) |
| CommCenter | TIER_1 | 3 | — | [report](CommCenter_analysis.md) |
| CoreCDPInternal | TIER_1 | 3 | — | [report](CoreCDPInternal_analysis.md) |
| FinanceDaemon | TIER_1 | 3 | — | [report](FinanceDaemon_analysis.md) |
| Freeform | TIER_1 | 3 | — | [report](Freeform_analysis.md) |
| LighthouseBackground | TIER_1 | 3 | — | [report](LighthouseBackground_analysis.md) |
| MobileStoreDemoKit | TIER_1 | 3 | — | [report](MobileStoreDemoKit_analysis.md) |
| QuartzCore | TIER_1 | 3 | — | [report](QuartzCore_analysis.md) |
| com.apple.driver.AppleH11ANEInterface | TIER_1 | 3 | — | [report](com.apple.driver.AppleH11ANEInterface_analysis.md) |
| com.apple.iokit.IONetworkingFamily | TIER_1 | 3 | — | [report](com.apple.iokit.IONetworkingFamily_analysis.md) |
| com.apple.iokit.IOUserEthernet | TIER_1 | 3 | — | [report](com.apple.iokit.IOUserEthernet_analysis.md) |
| demod_helper | TIER_1 | 3 | — | [report](demod_helper_analysis.md) |
| dockaccessoryd | TIER_1 | 3 | — | [report](dockaccessoryd_analysis.md) |
| identityservicesd | TIER_1 | 3 | — | [report](identityservicesd_analysis.md) |
| mediaanalysisd | TIER_1 | 3 | — | [report](mediaanalysisd_analysis.md) |
| mlhostd | TIER_1 | 3 | — | [report](mlhostd_analysis.md) |
| spaceattributiond | TIER_1 | 3 | — | [report](spaceattributiond_analysis.md) |
| AutomationMode | TIER_2 | 4 | `Automation` | [report](AutomationMode_analysis.md) |
| ContactPhotoCarouselRemoteAlert | TIER_2 | 4 | `Contacts` | [report](ContactPhotoCarouselRemoteAlert_analysis.md) |
| Contacts | TIER_2 | 4 | `Contacts` | [report](Contacts_analysis.md) |
| ContactsFoundation | TIER_2 | 4 | `Contacts` | [report](ContactsFoundation_analysis.md) |
| ContactsUICore | TIER_2 | 4 | `Contacts` | [report](ContactsUICore_analysis.md) |
| FindMy | TIER_2 | 4 | `Find My` | [report](FindMy_analysis.md) |
| Game Center | TIER_2 | 4 | `Game Center` | [report](Game_Center_analysis.md) |
| GameCenterFoundation | TIER_2 | 4 | `Game Center` | [report](GameCenterFoundation_analysis.md) |
| GameCenterRemoteAlert | TIER_2 | 4 | `Game Center` | [report](GameCenterRemoteAlert_analysis.md) |
| HomeAutomationInternal | TIER_2 | 4 | `Automation` | [report](HomeAutomationInternal_analysis.md) |
| Photos | TIER_2 | 4 | `Photos` | [report](Photos_analysis.md) |
| RelevanceEngineWeather | TIER_2 | 4 | `Weather` | [report](RelevanceEngineWeather_analysis.md) |
| ShareSheet | TIER_2 | 4 | `Share Sheet` | [report](ShareSheet_analysis.md) |
| Siri | TIER_2 | 4 | `Siri` | [report](Siri_analysis.md) |
| SiriContactsIntents | TIER_2 | 4 | `Contacts` | [report](SiriContactsIntents_analysis.md) |
| Weather | TIER_2 | 4 | `Weather` | [report](Weather_analysis.md) |
| WeatherAnalytics | TIER_2 | 4 | `Weather` | [report](WeatherAnalytics_analysis.md) |
| WeatherDaemon | TIER_2 | 4 | `Weather` | [report](WeatherDaemon_analysis.md) |
| WeatherUI | TIER_2 | 4 | `Weather` | [report](WeatherUI_analysis.md) |
| libxpc.dylib | TIER_2 | 4 | `libxpc` | [report](libxpc.dylib_analysis.md) |
| mDNSResponder | TIER_2 | 4 | `mDNSResponder` | [report](mDNSResponder_analysis.md) |
| BooksUI | TIER_2 | 3 | — | [report](BooksUI_analysis.md) |
| CloudKit | TIER_2 | 3 | — | [report](CloudKit_analysis.md) |
| CoreAudio | TIER_2 | 3 | — | [report](CoreAudio_analysis.md) |
| Fitness | TIER_2 | 3 | — | [report](Fitness_analysis.md) |
| MessageProtection | TIER_2 | 3 | — | [report](MessageProtection_analysis.md) |
| MusicApplication | TIER_2 | 3 | — | [report](MusicApplication_analysis.md) |
| PeopleSuggester | TIER_2 | 3 | — | [report](PeopleSuggester_analysis.md) |
| Preferences | TIER_2 | 3 | — | [report](Preferences_analysis.md) |
| SoftwareUpdateServices | TIER_2 | 3 | — | [report](SoftwareUpdateServices_analysis.md) |
| UnifiedAssetFramework | TIER_2 | 3 | — | [report](UnifiedAssetFramework_analysis.md) |
| com.apple.driver.AppleAVD | TIER_2 | 3 | — | [report](com.apple.driver.AppleAVD_analysis.md) |
| com.apple.filesystems.apfs | TIER_2 | 3 | — | [report](com.apple.filesystems.apfs_analysis.md) |
| libpcap.A.dylib | TIER_2 | 3 | — | [report](libpcap.A.dylib_analysis.md) |
| locationd | TIER_2 | 3 | — | [report](locationd_analysis.md) |
| mediaanalysisd-service | TIER_2 | 3 | — | [report](mediaanalysisd-service_analysis.md) |
| nearbyd | TIER_2 | 3 | — | [report](nearbyd_analysis.md) |
| softwareupdateservicesd | TIER_2 | 3 | — | [report](softwareupdateservicesd_analysis.md) |
| HomeKitDaemon | TIER_2 | 2 | — | [report](HomeKitDaemon_analysis.md) |
| HomeKitDaemonLegacy | TIER_2 | 2 | — | [report](HomeKitDaemonLegacy_analysis.md) |
| MobileSpotlightIndex | TIER_2 | 2 | — | [report](MobileSpotlightIndex_analysis.md) |
| PhotoLibraryServices | TIER_2 | 2 | — | [report](PhotoLibraryServices_analysis.md) |
| PhotosUICore | TIER_2 | 2 | — | [report](PhotosUICore_analysis.md) |
| libgraphcompute-rt.dylib | TIER_2 | 2 | — | [report](libgraphcompute-rt.dylib_analysis.md) |
| ContactsAutocompleteUI | TIER_3 | 4 | `Contacts` | [report](ContactsAutocompleteUI_analysis.md) |
| ContactsDonation | TIER_3 | 4 | `Contacts` | [report](ContactsDonation_analysis.md) |
| ContactsMetrics | TIER_3 | 4 | `Contacts` | [report](ContactsMetrics_analysis.md) |
| CoreRecents | TIER_3 | 4 | `Core Recents` | [report](CoreRecents_analysis.md) |
| GameCenterDashboardExtension | TIER_3 | 4 | `Game Center` | [report](GameCenterDashboardExtension_analysis.md) |
| GameCenterPrivateUIFramework | TIER_3 | 4 | `Game Center` | [report](GameCenterPrivateUIFramework_analysis.md) |
| GameCenterUIFramework | TIER_3 | 4 | `Game Center` | [report](GameCenterUIFramework_analysis.md) |
| GameCenterUIService | TIER_3 | 4 | `Game Center` | [report](GameCenterUIService_analysis.md) |
| NanoWeatherKitUICompanion | TIER_3 | 4 | `Weather` | [report](NanoWeatherKitUICompanion_analysis.md) |
| Safari | TIER_3 | 4 | `Safari` | [report](Safari_analysis.md) |
| SetupAssistant | TIER_3 | 4 | `Setup Assistant` | [report](SetupAssistant_analysis.md) |
| SetupAssistantUI | TIER_3 | 4 | `Setup Assistant` | [report](SetupAssistantUI_analysis.md) |
| WeatherComplications | TIER_3 | 4 | `Weather` | [report](WeatherComplications_analysis.md) |
| WebKit | TIER_3 | 4 | `WebKit` | [report](WebKit_analysis.md) |

</details>

## HIGH_SIGNAL — analysed but suppressed (LLM rated TIER_3)

| Component | Tier | Sec score | Apple Security Notes | Report |
|---|---|---|---|---|
| Measure | TIER_3 | 3 | — | _suppressed (TIER_3)_ |
| watchdogd | TIER_3 | 3 | — | _suppressed (TIER_3)_ |

## HIGH_SIGNAL — flagged security-relevant but not analysed (551, over budget)

<details><summary>Show 551 components</summary>

| Component | Tier | Sec score | Apple Security Notes | Report |
|---|---|---|---|---|
| AAIDMSAccountNotificationPlugin | TIER_2 | 2 | — | _not analysed_ |
| AGXMetalG15 | TIER_2 | 2 | — | _not analysed_ |
| AIMLInstrumentationStreams | TIER_2 | 2 | — | _not analysed_ |
| AMSAccountAuthenticationPlugin | TIER_2 | 2 | — | _not analysed_ |
| ANECompilerService | TIER_2 | 2 | — | _not analysed_ |
| ANEStorageMaintainer | TIER_2 | 2 | — | _not analysed_ |
| APFS | TIER_2 | 2 | — | _not analysed_ |
| ASOctaneSupportXPCService | TIER_2 | 2 | — | _not analysed_ |
| AUDeveloperSettings | TIER_2 | 2 | — | _not analysed_ |
| AVConference | TIER_2 | 2 | — | _not analysed_ |
| AVD.videodecoder | TIER_2 | 2 | — | _not analysed_ |
| AVFAudio | TIER_2 | 2 | — | _not analysed_ |
| AVFCapture | TIER_2 | 2 | — | _not analysed_ |
| AVKit | TIER_2 | 2 | — | _not analysed_ |
| AXCoreUtilities | TIER_2 | 2 | — | _not analysed_ |
| AccessibilitySettings | TIER_2 | 2 | — | _not analysed_ |
| AccessibilityUtilities | TIER_2 | 2 | — | _not analysed_ |
| AccountsDaemon | TIER_2 | 2 | — | _not analysed_ |
| ActionButtonSelector | TIER_2 | 2 | — | _not analysed_ |
| ActionKit | TIER_2 | 2 | — | _not analysed_ |
| ActivityAchievementsUI | TIER_2 | 2 | — | _not analysed_ |
| ActivityAwardsClient | TIER_2 | 2 | — | _not analysed_ |
| AirPlayReceiver | TIER_2 | 2 | — | _not analysed_ |
| AirPlaySender | TIER_2 | 2 | — | _not analysed_ |
| AirPlaySenderUIApp | TIER_2 | 2 | — | _not analysed_ |
| AirPlaySupport | TIER_2 | 2 | — | _not analysed_ |
| Ambient | TIER_2 | 2 | — | _not analysed_ |
| AmbientSettings | TIER_2 | 2 | — | _not analysed_ |
| Announce | TIER_2 | 2 | — | _not analysed_ |
| AppSSO | TIER_2 | 2 | — | _not analysed_ |
| AppStore | TIER_2 | 2 | — | _not analysed_ |
| AppStoreComponents | TIER_2 | 2 | — | _not analysed_ |
| AppStoreKit | TIER_2 | 2 | — | _not analysed_ |
| AppStoreOverlays | TIER_2 | 2 | — | _not analysed_ |
| AppleAccount | TIER_2 | 2 | — | _not analysed_ |
| AppleAccountUI | TIER_2 | 2 | — | _not analysed_ |
| AppleIDSetup | TIER_2 | 2 | — | _not analysed_ |
| AppleIDSetupUI | TIER_2 | 2 | — | _not analysed_ |
| AppleLockdownMode | TIER_2 | 2 | — | _not analysed_ |
| AppleMIDIUSBDriver | TIER_2 | 2 | — | _not analysed_ |
| AppleMediaServices | TIER_2 | 2 | — | _not analysed_ |
| AppleMediaServicesUI | TIER_2 | 2 | — | _not analysed_ |
| AppleMediaServicesUIDynamicService | TIER_2 | 2 | — | _not analysed_ |
| AppleNeuralEngine | TIER_2 | 2 | — | _not analysed_ |
| AssetsLibrary | TIER_2 | 2 | — | _not analysed_ |
| AssistantServices | TIER_2 | 2 | — | _not analysed_ |
| AssistantUI | TIER_2 | 2 | — | _not analysed_ |
| AttentionAwareness | TIER_2 | 2 | — | _not analysed_ |
| AudioCodecs | TIER_2 | 2 | — | _not analysed_ |
| AudioFlowDelegatePlugin | TIER_2 | 2 | — | _not analysed_ |
| AudioSession | TIER_2 | 2 | — | _not analysed_ |
| AudioSessionServer | TIER_2 | 2 | — | _not analysed_ |
| AudioToolbox | TIER_2 | 2 | — | _not analysed_ |
| AuthKit | TIER_2 | 2 | — | _not analysed_ |
| AuthKitUIService | TIER_2 | 2 | — | _not analysed_ |
| AuthenticationServices | TIER_2 | 2 | — | _not analysed_ |
| AuthenticationServicesCore | TIER_2 | 2 | — | _not analysed_ |
| AutoFillCore | TIER_2 | 2 | — | _not analysed_ |
| AutoFillUI | TIER_2 | 2 | — | _not analysed_ |
| BiomeStreams | TIER_2 | 2 | — | _not analysed_ |
| BlastDoor | TIER_2 | 2 | — | _not analysed_ |
| BookStoreUI | TIER_2 | 2 | — | _not analysed_ |
| Books | TIER_2 | 2 | — | _not analysed_ |
| BrailleTranslation | TIER_2 | 2 | — | _not analysed_ |
| CDMFoundation | TIER_2 | 2 | — | _not analysed_ |
| CMCapture | TIER_2 | 2 | — | _not analysed_ |
| CMContinuityCaptureCore | TIER_2 | 2 | — | _not analysed_ |
| CMPhoto | TIER_2 | 2 | — | _not analysed_ |
| CPMS | TIER_2 | 2 | — | _not analysed_ |
| CSExattrCrypto | TIER_2 | 2 | — | _not analysed_ |
| CalendarDaemon | TIER_2 | 2 | — | _not analysed_ |
| CaptiveNetwork | TIER_2 | 2 | — | _not analysed_ |
| CaptiveNetworkSupport | TIER_2 | 2 | — | _not analysed_ |
| CarouselAppViewSettings | TIER_2 | 2 | — | _not analysed_ |
| CarouselLayoutSettings | TIER_2 | 2 | — | _not analysed_ |
| CarouselPreferenceServices | TIER_2 | 2 | — | _not analysed_ |
| ChatKit | TIER_2 | 2 | — | _not analysed_ |
| ChronoKit | TIER_2 | 2 | — | _not analysed_ |
| ChronoServices | TIER_2 | 2 | — | _not analysed_ |
| ChronoUIServices | TIER_2 | 2 | — | _not analysed_ |
| CipherML | TIER_2 | 2 | — | _not analysed_ |
| ClarityBoard | TIER_2 | 2 | — | _not analysed_ |
| ClarityFoundation | TIER_2 | 2 | — | _not analysed_ |
| ClockKit | TIER_2 | 2 | — | _not analysed_ |
| ClockPoster | TIER_2 | 2 | — | _not analysed_ |
| CloudAsset | TIER_2 | 2 | — | _not analysed_ |
| CloudDocsDaemon | TIER_2 | 2 | — | _not analysed_ |
| CloudKitDaemon | TIER_2 | 2 | — | _not analysed_ |
| CloudServices | TIER_2 | 2 | — | _not analysed_ |
| CloudSubscriptionFeatures | TIER_2 | 2 | — | _not analysed_ |
| CommCenterMobileHelper | TIER_2 | 2 | — | _not analysed_ |
| CommunicationsFilter | TIER_2 | 2 | — | _not analysed_ |
| CompanionAppBacklightPrivacySettings | TIER_2 | 2 | — | _not analysed_ |
| CompanionAppViewSetup | TIER_2 | 2 | — | _not analysed_ |
| CompanionAutoLaunchSettings | TIER_2 | 2 | — | _not analysed_ |
| CompanionDockSettings | TIER_2 | 2 | — | _not analysed_ |
| CompanionReturnToClockSettings | TIER_2 | 2 | — | _not analysed_ |
| CompanionStingSettings | TIER_2 | 2 | — | _not analysed_ |
| CompanionWakeSettings | TIER_2 | 2 | — | _not analysed_ |
| ContainerManagerCommon | TIER_2 | 2 | — | _not analysed_ |
| ContentKit | TIER_2 | 2 | — | _not analysed_ |
| ConversationKit | TIER_2 | 2 | — | _not analysed_ |
| CoordinationCore | TIER_2 | 2 | — | _not analysed_ |
| CopresenceCore | TIER_2 | 2 | — | _not analysed_ |
| CoreAnalytics | TIER_2 | 2 | — | _not analysed_ |
| CoreCDP | TIER_2 | 2 | — | _not analysed_ |
| CoreCDPUI | TIER_2 | 2 | — | _not analysed_ |
| CoreData | TIER_2 | 2 | — | _not analysed_ |
| CoreDuet | TIER_2 | 2 | — | _not analysed_ |
| CoreEmbeddedSpeechRecognition | TIER_2 | 2 | — | _not analysed_ |
| CoreGPSTest | TIER_2 | 2 | — | _not analysed_ |
| CoreGraphics | TIER_2 | 2 | — | _not analysed_ |
| CoreHAP | TIER_2 | 2 | — | _not analysed_ |
| CoreHandwriting | TIER_2 | 2 | — | _not analysed_ |
| CoreIDV | TIER_2 | 2 | — | _not analysed_ |
| CoreIDVShared | TIER_2 | 2 | — | _not analysed_ |
| CoreIDVUI | TIER_2 | 2 | — | _not analysed_ |
| CoreImage | TIER_2 | 2 | — | _not analysed_ |
| CoreLocation | TIER_2 | 2 | — | _not analysed_ |
| CoreMedia | TIER_2 | 2 | — | _not analysed_ |
| CoreMediaIO | TIER_2 | 2 | — | _not analysed_ |
| CoreMediaStream | TIER_2 | 2 | — | _not analysed_ |
| CoreMotion | TIER_2 | 2 | — | _not analysed_ |
| CoreNFC | TIER_2 | 2 | — | _not analysed_ |
| CoreNavigation | TIER_2 | 2 | — | _not analysed_ |
| CoreRealityIO | TIER_2 | 2 | — | _not analysed_ |
| CoreRoutine | TIER_2 | 2 | — | _not analysed_ |
| CoreSpeech | TIER_2 | 2 | — | _not analysed_ |
| CoreSpeechFoundation | TIER_2 | 2 | — | _not analysed_ |
| CoreSpotlight | TIER_2 | 2 | — | _not analysed_ |
| CoreSuggestions | TIER_2 | 2 | — | _not analysed_ |
| CoreSuggestionsInternals | TIER_2 | 2 | — | _not analysed_ |
| CoreSuggestionsUI | TIER_2 | 2 | — | _not analysed_ |
| CoreUARP | TIER_2 | 2 | — | _not analysed_ |
| CoreUtils | TIER_2 | 2 | — | _not analysed_ |
| CoreUtilsSwift | TIER_2 | 2 | — | _not analysed_ |
| CredentialProviderExtensionHelper | TIER_2 | 2 | — | _not analysed_ |
| DADaemonCardDAV | TIER_2 | 2 | — | _not analysed_ |
| DADaemonEAS | TIER_2 | 2 | — | _not analysed_ |
| DMCEnrollmentLibrary | TIER_2 | 2 | — | _not analysed_ |
| DMCEnrollmentProvider | TIER_2 | 2 | — | _not analysed_ |
| DMCUtilities | TIER_2 | 2 | — | _not analysed_ |
| DaemonUtils | TIER_2 | 2 | — | _not analysed_ |
| DesktopServicesPriv | TIER_2 | 2 | — | _not analysed_ |
| DeviceActivity | TIER_2 | 2 | — | _not analysed_ |
| DeviceIdentity | TIER_2 | 2 | — | _not analysed_ |
| DiagnosticExtensionsDaemon | TIER_2 | 2 | — | _not analysed_ |
| DiagnosticsReporter | TIER_2 | 2 | — | _not analysed_ |
| DockKitCore | TIER_2 | 2 | — | _not analysed_ |
| EmailDaemon | TIER_2 | 2 | — | _not analysed_ |
| EmailFoundation | TIER_2 | 2 | — | _not analysed_ |
| EmbeddedAcousticRecognition | TIER_2 | 2 | — | _not analysed_ |
| EmojiFoundation | TIER_2 | 2 | — | _not analysed_ |
| Espresso | TIER_2 | 2 | — | _not analysed_ |
| EventKit | TIER_2 | 2 | — | _not analysed_ |
| EventKitUI | TIER_2 | 2 | — | _not analysed_ |
| FTServices | TIER_2 | 2 | — | _not analysed_ |
| FaceTimeMessageStore | TIER_2 | 2 | — | _not analysed_ |
| FamilyCircle | TIER_2 | 2 | — | _not analysed_ |
| FamilyControlsObjC | TIER_2 | 2 | — | _not analysed_ |
| FeedbackCore | TIER_2 | 2 | — | _not analysed_ |
| FileProvider | TIER_2 | 2 | — | _not analysed_ |
| FileProviderDaemon | TIER_2 | 2 | — | _not analysed_ |
| FinanceKit | TIER_2 | 2 | — | _not analysed_ |
| FinanceKitUI | TIER_2 | 2 | — | _not analysed_ |
| FinanceUIService | TIER_2 | 2 | — | _not analysed_ |
| FindMyLocate | TIER_2 | 2 | — | _not analysed_ |
| FindMyUICore | TIER_2 | 2 | — | _not analysed_ |
| FontPickerUIService | TIER_2 | 2 | — | _not analysed_ |
| Foundation | TIER_2 | 2 | — | _not analysed_ |
| FrontBoard | TIER_2 | 2 | — | _not analysed_ |
| FrontBoardServices | TIER_2 | 2 | — | _not analysed_ |
| GPUToolsCapture | TIER_2 | 2 | — | _not analysed_ |
| GameController | TIER_2 | 2 | — | _not analysed_ |
| GeoServices | TIER_2 | 2 | — | _not analysed_ |
| GroupActivities | TIER_2 | 2 | — | _not analysed_ |
| HMAssistant | TIER_2 | 2 | — | _not analysed_ |
| Haptics | TIER_2 | 2 | — | _not analysed_ |
| HeadphoneConfigs | TIER_2 | 2 | — | _not analysed_ |
| HealthRecordsExtraction | TIER_2 | 2 | — | _not analysed_ |
| HealthRecordsUI | TIER_2 | 2 | — | _not analysed_ |
| HearingCore | TIER_2 | 2 | — | _not analysed_ |
| HearingUtilities | TIER_2 | 2 | — | _not analysed_ |
| HelpKit | TIER_2 | 2 | — | _not analysed_ |
| HomeAccessoryControlUI | TIER_2 | 2 | — | _not analysed_ |
| HomeDeviceSetup | TIER_2 | 2 | — | _not analysed_ |
| HomeEnergy | TIER_2 | 2 | — | _not analysed_ |
| HomeEnergyUI | TIER_2 | 2 | — | _not analysed_ |
| HomeKit | TIER_2 | 2 | — | _not analysed_ |
| HomeKitCore | TIER_2 | 2 | — | _not analysed_ |
| HomeKitMatter | TIER_2 | 2 | — | _not analysed_ |
| HomeKitMetrics | TIER_2 | 2 | — | _not analysed_ |
| IDS | TIER_2 | 2 | — | _not analysed_ |
| IDSFoundation | TIER_2 | 2 | — | _not analysed_ |
| IMDaemonCore | TIER_2 | 2 | — | _not analysed_ |
| IMSharedUtilities | TIER_2 | 2 | — | _not analysed_ |
| IMTranscoderAgent | TIER_2 | 2 | — | _not analysed_ |
| IO80211 | TIER_2 | 2 | — | _not analysed_ |
| IOHIDMotionEventSessionFilter | TIER_2 | 2 | — | _not analysed_ |
| IOKit | TIER_2 | 2 | — | _not analysed_ |
| ImageIOXPCService | TIER_2 | 2 | — | _not analysed_ |
| InstalledContentLibrary | TIER_2 | 2 | — | _not analysed_ |
| Intents | TIER_2 | 2 | — | _not analysed_ |
| JSApp | TIER_2 | 2 | — | _not analysed_ |
| JavaScriptCore | TIER_2 | 2 | — | _not analysed_ |
| LanguageModeling | TIER_2 | 2 | — | _not analysed_ |
| LinkMetadata | TIER_2 | 2 | — | _not analysed_ |
| LinkPresentation | TIER_2 | 2 | — | _not analysed_ |
| LinkServices | TIER_2 | 2 | — | _not analysed_ |
| LocalAuthentication | TIER_2 | 2 | — | _not analysed_ |
| MDM | TIER_2 | 2 | — | _not analysed_ |
| MDMClientLibrary | TIER_2 | 2 | — | _not analysed_ |
| MOVStreamIO | TIER_2 | 2 | — | _not analysed_ |
| MPSBenchmarkLoop | TIER_2 | 2 | — | _not analysed_ |
| MTLReplayController | TIER_2 | 2 | — | _not analysed_ |
| MailKit | TIER_2 | 2 | — | _not analysed_ |
| MailSupport | TIER_2 | 2 | — | _not analysed_ |
| MapKit | TIER_2 | 2 | — | _not analysed_ |
| Maps | TIER_2 | 2 | — | _not analysed_ |
| MapsSettings | TIER_2 | 2 | — | _not analysed_ |
| MapsSupport | TIER_2 | 2 | — | _not analysed_ |
| MapsUI | TIER_2 | 2 | — | _not analysed_ |
| MaterialKit | TIER_2 | 2 | — | _not analysed_ |
| Matter | TIER_2 | 2 | — | _not analysed_ |
| MechanismBase | TIER_2 | 2 | — | _not analysed_ |
| MediaAnalysis | TIER_2 | 2 | — | _not analysed_ |
| MediaControls | TIER_2 | 2 | — | _not analysed_ |
| MediaCoreUI | TIER_2 | 2 | — | _not analysed_ |
| MediaExperience | TIER_2 | 2 | — | _not analysed_ |
| MediaMiningKit | TIER_2 | 2 | — | _not analysed_ |
| MediaPlaybackCore | TIER_2 | 2 | — | _not analysed_ |
| MediaPlayer | TIER_2 | 2 | — | _not analysed_ |
| MediaRemote | TIER_2 | 2 | — | _not analysed_ |
| MediaToolbox | TIER_2 | 2 | — | _not analysed_ |
| Message | TIER_2 | 2 | — | _not analysed_ |
| MessageStoreToolKit | TIER_2 | 2 | — | _not analysed_ |
| Messages | TIER_2 | 2 | — | _not analysed_ |
| MessagesCloudSync | TIER_2 | 2 | — | _not analysed_ |
| MessagesFlowDelegatePlugin | TIER_2 | 2 | — | _not analysed_ |
| MetalTools | TIER_2 | 2 | — | _not analysed_ |
| MobileKeyBag | TIER_2 | 2 | — | _not analysed_ |
| MobileMail | TIER_2 | 2 | — | _not analysed_ |
| MobileMailUI | TIER_2 | 2 | — | _not analysed_ |
| MobileNotes | TIER_2 | 2 | — | _not analysed_ |
| MobileSafariSettings | TIER_2 | 2 | — | _not analysed_ |
| MobileTimerUI | TIER_2 | 2 | — | _not analysed_ |
| MultipeerConnectivity | TIER_2 | 2 | — | _not analysed_ |
| MusicKit | TIER_2 | 2 | — | _not analysed_ |
| MusicKitInternal | TIER_2 | 2 | — | _not analysed_ |
| MusicLibrary | TIER_2 | 2 | — | _not analysed_ |
| MusicScriptUpdateService | TIER_2 | 2 | — | _not analysed_ |
| MusicUI | TIER_2 | 2 | — | _not analysed_ |
| NLPLearner | TIER_2 | 2 | — | _not analysed_ |
| NanoCalendarBridgeSettings | TIER_2 | 2 | — | _not analysed_ |
| NanoCalendarComplicationsCompanion | TIER_2 | 2 | — | _not analysed_ |
| NanoCalendarPingSubscriber | TIER_2 | 2 | — | _not analysed_ |
| NanoMusicSync | TIER_2 | 2 | — | _not analysed_ |
| NanoPassKit | TIER_2 | 2 | — | _not analysed_ |
| NanoTimeKit | TIER_2 | 2 | — | _not analysed_ |
| NearField | TIER_2 | 2 | — | _not analysed_ |
| Network | TIER_2 | 2 | — | _not analysed_ |
| NetworkExtension | TIER_2 | 2 | — | _not analysed_ |
| NeutrinoCore | TIER_2 | 2 | — | _not analysed_ |
| NeutrinoKit | TIER_2 | 2 | — | _not analysed_ |
| NotesShared | TIER_2 | 2 | — | _not analysed_ |
| NotesSupport | TIER_2 | 2 | — | _not analysed_ |
| NotesUI | TIER_2 | 2 | — | _not analysed_ |
| OctagonTrust | TIER_2 | 2 | — | _not analysed_ |
| PDSAgent | TIER_2 | 2 | — | _not analysed_ |
| PHASE | TIER_2 | 2 | — | _not analysed_ |
| PairedUnlockSettings | TIER_2 | 2 | — | _not analysed_ |
| PaperBoardUI | TIER_2 | 2 | — | _not analysed_ |
| PaperKit | TIER_2 | 2 | — | _not analysed_ |
| PassKitCore | TIER_2 | 2 | — | _not analysed_ |
| PassKitUI | TIER_2 | 2 | — | _not analysed_ |
| Passbook | TIER_2 | 2 | — | _not analysed_ |
| PassbookSettings | TIER_2 | 2 | — | _not analysed_ |
| PasswordManagerUI | TIER_2 | 2 | — | _not analysed_ |
| PerfPowerMetricMonitor | TIER_2 | 2 | — | _not analysed_ |
| PersonalizationPortraitInternals | TIER_2 | 2 | — | _not analysed_ |
| PhoneCallFlowDelegatePlugin | TIER_2 | 2 | — | _not analysed_ |
| PhotoImaging | TIER_2 | 2 | — | _not analysed_ |
| PhotoLibrary | TIER_2 | 2 | — | _not analysed_ |
| PhotoLibraryServicesCore | TIER_2 | 2 | — | _not analysed_ |
| PhotosFormats | TIER_2 | 2 | — | _not analysed_ |
| PhotosGraph | TIER_2 | 2 | — | _not analysed_ |
| PhotosPlayer | TIER_2 | 2 | — | _not analysed_ |
| PhotosUI | TIER_2 | 2 | — | _not analysed_ |
| PhotosUIPrivate | TIER_2 | 2 | — | _not analysed_ |
| PlatformSSO | TIER_2 | 2 | — | _not analysed_ |
| Podcasts | TIER_2 | 2 | — | _not analysed_ |
| PodcastsFoundation | TIER_2 | 2 | — | _not analysed_ |
| PointerUIServices | TIER_2 | 2 | — | _not analysed_ |
| PosterBoardUIServices | TIER_2 | 2 | — | _not analysed_ |
| PowerUI | TIER_2 | 2 | — | _not analysed_ |
| PowerlogHelperdOperators | TIER_2 | 2 | — | _not analysed_ |
| PowerlogLiteOperators | TIER_2 | 2 | — | _not analysed_ |
| PreferencesFramework | TIER_2 | 2 | — | _not analysed_ |
| PrivacySettingsUI | TIER_2 | 2 | — | _not analysed_ |
| PrivateFederatedLearning | TIER_2 | 2 | — | _not analysed_ |
| Rapport | TIER_2 | 2 | — | _not analysed_ |
| RemindersUICore | TIER_2 | 2 | — | _not analysed_ |
| RequestDispatcherBridges | TIER_2 | 2 | — | _not analysed_ |
| SEService | TIER_2 | 2 | — | _not analysed_ |
| SMS | TIER_2 | 2 | — | _not analysed_ |
| STSXPCHelper | TIER_2 | 2 | — | _not analysed_ |
| SafariCore | TIER_2 | 2 | — | _not analysed_ |
| SafariFoundation | TIER_2 | 2 | — | _not analysed_ |
| SafariServices | TIER_2 | 2 | — | _not analysed_ |
| SafariShared | TIER_2 | 2 | — | _not analysed_ |
| SafetyMonitorApp | TIER_2 | 2 | — | _not analysed_ |
| SceneKit | TIER_2 | 2 | — | _not analysed_ |
| SearchFoundation | TIER_2 | 2 | — | _not analysed_ |
| SearchUI | TIER_2 | 2 | — | _not analysed_ |
| SecureTransactionService | TIER_2 | 2 | — | _not analysed_ |
| Security | TIER_2 | 2 | — | _not analysed_ |
| Seeding | TIER_2 | 2 | — | _not analysed_ |
| SessionSQL | TIER_2 | 2 | — | _not analysed_ |
| Setup | TIER_2 | 2 | — | _not analysed_ |
| SharedUtils | TIER_2 | 2 | — | _not analysed_ |
| Sharing | TIER_2 | 2 | — | _not analysed_ |
| ShortcutsUI | TIER_2 | 2 | — | _not analysed_ |
| ShortcutsViewService | TIER_2 | 2 | — | _not analysed_ |
| SidecarCore | TIER_2 | 2 | — | _not analysed_ |
| SidecarRelay | TIER_2 | 2 | — | _not analysed_ |
| SignalCompression | TIER_2 | 2 | — | _not analysed_ |
| SiriAnalytics | TIER_2 | 2 | — | _not analysed_ |
| SiriInformationSearch | TIER_2 | 2 | — | _not analysed_ |
| SiriInstrumentation | TIER_2 | 2 | — | _not analysed_ |
| SiriKitRuntime | TIER_2 | 2 | — | _not analysed_ |
| SiriPlaybackControlIntents | TIER_2 | 2 | — | _not analysed_ |
| SiriPlaybackControlSupport | TIER_2 | 2 | — | _not analysed_ |
| SiriRemembers | TIER_2 | 2 | — | _not analysed_ |
| SiriStates | TIER_2 | 2 | — | _not analysed_ |
| SiriTTS | TIER_2 | 2 | — | _not analysed_ |
| SiriUIFoundation | TIER_2 | 2 | — | _not analysed_ |
| SiriUtilities | TIER_2 | 2 | — | _not analysed_ |
| SiriVOX | TIER_2 | 2 | — | _not analysed_ |
| SocialLayer | TIER_2 | 2 | — | _not analysed_ |
| SoftPosReader | TIER_2 | 2 | — | _not analysed_ |
| SoftwareUpdateCore | TIER_2 | 2 | — | _not analysed_ |
| SoftwareUpdateSettingsUI | TIER_2 | 2 | — | _not analysed_ |
| SpaceAttribution | TIER_2 | 2 | — | _not analysed_ |
| SpeakerRecognition | TIER_2 | 2 | — | _not analysed_ |
| Speech | TIER_2 | 2 | — | _not analysed_ |
| SpotlightDaemon | TIER_2 | 2 | — | _not analysed_ |
| SpotlightServices | TIER_2 | 2 | — | _not analysed_ |
| SpringBoard | TIER_2 | 2 | — | _not analysed_ |
| SpringBoardFoundation | TIER_2 | 2 | — | _not analysed_ |
| SpringBoardHome | TIER_2 | 2 | — | _not analysed_ |
| SpringBoardServices | TIER_2 | 2 | — | _not analysed_ |
| StateReplicator | TIER_2 | 2 | — | _not analysed_ |
| StorageData | TIER_2 | 2 | — | _not analysed_ |
| StoreKit | TIER_2 | 2 | — | _not analysed_ |
| StoreKitUI | TIER_2 | 2 | — | _not analysed_ |
| StoreKitUIService | TIER_2 | 2 | — | _not analysed_ |
| SwiftUI | TIER_2 | 2 | — | _not analysed_ |
| SystemStatusUI | TIER_2 | 2 | — | _not analysed_ |
| TDGSharing | TIER_2 | 2 | — | _not analysed_ |
| TDGSharingViewService | TIER_2 | 2 | — | _not analysed_ |
| TVRemoteUIService | TIER_2 | 2 | — | _not analysed_ |
| TelephonyUI | TIER_2 | 2 | — | _not analysed_ |
| TelephonyUtilities | TIER_2 | 2 | — | _not analysed_ |
| TextInput | TIER_2 | 2 | — | _not analysed_ |
| TextInputCJK | TIER_2 | 2 | — | _not analysed_ |
| TextInputCore | TIER_2 | 2 | — | _not analysed_ |
| TextInputUI | TIER_2 | 2 | — | _not analysed_ |
| TextToSpeech | TIER_2 | 2 | — | _not analysed_ |
| Tips | TIER_2 | 2 | — | _not analysed_ |
| TipsCore | TIER_2 | 2 | — | _not analysed_ |
| TranslationUIServices | TIER_2 | 2 | — | _not analysed_ |
| Transparency | TIER_2 | 2 | — | _not analysed_ |
| TrialServer | TIER_2 | 2 | — | _not analysed_ |
| UARPUpdaterServiceLegacyAudio | TIER_2 | 2 | — | _not analysed_ |
| UIAccessibility | TIER_2 | 2 | — | _not analysed_ |
| UIFoundation | TIER_2 | 2 | — | _not analysed_ |
| UIKit | TIER_2 | 2 | — | _not analysed_ |
| UIKitCore | TIER_2 | 2 | — | _not analysed_ |
| UsageTrackingAgent | TIER_2 | 2 | — | _not analysed_ |
| UserNotificationsUIKit | TIER_2 | 2 | — | _not analysed_ |
| VectorKit | TIER_2 | 2 | — | _not analysed_ |
| VideoSubscriberAccount | TIER_2 | 2 | — | _not analysed_ |
| VideoSubscriberAccountUI | TIER_2 | 2 | — | _not analysed_ |
| VideosUI | TIER_2 | 2 | — | _not analysed_ |
| VisageHRTF | TIER_2 | 2 | — | _not analysed_ |
| Vision | TIER_2 | 2 | — | _not analysed_ |
| VisionKitCore | TIER_2 | 2 | — | _not analysed_ |
| VoiceMemos | TIER_2 | 2 | — | _not analysed_ |
| VoiceServices | TIER_2 | 2 | — | _not analysed_ |
| VoiceShortcutClient | TIER_2 | 2 | — | _not analysed_ |
| VoiceShortcuts | TIER_2 | 2 | — | _not analysed_ |
| VoiceTrigger | TIER_2 | 2 | — | _not analysed_ |
| WatchListKit | TIER_2 | 2 | — | _not analysed_ |
| WebContentRestrictions | TIER_2 | 2 | — | _not analysed_ |
| WebCore | TIER_2 | 2 | — | _not analysed_ |
| WebUI | TIER_2 | 2 | — | _not analysed_ |
| WiFiCloudSyncEngine | TIER_2 | 2 | — | _not analysed_ |
| WiFiKitUI | TIER_2 | 2 | — | _not analysed_ |
| WiFiPolicy | TIER_2 | 2 | — | _not analysed_ |
| WidgetRenderer | TIER_2 | 2 | — | _not analysed_ |
| WorkflowKit | TIER_2 | 2 | — | _not analysed_ |
| WorkflowUI | TIER_2 | 2 | — | _not analysed_ |
| WorkflowUIServices | TIER_2 | 2 | — | _not analysed_ |
| WorkoutUI | TIER_2 | 2 | — | _not analysed_ |
| XCTTargetBootstrap | TIER_2 | 2 | — | _not analysed_ |
| XOJIT | TIER_2 | 2 | — | _not analysed_ |
| XOJITExecutor | TIER_2 | 2 | — | _not analysed_ |
| YamahaUSBMIDIDriver | TIER_2 | 2 | — | _not analysed_ |
| _GroupActivities_UIKit | TIER_2 | 2 | — | _not analysed_ |
| _MusicKitInternal_SwiftUI | TIER_2 | 2 | — | _not analysed_ |
| _StoreKit_SwiftUI | TIER_2 | 2 | — | _not analysed_ |
| accessoryd | TIER_2 | 2 | — | _not analysed_ |
| agx_b000 | TIER_2 | 2 | — | _not analysed_ |
| akd | TIER_2 | 2 | — | _not analysed_ |
| amsaccountsd | TIER_2 | 2 | — | _not analysed_ |
| amsengagementd | TIER_2 | 2 | — | _not analysed_ |
| aned | TIER_2 | 2 | — | _not analysed_ |
| anomalydetectiond | TIER_2 | 2 | — | _not analysed_ |
| apfs_vol_converter | TIER_2 | 2 | — | _not analysed_ |
| appleaccountd | TIER_2 | 2 | — | _not analysed_ |
| appstored | TIER_2 | 2 | — | _not analysed_ |
| apsd | TIER_2 | 2 | — | _not analysed_ |
| askpermissiond | TIER_2 | 2 | — | _not analysed_ |
| assistantd | TIER_2 | 2 | — | _not analysed_ |
| audioaccessoryd | TIER_2 | 2 | — | _not analysed_ |
| backgroundassets.user | TIER_2 | 2 | — | _not analysed_ |
| bluetoothd | TIER_2 | 2 | — | _not analysed_ |
| bookdatastored | TIER_2 | 2 | — | _not analysed_ |
| callservicesd | TIER_2 | 2 | — | _not analysed_ |
| captiveagent | TIER_2 | 2 | — | _not analysed_ |
| cloudd | TIER_2 | 2 | — | _not analysed_ |
| com.apple.AGXG15P | TIER_2 | 2 | — | _not analysed_ |
| com.apple.DriverKit-AppleBCMWLAN | TIER_2 | 2 | — | _not analysed_ |
| com.apple.MobileInstallationHelperService | TIER_2 | 2 | — | _not analysed_ |
| com.apple.SharePlay.NearbyInvitationsService | TIER_2 | 2 | — | _not analysed_ |
| com.apple.StreamingUnzipService | TIER_2 | 2 | — | _not analysed_ |
| com.apple.StreamingUnzipService.privileged | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleAVE2 | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleBasebandPCI | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleH13CameraInterface | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleLockdownMode | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleM2ScalerCSCDriver | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleM68Buttons | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleMobileFileIntegrity | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.ApplePhotonDetector | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleSARService | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleSEPCredentialManager | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleSEPKeyStore | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleSMC | TIER_2 | 2 | — | _not analysed_ |
| com.apple.driver.AppleSPMIPMU | TIER_2 | 2 | — | _not analysed_ |
| com.apple.filesystems.lifs | TIER_2 | 2 | — | _not analysed_ |
| com.apple.iokit.IOPCIFamily | TIER_2 | 2 | — | _not analysed_ |
| com.apple.kec.corecrypto | TIER_2 | 2 | — | _not analysed_ |
| com.apple.quicklook.ThumbnailsAgent | TIER_2 | 2 | — | _not analysed_ |
| com.apple.sbd | TIER_2 | 2 | — | _not analysed_ |
| com.apple.security.AppleImage4 | TIER_2 | 2 | — | _not analysed_ |
| com.apple.telemetry | TIER_2 | 2 | — | _not analysed_ |
| coreidvd | TIER_2 | 2 | — | _not analysed_ |
| corespeechd | TIER_2 | 2 | — | _not analysed_ |
| cryptexd | TIER_2 | 2 | — | _not analysed_ |
| ctkd | TIER_2 | 2 | — | _not analysed_ |
| demod | TIER_2 | 2 | — | _not analysed_ |
| diagnosticd | TIER_2 | 2 | — | _not analysed_ |
| diskarbitrationd | TIER_2 | 2 | — | _not analysed_ |
| driverkitd | TIER_2 | 2 | — | _not analysed_ |
| druid | TIER_2 | 2 | — | _not analysed_ |
| dyld | TIER_2 | 2 | — | _not analysed_ |
| findmylocated | TIER_2 | 2 | — | _not analysed_ |
| fsck_apfs | TIER_2 | 2 | — | _not analysed_ |
| gamed | TIER_2 | 2 | — | _not analysed_ |
| gpsd | TIER_2 | 2 | — | _not analysed_ |
| iCloudDriveCore | TIER_2 | 2 | — | _not analysed_ |
| iCloudQuota | TIER_2 | 2 | — | _not analysed_ |
| iCloudQuotaUI | TIER_2 | 2 | — | _not analysed_ |
| iMessage | TIER_2 | 2 | — | _not analysed_ |
| iTunesCloud | TIER_2 | 2 | — | _not analysed_ |
| icloudmailagent | TIER_2 | 2 | — | _not analysed_ |
| idcredd | TIER_2 | 2 | — | _not analysed_ |
| imagent | TIER_2 | 2 | — | _not analysed_ |
| installcoordination_proxy | TIER_2 | 2 | — | _not analysed_ |
| installcoordinationd | TIER_2 | 2 | — | _not analysed_ |
| itunescloudd | TIER_2 | 2 | — | _not analysed_ |
| keybagd | TIER_2 | 2 | — | _not analysed_ |
| launchd | TIER_2 | 2 | — | _not analysed_ |
| libAudioDSP.dylib | TIER_2 | 2 | — | _not analysed_ |
| libBasebandManager.dylib | TIER_2 | 2 | — | _not analysed_ |
| libBasebandManagerICE.dylib | TIER_2 | 2 | — | _not analysed_ |
| libFDR.dylib | TIER_2 | 2 | — | _not analysed_ |
| libGPUCompilerImplLazy.dylib | TIER_2 | 2 | — | _not analysed_ |
| libGPUCompilerUtils.dylib | TIER_2 | 2 | — | _not analysed_ |
| libIOAccessoryManager.dylib | TIER_2 | 2 | — | _not analysed_ |
| libSessionUtility.dylib | TIER_2 | 2 | — | _not analysed_ |
| libchannel.dylib | TIER_2 | 2 | — | _not analysed_ |
| libcorecrypto.dylib | TIER_2 | 2 | — | _not analysed_ |
| libcorecrypto_noasm.dylib | TIER_2 | 2 | — | _not analysed_ |
| libcorecrypto_trace.dylib | TIER_2 | 2 | — | _not analysed_ |
| libcoreroutine.dylib | TIER_2 | 2 | — | _not analysed_ |
| libcryptex.dylib | TIER_2 | 2 | — | _not analysed_ |
| libcryptex_core.dylib | TIER_2 | 2 | — | _not analysed_ |
| libcryptex_interface.dylib | TIER_2 | 2 | — | _not analysed_ |
| libcryptex_trampoline.dylib | TIER_2 | 2 | — | _not analysed_ |
| libfire7.dylib | TIER_2 | 2 | — | _not analysed_ |
| libiconv_std.dylib | TIER_2 | 2 | — | _not analysed_ |
| libimg4.dylib | TIER_2 | 2 | — | _not analysed_ |
| liblog_location.dylib | TIER_2 | 2 | — | _not analysed_ |
| libmdns.dylib | TIER_2 | 2 | — | _not analysed_ |
| libmobileassetd.dylib | TIER_2 | 2 | — | _not analysed_ |
| libnetworkextension.dylib | TIER_2 | 2 | — | _not analysed_ |
| libsqlite3.dylib | TIER_2 | 2 | — | _not analysed_ |
| libsystem_c_debug.dylib | TIER_2 | 2 | — | _not analysed_ |
| libsystem_containermanager.dylib | TIER_2 | 2 | — | _not analysed_ |
| libsystem_networkextension.dylib | TIER_2 | 2 | — | _not analysed_ |
| libusd_ms.dylib | TIER_2 | 2 | — | _not analysed_ |
| lifs | TIER_2 | 2 | — | _not analysed_ |
| logd | TIER_2 | 2 | — | _not analysed_ |
| logd_helper | TIER_2 | 2 | — | _not analysed_ |
| maild | TIER_2 | 2 | — | _not analysed_ |
| mediaremoted | TIER_2 | 2 | — | _not analysed_ |
| merchantd | TIER_2 | 2 | — | _not analysed_ |
| mmaintenanced | TIER_2 | 2 | — | _not analysed_ |
| mobileactivationd | TIER_2 | 2 | — | _not analysed_ |
| momentsd | TIER_2 | 2 | — | _not analysed_ |
| mstreamd | TIER_2 | 2 | — | _not analysed_ |
| ndoagent | TIER_2 | 2 | — | _not analysed_ |
| nesessionmanager | TIER_2 | 2 | — | _not analysed_ |
| networkserviceproxy | TIER_2 | 2 | — | _not analysed_ |
| nfcd | TIER_2 | 2 | — | _not analysed_ |
| otctl | TIER_2 | 2 | — | _not analysed_ |
| passd | TIER_2 | 2 | — | _not analysed_ |
| promotedcontentd | TIER_2 | 2 | — | _not analysed_ |
| rapportd | TIER_2 | 2 | — | _not analysed_ |
| revisiond | TIER_2 | 2 | — | _not analysed_ |
| safetyalertsd | TIER_2 | 2 | — | _not analysed_ |
| scrod | TIER_2 | 2 | — | _not analysed_ |
| searchpartyd | TIER_2 | 2 | — | _not analysed_ |
| securityd | TIER_2 | 2 | — | _not analysed_ |
| seserviced | TIER_2 | 2 | — | _not analysed_ |
| sharingd | TIER_2 | 2 | — | _not analysed_ |
| shazamd | TIER_2 | 2 | — | _not analysed_ |
| softposreaderd | TIER_2 | 2 | — | _not analysed_ |
| speechmodeltrainingd | TIER_2 | 2 | — | _not analysed_ |
| storekitd | TIER_2 | 2 | — | _not analysed_ |
| tccd | TIER_2 | 2 | — | _not analysed_ |
| transparencyd | TIER_2 | 2 | — | _not analysed_ |
| trustd | TIER_2 | 2 | — | _not analysed_ |
| usermanagerd | TIER_2 | 2 | — | _not analysed_ |
| voicememod | TIER_2 | 2 | — | _not analysed_ |
| wifianalyticsd | TIER_2 | 2 | — | _not analysed_ |
| wifid | TIER_2 | 2 | — | _not analysed_ |
| wifip2pd | TIER_2 | 2 | — | _not analysed_ |
| xpcproxy | TIER_2 | 2 | — | _not analysed_ |

</details>

## HIGH_SIGNAL — excluded, low/no security relevance (1225)

<details><summary>Show 1225 components</summary>

- AAAFoundation
- AADataclassEnableNotificationPlugin
- ABMHelper
- ACCBaker
- ACTFramework
- AEBookPlugins
- AGXCompilerCore
- AMSAccountSyncNotificationPlugin
- ANECompiler
- ANEServices
- APTransport
- ARKit
- ARTraceModule
- ASMessagesProvider
- ASPCarryLog
- AUSettings
- AVAudioDeviceTestService
- AVFCore
- AVFoundation
- AXActionSheetUIServer
- AXAssetAndDataServer
- AXBuddyBundle
- AXElementInteraction
- AXFrontBoardUtils
- AXIDSServices
- AXMediaUtilities
- AXRuntime
- AXSoundDetection
- AXSoundDetectionUI
- AXSpeechAssetServices
- AXSpringBoardServerInstance
- AXTapToSpeakTime
- AXWatchRemoteScreenUI
- AccessibilityPhysicalInteraction
- AccessibilityPlatformTranslation
- AccessibilitySettingsLoader
- AccessibilitySharedSupport
- AccessibilitySharedUISupport
- AccessibilityUI
- AccessibilityUIService
- AccessibilityUIUtilities
- AccessoryBLEPairing
- AccessoryDeveloperSettings
- Accounts
- AccountsUI
- AcousticId-Assistant
- ActionButtonConfigurationUI
- ActionButtonSettings
- ActionKitUI
- ActionPredictionHeuristicsInternal
- ActiveSyncSettings
- ActivityBridgeSetup
- ActivityKit
- ActivityRingsUI
- ActivitySharing
- ActivitySharingClient
- ActivityUIServices
- AddressBook-Assistant
- AddressBookLegacy
- AddressBookUIFramework
- AirDrop
- AirDropUI
- AirPlayMirroringModule
- AirPlayReceiverKit
- AirPlaySenderUI
- AirPortSettings
- AirTrafficSettings
- AlarmFlowPlugin
- AmbientUI
- Animoji
- AnnotationKit
- AnnounceDaemon
- AppAnalytics
- AppConduit
- AppInstallExtension
- AppIntents
- AppNotificationsLoggingClient
- AppPredictionClient
- AppPredictionInternal
- AppPredictionUI
- AppPredictionUIWidget
- AppServerSupport
- AppStoreKitInternal
- AppearanceModule
- AppleAVE2FW_H15.im4p
- AppleAccountSettings
- AppleBasebandManager
- AppleBasebandServices
- AppleCV3D
- AppleCV3DMOVKit
- AppleCredentialManagerDaemon
- AppleDepth
- AppleDepthCore
- AppleEmbeddedAccessoryUpdaterService
- AppleMCTF
- AppleMediaServicesUIDynamic
- AppleMediaServicesUIPaymentSheets
- AppleMobileFileIntegrity
- ApplePencilSessionFilter
- AppleProxServiceFilter
- ApplePushService
- AppleServiceToolkit
- AppleTV
- AppleVideoEncoder
- Arcade
- AssetExplorer
- AssetViewer
- AssistantSettingsSupport
- AttributionWeeApp
- Audio-QuickLook
- AudioAnalyticsExternal
- AudioServerDriver
- AudiogramIngestion
- AuthKitUI
- AutoBugCaptureCore
- AvatarKit
- AvatarPickerMemojiPicker
- AvatarUI
- BKAudiobooks
- BKLibrary
- BPSStingSetup
- BTAudioHALPlugin
- BTLEServer
- BackBoard
- BackgroundAssets
- BackgroundShortcutRunner
- BackgroundSystemTasks
- BacklightServicesHost
- BannerKit
- BarcodeScanner
- BaseBoard
- BaseBoardUI
- BasebandTraceHelper
- BatteryCenterUI
- BatteryUsageUI
- BatteryWidget
- BiomeFoundation
- BiomeLibrary
- BiomeStorage
- BiometricKit
- BiometricKitUI
- BlissReader
- BlueTool
- BluetoothManager
- BluetoothSettings
- BluetoothUIService
- BookAnalytics
- BookCore
- BookDataStore
- BookEPUB
- BookFoundation
- BookLibraryCore
- BookUtility
- BooksPersonalization
- BrailleNBSC
- Bridge
- BridgePreferences
- BridgeStoreExtension
- BulletinBoard
- BulletinDistributorCompanion
- Business
- BusinessChat
- BusinessChatFramework
- CAMRootFlowPlugin
- CARDNDUI
- CFNetwork
- CMCaptureCore
- CMImaging
- CSExattrCryptoService
- Calculator
- Calendar-Assistant
- CalendarDatabase
- CalendarFoundation
- CalendarMigration
- CalendarNotification
- CalendarUIKit
- CalendarWidget
- CallHistory
- Camera
- CameraColorProcessing
- CameraEditKitFramework
- CameraEffectsKit
- CameraKit
- CameraUI
- CarCommandsFlowDelegatePlugin
- CarKitNavigation
- CarModeModule
- CarPlay
- CarPlayHalogen
- CarPlaySettings
- CarPlaySupport
- CarPlayUI
- CarPlayUIServices
- CardKit
- Cards
- Categories
- CertInfo
- ChargingViewService
- Charts
- ChatKitAssistantUI-Assistant
- ChatKitFramework
- CheckerBoard
- CheckerBoardRemoteSetup
- ChronoCore
- Ciconia
- CinematicFraming
- ClarityBoardFoundation
- ClarityCamera
- ClarityPhotos
- ClarityUIMusicSettings
- ClarityUIPhoneFaceTimeSettings
- ClarityUIPhotosSettings
- ClarityUIServer
- ClipUIServices
- ClockAngel
- CloudDocs
- CloudPhotoLibrary
- CloudPhotoServices
- CloudRecommendation
- CloudSharingUI
- Coherence
- ColorPickerUIService
- ColorSync
- CommonUtilities
- CommunicationsSetupUI
- CompanionInternationalSettings
- Compass
- CompassViewCalibrationService
- ComplicationDisplay
- ConnectivityModule
- ContactlessReaderUI
- ContextSync
- ContextualSuggestionClient
- ContextualUnderstanding
- ContinuityDisplay
- ControlCenterServices
- ControlCenterUI
- ControlCenterUIKit
- Coordination
- CoreAccessories
- CoreAuthUI
- CoreAutoLayout
- CoreBluetooth
- CoreBrightness
- CoreDAV
- CoreEmoji
- CoreFollowUp
- CoreFollowUpUI
- CoreFoundation
- CoreIDVPAD
- CoreIDVRGBLiveness
- CoreIndoor
- CoreML
- CoreMotionAlgorithms
- CoreOC
- CoreODI
- CoreODIEssentials
- CorePhotogrammetry
- CoreRE
- CoreRecognition
- CoreSVG
- CoreTelephony
- CoreText
- CoreThreadCommissionerServiced
- CoreTransferable
- CoreUI
- CoreUtilsExtras
- CoreVideo
- CoreWiFi
- CoverSheet
- CoverSheetKit
- Coverage Details
- CryptoTokenKit
- DACalDAV
- DADaemonIMAPNotes
- DADaemonSupport
- DDActionsService
- DKPairingUIService
- DOT Driver
- DPSubmissionService
- DashBoard
- DeepThought
- DeepThoughtBiomeFoundation
- DefaultMediaPlayer-QuickLook
- DepthCompanionSettings
- DepthComplicationBundleCompanion
- DepthCore
- DeveloperSettings
- DeveloperToolsSupport
- DeviceActivityConductor
- DeviceDiscoveryUICore
- DiagnosticExtensions
- DiagnosticRequestService
- Diagnostics
- DiagnosticsReporterServices
- DialogEngine
- DictionarySettings
- DigitalSeparationSettings
- DigitalSeparationUI
- DigitalTouchBalloonProvider
- DigitalTouchShared
- DisembarkUI
- DiskImages2
- DisplayAndBrightnessSettings
- DisplayModule
- DistributedEvaluation
- DoNotDisturbModule
- DoNotDisturbServer
- DoNotDisturbSettings
- DockKit
- DocumentCamera
- DocumentManager
- DocumentManagerExecutables
- DocumentManagerUICore
- DrawingKit
- DriverKit
- DualSenseHIDServicePlugin
- DualShock4HIDServicePlugin
- DuetActivityScheduler
- DumpPanic
- Duxbury
- EAP8021X
- EAUpdaterService
- Email
- EmojiKit
- EngagementCollector
- EnhancedLoggingState
- Eurobraille
- EventKitUIFramework
- ExposureNotificationSettingsUI
- FMFCore
- FMFUI
- FMFindingUI
- FaceTime
- FacebookSettings
- Family
- FamilyCircleUI
- FamilyControls
- FamilyControlsAgent
- FamilyControlsAuthenticationUI
- FeatureStore
- Feedback
- Feedback Assistant iOS
- FeedbackService
- Files
- FilesystemMetadataSnapshotService
- FindMyBase
- FindMyMessaging
- FindMyNotificationsSettings
- FitnessApp
- FitnessCoachingHealthServices
- FitnessCoachingServices
- FitnessUI
- FlashlightModule
- FlightUtilities
- Focus
- FocusSettings
- FocusSettingsUI
- FocusUI
- FocusUIModule
- FontPicker
- FreeformDataclassOwner
- FreeformSettings
- GAXBackboardServer
- GAXSpringboardServer
- GPUTools
- GPUToolsTransport
- Gambit
- GameControllerFoundation
- GameKitFramework
- GeneralKnowledge-Assistant
- GeneralSettingsUI
- GenericGamepadHIDServicePlugin
- GeoFlowDelegatePlugin
- Gif-QuickLook
- GridDataServices
- H13ISP.mediacapture
- H264H9.videoencoder
- H9.videoencoder
- HDSViewService
- HMFoundation
- HRTFEnrollmentService
- HandwritingProvider
- HandyTech
- HashtagImagesExtension
- HeadphoneSettings
- Health
- HealthArticlesUI
- HealthBridgePrivacySettings
- HealthDaemon
- HealthDataclassOwnerPlugin
- HealthExperience
- HealthExperienceUI
- HealthExposureNotificationUI
- HealthFeaturesBridgeSetupPlugin
- HealthKit
- HealthKitUI
- HealthMedicationsUI
- HealthPlatform
- HealthPlatformCore
- HealthRecordServices
- HealthRecords
- HealthRecordsPlugin
- HealthRecordsWalletSupport
- HealthSafety
- HealthToolbox
- HealthUI
- HealthVisualization
- HearingAidUIServer
- HearingAidsModule
- HearingApp
- HearingAppPlugin
- HearingSettings
- HearingUI
- Heart
- HeartHealthDaemon
- HeartRhythmUI
- Home
- HomeAI
- HomeControlCenterCompactModule
- HomeControlCenterModule
- HomeDataModel
- HomeEnergyDaemon
- HomeKitEventRouter
- HomeKitEvents
- HomeMessagingUtils
- HomePodSettings
- HomeSettings
- HomeUI
- HomeUIService
- HoverTextUI
- IMAVCore
- IMAssistantCore
- IMCore
- IMDPersistence
- IMFoundation
- IMTranscoding
- IMTransferServices
- IOAccessoryManager
- IOAnalytics
- IOGPU
- IOHIDRemoteSensorSessionFilter
- IconServices
- Image-QuickLook
- ImageCaptureCore
- InCallLockScreen
- InCallService
- IncomingCall
- InformationFlowPlugin
- InputUI
- InstallCoordination
- IntelligencePlatform
- IntelligencePlatformCore
- IntelligentRouting
- IntentsUI
- InternationalSettings
- JetEngine
- JoyConHIDServicePlugin
- KGS Driver
- KeyboardArbiter
- KeyboardSettings
- KnowledgeGraphKit
- KnowledgeMonitor
- LegalAndRegulatorySettingsPrivate
- Lexicon
- LiftUI
- LighthouseCoreMLFeatureStore
- LighthouseCoreMLModelStore
- LighthouseDictation
- LighthouseModelMonitoring
- LiveExecutionResultsProbe
- LiveFSFPHelper
- LiveSpeechServices
- LiveSpeechUI
- LiveTranscriptionUI
- LocalAuthenticationCoreUI
- LocalAuthenticationRGBCapture
- LocalAuthenticationUI
- LocalSpeechRecognitionBridge
- LoggingSupport
- LoginUI
- LunaHIDServicePlugin
- MFAANetwork
- MSMessageExtensionBalloonPlugin
- MTLCompiler
- MTLReplayer
- MagnifierSupport
- Mail-Assistant
- MailAccountSettings
- MailAttachmentPlugin
- MailUI
- MailVIPWidget
- ManagedConfiguration
- ManagedConfigurationUI
- MapKitFramework
- MapKitSwiftUI
- Maps-Assistant
- MapsSync
- MarkupUI
- MechPasscode
- MediaAnalysisServices
- MediaControlSender
- MediaConversionService
- MediaLibrary-iOS
- MediaLibraryCore
- MediaPlayerFramework
- MediaPlayerUIFramework
- MediaRemoteUI
- MediaRemoteUIService
- MediaServices
- MediaStream
- MedicationsHealthAppPlugin
- Memories
- MenstrualCyclesAppPlugin
- MentalHealthAppPlugin
- MentalHealthUI
- Mercury
- MessageUI
- MessageUIFramework
- MessagesDataMigrator
- MessagesDataclassOwner
- MessagesUIPlugin
- Metal
- MetalFX
- MetalPerformanceShadersGraph
- MetricMeasurementHelper
- MindSettings
- MobileActivation
- MobileActivationMigrator
- MobileAsset
- MobileBackup
- MobileCal
- MobileMailSettings
- MobilePhone
- MobileSMS
- MobileSafari
- MobileSafariFramework
- MobileSafariSwift
- MobileSafariUI
- MobileSlideShow
- MobileSlideShowSettings
- MobileStore
- MobileStoreUI
- MobileTimer
- MobileTimer-Assistant
- MobileTimerFramework
- MobileTimerUIFramework
- MobileWiFi
- MobilityAppPlugin
- ModelIO
- ModuleACM
- Moments
- MonogramPosterExtension
- MotionSensorLogging
- Movie-QuickLook
- Movies-Assistant
- Music
- MusicCarDisplayUI
- MusicMessagesApp
- MusicRecognition
- MusicSettings
- MusicUsage
- MuteModule
- NDOAccountNotificationPlugin
- NFCControlCenterModule
- NPKCompanionAgent
- NTKCustomization
- NTKTimerComplicationBundle
- NanoBedtimeBridgeSettings
- NanoCompassComplications
- NanoMediaBridgeUI
- NanoMediaRemote
- NanoMenstrualCyclesCompanionSettings
- NanoMusicBridgeSettings
- NanoPassbookBridgeSettings
- NanoPhotosBridgeSettings
- NanoPhotosBridgeSetup
- NanoTimeKitCompanion
- Navigation
- Nearby
- NearbyInteraction
- NeighborhoodActivityConduit
- NetworkServiceProxy
- NetworkStatistics
- NightingaleTraining
- Ninepoint Systems Driver
- Notes
- NotesAccountNotificationPlugin
- NotesAnalytics
- NotesEditor
- NotesSettings
- NotificationCenter
- NotificationsSettings
- NowPlayingUI
- OSAnalytics
- OSLog
- OnBoardingKit
- OpusKit
- OrientationLockModule
- OxygenSaturationSettings
- PASViewService
- PBBridgeSupport
- PCViewService
- PDFKit
- POP
- PassKitFramework
- PassKitUIFoundation
- PassbookSecureUIService
- PassesLockScreenPlugin
- PeerPaymentMessagesExtension
- Pegasus
- PegasusAPI
- PegasusKit
- PencilKit
- PencilPairingUI
- People
- PeopleUI
- PeopleViewService
- PerfPowerServicesMetadata
- PerfPowerServicesReader
- PerformanceTraceModule
- PhoneSnippetUI
- PhoneSuggestions
- PhoneUIPlugin
- Photo Booth
- PhotoAnalysis
- PhotoFoundation
- PhotoLibraryFramework
- PhotosEditUI
- PhotosFramework
- PhotosIntelligence
- PhotosUIEdit
- PhotosUIFramework
- PhotosensitivityProcessing
- PlatterKit
- PodcastsBridgeSettings
- PodcastsKit
- PodcastsPodcastsTodayExtension
- PodcastsStoreUI
- PodcastsUI
- Portrait
- PostSiriEngagement
- PosterBoard
- PosterBoardFramework
- PosterBoardServices
- PosterBoardUI
- PosterKit
- PowerLog
- PowerlogCore
- PreBoard
- PreferencesUI
- PreviewUI
- PrintKitUI
- ProVideo
- ProductKit
- ProductPageExtension
- Profiles
- ProofReader
- ProxCardKit
- ProximityAppleIDSetup
- ProximityAppleIDSetupUI
- ProximityReader
- QOSToolkit
- QueryParser
- QuickLook
- QuickLookSupport
- QuickLookThumbnailingDaemon
- QuickTime Plugin
- RTTUI
- RTTUtilities
- RealityFoundation
- RealityKit
- RecentlyPlayedTodayExtension
- RecentsAvocado
- Recon3D
- RecoverDeviceUI
- ReminderKit
- ReminderKitInternal
- Reminders
- RemoteHID
- RemoteManagementAgent
- RemoteManagementModel
- RemoteManagementStore
- RemotePairingDevice
- RemotePaymentPassActionsService
- RemoteServiceDiscovery
- RemoteUI
- RemoteUIFramework
- RemoteXPC
- RemoteiCloudQuotaUI
- RenderBox
- ReplayKit
- ReplayKitAngel
- ReplayKitModule
- ReportCrash
- ReportMemoryException
- ReportingPlugin
- RespiratoryHealth
- RespiratoryHealthAppPlugin
- Restaurants-Assistant
- RoomPlan
- RoomScanCore
- RunningBoard
- RunningBoardServices
- SFSymbols
- SIMSetupSupport
- SIMSetupUIService
- SOS
- SOSBuddy
- SOSSettings
- SPShared
- SafariBookmarksSyncAgent
- SafariSafeBrowsing
- SafariSharedUI
- Safety
- SafetyKit
- SafetyMonitor
- SafetyMonitorUI
- SampleAnalysis
- SaveToFiles
- ScreenReaderBrailleDriver
- ScreenReaderOutput
- ScreenTimeAgent
- ScreenTimeCore
- ScreenTimeSettingsUI
- ScreenTimeSwift
- ScreenTimeUI
- ScreenTimeUICore
- ScreenshotServicesFramework
- ScreenshotServicesService
- Search
- SearchSettings
- SearchToShareCore
- SensingAlgsService
- SensitiveContentAnalysisUI
- SensorKitHelper
- SeparationAlerts
- SequoiaTranslator
- SessionAssertion
- SessionTrackerAppSettings
- Settings
- Settings-Assistant
- SettingsCellularUI
- SettingsFoundation
- SettingsUIKitPrivate
- SeymourClient
- SeymourCore
- SeymourMedia
- SeymourServices
- SeymourUI
- SharedWithYou
- SharedWithYouFramework
- SharingHUDService
- SharingUI
- SharingUIService
- SharingViewService
- SharingXPCHelper
- ShazamCore
- Shortcuts
- Sidecar
- SignpostSupport
- Silex
- SiriActivation
- SiriAppLaunchIntents
- SiriAudioInternal
- SiriAudioSupport
- SiriCalendarIntents
- SiriCore
- SiriCoreMetrics
- SiriDialogEngine
- SiriExpanseInternal
- SiriExpanseInternalUI
- SiriFindMy
- SiriFlowEnvironment
- SiriHeadlessService
- SiriIdentityInternal
- SiriInCall
- SiriInference
- SiriInferenceFlow
- SiriInferredHelpfulness
- SiriInteractive
- SiriInvocationAnalytics
- SiriKitFlow
- SiriLinkFlowPlugin
- SiriMailInternal
- SiriMailUI
- SiriMessageBus
- SiriMessageTypes
- SiriNLUTypes
- SiriNaturalLanguageParsing
- SiriNetwork
- SiriPaymentsIntents
- SiriPrivateLearningAnalytics
- SiriPrivateLearningInference
- SiriPrivateLearningInferencePlugin
- SiriPrivateLearningLogging
- SiriReferenceResolution
- SiriReferenceResolver
- SiriRequestDispatcher
- SiriSettingsIntents
- SiriSetup
- SiriSharedUI
- SiriSuggestionsAPI
- SiriTTSService
- SiriTTSTrainingAgent
- SiriTaskEngagement
- SiriTimeAlarmInternal
- SiriTimeInternal
- SiriTimeTimerInternal
- SiriTranslationIntents
- SiriTurnTakingManager
- SiriUI
- SiriUIActivation
- SiriUICore
- SiriVideoIntents
- SiriVirtualDeviceResolution
- Siriland
- SleepHealthAppPlugin
- SleepHealthUI
- SleepWidgetUI
- SmartReplies
- SnippetUI
- Social
- SocialFramework
- SocialWeeApp
- SoftwareUpdateBridge
- SoftwareUpdateServicesUI
- SoftwareUpdateServicesUIPlugin
- SoftwareUpdateSettings
- SoftwareUpdateSubscriber
- SoftwareUpdateUIService
- SoundAnalysis
- SoundsAndHapticsSettings
- SpeakThis
- SpeakThisServices
- SpeakTypingServices
- SpeechDetector
- SpeechRecognitionCommandAndControl
- SplashBoard
- Sports-Assistant
- SportsKit
- Spotlight
- SpotlightUIInternal
- SpotlightUIInternalFramework
- SpringBoardUI
- SpringBoardUIServices
- SpriteKit
- StatusKitAgentCore
- Stickers
- StickersUI
- Stocks-Assistant
- StocksAnalytics
- StocksCore
- StocksFramework
- StocksKit
- StocksUI
- StocksWidget
- StorageSettings
- StorageSettingsFramework
- StorageSettingsUI
- StoreDynamicUIPlugin
- StoreKitFramework
- StreamingZip
- Summaries
- SwiftData
- SymptomEvaluator
- Synapse
- System-Assistant
- SystemApertureUI
- SystemStatusServer
- TCC
- TV
- TVMLKit
- TVPlayback
- TVRemoteCore
- TVRemoteModule
- TVRemoteUI
- TVSettings
- TeaUI
- TelephonyRPC
- TelephonyUIFramework
- TemplateKit
- TemplateUI
- TestFlightCore
- TextComposer
- TextInputTestingKit
- TextInput_hi
- TextInput_ja
- TextInput_ko
- TextInput_mr
- TextInput_th
- TextInput_vi
- TextInput_zh
- TextRecognition
- TextToSpeechBundleSupport
- TextToSpeechKonaSupport
- TextToSpeechMauiSupport
- TextToSpeechVoiceBankingSupport
- TextToSpeechVoiceBankingUI
- ThirdPartyApplicationSettings
- TimerFlowDelegatePlugin
- TimerModule
- TipKit
- TipKitCore
- TipsApp
- TipsDaemon
- TipsNext
- TipsNotificationExtension
- TipsTryIt
- TipsUI
- TipsWidgetExtension
- ToneKit
- TouchRemote
- TrackingAvoidance
- Translate
- Translation
- TranslationDaemon
- Trial
- TrustedPeers
- TrustedPeersHelper
- TwitterFramework
- TypistFramework
- UARPUpdaterServiceHID
- UARPUpdaterServiceUSBPD
- USBHost
- USDKit
- UnityPoster
- UniversalHID
- UpNext
- UsageSettings
- UserNotificationsCore
- UserNotificationsServer
- UserNotificationsUI
- UserSafetyUI
- VFX
- ViceroyTrace
- VictoriaSettings
- VideoConferenceControlCenterModule
- VideoProcessing
- VideoSubscriberAccountDeveloperSettings
- VideoSubscriberAccountSettings
- VideoToolbox
- Videos
- VideosExtrasFramework
- VideosUICore
- VideosUIFramework
- VirtualAudio
- VisionHealthAppPlugin
- VisualAlert
- VisualIntelligence
- VisualUnderstanding
- VoiceOver
- VoiceOverServices
- VoiceShortcutsUI
- VoiceTriggerUI
- WAAnswer-Assistant
- WPDaemon
- Wallpaper
- WallpaperKit
- WallpaperSettings
- WatchControlSettings
- WatchQuickActionsServices
- WebBookmarks
- WebGPU
- WebInspector
- WebKitLegacy
- WebProcess
- WebProcessLoader
- WiFiKit
- WidgetKit
- WidgetPreviewsShellPlugin
- WidgetPreviewsSupport
- Widgets
- WirelessModemSettings
- WirelessProximity
- WirelessRadioManagerd
- WorkflowEditor
- WorkflowUICore
- WorkoutAnnouncements
- WorkoutCore
- WorkoutKit
- WorkoutKitUI
- WorkoutRemoteViewService
- XboxOneHIDServicePlugin
- ZhuGeSupport
- ZoomServices
- _IconServices_SwiftUI
- _JetEngine_SwiftUI
- _MapKit_SwiftUI
- _MusicKitInternal_MediaPlaybackCore
- _MusicKitInternal_MediaPlayer
- _MusicKit_SwiftUI
- _WorkoutKit_SwiftUI
- accessoryupdaterd
- adc-kronos-d3y.im4p
- addressbooksyncd
- adid
- afktool
- analyticsd
- ansf.t8120.release.im4p
- aopfw-iphone15baop.im4p
- appconduitd
- appleh13camerad
- appstorecomponentsd
- asd
- assetsd
- assistivetouchd
- audioanalyticsd
- audiomxd
- automationmode-writer
- axassetsd
- backboardd
- backupd
- batteryintelligenced
- biomesyncd
- calaccessd
- catutil
- cloudphotod
- com.apple.CloudDocsUI.CloudSharing-AppExtension
- com.apple.DocumentManager.Service-AppExtension
- com.apple.FTLivePhotoService
- com.apple.MobileSoftwareUpdate.CleanupPreparePathService
- com.apple.NeighborhoodActivityConduitService
- com.apple.SpeechRecognitionCore.speechrecognitiond
- com.apple.accessoryd.matching
- com.apple.cts
- com.apple.driver.AppleARMPlatform
- com.apple.driver.AppleBasebandM20
- com.apple.driver.AppleDCPDPTXProxy
- com.apple.driver.AppleDiskImages2
- com.apple.driver.AppleEmbeddedMikeyBus
- com.apple.driver.AppleEmbeddedUSBHost
- com.apple.driver.AppleHIDTransportSPI
- com.apple.driver.AppleHPM
- com.apple.driver.AppleJPEGDriver
- com.apple.driver.AppleMobileDispH15P-DCP
- com.apple.driver.AppleOLYHAL
- com.apple.driver.ApplePMGR
- com.apple.driver.ApplePPMCPMS
- com.apple.driver.AppleS5L8940XI2C
- com.apple.driver.AppleSPMI
- com.apple.driver.AppleT8120CLPC
- com.apple.driver.AppleTriStar
- com.apple.driver.AppleUSBCardReader
- com.apple.driver.AppleUSBLightningAdapter
- com.apple.driver.AppleUVDMDriver
- com.apple.driver.DiskImages
- com.apple.driver.IODARTFamily
- com.apple.driver.IOHIDPowerSource
- com.apple.driver.usb.AppleSynopsysUSBXHCI
- com.apple.driver.usb.AppleUSBHub
- com.apple.driver.usb.AppleUSBXHCI
- com.apple.driver.usb.cdc.ncm
- com.apple.iokit.IOAVFamily
- com.apple.iokit.IOAccessoryManager
- com.apple.iokit.IODisplayPortFamily
- com.apple.iokit.IOUSBHostFamily
- com.apple.iokit.IOUSBMassStorageDriver
- com.apple.photos.ImageConversionService
- com.apple.photos.VideoConversionService
- com.apple.siri.embeddedspeech
- com.apple.tailspin
- contactsd
- contactsdonationagent
- continuitycaptured
- coreauthd
- coreduetd
- dasd
- dietappleh13camerad
- diskimagescontroller
- diskimagesiod
- dmd
- eventkitsyncd
- familycircled
- feedbackd
- fileproviderctl
- fileproviderd
- financed
- fmfd
- gamepolicyd
- geoanalyticsd
- h15_ane_fw_themis_d7x.im4p
- iAdFramework
- iBooksSettings
- iCloud+
- iCloudDriveApp
- iCloudMailAccountUI
- iCloudNotification
- iTunesStoreUIFramework
- icloudCalendarSettings
- icloudMailSettings
- inboxupdaterd
- ind
- installd
- iphone15dcp.im4p
- libANGLE-shared.dylib
- libAce3Updater.dylib
- libAudioDSPCore.dylib
- libAudioIssueDetector.dylib
- libAudioToolboxUtility.dylib
- libBBUpdaterDynamic.dylib
- libBIG5.dylib
- libBKDM2.dylib
- libBNNS.dylib
- libBasebandCommandDrivers.dylib
- libBasebandCommandDriversARI.dylib
- libBasebandCommandDriversQMI.dylib
- libCommCenterAWDMetrics.dylib
- libCommCenterBase.dylib
- libCommCenterKCommandDrivers.dylib
- libCommCenterMCommandDrivers.dylib
- libComposeFilters.dylib
- libDECHanyu.dylib
- libDECKanji.dylib
- libEUC.dylib
- libEUCTW.dylib
- libEmbeddedSystemAUs.dylib
- libFontParser.dylib
- libGBK2K.dylib
- libGPUCompiler.dylib
- libGPUCompilerImpl.dylib
- libHSFilerDynamic.dylib
- libIPTelephony.dylib
- libInFieldCollection.dylib
- libJOHAB.dylib
- libKTLDynamic.dylib
- libLLVM.dylib
- libLogRedirect.dylib
- libMSKanji.dylib
- libMemoryResourceException.dylib
- libMobileGestalt.dylib
- libPN548_API.dylib
- libSTS-N.dylib
- libUES.dylib
- libUTF1632.dylib
- libUTF7.dylib
- libUTF8.dylib
- libUTF8MAC.dylib
- libVFXCore.dylib
- libVIQR.dylib
- libVinylUpdater.dylib
- libZW.dylib
- libZhuGeArmory.dylib
- libarchive.2.dylib
- libauthinstall.dylib
- libdns_services.dylib
- libheimdalasn1.dylib
- libiconv.2.dylib
- libicucore.A.dylib
- libllvm-flatbuffers.dylib
- libmapper_none.dylib
- libmapper_parallel.dylib
- libmapper_serial.dylib
- libmecabra.dylib
- libmis.dylib
- libnfrestore.dylib
- libnfshared.dylib
- libquic.dylib
- librealtime_safety.dylib
- libsandbox.1.dylib
- libswiftShazamKit.dylib
- libsystem_c.dylib
- libwebrtc.dylib
- lighthouse_runtime
- linkd
- lockdownd
- lockdownmoded
- logd_reporter
- magicswitchd
- mapspushd
- mapssyncd
- mediasetupd
- mlruntimed
- mobile_obliterator
- mobileassetd
- nanobackupd
- nanomapscd
- nanoprefsyncd
- nanoregistryd
- nanosystemsettingsd
- nanotimekitcompaniond
- navd
- nehelper
- nsurlsessiond
- otpaird
- parsecd
- pasted
- peopled
- pipelined
- pointeruid
- profiled
- rans.t8120.release.im4p
- recentsd
- remindd
- remoted
- remotemanagementd
- remotepairingdeviced
- rmdinspect
- searchd
- securityuploadd
- seld
- siriinferenced
- sirittsd
- sportsd
- spotlightknowledged
- sptm.t8120.release.im4p
- stickersd
- subridged
- suggestd
- sysdiagnose
- sysdiagnose_helper
- sysdiagnosed
- t8120pmp.im4p
- teslad
- thermalmonitord
- timed
- transparency-sysdiagnose
- tvremoted
- txm.iphoneos.release.im4p
- voicebankingd
- vot
- weatherd
- webbookmarksd
- wirelessinsightsd
- xpcroleaccountd

</details>

## LOW_SIGNAL — excluded (1284, metadata/timestamp churn only)

<details><summary>Show 1284 components</summary>

- AAAFoundationSwift
- AAAccountNotificationPlugin
- ACDatabaseBackupNotificationPlugin
- AFKUser
- AGXCompilerConnection-S2A8
- AGXCompilerCore-S2A8
- AGXGPURawCounter
- AGXGPURawCounterBundle
- AISAccountNotificationPlugin
- AKAccountNotificationPlugin
- AMPCoreUI
- AMSAccountNotificationPlugin
- APConfigurationSystem
- APFoundation
- ARKitCore
- ASDAccountNotficationPlugin
- ASIOKit
- ASOctaneSupport
- ATFoundation
- AVRouting
- AXAggregateStatisticsServices
- AXAssetLoader
- AXContainerServices
- AXLocalizationCaptionService
- AXNTKUtilities
- AXSpeakFingerManager
- AXSpeechImplementation
- AXWatchRemoteScreenServices
- Accessibility
- AccessibilityFocusEngine
- AccessibilityGuidedAccessControlCenterModule
- AccessibilityRemoteServices
- AccessibilityRemoteUIServices
- AccessibilityShorcutsModule
- AccessibilitySoundDetectionControlCenterModule
- AccessibilityTextSizeModule
- AccessibilityUIShared
- AccessibilityUIViewServices
- AccessoryAssistiveTouch
- AccessoryAudio
- AccessoryCommunications
- AccessoryComponentAuth
- AccessoryHID
- AccessoryMediaLibrary
- AccessoryNavigation
- AccessoryNowPlaying
- AccessoryOOBBTPairing
- AccessoryVoiceOver
- AccessoryiAP2Shim
- ActionPredictionHeuristics
- ActivityAchievements
- ActivityAchievementsDaemon
- ActivityAchievementsPlugin
- ActivityAwardsCore
- ActivityAwardsPlugin
- ActivityAwardsServices
- ActivitySharingAwardsPlugin
- ActivitySharingDaemonCore
- ActivitySharingPlugin
- ActivitySharingServices
- ActivitySharingUI
- AdPlatformsCommon
- AdPlatformsCommonUI
- AdServices
- AirFair
- AirFair2
- AirPlayKit
- AirPlayRoutePrediction
- AirTraffic
- AirTrafficDevice
- AlarmModule
- AlgosScoreFramework
- AltimeterHarvest
- AmbientUIKit
- AmbientUIServices
- AnnounceSiriExtensions
- AppC3D
- AppClip
- AppGenius
- AppPredictionFoundation
- AppPredictionUIFoundation
- AppRecommendations
- AppSSOCore
- AppSSOKerberos
- AppSSOUI
- AppState
- AppStoreDaemon
- AppStoreFoundation
- AppStoreUI
- AppSupport
- AppSupportUI
- AppleAOPAudioPlugin
- AppleCV3DHA
- AppleCV3DModels
- AppleCVAPhoto
- AppleFirmwareUpdate
- AppleHIDTransportSupport
- AppleIDAuthentication
- AppleKeyStore
- AppleMediaDiscovery
- AppleSARHelper
- AppleTracingSupportSymbolication
- AskPermission
- AskTo
- AskToCore
- AssertionServices
- AssistantCardServiceSupport
- AssistiveTouch
- AssistiveTouch-iOS
- AtomicsInternal
- AttentionAwarenessFilter
- AudioAccessoryServices
- AudioAnalytics
- AudioAnalyticsBase
- AudioAnalyticsInternal
- AudioDataAnalysis
- AudioServerApplication
- AudioSuggestionsPlugin
- AudioToolboxCore
- AutocorrectionTesterDESPlugin
- AvailabilityKit
- AvatarPersistence
- AvatarPoster
- BLEPairing-iOS
- BTCloudPairingAccountNotificationPlugin
- BWCrucible
- BackBoardHIDEventFoundation
- BackBoardHIDEventProcessors
- BackBoardServices
- BackgroundTasks
- BacklightServices
- BagKit
- BatteryCenter
- Baum
- BiomeDSL
- BiomeFlexibleStorage
- BiomePubSub
- BiomeSequence
- BiomeSync
- BiometricSupport
- BluetoothAudio
- BluetoothServices
- BluetoothServicesUI
- BoardServices
- Bom
- BookCoverUtility
- BookLibrary
- BrailleSymbology
- BridgeCommons
- BridgeReporting
- BrightnessControl
- BusinessChatService
- BusinessServices
- BusinessServicesUI
- CARP
- CBORLibrary
- CDDataAccess
- CDDataAccessExpress
- CDPAccountNotificationPlugin_IOS
- CPAnalytics
- CTCarrierSpace
- CTParser
- CVNLP
- CacheDelete
- CalculatorModule
- CalendarLink
- CallKit
- CallScreeningActivity_Shared
- CameraEditKit
- CameraModule
- CarCommandsUIFramework
- CarKey
- CarKit
- CarPlayServices
- CarPlaySetup
- CarrierSettings
- Celestial
- CellularBridgeUI
- CellularPlanManager
- CheckerBoardServices
- Cinematic
- ClassroomKit
- ClassroomUIKit
- ClipServices
- ClockComplications
- ClockKitUI
- CloudAssetDaemon
- CloudDocsDataclassOwnerPlugin
- CloudDocsFileProvider
- CloudKitAccessPlugin
- CloudKitAuthenticationPlugin
- CloudKitCode
- CloudKitCodeProtobuf
- CloudKitDistributedSync
- CloudKitNotificationPlugin
- CloudKitSettings
- CloudMediaServicesInterfaceKit
- CloudSharing
- CollectionViewCore
- CollectionsInternal
- Combine
- CombineCocoa
- CommandAndControlUI
- CommonAuth
- CommunicationSafetySettingsUI
- Communications-iOS
- CompanionCamera
- CompanionHealthDaemon
- CompanionHealthPlugin
- CompanionServices
- CompanionSync
- CompassCalibration
- CompassUI
- ConfigurationEngineModel
- ConnectedAudioTest
- ContainerManagerSystem
- ContainerManagerUser
- ContainerMigrator
- ContextualActionsClient
- ContinuousDialogManagerService
- CoreAccessoriesFeatures
- CoreBluetoothUI
- CoreCDPUIInternal
- CoreDuetContext
- CoreDuetDaemonProtocol
- CoreDuetSync
- CoreGPS
- CoreGlyphsPrivate
- CoreHaptics
- CoreIDCred
- CoreIDCredBuilder
- CoreIDVAccountNotificationPlugin
- CoreLocationAccountNotificationPlugin
- CoreLocationReplay
- CoreLocationSync
- CoreLocationUI
- CoreMIDI
- CoreMaterial
- CoreOCModules
- CoreParsec
- CorePhoneNumbers
- CoreRecentsAccountNotificationPlugin
- CoreRepairCore
- CoreRepairKit
- CoreRepairLite
- CoreRepairUI
- CoreRoutineAccountNotificationPlugin
- CoreServices
- CoreServicesStore
- CoreSpeechGazeTracking
- CoreSuggestionsML
- CoreThread
- CoreTime
- CoreUtilsUI
- CorrectionsProfilesSync
- Coverage
- CrisisResources
- DAAPKit
- DAAccount
- DAAccountAuthenticator
- DAAccountNotifier
- DACardDAV
- DACoreDAVGlue
- DADaemonSubCal
- DAEAS
- DAEASOAuthFramework
- DAIMAPNotes
- DALDAP
- DASDaemon
- DASDelegate
- DASubCal
- DEPClientLibrary
- DMCApps
- DMCToolsUIUtilities
- DMDAccountNotificationPlugin
- DOT
- DSRemotePairing
- DailyBriefingFlowPlugin
- DataAccess
- DataAccessExpress
- DataAccessUI
- DataActivation
- DefaultAccessPlugin
- DeviceDiscoveryUI
- DeviceManagement
- DeviceOMatic
- DiagnosticLogCollection
- DiagnosticRequest
- DiagnosticsKit
- DiagnosticsSupport
- DictionaryUI
- DifferentialPrivacy
- DigitalAccess
- DigitalSeparation
- Disembark
- DiskArbitration
- DiskImages
- DiskSpaceDiagnostics
- DoNotDisturb
- DoNotDisturbKit
- DocumentManagerCore
- DocumentUnderstanding
- DocumentUnderstandingClient
- DonationAccountWatcher
- DragUI
- DrawingBoard
- DriverManagement
- DropIn
- DropInCore
- EAFirmwareUpdater
- EAPOLController
- ESAccountAuthenticator
- ESAccountNotifier
- ESDaemonSupport
- EasyConfig
- EmailAddressing
- EmailCore
- EmbeddingService
- EmergencyAlertExtension
- EmergencyAlerts
- EncoreXPCService
- Engram
- EventKitTCCUI
- EventKitUICore
- ExchangeSync
- ExchangeSyncExpress
- ExpansionBoard
- ExposureNotification
- ExposureNotificationDaemon
- FMF
- FMIPCore
- FMNetworking
- FSEvents
- FSKit
- FTAWD
- FTClientServices
- FaceTimeMigrator
- FamilyNotification
- FeedbackAssistantModule
- FeedbackLogger
- FileProviderTelemetry
- FinHealth
- FinHealthCore
- FinHealthInsights
- FindMyBluetooth
- FindMyCloudKit
- FindMyCommon
- FindMyCrypto
- FindMyDaemonSupport
- FindMyDevice
- FindMyDeviceAccountNotificationPlugin
- FindMyDeviceUI
- FindMyLocateObjCWrapper
- FindMyServerInteraction
- FindMyStorage
- FitnessCoaching
- FitnessCoachingCore
- FlowFrameKit
- Fluid
- FoundInAppsPlugins
- FoundationODR
- FusionTracker
- GEO
- GKSPerformance
- GLEngine
- GLTools
- GLToolsCore
- GPURawCounter
- GPUToolsCore
- GPUToolsPlayback
- GPUToolsiOS
- GSS
- Game
- GameControllerSettings
- GameKit
- GameKitServices
- GamePolicy
- GamePolicyServices
- GenerationalStorage
- GeoAnalytics
- GeoServicesCore
- GoogleAuthenticationPlugin
- GroupKit
- GroupKitCore
- H10ISPServices
- H13ISPServices
- H264H8.videodecoder
- H264SW.videocodec
- HAENotifications
- HID
- HIDAnalytics
- HIDDisplay
- HIDPreferences
- HRTFEnrollment
- HSAAuthentication
- HangTracer
- HangTracerSettingsClient
- HealthAlgorithms
- HealthAppHealthDaemon
- HealthAppHealthDaemonSupport
- HealthAppPlugin
- HealthAppServices
- HealthAppSupport
- HealthArticles
- HealthArticlesGeneration
- HealthDaemonFoundation
- HealthDiagnosticExtensionCore
- HealthDomainsTools
- HealthFlowDelegatePlugin
- HealthHearing
- HealthHearingDaemon
- HealthKitAccountNotificationPlugin
- HealthKitAdditions
- HealthMedications
- HealthMedicationsDaemonPlugin
- HealthMedicationsExperience
- HealthMedicationsVision
- HealthMedicationsVisionUI
- HealthMedicationsWidgetUI
- HealthMenstrualCycles
- HealthMenstrualCyclesDaemon
- HealthMenstrualCyclesUI
- HealthMobility
- HealthMobilityDaemon
- HealthMobilityUI
- HealthPluginHost
- HealthRecordsConceptsSupport
- HealthRecordsDaemon
- HearingMLHelper
- HeartDaemonPlugin
- HeartHealth
- Heimdal
- HeroDataClient
- HighlightAlerts
- Highlights
- HomeCommunicationUIFramework
- HomeKitAccountNotificationPlugin
- HomeKitBackingStore
- HomeKitFeatures
- HomePlatformSettingsUI
- HomeRecommendationEngine
- HomeServices
- HomeSharing
- HomeUICommon
- HomeUtilityServices
- HoverTextServices
- HumanUnderstandingEvidence
- HumanUnderstandingFoundation
- IAP
- IAPAuthentication
- ICE
- IDSAccountNotificationPlugin
- IDSBlastDoorSupport
- IDSHashPersistence
- IDSKVStore
- IMAP
- IMAccountNotificationPlugin
- IMCorePipeline
- IMDMessageServices
- IMDMessageServicesAgent
- IMSharedUI
- IMTransferAgent
- INDAccountNotificationPlugin
- IOHIDDisplaySessionFilter
- IOHIDEventProcessorFilter
- IOHIDEventSystemStatistics
- IOHIDKeyboardFilter
- IOHIDLib
- IOHIDPointerScrollFilter
- IOHIDT8027USBSessionFilter
- IOMobileFramebuffer
- IOSurface
- IOSurfaceAccelerator
- IOUSBDeviceLib
- IOUSBHost
- ISPAirPlay.plugin
- ITMLKit
- IXATestAppRelay
- IconFoundation
- IdentityFlowPlugin
- IdentityLookup
- IdentityLookupUI
- InAppMessages
- InAppMessagesCore
- IncomingCallFilter
- InfoQueryPersonalizationFeatures
- InputAnalytics
- IntelligencePlatformCompute
- IntelligencePlatformComputeService
- IntelligencePlatformLibrary
- IntelligentRoutingDaemon
- IntentsCore
- IntentsFoundation
- IntentsServices
- IntlPreferences
- IntlPreferencesUI
- IonosphereHarvest
- JPEGH1.videodecoder
- JPEGH1.videoencoder
- JetPack
- JetUI
- JoinRequests
- KGS
- KRExperiments
- KerberosAuthenticationPlugin
- KeyboardBrightnessModule
- KeyboardServices
- KeyboardSettingsFeedback
- KeychainCircle
- KeychainDataclassOwner
- KeychainSyncAccountNotification
- LearnedFeatures
- LegacyGameKit
- LegacyHandle
- LiblouisBrailleTranslator
- LighthouseAV
- LighthouseCoreMLModelAnalysis
- LighthousePAN
- LighthouseQuartz
- LinguisticData
- LiveFS
- LiveTranscription
- LocalAuthenticationCore
- LocalAuthenticationEmbeddedUI
- LocalAuthenticationPrivateUI
- LocalStatusKit
- LocaleSettings
- LocationFenceSync
- LocationPromptUI
- LocationSupport
- LockdownMode
- LockdownModeAccountNotificationPlugin
- LoopKitGeneratedKernels
- LowPowerMode
- LowPowerModule
- MFAAuthentication
- MIDI
- MIME
- MLAssetIO
- MLRuntime
- MMCSServices
- MP4VH8.videodecoder
- MPUFoundation
- MSUDataAccessor
- MTLSpline
- MTLToolsDeviceSupport
- MacinTalk
- MagnifierModule
- MailServices
- MailWebProcessSupport
- ManagedEvent
- ManagedSettings
- ManagedSettingsObjC
- ManagedSettingsSupport
- ManagedSettingsUI
- MapsSuggestions
- Marco
- Marrs
- MatterSupport
- MeasureFoundation
- MechPearl
- Media
- MediaAccessibility
- MediaControlsAudioModule
- MediaControlsModule
- MediaFoundation
- MediaGroups
- MediaGroupsDaemon
- MediaML
- MediaMLServices
- MediaPlatform
- MediaPlayerUI
- MediaRemoteDaemonServices
- MediaServicesBroker
- MediaSetup
- MemoryDiagnostics
- MenstrualAlgorithmsInternal
- MenstrualCyclesDaemonPlugin
- MentalHealth
- MentalHealthDaemon
- MentalHealthWidgetUI
- MessageAccountAuthenticationPlugin
- MessageAccountNotificationPlugin
- MessageSecurity
- MessageSupport
- MessagesAirlockService
- MessagesBlastDoorService
- MessagesBlastDoorSupport
- MessagesComplication
- MessagesDataKeyboardPlugin
- MessagesSupport
- MetadataUtilities
- MetalKit
- MetricKit
- MetricKitCore
- MetricKitServices
- MetricKitSource
- MetricMeasurement
- MobileAccessoryUpdater
- MobileAssetUpdater
- MobileBluetooth
- MobileCalSettings
- MobileContainerManager
- MobileCoreServices
- MobileDevices-0001
- MobileDevices-0003
- MobileIcons
- MobileInBoxUpdate
- MobileInstallation
- MobileObliteration
- MobilePhoneSettings
- MobileSoftwareUpdate
- MobileStoreDemoSetupUI
- MobileTimerSupport
- ModuleBase
- MomentsOnboardingAndSettings
- MonogramPoster
- MotionCalibration
- MultitaskingAndGesturesSettings
- MusicSettingsSupport
- MusicStoreUI
- NCLaunchStats
- NFC
- NPTKit
- NanoAudioControl
- NanoBackup
- NanoBooksComplicationsCompanion
- NanoMailCompanionUI
- NanoMailKitServer
- NanoMapsNavigationCompanionDataSource
- NanoMapsSampleDataSource
- NanoMediaAPI
- NanoMenstrualCyclesComplication
- NanoPhotosCore
- NanoRegistry
- NanoSleepComplication
- NanoSystemSettings
- NanoUniverse
- Navigation-iOS
- NearFieldAccessory
- NearbySessions
- NetAppsUtilities
- NetAppsUtilitiesUI
- Netrb
- NetworkQualityServices
- NetworkRelay
- NeuralNetworks
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
- NewsNotificationPlugin
- NewsPersonalization
- NewsServices
- NewsServicesInternal
- NewsSubscription
- NewsToday
- NewsTransport
- NewsUI
- NewsUI2
- NewsURLBucket
- NewsURLResolution
- Nexus
- Ninepoint
- NotesPreviewKit
- NotesUIServices
- NowPlaying-iOS
- OOBBTPairing-iOS
- OSAServicesClient
- OSASubmissionClient
- OSASyncProxyClient
- OSAnalyticsPrivate
- OTSVG
- OpenGLES
- Osprey
- PCSAccountNotificationPlugin
- PDS
- PLAMonitor
- PLSnapshot
- PairedUnlock
- PairingProximity
- ParavirtualizedANE
- ParsecModel
- ParsecSubscriptionServiceSupport
- PassKit
- PassKitServices
- PassbookAccountNotificationPlugin
- PasswordsDigitalSeparation
- Pasteboard
- PaymentUI
- PaymentUIBase
- PearlEventFilter
- PegasusConfiguration
- PegasusPersistence
- PeopleUIInternal
- PerfPowerServicesSignpostReader
- PerfPowerTelemetryReaderService
- PerformanceControlKit
- PerformanceTrace
- PersonalAudio
- PersonalIntelligenceCore
- PersonalizationPortrait
- Phoenix
- Phone
- PhoneNumbers
- Photo
- PhotosAccountNotificationPlugin
- PhotosImagingFoundation
- PhotosKnowledgeGraph
- PlacesKit
- Platform-Bluetooth
- PointerUISystemServices
- PortraitCore
- PowerlogAccounting
- PowerlogControl
- PowerlogDatabaseReader
- PowerlogFullOperators
- PreviewShellKit
- PreviewsFoundation
- PreviewsInjection
- PreviewsMessaging
- PreviewsOSSupport
- PreviewsOSSupportUI
- PreviewsServices
- PreviewsServicesUI
- ProactiveBlendingLayer_iOS
- ProactiveCDNDownloader
- ProactiveContextClient
- ProactiveExperiments
- ProactiveExperimentsInternals
- ProactiveHarvesting
- ProactiveInputPredictions
- ProactiveInputPredictionsInternals
- ProactiveML
- ProactiveMagicalMoments
- ProactiveSuggestionClientModel
- PromotedContent
- PromotedContentProxy
- PromotedContentSupport
- PromotedContentUI
- ProofingPlugin
- ProtectedCloudKeySyncing
- ProtectedCloudStorage
- ProtocolBuffer
- Proximity
- ProximityControl
- ProximityUI
- PushKit
- PushToTalk
- QRCodeModule
- QueryUnderstanding
- QuickLookThumbnailGeneration
- QuickLookThumbnailing
- QuickLookUICore
- QuickNoteModule
- QuickSpeak
- QuickTime
- RPAccountNotificationPlugin
- RTBuddyCrashlogDecoder
- Radio
- RapportUI
- RawCamera
- Recap
- ReflectionInternal
- RegulatoryDomain
- RelativeMotion
- RelevanceEngineSolar
- ReminderKitUI
- RemindersAccountNotificationPlugin
- RemindersSiriUIPlugin
- RemoteConfiguration
- RemoteManagement
- RemoteManagementProtocol
- RemoteManagementUI
- RemoteMediaServices
- RemoteStateDumpKit
- RemoteTextInput
- ResearchApp
- RespiratoryHealthDaemon
- RespiratoryHealthDaemonPlugin
- RespiratoryHealthUI
- Routine
- RuntimeInternal
- SAML
- SCHelper
- SDAPI
- SMBClientProvider
- SMBSearch
- SOSUI
- SPFinder
- SPOwner
- STExtractionService
- STExtractionService.privileged
- STSXPCHelperClient
- SafetyAlerts
- SafetyMonitorMessages
- SchoolTime
- SchoolTimeSettingsUI
- ScreenReaderCore
- ScreenTime
- ScreenshotServices
- SearchPartyAccountNotificationPlugin
- SecureBackupNotification
- SensitiveContentAnalysis
- SensitiveContentAnalysisML
- SensorKit
- SensorKitUI
- SentencePiece
- ServiceManagement
- SessionAlert
- SessionCore
- SessionFoundation
- SessionPushNotifications
- SessionSyncEngine
- SettingsCellular
- SetupKit
- SeymourAwardsPlugin
- SeymourServerProtocol
- SharedWebCredentialViewService
- SharedWithYouCore
- SharingAccountNotificationPlugin
- SharingHUD
- SharingXPCServices
- ShazamEvents
- ShazamInsights
- ShazamKit
- ShazamKitUI
- ShazamModule
- ShortcutUIKit
- ShortcutsCloudKitAccountNotificationPlugin
- SidecarUI
- SignpostCollection
- SignpostMetrics
- SignpostNotification
- SilexVideo
- SilexWeb
- SimpleKeyExchange
- SiriActivationFoundation
- SiriAppResolution
- SiriAudioIntentUtils
- SiriAudioSnippetKit
- SiriAudioSnippetUI
- SiriCarCommandsIntents
- SiriCloudKitAccountsNotifier
- SiriCorrections
- SiriDailyBriefingInternal
- SiriEmergencyIntents
- SiriFindMyUI
- SiriGeo
- SiriHomeAccessoryFramework
- SiriInformationTypes
- SiriIntentEvents
- SiriLiminal
- SiriNLUOverrides
- SiriNotebook
- SiriObservation
- SiriOntology
- SiriOntologyProtobuf
- SiriReaderServices
- SiriReferenceResolutionDataModel
- SiriSignals
- SiriSpeechSynthesis
- SiriSuggestions
- SiriSuggestionsKit
- SiriSuggestionsSupport
- SiriTasks
- SiriUICardKitProviderSupport
- SiriWellnessIntents
- Sleep
- SleepDaemon
- SleepHealth
- SleepHealthDaemon
- SleepHealthDaemonPlugin
- SmartRepliesServer
- SmartRepliesUI
- SnippetCommands
- SnippetKit
- SocialAccountNotificationPlugin
- SocialServices
- SoftwareUpdateController
- SoftwareUpdateCoreConnect
- SoftwareUpdateCoreSupport
- SoundBoardServices
- SoundScapesUtility
- SpeechRecognitionCore
- SpeechRecognitionSharedSupport
- SpokenNotificationsModule
- SpotlightFoundation
- SpotlightLinguistics
- SpotlightReceiver
- SpotlightRecommendation
- SpotlightResources
- SpotlightUI
- SpotlightUIShared
- SpringBoardIntents
- StatusKit
- StopwatchModule
- StorageKit
- StorageUI
- StoreBookkeeper
- StoreBookkeeperClient
- StoreServices
- SuggestionsSpotlightMetrics
- SummariesHealthDaemon
- SurfStatusSync
- SwiftCertificate
- SwiftNN
- SwiftSQLite
- SwiftUIAccessibility
- Symbols
- SymptomAnalytics
- SymptomDiagnosticReporter
- SymptomNetworkUsage
- SymptomPresentationFeed
- SymptomPresentationLite
- SymptomReporter
- SynapseSyncPlugin
- System
- SystemAperture
- SystemConfiguration
- SystemCustomization
- SystemPaperPresentation
- SystemStatus
- SystemWake
- TSApplication
- TSReading
- TSUtility
- TVAppServices
- TVLatency
- TVUIKit
- TailspinSymbolication
- TailspinSymbolicationServer
- TeaCharts
- TeaDB
- TeaFoundation
- TeaSettings
- TeaSnappy
- TeaTemplate
- TextInput_bo
- TextInput_ca
- TextInput_chr
- TextInput_cs
- TextInput_de
- TextInput_el
- TextInput_emoji
- TextInput_en
- TextInput_es
- TextInput_fr
- TextInput_haw
- TextInput_he
- TextInput_intl
- TextInput_mul
- TextInput_my
- TextInput_nl
- TextInput_pa
- TextInput_pt
- TextInput_si
- TextInput_sk
- TextInput_ta
- TextInput_tr
- TextInput_ug
- TextInput_yue
- TextUnderstandingShared
- ThreadNetwork
- TimeAppServices
- TimeZone
- TinCanShared
- TipKitLegacy
- TipKitServices
- TipsNextServices
- ToneLibrary
- TraitsArbiter
- TranslationUI
- TrialArchivingService
- TrialProto
- TypingDESPlugin
- TypologyAccess
- UARPUpdaterService
- UARPiCloud
- UIKitServices
- UITriggerVC
- URLFormatting
- USDLib_FormatLoaderProxy
- UVFSService
- UVFSXPCService
- UniformTypeIdentifiers
- UsageTracking
- UserEventAgent
- UserFS
- UserManagement
- UserManagementLayout
- UserManagementUI
- UserNotifications
- UserNotificationsKit
- UserNotificationsSettings
- UserNotificationsTranslation
- UserSafety
- VPNPreferences
- VideoToolboxParavirtualizationSupport
- VirtualGarage
- VisionCore
- VisionKit
- VisionKitInternal
- VisualLocalization
- VisualLogger
- VoiceDial
- VoiceMemosModule
- VoiceShortcutsUICardKitProviderSupport
- WalletModule
- WatchControlAssets
- WatchFacesWallpaperSupport
- WatchReplies
- WatchdogClient
- WebApp
- WebBookmarksNotificationPlugin
- WebBookmarksSwift
- WebContentAnalysis
- WebContentAnalysisUI
- WebSheet
- WellnessUI
- WiFiAnalytics
- WiFiPeerToPeer
- WiFiSharing
- WiFiVelocity
- WidgetPreviewsExtensionAgent
- WirelessCoexManager
- WirelessInsights
- WorkoutHealthBridge
- WorkoutKitServices
- WorldClockComplications
- XGBoostFramework
- XPCAcmeService
- XavierCore
- XavierNews
- YahooAuthenticationPlugin
- YelpAccessPlugin
- _AVKit_SwiftUI
- _AppIntents_SwiftUI
- _AppIntents_UIKit
- _AuthenticationServices_SwiftUI
- _Coherence_CloudKit_Private
- _CoreLocationUI_SwiftUI
- _DeviceActivity_SwiftUI
- _HomeKit_SwiftUI
- _JetUI_SwiftUI
- _PassKit_SwiftUI
- _PhotosUI_SwiftUI
- _QuickLook_SwiftUI
- _SceneKit_SwiftUI
- _SwiftData_CoreData
- _SwiftData_SwiftUI
- apfs_boot_mount
- apfs_checkseal
- apfs_condenser
- bookassetd
- brctl
- cfprefsd
- ckdiscretionaryd
- com.apple.DriverKit-AppleEthernetMLX5
- com.apple.Translate.appremoval
- com.apple.askpermission.AccountNotificationPlugin
- com.apple.corelocation.locationUI
- com.apple.dispatch.vfs
- com.apple.driver.AppleAOPAudio
- com.apple.driver.AppleAOPVoiceTrigger
- com.apple.driver.AppleIDV
- com.apple.driver.AppleSmartIO2
- com.apple.driver.AppleUSBDeviceMux
- com.apple.driver.AudioDMAController-T8120
- com.apple.driver.RTBuddy
- com.apple.fsevents.matching
- com.apple.systemconfiguration
- companion_proxy
- containermanagerd
- containermanagerd_system
- countryd
- destinationd
- deu.dylib
- distnoted
- eci.dylib
- eng.dylib
- enu.dylib
- esm.dylib
- esp.dylib
- fairplayd.H2
- filecoordinationd
- fin.dylib
- findmydeviced
- fra.dylib
- frc.dylib
- fskitd
- geocorrectiond
- gputoolsserviced
- hangreporter
- hangtracerd
- iCloudDriveService
- iMessageApps
- iOSDiagnostics
- iTunesStore
- iTunesStoreFramework
- iTunesStoreUI
- iapd
- icloudMCCKit
- ita.dylib
- itunesstored
- keychainsharingmessagingd
- libAHTRestore.dylib
- libATCommandStudioDynamic.dylib
- libAXSafeCategoryBundle.dylib
- libAXSpeechManager.dylib
- libAccessibility.dylib
- libAppPatch.dylib
- libAppleEXR.dylib
- libAppleSSEExt.dylib
- libAudioStatistics.dylib
- libBASupport.dylib
- libBBUpdaterDynamic_stubs.dylib
- libBasebandDiagnostic.dylib
- libCTGreenTeaLogger.dylib
- libCVMSPluginSupport.dylib
- libCellularDecoders.dylib
- libCommCenterCNTargetData.dylib
- libCommCenterCommandDrivers.dylib
- libCoreFSCache.dylib
- libCoreVMClient.dylib
- libETLDIAGLoggingDynamic.dylib
- libETLDLFDynamic.dylib
- libETLDLOADCoreDumpDynamic.dylib
- libETLDLOADDynamic.dylib
- libETLDMCDynamic.dylib
- libETLDynamic.dylib
- libETLEFSDumpDynamic.dylib
- libETLSAHDynamic.dylib
- libFDRDecode.dylib
- libGFXShared.dylib
- libGLImage.dylib
- libGLProgrammability.dylib
- libGLVMPlugin.dylib
- libGPUSupportMercury.dylib
- libHDLCDynamic.dylib
- libHZ.dylib
- libIOABP.dylib
- libIOACIPC.dylib
- libIOReport.dylib
- libISO2022.dylib
- libMTLCompilerHelper.dylib
- libMainThreadChecker.dylib
- libMatch.1.dylib
- libMobileGestaltExtensions.dylib
- libNFC_Comet.dylib
- libNFC_HAL.dylib
- libORTools.dylib
- libPPM.dylib
- libPPMDataModel.dylib
- libQMIParserDynamic.dylib
- libRoseBooter.dylib
- libRoseUpdater.dylib
- libSESShared.dylib
- libSoftwareUpdateSSO.dylib
- libSpatial.dylib
- libSystemDetermination.dylib
- libSystemHealth.dylib
- libValidationCapsule.dylib
- libVibeSynthEngine.dylib
- libWISSupport.dylib
- libamsupport.dylib
- libcharset.1.dylib
- libcupolicy.dylib
- libdscsym.dylib
- libdyld.dylib
- libfaceCore.dylib
- libheimdal-asn1.dylib
- libhvf.dylib
- libiconv_none.dylib
- liblaunch.dylib
- liblivefiles.plugin.dummy.dylib
- libllvm-lmdb.dylib
- liblockdown.dylib
- liblog_IOHIDFamily.dylib
- liblog_SystemConfiguration.dylib
- liblog_coreacc.dylib
- liblog_geo.dylib
- liblog_mdns.dylib
- liblog_mdnsresponder.dylib
- liblog_network.dylib
- liblog_signpost.description.dylib
- liblog_signpost.dylib
- liblog_signpost.telemetry.dylib
- libmapper_646.dylib
- libmapper_std.dylib
- libmapper_zone.dylib
- libmav_ipc_router_dynamic.dylib
- libmecab.dylib
- libmrc.dylib
- libnetquality.dylib
- libnetwork.dylib
- libnfstorage.dylib
- libolaf.dylib
- libpartition2_dynamic.dylib
- libprequelite.dylib
- libskit.dylib
- libswiftAVFoundation.dylib
- libswiftAssetsLibrary.dylib
- libswiftCarPlay.dylib
- libswiftCore.dylib
- libswiftCoreML.dylib
- libswiftCoreMedia.dylib
- libswiftCryptoTokenKit.dylib
- libswiftDarwin.dylib
- libswiftDemangle.dylib
- libswiftDistributed.dylib
- libswiftFileProvider.dylib
- libswiftHealthKit.dylib
- libswiftHomeKit.dylib
- libswiftIdentityLookup.dylib
- libswiftMediaPlayer.dylib
- libswiftMetal.dylib
- libswiftNearbyInteraction.dylib
- libswiftNetwork.dylib
- libswiftObservation.dylib
- libswiftPassKit.dylib
- libswiftPhotos.dylib
- libswiftPhotosUI.dylib
- libswiftRegexBuilder.dylib
- libswiftSpatial.dylib
- libswiftSwiftOnoneSupport.dylib
- libswiftUIKit.dylib
- libswiftUniformTypeIdentifiers.dylib
- libswiftVideoToolbox.dylib
- libswiftWebKit.dylib
- libswift_Concurrency.dylib
- libswift_Differentiation.dylib
- libswift_RegexParser.dylib
- libswift_StringProcessing.dylib
- libsysdiagnose.dylib
- libsystem_collections.dylib
- libsystem_configuration.dylib
- libsystem_darwin.dylib
- libsystem_dnssd.dylib
- libsystem_kernel.dylib
- libsystem_m.dylib
- libsystem_symptoms.dylib
- libsystem_trace.dylib
- libsystemstats.dylib
- libtailspin.dylib
- libusrtcp.dylib
- libutil.dylib
- libvDSP.dylib
- libxml2.2.dylib
- libxpc_datastores.dylib
- libz.1.dylib
- livefiles_apfs.dylib
- livefiles_exfat.dylib
- livefiles_ntfs.dylib
- localspeechrecognition
- locationd.events
- managedappdistributiond
- microstackshot
- mscamerad-xpc
- newfs_apfs
- powerlogHelperd
- ptb.dylib
- ptpcamerad
- ptpd
- replayd
- snatmap
- softwareupdated
- suggest_tool
- tailspind
- terminusd
- triald_system
- usbsmartcardreaderd
- useractivityd
- vCard

</details>
