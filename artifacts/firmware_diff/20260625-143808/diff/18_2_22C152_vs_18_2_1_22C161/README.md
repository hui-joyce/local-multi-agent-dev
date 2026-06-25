# 18.2 (22C152) .vs 18.2.1 (22C161)

## IPSWs

- `iPhone17,1_18.2_22C152_Restore.ipsw`
- `iPhone17,1_18.2.1_22C161_Restore.ipsw`

## Kernel

### Version

| iOS | Version | Build | Date |
| :-- | :------ | :---- | :--- |
| 18.2 *(22C152)* | 24.2.0 | 11215.62.3~1 | Thu, 14Nov2024 22:55:26 PST |
| 18.2.1 *(22C161)* | 24.2.0 | 11215.62.3~1 | Thu, 14Nov2024 22:55:26 PST |

## MachO

### filesystem

#### ⬆️ Updated (7)

<details>
  <summary><i>View Updated</i></summary>


#### DiagnosticsReporter

>  `/Applications/DiagnosticsReporter.app/DiagnosticsReporter`

```diff

-727.60.31.0.0
+727.62.1.0.0
   __TEXT.__text: 0xe0f8
   __TEXT.__auth_stubs: 0xce0
   __TEXT.__objc_methlist: 0x180
   __TEXT.__cstring: 0xd03
   __TEXT.__swift5_typeref: 0x2f0
   __TEXT.__swift5_fieldmd: 0x2d0
   __TEXT.__const: 0x884
   __TEXT.__constg_swiftt: 0x4a4
   __TEXT.__swift5_protos: 0x8
   __TEXT.__objc_classname: 0x3c

   __TEXT.__eh_frame: 0x3f8
   __DATA_CONST.__auth_got: 0x670
   __DATA_CONST.__got: 0x110
-  __DATA_CONST.__auth_ptr: 0x210
+  __DATA_CONST.__auth_ptr: 0x1d0
   __DATA_CONST.__const: 0x5a0
   __DATA_CONST.__objc_classlist: 0x38
   __DATA_CONST.__objc_protolist: 0x38
   __DATA_CONST.__objc_imageinfo: 0x8

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 01A218A9-572E-3FF1-BBF6-80F2FBB5549C
+  UUID: 2004DF5B-CCA8-34BF-B2EE-03C7EB7CAE14
   Functions: 311
   Symbols:   330
   CStrings:  338

```

#### osanalyticshelper

>  `/System/Library/CoreServices/osanalyticshelper`

```diff

-727.60.31.0.0
+727.62.1.0.0
-  __TEXT.__text: 0x11c80
+  __TEXT.__text: 0x11cd8
-  __TEXT.__auth_stubs: 0xcc0
+  __TEXT.__auth_stubs: 0xcd0
   __TEXT.__objc_stubs: 0x2420
   __TEXT.__objc_methlist: 0x664
   __TEXT.__const: 0x1ba
   __TEXT.__oslogstring: 0x1b1c
   __TEXT.__cstring: 0x1c31
   __TEXT.__objc_classname: 0x14c
   __TEXT.__objc_methtype: 0x3c6
-  __TEXT.__gcc_except_tab: 0x794
+  __TEXT.__gcc_except_tab: 0x79c
   __TEXT.__objc_methname: 0x1e01
   __TEXT.__constg_swiftt: 0x94
   __TEXT.__swift5_typeref: 0x78
   __TEXT.__swift5_reflstr: 0xd
   __TEXT.__swift5_fieldmd: 0x28
   __TEXT.__swift5_capture: 0x34
   __TEXT.__swift5_types: 0x4
-  __TEXT.__info_plist: 0x3de
+  __TEXT.__info_plist: 0x3e4
   __TEXT.__unwind_info: 0x430
-  __DATA_CONST.__auth_got: 0x678
+  __DATA_CONST.__auth_got: 0x680
   __DATA_CONST.__got: 0x480
   __DATA_CONST.__auth_ptr: 0x40
   __DATA_CONST.__const: 0x8e0
   __DATA_CONST.__cfstring: 0x1820
   __DATA_CONST.__objc_classlist: 0x70
   __DATA_CONST.__objc_protolist: 0x18
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_superrefs: 0x50
   __DATA_CONST.__objc_intobj: 0x198
   __DATA_CONST.__objc_arraydata: 0x38
   __DATA_CONST.__objc_arrayobj: 0x18
   __DATA_CONST.__objc_dictobj: 0x50
   __DATA.__objc_const: 0x1170
   __DATA.__objc_selrefs: 0x988
   __DATA.__objc_ivar: 0x84
   __DATA.__objc_data: 0x520
   __DATA.__data: 0x1a8
   __DATA.__bss: 0xe8
   - /System/Library/Frameworks/CoreFoundation.framework/CoreFoundation
   - /System/Library/Frameworks/CoreServices.framework/CoreServices

   - /usr/lib/swift/libswiftos.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 28C21D92-0689-3F3F-A4AE-79E776141D43
+  UUID: 5D325F7D-CE7E-335B-B687-04500452B15A
   Functions: 272
-  Symbols:   379
+  Symbols:   380
   CStrings:  1088
 
Symbols:
+ _arc4random_uniform

```

#### TrustedPeersHelper

>  `/System/Library/Frameworks/Security.framework/XPCServices/TrustedPeersHelper.xpc/TrustedPeersHelper`

```diff

-61439.62.1.0.0
+61439.62.2.0.0
   __TEXT.__text: 0x21f38c
   __TEXT.__auth_stubs: 0x1e70
   __TEXT.__objc_stubs: 0x2860
   __TEXT.__objc_methlist: 0x2b34
   __TEXT.__const: 0x9608
   __TEXT.__cstring: 0x16315
   __TEXT.__objc_methname: 0x8204
   __TEXT.__oslogstring: 0xa081
   __TEXT.__swift5_entry: 0x8
   __TEXT.__constg_swiftt: 0x3474
   __TEXT.__swift5_typeref: 0x35c6
   __TEXT.__swift5_fieldmd: 0x2458
   __TEXT.__swift5_reflstr: 0x1e27
   __TEXT.__swift5_builtin: 0xb4

   __TEXT.__eh_frame: 0x7050
   __DATA_CONST.__auth_got: 0xf48
   __DATA_CONST.__got: 0x848
-  __DATA_CONST.__auth_ptr: 0x658
+  __DATA_CONST.__auth_ptr: 0x648
   __DATA_CONST.__const: 0xfb30
   __DATA_CONST.__cfstring: 0x1f20
   __DATA_CONST.__objc_classlist: 0x270
   __DATA_CONST.__objc_catlist: 0x20

   __DATA.__data: 0x7620
   __DATA.__objc_stublist: 0x90
   __DATA.__common: 0x8d0
   __DATA.__bss: 0x104f8
   - /System/Library/Frameworks/CloudKit.framework/CloudKit
   - /System/Library/Frameworks/CoreData.framework/CoreData
   - /System/Library/Frameworks/CoreFoundation.framework/CoreFoundation

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 55DB2A1D-A6A1-3C22-89B0-083B7DDEA735
+  UUID: 49E7189B-4F35-3041-A21A-A81A4DCF04D6
   Functions: 8123
   Symbols:   497
   CStrings:  3614

```

#### cdpd

>  `/System/Library/PrivateFrameworks/CoreCDP.framework/cdpd`

```diff

-386.231.0.0.0
+386.231.1.0.0
-  __TEXT.__text: 0x24c
+  __TEXT.__text: 0x214
-  __TEXT.__auth_stubs: 0xe0
+  __TEXT.__auth_stubs: 0xd0
   __TEXT.__objc_stubs: 0xe0
   __TEXT.__const: 0x30
   __TEXT.__oslogstring: 0xd
   __TEXT.__info_plist: 0x593
   __TEXT.__objc_methname: 0x5e
   __TEXT.__unwind_info: 0x60
-  __DATA_CONST.__auth_got: 0x78
+  __DATA_CONST.__auth_got: 0x70
-  __DATA_CONST.__got: 0x50
+  __DATA_CONST.__got: 0x48
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA.__objc_selrefs: 0x38
   - /System/Library/Frameworks/CoreFoundation.framework/CoreFoundation

   - /System/Library/PrivateFrameworks/CoreCDPInternal.framework/CoreCDPInternal
   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: 6C1C13B3-63F9-3E84-8118-E002420C8A24
+  UUID: 0852048F-712F-33DD-B876-D3E494C0BB3C
   Functions: 2
-  Symbols:   27
+  Symbols:   25
   CStrings:  8
 
Symbols:
- _OBJC_CLASS_$_CDPDUnlockObserver
- _objc_release_x23

```

#### imagent

>  `/System/Library/PrivateFrameworks/IMCore.framework/imagent.app/imagent`

```diff

-1402.300.181.2.20
+1402.300.181.2.21
   __TEXT.__text: 0x47424
   __TEXT.__auth_stubs: 0x1550
   __TEXT.__objc_stubs: 0x5800
   __TEXT.__objc_methlist: 0x1680
   __TEXT.__const: 0x1024
   __TEXT.__gcc_except_tab: 0x3bd8
   __TEXT.__cstring: 0x1bbc
   __TEXT.__oslogstring: 0x590b
   __TEXT.__objc_methname: 0x99b2
   __TEXT.__objc_classname: 0x598
   __TEXT.__objc_methtype: 0x2228
   __TEXT.__swift5_typeref: 0x42c
   __TEXT.__swift5_fieldmd: 0x2b0
   __TEXT.__constg_swiftt: 0x4c0
   __TEXT.__swift5_protos: 0x10
   __TEXT.__swift5_capture: 0x130
   __TEXT.__swift5_proto: 0xac

   __TEXT.__eh_frame: 0x500
   __DATA_CONST.__auth_got: 0xab8
   __DATA_CONST.__got: 0x8d8
-  __DATA_CONST.__auth_ptr: 0x2d0
+  __DATA_CONST.__auth_ptr: 0x2d8
   __DATA_CONST.__const: 0x12e0
   __DATA_CONST.__cfstring: 0x7c0
   __DATA_CONST.__objc_classlist: 0x100
   __DATA_CONST.__objc_protolist: 0x198
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_protorefs: 0xc8
   __DATA_CONST.__objc_superrefs: 0x18
   __DATA_CONST.__objc_arraydata: 0x10
   __DATA_CONST.__objc_dictobj: 0x28
   __DATA.__objc_const: 0x5348
   __DATA.__objc_selrefs: 0x21a8
   __DATA.__objc_ivar: 0x44
   __DATA.__objc_data: 0xaf8
   __DATA.__data: 0x1200
   __DATA.__common: 0xe0
   __DATA.__bss: 0xf70

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 444669B1-6C34-329E-8F40-E201F9DD0117
+  UUID: B151D8C4-0CA1-3FE8-B673-ECDA55332EDF
   Functions: 966
   Symbols:   527
   CStrings:  2219
CStrings:
+ "16:36:36"
+ "Dec 18 2024"
- "19:20:06"
- "Dec  6 2024"

```

#### securityd

>  `/usr/libexec/securityd`

```diff

-61439.62.1.0.0
+61439.62.2.0.0
-  __TEXT.__text: 0x23075c
+  __TEXT.__text: 0x230754
   __TEXT.__auth_stubs: 0x38c0
   __TEXT.__objc_stubs: 0x1a4c0
   __TEXT.__objc_methlist: 0x128e4
   __TEXT.__const: 0x8cd
   __TEXT.__cstring: 0x1f937
   __TEXT.__oslogstring: 0x29037
   __TEXT.__gcc_except_tab: 0xacb0
   __TEXT.__objc_classname: 0x2284
   __TEXT.__objc_methname: 0x292ad
   __TEXT.__objc_methtype: 0x99e2
   __TEXT.__dlopen_cstrs: 0x1c8
   __TEXT.__ustring: 0x28
   __TEXT.__unwind_info: 0x6218
   __DATA_CONST.__auth_got: 0x1c70
   __DATA_CONST.__got: 0x1040
   __DATA_CONST.__auth_ptr: 0x20
   __DATA_CONST.__const: 0x13080
   __DATA_CONST.__cfstring: 0x1a5a0
   __DATA_CONST.__objc_classlist: 0x870
   __DATA_CONST.__objc_catlist: 0x68

   __DATA.__objc_selrefs: 0x8758
   __DATA.__objc_ivar: 0x185c
   __DATA.__objc_data: 0x5460
   __DATA.__data: 0x20b8
   __DATA.__thread_vars: 0xd8
   __DATA.__thread_bss: 0x1e
   __DATA.__bss: 0x9d0

   - /usr/lib/libprequelite.dylib
   - /usr/lib/libsqlite3.dylib
   - /usr/lib/libz.1.dylib
-  UUID: 84302102-8AA9-3089-A8CA-69709C8707AA
+  UUID: 9BCCBC0C-D0AD-39C6-A544-0596BECC5D1A
   Functions: 9066
   Symbols:   1451
   CStrings:  18462

```

#### securityuploadd

>  `/usr/libexec/securityuploadd`

```diff

-61439.62.1.0.0
+61439.62.2.0.0
   __TEXT.__text: 0xcb10
   __TEXT.__auth_stubs: 0x780
   __TEXT.__objc_stubs: 0x1be0
   __TEXT.__objc_methlist: 0x664
   __TEXT.__const: 0xc8
   __TEXT.__gcc_except_tab: 0x328
   __TEXT.__cstring: 0xf12
   __TEXT.__oslogstring: 0xe49
   __TEXT.__objc_classname: 0xd7
   __TEXT.__objc_methname: 0x1eaa

   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libobjc.A.dylib
   - /usr/lib/libz.1.dylib
-  UUID: 51AE907F-BA14-3385-9B24-51E848B60C43
+  UUID: DC18DBF1-6CAF-3357-BC6D-746753D36B01
   Functions: 189
   Symbols:   204
   CStrings:  878
CStrings:
+ "61439.62.2"
- "61439.62.1"

```


</details>

### iBoot

| iOS | Version |
| :-- | :------ |
| 18.2 *(22C152)* | iBoot-11881.62.2 |
| 18.2.1 *(22C161)* | iBoot-11881.62.2 |

## DSC

### WebKit

| iOS | Version |
| :-- | :------ |
| 18.2 *(22C152)* | 620.1.16.10.11 |
| 18.2.1 *(22C161)* | 620.1.16.10.11 |

### Dylibs

#### ⬆️ Updated (9)

<details>
  <summary><i>View Updated</i></summary>



#### QuickLook

>  `/System/Library/Frameworks/QuickLook.framework/QuickLook`

```diff

-969.3.4.0.0
+969.3.5.0.0
   __TEXT.__text: 0xd31c8
   __TEXT.__auth_stubs: 0x2420
   __TEXT.__delay_stubs: 0x2c
   __TEXT.__delay_helper: 0x7a8
   __TEXT.__objc_methlist: 0x8f38
   __TEXT.__const: 0x2354
   __TEXT.__gcc_except_tab: 0x1b30
   __TEXT.__oslogstring: 0x589f
   __TEXT.__cstring: 0x5ec8
   __TEXT.__ustring: 0x1c
   __TEXT.__swift5_typeref: 0x18d2
   __TEXT.__swift5_reflstr: 0x6b7
   __TEXT.__swift5_assocty: 0x258
   __TEXT.__constg_swiftt: 0x1558
   __TEXT.__swift5_fieldmd: 0x924
   __TEXT.__swift5_builtin: 0xf0
   __TEXT.__swift5_proto: 0x10c

   __TEXT.__swift5_capture: 0xe38
   __TEXT.__swift5_protos: 0x18
   __TEXT.__swift5_mpenum: 0x8
   __TEXT.__unwind_info: 0x4a40
   __TEXT.__eh_frame: 0x4534
   __TEXT.__objc_classname: 0x177f
   __TEXT.__objc_methname: 0x1ef27
   __TEXT.__objc_methtype: 0x6a7f
   __TEXT.__objc_stubs: 0x14f80
   __DATA_CONST.__got: 0xef8
   __DATA_CONST.__const: 0x2958
   __DATA_CONST.__objc_classlist: 0x468
   __DATA_CONST.__objc_catlist: 0x70
   __DATA_CONST.__objc_protolist: 0x388
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_selrefs: 0x63c0
   __DATA_CONST.__objc_protorefs: 0x158
   __DATA_CONST.__objc_superrefs: 0x288
   __DATA_CONST.__objc_arraydata: 0x98
   __AUTH_CONST.__auth_got: 0x1228
-  __AUTH_CONST.__auth_ptr: 0x640
+  __AUTH_CONST.__auth_ptr: 0x600
   __AUTH_CONST.__const: 0x3048
   __AUTH_CONST.__cfstring: 0x2f80
   __AUTH_CONST.__objc_const: 0x15420
   __AUTH_CONST.__objc_intobj: 0x228
   __AUTH_CONST.__objc_dictobj: 0x28
   __AUTH_CONST.__objc_arrayobj: 0x60
   __AUTH_CONST.__objc_doubleobj: 0x10
   __AUTH.__objc_data: 0x2c08
   __AUTH.__data: 0x1370
   __DATA.__objc_ivar: 0xbac
   __DATA.__data: 0x3810
   __DATA.__bss: 0x23c8
   __DATA.__common: 0x68
   __DATA_DIRTY.__objc_data: 0x460
   - /System/Library/Frameworks/AVFAudio.framework/AVFAudio
   - /System/Library/Frameworks/AVFoundation.framework/AVFoundation
   - /System/Library/Frameworks/AVKit.framework/AVKit

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 299ED81C-DA28-3B16-A48A-EF61803FBF63
+  UUID: 6AEA76C8-2294-30AA-AA6A-24830BB6A80C
   Functions: 5462
   Symbols:   13856
   CStrings:  6995

```

#### ChatKit

>  `/System/Library/PrivateFrameworks/ChatKit.framework/ChatKit`

```diff

-1402.300.181.2.20
+1402.300.181.2.21
-  __TEXT.__text: 0x8977e8
+  __TEXT.__text: 0x897694
   __TEXT.__auth_stubs: 0x8b80
   __TEXT.__delay_helper: 0x190
   __TEXT.__objc_methlist: 0x5c760
   __TEXT.__const: 0x1b674
-  __TEXT.__gcc_except_tab: 0x26184
+  __TEXT.__gcc_except_tab: 0x2613c
   __TEXT.__cstring: 0x41909
   __TEXT.__oslogstring: 0x3d96b
   __TEXT.__dlopen_cstrs: 0xa79
   __TEXT.__ustring: 0x17c
   __TEXT.__swift5_typeref: 0x270fc
   __TEXT.__swift5_capture: 0x3820
   __TEXT.__constg_swiftt: 0xf5c4
   __TEXT.__swift5_builtin: 0x5f0
   __TEXT.__swift5_reflstr: 0x8da6
   __TEXT.__swift5_fieldmd: 0x7ed4
   __TEXT.__swift5_assocty: 0x2390
   __TEXT.__swift5_proto: 0xc88
   __TEXT.__swift5_types: 0x9c8
   __TEXT.__swift5_protos: 0x80
   __TEXT.__swift5_mpenum: 0x18
-  __TEXT.__unwind_info: 0x24728
+  __TEXT.__unwind_info: 0x24720
   __TEXT.__eh_frame: 0x62f0
   __TEXT.__objc_classname: 0xb197
   __TEXT.__objc_methname: 0xfa3d5
   __TEXT.__objc_methtype: 0x21dfa
   __TEXT.__objc_stubs: 0x9b8a0
   __DATA_CONST.__got: 0x5f08
   __DATA_CONST.__const: 0xd9a0
   __DATA_CONST.__objc_classlist: 0x2778
   __DATA_CONST.__objc_catlist: 0x500
   __DATA_CONST.__objc_protolist: 0x1198
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_selrefs: 0x30320
   __DATA_CONST.__objc_protorefs: 0x390
   __DATA_CONST.__objc_superrefs: 0x19a0
   __DATA_CONST.__objc_arraydata: 0x1040
   __AUTH_CONST.__auth_got: 0x45d0
-  __AUTH_CONST.__auth_ptr: 0x33d8
+  __AUTH_CONST.__auth_ptr: 0x3380
   __AUTH_CONST.__const: 0x264f0
   __AUTH_CONST.__cfstring: 0x24300
   __AUTH_CONST.__objc_const: 0xa43c8
   __AUTH_CONST.__objc_arrayobj: 0xea0
   __AUTH_CONST.__objc_intobj: 0x1068
   __AUTH_CONST.__objc_doubleobj: 0x8e0
   __AUTH_CONST.__objc_floatobj: 0x180
   __AUTH_CONST.__objc_dictobj: 0x2f8
   __AUTH.__objc_data: 0x1b9c8
   __AUTH.__data: 0x8928
   __DATA.__objc_ivar: 0x489c
   __DATA.__data: 0x17b60
   __DATA.__objc_stublist: 0x10
   __DATA.__bss: 0x224c8
   __DATA.__common: 0x9c8
   __DATA_DIRTY.__objc_data: 0xa510
   __DATA_DIRTY.__data: 0x680
   __DATA_DIRTY.__bss: 0x1978
   __DATA_DIRTY.__common: 0x50
   - /System/Library/Frameworks/AVFAudio.framework/AVFAudio

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 729639FD-827F-3909-BD29-5DE9E25780ED
+  UUID: 508DA8C8-9BB8-34AB-BC87-D39BA7B34DF3
-  Functions: 53368
+  Functions: 53367
-  Symbols:   128702
+  Symbols:   128700
   CStrings:  55448
 
Symbols:
- ___73-[CKMovieMediaObject generateThumbnailFillToSize:contentAlignmentInsets:]_block_invoke

```

#### CoreCDPInternal

>  `/System/Library/PrivateFrameworks/CoreCDPInternal.framework/CoreCDPInternal`

```diff

-386.231.0.0.0
+386.231.1.0.0
-  __TEXT.__text: 0x8ec04
+  __TEXT.__text: 0x8dacc
-  __TEXT.__auth_stubs: 0x11d0
+  __TEXT.__auth_stubs: 0x1130
-  __TEXT.__objc_methlist: 0x44cc
+  __TEXT.__objc_methlist: 0x4474
-  __TEXT.__const: 0x730
+  __TEXT.__const: 0x720
-  __TEXT.__oslogstring: 0x13768
+  __TEXT.__oslogstring: 0x13538
-  __TEXT.__cstring: 0x7705
+  __TEXT.__cstring: 0x7675
   __TEXT.__gcc_except_tab: 0xbac
   __TEXT.__dlopen_cstrs: 0xb0
   __TEXT.__swift5_typeref: 0x301
   __TEXT.__swift5_fieldmd: 0x8c
   __TEXT.__constg_swiftt: 0x1b0
   __TEXT.__swift5_builtin: 0x64
   __TEXT.__swift5_reflstr: 0x79
   __TEXT.__swift5_assocty: 0x90
   __TEXT.__swift5_protos: 0x4
   __TEXT.__swift5_proto: 0x40
   __TEXT.__swift5_types: 0x20
   __TEXT.__swift5_capture: 0x1b8
-  __TEXT.__unwind_info: 0x1cb8
+  __TEXT.__unwind_info: 0x1c90
   __TEXT.__eh_frame: 0x8e0
-  __TEXT.__objc_classname: 0xc8c
+  __TEXT.__objc_classname: 0xc79
-  __TEXT.__objc_methname: 0xeb7e
+  __TEXT.__objc_methname: 0xeb56
   __TEXT.__objc_methtype: 0x28e1
   __TEXT.__objc_stubs: 0xbea0
-  __DATA_CONST.__got: 0x1008
+  __DATA_CONST.__got: 0x1000
   __DATA_CONST.__const: 0x2588
-  __DATA_CONST.__objc_classlist: 0x288
+  __DATA_CONST.__objc_classlist: 0x280
   __DATA_CONST.__objc_catlist: 0x40
-  __DATA_CONST.__objc_protolist: 0x178
+  __DATA_CONST.__objc_protolist: 0x168
   __DATA_CONST.__objc_imageinfo: 0x8
-  __DATA_CONST.__objc_selrefs: 0x3530
+  __DATA_CONST.__objc_selrefs: 0x3520
-  __DATA_CONST.__objc_protorefs: 0x40
+  __DATA_CONST.__objc_protorefs: 0x38
   __DATA_CONST.__objc_superrefs: 0x160
   __DATA_CONST.__objc_arraydata: 0x78
-  __AUTH_CONST.__auth_got: 0x8f8
+  __AUTH_CONST.__auth_got: 0x8a8
   __AUTH_CONST.__auth_ptr: 0x1d8
   __AUTH_CONST.__const: 0x9e8
   __AUTH_CONST.__cfstring: 0x4e60
-  __AUTH_CONST.__objc_const: 0x11af8
+  __AUTH_CONST.__objc_const: 0x116c8
   __AUTH_CONST.__objc_intobj: 0x180
   __AUTH_CONST.__objc_arrayobj: 0x30
-  __AUTH.__objc_data: 0x1110
+  __AUTH.__objc_data: 0x10a0
-  __AUTH.__data: 0x78
+  __AUTH.__data: 0x58
   __DATA.__objc_ivar: 0x3a0
-  __DATA.__data: 0x1308
+  __DATA.__data: 0x1288
   __DATA.__bss: 0x840
   __DATA.__common: 0x18
   __DATA_DIRTY.__objc_data: 0x920
   __DATA_DIRTY.__data: 0x58
   __DATA_DIRTY.__bss: 0x120
   - /System/Library/Frameworks/Accounts.framework/Accounts
   - /System/Library/Frameworks/CloudKit.framework/CloudKit

   - /usr/lib/swift/libswiftos.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 55AA7626-BB7C-3FA9-BA81-AF874097C680
+  UUID: 49E3D0DA-2D68-3A8E-9986-7B1A5CB3AB4F
-  Functions: 3027
+  Functions: 3015
-  Symbols:   9826
+  Symbols:   9800
-  CStrings:  5346
+  CStrings:  5328
 
Symbols:
- -[CDPDManateeStateObserver deviceDidUnlock]
- _MKBGetDeviceLockState
- _OBJC_CLASS_$_CDPDUnlockObserver
- _OBJC_METACLASS_$_CDPDUnlockObserver
- __DATA_CDPDUnlockObserver
- __INSTANCE_METHODS_CDPDUnlockObserver
- __IVARS_CDPDUnlockObserver
- __METACLASS_DATA_CDPDUnlockObserver
- __OBJC_$_PROTOCOL_INSTANCE_METHODS_CDPDUnlockListener
- __OBJC_$_PROTOCOL_METHOD_TYPES_CDPDUnlockListener
- __OBJC_$_PROTOCOL_REFS_CDPDUnlockListener
- __OBJC_LABEL_PROTOCOL_$_CDPDUnlockListener
- __OBJC_PROTOCOL_$_CDPDUnlockListener
- __PROTOCOLS_CDPDUnlockObserver
- __PROTOCOLS_CDPDUnlockObserver.2
- _swift_endAccess
- _swift_unknownObjectRelease_n
- _swift_unknownObjectRetain_n
CStrings:
- "%{public}s device is not unlocked. Found lock state %{public}d."
- "%{public}s ignoring event %{public}s because device is not unlocked"
- "%{public}s ignoring notification event %{public}s"
- "%{public}s received a nil eventName"
- "%{public}s recognizes event name %{public}s as unlocked. Notifying %{public}ld listeners."
- "CDPDUnlockListener"
- "CDPDUnlockObserver"
- "Fetched manatee status after device unlock with altDSID=%@, isPrimaryAccount=%{BOOL}d"
- "Fetching manatee status after device unlock with altDSID=%@, isPrimaryAccount=%{BOOL}d"
- "Notifying listener %{public}s"
- "com.apple.mobile.keybagd.lock_status"
- "currentDeviceIsUnlocked"
- "deviceDidUnlock"

```

#### IMSharedUtilities

>  `/System/Library/PrivateFrameworks/IMSharedUtilities.framework/IMSharedUtilities`

```diff

-1402.300.181.2.20
+1402.300.181.2.21
   __TEXT.__text: 0x27d2e4
   __TEXT.__auth_stubs: 0x3e40
   __TEXT.__objc_methlist: 0x109d8
   __TEXT.__const: 0x10938
   __TEXT.__cstring: 0x20c27
   __TEXT.__gcc_except_tab: 0xab48
   __TEXT.__oslogstring: 0x17b45
   __TEXT.__dlopen_cstrs: 0x46a
   __TEXT.__ustring: 0x416
   __TEXT.__constg_swiftt: 0x3f4c
   __TEXT.__swift5_typeref: 0x4624
   __TEXT.__swift5_fieldmd: 0x5344
   __TEXT.__swift5_builtin: 0x8c
   __TEXT.__swift5_reflstr: 0x49b3

   __TEXT.__swift5_capture: 0xb88
   __TEXT.__swift5_protos: 0x80
   __TEXT.__swift5_mpenum: 0x8
   __TEXT.__unwind_info: 0xb2e0
   __TEXT.__eh_frame: 0xa150
   __TEXT.__objc_classname: 0x25c3
   __TEXT.__objc_methname: 0x30765
   __TEXT.__objc_methtype: 0x7865
   __TEXT.__objc_stubs: 0x170a0
   __DATA_CONST.__got: 0x1540
   __DATA_CONST.__const: 0x5680
   __DATA_CONST.__objc_classlist: 0xa60
   __DATA_CONST.__objc_catlist: 0xb0
   __DATA_CONST.__objc_protolist: 0x3f8
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_selrefs: 0x95c8
   __DATA_CONST.__objc_protorefs: 0x1c8
   __DATA_CONST.__objc_superrefs: 0x530
   __DATA_CONST.__objc_arraydata: 0x6b0
   __AUTH_CONST.__auth_got: 0x1f30
-  __AUTH_CONST.__auth_ptr: 0x1380
+  __AUTH_CONST.__auth_ptr: 0x1398
   __AUTH_CONST.__const: 0xd310
   __AUTH_CONST.__cfstring: 0x19ce0
   __AUTH_CONST.__objc_const: 0x20f80
   __AUTH_CONST.__objc_intobj: 0x348
   __AUTH_CONST.__objc_arrayobj: 0x4b0
   __AUTH_CONST.__objc_dictobj: 0x78
   __AUTH_CONST.__objc_doubleobj: 0x10
   __AUTH.__objc_data: 0x5168
   __AUTH.__data: 0x3f48
   __DATA.__objc_ivar: 0xc88
   __DATA.__data: 0x7508
   __DATA.__bss: 0x23e50
   __DATA.__common: 0xc8
   __DATA_DIRTY.__objc_data: 0x2118
   __DATA_DIRTY.__data: 0x6e8
   __DATA_DIRTY.__bss: 0xa88
   - /System/Library/Frameworks/AVFoundation.framework/AVFoundation
   - /System/Library/Frameworks/Accounts.framework/Accounts

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 59814AAE-E111-3861-8BF4-F74AF70840E9
+  UUID: 49261D6E-811B-3178-B0CA-CAB43F438808
   Functions: 14194
   Symbols:   3260
   CStrings:  17654

```

#### IMTranscoderAgent

>  `/System/Library/PrivateFrameworks/IMTranscoderAgent.framework/IMTranscoderAgent`

```diff

-1402.300.181.2.20
+1402.300.181.2.21
   __TEXT.__text: 0x1dca4
   __TEXT.__auth_stubs: 0xb70
   __TEXT.__objc_methlist: 0x944
   __TEXT.__const: 0x2b8
   __TEXT.__gcc_except_tab: 0x24e4
   __TEXT.__cstring: 0xb6a
   __TEXT.__oslogstring: 0x503f
   __TEXT.__unwind_info: 0x598
   __TEXT.__objc_classname: 0x1d9
   __TEXT.__objc_methname: 0x382f
   __TEXT.__objc_methtype: 0xb27
   __TEXT.__objc_stubs: 0x28c0
   __DATA_CONST.__got: 0x5c0
   __DATA_CONST.__const: 0x5d8
   __DATA_CONST.__objc_classlist: 0x80
   __DATA_CONST.__objc_protolist: 0x18
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_selrefs: 0xb68
   __DATA_CONST.__objc_protorefs: 0x8
   __DATA_CONST.__objc_superrefs: 0x48
   __DATA_CONST.__objc_arraydata: 0x258
   __AUTH_CONST.__auth_got: 0x5c8
   __AUTH_CONST.__const: 0x140
   __AUTH_CONST.__cfstring: 0xa80
   __AUTH_CONST.__objc_const: 0x13c0
   __AUTH_CONST.__objc_intobj: 0xd8
   __AUTH_CONST.__objc_arrayobj: 0x48
   __AUTH_CONST.__objc_doubleobj: 0x1c0
   __AUTH_CONST.__objc_dictobj: 0x50
   __DATA.__objc_ivar: 0x90
   __DATA.__data: 0x120
   __DATA.__bss: 0x78
   __DATA_DIRTY.__objc_data: 0x500
   __DATA_DIRTY.__bss: 0x10
   - /System/Library/Frameworks/AVFoundation.framework/AVFoundation
   - /System/Library/Frameworks/Accelerate.framework/Accelerate

   - /usr/lib/libMobileGestalt.dylib
   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: 707A39B4-606F-30BF-B869-1992B2400947
+  UUID: 5532D675-98E8-39FB-873D-FD0761AE3247
   Functions: 260
   Symbols:   399
   CStrings:  1206
CStrings:
+ "15:58:06"
+ "Dec 18 2024"
- "18:52:34"
- "Dec  6 2024"

```

#### MessagesCloudSync

>  `/System/Library/PrivateFrameworks/MessagesCloudSync.framework/MessagesCloudSync`

```diff

-1402.300.181.2.20
+1402.300.181.2.21
   __TEXT.__text: 0x111e78
   __TEXT.__auth_stubs: 0x1f20
   __TEXT.__objc_methlist: 0x610
   __TEXT.__const: 0x7490
   __TEXT.__cstring: 0x4ad1
   __TEXT.__constg_swiftt: 0x2b20
   __TEXT.__swift5_typeref: 0x267c
   __TEXT.__swift5_builtin: 0x154
   __TEXT.__swift5_reflstr: 0x2b0a
   __TEXT.__swift5_fieldmd: 0x3138

   __TEXT.__objc_classname: 0x195
   __TEXT.__objc_methname: 0x2852
   __TEXT.__objc_methtype: 0x55f
   __TEXT.__objc_stubs: 0x4a0
   __DATA_CONST.__got: 0x780
   __DATA_CONST.__const: 0x1b0
   __DATA_CONST.__objc_classlist: 0x110
   __DATA_CONST.__objc_catlist: 0x8
   __DATA_CONST.__objc_protolist: 0x100
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_selrefs: 0xd58
   __DATA_CONST.__objc_protorefs: 0x88
   __DATA_CONST.__objc_superrefs: 0x10
   __AUTH_CONST.__auth_got: 0xf98
-  __AUTH_CONST.__auth_ptr: 0xa90
+  __AUTH_CONST.__auth_ptr: 0xaf8
   __AUTH_CONST.__const: 0x8678
   __AUTH_CONST.__cfstring: 0x60
   __AUTH_CONST.__objc_const: 0x2db8
   __AUTH_CONST.__objc_intobj: 0x18
   __AUTH.__objc_data: 0x3a8
   __AUTH.__data: 0x578
   __DATA.__objc_ivar: 0x8
   __DATA.__data: 0x1a98
   __DATA.__bss: 0x9bf0
   __DATA.__common: 0x18
   __DATA_DIRTY.__objc_data: 0x588
   __DATA_DIRTY.__data: 0x23b8
   __DATA_DIRTY.__bss: 0x2b80
   __DATA_DIRTY.__common: 0x260
   - /System/Library/Frameworks/CloudKit.framework/CloudKit

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 31072C9D-1D9D-3E90-A8B6-25F4ED531EC1
+  UUID: 29C6C406-03D0-3CC2-ACB1-6655FDECBC83
   Functions: 4198
   Symbols:   403
   CStrings:  1516

```

#### MessagesSettingsUI

>  `/System/Library/PrivateFrameworks/MessagesSettingsUI.framework/MessagesSettingsUI`

```diff

-1402.300.181.2.20
+1402.300.181.2.21
   __TEXT.__text: 0x2e594
   __TEXT.__auth_stubs: 0x1200
   __TEXT.__objc_methlist: 0x11d8
   __TEXT.__const: 0x1ec4
   __TEXT.__cstring: 0x2747
   __TEXT.__gcc_except_tab: 0xa20
   __TEXT.__oslogstring: 0x8c5
   __TEXT.__dlopen_cstrs: 0x58
   __TEXT.__constg_swiftt: 0x100c
   __TEXT.__swift5_typeref: 0x3100
   __TEXT.__swift5_fieldmd: 0x680
   __TEXT.__swift5_reflstr: 0x896
   __TEXT.__swift5_assocty: 0x308

   __TEXT.__swift5_capture: 0x140
   __TEXT.__swift5_builtin: 0x14
   __TEXT.__swift5_protos: 0x4
   __TEXT.__unwind_info: 0xbe8
   __TEXT.__eh_frame: 0x40
   __TEXT.__objc_classname: 0x357
   __TEXT.__objc_methname: 0x4af2
   __TEXT.__objc_methtype: 0xd7c
   __TEXT.__objc_stubs: 0x3820
   __DATA_CONST.__got: 0x660
   __DATA_CONST.__const: 0x428
   __DATA_CONST.__objc_classlist: 0x170
   __DATA_CONST.__objc_catlist: 0x8
   __DATA_CONST.__objc_protolist: 0x20
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_selrefs: 0x1218
   __DATA_CONST.__objc_superrefs: 0x90
   __DATA_CONST.__objc_arraydata: 0x28
   __AUTH_CONST.__auth_got: 0x910
-  __AUTH_CONST.__auth_ptr: 0x560
+  __AUTH_CONST.__auth_ptr: 0x578
   __AUTH_CONST.__const: 0xd70
   __AUTH_CONST.__cfstring: 0x15c0
   __AUTH_CONST.__objc_const: 0x3ab8
   __AUTH_CONST.__objc_intobj: 0x60
   __AUTH_CONST.__objc_arrayobj: 0x30
   __AUTH_CONST.__objc_dictobj: 0x28
   __AUTH.__objc_data: 0x9c0
   __AUTH.__data: 0x14f0
   __DATA.__objc_ivar: 0xd8
   __DATA.__data: 0xb38
   __DATA.__bss: 0x1fc8
   __DATA.__common: 0x40
   - /System/Library/Frameworks/Accounts.framework/Accounts

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 178C8F05-4BA2-3592-910B-85BC2A91E116
+  UUID: 9DB693A2-8D4E-35C0-9DB5-16D268CD47F3
   Functions: 1139
   Symbols:   2297
   CStrings:  1468

```

#### MessagesSupport

>  `/System/Library/PrivateFrameworks/MessagesSupport.framework/MessagesSupport`

```diff

-1402.300.181.2.20
+1402.300.181.2.21
   __TEXT.__text: 0xca8c
   __TEXT.__auth_stubs: 0xba0
   __TEXT.__objc_methlist: 0x5c4
   __TEXT.__const: 0x938
   __TEXT.__cstring: 0x7da
   __TEXT.__constg_swiftt: 0x3b0
   __TEXT.__swift5_typeref: 0xa67
   __TEXT.__swift5_builtin: 0x3c
   __TEXT.__swift5_types: 0x40
   __TEXT.__swift5_reflstr: 0x24d

   __TEXT.__objc_classname: 0x12d
   __TEXT.__objc_methname: 0x10c6
   __TEXT.__objc_methtype: 0x4e5
   __TEXT.__objc_stubs: 0x480
   __DATA_CONST.__got: 0x1f0
   __DATA_CONST.__const: 0x1c8
   __DATA_CONST.__objc_classlist: 0x68

   __DATA_CONST.__objc_protorefs: 0x20
   __DATA_CONST.__objc_superrefs: 0x30
   __AUTH_CONST.__auth_got: 0x5d8
-  __AUTH_CONST.__auth_ptr: 0x290
+  __AUTH_CONST.__auth_ptr: 0x298
   __AUTH_CONST.__const: 0x400
   __AUTH_CONST.__cfstring: 0x20
   __AUTH_CONST.__objc_const: 0x1350
   __AUTH.__data: 0x140
   __DATA.__objc_ivar: 0x58
   __DATA.__data: 0x488
   __DATA.__bss: 0x850
   __DATA.__common: 0x28
   __DATA_DIRTY.__objc_data: 0x568
   __DATA_DIRTY.__data: 0x160
   - /System/Library/Frameworks/Combine.framework/Combine
   - /System/Library/Frameworks/CoreFoundation.framework/CoreFoundation
   - /System/Library/Frameworks/EventKitUI.framework/EventKitUI

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 7E7DC074-FE32-35B5-BEAB-561F6F43D313
+  UUID: 5694B4D3-DF49-38F6-99F6-0C00FEC2D232
   Functions: 422
   Symbols:   645
   CStrings:  335

```

#### SettingsFoundation

>  `/System/Library/PrivateFrameworks/SettingsFoundation.framework/SettingsFoundation`

```diff

-1080.2.3.0.0
+1080.2.6.0.0
-  __TEXT.__text: 0x10ce0
+  __TEXT.__text: 0x10d30
   __TEXT.__auth_stubs: 0x760
   __TEXT.__objc_methlist: 0x604
   __TEXT.__const: 0x7f8
-  __TEXT.__cstring: 0x199b
+  __TEXT.__cstring: 0x19a7
   __TEXT.__ustring: 0x78
   __TEXT.__oslogstring: 0x158c
   __TEXT.__gcc_except_tab: 0x28
   __TEXT.__dlopen_cstrs: 0x5a
   __TEXT.__unwind_info: 0x310
   __TEXT.__objc_classname: 0x107
   __TEXT.__objc_methname: 0x1c3f
   __TEXT.__objc_methtype: 0x144
   __TEXT.__objc_stubs: 0x1ce0
   __DATA_CONST.__got: 0x2c0
   __DATA_CONST.__const: 0x248
   __DATA_CONST.__objc_classlist: 0x50
   __DATA_CONST.__objc_catlist: 0x8
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_selrefs: 0x890
   __DATA_CONST.__objc_superrefs: 0x38
-  __DATA_CONST.__objc_arraydata: 0x60
+  __DATA_CONST.__objc_arraydata: 0x88
   __AUTH_CONST.__auth_got: 0x3c0
   __AUTH_CONST.__const: 0x460
-  __AUTH_CONST.__cfstring: 0x2040
+  __AUTH_CONST.__cfstring: 0x20c0
   __AUTH_CONST.__objc_const: 0x8b0
-  __AUTH_CONST.__objc_arrayobj: 0xa8
+  __AUTH_CONST.__objc_arrayobj: 0xc0
   __AUTH_CONST.__objc_intobj: 0x48
   __DATA.__objc_ivar: 0x2c
   __DATA.__data: 0x28
   __DATA.__bss: 0xc8
   __DATA_DIRTY.__objc_data: 0x320
   __DATA_DIRTY.__bss: 0x178
   - /System/Library/Frameworks/CoreFoundation.framework/CoreFoundation
   - /System/Library/Frameworks/CoreGraphics.framework/CoreGraphics

   - /usr/lib/libMobileGestalt.dylib
   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: A190A6AC-8008-3FF2-96E3-B37DA5EE646F
+  UUID: E383D6DD-538B-3B3C-A938-B7AD08375246
   Functions: 286
   Symbols:   1173
-  CStrings:  977
+  CStrings:  985
 
Symbols:
+ _SFBuiltInRegulatoryImageForModelAndVariant.styleSensitiveImage.309
+ _SFBuiltInRegulatoryImageForModelAndVariant.styleSensitiveImage.316
+ ___block_literal_global.258
+ ___block_literal_global.260
+ ___block_literal_global.265
+ ___block_literal_global.267
+ ___block_literal_global.273
+ ___block_literal_global.339
+ ___block_literal_global.355
+ ___block_literal_global.360
+ ___block_literal_global.382
+ ___block_literal_global.390
+ ___block_literal_global.506
- _SFBuiltInRegulatoryImageForModelAndVariant.styleSensitiveImage.291
- _SFBuiltInRegulatoryImageForModelAndVariant.styleSensitiveImage.298
- ___block_literal_global.240
- ___block_literal_global.242
- ___block_literal_global.247
- ___block_literal_global.249
- ___block_literal_global.255
- ___block_literal_global.321
- ___block_literal_global.337
- ___block_literal_global.342
- ___block_literal_global.364
- ___block_literal_global.372
- ___block_literal_global.488
CStrings:
+ "CI"
+ "LL"
+ "LZ"
+ "VC"

```


</details>

## EOF