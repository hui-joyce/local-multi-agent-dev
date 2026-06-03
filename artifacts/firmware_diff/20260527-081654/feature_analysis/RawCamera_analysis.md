# Feature Analysis: RawCamera

## What this feature does
This update modifies the `RawCamera` component by incrementing its version number and adjusting internal memory layout offsets for text, exception tables, and Objective-C runtime data structures. Additionally, it introduces a new dependency on the `CMPhoto` framework while removing several existing image processing frameworks, suggesting a shift toward utilizing the newer `CMPhoto` system for handling raw image data.

## How is it implemented
**Component:** `RawCamera` (located in `/System/Library/CoreServices/RawCamera.bundle`)
**Version Change:** 18.6.1 (22G90) → 18.6.2 (22G100)

**Call Graph Context & Implementation:**
`RawCamera` is a system-level binary responsible for processing raw image data (e.g., DNG, CR2, NEF). It functions as a library loaded by the Photos framework or Camera app, rather than a standalone executable.

**Evidence Analysis:**
1.  **Dependency Shift:** The most significant change is the addition of `CMPhoto` (`/System/Library/PrivateFrameworks/CMPhoto.framework/CMPhoto`) to the linked frameworks.
    *   *Implication:* `RawCamera` now likely delegates specific photo asset handling, metadata extraction, or camera-specific optimizations to the `CMPhoto` framework, which manages the core photo library logic. This suggests a refactoring where `RawCamera` offloads generic asset processing to `CMPhoto` while retaining low-level raw decoding logic.
2.  **Binary Growth:** The binary size increased (version 11 vs 0), with corresponding growth in text segments (`__text`, `__gcc_except_tab`, `__unwind_info`) and data segments (`__objc_arraydata`, `__objc_intobj`).
    *   *Implication:* The implementation likely includes new Objective-C methods or data structures for supporting new camera formats or improved raw decoding algorithms. The increased `__objc_*` sections indicate added dynamic dispatch logic.
3.  **Security/Linking:** The `__auth_stubs` and `__auth_got` sections shifted, indicating changes in dynamic linking or security checks (e.g., ASLR, code signing) within the bundle.

**Likely Callers:**
*   **Photos Framework:** Likely calls `RawCamera` to decode raw images from the photo library.
*   **Camera App:** Invokes `RawCamera` directly during image capture to process raw files immediately.
*   **`CMPhoto`:** The newly linked framework suggests `CMPhoto` may call back into `RawCamera` for specific raw format parsing or `RawCamera` calls `CMPhoto` for asset metadata resolution.

**Entry Points:**
*   Standard Objective-C entry points (e.g., `+initialize`, `+load`) for the bundle.
*   Specific raw decoding entry points (e.g., `+[RawCamera decodeRawImage:fromData:]` or similar internal C functions exposed via the Objective-C runtime).

**Connected Components:**
*   **`CMPhoto`**: Primary new dependency for asset management integration.
*   **`AppleJPEG` / `AppleJPEGXL`**: Existing dependencies likely used for post-processing raw data (e.g., converting raw to JPEG

## How to trigger this feature
The `RawCamera` component is activated via user action, specifically when a user opens the Photos app and selects an image file with a `.raw` extension (e.g., `.dng`, `.cr2`, `.nef`). This triggers the system to launch the `RawCamera` executable located at `/System/Library/CoreServices/RawCamera.bundle/RawCamera` to process the file. The diff indicates a version update (18.6.1 to 18.6.2) involving internal binary changes and the addition of the `CMPhoto` framework dependency, but no new external launch mechanisms (like `launchd` jobs or IPC hooks) are introduced in the provided evidence.

## Evidence
- Source: dsc
- Evidence: >  `/System/Library/CoreServices/RawCamera.bundle/RawCamera`

```diff

-1738.140.3.0.0
-  __TEXT.__text: 0x1e2d70
-  __TEXT.__auth_stubs: 0x1850
+1738.140.3.0.11
+  __TEXT.__text: 0x1e3470
+  __TEXT.__auth_stubs: 0x1870
   __TEXT.__objc_methlist: 0x16e4
   __TEXT.__const: 0x15326
-  __TEXT.__gcc_except_tab: 0x2d440
+  __TEXT.__gcc_except_tab: 0x2d588
   __TEXT.__oslogstring: 0xec0
   __TEXT.__cstring: 0xee23
   __TEXT.__dof_RawCamera: 0x8f7
-  __TEXT.__unwind_info: 0xb1d0
+  __TEXT.__unwind_info: 0xb1e8
   __TEXT.__eh_frame: 0x278
   __TEXT.__objc_classname: 0x4b9
   __TEXT.__objc_methname: 0x3918
   __TEXT.__objc_methtype: 0xdd3
   __TEXT.__objc_stubs: 0x2da0
-  __DATA_CONST.__got: 0x9b0
+  __DATA_CONST.__got: 0x9c8
   __DATA_CONST.__const: 0x2a18
   __DATA_CONST.__objc_classlist: 0x1e0
   __DATA_CONST.__objc_catlist: 0x20
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_selrefs: 0xcf8
   __DATA_CONST.__objc_superrefs: 0xf0
-  __DATA_CONST.__objc_arraydata: 0x3948
-  __AUTH_CONST.__auth_got: 0xc40
+  __DATA_CONST.__objc_arraydata: 0x3950
+  __AUTH_CONST.__auth_got: 0xc50
   __AUTH_CONST.__auth_ptr: 0xc0
   __AUTH_CONST.__const: 0x35978
   __AUTH_CONST.__cfstring: 0x18080
   __AUTH_CONST.__objc_const: 0x48b0
-  __AUTH_CONST.__objc_arrayobj: 0x570
-  __AUTH_CONST.__objc_intobj: 0x39f0
+  __AUTH_CONST.__objc_arrayobj: 0x588
+  __AUTH_CONST.__objc_intobj: 0x3a20
   __AUTH_CONST.__objc_doubleobj: 0x480
   __AUTH_CONST.__objc_dictobj: 0x4d58
   __AUTH_CONST.__objc_floatobj: 0xc0

   - /System/Library/Frameworks/UniformTypeIdentifiers.framework/UniformTypeIdentifiers
   - /System/Library/PrivateFrameworks/AppleJPEG.framework/AppleJPEG
   - /System/Library/PrivateFrameworks/AppleJPEGXL.framework/AppleJPEGXL
+  - /System/Library/PrivateFrameworks/CMPhoto.framework/CMPhoto
   - /System/Library/PrivateFrameworks/CoreAnalytics.framework/CoreAnalytics
   - /System/Library/PrivateFrameworks/MobileAsset.framework/MobileAsset
   - /usr/lib/libSystem.B.dylib

   - /usr/lib/libobjc.A.dylib
   - /usr/lib/libxml2.2.dylib
   - /usr/lib/libz.1.dylib
-  UUID: 1BE38EB6-51C0-3069-A50F-CA3B000E0847
-  Functions: 6433
-  Symbols:   781
+  UUID: AF5B7B35-3549-329B-B706-F877FA8DF849
+  Functions: 6435
+  Symbols:   786
   CStrings:  0
 
Symbols:
+ _CMPhotoDecompressionContainerCreateImageForIndex
+ _CMPhotoDecompressionContainerGetImageCount
+ _CMPhotoDecompressionSessionCreate
+ _CMPhotoDecompressionSessionCreateContainer
+ _CVPixelBufferGetDataSize
+ _kCMPhotoContainerFormatString_JFIF
+ _kCMPhotoDecompressionContainerOption_AllowedFormatsAndCodecs
+ _kCMPhotoDecompressionOption_OutputPixelFormat
- _CGImageGetBytesPerRow
- _CGImageGetHeight
- _CGImageGetWidth

```


</details>
