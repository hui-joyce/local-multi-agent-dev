## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "%@-%@%@%@"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 0 (0 AI-authored, 0 auto-generated); comments: 0 (0 AI-authored, 0 auto-generated); across 0 function(s); verified persisted in .i64: 0 named variables, 0 comments.

## What this feature does

The CoreSpeech component has undergone significant changes between iOS 17.0.3 and 17.1, primarily focused on **voice trigger architecture refactoring** and **benchmarking infrastructure expansion**.

### Key Changes Summary:

**1. Voice Trigger Architecture Simplification:**
- Removed `CSBuiltInVoiceTrigger` class and its associated methods (`_transitAOPModeIfNeeded:`, `_transitAOPModeIfNeededAsync:`, `_transitAOPModeIfNeededSync:`, `jarvisTriggerModeLogHeartbeat`, `setJarvisTriggerModeLogHeartbeat:`)
- This suggests a consolidation of voice trigger logic, possibly moving from a multi-stage approach to a more streamlined implementation

**2. Enhanced Benchmarking Infrastructure:**
- Added `CSBenchmarkService` with methods: `disableBenchmarkService`, `enableBenchmarkService`, `runNCModelWithConfig:completion:`
- Added `CSModelBenchmarker` class with extensive benchmarking capabilities for on-device model compilation and execution
- New benchmarking strings indicate support for:
  - NC (Neural Network) model benchmarking
  - Nov (Novelty Detection) detector benchmarking
  - ODLD (Online Deep Learning) model benchmarking
  - VT (Voice Trigger) second-pass model benchmarking
  - OSD (On-Screen Display) analyzer benchmarking
  - PSR (Speaker Recognition) audio processor benchmarking

**3. Audio Processing Enhancements:**
- Added audio injection engine support with new strings like "startRecording", "stopRecording", "audioInjectionEngine"
- New audio processing classes: `CSAudioInjectionEngine`, `CSAudioInjectionProvider`
- Enhanced audio recording and playback tracking with host time monitoring

**4. New Audio Processing Classes:**
- `CSSyncKeywordAnalyzerQuasar` - New keyword analysis engine
- `EARSyncPSRAudioProcessor` - Enhanced speaker recognition audio processor
- `SLODLDProcessor` - New online deep learning processor

**5. Diagnostic and Monitoring Improvements:**
- Added endpoint delay reporting with new string: "_emitEndpointDelayMessage:epdModel:speakingStart:speakingEnd:"
- Enhanced Bluetooth state logging (with M9 watch exception)
- New diagnostic strings for audio recording metrics

**6. Removed Features:**
- Simplified alert dictionary methods (fewer parameters in `_alertDictionaryForRecordRoute:...`)
- Removed AOP (Audio Output Processing) mode transit methods
- Removed some legacy voice trigger logging

## How is it implemented

Based on the diff evidence, the implementation involves:

### Removed Components:
```objc
// CSBuiltInVoiceTrigger class removed entirely
- [CSBuiltInVoiceTrigger _transitAOPModeIfNeeded:]
- [CSBuiltInVoiceTrigger _transitAOPModeIfNeededAsync:]
- [CSBuiltInVoiceTrigger _transitAOPModeIfNeededSync:]
- [CSBuiltInVoiceTrigger jarvisTriggerModeLogHeartbeat]
- [CSBuiltInVoiceTrigger setJarvisTriggerModeLogHeartbeat:]
```

### Added Components:
```objc
// New Benchmarking Service
+ [CSBenchmarkService disableBenchmarkService]
+ [CSBenchmarkService enableBenchmarkService]
+ [CSBenchmarkService runNCModelWithConfig:completion:]

// New Model Benchmarker
- [CSModelBenchmarker init]
- [CSModelBenchmarker _onDeviceCompilationWithConfigFile:locale:]
- [CSModelBenchmarker _setupAudioInjectionEngineWithAudioURL:]
- [CSModelBenchmarker audioEngineDidStartRecord:audioStreamHandleId:successfully:error:]
- [CSModelBenchmarker audioEngineDidStopRecord:audioStreamHandleId:reason:]
- [CSModelBenchmarker benchmarkOnDeviceCompilationCleanup:]
- [CSModelBenchmarker pingpong:completion:]
- [CSModelBenchmarker runNovDetectorWithConfig:configRoot:withUrl:completion:]
- [CSModelBenchmarker runODLDModelWithConfig:locale:inputText:completion:]
- [CSModelBenchmarker runOSDAnalyzerWithConfig:withUrl:completion:]
- [CSModelBenchmarker runVTSecondPassModelWithConfig:locale:withUrl:completion:]
- [CSModelBenchmarker setAllFramesInferenceLatency:]
- [CSModelBenchmarker setAudioInjectionEngine:]
- [CSModelBenchmarker setCompletion:]
- [CSModelBenchmarker setInferenceTimeSpan:]
- [CSModelBenchmarker setModelExeQueue:]
- [CSModelBenchmarker setNovDetectAnalyzer:]
- [CSModelBenchmarker setOdldModelAnalyzer:]
- [CSModelBenchmarker setOsdAnalyzer:]
- [CSModelBenchmarker setPsrAudioProcessor:]
- [CSModelBenchmarker setQueue:]
- [CSModelBenchmarker setTempCacheDirectoryForMil2Bnns:]
- [CSModelBenchmarker setTotalNumberSamples:]
- [CSModelBenchmarker setVtSecondPassAnalyzer:]
```

### Audio Injection Engine:
```objc
// New audio injection capabilities
- [CSAudioInjectionProvider startAudioStreamWithOption:recordDeviceIndicator:error:]
- [CSModelBenchmarker _setupAudioInjectionEngineWithAudioURL:]
```

### Enhanced Siri Speech Recording:
```objc
// Improved recording and event tracking
- [CSSiriSpeechRecorder _logBluetoothStateWithMHUUID:]
- [CSSiriSpeechRecordingContext emitRequestLinkEventForRtsSessionId:]
```

## How to trigger this feature

The feature is triggered through:

1. **Benchmark Service Control:**
   - `CSBenchmarkService.enableBenchmarkService` - Enables benchmarking mode
   - `CSBenchmarkService.disableBenchmarkService` - Disables benchmarking mode

2. **Model Benchmarking:**
   - `CSModelBenchmarker` is initialized with configuration files
   - Models are compiled on-device with locale-specific configurations
   - Audio injection engine is set up with audio URLs
   - Various model types (NC, Nov, ODLD, VT, OSD, PSR) are benchmarked

3. **Audio Recording:**
   - Recording starts/stops via `startRecording`/`stopRecording` strings
   - Audio stream handling with device indicators
   - Endpoint detection and timing tracking

4. **Device Detection:**
   - `isM9Device` check for special handling (e.g., skip Bluetooth logging on M9 watch)

## Vulnerability Assessment

**No direct security vulnerabilities identified in this change.**

The changes are primarily **functional enhancements** and **refactoring**:

1. **Architecture Refactoring:** Removal of `CSBuiltInVoiceTrigger` suggests consolidation of voice trigger logic, not a security fix
2. **Performance Monitoring:** Addition of extensive benchmarking infrastructure for model performance tracking
3. **Audio Processing:** Enhanced audio injection and recording capabilities
4. **Diagnostic Improvements:** Better endpoint delay reporting and Bluetooth state logging

**Risk Assessment:**
- **Low Risk:** These are additive changes to benchmarking and audio processing
- **No Memory Safety Issues:** No evidence of use-after-free, out-of-bounds, or race conditions
- **No Privilege Escalation:** Changes are within the CoreSpeech sandbox
- **No IPC Protocol Changes:** No modifications to inter-process communication protocols

**Recommendation:** Monitor for performance regressions in voice trigger response times due to the new benchmarking overhead, but no critical security concerns.

## Evidence

### Added Symbols (Priority):
- `CSBenchmarkService` methods
- `CSModelBenchmarker` class and methods
- `CSAudioInjectionEngine`
- `CSSyncKeywordAnalyzerQuasar`
- `EARSyncPSRAudioProcessor`
- `SLODLDProcessor`

### Added Strings (Priority):
- Benchmark-related: "CSBenchmarker", "Model benchmark Queue", "runNCModelWithConfig", etc.
- Audio recording: "startRecording", "stopRecording", "Setting alertBehavior recordStarting"
- Audio injection: "startRecording", "audioInjectionEngine"
- New processors: "CSyncKeywordAnalyzerQuasar", "EARSyncPSRAudioProcessor", "SLODLDProcessor"

### Removed Symbols:
- `CSBuiltInVoiceTrigger` class and all its methods
- Legacy AOP mode transit methods

### Removed Strings:
- Simplified alert dictionary methods
- Legacy AOP mode strings

### Binary Diff Summary:
- **Version 1 (17.0.3):** Contains `CSBuiltInVoiceTrigger` with AOP mode support
- **Version 2 (17.1):** `CSBuiltInVoiceTrigger` removed, replaced with streamlined architecture
- **Net Result:** Architecture simplification with enhanced benchmarking capabilities

## AI Prioritisation Scoring System

- **Static binary diff analysis with string and symbol examination**
  - **Tier**: TIER_2
  - **Category**: Voice Trigger Architecture Refactoring
  - **Reasoning**: Core voice trigger architecture changes with significant functional impact. Removal of CSBuiltInVoiceTrigger class and addition of comprehensive benchmarking infrastructure (CSModelBenchmarker, CSBenchmarkService) represents a major refactoring of the voice trigger system. While not a critical security fix (TIER_1), these changes affect core Siri functionality and performance monitoring capabilities, making them medium priority for analysis and monitoring.

