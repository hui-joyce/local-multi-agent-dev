# 18.4 (22E240) .vs 18.4.1 (22E252)

## IPSWs

- `iPhone17,1_18.4_22E240_Restore.ipsw`
- `iPhone17,1_18.4.1_22E252_Restore.ipsw`

## Kernel

### Version

| iOS | Version | Build | Date |
| :-- | :------ | :---- | :--- |
| 18.4 *(22E240)* | 24.4.0 | 11417.102.9~20 | Sat, 15Mar2025 18:26:55 PDT |
| 18.4.1 *(22E252)* | 24.4.0 | 11417.102.9~20 | Sat, 15Mar2025 18:26:55 PDT |

### Kexts

#### ⬆️ Updated (3)

<details>
  <summary><i>View Updated</i></summary>



#### com.apple.driver.AppleAOPAudio

>  `com.apple.driver.AppleAOPAudio`

```diff

 440.12.0.0.0
   __TEXT.__cstring: 0xc591
   __TEXT.__const: 0x136
   __TEXT.__os_log: 0xf
   __TEXT_EXEC.__text: 0x31a24

   __DATA_CONST.__mod_term_func: 0xe0
   __DATA_CONST.__const: 0xb7c8
   __DATA_CONST.__kalloc_type: 0xa00
-  UUID: DE297260-D106-30E9-99B8-E124CE2C68D8
+  UUID: 31CDCC0D-0E7C-3354-B0F5-3504D270EE2A
   Functions: 1226
   Symbols:   0
   CStrings:  1152
CStrings:
+ "18:37:03"
+ "18:37:09"
+ "Apr  7 2025"
- "19:46:32"
- "19:46:33"
- "Mar 17 2025"

```

#### com.apple.driver.AppleHIDTransportSPI

>  `com.apple.driver.AppleHIDTransportSPI`

```diff

 8150.1.0.0.0
   __TEXT.__const: 0x3c8
   __TEXT.__cstring: 0x7d31
   __TEXT_EXEC.__text: 0x43854
   __TEXT_EXEC.__auth_stubs: 0x0
   __DATA.__data: 0x3e8

   __DATA_CONST.__const: 0x32e0
   __DATA_CONST.__kalloc_type: 0xa80
   __DATA_CONST.__kalloc_var: 0x320
-  UUID: 49FF42C2-5162-3307-9397-2041692F30F8
+  UUID: C8003D35-471D-3FE4-9912-59F377151ADE
   Functions: 1041
   Symbols:   0
   CStrings:  899
CStrings:
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/hidspi/HSMDevice.h"
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/hidspi/HSMDeviceInterface.h"
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/hidspi/HSMDeviceTest.h"
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/hidspi/HSMHIDInterface.h"
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/hidspi/HSMParserTest.h"
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/hidspi/HSMSPITest.h"
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/hidspi/HSMTransferDevice.h"
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/hidspi/HSMTransferTest.h"
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/hidspi/HSParserDevice.h"
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/hidspi/HSParserTest.h"
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/hidspi/HSTransferTest.h"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/hidspi/HSMDevice.h"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/hidspi/HSMDeviceInterface.h"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/hidspi/HSMDeviceTest.h"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/hidspi/HSMHIDInterface.h"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/hidspi/HSMParserTest.h"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/hidspi/HSMSPITest.h"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/hidspi/HSMTransferDevice.h"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/hidspi/HSMTransferTest.h"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/hidspi/HSParserDevice.h"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/hidspi/HSParserTest.h"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/hidspi/HSTransferTest.h"

```

#### com.apple.driver.IOPAudioVoiceTriggerDevice

>  `com.apple.driver.IOPAudioVoiceTriggerDevice`

```diff

 440.4.0.0.0
   __TEXT.__const: 0x78
-  __TEXT.__cstring: 0x2c29
+  __TEXT.__cstring: 0x2c32
   __TEXT.__os_log: 0x16f1
   __TEXT_EXEC.__text: 0xafb0
   __TEXT_EXEC.__auth_stubs: 0x0
   __DATA.__data: 0xf8
   __DATA.__common: 0x88
   __DATA.__bss: 0x1
   __DATA_CONST.__auth_got: 0x2b0
   __DATA_CONST.__got: 0x60
   __DATA_CONST.__mod_init_func: 0x18
   __DATA_CONST.__mod_term_func: 0x18
   __DATA_CONST.__const: 0x1780
   __DATA_CONST.__kalloc_type: 0xc0
-  UUID: D62E89CF-D5DA-3591-B99C-63DE4DCB9D61
+  UUID: 01E1D500-5F49-3503-8949-033F73FE85FF
   Functions: 258
   Symbols:   0
-  CStrings:  232
+  CStrings:  233
 
CStrings:
+ "18:44:27"
+ "18:44:28"
+ "Apr  7 2025"
- "19:48:02"
- "Mar 17 2025"

```



</details>

## MachO

### filesystem

#### ⬆️ Updated (18)

<details>
  <summary><i>View Updated</i></summary>



#### Siri

>  `/Applications/Siri.app/Siri`

```diff

-3404.71.4.11.4
+3404.71.4.11.5
-  __TEXT.__text: 0xbc098
+  __TEXT.__text: 0xbc0a0
   __TEXT.__auth_stubs: 0x24f0
   __TEXT.__objc_stubs: 0x173a0
   __TEXT.__objc_methlist: 0xca08
   __TEXT.__const: 0x1544
   __TEXT.__cstring: 0x220e3
   __TEXT.__oslogstring: 0x96f7
   __TEXT.__objc_classname: 0x165f

   __TEXT.__objc_methname: 0x246dd
   __TEXT.__dlopen_cstrs: 0xb2
   __TEXT.__ustring: 0x4
   __TEXT.__swift5_typeref: 0x131c
   __TEXT.__constg_swiftt: 0x1618
   __TEXT.__swift5_reflstr: 0xc8c
   __TEXT.__swift5_fieldmd: 0x978
   __TEXT.__swift5_builtin: 0xb4

   __TEXT.__swift5_proto: 0x9c
   __TEXT.__swift5_types: 0xa8
   __TEXT.__swift5_capture: 0x3cc
   __TEXT.__swift_as_entry: 0x38
   __TEXT.__swift_as_ret: 0x38
   __TEXT.__swift5_protos: 0x14
   __TEXT.__unwind_info: 0x2d40
   __TEXT.__eh_frame: 0x950
   __DATA_CONST.__auth_got: 0x1288
   __DATA_CONST.__got: 0x1450
-  __DATA_CONST.__auth_ptr: 0x648
+  __DATA_CONST.__auth_ptr: 0x610
   __DATA_CONST.__const: 0x35d8
   __DATA_CONST.__cfstring: 0x2fe0
   __DATA_CONST.__objc_classlist: 0x348
   __DATA_CONST.__objc_catlist: 0x120
   __DATA_CONST.__objc_protolist: 0x448

   __DATA_CONST.__objc_protorefs: 0x128
   __DATA_CONST.__objc_superrefs: 0x1e0
   __DATA_CONST.__objc_doubleobj: 0xd0
   __DATA_CONST.__objc_intobj: 0xc0
   __DATA_CONST.__objc_arraydata: 0x140
   __DATA_CONST.__objc_dictobj: 0xa0
   __DATA.__objc_const: 0xec20
   __DATA.__objc_selrefs: 0x8168
   __DATA.__objc_ivar: 0x800
   __DATA.__objc_data: 0x3ab8
   __DATA.__data: 0x3908
   __DATA.__objc_stublist: 0x10
   __DATA.__bss: 0x1050
   __DATA.__common: 0x88

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: D9DAB53F-F6DB-31D3-87E8-107E62677F54
+  UUID: 71D7470F-E04A-3CE9-A294-13321F391F6D
   Functions: 4043
   Symbols:   1515
   CStrings:  8298

```

#### com.apple.DriverKit-AppleBCMWLAN

>  `/System/Library/DriverExtensions/com.apple.DriverKit-AppleBCMWLAN.dext/com.apple.DriverKit-AppleBCMWLAN`

```diff

   __TEXT.__text: 0x2b0a2c
   __TEXT.__auth_stubs: 0x24e0
   __TEXT.__init_offsets: 0x1bc
   __TEXT.__cstring: 0x7e56c
   __TEXT.__const: 0x7e310
   __TEXT.__oslogstring: 0x1f52
   __TEXT.__unwind_info: 0x5d60

   - /System/DriverKit/System/Library/PrivateFrameworks/IOFileValidation.framework/IOFileValidation
   - /System/DriverKit/System/Library/PrivateFrameworks/OLYHALDriverKit.framework/OLYHALDriverKit
   - /System/DriverKit/usr/lib/libc++.dylib
-  UUID: C405E60D-5964-3527-A840-2D9475FE774B
+  UUID: 60EBDFCE-C9C7-3A7D-8BBF-18FDE19C122F
   Functions: 13065
   Symbols:   16278
   CStrings:  12689
CStrings:
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/DriverKit.platform/Developer/SDKs/DriverKit.iPhoneOS24.4.Internal.sdk/System/DriverKit/System/Library/PrivateFrameworks/IO80211DriverKit.framework/PrivateHeaders/IO80211Util.h"
+ "Apr  7 2025 18:59:11"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/DriverKit.platform/Developer/SDKs/DriverKit.iPhoneOS24.4.Internal.sdk/System/DriverKit/System/Library/PrivateFrameworks/IO80211DriverKit.framework/PrivateHeaders/IO80211Util.h"
- "Mar 17 2025 20:06:53"

```

#### CommCenter

>  `/System/Library/Frameworks/CoreTelephony.framework/Support/CommCenter`

```diff

   __TEXT.__const: 0x1c2034
   __TEXT.__gcc_except_tab: 0x173e94
   __TEXT.__oslogstring: 0x11aff9
   __TEXT.__cstring: 0x706fc
   __TEXT.__objc_classname: 0x1ea9
   __TEXT.__objc_methname: 0x1a8df
   __TEXT.__objc_methtype: 0x1648c

   __TEXT.__swift5_types: 0x4c
   __TEXT.__swift_as_entry: 0x60
   __TEXT.__swift_as_ret: 0x2c
   __TEXT.__info_plist: 0x67a
   __TEXT.__unwind_info: 0x82320
   __TEXT.__eh_frame: 0x2268
   __DATA_CONST.__auth_got: 0x8000

   - /usr/lib/swift/libswiftos.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 4A567EB6-6F78-3C3C-9E89-C888429F06DB
+  UUID: B693379F-82FD-3B8B-879A-ABC02FBAB556
   Functions: 98407
   Symbols:   6939
   CStrings:  51548
CStrings:
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/geometry/algorithms/detail/has_self_intersections.hpp"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/geometry/algorithms/detail/has_self_intersections.hpp"

```

#### MobileStoreSettings

>  `/System/Library/PreferenceBundles/MobileStoreSettings.bundle/MobileStoreSettings`

```diff

-11.4.24.2.2
+11.4.24.2.4
   __TEXT.__text: 0x2b4a0
   __TEXT.__auth_stubs: 0x1400
   __TEXT.__objc_stubs: 0x600
   __TEXT.__objc_methlist: 0x3fc
   __TEXT.__cstring: 0x12f4
   __TEXT.__const: 0x1318
   __TEXT.__constg_swiftt: 0x7b4
   __TEXT.__swift5_typeref: 0x2abb
   __TEXT.__swift5_reflstr: 0x54a
   __TEXT.__swift5_fieldmd: 0x318
   __TEXT.__swift5_assocty: 0x140

   __TEXT.__eh_frame: 0xc08
   __DATA_CONST.__auth_got: 0xa08
   __DATA_CONST.__got: 0x4d0
-  __DATA_CONST.__auth_ptr: 0x520
+  __DATA_CONST.__auth_ptr: 0x508
   __DATA_CONST.__const: 0xd10
   __DATA_CONST.__cfstring: 0x120
   __DATA_CONST.__objc_classlist: 0x30
   __DATA_CONST.__objc_protolist: 0x38

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 834A8AF4-1408-3D7B-B396-27AF977E96D4
+  UUID: 2230C3CD-A580-3B8F-8CB3-F3E7EF28432A
   Functions: 747
   Symbols:   253
   CStrings:  404

```

#### appstored

>  `/System/Library/PrivateFrameworks/AppStoreDaemon.framework/Support/appstored`

```diff

-11.4.24.2.2
+11.4.24.2.4
-  __TEXT.__text: 0x43d8e8
+  __TEXT.__text: 0x43d300
   __TEXT.__auth_stubs: 0x3f50
-  __TEXT.__objc_stubs: 0x12820
+  __TEXT.__objc_stubs: 0x12840
   __TEXT.__objc_methlist: 0xdcc8
   __TEXT.__dlopen_cstrs: 0x45e
   __TEXT.__const: 0x1aca8
-  __TEXT.__cstring: 0x21fda
+  __TEXT.__cstring: 0x21f97
-  __TEXT.__objc_methname: 0x1acc9
+  __TEXT.__objc_methname: 0x1acd8
   __TEXT.__constg_swiftt: 0x2194
   __TEXT.__swift5_typeref: 0x3806
   __TEXT.__swift5_fieldmd: 0x232c
   __TEXT.__swift5_builtin: 0x168
   __TEXT.__swift5_reflstr: 0x193a
   __TEXT.__swift5_assocty: 0x420
   __TEXT.__swift5_proto: 0x3cc
   __TEXT.__swift5_types: 0x258
   __TEXT.__objc_classname: 0x4284
   __TEXT.__objc_methtype: 0x7b02
   __TEXT.__swift5_capture: 0x1cbc
   __TEXT.__swift5_mpenum: 0x18
   __TEXT.__swift_as_entry: 0x36c
-  __TEXT.__oslogstring: 0x38ab7
+  __TEXT.__oslogstring: 0x38a41
   __TEXT.__swift5_types2: 0x4
   __TEXT.__swift_as_ret: 0x424
   __TEXT.__swift5_protos: 0x18
   __TEXT.__gcc_except_tab: 0xabf8
   __TEXT.__info_plist: 0x5e3
-  __TEXT.__unwind_info: 0xa810
+  __TEXT.__unwind_info: 0xa7f0
   __TEXT.__eh_frame: 0xb06c
   __DATA_CONST.__auth_got: 0x1fb8
   __DATA_CONST.__got: 0x18c0
-  __DATA_CONST.__auth_ptr: 0x8f0
+  __DATA_CONST.__auth_ptr: 0x8e8
-  __DATA_CONST.__const: 0x1f638
+  __DATA_CONST.__const: 0x1f5e8
-  __DATA_CONST.__cfstring: 0x1b380
+  __DATA_CONST.__cfstring: 0x1b320
   __DATA_CONST.__objc_classlist: 0x1650
   __DATA_CONST.__objc_catlist: 0x58
   __DATA_CONST.__objc_protolist: 0x538
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_protorefs: 0x190
   __DATA_CONST.__objc_superrefs: 0xdc8
   __DATA_CONST.__objc_intobj: 0x1dd0
   __DATA_CONST.__objc_arraydata: 0x870
   __DATA_CONST.__objc_arrayobj: 0x4b0
   __DATA_CONST.__objc_dictobj: 0x168
   __DATA_CONST.__objc_doubleobj: 0x40
   __DATA.__objc_const: 0x35738
-  __DATA.__objc_selrefs: 0x62c0
+  __DATA.__objc_selrefs: 0x62c8
   __DATA.__objc_ivar: 0x2494
   __DATA.__objc_data: 0xff80
   __DATA.__data: 0x7580
   __DATA.__bss: 0x81d0
   __DATA.__common: 0xb64
   - /System/Library/Frameworks/Accounts.framework/Accounts
   - /System/Library/Frameworks/AdAttributionKit.framework/AdAttributionKit
   - /System/Library/Frameworks/BackgroundAssets.framework/BackgroundAssets

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 5F760438-346E-3E2D-A0D3-E97735810D9B
+  UUID: 4D4EBECE-6B02-3A0A-8028-AEC02D2A8FD2
-  Functions: 12584
+  Functions: 12573
   Symbols:   2036
-  CStrings:  18428
+  CStrings:  18421
 
CStrings:
+ "17:59:21"
+ "Apr  4 2025"
+ "addDependency:"
- "22:07:10"
- "Completed store queue checks on reboot"
- "Failed to complete store queue checks on reboot; will retry next daemon launch"
- "Mar 11 2025"
- "Reboot"
- "checkStoreQueues"
- "com.apple.appstored.TaskQueue.barrierBlock"

```

#### assistantd

>  `/System/Library/PrivateFrameworks/AssistantServices.framework/assistantd`

```diff

-3404.80.4.11.3
+3404.80.4.11.4
   __TEXT.__text: 0x36c048
   __TEXT.__auth_stubs: 0x34b0
   __TEXT.__objc_stubs: 0x45280

   __TEXT.__const: 0x10990
   __TEXT.__dlopen_cstrs: 0xafa
   __TEXT.__gcc_except_tab: 0x487c
   __TEXT.__cstring: 0x51712
   __TEXT.__oslogstring: 0x3f68c
   __TEXT.__objc_classname: 0x519f
   __TEXT.__objc_methname: 0x5d0d9

   - /usr/lib/libobjc.A.dylib
   - /usr/lib/libresolv.9.dylib
   - /usr/lib/libz.1.dylib
-  UUID: E486252C-DC13-3AD4-9021-BA417E98D6B6
+  UUID: B770C9F7-E173-3FEF-93EA-04E86239E55F
   Functions: 14308
   Symbols:   2888
   CStrings:  29413
CStrings:
+ "MobileAssistantDaemons-3404.80.4.11.4"
- "MobileAssistantDaemons-3404.80.4.11.3"

```

#### diskimagescontroller

>  `/System/Library/PrivateFrameworks/DiskImages2.framework/XPCServices/diskimagescontroller.xpc/diskimagescontroller`

```diff

   __TEXT.__objc_methlist: 0x2d7c
   __TEXT.__gcc_except_tab: 0x14438
   __TEXT.__const: 0xe0a4
   __TEXT.__cstring: 0x103e8
   __TEXT.__oslogstring: 0x14a5
   __TEXT.__objc_methname: 0x5b23
   __TEXT.__objc_classname: 0x5af

   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
   - /usr/local/lib/libcurl.4.dylib
-  UUID: DFD258B0-D65A-37EE-8B10-00C95C9F94E5
+  UUID: A0BA7CB7-0D85-392E-AED6-49569725F2B9
   Functions: 8336
   Symbols:   709
   CStrings:  3625
CStrings:
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/algorithm/hex.hpp"
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/uuid/detail/sha1.hpp"
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/uuid/string_generator.hpp"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/algorithm/hex.hpp"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/uuid/detail/sha1.hpp"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/uuid/string_generator.hpp"

```

#### softwareupdated

>  `/System/Library/PrivateFrameworks/MobileSoftwareUpdate.framework/Support/softwareupdated`

```diff

-2171.100.143.0.0
+2171.102.1.0.0
   __TEXT.__text: 0x2a828
   __TEXT.__auth_stubs: 0x1480
   __TEXT.__objc_stubs: 0x3980

   __TEXT.__objc_methname: 0x3b0d
   __TEXT.__objc_methtype: 0x1084
   __TEXT.__oslogstring: 0x32d6
   __TEXT.__info_plist: 0x594
   __TEXT.__unwind_info: 0x960
   __DATA_CONST.__auth_got: 0xa50
   __DATA_CONST.__got: 0x3a0

   - /usr/lib/liblzma.5.dylib
   - /usr/lib/libobjc.A.dylib
   - /usr/lib/libpartition2_dynamic.dylib
-  UUID: 0549EC7B-FF6B-3642-BA41-C2E4A9CC5A1B
+  UUID: 42C40E17-4BEE-39FE-A4BE-C4F4E06B6715
   Functions: 772
   Symbols:   5879
   CStrings:  3713
Symbols:
+ /AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/lib/libUpdateMetrics.a(UMEventCheckpoint.o)
+ /AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/lib/libUpdateMetrics.a(UMEventRecorder.o)
+ /AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/lib/libUpdateMetrics.a(UMEventShim.o)
+ /AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/lib/libUpdateMetrics.a(UMEventSubmitter.o)
+ /AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/lib/libRamrodUpdateBrain.a(ramrod_error.o)
+ /AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/lib/libRamrodUpdateBrain.a(ramrod_log.o)
+ /AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/lib/libRamrodUpdateBrain.a(ramrod_splat.o)
+ /AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/lib/libpartition.a(partition.o)
+ /AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/lib/librestorecommon.a(RestoreCommon.o)
- /AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/lib/libUpdateMetrics.a(UMEventCheckpoint.o)
- /AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/lib/libUpdateMetrics.a(UMEventRecorder.o)
- /AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/lib/libUpdateMetrics.a(UMEventShim.o)
- /AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/lib/libUpdateMetrics.a(UMEventSubmitter.o)
- /AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/lib/libRamrodUpdateBrain.a(ramrod_error.o)
- /AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/lib/libRamrodUpdateBrain.a(ramrod_log.o)
- /AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/lib/libRamrodUpdateBrain.a(ramrod_splat.o)
- /AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/lib/libpartition.a(partition.o)
- /AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/lib/librestorecommon.a(RestoreCommon.o)

```

#### IPConfiguration

>  `/System/Library/SystemConfiguration/IPConfiguration.bundle/IPConfiguration`

```diff

-494.102.1.0.0
+494.102.2.0.0
-  __TEXT.__text: 0x59cf0
+  __TEXT.__text: 0x59d50
   __TEXT.__auth_stubs: 0xf90
   __TEXT.__const: 0x300
   __TEXT.__oslogstring: 0x63a5
   __TEXT.__cstring: 0x3c92
-  __TEXT.__unwind_info: 0xb80
+  __TEXT.__unwind_info: 0xb90
   __DATA_CONST.__auth_got: 0x7c8
   __DATA_CONST.__got: 0x370
   __DATA_CONST.__auth_ptr: 0xf8
   __DATA_CONST.__const: 0x1d30
   __DATA_CONST.__cfstring: 0x27c0
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA.__data: 0x110
   __DATA.__bss: 0x1e0
   __DATA.__common: 0x10
   - /System/Library/Frameworks/CoreFoundation.framework/CoreFoundation

   - /usr/lib/libMobileGestalt.dylib
   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libbsm.0.dylib
-  UUID: AA4D7092-7655-3419-842B-FC368774724D
+  UUID: 2F8E78A7-42B7-3C96-9B34-4A69D7A1CBEF
-  Functions: 985
+  Functions: 987
   Symbols:   466
   CStrings:  1988
 
CStrings:
+ "IPv6.Prefix=%s/%d;IPv6.RouterHardwareAddress="
- "IPv6.Prefix=%@/%@;IPv6.RouterHardwareAddress="

```

#### libRPAC.dylib

>  `/usr/lib/libRPAC.dylib`

```diff

-84.0.0.0.0
+88.0.0.0.0
-  __TEXT.__text: 0x9245c
+  __TEXT.__text: 0x92424
-  __TEXT.__auth_stubs: 0xad0
+  __TEXT.__auth_stubs: 0xac0
   __TEXT.__objc_stubs: 0x1a0
   __TEXT.__init_offsets: 0x4
-  __TEXT.__cstring: 0x5190
+  __TEXT.__cstring: 0x5140
   __TEXT.__gcc_except_tab: 0x5c
   __TEXT.__const: 0x1d58
   __TEXT.__objc_methname: 0x13b
   __TEXT.__oslogstring: 0x1d
   __TEXT.__objc_classname: 0x1
-  __TEXT.__unwind_info: 0x320
+  __TEXT.__unwind_info: 0x330
-  __DATA_CONST.__auth_got: 0x580
+  __DATA_CONST.__auth_got: 0x578
-  __DATA_CONST.__got: 0x148
+  __DATA_CONST.__got: 0x140
   __DATA_CONST.__auth_ptr: 0x10
   __DATA_CONST.__const: 0x3f0
   __DATA_CONST.__cfstring: 0x260
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_arraydata: 0x20
   __DATA_CONST.__objc_arrayobj: 0x30
-  __AUTH_CONST.__interpose: 0x230
+  __AUTH_CONST.__interpose: 0x220
   __DATA.__objc_selrefs: 0x88
-  __DATA.__data: 0x7c8
+  __DATA.__data: 0x7c4
   __DATA.__common: 0x800e8
-  __DATA.__bss: 0x5809e0
+  __DATA.__bss: 0x5807d8
   - /System/Library/Frameworks/CoreFoundation.framework/CoreFoundation
   - /System/Library/Frameworks/Foundation.framework/Foundation
   - /System/Library/Frameworks/ImageIO.framework/ImageIO

   - /usr/lib/libc++.1.dylib
   - /usr/lib/libobjc.A.dylib
   - /usr/lib/libsqlite3.dylib
-  UUID: 484E4D90-56E9-3A4E-84D4-EC82121D79D8
+  UUID: 952FD03E-567F-3E2D-A26A-8748FF1471AD
-  Functions: 277
+  Functions: 279
-  Symbols:   732
+  Symbols:   730
-  CStrings:  654
+  CStrings:  652
 
Symbols:
+ _lockLockInDispatchLockMap
+ _lockLockInNSCondtionLockMap
+ _unlockLockInDispatchLockMap
+ _unlockLockInNSConditionLockMap
- __ZL18max_primitive_maps
- __interpose_dlsym
- _dlsym
- _interposed_dlsym
- deletePrimitiveEntry.cold.1
- interposed_dlsym.dlsym_count
CStrings:
+ "Inversion detection for %s\n"
+ "SemaphoreWaitingAGPCLogType"
+ "semaphorewaitingagpclogtype"
- "DispatchSemaphoreWaitingOnMainThreadAGPCLogType"
- "deletePrimitiveEntry"
- "dispatchsemaphorewaitingonmainthreadagpclogtype"
- "dlsym"
- "libRPAC.dylib: interposed_dlsym invoked\n"

```

#### NRDUpdated

>  `/usr/libexec/NRDUpdated`

```diff

-2171.100.143.0.0
+2171.102.1.0.0
   __TEXT.__text: 0xbaa4
   __TEXT.__auth_stubs: 0x660
   __TEXT.__objc_stubs: 0x1b00
   __TEXT.__objc_methlist: 0xc54
   __TEXT.__const: 0x90
   __TEXT.__cstring: 0x10a9
   __TEXT.__gcc_except_tab: 0x1a4
   __TEXT.__objc_methname: 0x1a46
   __TEXT.__objc_classname: 0x20f
   __TEXT.__objc_methtype: 0x833
   __TEXT.__oslogstring: 0x1792
-  __TEXT.__info_plist: 0x5fa
+  __TEXT.__info_plist: 0x600
   __TEXT.__unwind_info: 0x338
   __DATA_CONST.__auth_got: 0x340
   __DATA_CONST.__got: 0x158

   - /usr/lib/libMobileGestalt.dylib
   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: AB949DBD-4185-360D-A126-B20675E7FBFD
+  UUID: A72BAD11-519B-345A-BFF5-9072D13B3893
   Functions: 271
   Symbols:   2146
   CStrings:  842
CStrings:
+ "10:26:24"
+ "Mar 29 2025"
- "00:34:06"
- "Mar  8 2025"

```

#### diskimagesiod

>  `/usr/libexec/diskimagesiod`

```diff

   __TEXT.__objc_methlist: 0x30bc
   __TEXT.__gcc_except_tab: 0x133ac
   __TEXT.__const: 0xd964
   __TEXT.__cstring: 0xe154
   __TEXT.__oslogstring: 0x1f4b
   __TEXT.__objc_methname: 0x6561
   __TEXT.__objc_classname: 0x5b1

   __TEXT.__swift5_fieldmd: 0x10
   __TEXT.__swift5_types: 0x4
   __TEXT.__ustring: 0x13c
   __TEXT.__info_plist: 0x454
   __TEXT.__unwind_info: 0xa010
   __TEXT.__eh_frame: 0x158
   __DATA_CONST.__auth_got: 0x1018

   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
   - /usr/local/lib/libcurl.4.dylib
-  UUID: 64A195C3-CB7A-3F21-BABF-9250AE5350D1
+  UUID: F2AFF907-A6B8-338A-A945-64006F5DC4F8
   Functions: 8207
   Symbols:   708
   CStrings:  3837
CStrings:
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/algorithm/hex.hpp"
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/uuid/detail/sha1.hpp"
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/uuid/string_generator.hpp"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/algorithm/hex.hpp"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/uuid/detail/sha1.hpp"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/uuid/string_generator.hpp"

```

#### locationd

>  `/usr/libexec/locationd`

```diff

   __TEXT.__init_offsets: 0xb30
   __TEXT.__objc_methlist: 0x2eff8
   __TEXT.__const: 0x1503e9
   __TEXT.__cstring: 0x1d9b55
   __TEXT.__gcc_except_tab: 0xdeaa4
   __TEXT.__objc_methname: 0x5fe15
   __TEXT.__oslogstring: 0x275624

   __TEXT.__swift5_reflstr: 0x29
   __TEXT.__swift5_builtin: 0x14
   __TEXT.__swift5_capture: 0x40
   __TEXT.__info_plist: 0x6ba
   __TEXT.__unwind_info: 0x6f250
   __TEXT.__eh_frame: 0x1370
   __DATA_CONST.__auth_got: 0x3070

   - /usr/lib/swift/libswiftos.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 6DEA3C52-31EE-3C91-95E7-E5E0707ADB89
+  UUID: 789ED4AF-2459-3842-A498-53D5A08E2352
   Functions: 100701
   Symbols:   3067
   CStrings:  91557
CStrings:
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/geometry/algorithms/detail/throw_on_empty_input.hpp"
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/uuid/detail/random_provider_posix.ipp"
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/uuid/string_generator.hpp"
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/google/protobuf/repeated_field.h"
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/google/protobuf/wire_format_lite_inl.h"
+ "19:17:04"
+ "19:32:44"
+ "Apr  7 2025"
+ "Apr  7 2025 19:19:55"
- "/AppleInternal/Library/BuildRoots/de27167c-06c7-11f0-ae84-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/geometry/algorithms/detail/throw_on_empty_input.hpp"
- "/AppleInternal/Library/BuildRoots/de27167c-06c7-11f0-ae84-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/uuid/detail/random_provider_posix.ipp"
- "/AppleInternal/Library/BuildRoots/de27167c-06c7-11f0-ae84-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/uuid/string_generator.hpp"
- "/AppleInternal/Library/BuildRoots/de27167c-06c7-11f0-ae84-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/google/protobuf/repeated_field.h"
- "/AppleInternal/Library/BuildRoots/de27167c-06c7-11f0-ae84-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/google/protobuf/wire_format_lite_inl.h"
- "19:43:49"
- "20:06:31"
- "Mar 25 2025"
- "Mar 25 2025 19:47:09"

```

#### nearbyd

>  `/usr/libexec/nearbyd`

```diff

   __TEXT.__objc_methlist: 0xc08c
   __TEXT.__gcc_except_tab: 0x49fd4
   __TEXT.__const: 0x2d6920
   __TEXT.__cstring: 0x32b5a
   __TEXT.__objc_methname: 0x1b728
   __TEXT.__oslogstring: 0x505a0
   __TEXT.__objc_classname: 0x18e5

   __TEXT.__swift5_reflstr: 0x13
   __TEXT.__swift5_fieldmd: 0x28
   __TEXT.__swift5_types: 0x4
   __TEXT.__info_plist: 0x40f
   __TEXT.__unwind_info: 0x17d50
   __TEXT.__eh_frame: 0x38
   __DATA_CONST.__auth_got: 0x1478

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 49E77228-48BE-3CFE-91FC-A5CD1C39A1EE
+  UUID: F5523041-3C93-3AB9-8B61-07926BF07BF7
   Functions: 19161
   Symbols:   999
   CStrings:  19622
CStrings:
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/google/protobuf/repeated_field.h"
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/google/protobuf/wire_format_lite_inl.h"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/google/protobuf/repeated_field.h"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/google/protobuf/wire_format_lite_inl.h"

```

#### wifianalyticsd

>  `/usr/libexec/wifianalyticsd`

```diff

   __TEXT.__objc_methlist: 0x31a8
   __TEXT.__const: 0x118
   __TEXT.__dlopen_cstrs: 0x17a
   __TEXT.__cstring: 0x12c77
   __TEXT.__gcc_except_tab: 0x4d74
   __TEXT.__objc_methname: 0xce26
   __TEXT.__oslogstring: 0x125db

   - /usr/lib/libc++.1.dylib
   - /usr/lib/libobjc.A.dylib
   - /usr/lib/libsqlite3.dylib
-  UUID: 8C4C5A7D-7EBB-3C06-A192-1A84AB3C42DF
+  UUID: EA77D9F8-17BE-3235-8915-A312F7BED484
   Functions: 1240
   Symbols:   373
   CStrings:  7900
CStrings:
+ "Apr  7 2025 18:59:56"
+ "WiFiAnalytics_executables-725.36 Apr  7 2025 18:59:52"
- "Mar 17 2025 19:51:49"
- "WiFiAnalytics_executables-725.36 Mar 17 2025 19:51:48"

```

#### wifip2pd

>  `/usr/libexec/wifip2pd`

```diff

   __TEXT.__auth_stubs: 0x38f0
   __TEXT.__objc_methlist: 0x13ec
   __TEXT.__const: 0x31ca0
   __TEXT.__cstring: 0xb30a
   __TEXT.__swift5_typeref: 0x968c
   __TEXT.__swift5_entry: 0x8
   __TEXT.__oslogstring: 0xd393

   __TEXT.__objc_methtype: 0xd1d
   __TEXT.__swift5_capture: 0x5a7c
   __TEXT.__swift5_mpenum: 0x164
   __TEXT.__info_plist: 0x56f
   __TEXT.__unwind_info: 0xc5a0
   __TEXT.__eh_frame: 0x151b8
   __DATA_CONST.__auth_got: 0x1c78

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 8FB8D31E-C203-3AED-8212-4BF9BB31F7A9
+  UUID: 5DA4A22F-2ABD-313D-9611-397F2AF87DEF
   Functions: 19110
   Symbols:   1762
   CStrings:  2887
CStrings:
+ "WiFiP2P-780.43 Apr 07 2025 18:04:59"
- "WiFiP2P-780.43 Mar 17 2025 19:03:48"

```

#### bluetoothd

>  `/usr/sbin/bluetoothd`

```diff

   __TEXT.__objc_methlist: 0x6554
   __TEXT.__const: 0xa77c
   __TEXT.__gcc_except_tab: 0x619a4
   __TEXT.__cstring: 0xa2bbe
   __TEXT.__objc_classname: 0x7eb
   __TEXT.__objc_methname: 0x15e31
   __TEXT.__objc_methtype: 0x44e3
   __TEXT.__oslogstring: 0xa1867
   __TEXT.__ustring: 0x34
   __TEXT.__dlopen_cstrs: 0x64
   __TEXT.__info_plist: 0x420
   __TEXT.__unwind_info: 0x1faa8
   __TEXT.__eh_frame: 0x60
   __DATA_CONST.__auth_got: 0x2328

   - /usr/lib/libobjc.A.dylib
   - /usr/lib/libprotobuf.dylib
   - /usr/lib/libsqlite3.dylib
-  UUID: 7523CA9E-A62A-3D20-97D7-D75F41EBCC53
+  UUID: DC50C3F4-3026-30C5-BB06-E088007AF613
   Functions: 30457
   Symbols:   1547
   CStrings:  39592
CStrings:
+ "19:01:07"
+ "Apr  7 2025"
- "20:03:16"
- "Mar 17 2025"

```

#### wifid

>  `/usr/sbin/wifid`

```diff

-1925.47.4.1.0
+1925.47.4.2.0
   __TEXT.__text: 0x1a8a24
   __TEXT.__auth_stubs: 0x2740
   __TEXT.__objc_stubs: 0x12560
   __TEXT.__objc_methlist: 0x60e8
   __TEXT.__gcc_except_tab: 0x1c5c
   __TEXT.__const: 0x8e0
   __TEXT.__cstring: 0x6b042
   __TEXT.__objc_methname: 0x17ce5
   __TEXT.__objc_classname: 0x83a
   __TEXT.__objc_methtype: 0x2d53
   __TEXT.__ustring: 0x4c2
   __TEXT.__oslogstring: 0x1117
   __TEXT.__dlopen_cstrs: 0x1a5
   __TEXT.__info_plist: 0x63e
   __TEXT.__unwind_info: 0x3b20
   __DATA_CONST.__auth_got: 0x13b0
   __DATA_CONST.__got: 0x15d0

   - /usr/lib/libnetwork.dylib
   - /usr/lib/libobjc.A.dylib
   - /usr/lib/libpcap.A.dylib
-  UUID: B66CCA24-80AB-34B3-8E14-7E3989EFED45
+  UUID: 411ACF79-4E01-3A55-A761-D7A49A5B00F8
   Functions: 7515
   Symbols:   1342
   CStrings:  19683
CStrings:
+ "WiFiManager-1925.47.4.2 Apr  7 2025 18:59:25"
+ "WiFiManager-1925.47.4.2 Apr  7 2025 18:59:59"
- "WiFiManager-1925.47.4.1 Mar 17 2025 20:01:17"
- "WiFiManager-1925.47.4.1 Mar 17 2025 20:01:45"

```



</details>

## Firmware

### iBoot

| iOS | Version |
| :-- | :------ |
| 18.4 *(22E240)* | iBoot-11881.100.993 |
| 18.4.1 *(22E252)* | iBoot-11881.100.993 |

## DSC

### WebKit

| iOS | Version |
| :-- | :------ |
| 18.4 *(22E240)* | 621.1.15.10.7 |
| 18.4.1 *(22E252)* | 621.1.15.10.7 |

### Dylibs

#### ⬆️ Updated (19)

<details>
  <summary><i>View Updated</i></summary>



#### AudioCodecs

>  `/System/Library/Frameworks/AudioToolbox.framework/AudioCodecs`

```diff

-746.5.10.0.0
+746.5.11.0.0
-  __TEXT.__text: 0x598514
+  __TEXT.__text: 0x598534
   __TEXT.__auth_stubs: 0x1540
   __TEXT.__const: 0x3028cc
   __TEXT.__cstring: 0xa204
   __TEXT.__gcc_except_tab: 0x106b8
   __TEXT.__oslogstring: 0x17be7
   __TEXT.__ustring: 0x20
   __TEXT.__unwind_info: 0x8a00
   __TEXT.__eh_frame: 0x790
   __DATA_CONST.__got: 0x258
   __DATA_CONST.__const: 0xd2b8
   __AUTH_CONST.__auth_got: 0xaa8
   __AUTH_CONST.__auth_ptr: 0x10
   __AUTH_CONST.__const: 0xf2a8
   __AUTH_CONST.__cfstring: 0x4320
   __DATA.__data: 0x2d4
   __DATA.__bss: 0x5d8
   __DATA_DIRTY.__bss: 0xe8
   - /System/Library/Frameworks/Accelerate.framework/Accelerate

   - /usr/lib/libMobileGestalt.dylib
   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libc++.1.dylib
-  UUID: C37282EE-EF5F-323D-BA9B-C5B820271773
+  UUID: 2D3D1ECD-D220-30F0-91EF-9EE201C5EAA9
   Functions: 8800
   Symbols:   25768
   CStrings:  3578
CStrings:
+ "17:49:08"
+ "Apr  4 2025"
- "21:23:18"
- "Mar  7 2025"

```

#### CoreLocation

>  `/System/Library/Frameworks/CoreLocation.framework/CoreLocation`

```diff

 2960.0.60.0.0
   __TEXT.__text: 0x1c3f90
   __TEXT.__auth_stubs: 0x1a40
   __TEXT.__objc_methlist: 0xa26c
   __TEXT.__const: 0x4a95
   __TEXT.__gcc_except_tab: 0xd448
   __TEXT.__oslogstring: 0x34996
   __TEXT.__cstring: 0x215fa
   __TEXT.__ustring: 0x750
   __TEXT.__unwind_info: 0x5438
   __TEXT.__objc_classname: 0x13ec

   - /usr/lib/libsqlite3.dylib
   - /usr/lib/libxml2.2.dylib
   - /usr/lib/libz.1.dylib
-  UUID: 8737AA4D-14D4-32FA-9CEE-8F0342AA0772
+  UUID: 39D28978-9170-3EE3-8747-E3FCAA9E0DE8
   Functions: 5086
   Symbols:   1123
   CStrings:  11344
CStrings:
+ "18:46:31"
+ "Apr  7 2025"
- "19:12:50"
- "Mar 25 2025"

```

#### CoreMotion

>  `/System/Library/Frameworks/CoreMotion.framework/CoreMotion`

```diff

 2960.0.60.0.0
   __TEXT.__text: 0x352424
   __TEXT.__auth_stubs: 0x29f0
   __TEXT.__objc_methlist: 0xbf5c
   __TEXT.__const: 0xa4d8
   __TEXT.__swift5_typeref: 0x257

   __TEXT.__constg_swiftt: 0xb8
   __TEXT.__swift5_fieldmd: 0x70
   __TEXT.__swift5_capture: 0x40
   __TEXT.__cstring: 0x3fc71
   __TEXT.__oslogstring: 0x2820b
   __TEXT.__swift5_proto: 0x10
   __TEXT.__swift5_types: 0x10

   __DATA_CONST.__objc_arraydata: 0x250
   __AUTH_CONST.__auth_got: 0x1510
   __AUTH_CONST.__auth_ptr: 0xf0
   __AUTH_CONST.__const: 0x12bc8
   __AUTH_CONST.__cfstring: 0x12260
   __AUTH_CONST.__objc_const: 0x1ae08
   __AUTH_CONST.__objc_arrayobj: 0x90

   - /usr/lib/swift/libswiftos.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: EC07CEB1-AAB5-3630-97CD-2C6A11BB0150
+  UUID: 02809943-8CC0-3008-9BEB-025ECA667E1A
   Functions: 11186
   Symbols:   1735
   CStrings:  17367
CStrings:
+ "18:51:00"
+ "Apr  7 2025"
- "19:16:19"
- "Mar 25 2025"

```

#### CoreServices

>  `/System/Library/Frameworks/CoreServices.framework/CoreServices`

```diff

-1378.17.0.0.0
+1378.18.0.0.0
-  __TEXT.__text: 0x199688
+  __TEXT.__text: 0x199700
   __TEXT.__auth_stubs: 0x3210
   __TEXT.__objc_methlist: 0xc3ec
   __TEXT.__const: 0x920
   __TEXT.__cstring: 0x208e9
   __TEXT.__oslogstring: 0x12f56
   __TEXT.__gcc_except_tab: 0x24424
   __TEXT.__ustring: 0x23c
-  __TEXT.__unwind_info: 0xa710
+  __TEXT.__unwind_info: 0xa718
   __TEXT.__eh_frame: 0x60
   __TEXT.__objc_classname: 0x1d52
   __TEXT.__objc_methname: 0x1be4b
   __TEXT.__objc_methtype: 0xadff
   __TEXT.__objc_stubs: 0xf600
   __DATA_CONST.__got: 0x9f8
   __DATA_CONST.__const: 0x6a70
   __DATA_CONST.__objc_classlist: 0x670
   __DATA_CONST.__objc_catlist: 0x48
   __DATA_CONST.__objc_protolist: 0x140

   __DATA_CONST.__objc_arraydata: 0x198
   __AUTH_CONST.__auth_got: 0x1920
   __AUTH_CONST.__auth_ptr: 0x60
   __AUTH_CONST.__const: 0x3468
   __AUTH_CONST.__cfstring: 0x15f80
   __AUTH_CONST.__objc_const: 0x12520
   __AUTH_CONST.__objc_intobj: 0x7e0
   __AUTH_CONST.__objc_dictobj: 0xf0
   __AUTH_CONST.__objc_arrayobj: 0xf0
   __AUTH.__objc_data: 0x2940
   __AUTH.__data: 0x328
   __DATA.__objc_ivar: 0xa24
   __DATA.__data: 0x1350
   __DATA.__bss: 0xeb8
   __DATA.__common: 0x40
   __DATA_DIRTY.__objc_data: 0x1720
   __DATA_DIRTY.__data: 0x58
   __DATA_DIRTY.__crash_info: 0x40
   __DATA_DIRTY.__bss: 0x858
   __DATA_DIRTY.__common: 0x8

   - /usr/lib/libicucore.A.dylib
   - /usr/lib/libobjc.A.dylib
   - /usr/lib/libsqlite3.dylib
-  UUID: A14CBB38-86E6-3807-9738-A00B19AA4ED7
+  UUID: 0E9DF97F-96AA-3C2D-A5AD-3A764A0C4330
-  Functions: 8263
+  Functions: 8264
-  Symbols:   26933
+  Symbols:   26936
   CStrings:  13085
 
Symbols:
+ GCC_except_table128
+ GCC_except_table142
+ GCC_except_table164
+ __ZN14LaunchServices17BindingEvaluation25BindingEligibilityChecker36isDefaultAppCategoryBindingEligibileERKNS0_5StateEPK24LSDefaultAppCategoryInfoRKNS0_15ExtendedBindingE
- GCC_except_table162

```

#### libCommCenterAWDMetrics.dylib

>  `/System/Library/Frameworks/CoreTelephony.framework/Support/libCommCenterAWDMetrics.dylib`

```diff

 12322.6.0.0.0
   __TEXT.__text: 0xb7910
   __TEXT.__auth_stubs: 0x380
   __TEXT.__init_offsets: 0x44
   __TEXT.__const: 0x3664
   __TEXT.__gcc_except_tab: 0x22f4
   __TEXT.__cstring: 0x45a4
   __TEXT.__unwind_info: 0x2d70
   __DATA_CONST.__got: 0x28
   __AUTH_CONST.__auth_got: 0x1c8
   __AUTH_CONST.__const: 0xaa70
   __DATA_DIRTY.__bss: 0xa00
   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libTelephonyCapabilities.dylib
   - /usr/lib/libc++.1.dylib
   - /usr/lib/libprotobuf-lite.dylib
   - /usr/lib/libprotobuf.dylib
-  UUID: 6C3576C0-87C9-3769-85DB-3EE594D4A4E1
+  UUID: 44015565-6021-3EC2-9D8D-9DBFB36A5B7D
   Functions: 3829
   Symbols:   8838
   CStrings:  408
CStrings:
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/google/protobuf/repeated_field.h"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/google/protobuf/repeated_field.h"

```

#### libCommCenterKCommandDrivers.dylib

>  `/System/Library/Frameworks/CoreTelephony.framework/Support/libCommCenterKCommandDrivers.dylib`

```diff

 12322.6.0.0.0
   __TEXT.__text: 0x12e7f0
   __TEXT.__auth_stubs: 0x7860
   __TEXT.__const: 0x17591
   __TEXT.__gcc_except_tab: 0x14b64
   __TEXT.__oslogstring: 0x13a4a
   __TEXT.__cstring: 0x4727
   __TEXT.__unwind_info: 0x7100
   __DATA_CONST.__got: 0x438
   __DATA_CONST.__const: 0x988
   __AUTH_CONST.__auth_got: 0x3c38
   __AUTH_CONST.__const: 0x113d0
   __AUTH_CONST.__cfstring: 0x100
   __DATA.__bss: 0x18
   - /System/Library/Frameworks/CoreFoundation.framework/CoreFoundation

   - /usr/lib/libTelephonyCapabilities.dylib
   - /usr/lib/libTelephonyUtilDynamic.dylib
   - /usr/lib/libc++.1.dylib
-  UUID: AC162BA6-90CA-3CB1-9A00-4BF289A55483
+  UUID: D0FE3507-1D3A-3901-A4A0-1B642F2B822B
   Functions: 5530
   Symbols:   17766
   CStrings:  2329
CStrings:
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/ARI/ari_sdk_msg.h"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/ARI/ari_sdk_msg.h"

```

#### _MapKit_SwiftUI

>  `/System/Library/Frameworks/_MapKit_SwiftUI.framework/_MapKit_SwiftUI`

```diff

 2464.34.9.12.31
   __TEXT.__text: 0xacae0
   __TEXT.__auth_stubs: 0x2160
   __TEXT.__objc_methlist: 0xbc4
   __TEXT.__const: 0x9480
   __TEXT.__constg_swiftt: 0x4a08
   __TEXT.__swift5_typeref: 0x3838
   __TEXT.__swift5_reflstr: 0x1fca
   __TEXT.__swift5_fieldmd: 0x30c4
   __TEXT.__swift5_builtin: 0x208

   __DATA_CONST.__objc_selrefs: 0x9f0
   __DATA_CONST.__objc_protorefs: 0x48
   __AUTH_CONST.__auth_got: 0x10b0
-  __AUTH_CONST.__auth_ptr: 0x10c8
+  __AUTH_CONST.__auth_ptr: 0xeb8
   __AUTH_CONST.__const: 0x6fe0
   __AUTH_CONST.__objc_const: 0x14e0
   __AUTH.__objc_data: 0x7a0
   __AUTH.__data: 0x1f88
   __DATA.__data: 0x3d88
   __DATA.__objc_stublist: 0x8
   __DATA.__bss: 0x8598
   __DATA.__common: 0x60
   __DATA_DIRTY.__objc_data: 0xf8
   __DATA_DIRTY.__data: 0x28
   - /System/Library/Frameworks/Combine.framework/Combine
   - /System/Library/Frameworks/CoreFoundation.framework/CoreFoundation
   - /System/Library/Frameworks/CoreLocation.framework/CoreLocation

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 484792EF-3A88-37EB-B991-C3BAD02063A3
+  UUID: FEE2B399-57DD-36D0-9AE9-58648376C76E
   Functions: 3726
   Symbols:   1967
   CStrings:  575

```

#### AssistantServices

>  `/System/Library/PrivateFrameworks/AssistantServices.framework/AssistantServices`

```diff

-3404.80.4.11.3
+3404.80.4.11.4
-  __TEXT.__text: 0x1ac3f8
+  __TEXT.__text: 0x1ac720
   __TEXT.__auth_stubs: 0x1550
   __TEXT.__objc_methlist: 0x1dbfc
   __TEXT.__const: 0x458
   __TEXT.__dlopen_cstrs: 0x484
   __TEXT.__gcc_except_tab: 0x2adc
-  __TEXT.__cstring: 0x3d2cb
+  __TEXT.__cstring: 0x3d2d1
-  __TEXT.__oslogstring: 0x10ea8
+  __TEXT.__oslogstring: 0x10f6b
   __TEXT.__ustring: 0x2ac
-  __TEXT.__unwind_info: 0x7d10
+  __TEXT.__unwind_info: 0x7d18
   __TEXT.__objc_classname: 0x4f0c
   __TEXT.__objc_methname: 0x3b165
   __TEXT.__objc_methtype: 0xaaf0
   __TEXT.__objc_stubs: 0x247e0
   __DATA_CONST.__got: 0x1648
   __DATA_CONST.__const: 0x8438
   __DATA_CONST.__objc_classlist: 0xdd8
   __DATA_CONST.__objc_catlist: 0x290
   __DATA_CONST.__objc_protolist: 0x558
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_selrefs: 0xc328
   __DATA_CONST.__objc_protorefs: 0x148
   __DATA_CONST.__objc_superrefs: 0xdf0
   __DATA_CONST.__objc_arraydata: 0x2090
   __AUTH_CONST.__auth_got: 0xab8
   __AUTH_CONST.__auth_ptr: 0x8
-  __AUTH_CONST.__const: 0x3a60
+  __AUTH_CONST.__const: 0x3a80
-  __AUTH_CONST.__cfstring: 0x27080
+  __AUTH_CONST.__cfstring: 0x270a0
   __AUTH_CONST.__objc_const: 0x33638
   __AUTH_CONST.__objc_intobj: 0x2328
   __AUTH_CONST.__objc_dictobj: 0xb90
   __AUTH_CONST.__objc_arrayobj: 0x5d0
   __AUTH_CONST.__objc_doubleobj: 0x30
   __AUTH.__objc_data: 0x7918
   __AUTH.__data: 0x2b0
   __DATA.__objc_ivar: 0x255c
   __DATA.__data: 0x4178
-  __DATA.__bss: 0x1330
+  __DATA.__bss: 0x1340
   __DATA.__common: 0x18
   __DATA_DIRTY.__objc_data: 0x1158
   __DATA_DIRTY.__common: 0xf8
   __DATA_DIRTY.__bss: 0x190
   - /System/Library/Frameworks/AudioToolbox.framework/AudioToolbox

   - /usr/lib/libMobileGestalt.dylib
   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: 48240B46-2E2A-332B-9ADC-DF6123EB6CD7
+  UUID: 7A44BD8F-2535-3644-9869-340513E68BB9
-  Functions: 11758
+  Functions: 11759
-  Symbols:   37463
+  Symbols:   37468
-  CStrings:  24143
+  CStrings:  24147
 
Symbols:
+ GCC_except_table11507
+ GCC_except_table11652
+ GCC_except_table11671
+ GCC_except_table11674
+ GCC_except_table11676
+ _AFIsLocaleSupportedForSirClassic.once
+ _AFIsLocaleSupportedForSirClassic.supportedSiriClassicLocales
+ ___AFIsLocaleSupportedForSirClassic_block_invoke
+ ___Block_byref_object_copy_.47686
+ ___Block_byref_object_copy_.48414
+ ___Block_byref_object_copy_.48696
+ ___Block_byref_object_dispose_.47687
+ ___Block_byref_object_dispose_.48415
+ ___Block_byref_object_dispose_.48697
+ ___block_literal_global.1089
+ ___block_literal_global.22.47192
+ ___block_literal_global.25.47186
+ ___block_literal_global.46852
+ ___block_literal_global.46878
+ ___block_literal_global.47.48709
+ ___block_literal_global.47032
+ ___block_literal_global.47180
+ ___block_literal_global.47706
+ ___block_literal_global.48370
+ ___block_literal_global.48717
+ ___block_literal_global.5.48702
+ _sharedObserver.onceToken.48716
+ _sharedObserver.sharedObserver.48718
- GCC_except_table11506
- GCC_except_table11651
- GCC_except_table11670
- GCC_except_table11673
- GCC_except_table11675
- ___Block_byref_object_copy_.47681
- ___Block_byref_object_copy_.48409
- ___Block_byref_object_copy_.48691
- ___Block_byref_object_dispose_.47682
- ___Block_byref_object_dispose_.48410
- ___Block_byref_object_dispose_.48692
- ___block_literal_global.22.47187
- ___block_literal_global.25.47181
- ___block_literal_global.46847
- ___block_literal_global.46873
- ___block_literal_global.47.48704
- ___block_literal_global.47027
- ___block_literal_global.47175
- ___block_literal_global.47701
- ___block_literal_global.48365
- ___block_literal_global.48712
- ___block_literal_global.5.48697
- _sharedObserver.onceToken.48711
- _sharedObserver.sharedObserver.48713
CStrings:
+ "%s AFDeviceSupportsDisablingServerFallbackWhenMissingAsset returns true as locale is nil"
+ "%s AFDeviceSupportsDisablingServerFallbackWhenMissingAsset returns true for unsupported server locale: %@"
+ "hi_IN"

```

#### DiskImages2

>  `/System/Library/PrivateFrameworks/DiskImages2.framework/DiskImages2`

```diff

 385.100.33.0.0
   __TEXT.__text: 0x172460
   __TEXT.__auth_stubs: 0x1ee0
   __TEXT.__objc_methlist: 0x2f34
   __TEXT.__const: 0xe4b4
   __TEXT.__gcc_except_tab: 0x142b8
   __TEXT.__cstring: 0xee18
   __TEXT.__oslogstring: 0x136d
   __TEXT.__ustring: 0x13c
   __TEXT.__constg_swiftt: 0x60
   __TEXT.__swift5_typeref: 0x4f
   __TEXT.__swift5_fieldmd: 0x10
   __TEXT.__swift5_types: 0x4
   __TEXT.__unwind_info: 0xac80

   __TEXT.__objc_classname: 0x597
   __TEXT.__objc_methname: 0x61e6
   __TEXT.__objc_methtype: 0x1da4
   __TEXT.__objc_stubs: 0x5260
   __DATA_CONST.__got: 0x540
   __DATA_CONST.__const: 0xd00
   __DATA_CONST.__objc_classlist: 0x210

   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
   - /usr/local/lib/libcurl.4.dylib
-  UUID: D19CFCBD-08B8-3FB6-A917-943777464799
+  UUID: CEFA07D6-E4A4-3D66-AC89-A909A1438A57
   Functions: 8840
   Symbols:   25540
   CStrings:  3706
CStrings:
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/algorithm/hex.hpp"
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/uuid/detail/sha1.hpp"
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/uuid/string_generator.hpp"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/algorithm/hex.hpp"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/uuid/detail/sha1.hpp"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/boost/uuid/string_generator.hpp"

```

#### SiriSharedUI

>  `/System/Library/PrivateFrameworks/SiriSharedUI.framework/SiriSharedUI`

```diff

-3404.71.4.11.4
+3404.71.4.11.5
   __TEXT.__text: 0xc0d5c
   __TEXT.__auth_stubs: 0x2b50
   __TEXT.__objc_methlist: 0x6064
   __TEXT.__const: 0x3454
   __TEXT.__cstring: 0x78cc
   __TEXT.__oslogstring: 0x11c8
   __TEXT.__gcc_except_tab: 0x32c
   __TEXT.__ustring: 0x1a
   __TEXT.__dlopen_cstrs: 0x58
   __TEXT.__swift5_typeref: 0x711c
   __TEXT.__swift5_fieldmd: 0x1218
   __TEXT.__constg_swiftt: 0x2598
   __TEXT.__swift5_reflstr: 0x1816
   __TEXT.__swift5_builtin: 0xa0
   __TEXT.__swift5_capture: 0xc94

   __TEXT.__objc_methtype: 0x2c25
   __TEXT.__objc_stubs: 0x8520
   __DATA_CONST.__got: 0xf60
   __DATA_CONST.__const: 0xa68
   __DATA_CONST.__objc_classlist: 0x2f0
   __DATA_CONST.__objc_catlist: 0x18
   __DATA_CONST.__objc_protolist: 0x240
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_selrefs: 0x38a0
   __DATA_CONST.__objc_protorefs: 0xb0
   __DATA_CONST.__objc_superrefs: 0x138
   __DATA_CONST.__objc_arraydata: 0x70
   __AUTH_CONST.__auth_got: 0x15b8
-  __AUTH_CONST.__auth_ptr: 0xb50
+  __AUTH_CONST.__auth_ptr: 0xba0
   __AUTH_CONST.__const: 0x2d80
   __AUTH_CONST.__cfstring: 0xc40
   __AUTH_CONST.__objc_const: 0xac70
   __AUTH_CONST.__objc_arrayobj: 0x60
   __AUTH_CONST.__objc_intobj: 0xd8
   __AUTH_CONST.__objc_doubleobj: 0xc0
   __AUTH.__objc_data: 0x10c8
   __AUTH.__data: 0xd58
   __DATA.__objc_ivar: 0x5d8
   __DATA.__data: 0x2a38
   __DATA.__bss: 0x1e90
   __DATA.__common: 0xc0
   __DATA_DIRTY.__objc_data: 0x2380
   __DATA_DIRTY.__data: 0x1700
   __DATA_DIRTY.__bss: 0x7a0
   __DATA_DIRTY.__common: 0x130
   - /System/Library/Frameworks/Combine.framework/Combine

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 0518C4AB-6502-391C-8F1F-958821523A5D
+  UUID: 54135550-78AC-3E12-9A19-C34400487112
   Functions: 4333
   Symbols:   6797
   CStrings:  3745

```

#### UserNotificationsKit

>  `/System/Library/PrivateFrameworks/UserNotificationsKit.framework/UserNotificationsKit`

```diff

-941.5.3.106.0
+941.5.3.107.0
   __TEXT.__text: 0x58c38
   __TEXT.__auth_stubs: 0x1bb0
   __TEXT.__objc_methlist: 0x2c0c
   __TEXT.__const: 0x2114
   __TEXT.__cstring: 0x3374
   __TEXT.__gcc_except_tab: 0x1b4
   __TEXT.__oslogstring: 0x2adc
   __TEXT.__constg_swiftt: 0xc70
   __TEXT.__swift5_typeref: 0x3c38
   __TEXT.__swift5_reflstr: 0x675
   __TEXT.__swift5_fieldmd: 0x8b0
   __TEXT.__swift5_builtin: 0x64

   __TEXT.__objc_classname: 0x57e
   __TEXT.__objc_methname: 0x8e28
   __TEXT.__objc_methtype: 0x1072
   __TEXT.__objc_stubs: 0x43c0
   __DATA_CONST.__got: 0x6e8
   __DATA_CONST.__const: 0x4b0
   __DATA_CONST.__objc_classlist: 0x148
   __DATA_CONST.__objc_catlist: 0x18
   __DATA_CONST.__objc_protolist: 0xb8
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_selrefs: 0x1c80
   __DATA_CONST.__objc_protorefs: 0x38
   __DATA_CONST.__objc_superrefs: 0x98
   __AUTH_CONST.__auth_got: 0xde8
-  __AUTH_CONST.__auth_ptr: 0x5c0
+  __AUTH_CONST.__auth_ptr: 0x5c8
   __AUTH_CONST.__const: 0x1a20
   __AUTH_CONST.__cfstring: 0x18e0
   __AUTH_CONST.__objc_const: 0x53d0
   __AUTH.__objc_data: 0x430
   __AUTH.__data: 0xc48
   __DATA.__objc_ivar: 0x2d4
   __DATA.__data: 0x15d8
   __DATA.__bss: 0x2c50
   __DATA.__common: 0x160
   __DATA_DIRTY.__objc_data: 0x8e8
   __DATA_DIRTY.__data: 0x28
   __DATA_DIRTY.__bss: 0x18
   __DATA_DIRTY.__common: 0x50
   - /System/Library/Frameworks/Combine.framework/Combine

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: FFFB4C90-D276-38D8-BF19-DAD108485AC4
+  UUID: 22DDE2EB-E49F-3904-AA8A-C266810462D9
   Functions: 2007
   Symbols:   3623
   CStrings:  2330

```

#### UserNotificationsUIKit

>  `/System/Library/PrivateFrameworks/UserNotificationsUIKit.framework/UserNotificationsUIKit`

```diff

-941.5.3.106.0
+941.5.3.107.0
   __TEXT.__text: 0x19c080
   __TEXT.__auth_stubs: 0x24f0
   __TEXT.__objc_methlist: 0x196a4
   __TEXT.__const: 0x3644
   __TEXT.__gcc_except_tab: 0x2d58
   __TEXT.__cstring: 0xc386
   __TEXT.__oslogstring: 0xc310
   __TEXT.__ustring: 0x22
   __TEXT.__swift5_typeref: 0x3de8
   __TEXT.__swift5_fieldmd: 0x1274
   __TEXT.__constg_swiftt: 0x1d8c
   __TEXT.__swift5_reflstr: 0x138e
   __TEXT.__swift5_builtin: 0x104
   __TEXT.__swift5_assocty: 0x1f8

   __TEXT.__unwind_info: 0x6c08
   __TEXT.__eh_frame: 0xdb0
   __TEXT.__objc_classname: 0x370b
   __TEXT.__objc_methname: 0x44afc
   __TEXT.__objc_methtype: 0xbf6f
   __TEXT.__objc_stubs: 0x27b00
   __DATA_CONST.__got: 0x1728
   __DATA_CONST.__const: 0x4098
   __DATA_CONST.__objc_classlist: 0x7b0
   __DATA_CONST.__objc_catlist: 0xb8
   __DATA_CONST.__objc_protolist: 0x5e8
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_selrefs: 0xc330
   __DATA_CONST.__objc_protorefs: 0xc8
   __DATA_CONST.__objc_superrefs: 0x550
   __DATA_CONST.__objc_arraydata: 0x158
   __AUTH_CONST.__auth_got: 0x1288
-  __AUTH_CONST.__auth_ptr: 0x798
+  __AUTH_CONST.__auth_ptr: 0x740
   __AUTH_CONST.__const: 0x5168
   __AUTH_CONST.__cfstring: 0x7d00
   __AUTH_CONST.__objc_const: 0x24738
   __AUTH_CONST.__objc_intobj: 0x360
   __AUTH_CONST.__objc_arrayobj: 0x150
   __AUTH_CONST.__objc_dictobj: 0x28
   __AUTH_CONST.__objc_doubleobj: 0x20
   __AUTH.__objc_data: 0x2590
   __AUTH.__data: 0x728
   __DATA.__objc_ivar: 0x1628
   __DATA.__data: 0x50f0
   __DATA.__objc_stublist: 0x8
   __DATA.__bss: 0x1a50
   __DATA.__common: 0x48
   __DATA_DIRTY.__objc_data: 0x3810
   __DATA_DIRTY.__data: 0x11b0
   __DATA_DIRTY.__bss: 0xc00
   __DATA_DIRTY.__common: 0x68
   - /System/Library/Frameworks/Charts.framework/Charts

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 09B6B9E6-5D3B-333D-8F5B-AAAEE7097E14
+  UUID: 35AC9B08-DF40-3BBF-A3BE-A8191120E92D
   Functions: 10255
   Symbols:   27781
   CStrings:  13314
Symbols:
+ _objc_msgSend$addAttributes:range:
- _objc_msgSend$setAttributes:range:
CStrings:
+ "addAttributes:range:"
- "setAttributes:range:"

```

#### WatchListKit

>  `/System/Library/PrivateFrameworks/WatchListKit.framework/WatchListKit`

```diff

-850.40.40.0.0
+850.41.1.0.0
-  __TEXT.__text: 0x65a34
+  __TEXT.__text: 0x65a0c
   __TEXT.__auth_stubs: 0x850
   __TEXT.__objc_methlist: 0x6e94
   __TEXT.__const: 0x1ac
   __TEXT.__cstring: 0x7986
   __TEXT.__oslogstring: 0x6031
   __TEXT.__gcc_except_tab: 0x1210
   __TEXT.__dlopen_cstrs: 0x5a
   __TEXT.__unwind_info: 0x1e30
   __TEXT.__objc_classname: 0x1320
   __TEXT.__objc_methname: 0xfde4
   __TEXT.__objc_methtype: 0x1c56
   __TEXT.__objc_stubs: 0x9b60
   __DATA_CONST.__got: 0x8d8
   __DATA_CONST.__const: 0x2780
   __DATA_CONST.__objc_classlist: 0x560
   __DATA_CONST.__objc_catlist: 0x50
   __DATA_CONST.__objc_protolist: 0x98
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_selrefs: 0x3828
   __DATA_CONST.__objc_protorefs: 0x20
   __DATA_CONST.__objc_superrefs: 0x4b0
   __DATA_CONST.__objc_arraydata: 0x620
   __AUTH_CONST.__auth_got: 0x438
   __AUTH_CONST.__const: 0xe60
   __AUTH_CONST.__cfstring: 0xa100
   __AUTH_CONST.__objc_const: 0x11988
   __AUTH_CONST.__objc_intobj: 0x390
   __AUTH_CONST.__objc_dictobj: 0x190
   __AUTH_CONST.__objc_arrayobj: 0x78
   __AUTH.__objc_data: 0xf0
   __DATA.__objc_ivar: 0xa0c
   __DATA.__data: 0x7a0
   __DATA.__bss: 0x110
   __DATA_DIRTY.__objc_data: 0x34d0
   __DATA_DIRTY.__data: 0x8
   __DATA_DIRTY.__bss: 0x438
   __DATA_DIRTY.__common: 0x8

   - /usr/lib/libMobileGestalt.dylib
   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: 6D7309F5-E55C-35B1-8328-8249AF818FDC
+  UUID: 594CC431-7F49-3E95-90EA-9C1822C52506
   Functions: 2713
   Symbols:   9992
   CStrings:  6350

```

#### WiFiAnalytics

>  `/System/Library/PrivateFrameworks/WiFiAnalytics.framework/WiFiAnalytics`

```diff

 725.36.0.0.0
   __TEXT.__text: 0xf456c
   __TEXT.__auth_stubs: 0xf40
   __TEXT.__objc_methlist: 0xc574
   __TEXT.__const: 0x298
   __TEXT.__cstring: 0xe0d0
   __TEXT.__oslogstring: 0xabf0
   __TEXT.__swift5_typeref: 0xfb
   __TEXT.__constg_swiftt: 0x178
   __TEXT.__swift5_reflstr: 0x61
   __TEXT.__swift5_fieldmd: 0x70

   __TEXT.__objc_classname: 0xa6b
   __TEXT.__objc_methname: 0x1944a
   __TEXT.__objc_methtype: 0x34b7
   __TEXT.__objc_stubs: 0x9320
   __DATA_CONST.__got: 0x608
   __DATA_CONST.__const: 0x1b20
   __DATA_CONST.__objc_classlist: 0x2c0

   - /usr/lib/swift/libswiftos.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: E9D99B88-0A28-35AB-AC06-BE46FDF3E4B3
+  UUID: BDE56B90-8666-304D-9380-26C233EAAAEE
   Functions: 4685
   Symbols:   12529
   CStrings:  9658
CStrings:
+ "WiFiAnalytics-725.36 Apr  7 2025 19:00:04"
+ "WiFiAnalytics-725.36 Apr  7 2025 19:00:05"
- "WiFiAnalytics-725.36 Mar 17 2025 20:01:07"
- "WiFiAnalytics-725.36 Mar 17 2025 20:01:08"

```

#### WiFiCloudSyncEngine

>  `/System/Library/PrivateFrameworks/WiFiCloudSyncEngine.framework/WiFiCloudSyncEngine`

```diff

 752.13.0.0.0
   __TEXT.__text: 0x11328
   __TEXT.__auth_stubs: 0x4b0
   __TEXT.__objc_methlist: 0x1dc
   __TEXT.__const: 0x30
   __TEXT.__oslogstring: 0x24ec
   __TEXT.__cstring: 0x14f1
   __TEXT.__unwind_info: 0x1e0
   __TEXT.__objc_classname: 0x33
   __TEXT.__objc_methname: 0x8ce
   __TEXT.__objc_methtype: 0xfe
   __TEXT.__objc_stubs: 0xba0
   __DATA_CONST.__got: 0xe8
   __DATA_CONST.__const: 0x158
   __DATA_CONST.__objc_classlist: 0x10

   - /System/Library/Frameworks/Security.framework/Security
   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: 51847EF7-1451-332E-8C6D-97DD2007E713
+  UUID: DCA87AA7-4810-334C-9447-D76CDBF1AC38
   Functions: 259
   Symbols:   734
   CStrings:  558
CStrings:
+ "18:44:19"
+ "Apr  7 2025"
- "19:46:08"
- "Mar 17 2025"

```

#### WiFiKitUI

>  `/System/Library/PrivateFrameworks/WiFiKitUI.framework/WiFiKitUI`

```diff

 1100.42.4.1.0
   __TEXT.__text: 0x915f4
   __TEXT.__auth_stubs: 0x1910
   __TEXT.__objc_methlist: 0x68c8
   __TEXT.__const: 0x25e4
   __TEXT.__oslogstring: 0x331d
   __TEXT.__cstring: 0x88f8
   __TEXT.__gcc_except_tab: 0x1080
   __TEXT.__swift5_typeref: 0x5062
   __TEXT.__swift5_reflstr: 0x90a
   __TEXT.__swift5_assocty: 0x218
   __TEXT.__constg_swiftt: 0xf28
   __TEXT.__swift5_fieldmd: 0x5e4
   __TEXT.__swift5_builtin: 0xb4
   __TEXT.__swift5_capture: 0x70c

   __TEXT.__objc_classname: 0x996
   __TEXT.__objc_methname: 0x105c1
   __TEXT.__objc_methtype: 0x21e5
   __TEXT.__objc_stubs: 0xa640
   __DATA_CONST.__got: 0x918
   __DATA_CONST.__const: 0x11c0
   __DATA_CONST.__objc_classlist: 0x240
   __DATA_CONST.__objc_catlist: 0x40
   __DATA_CONST.__objc_protolist: 0xf0
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_selrefs: 0x3cb0
   __DATA_CONST.__objc_protorefs: 0x30
   __DATA_CONST.__objc_superrefs: 0x198
   __DATA_CONST.__objc_arraydata: 0x150
   __AUTH_CONST.__auth_got: 0xc98
-  __AUTH_CONST.__auth_ptr: 0x708
+  __AUTH_CONST.__auth_ptr: 0x750
   __AUTH_CONST.__const: 0x1c40
   __AUTH_CONST.__cfstring: 0x67e0
   __AUTH_CONST.__objc_const: 0x13330
   __AUTH_CONST.__objc_intobj: 0x6a8
   __AUTH_CONST.__objc_arrayobj: 0x228
   __AUTH_CONST.__objc_doubleobj: 0x10
   __AUTH.__objc_data: 0x2270
   __AUTH.__data: 0x2c8
   __DATA.__objc_ivar: 0x7ac
   __DATA.__data: 0x1748
   __DATA.__bss: 0x1970
   __DATA.__common: 0xe0
   __DATA_DIRTY.__objc_data: 0x188
   __DATA_DIRTY.__data: 0x28
   - /System/Library/Frameworks/AccessorySetupKit.framework/AccessorySetupKit
   - /System/Library/Frameworks/Combine.framework/Combine
   - /System/Library/Frameworks/CoreFoundation.framework/CoreFoundation

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 892DD915-2B63-3B67-A1F5-36120AB4AA73
+  UUID: 4F1F2DE9-065B-30DA-AD99-6EE249CD6E94
   Functions: 3349
   Symbols:   7751
   CStrings:  5431

```

#### libBBUpdaterDynamic.dylib

>  `/usr/lib/libBBUpdaterDynamic.dylib`

```diff

 1249.1.0.0.0
   __TEXT.__text: 0x112de8
   __TEXT.__auth_stubs: 0x33f0
   __TEXT.__init_offsets: 0x118
   __TEXT.__const: 0x65b5
   __TEXT.__cstring: 0x205b7
   __TEXT.__oslogstring: 0x4bc
   __TEXT.__gcc_except_tab: 0xf35c
   __TEXT.__unwind_info: 0x3c48
   __TEXT.__objc_classname: 0x1
   __TEXT.__objc_methname: 0x8c
   __TEXT.__objc_stubs: 0x120
   __DATA_CONST.__got: 0x258
   __DATA_CONST.__const: 0x1018
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_selrefs: 0x48
   __AUTH_CONST.__auth_got: 0x1a10
   __AUTH_CONST.__auth_ptr: 0x28
   __AUTH_CONST.__const: 0x6f30
   __AUTH_CONST.__cfstring: 0x3240
   __DATA.__data: 0x788
   __DATA.__bss: 0x5e0

   - /usr/lib/libc++.1.dylib
   - /usr/lib/libobjc.A.dylib
   - /usr/lib/libz.1.dylib
-  UUID: A00A97C3-2A3C-3BF5-9531-1203CE9D7F84
+  UUID: 8BC88B9B-7B36-3B6C-A49E-D2FDB93C7FD2
   Functions: 2646
   Symbols:   8911
   CStrings:  4141
CStrings:
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/ARI/ari_sdk_msg.h"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/ARI/ari_sdk_msg.h"

```

#### libHSFilerDynamic.dylib

>  `/usr/lib/libHSFilerDynamic.dylib`

```diff

 1249.1.0.0.0
   __TEXT.__text: 0x2e8a0
   __TEXT.__auth_stubs: 0xbe0
   __TEXT.__init_offsets: 0x38
   __TEXT.__const: 0x218f
   __TEXT.__gcc_except_tab: 0x25d8
   __TEXT.__cstring: 0xc79
   __TEXT.__oslogstring: 0x2349
   __TEXT.__unwind_info: 0x1018
   __DATA_CONST.__got: 0x120
   __DATA_CONST.__const: 0x610
   __AUTH_CONST.__auth_got: 0x5f8
   __AUTH_CONST.__const: 0x2028
   __DATA.__data: 0x1d0
   __DATA.__common: 0x78
   __DATA.__bss: 0x48

   - /usr/lib/libTelephonyCapabilities.dylib
   - /usr/lib/libTelephonyUtilDynamic.dylib
   - /usr/lib/libc++.1.dylib
-  UUID: ED450DB2-33ED-36B5-87CA-C1445C829547
+  UUID: 4C6BF932-6959-3DE0-B6AB-4C7E7D7D1A63
   Functions: 733
   Symbols:   2111
   CStrings:  335
CStrings:
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/ARI/ari_sdk_msg.h"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/ARI/ari_sdk_msg.h"

```

#### libKTLDynamic.dylib

>  `/usr/lib/libKTLDynamic.dylib`

```diff

 1249.1.0.0.0
   __TEXT.__text: 0x21760
   __TEXT.__auth_stubs: 0x15b0
   __TEXT.__init_offsets: 0x8
   __TEXT.__const: 0x128
   __TEXT.__gcc_except_tab: 0x14d0
   __TEXT.__cstring: 0x2f52
   __TEXT.__unwind_info: 0xa78
   __DATA_CONST.__got: 0x40
   __DATA_CONST.__const: 0x160

   - /usr/lib/libTelephonyCapabilities.dylib
   - /usr/lib/libTelephonyUtilDynamic.dylib
   - /usr/lib/libc++.1.dylib
-  UUID: 3303D362-D9FB-3E55-92FC-6E7FA5D1B824
+  UUID: 2FA116AB-A668-3874-8A6F-2482AC1ED0A1
   Functions: 400
   Symbols:   1269
   CStrings:  385
CStrings:
+ "/AppleInternal/Library/BuildRoots/514d6383-11dc-11f0-9d32-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/ARI/ari_sdk_msg.h"
- "/AppleInternal/Library/BuildRoots/46a745fc-02fe-11f0-b780-c2c15871b32e/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.4.Internal.sdk/usr/local/include/ARI/ari_sdk_msg.h"

```


</details>

## EOF


