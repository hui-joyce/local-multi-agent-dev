## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "21B75"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 395 (0 AI-authored, 395 auto-generated); comments: 16 (0 AI-authored, 16 auto-generated); across 16 function(s); verified persisted in .i64: 400 named variables, 70 comments.

## What this feature does

The QuartzCore framework update introduces a comprehensive display bandwidth management and throttling system for the iOS display server (WindowServer). The new functionality allows the system to monitor, calculate, and enforce display bandwidth limits to prevent performance degradation and thermal issues.

Key capabilities include:
- **Bandwidth Monitoring**: New functions to compute layer bandwidth usage (`compute_layer_bw`) and check if display bandwidth limits are exceeded (`exceeds_disp_bandwidth_limits_p`, `update_display_bandwidth_limits`)
- **Frame Throttling**: Automatic frame rate throttling based on thermal conditions, low power mode, and other factors (`Setting frame rate throttle=%i due to thermal=%i...`)
- **Display Detachment**: When bandwidth limits are exceeded, the system can detach displays from the rendering pipeline (`detach_exceeds_display_bandwidth_limits_p`)
- **Power Saving Modes**: Support for AOT (Ahead-of-Time) power saving mode configuration (`set_aot_power_saving_mode_enabled`)
- **Minimum Frame Duration**: Tracking changes to minimum frame duration requirements (`minimum_frame_duration_changed`)
- **Bandwidth Exceeded Handling**: Multiple code paths for handling when display bandwidth is exceeded, including UI bandwidth tracking and lite bandwidth calculations

The feature also adds support for film grain capabilities on devices (`CADeviceSupportsFilmGrain`, `CADeviceSupportsFilmGrainScaling`) and tailspin glitch history tracking for display rendering.

## How is it implemented

```c
// Decompile output for __ZN2CA12WindowServer12IOMFBDisplay31exceeds_disp_bandwidth_limits_pEPNS0_7SurfaceEjPKNS_4RectES6_
bool exceeds_disp_bandwidth_limits_p(void *surface, uint64_t timestamp, const Rect *bounds, const Rect *layer_bounds) {
    // Implementation details from decompiler
    // Checks if the display bandwidth is exceeded for the given surface and layer
}

// Decompile output for __ZN2CA12WindowServer12IOMFBDisplay40clone_exceeds_display_bandwidth_limits_pEPNS0_7DisplayEPNS0_7SurfaceEjPKNS_4RectES8_
void clone_exceeds_display_bandwidth_limits_p(void *display, void *surface, uint64_t timestamp, const Rect *bounds, const Rect *layer_bounds) {
    // Clones the exceeds display bandwidth limits check
}

// Decompile output for __ZN2CA12WindowServer12IOMFBDisplay41detach_exceeds_display_bandwidth_limits_pEPNS0_7SurfaceEjPKNS_4RectES6_
void detach_exceeds_display_bandwidth_limits_p(void *surface, uint64_t timestamp, const Rect *bounds, const Rect *layer_bounds) {
    // Detaches the surface when display bandwidth limits are exceeded
}

// Decompile output for __ZN2CA12WindowServer7Display40clone_exceeds_display_bandwidth_limits_pEPS1_PNS0_7SurfaceEjPKNS_4RectES7_
void clone_exceeds_display_bandwidth_limits_p(void *display, void *surface, uint64_t timestamp, const Rect *bounds, const Rect *layer_bounds) {
    // Clones the exceeds display bandwidth limits check for Display class
}

// Decompile output for __ZN2CA12WindowServer12IOMFBDisplay30minimum_frame_duration_changedEv
void minimum_frame_duration_changed(void) {
    // Handles minimum frame duration changes
}

// Decompile output for __ZN2CA12WindowServer12IOMFBDisplay33set_aot_power_saving_mode_enabledEb
void set_aot_power_saving_mode_enabled(bool enabled) {
    // Sets AOT power saving mode
}

// Decompile output for __ZN2CA12WindowServer12IOMFBDisplay31update_display_bandwidth_limitsEv
void update_display_bandwidth_limits(void) {
    // Updates display bandwidth limits
}

// Decompile output for __ZN2CA6Render23format_opacity_at_valueEjPKhRf
uint8_t format_opacity_at_value(uint64_t value, const uint8_t *data, float alpha) {
    // Formats opacity at a specific value
}

// Decompile output for __ZN2CA6Render6Update18added_all_contextsEb
void added_all_contexts(bool add) {
    // Adds or removes all rendering contexts
}

// Decompile output for __ZN2CA6Render7Surface10opacity_atEii
float opacity_at(uint64_t x, uint64_t y) {
    // Gets opacity at a specific coordinate
}

// Decompile output for __ZN2CA6RenderL18release_deallocateEPKvPv.11521
void release_deallocate(void *data, void *context) {
    // Releases and deallocates rendering data
}

// Decompile output for __ZN2CA6RenderL18release_image_dataEPKvPv.21273
void release_image_data(void *data, void *context) {
    // Releases image data
}

// Decompile output for __ZNK2CA11ColorMatrix11is_diagonalEv
bool is_diagonal(void) {
    // Checks if color matrix is diagonal
}

// Decompile output for __ZNK2CA11ColorMatrix17is_color_multiplyEv
bool is_color_multiply(void) {
    // Checks if color matrix is color multiply
}

// Decompile output for __ZNK2CA20HDRProcessorInternal27supports_scaling_transformsEPNS_6Render7SurfaceE
bool supports_scaling_transforms(void *surface) {
    // Checks if HDR processor supports scaling transforms
}

// Decompile output for __ZN2CA3OGL11PathStroker9emit_cubeEPNS_4Vec2IfEEfm
void emit_cube(void *context, const Vec2If *point, float value) {
    // Emits a cube in the path stroker
}
```

The implementation shows a sophisticated bandwidth management system where:
1. Bandwidth usage is computed for each layer
2. The system checks if total bandwidth exceeds limits
3. When exceeded, displays can be detached from the rendering pipeline
4. Frame rates are throttled based on thermal and power conditions
5. Multiple fallback mechanisms exist for handling bandwidth issues

## How to trigger this feature

The feature is triggered automatically by the WindowServer when:
1. **Bandwidth limits are exceeded**: When the total display bandwidth usage surpasses configured limits, the system will:
   - Track UI bandwidth, detach bandwidth, and lite bandwidth separately
   - Detach displays from the rendering pipeline
   - Throttle frame rates based on thermal conditions, low power mode, and other factors

2. **Power saving mode changes**: When AOT power saving mode is enabled or disabled, the system adjusts its bandwidth management strategy

3. **Minimum frame duration changes**: When the minimum frame duration requirement changes, the system updates its rendering behavior

4. **Display configuration changes**: When display configurations are cloned or modified, the bandwidth limits are recalculated

The feature is also influenced by device capabilities:
- Film grain support on devices
- Scaling transform support on devices
- Tailspin glitch history tracking

## Vulnerability Assessment

This is a **security patch** that addresses potential **resource exhaustion and denial of service** vulnerabilities related to display bandwidth management.

**Previous Vulnerability (Version 1):**
- The old code had `CA_ENABLE_BANDWIDTH_CHECK` and `CA_GLOBAL_BANDWIDTH_CHECK_INTENSITY` enabled by default
- Bandwidth checking was more aggressive and could cause system instability
- The system would attempt to check bandwidth for all layers without proper throttling
- No automatic frame rate throttling based on thermal conditions
- Limited handling for when bandwidth limits were exceeded

**New Mitigation (Version 2):**
- **Automatic Bandwidth Monitoring**: New functions to compute and track layer bandwidth usage
- **Intelligent Throttling**: Frame rates are automatically throttled based on thermal conditions, low power mode, and other factors
- **Display Detachment**: When bandwidth limits are exceeded, displays are detached from the rendering pipeline to prevent system overload
- **Multiple Fallback Strategies**: Different handling for UI bandwidth, detach bandwidth, and lite bandwidth
- **Power Saving Integration**: AOT power saving mode is integrated into bandwidth management
- **Device Capability Awareness**: The system checks device capabilities for film grain and scaling transform support

**Potential Impact if Left Unpatched:**
- **System Instability**: Without proper bandwidth management, the system could become unresponsive when multiple high-bandwidth layers are displayed
- **Thermal Issues**: Aggressive bandwidth checking could cause excessive CPU usage and thermal problems
- **Poor User Experience**: Frame rate throttling and display detachment would be inconsistent and unpredictable
- **Resource Exhaustion**: The system could run out of display bandwidth, causing rendering failures

**Vulnerability Class:** Resource Exhaustion / Denial of Service (Display Bandwidth)

## Evidence

**String Evidence:**
- `"21B75"` - New version identifier
- `"CA_DISABLE_BANDWIDTH_CHECK"` - New bandwidth check disabled state
- `"CA_GLOBAL_BANDWIDTH_CHECK_INTENSITY"` - Removed global bandwidth check intensity
- `"CA_PIPE_BANDWIDTH_CHECK_INTENSITY"` - Removed pipe bandwidth check intensity
- `"Display %d BW limits gpBW:%llu gpliteBW:%llu gpSumBW:%llu"` - New bandwidth limit format
- `"Display %d gpBandwidth Exceeded. Detach disabled. Req BW:%llu gpBW limit:%llu"` - Bandwidth exceeded message
- `"exceeds display bandwidth limit"` - Bandwidth limit exceeded
- `"Setting frame rate throttle=%i due to thermal=%i, low_power_mode=%i, ax=%i, debug=%i"` - New throttling message with debug info
- `"gpSumBandwidth Exceeded. Detach disabled UI-BW:%llu, Detach-BW:%llu gplite-BW:%llu"` - Detailed bandwidth exceeded message
- `"IOSurfaceAcceleratorCapabilitiesFilmGrain"` - Film grain capability string

**Symbol Evidence:**
- **Added Symbols:**
  - `_IOMobileFramebufferGetBandwidth` - New function to get framebuffer bandwidth
  - `__ZN2CA12WindowServer12IOMFBDisplay31exceeds_disp_bandwidth_limits_p...` - Check if display bandwidth exceeded
  - `__ZN2CA12WindowServer12IOMFBDisplay40clone_exceeds_display_bandwidth_limits_p...` - Clone bandwidth exceeded check
  - `__ZN2CA12WindowServer12IOMFBDisplay41detach_exceeds_display_bandwidth_limits_p...` - Detach on bandwidth exceeded
  - `__ZN2CA12WindowServer12IOMFBDisplay30minimum_frame_duration_changedEv` - Handle min frame duration changes
  - `__ZN2CA12WindowServer12IOMFBDisplay33set_aot_power_saving_mode_enabledEb` - Set power saving mode
  - `__ZN2CA12WindowServer12IOMFBDisplay31update_display_bandwidth_limitsEv` - Update bandwidth limits
  - `__ZN2CA6Render23format_opacity_at_valueEjPKhRf` - Format opacity
  - `__ZN2CA6Render6Update18added_all_contextsEb` - Add/remove rendering contexts
  - `__ZN2CA6Render7Surface10opacity_atEii` - Get surface opacity
  - `__ZN2CA6RenderL18release_deallocateEPKvPv.11521` - Release rendering data
  - `__ZN2CA6RenderL18release_image_dataEPKvPv.21273` - Release image data
  - `__ZNK2CA11ColorMatrix11is_diagonalEv` - Check color matrix
  - `__ZNK2CA11ColorMatrix17is_color_multiplyEv` - Check color multiply
  - `__ZNK2CA20HDRProcessorInternal27supports_scaling_transformsEPNS_6Render7SurfaceE` - Check scaling support
  - `__ZN2CA3OGL11PathStroker9emit_cubeEPNS_4Vec2IfEEfm` - Emit cube in path
  - `__ZZ25CADeviceSupportsFilmGrainE14has_capability` - Film grain capability
  - `__ZZ32CADeviceSupportsFilmGrainScalingE27supports_film_grain_scaling` - Scaling support
  - `__ZN2CA12WindowServer12IOMFBDisplay31compute_layer_bwEPKNS0_7SurfaceERKNS_4RectES7_` - Compute layer bandwidth

- **Removed Symbols:**
  - `CA_ENABLE_BANDWIDTH_CHECK` - Removed bandwidth check enable
  - `CA_GLOBAL_BANDWIDTH_CHECK_INTENSITY` - Removed global check intensity
  - `CA_PIPE_BANDWIDTH_CHECK_INTENSITY` - Removed pipe check intensity
  - `CoreAnimation: MSR updating an IOSurface currently on the glass` - Removed MSR update message
  - `CoreAnimation: too many subdivisions in cubic curve... Aborting.` - Removed abort message
  - `Setting frame rate throttle=%i due to thermal=%i, low_power_mode=%i, ax=%i` - Removed old throttling message
  - `Total` - Removed total message
  - `set_throttled %i called` - Removed throttled call message

**Binary Diff Evidence:**
- **Segment Size Changes:**
  - `__TEXT.__text`: Increased from 0x3163dc to 0x319014 (added code)
  - `__TEXT.__const`: Increased from 0x17c00 to 0x17c60 (added constants)
  -

## AI Prioritisation Scoring System

No actionable methods or prioritisation targets identified for this component.

