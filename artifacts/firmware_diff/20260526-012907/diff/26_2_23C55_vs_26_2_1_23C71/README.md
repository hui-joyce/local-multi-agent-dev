# 26.2 (23C55) .vs 26.2.1 (23C71)

## Inputs

- `iPhone18,1_26.2_23C55_Restore.ipsw`
- `iPhone18,1_26.2.1_23C71_Restore.ipsw`

## Kernel

### Version

| iOS | Version | Build | Date |
| :-- | :------ | :---- | :--- |
| 26.2 *(23C55)* | 25.2.0 | 12377.62.10~1 | Tue, 18Nov2025 21:11:04 PST |
| 26.2.1 *(23C71)* | 25.2.0 | 12377.62.10~267 | Fri, 09Jan2026 18:29:04 PST |

### Kexts

### ⬆️ Updated (2)

<details>
  <summary><i>View Updated</i></summary>

#### com.apple.kernel

>  `com.apple.kernel`

```diff

 12377.62.10.0.0
-  __TEXT.__const: 0x353a0
+  __TEXT.__const: 0x353b0
   __TEXT.__copyio_vectors: 0x2c0
   __TEXT.__cstring: 0x7ca18
   __TEXT.__os_log: 0x3c5cb

   __PLK_LLVM_COV.__llvm_covmap: 0x0
   __PLK_LINKEDIT.__data: 0x0
   __LINKINFO.__symbolsets: 0x471ae
-  UUID: F6D0BE58-5B4C-39B5-89D6-8CCE7D005882
+  UUID: 1C8880A4-4F76-3DC2-8E39-2AECD072C76A
   Functions: 20560
   Symbols:   0
   CStrings:  0

```

#### com.apple.security.AppleImage4

>  `com.apple.security.AppleImage4`

```diff

 349.60.2.0.0
   __TEXT.__const: 0x9eef
   __TEXT.__cstring: 0x6193
-  __TEXT.__info_plist: 0x4e7
+  __TEXT.__info_plist: 0x4e2
   __TEXT_EXEC.__text: 0x23648
   __TEXT_EXEC.__auth_stubs: 0x0
   __DATA.__data: 0x8f8

   __DATA_CONST.__const: 0xc1b8
   __DATA_CONST.__kalloc_type: 0x200
   __DATA_CONST.__image4_exp: 0x10
-  UUID: 4DB9E9C4-85DE-38EB-8A10-D2467395959D
+  UUID: 1E264307-0CA6-3243-BE52-7BFE1588323A
   Functions: 1117
   Symbols:   0
   CStrings:  0

```


</details>

## MachO

### ⬆️ Updated (456)

<details>
  <summary><i>View Updated</i></summary>

- [/Applications/KaleidoscopePosterApp.app/Extensions/KaleidoscopePoster.appex/NTKKaleidoscopeShaders.metallib](MACHOS/NTKKaleidoscopeShaders.metallib.md)
- [/Applications/SoftwareUpdateUIService.app/SoftwareUpdateUIService](MACHOS/SoftwareUpdateUIService.md)
- [/System/Library/Audio/Plug-Ins/usbaudio.bundle/usbaudiod](MACHOS/usbaudiod.md)
- [/System/Library/CoreImage/PortraitFilters.cifilter/portrait_filters_archive_bin.metallib](MACHOS/portrait_filters_archive_bin.metallib.md)
- [/System/Library/CoreImage/PortraitFilters.cifilter/portrait_filters_fullsize_archive_bin.metallib](MACHOS/portrait_filters_fullsize_archive_bin.metallib.md)
- [/System/Library/CoreServices/appplaceholdersyncd](MACHOS/appplaceholdersyncd.md)
- [/System/Library/CoreServices/diagnosticservicesd](MACHOS/diagnosticservicesd.md)
- [/System/Library/CoreServices/iconservicesagent](MACHOS/iconservicesagent.md)
- [/System/Library/CoreServices/osanalyticshelper](MACHOS/osanalyticshelper.md)
- [/System/Library/DataClassMigrators/SystemAppMigrator.migrator/SystemAppMigrator](MACHOS/SystemAppMigrator.md)
- [/System/Library/ExtensionKit/Extensions/MercuryPosterExtension.appex/Space.metallib](MACHOS/Space.metallib.md)
- [/System/Library/ExtensionKit/Extensions/ProductPageExtension.appex/ProductPageExtension](MACHOS/ProductPageExtension.md)
- [/System/Library/ExtensionKit/Extensions/SubscribePageExtension.appex/SubscribePageExtension](MACHOS/SubscribePageExtension.md)
- [/System/Library/Frameworks/Accounts.framework/accountsd](MACHOS/accountsd.md)
- [/System/Library/Frameworks/AdAttributionKit.framework/Support/attributionkitd](MACHOS/attributionkitd.md)
- [/System/Library/Frameworks/AssetsLibrary.framework/Support/assetsd](MACHOS/assetsd.md)
- [/System/Library/Frameworks/CFNetwork.framework/AuthBrokerAgent](MACHOS/AuthBrokerAgent.md)
- [/System/Library/Frameworks/CFNetwork.framework/CFNetworkAgent](MACHOS/CFNetworkAgent.md)
- [/System/Library/Frameworks/ClassKit.framework/progressd](MACHOS/progressd.md)
- [/System/Library/Frameworks/Contacts.framework/Support/contactsd](MACHOS/contactsd.md)
- [/System/Library/Frameworks/Contacts.framework/Support/postersyncd](MACHOS/postersyncd.md)
- [/System/Library/Frameworks/CoreImage.framework/ci_uberwrapper_bin.metallib](MACHOS/ci_uberwrapper_bin.metallib.md)
- [/System/Library/Frameworks/CoreImage.framework/coreui_archive_bin.metallib](MACHOS/coreui_archive_bin.metallib.md)
- [/System/Library/Frameworks/CoreImage.framework/photo_style_archive_bin.metallib](MACHOS/photo_style_archive_bin.metallib.md)
- [/System/Library/Frameworks/CoreImage.framework/redeye_repair_archive_bin.metallib](MACHOS/redeye_repair_archive_bin.metallib.md)
- [/System/Library/Frameworks/CoreImage.framework/ubershader_archive_bin.metallib](MACHOS/ubershader_archive_bin.metallib.md)
- [/System/Library/Frameworks/CoreSpotlight.framework/CoreSpotlightService](MACHOS/CoreSpotlightService.md)
- [/System/Library/Frameworks/CoreSpotlight.framework/Support/com.apple.spotlight.IndexAgent](MACHOS/com.apple.spotlight.IndexAgent.md)
- [/System/Library/Frameworks/CoreSpotlight.framework/spotlightknowledged](MACHOS/spotlightknowledged.md)
- [/System/Library/Frameworks/CoreTelephony.framework/Support/CommCenterMobileHelper](MACHOS/CommCenterMobileHelper.md)
- [/System/Library/Frameworks/CoreTelephony.framework/Support/CommCenterRootHelper](MACHOS/CommCenterRootHelper.md)
- [/System/Library/Frameworks/CryptoTokenKit.framework/ctkd](MACHOS/ctkd.md)
- [/System/Library/Frameworks/FamilyControls.framework/FamilyControlsAgent](MACHOS/FamilyControlsAgent.md)
- [/System/Library/Frameworks/FileProvider.framework/Support/fileproviderd](MACHOS/fileproviderd.md)
- [/System/Library/Frameworks/FinanceKit.framework/financed](MACHOS/financed.md)
- [/System/Library/Frameworks/ImageIO.framework/archive.metallib](MACHOS/archive.metallib.md)
- [/System/Library/Frameworks/LocalAuthentication.framework/Support/coreauthd](MACHOS/coreauthd.md)
- [/System/Library/Frameworks/ManagedAppDistribution.framework/Support/applicensedeliveryd](MACHOS/applicensedeliveryd.md)
- [/System/Library/Frameworks/ManagedAppDistribution.framework/Support/managedappdistributiond](MACHOS/managedappdistributiond.md)
- [/System/Library/Frameworks/ManagedSettings.framework/ManagedSettingsAgent](MACHOS/ManagedSettingsAgent.md)
- [/System/Library/Frameworks/ShazamKit.framework/shazamd](MACHOS/shazamd.md)
- [/System/Library/Frameworks/StoreKit.framework/Support/storekitd](MACHOS/storekitd.md)
- [/System/Library/Frameworks/Translation.framework/translationd](MACHOS/translationd.md)
- [/System/Library/Frameworks/WirelessInsights.framework/Support/wirelessinsightsd](MACHOS/wirelessinsightsd.md)
- [/System/Library/Messages/iMessageBalloons/ASMessagesProvider.bundle/ASMessagesProvider](MACHOS/ASMessagesProvider.md)
- [/System/Library/NanoTimeKit/FaceBundles/KaleidoscopeFaceBundle.bundle/NTKKaleidoscopeShaders.metallib](MACHOS/NTKKaleidoscopeShaders.metallib.md)
- [/System/Library/NanoTimeKit/FaceBundles/NTKWarlockFaceBundle.bundle/warlock.metallib](MACHOS/warlock.metallib.md)
- [/System/Library/PreferenceBundles/AccountSettings/AppleAccountSettings.bundle/AppleAccountSettings](MACHOS/AppleAccountSettings.md)
- [/System/Library/PrivateFrameworks/ABMHelper.framework/Support/abm-helper](MACHOS/abm-helper.md)
- [/System/Library/PrivateFrameworks/ACTFramework.framework/binaryArchive.g18p](MACHOS/binaryArchive.g18p.md)
- [/System/Library/PrivateFrameworks/ARKitCore.framework/deflicker-binary-applegpu_g18p.metallib](MACHOS/deflicker-binary-applegpu_g18p.metallib.md)
- [/System/Library/PrivateFrameworks/ARKitCore.framework/deflicker-binary.metallib](MACHOS/deflicker-binary.metallib.md)
- [/System/Library/PrivateFrameworks/AXAssetLoader.framework/Support/axassetsd](MACHOS/axassetsd.md)
- [/System/Library/PrivateFrameworks/AccessibilityRemoteServices.framework/Support/axremoted](MACHOS/axremoted.md)
- [/System/Library/PrivateFrameworks/AccessibilitySharedSupport.framework/Support/motiontrackingd](MACHOS/motiontrackingd.md)
- [/System/Library/PrivateFrameworks/ActivityAwardsServices.framework/activityawardsd](MACHOS/activityawardsd.md)
- [/System/Library/PrivateFrameworks/ActivitySharingServices.framework/activitysharingd](MACHOS/activitysharingd.md)
- [/System/Library/PrivateFrameworks/AppInstallationMetrics.framework/Support/appinstallationmetricsd](MACHOS/appinstallationmetricsd.md)
- [/System/Library/PrivateFrameworks/AppSSO.framework/Support/AppSSODaemon](MACHOS/AppSSODaemon.md)
- [/System/Library/PrivateFrameworks/AppStoreComponents.framework/Support/appstorecomponentsd](MACHOS/appstorecomponentsd.md)
- [/System/Library/PrivateFrameworks/AppStoreDaemon.framework/Support/appstored](MACHOS/appstored.md)
- [/System/Library/PrivateFrameworks/AppleCredentialManager.framework/AppleCredentialManagerDaemon](MACHOS/AppleCredentialManagerDaemon.md)
- [/System/Library/PrivateFrameworks/AppleMediaServices.framework/amsaccountsd](MACHOS/amsaccountsd.md)
- [/System/Library/PrivateFrameworks/AppleMediaServicesUI.framework/amsengagementd](MACHOS/amsengagementd.md)
- [/System/Library/PrivateFrameworks/ApplePushService.framework/apsd](MACHOS/apsd.md)
- [/System/Library/PrivateFrameworks/AssistantServices.framework/assistantd](MACHOS/assistantd.md)
- [/System/Library/PrivateFrameworks/AuthKit.framework/akd](MACHOS/akd.md)
- [/System/Library/PrivateFrameworks/AvatarPersistence.framework/Support/avatarsd](MACHOS/avatarsd.md)
- [/System/Library/PrivateFrameworks/BarcodeSupport.framework/com.apple.BarcodeSupport.BarcodeNotificationService](MACHOS/com.apple.BarcodeSupport.BarcodeNotificationService.md)
- [/System/Library/PrivateFrameworks/BiomeStreams.framework/Support/biomed](MACHOS/biomed.md)
- [/System/Library/PrivateFrameworks/BookDataStore.framework/Support/bookdatastored](MACHOS/bookdatastored.md)
- [/System/Library/PrivateFrameworks/BookLibraryCore.framework/Support/bookassetd](MACHOS/bookassetd.md)
- [/System/Library/PrivateFrameworks/BusinessChatService.framework/businessservicesd](MACHOS/businessservicesd.md)
- [/System/Library/PrivateFrameworks/CMCapture.framework/BWPreviewStitcherNodeCoreImageArchive_bin.metallib](MACHOS/BWPreviewStitcherNodeCoreImageArchive_bin.metallib.md)
- [/System/Library/PrivateFrameworks/CMCapture.framework/BWVideoPIPOverlayNodeCoreImageArchive_bin.metallib](MACHOS/BWVideoPIPOverlayNodeCoreImageArchive_bin.metallib.md)
- [/System/Library/PrivateFrameworks/CalendarDaemon.framework/Support/calaccessd](MACHOS/calaccessd.md)
- [/System/Library/PrivateFrameworks/CallHistory.framework/Support/CallHistorySyncHelper](MACHOS/CallHistorySyncHelper.md)
- [/System/Library/PrivateFrameworks/CallHistory.framework/Support/callhistoryd](MACHOS/callhistoryd.md)
- [/System/Library/PrivateFrameworks/CallIntelligence.framework/callintelligenced](MACHOS/callintelligenced.md)
- [/System/Library/PrivateFrameworks/CameraUI.framework/FRSVCoreImageArchive_bin.metallib](MACHOS/FRSVCoreImageArchive_bin.metallib.md)
- [/System/Library/PrivateFrameworks/CameraUI.framework/Support/nebulad](MACHOS/nebulad.md)
- [/System/Library/PrivateFrameworks/ChatKit.framework/companionmessagesd](MACHOS/companionmessagesd.md)
- [/System/Library/PrivateFrameworks/ChronoCore.framework/Support/chronod](MACHOS/chronod.md)
- [/System/Library/PrivateFrameworks/ClipServices.framework/clipserviced](MACHOS/clipserviced.md)
- [/System/Library/PrivateFrameworks/CloudKitDaemon.framework/Support/ckdiscretionaryd](MACHOS/ckdiscretionaryd.md)
- [/System/Library/PrivateFrameworks/CloudKitDaemon.framework/Support/cloudd](MACHOS/cloudd.md)
- [/System/Library/PrivateFrameworks/CloudPhotoLibrary.framework/Support/cloudphotod](MACHOS/cloudphotod.md)
- [/System/Library/PrivateFrameworks/CloudServices.framework/Helpers/com.apple.sbd](MACHOS/com.apple.sbd.md)
- [/System/Library/PrivateFrameworks/CloudSubscriptionFeatures.framework/featureaccessd](MACHOS/featureaccessd.md)
- [/System/Library/PrivateFrameworks/CommunicationTrust.framework/Support/communicationtrustd](MACHOS/communicationtrustd.md)
- [/System/Library/PrivateFrameworks/CommunicationsFilter.framework/CMFSyncAgent](MACHOS/CMFSyncAgent.md)
- [/System/Library/PrivateFrameworks/CompanionInferenceCore.framework/companioninferenceserviced](MACHOS/companioninferenceserviced.md)
- [/System/Library/PrivateFrameworks/ContactsDonation.framework/Versions/A/Support/contactsdonationagent](MACHOS/contactsdonationagent.md)
- [/System/Library/PrivateFrameworks/ContinuousDialogManagerService.framework/assistant_cdmd](MACHOS/assistant_cdmd.md)
- [/System/Library/PrivateFrameworks/CoreAccessories.framework/Support/accessoryd](MACHOS/accessoryd.md)
- [/System/Library/PrivateFrameworks/CoreAnalytics.framework/Support/analyticsagent](MACHOS/analyticsagent.md)
- [/System/Library/PrivateFrameworks/CoreCDP.framework/cdpd](MACHOS/cdpd.md)
- [/System/Library/PrivateFrameworks/CoreDuetContext.framework/Resources/contextstored](MACHOS/contextstored.md)
- [/System/Library/PrivateFrameworks/CoreFollowUp.framework/followupd](MACHOS/followupd.md)
- [/System/Library/PrivateFrameworks/CoreRE.framework/default-binaryarchive.metallib](MACHOS/default-binaryarchive.metallib.md)
- [/System/Library/PrivateFrameworks/CoreRE.framework/mxi-binaryarchive.metallib](MACHOS/mxi-binaryarchive.metallib.md)
- [/System/Library/PrivateFrameworks/CoreRE3DGSFoundation.framework/archive.metallib](MACHOS/archive.metallib.md)
- [/System/Library/PrivateFrameworks/CoreSpeech.framework/corespeechd](MACHOS/corespeechd.md)
- [/System/Library/PrivateFrameworks/CoreSpeech.framework/speechmodeltrainingd](MACHOS/speechmodeltrainingd.md)
- [/System/Library/PrivateFrameworks/CoreSuggestions.framework/reversetemplated](MACHOS/reversetemplated.md)
- [/System/Library/PrivateFrameworks/CoreSuggestions.framework/suggestd](MACHOS/suggestd.md)
- [/System/Library/PrivateFrameworks/CoreThreadCommissionerService.framework/CoreThreadCommissionerServiced](MACHOS/CoreThreadCommissionerServiced.md)
- [/System/Library/PrivateFrameworks/CoreThreadRadio.framework/threadradiod](MACHOS/threadradiod.md)
- [/System/Library/PrivateFrameworks/DVTInstrumentsFoundation.framework/DTServiceHub](MACHOS/DTServiceHub.md)
- [/System/Library/PrivateFrameworks/DVTInstrumentsFoundation.framework/LeakAgent](MACHOS/LeakAgent.md)
- [/System/Library/PrivateFrameworks/DVTInstrumentsFoundation.framework/RemoteInjectionAgent](MACHOS/RemoteInjectionAgent.md)
- [/System/Library/PrivateFrameworks/DataAccess.framework/Support/dataaccessd](MACHOS/dataaccessd.md)
- [/System/Library/PrivateFrameworks/DesktopServicesPriv.framework/DesktopServicesHelper](MACHOS/DesktopServicesHelper.md)
- [/System/Library/PrivateFrameworks/DoNotDisturbServer.framework/Support/donotdisturbd](MACHOS/donotdisturbd.md)
- [/System/Library/PrivateFrameworks/DragUI.framework/Support/druid](MACHOS/druid.md)
- [/System/Library/PrivateFrameworks/EcosystemAnalytics.framework/Support/ecosystemanalyticsd](MACHOS/ecosystemanalyticsd.md)
- [/System/Library/PrivateFrameworks/EmailDaemon.framework/maild](MACHOS/maild.md)
- [/System/Library/PrivateFrameworks/EmbeddedDataReset.framework/Support/devicedataresetd](MACHOS/devicedataresetd.md)
- [/System/Library/PrivateFrameworks/ExchangeSync.framework/Support/exchangesyncd](MACHOS/exchangesyncd.md)
- [/System/Library/PrivateFrameworks/Eyedropper.framework/Support/eyedropperd](MACHOS/eyedropperd.md)
- [/System/Library/PrivateFrameworks/FaceTimeMessageStore.framework/facetimemessagestored](MACHOS/facetimemessagestored.md)
- [/System/Library/PrivateFrameworks/FamilyCircle.framework/familycircled](MACHOS/familycircled.md)
- [/System/Library/PrivateFrameworks/FileIndexerDaemon.framework/Support/fileindexerd](MACHOS/fileindexerd.md)
- [/System/Library/PrivateFrameworks/FinHealth.framework/finhealthd](MACHOS/finhealthd.md)
- [/System/Library/PrivateFrameworks/FitnessCoachingServices.framework/fitnesscoachingd](MACHOS/fitnesscoachingd.md)
- [/System/Library/PrivateFrameworks/FitnessIntelligenceDaemonCore.framework/fitnessintelligenced](MACHOS/fitnessintelligenced.md)
- [/System/Library/PrivateFrameworks/FontServices.framework/Support/fontservicesd](MACHOS/fontservicesd.md)
- [/System/Library/PrivateFrameworks/GenerationalStorage.framework/revisiond](MACHOS/revisiond.md)
- [/System/Library/PrivateFrameworks/GenerativeExperiencesRuntime.framework/generativeexperiencesd](MACHOS/generativeexperiencesd.md)
- [/System/Library/PrivateFrameworks/GeoAnalytics.framework/geoanalyticsd](MACHOS/geoanalyticsd.md)
- [/System/Library/PrivateFrameworks/GeoServices.framework/geod](MACHOS/geod.md)
- [/System/Library/PrivateFrameworks/HealthPluginHost.framework/healthappd](MACHOS/healthappd.md)
- [/System/Library/PrivateFrameworks/HearingCore.framework/heard](MACHOS/heard.md)
- [/System/Library/PrivateFrameworks/HomeEnergyDaemon.framework/Support/homeenergyd](MACHOS/homeenergyd.md)
- [/System/Library/PrivateFrameworks/HomeKitDaemon.framework/Support/homed](MACHOS/homed.md)
- [/System/Library/PrivateFrameworks/HomeKitEvents.framework/Support/homeeventsd](MACHOS/homeeventsd.md)
- [/System/Library/PrivateFrameworks/IAP.framework/Support/iapd](MACHOS/iapd.md)
- [/System/Library/PrivateFrameworks/IAP.framework/Support/iaptransportd](MACHOS/iaptransportd.md)
- [/System/Library/PrivateFrameworks/IAPAuthentication.framework/Support/iapauthd](MACHOS/iapauthd.md)
- [/System/Library/PrivateFrameworks/InstallCoordination.framework/Support/installcoordinationd](MACHOS/installcoordinationd.md)
- [/System/Library/PrivateFrameworks/IntelligenceFlowContextRuntime.framework/intelligencecontextd](MACHOS/intelligencecontextd.md)
- [/System/Library/PrivateFrameworks/IntelligenceFlowRuntime.framework/intelligenceflowd](MACHOS/intelligenceflowd.md)
- [/System/Library/PrivateFrameworks/IntelligencePlatformCore.framework/intelligenceplatformd](MACHOS/intelligenceplatformd.md)
- [/System/Library/PrivateFrameworks/IntelligencePlatformCore.framework/knowledgeconstructiond](MACHOS/knowledgeconstructiond.md)
- [/System/Library/PrivateFrameworks/IntelligenceTasksEngine.framework/Support/intelligencetasksd](MACHOS/intelligencetasksd.md)
- [/System/Library/PrivateFrameworks/IntentRecommendRuntime.framework/intentrecommendd](MACHOS/intentrecommendd.md)
- [/System/Library/PrivateFrameworks/JetCore.framework/Support/jetpackassetd](MACHOS/jetpackassetd.md)
- [/System/Library/PrivateFrameworks/LockdownMode.framework/lockdownmoded](MACHOS/lockdownmoded.md)
- [/System/Library/PrivateFrameworks/MXI.framework/mxi_archive.metallib](MACHOS/mxi_archive.metallib.md)
- [/System/Library/PrivateFrameworks/MapsSuggestions.framework/destinationd](MACHOS/destinationd.md)
- [/System/Library/PrivateFrameworks/MapsSupport.framework/geocorrectiond](MACHOS/geocorrectiond.md)
- [/System/Library/PrivateFrameworks/MapsSupport.framework/mapspushd](MACHOS/mapspushd.md)
- [/System/Library/PrivateFrameworks/MapsSync.framework/mapssyncd](MACHOS/mapssyncd.md)
- [/System/Library/PrivateFrameworks/MediaAnalysis.framework/mediaanalysisd](MACHOS/mediaanalysisd.md)
- [/System/Library/PrivateFrameworks/MediaAnalysis.framework/mediaanalysisd-service](MACHOS/mediaanalysisd-service.md)
- [/System/Library/PrivateFrameworks/MediaRemote.framework/Support/mediaremoted](MACHOS/mediaremoted.md)
- [/System/Library/PrivateFrameworks/MediaServices.framework/Support/mediaartworkd](MACHOS/mediaartworkd.md)
- [/System/Library/PrivateFrameworks/MediaStream.framework/Support/mstreamd](MACHOS/mstreamd.md)
- [/System/Library/PrivateFrameworks/MobileAccessoryUpdater.framework/Support/accessoryupdaterd](MACHOS/accessoryupdaterd.md)
- [/System/Library/PrivateFrameworks/MobileAccessoryUpdater.framework/Support/auearlyboot](MACHOS/auearlyboot.md)
- [/System/Library/PrivateFrameworks/MobileBackup.framework/MobileBackupCacheDeleteService](MACHOS/MobileBackupCacheDeleteService.md)
- [/System/Library/PrivateFrameworks/MobileBackup.framework/backupd](MACHOS/backupd.md)
- [/System/Library/PrivateFrameworks/MobileInstallation.framework/XPCServices/com.apple.MobileInstallationHelperService.xpc/com.apple.MobileInstallationHelperService](MACHOS/com.apple.MobileInstallationHelperService.md)
- [/System/Library/PrivateFrameworks/MobileSoftwareUpdate.framework/Support/softwareupdated](MACHOS/softwareupdated.md)
- [/System/Library/PrivateFrameworks/MobileTimer.framework/Executables/mobiletimerd](MACHOS/mobiletimerd.md)
- [/System/Library/PrivateFrameworks/MusicLibrary.framework/Support/medialibraryd](MACHOS/medialibraryd.md)
- [/System/Library/PrivateFrameworks/NanoPassKit.framework/NPKCompanionAgent](MACHOS/NPKCompanionAgent.md)
- [/System/Library/PrivateFrameworks/NanoSystemSettings.framework/nanosystemsettingsd](MACHOS/nanosystemsettingsd.md)
- [/System/Library/PrivateFrameworks/NanoTimeKit.framework/nanotimekitcompaniond](MACHOS/nanotimekitcompaniond.md)
- [/System/Library/PrivateFrameworks/NanoUniverse.framework/NUNICalliopeShadersCompanion.metallib](MACHOS/NUNICalliopeShadersCompanion.metallib.md)
- [/System/Library/PrivateFrameworks/NewsDaemon.framework/newsd](MACHOS/newsd.md)
- [/System/Library/PrivateFrameworks/NewsServices.framework/nanonewscd](MACHOS/nanonewscd.md)
- [/System/Library/PrivateFrameworks/OmniSearch.framework/searchtoold](MACHOS/searchtoold.md)
- [/System/Library/PrivateFrameworks/OnDeviceStorage.framework/Support/amsondevicestoraged](MACHOS/amsondevicestoraged.md)
- [/System/Library/PrivateFrameworks/PassKitCore.framework/passd](MACHOS/passd.md)
- [/System/Library/PrivateFrameworks/People.framework/peopled](MACHOS/peopled.md)
- [/System/Library/PrivateFrameworks/PhotoAnalysis.framework/Support/photoanalysisd](MACHOS/photoanalysisd.md)
- [/System/Library/PrivateFrameworks/PointerUIServices.framework/Support/pointeruid](MACHOS/pointeruid.md)
- [/System/Library/PrivateFrameworks/PreviewsOSSupport.framework/Support/previewsd](MACHOS/previewsd.md)
- [/System/Library/PrivateFrameworks/PrivacyAccounting.framework/Versions/A/Resources/privacyaccountingd](MACHOS/privacyaccountingd.md)
- [/System/Library/PrivateFrameworks/ProtectedCloudStorage.framework/Helpers/ProtectedCloudKeySyncing](MACHOS/ProtectedCloudKeySyncing.md)
- [/System/Library/PrivateFrameworks/Recon3D.framework/Reconstruction_Gpu_Archive.metallib](MACHOS/Reconstruction_Gpu_Archive.metallib.md)
- [/System/Library/PrivateFrameworks/RemoteManagement.framework/RemoteManagementAgent](MACHOS/RemoteManagementAgent.md)
- [/System/Library/PrivateFrameworks/RemoteManagement.framework/remotemanagementd](MACHOS/remotemanagementd.md)
- [/System/Library/PrivateFrameworks/RemoteManagement.framework/rmdinspect](MACHOS/rmdinspect.md)
- [/System/Library/PrivateFrameworks/RenderBox.framework/archive.metallib](MACHOS/archive.metallib.md)
- [/System/Library/PrivateFrameworks/ReplicatorCore.framework/Support/replicatord](MACHOS/replicatord.md)
- [/System/Library/PrivateFrameworks/SMBClientProvider.framework/smbclientd](MACHOS/smbclientd.md)
- [/System/Library/PrivateFrameworks/SOS.framework/sosd](MACHOS/sosd.md)
- [/System/Library/PrivateFrameworks/SchoolTime.framework/Support/schooltimed](MACHOS/schooltimed.md)
- [/System/Library/PrivateFrameworks/ScreenTimeCore.framework/ScreenTimeAgent](MACHOS/ScreenTimeAgent.md)
- [/System/Library/PrivateFrameworks/SecureMessaging.framework/SecureMessagingAgent](MACHOS/SecureMessagingAgent.md)
- [/System/Library/PrivateFrameworks/ServicesIntelligence.framework/servicesintelligenced](MACHOS/servicesintelligenced.md)
- [/System/Library/PrivateFrameworks/SessionCore.framework/Support/liveactivitiesd](MACHOS/liveactivitiesd.md)
- [/System/Library/PrivateFrameworks/SeymourServices.framework/fitcored](MACHOS/fitcored.md)
- [/System/Library/PrivateFrameworks/SeymourServices.framework/fitcoresessiond](MACHOS/fitcoresessiond.md)
- [/System/Library/PrivateFrameworks/SiriInference.framework/Support/siriinferenced](MACHOS/siriinferenced.md)
- [/System/Library/PrivateFrameworks/SiriTTSService.framework/sirittsd](MACHOS/sirittsd.md)
- [/System/Library/PrivateFrameworks/SiriTTSTraining.framework/SiriTTSTrainingAgent](MACHOS/SiriTTSTrainingAgent.md)
- [/System/Library/PrivateFrameworks/SiriUICore.framework/archive.metallib](MACHOS/archive.metallib.md)
- [/System/Library/PrivateFrameworks/SiriVOX.framework/SiriHeadlessService](MACHOS/SiriHeadlessService.md)
- [/System/Library/PrivateFrameworks/SleepDaemon.framework/sleepd](MACHOS/sleepd.md)
- [/System/Library/PrivateFrameworks/SoftwareUpdateBridge.framework/Support/subridged](MACHOS/subridged.md)
- [/System/Library/PrivateFrameworks/SoftwareUpdateServices.framework/PlugIns/SUSFollowUpExtension.appex/SUSFollowUpExtension](MACHOS/SUSFollowUpExtension.md)
- [/System/Library/PrivateFrameworks/SoftwareUpdateServicesUI.framework/Plugins/SoftwareUpdateServicesUIPlugin.servicebundle/SoftwareUpdateServicesUIPlugin](MACHOS/SoftwareUpdateServicesUIPlugin.md)
- [/System/Library/PrivateFrameworks/StatusKit.framework/StatusKitAgent](MACHOS/StatusKitAgent.md)
- [/System/Library/PrivateFrameworks/Stickers.framework/Support/stickersd](MACHOS/stickersd.md)
- [/System/Library/PrivateFrameworks/Synapse.framework/Support/contentlinkingd](MACHOS/contentlinkingd.md)
- [/System/Library/PrivateFrameworks/SyncedDefaults.framework/Support/syncdefaultsd](MACHOS/syncdefaultsd.md)
- [/System/Library/PrivateFrameworks/SystemStatusServer.framework/Support/systemstatusd](MACHOS/systemstatusd.md)
- [/System/Library/PrivateFrameworks/TCC.framework/Support/tccd](MACHOS/tccd.md)
- [/System/Library/PrivateFrameworks/TelephonyUtilities.framework/callservicesd](MACHOS/callservicesd.md)
- [/System/Library/PrivateFrameworks/TextToSpeechVoiceBankingSupport.framework/Support/voicebankingd](MACHOS/voicebankingd.md)
- [/System/Library/PrivateFrameworks/UsageTracking.framework/UsageTrackingAgent](MACHOS/UsageTrackingAgent.md)
- [/System/Library/PrivateFrameworks/UserActivity.framework/Agents/useractivityd](MACHOS/useractivityd.md)
- [/System/Library/PrivateFrameworks/UserNotificationsCore.framework/Support/usernotificationsd](MACHOS/usernotificationsd.md)
- [/System/Library/PrivateFrameworks/VectorKit.framework/metal_libraries/binary.metallib](MACHOS/binary.metallib.md)
- [/System/Library/PrivateFrameworks/VisualVoicemail.framework/vmd](MACHOS/vmd.md)
- [/System/Library/PrivateFrameworks/VoiceServices.framework/Support/voiced](MACHOS/voiced.md)
- [/System/Library/PrivateFrameworks/VoiceShortcuts.framework/Support/siriactionsd](MACHOS/siriactionsd.md)
- [/System/Library/PrivateFrameworks/WatchListKit.framework/Support/watchlistd](MACHOS/watchlistd.md)
- [/System/Library/PrivateFrameworks/WeatherDaemon.framework/weatherd](MACHOS/weatherd.md)
- [/System/Library/PrivateFrameworks/WebPrivacy.framework/webprivacyd](MACHOS/webprivacyd.md)
- [/System/Library/PrivateFrameworks/WiFiPolicy.framework/XPCServices/WiFiCloudAssetsXPCService.xpc/WiFiCloudAssetsXPCService](MACHOS/WiFiCloudAssetsXPCService.md)
- [/System/Library/PrivateFrameworks/iCloudDriveCore.framework/bird](MACHOS/bird.md)
- [/System/Library/PrivateFrameworks/iCloudSubscriptionOptimizerDaemon.framework/icloudsubscriptionoptimizerd/icloudsubscriptionoptimizerd](MACHOS/icloudsubscriptionoptimizerd.md)
- [/System/Library/PrivateFrameworks/iOSDiagnostics.framework/iosdiagnosticsd](MACHOS/iosdiagnosticsd.md)
- [/System/Library/PrivateFrameworks/iTunesCloud.framework/Support/itunescloudd](MACHOS/itunescloudd.md)
- [/System/Library/Video/Plug-Ins/AppleVideoEncoder.bundle/AppleVideoEncoder](MACHOS/AppleVideoEncoder.md)
- [/System/Library/VideoProcessors/CCPortrait.bundle/ccportrait_archive_bin.metallib](MACHOS/ccportrait_archive_bin.metallib.md)
- [/System/Library/VideoProcessors/ColourConstancyV1.bundle/binaryArchive.g18p_a0](MACHOS/binaryArchive.g18p_a0.md)
- [/System/Library/VideoProcessors/DepthProcessorV2.bundle/binaryArchive.g18p_a0](MACHOS/binaryArchive.g18p_a0.md)
- [/System/Library/VideoProcessors/IntelligentDistortionCorrectionV1.bundle/binaryArchive.g18p](MACHOS/binaryArchive.g18p.md)
- [/System/Library/VideoProcessors/IntelligentDistortionCorrectionV1.bundle/binaryArchive.g18p_a0](MACHOS/binaryArchive.g18p_a0.md)
- [/System/Library/VideoProcessors/MetalFilter.bundle/binaryArchive.g18p_a0](MACHOS/binaryArchive.g18p_a0.md)
- [/System/Library/VideoProcessors/NRFV4.bundle/binaryArchive.g18p](MACHOS/binaryArchive.g18p.md)
- [/System/Library/VideoProcessors/NRFV4.bundle/binaryArchive.g18p_a0](MACHOS/binaryArchive.g18p_a0.md)
- [/System/Library/VideoProcessors/STF.bundle/binaryArchive.g18p_a0](MACHOS/binaryArchive.g18p_a0.md)
- [/System/Library/VideoProcessors/SmartStyleV1.bundle/binaryArchive.g18p_a0](MACHOS/binaryArchive.g18p_a0.md)
- [/System/Library/VideoProcessors/SuperResolutionV2.bundle/binaryArchive.g18p_a0](MACHOS/binaryArchive.g18p_a0.md)
- [/System/Library/VideoProcessors/VideoDeghostingV1.bundle/binaryArchive.g18p](MACHOS/binaryArchive.g18p.md)
- [/System/Library/VideoProcessors/VideoDeghostingV1.bundle/binaryArchive.g18p_a0](MACHOS/binaryArchive.g18p_a0.md)
- [/System/Library/VideoProcessors/VideoDeghostingV2.bundle/binaryArchive.g18p_a0](MACHOS/binaryArchive.g18p_a0.md)
- [/System/Library/VideoProcessors/VideoStabilizationV2.bundle/binaryArchive.g18p](MACHOS/binaryArchive.g18p.md)
- [/System/Library/VideoProcessors/VideoStabilizationV2.bundle/binaryArchive.g18p_a0](MACHOS/binaryArchive.g18p_a0.md)
- [/private/var/staged_system_apps/AppStore.app/AppStore](MACHOS/AppStore.md)
- [/sbin/launchd](MACHOS/launchd.md)
- [/usr/bin/brctl](MACHOS/brctl.md)
- [/usr/bin/footprint](MACHOS/footprint.md)
- [/usr/bin/modelcatalogdump](MACHOS/modelcatalogdump.md)
- [/usr/lib/dyld](MACHOS/dyld.md)
- [/usr/libexec/ASPCarryLog](MACHOS/ASPCarryLog.md)
- [/usr/libexec/AuthenticationServicesAgent](MACHOS/AuthenticationServicesAgent.md)
- [/usr/libexec/ContinuityCaptureAgent](MACHOS/ContinuityCaptureAgent.md)
- [/usr/libexec/DataDetectorsSourceAccess](MACHOS/DataDetectorsSourceAccess.md)
- [/usr/libexec/MTLAssetUpgraderD](MACHOS/MTLAssetUpgraderD.md)
- [/usr/libexec/NANDTaskScheduler](MACHOS/NANDTaskScheduler.md)
- [/usr/libexec/NRDUpdated](MACHOS/NRDUpdated.md)
- [/usr/libexec/PowerUIAgent](MACHOS/PowerUIAgent.md)
- [/usr/libexec/PreboardService](MACHOS/PreboardService.md)
- [/usr/libexec/SensorKitALSHelper](MACHOS/SensorKitALSHelper.md)
- [/usr/libexec/SidecarRelay](MACHOS/SidecarRelay.md)
- [/usr/libexec/ViewHierarchyAgent](MACHOS/ViewHierarchyAgent.md)
- [/usr/libexec/accessorysensormgrd](MACHOS/accessorysensormgrd.md)
- [/usr/libexec/adprivacyd](MACHOS/adprivacyd.md)
- [/usr/libexec/airplayd](MACHOS/airplayd.md)
- [/usr/libexec/amfid](MACHOS/amfid.md)
- [/usr/libexec/announced](MACHOS/announced.md)
- [/usr/libexec/anomalydetectiond](MACHOS/anomalydetectiond.md)
- [/usr/libexec/aonsensed](MACHOS/aonsensed.md)
- [/usr/libexec/appleaccountd](MACHOS/appleaccountd.md)
- [/usr/libexec/appleidsetupd](MACHOS/appleidsetupd.md)
- [/usr/libexec/applekeystored](MACHOS/applekeystored.md)
- [/usr/libexec/appprotectiond](MACHOS/appprotectiond.md)
- [/usr/libexec/arkitd](MACHOS/arkitd.md)
- [/usr/libexec/asktod](MACHOS/asktod.md)
- [/usr/libexec/assessmentagent](MACHOS/assessmentagent.md)
- [/usr/libexec/assetsubscriptiond](MACHOS/assetsubscriptiond.md)
- [/usr/libexec/atc](MACHOS/atc.md)
- [/usr/libexec/audioaccessoryd](MACHOS/audioaccessoryd.md)
- [/usr/libexec/audioclocksyncd](MACHOS/audioclocksyncd.md)
- [/usr/libexec/avconferenced](MACHOS/avconferenced.md)
- [/usr/libexec/backboardd](MACHOS/backboardd.md)
- [/usr/libexec/backgroundassets.user](MACHOS/backgroundassets.user.md)
- [/usr/libexec/batteryintelligenced](MACHOS/batteryintelligenced.md)
- [/usr/libexec/batterytrapd](MACHOS/batterytrapd.md)
- [/usr/libexec/betaenrollmentd](MACHOS/betaenrollmentd.md)
- [/usr/libexec/biomesyncd](MACHOS/biomesyncd.md)
- [/usr/libexec/biometrickitd](MACHOS/biometrickitd.md)
- [/usr/libexec/bluetoothuserd](MACHOS/bluetoothuserd.md)
- [/usr/libexec/brookcompaniond](MACHOS/brookcompaniond.md)
- [/usr/libexec/bulletindistributord](MACHOS/bulletindistributord.md)
- [/usr/libexec/cameracaptured](MACHOS/cameracaptured.md)
- [/usr/libexec/caraccessoryd](MACHOS/caraccessoryd.md)
- [/usr/libexec/carkitd](MACHOS/carkitd.md)
- [/usr/libexec/centaurid](MACHOS/centaurid.md)
- [/usr/libexec/ciphermld](MACHOS/ciphermld.md)
- [/usr/libexec/com.apple.Safari.History](MACHOS/com.apple.Safari.History.md)
- [/usr/libexec/companiond](MACHOS/companiond.md)
- [/usr/libexec/continuitycaptured](MACHOS/continuitycaptured.md)
- [/usr/libexec/coreduetd](MACHOS/coreduetd.md)
- [/usr/libexec/coreidvd](MACHOS/coreidvd.md)
- [/usr/libexec/corercd](MACHOS/corercd.md)
- [/usr/libexec/countryd](MACHOS/countryd.md)
- [/usr/libexec/cryptexd](MACHOS/cryptexd.md)
- [/usr/libexec/dasd](MACHOS/dasd.md)
- [/usr/libexec/deferredmediad](MACHOS/deferredmediad.md)
- [/usr/libexec/demod](MACHOS/demod.md)
- [/usr/libexec/deviceaccessd](MACHOS/deviceaccessd.md)
- [/usr/libexec/devicesharingd](MACHOS/devicesharingd.md)
- [/usr/libexec/diagnosticd](MACHOS/diagnosticd.md)
- [/usr/libexec/diagnosticextensionsd](MACHOS/diagnosticextensionsd.md)
- [/usr/libexec/diskimagesiod](MACHOS/diskimagesiod.md)
- [/usr/libexec/dmd](MACHOS/dmd.md)
- [/usr/libexec/dockaccessoryd](MACHOS/dockaccessoryd.md)
- [/usr/libexec/facemetricsd](MACHOS/facemetricsd.md)
- [/usr/libexec/fairplaydeviceidentityd](MACHOS/fairplaydeviceidentityd.md)
- [/usr/libexec/feedbackd](MACHOS/feedbackd.md)
- [/usr/libexec/findmybeaconingd](MACHOS/findmybeaconingd.md)
- [/usr/libexec/findmydeviced](MACHOS/findmydeviced.md)
- [/usr/libexec/findmylocated](MACHOS/findmylocated.md)
- [/usr/libexec/fmflocatord](MACHOS/fmflocatord.md)
- [/usr/libexec/frauddefensed](MACHOS/frauddefensed.md)
- [/usr/libexec/fskitd](MACHOS/fskitd.md)
- [/usr/libexec/gamecontrollerd](MACHOS/gamecontrollerd.md)
- [/usr/libexec/gamed](MACHOS/gamed.md)
- [/usr/libexec/gamepolicyd](MACHOS/gamepolicyd.md)
- [/usr/libexec/gamesaved](MACHOS/gamesaved.md)
- [/usr/libexec/gpsd](MACHOS/gpsd.md)
- [/usr/libexec/gputoolsserviced](MACHOS/gputoolsserviced.md)
- [/usr/libexec/griddatad](MACHOS/griddatad.md)
- [/usr/libexec/hangtelemetryd](MACHOS/hangtelemetryd.md)
- [/usr/libexec/hangtracerd](MACHOS/hangtracerd.md)
- [/usr/libexec/heartratecoordinatord](MACHOS/heartratecoordinatord.md)
- [/usr/libexec/icloudmailagent](MACHOS/icloudmailagent.md)
- [/usr/libexec/idcredd](MACHOS/idcredd.md)
- [/usr/libexec/inboxupdaterd](MACHOS/inboxupdaterd.md)
- [/usr/libexec/inputanalyticsd](MACHOS/inputanalyticsd.md)
- [/usr/libexec/installd](MACHOS/installd.md)
- [/usr/libexec/keychainsharingmessagingd](MACHOS/keychainsharingmessagingd.md)
- [/usr/libexec/linkd](MACHOS/linkd.md)
- [/usr/libexec/locationaccessstored](MACHOS/locationaccessstored.md)
- [/usr/libexec/locationd](MACHOS/locationd.md)
- [/usr/libexec/locationpushd](MACHOS/locationpushd.md)
- [/usr/libexec/logd](MACHOS/logd.md)
- [/usr/libexec/logd_helper](MACHOS/logd_helper.md)
- [/usr/libexec/logd_reporter](MACHOS/logd_reporter.md)
- [/usr/libexec/managedappsd](MACHOS/managedappsd.md)
- [/usr/libexec/managedassetsd](MACHOS/managedassetsd.md)
- [/usr/libexec/mdmd](MACHOS/mdmd.md)
- [/usr/libexec/mdmuserd](MACHOS/mdmuserd.md)
- [/usr/libexec/mediacontinuityd](MACHOS/mediacontinuityd.md)
- [/usr/libexec/mediaparserd](MACHOS/mediaparserd.md)
- [/usr/libexec/mediaplaybackd](MACHOS/mediaplaybackd.md)
- [/usr/libexec/mediasetupd](MACHOS/mediasetupd.md)
- [/usr/libexec/merchantd](MACHOS/merchantd.md)
- [/usr/libexec/metrickitd](MACHOS/metrickitd.md)
- [/usr/libexec/microstackshot](MACHOS/microstackshot.md)
- [/usr/libexec/mlhostd](MACHOS/mlhostd.md)
- [/usr/libexec/mlruntimed](MACHOS/mlruntimed.md)
- [/usr/libexec/mobile_diagnostics_relay](MACHOS/mobile_diagnostics_relay.md)
- [/usr/libexec/mobile_installation_proxy](MACHOS/mobile_installation_proxy.md)
- [/usr/libexec/mobilerepaird](MACHOS/mobilerepaird.md)
- [/usr/libexec/modelmanagerd](MACHOS/modelmanagerd.md)
- [/usr/libexec/momentsd](MACHOS/momentsd.md)
- [/usr/libexec/nanomediaremotelinkagent](MACHOS/nanomediaremotelinkagent.md)
- [/usr/libexec/nanoregistryd](MACHOS/nanoregistryd.md)
- [/usr/libexec/naturallanguaged](MACHOS/naturallanguaged.md)
- [/usr/libexec/neagent](MACHOS/neagent.md)
- [/usr/libexec/nearbyd](MACHOS/nearbyd.md)
- [/usr/libexec/nehelper](MACHOS/nehelper.md)
- [/usr/libexec/nesessionmanager](MACHOS/nesessionmanager.md)
- [/usr/libexec/networkserviceproxy](MACHOS/networkserviceproxy.md)
- [/usr/libexec/nexusd](MACHOS/nexusd.md)
- [/usr/libexec/nfcd](MACHOS/nfcd.md)
- [/usr/libexec/nptocompaniond](MACHOS/nptocompaniond.md)
- [/usr/libexec/nsurlsessiond](MACHOS/nsurlsessiond.md)
- [/usr/libexec/otpaird](MACHOS/otpaird.md)
- [/usr/libexec/passcodenagd](MACHOS/passcodenagd.md)
- [/usr/libexec/passwordbreachd](MACHOS/passwordbreachd.md)
- [/usr/libexec/photosfaced](MACHOS/photosfaced.md)
- [/usr/libexec/pipelined](MACHOS/pipelined.md)
- [/usr/libexec/pkd](MACHOS/pkd.md)
- [/usr/libexec/powerdatad](MACHOS/powerdatad.md)
- [/usr/libexec/proactiveeventtrackerd](MACHOS/proactiveeventtrackerd.md)
- [/usr/libexec/profiled](MACHOS/profiled.md)
- [/usr/libexec/promotedcontentd](MACHOS/promotedcontentd.md)
- [/usr/libexec/proximitycontrold](MACHOS/proximitycontrold.md)
- [/usr/libexec/ptpassivecollectiond](MACHOS/ptpassivecollectiond.md)
- [/usr/libexec/ptpcamerad](MACHOS/ptpcamerad.md)
- [/usr/libexec/ptpd](MACHOS/ptpd.md)
- [/usr/libexec/rapportd](MACHOS/rapportd.md)
- [/usr/libexec/relatived](MACHOS/relatived.md)
- [/usr/libexec/remindd](MACHOS/remindd.md)
- [/usr/libexec/remoteappintentsd](MACHOS/remoteappintentsd.md)
- [/usr/libexec/remoted](MACHOS/remoted.md)
- [/usr/libexec/remotepairingdeviced](MACHOS/remotepairingdeviced.md)
- [/usr/libexec/remotesoftwareupdated](MACHOS/remotesoftwareupdated.md)
- [/usr/libexec/replayd](MACHOS/replayd.md)
- [/usr/libexec/routined](MACHOS/routined.md)
- [/usr/libexec/rtcreportingd](MACHOS/rtcreportingd.md)
- [/usr/libexec/safarifetcherd](MACHOS/safarifetcherd.md)
- [/usr/libexec/safetyalertsd](MACHOS/safetyalertsd.md)
- [/usr/libexec/searchpartyd](MACHOS/searchpartyd.md)
- [/usr/libexec/sensingpredictd](MACHOS/sensingpredictd.md)
- [/usr/libexec/sensorkitd](MACHOS/sensorkitd.md)
- [/usr/libexec/seserviced](MACHOS/seserviced.md)
- [/usr/libexec/sharingd](MACHOS/sharingd.md)
- [/usr/libexec/siriknowledged](MACHOS/siriknowledged.md)
- [/usr/libexec/sirireaderd](MACHOS/sirireaderd.md)
- [/usr/libexec/softposreaderd](MACHOS/softposreaderd.md)
- [/usr/libexec/soundanalysisd](MACHOS/soundanalysisd.md)
- [/usr/libexec/srp-mdns-proxy](MACHOS/srp-mdns-proxy.md)
- [/usr/libexec/storagedatad](MACHOS/storagedatad.md)
- [/usr/libexec/storagekitd](MACHOS/storagekitd.md)
- [/usr/libexec/swcd](MACHOS/swcd.md)
- [/usr/libexec/swiftuitraced](MACHOS/swiftuitraced.md)
- [/usr/libexec/swtransparencyd](MACHOS/swtransparencyd.md)
- [/usr/libexec/symptomsd](MACHOS/symptomsd.md)
- [/usr/libexec/symptomsd-diag](MACHOS/symptomsd-diag.md)
- [/usr/libexec/symptomsd-distributed](MACHOS/symptomsd-distributed.md)
- [/usr/libexec/terminusd](MACHOS/terminusd.md)
- [/usr/libexec/teslad](MACHOS/teslad.md)
- [/usr/libexec/textcomposerd](MACHOS/textcomposerd.md)
- [/usr/libexec/textcontextd](MACHOS/textcontextd.md)
- [/usr/libexec/textunderstandingd](MACHOS/textunderstandingd.md)
- [/usr/libexec/thermalmonitord](MACHOS/thermalmonitord.md)
- [/usr/libexec/timed](MACHOS/timed.md)
- [/usr/libexec/tipsd](MACHOS/tipsd.md)
- [/usr/libexec/transparencyd](MACHOS/transparencyd.md)
- [/usr/libexec/triald](MACHOS/triald.md)
- [/usr/libexec/triald_system](MACHOS/triald_system.md)
- [/usr/libexec/trustd](MACHOS/trustd.md)
- [/usr/libexec/tursd](MACHOS/tursd.md)
- [/usr/libexec/tvremoted](MACHOS/tvremoted.md)
- [/usr/libexec/uarpassetmanagerd](MACHOS/uarpassetmanagerd.md)
- [/usr/libexec/uarpd](MACHOS/uarpd.md)
- [/usr/libexec/uarphidd](MACHOS/uarphidd.md)
- [/usr/libexec/uarppersonalizationd](MACHOS/uarppersonalizationd.md)
- [/usr/libexec/videocodecd](MACHOS/videocodecd.md)
- [/usr/libexec/videosubscriptionsd](MACHOS/videosubscriptionsd.md)
- [/usr/libexec/visioncompaniond](MACHOS/visioncompaniond.md)
- [/usr/libexec/webbookmarksd](MACHOS/webbookmarksd.md)
- [/usr/libexec/webinspectord](MACHOS/webinspectord.md)
- [/usr/libexec/wifip2pd](MACHOS/wifip2pd.md)
- [/usr/libexec/wifivelocityd](MACHOS/wifivelocityd.md)
- [/usr/libexec/xpcproxy](MACHOS/xpcproxy.md)
- [/usr/libexec/xpcroleaccountd](MACHOS/xpcroleaccountd.md)
- [/usr/sbin/BTAvrcp](MACHOS/BTAvrcp.md)
- [/usr/sbin/BTLEServer](MACHOS/BTLEServer.md)
- [/usr/sbin/WirelessRadioManagerd](MACHOS/WirelessRadioManagerd.md)
- [/usr/sbin/bluetoothd](MACHOS/bluetoothd.md)
- [/usr/sbin/distnoted](MACHOS/distnoted.md)
- [/usr/sbin/mDNSResponderHelper](MACHOS/mDNSResponderHelper.md)
- [/usr/sbin/otctl](MACHOS/otctl.md)
- [/usr/sbin/wifid](MACHOS/wifid.md)

</details>

## Firmware

### ⬆️ Updated (4)

<details>
  <summary><i>View Updated</i></summary>

#### AppleAVE2FW_H18.im4p

>  `AppleAVE2FW_H18.im4p`

```diff

   __TEXT.__chain_starts: 0x20
   __DATA.__const: 0x39b0
   __DATA._rtk_patchbay: 0x211
-  __DATA.__data: 0x16f8
+  __DATA.__data: 0x1700
   __DATA._rtk_mtab: 0x320
   __DATA._rtk_power: 0x3b8
   __DATA.__gxf_data: 0x10

   __DATA._rtk_threads: 0x0
   __DATA.__constructor: 0x0
   __DATA.__zerofill: 0xc6838
-  UUID: AF935BA4-F481-3022-AC11-B5A297C06BEC
+  UUID: 370AA171-D6A5-30F5-8EBF-6FAC89350A47
   Functions: 1212
   Symbols:   1703
   CStrings:  0

```

#### adc-silenus-v5x.im4p

>  `adc-silenus-v5x.im4p`

```diff

 
   __TEXT.__text: 0xb6e764
-  __TEXT.__const: 0x832c54
-  __TEXT.__cstring: 0xaa596
+  __TEXT.__const: 0x832c20
+  __TEXT.__cstring: 0xaa5a2
   __TEXT.text_env: 0x57888
   __TEXT.__constructor: 0x0
   __TEXT.__init_offsets: 0x0

   __DATA.__mod_init_func: 0x8
   __DATA._rtk_threads: 0x0
   __DATA.__zerofill: 0x5d2b00
-  UUID: F6E6D400-1D8C-3973-BEB7-D050002467A8
+  UUID: A421C8EC-3B66-38AE-B1E9-D00B8F0FF0B9
   Functions: 9794
   Symbols:   0
   CStrings:  0

```

#### exclave_sharedcache

>  `exclave_sharedcache`

```diff

 1116.62.1.0.0
-  __TEXT.__text: 0x583524
+  __TEXT.__text: 0x5836e4
   __TEXT.__lcxx_override: 0x34c
   __TEXT.__cstring: 0x438fc
   __TEXT.__const: 0x107864

   __PDATA.__common: 0x2278
   __DATA_CONST.__mod_init_func: 0x0
   __DATA_CONST.__mod_term_func: 0x0
-  UUID: F95A8E21-A1A2-386E-9239-4FE4283D810C
-  Functions: 21429
+  UUID: 3AFB96F0-36BE-3E83-A354-FEB258C81DD5
+  Functions: 21433
   Symbols:   0
   CStrings:  0
 

```

#### txm.iphoneos.release.im4p

>  `txm.iphoneos.release.im4p`

```diff

 182.40.3.0.0
-  __TEXT.__cstring: 0x629a
+  __TEXT.__cstring: 0x629c
   __TEXT.__const: 0x6100
   __TEXT.__binname: 0x40
-  __TEXT.__info_plist: 0x505
+  __TEXT.__info_plist: 0x500
   __TEXT.__chain_starts: 0x20
   __DATA_CONST.__auth_ptr: 0x58
   __DATA_CONST.__const: 0xaa30

   __DATA.__data: 0x4a0
   __DATA.__common: 0xa90
   __DATA.__bss: 0x590
-  UUID: 736229C2-EEAC-3B25-A83C-7E00CAE8EC04
+  UUID: 83DADA9B-F2CB-3D76-B95D-E3FB4FB25A4C
   Functions: 927
   Symbols:   1
   CStrings:  0

```


</details>

### iBoot

| iOS | Version |
| :-- | :------ |
| 26.2 *(23C55)* | iBoot-13822.62.5 |
| 26.2.1 *(23C71)* | iBoot-13822.62.5 |

#### 🆕 NEW (1)

<details>
  <summary><i>View NEW</i></summary>

##### `iboot_blob33.bin`
  - `root@Jan 09 2026@17:59:38~.release`

</details>

#### ❌ Removed (1)

<details>
  <summary><i>View Removed</i></summary>

##### `iboot_blob33.bin`
  - `root@Nov 08 2025@17:57:48~.release`

</details>

## DSC

### WebKit

| iOS | Version |
| :-- | :------ |
| 26.2 *(23C55)* | 623.1.14.10.9 |
| 26.2.1 *(23C71)* | 623.1.14.10.9 |

### Dylibs

#### ⬆️ Updated (28)

<details>
  <summary><i>View Updated</i></summary>

- [/System/Library/Frameworks/CFNetwork.framework/CFNetwork](DYLIBS/CFNetwork.md)
- [/System/Library/Frameworks/CoreTelephony.framework/CoreTelephony](DYLIBS/CoreTelephony.md)
- [/System/Library/Frameworks/Foundation.framework/Foundation](DYLIBS/Foundation.md)
- [/System/Library/Frameworks/QuartzCore.framework/QuartzCore](DYLIBS/QuartzCore.md)
- [/System/Library/Health/FeedItemPlugins/Heart.healthplugin/Heart](DYLIBS/Heart.md)
- [/System/Library/Health/FeedItemPlugins/Summaries.healthplugin/Summaries](DYLIBS/Summaries.md)
- [/System/Library/PrivateFrameworks/AccessibilityUtilities.framework/AccessibilityUtilities](DYLIBS/AccessibilityUtilities.md)
- [/System/Library/PrivateFrameworks/AppStoreKit.framework/AppStoreKit](DYLIBS/AppStoreKit.md)
- [/System/Library/PrivateFrameworks/CentauriBooter.framework/CentauriBooter](DYLIBS/CentauriBooter.md)
- [/System/Library/PrivateFrameworks/ContainerManagerCommon.framework/ContainerManagerCommon](DYLIBS/ContainerManagerCommon.md)
- [/System/Library/PrivateFrameworks/CoreEmbeddedSpeechRecognition.framework/CoreEmbeddedSpeechRecognition](DYLIBS/CoreEmbeddedSpeechRecognition.md)
- [/System/Library/PrivateFrameworks/CoreSpeechFoundation.framework/CoreSpeechFoundation](DYLIBS/CoreSpeechFoundation.md)
- [/System/Library/PrivateFrameworks/CoreUARP.framework/CoreUARP](DYLIBS/CoreUARP.md)
- [/System/Library/PrivateFrameworks/FindMyBluetooth.framework/FindMyBluetooth](DYLIBS/FindMyBluetooth.md)
- [/System/Library/PrivateFrameworks/GridZero.framework/GridZero](DYLIBS/GridZero.md)
- [/System/Library/PrivateFrameworks/IntelligencePlatformCore.framework/IntelligencePlatformCore](DYLIBS/IntelligencePlatformCore.md)
- [/System/Library/PrivateFrameworks/NanoControlCenter.framework/NanoControlCenter](DYLIBS/NanoControlCenter.md)
- [/System/Library/PrivateFrameworks/PromotedContent.framework/PromotedContent](DYLIBS/PromotedContent.md)
- [/System/Library/PrivateFrameworks/SoftwareUpdateServicesUI.framework/SoftwareUpdateServicesUI](DYLIBS/SoftwareUpdateServicesUI.md)
- [/System/Library/PrivateFrameworks/SoftwareUpdateSettings.framework/SoftwareUpdateSettings](DYLIBS/SoftwareUpdateSettings.md)
- [/System/Library/PrivateFrameworks/SoftwareUpdateSettingsUI.framework/SoftwareUpdateSettingsUI](DYLIBS/SoftwareUpdateSettingsUI.md)
- [/System/Library/PrivateFrameworks/SoftwareUpdateUIFoundation.framework/SoftwareUpdateUIFoundation](DYLIBS/SoftwareUpdateUIFoundation.md)
- [/System/Library/PrivateFrameworks/SoftwareUpdateUIMobile.framework/SoftwareUpdateUIMobile](DYLIBS/SoftwareUpdateUIMobile.md)
- [/System/Library/PrivateFrameworks/SpeakerRecognition.framework/SpeakerRecognition](DYLIBS/SpeakerRecognition.md)
- [/System/Library/PrivateFrameworks/WebCore.framework/Frameworks/libANGLE-shared.dylib](DYLIBS/libANGLE-shared.dylib.md)
- [/usr/lib/dyld](DYLIBS/dyld.md)
- [/usr/lib/libimage4.dylib](DYLIBS/libimage4.dylib.md)
- [/usr/lib/system/libsystem_containermanager.dylib](DYLIBS/libsystem_containermanager.dylib.md)

</details>

## EOF
