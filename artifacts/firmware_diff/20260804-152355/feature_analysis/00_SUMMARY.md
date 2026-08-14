# Feature Analysis Summary -- iOS 26.3.1

- **Total components in diff**: 316  (**HIGH_SIGNAL**: 216, **LOW_SIGNAL**: 100)
- **Analysed** (report written): 38  |  **Apple Security Notes matches**: 0  |  **Suppressed TIER_3**: 7  |  **HIGH_SIGNAL not analysed** (budget/security filter): 171

Tier shown is the LLM-assigned tier for analysed components, otherwise a deterministic estimate from the security score (4=Apple Security Notes, 3=hard indicator, 2=security vocabulary, 1=code change, 0=asset/UI/log).

## Analysed components (reports written)

| Component | Tier | Sec score | Apple Security Notes | Report |
|---|---|---|---|---|
| CoreBrightness | TIER_1 | 3 | -- | [report](CoreBrightness_analysis.md) |
| libAppleTconUARPUpdater.dylib | TIER_1 | 3 | -- | [report](libAppleTconUARPUpdater.dylib_analysis.md) |
| AudioToolbox | TIER_1 | 2 | -- | [report](AudioToolbox_analysis.md) |
| CryptexServer | TIER_1 | 2 | -- | [report](CryptexServer_analysis.md) |
| corespeechd | TIER_1 | 2 | -- | [report](corespeechd_analysis.md) |
| cryptexd | TIER_1 | 2 | -- | [report](cryptexd_analysis.md) |
| libAce3Updater.dylib | TIER_1 | 2 | -- | [report](libAce3Updater.dylib_analysis.md) |
| libBKDM2.dylib | TIER_1 | 2 | -- | [report](libBKDM2.dylib_analysis.md) |
| mobileactivationd | TIER_1 | 2 | -- | [report](mobileactivationd_analysis.md) |
| Measure | TIER_2 | 3 | -- | [report](Measure_analysis.md) |
| Setup | TIER_2 | 3 | -- | [report](Setup_analysis.md) |
| AVFAudio | TIER_2 | 2 | -- | [report](AVFAudio_analysis.md) |
| ActionButtonSelector | TIER_2 | 2 | -- | [report](ActionButtonSelector_analysis.md) |
| CoreRealityIO | TIER_2 | 2 | -- | [report](CoreRealityIO_analysis.md) |
| CoreSpeechFoundation | TIER_2 | 2 | -- | [report](CoreSpeechFoundation_analysis.md) |
| DiskImages2 | TIER_2 | 2 | -- | [report](DiskImages2_analysis.md) |
| IOKit | TIER_2 | 2 | -- | [report](IOKit_analysis.md) |
| IOMFB_FDR_Loader | TIER_2 | 2 | -- | [report](IOMFB_FDR_Loader_analysis.md) |
| MediaExperience | TIER_2 | 2 | -- | [report](MediaExperience_analysis.md) |
| PhotosUICore | TIER_2 | 2 | -- | [report](PhotosUICore_analysis.md) |
| ProDisplayLibrary | TIER_2 | 2 | -- | [report](ProDisplayLibrary_analysis.md) |
| SiriInstrumentation | TIER_2 | 2 | -- | [report](SiriInstrumentation_analysis.md) |
| SpringBoardFoundation | TIER_2 | 2 | -- | [report](SpringBoardFoundation_analysis.md) |
| StoreKit | TIER_2 | 2 | -- | [report](StoreKit_analysis.md) |
| T8150_CoreAAClientKit_asan | TIER_2 | 2 | -- | [report](T8150_CoreAAClientKit_asan_analysis.md) |
| WebCore | TIER_2 | 2 | -- | [report](WebCore_analysis.md) |
| accessoryd | TIER_2 | 2 | -- | [report](accessoryd_analysis.md) |
| com.apple.driver.AppleEmbeddedUSBHost | TIER_2 | 2 | -- | [report](com.apple.driver.AppleEmbeddedUSBHost_analysis.md) |
| com.apple.driver.AppleProcessorTrace | TIER_2 | 2 | -- | [report](com.apple.driver.AppleProcessorTrace_analysis.md) |
| com.apple.driver.AppleUSBAudio | TIER_2 | 2 | -- | [report](com.apple.driver.AppleUSBAudio_analysis.md) |
| libcryptex.dylib | TIER_2 | 2 | -- | [report](libcryptex.dylib_analysis.md) |
| libcryptex_core.dylib | TIER_2 | 2 | -- | [report](libcryptex_core.dylib_analysis.md) |
| libcryptex_interface.dylib | TIER_2 | 2 | -- | [report](libcryptex_interface.dylib_analysis.md) |
| libcryptex_trampoline.dylib | TIER_2 | 2 | -- | [report](libcryptex_trampoline.dylib_analysis.md) |
| libimage4.dylib | TIER_2 | 2 | -- | [report](libimage4.dylib_analysis.md) |
| libsystem_containermanager.dylib | TIER_2 | 2 | -- | [report](libsystem_containermanager.dylib_analysis.md) |
| usbaudiod | TIER_2 | 2 | -- | [report](usbaudiod_analysis.md) |
| xpcproxy | TIER_2 | 2 | -- | [report](xpcproxy_analysis.md) |

## HIGH_SIGNAL -- analysed but suppressed (LLM rated TIER_3)

| Component | Tier | Sec score | Apple Security Notes | Report |
|---|---|---|---|---|
| CoreSpeech | TIER_3 | 2 | -- | _suppressed (TIER_3)_ |
| CryptexKit | TIER_3 | 2 | -- | _suppressed (TIER_3)_ |
| T8150_IR_ISP_EK_Component_asan | TIER_3 | 2 | -- | _suppressed (TIER_3)_ |
| T8150_RGB_ISP_EK_Component_asan | TIER_3 | 2 | -- | _suppressed (TIER_3)_ |
| com.apple.driver.AppleDisplayCrossbar | TIER_3 | 2 | -- | _suppressed (TIER_3)_ |
| launchd | TIER_3 | 2 | -- | _suppressed (TIER_3)_ |
| txm.iphoneos.release.im4p | TIER_3 | 2 | -- | _suppressed (TIER_3)_ |

## HIGH_SIGNAL -- excluded, low/no security relevance (171)

<details><summary>Show 171 components</summary>

- ACCBaker
- ACCHWComponentAuthService
- ANECompiler
- AVFCapture
- AccessoryComponentAuth
- AppleCV3D
- AppleDepth
- AudioDSPManager
- AudioServerDriver
- BatteryAlgorithms
- BlissReader
- BlueTool
- CMCapture
- CameraColorProcessing
- CameraUI
- CinematicFraming
- CommCenter
- ContainerManagerCommon
- CoreEmoji
- CoreGEM.dylib
- CoreGPSTest.dylib
- CoreGraphics
- CoreIndoor
- CoreMLOdie
- CoreNavigation
- CorePhotogrammetry
- CoreRepairCore
- CoreRepairLite
- CoreRoutineHelperService
- CoreUARP
- CoverSheet
- EAUpdaterService
- EmbeddedAcousticRecognition
- Espresso
- FitnessCoachingServices
- Freeform
- Haptics
- ISPExclaveKitServices
- JavaScriptCore
- Lexicon
- MPSCore
- MPSHost
- MPSImage
- MPSMatrix
- MPSNDArray
- MPSNeuralNetwork
- MPSRayIntersector
- MailUI
- MediaRemote
- Message
- Metal
- MicroLocationDaemon
- ModelIO
- NanoCalendarBridgeSettings
- NanoCalendarComplicationsCompanion
- NanoCalendarPingSubscriber
- PDFKit
- PaperBoardUI
- PhotosFormats
- PowerLog
- PowerlogCore
- ProVideo
- ProductKit
- ProductKitCore
- QuartzCore
- Recon3D
- SILManager
- SafariShared
- SafariSharedUI
- SceneKit
- SensingAlgsPadHostServiceJ8xx
- SensingAlgsService
- SensingAlgsTouchButtonHost
- SettingsFoundation
- SiriHeadlessService
- SiriNaturalLanguageParsing
- SiriTTS
- SoftwareUpdateController
- SoundAnalysis
- SpringBoard
- SpringBoardHome
- UARPUpdaterServiceLegacyAudio
- UARPUpdaterServiceUSBPD
- USDKit
- VFX
- VectorKit
- VirtualAudio
- VoiceProcessor
- VoiceTrigger
- WPDaemon
- WebGPU
- WebInspector
- WebKitLegacy
- WiFiAnalytics
- WirelessRadioManagerd
- WorkoutCore
- afktool
- agx_a000
- agx_a010
- agx_b000
- ansf.t8150.release.im4p
- appinstallationmetricsd
- assistantd
- bluetoothd
- com.apple.AGXG18P
- com.apple.DriverKit-AppleBCMWLAN
- com.apple.MobileInstallationHelperService
- com.apple.driver.AppleH16ANEInterface
- com.apple.driver.AppleHIDTransportSPI
- com.apple.driver.AppleHPM
- com.apple.driver.AppleSMCWirelessCharger
- com.apple.driver.AppleSPMIPMU
- com.apple.driver.AppleT8150CLPC
- com.apple.driver.usb.AppleSynopsysUSB40XHCI
- com.apple.driver.usb.AppleSynopsysUSBXHCI
- com.apple.driver.usb.AppleUSBXHCI
- com.apple.filesystems.apfs
- com.apple.iokit.IOAccessoryManager
- com.apple.iokit.IOUSBHostFamily
- com.apple.security.AppleImage4
- corerepaird
- diskimagescontroller
- diskimagesiod
- dyld
- exclave_ExclaveStackshotServer
- exclave_pmm_exclave
- exclave_roottask
- exclave_sharedcache
- gpsd
- libAudioDSP.dylib
- libBBUpdaterDynamic.dylib
- libBNNS.dylib
- libBasebandCommandDriversARI.dylib
- libCommCenterAWDMetrics.dylib
- libCommCenterKCommandDrivers.dylib
- libGPUCompilerUtils.dylib
- libHSFilerDynamic.dylib
- libIPTelephony.dylib
- libKTLDynamic.dylib
- libLLVM.dylib
- libMobileGestalt.dylib
- libPN548_API.dylib
- libVinylNonUpdater.dylib
- libVinylUpdater.dylib
- libauthinstall.dylib
- libfire7.dylib
- libhwtrace.dylib
- libmobileassetd.dylib
- libramrod.dylib
- libsandbox.1.dylib
- libswiftPrespecialized.dylib
- libusd_ms.dylib
- locationd
- magicswitchd
- mediaremoted
- mobileassetd
- nanobackupd
- nanoprefsyncd
- nanoregistryd
- nanosystemsettingsd
- nearbyd
- pipelined
- rans.t8150.release.im4p
- restoreserviced
- sptm.t8150.release.im4p
- threadradiod
- uarpassetmanagerd
- wifianalyticsd
- wifid
- wifip2pd
- xpcroleaccountd

</details>

## LOW_SIGNAL -- excluded (100, metadata/timestamp churn only)

<details><summary>Show 100 components</summary>

- AGXCompilerCore
- ARKitCore
- AVConference
- AVD.videodecoder
- AppleAOPAudioPlugin
- AppleMCTF
- AppleNeuralEngine
- AppleSMCFirmware.bin
- AppleVideoEncoder
- AudioCodecs
- Books
- CallHistory
- ClarityBoard
- CoreLocation
- CoreMotion
- CoreTelephony
- CoreUI
- Foundation
- GameKitServices
- H16ISP.mediacapture
- H264H9.videoencoder
- H9.videoencoder
- IMTranscoderAgent
- IconFoundation
- IconServices
- IntelligencePlatformCore
- ManifestStorageService
- MapsSuggestions
- MetalPerformanceShadersGraph
- ModelCatalogRuntime
- MultipeerConnectivity
- NRDUpdated
- PhoneKit
- PolarisBufferService
- RTKit.bin
- Recap
- SDAPI
- STExtractionService
- STExtractionService.privileged
- StoreKitUISceneService
- WebKit
- WiFiCloudSyncEngine
- _LocationEssentials
- _StoreKit_SwiftUI
- adc-silenus-d23.im4p
- anomalydetectiond
- appstored
- askpermissiond
- batteryintelligenced
- com.apple.DeviceRecoveryBuiltinBrain
- com.apple.StreamingUnzipService
- com.apple.StreamingUnzipService.privileged
- com.apple.driver.AppleAOPAudio
- com.apple.driver.AppleAVE2
- com.apple.driver.AppleMSG
- com.apple.driver.AppleMobileFileIntegrity
- com.apple.driver.ApplePMGR
- com.apple.driver.AppleSEPKeyStore
- com.apple.driver.AppleSMC
- com.apple.driver.AppleSmartIO2
- com.apple.driver.AppleThunderboltNHI
- com.apple.driver.AppleUSBDeviceMux
- com.apple.driver.AudioDMACLLTEscalationDetector-T8150
- com.apple.driver.AudioDMAController-T8150
- com.apple.driver.AudioDMAFamily
- com.apple.driver.IOPAudioVoiceTriggerDevice
- com.apple.driver.RTBuddy
- com.apple.iokit.IOPCIFamily
- com.apple.iokit.IOThunderboltFamily
- com.apple.kernel
- com.apple.security.AKSAnalytics
- companion_proxy
- destinationd
- devicerecoveryd
- eligibilityd
- gamepolicyd
- h18_ane_fw_apollo_v5x.im4p
- iboot_blob30.bin
- iboot_blob31.bin
- iboot_blob32.bin
- iboot_blob45.bin
- identityservicesd
- imagent
- installcoordination_proxy
- installcoordinationd
- itunesstored
- libGLProgrammability.dylib
- libGPUCompilerImpl.dylib
- libTelephonyCapabilities.dylib
- libcoreroutine.dylib
- libnfshared.dylib
- polarisd
- revisiond
- securem3fw-d23.im4p
- softwareupdated
- srp-mdns-proxy
- storekitd
- terminusd
- useractivityd
- wirelessinsightsd

</details>
