# 26.4.1 (23E254) .vs 26.4.2 (23E261)

## IPSWs

- `iPhone18,1_26.4.1_23E254_Restore.ipsw`
- `iPhone18,1_26.4.2_23E261_Restore.ipsw`

## Kernel

### Version

| iOS | Version | Build | Date |
| :-- | :------ | :---- | :--- |
| 26.4.1 *(23E254)* | 25.4.0 | 12377.102.10~3 | Thu, 05Mar2026 23:59:10 PST |
| 26.4.2 *(23E261)* | 25.4.0 | 12377.102.10~3 | Thu, 05Mar2026 23:59:10 PST |

## MachO

### filesystem

#### ⬆️ Updated (6)

<details>
  <summary><i>View Updated</i></summary>


#### iMessage

>  `/System/Library/Messages/PlugIns/iMessage.imservice/iMessage`

```diff

-1450.500.221.2.9
+1450.500.221.2.14
-  __TEXT.__text: 0xc3e20
+  __TEXT.__text: 0xc3f60
-  __TEXT.__auth_stubs: 0x1c20
+  __TEXT.__auth_stubs: 0x1c30
-  __TEXT.__objc_stubs: 0xd2e0
+  __TEXT.__objc_stubs: 0xd320
-  __TEXT.__objc_methlist: 0x29bc
+  __TEXT.__objc_methlist: 0x29c4
   __TEXT.__const: 0xe58
-  __TEXT.__gcc_except_tab: 0xa058
+  __TEXT.__gcc_except_tab: 0xa05c
-  __TEXT.__cstring: 0x327d
+  __TEXT.__cstring: 0x32ad
   __TEXT.__oslogstring: 0x1738b
   __TEXT.__objc_classname: 0x61c
-  __TEXT.__objc_methname: 0x12804
+  __TEXT.__objc_methname: 0x12864
-  __TEXT.__objc_methtype: 0x2c69
+  __TEXT.__objc_methtype: 0x2c79
   __TEXT.__ustring: 0x4
   __TEXT.__swift5_typeref: 0x67e
   __TEXT.__constg_swiftt: 0x370
   __TEXT.__swift5_reflstr: 0x2d6
   __TEXT.__swift5_fieldmd: 0x368
   __TEXT.__swift5_proto: 0x3c
   __TEXT.__swift5_types: 0x3c
   __TEXT.__swift_as_entry: 0x48
   __TEXT.__swift_as_ret: 0x4c
   __TEXT.__swift5_capture: 0x308
   __TEXT.__swift5_assocty: 0x48
   __TEXT.__swift5_builtin: 0x64
   __TEXT.__swift5_mpenum: 0x38
   __TEXT.__swift5_protos: 0x4
   __TEXT.__unwind_info: 0x2330
   __TEXT.__eh_frame: 0x988
-  __DATA_CONST.__auth_got: 0xe20
+  __DATA_CONST.__auth_got: 0xe28
   __DATA_CONST.__got: 0x10d8
   __DATA_CONST.__auth_ptr: 0x1d8
   __DATA_CONST.__const: 0x3a48
-  __DATA_CONST.__cfstring: 0x3840
+  __DATA_CONST.__cfstring: 0x3860
   __DATA_CONST.__objc_classlist: 0xe0
   __DATA_CONST.__objc_catlist: 0x38
   __DATA_CONST.__objc_protolist: 0x78
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_protorefs: 0x18
   __DATA_CONST.__objc_superrefs: 0x90
   __DATA_CONST.__objc_intobj: 0x3c0
   __DATA_CONST.__objc_arraydata: 0x30
   __DATA_CONST.__objc_arrayobj: 0x78
   __DATA_CONST.__objc_doubleobj: 0x20
   __DATA.__objc_const: 0x2e08
-  __DATA.__objc_selrefs: 0x3ac0
+  __DATA.__objc_selrefs: 0x3ad0
   __DATA.__objc_ivar: 0x1c8
   __DATA.__objc_data: 0x9c0
   __DATA.__data: 0xa60
   __DATA.__bss: 0x8f0
   - /System/Library/Frameworks/CloudKit.framework/CloudKit
   - /System/Library/Frameworks/CoreFoundation.framework/CoreFoundation
   - /System/Library/Frameworks/CoreServices.framework/CoreServices

   - /usr/lib/swift/libswift_Concurrency.dylib
   - /usr/lib/swift/libswiftos.dylib
   - /usr/lib/swift/libswiftsimd.dylib
-  UUID: 95C89B97-D474-32AB-83F0-DFAC73717D2C
+  UUID: 3BBE6D71-A477-31DA-A41C-1FDFE5C36B8F
-  Functions: 1668
+  Functions: 1669
-  Symbols:   892
+  Symbols:   893
-  CStrings:  5119
+  CStrings:  5124
 
Symbols:
+ _IMSharedHelperPayloadByStrippingServerBagKeys
CStrings:
+ "B36@0:8@16B24@28"
+ "MessageGroupController-strip-payload-keys"
+ "_shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:"
+ "getNumberOfTimesRespondedToThread"

```

#### HeuristicInterpreter

>  `/System/Library/PrivateFrameworks/ActionPredictionHeuristics.framework/XPCServices/HeuristicInterpreter.xpc/HeuristicInterpreter`

```diff

-627.11.0.0.0
+627.11.0.1.0
   __TEXT.__text: 0x17a30
   __TEXT.__auth_stubs: 0x600
   __TEXT.__objc_stubs: 0x24c0
   __TEXT.__objc_methlist: 0xacc
-  __TEXT.__const: 0xf0
+  __TEXT.__const: 0xf8
   __TEXT.__cstring: 0x2393
   __TEXT.__objc_classname: 0xcc
   __TEXT.__objc_methname: 0x28bc
   __TEXT.__objc_methtype: 0xa35
   __TEXT.__oslogstring: 0xb6f
   __TEXT.__gcc_except_tab: 0xd10
   __TEXT.__unwind_info: 0x820
   __DATA_CONST.__auth_got: 0x310
   __DATA_CONST.__got: 0x270
   __DATA_CONST.__const: 0x16c0
   __DATA_CONST.__cfstring: 0x23c0
   __DATA_CONST.__objc_classlist: 0x20
   __DATA_CONST.__objc_catlist: 0x18
   __DATA_CONST.__objc_protolist: 0x28

   __DATA_CONST.__objc_protorefs: 0x8
   __DATA_CONST.__objc_superrefs: 0x18
   __DATA_CONST.__linkguard: 0xe
   __DATA_CONST.__objc_intobj: 0x108
   __DATA_CONST.__objc_arraydata: 0x90
   __DATA_CONST.__objc_dictobj: 0xc8
   __DATA_CONST.__objc_arrayobj: 0x30
   __DATA.__objc_const: 0xfa8
   __DATA.__objc_selrefs: 0xa70
   __DATA.__objc_ivar: 0x44
   __DATA.__objc_data: 0x140
   __DATA.__data: 0x1e0
   __DATA.__bss: 0x320
   - /System/Library/Frameworks/Contacts.framework/Contacts
   - /System/Library/Frameworks/CoreFoundation.framework/CoreFoundation

   - /usr/lib/libMobileGestalt.dylib
   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: 6237953C-F2BD-33F2-A4F0-EBDC8C7C4E9D
+  UUID: 4C5366B0-29BB-3196-9446-5E68E2E43C06
   Functions: 523
   Symbols:   199
   CStrings:  1227

```

#### AppPredictionIntentsHelperService

>  `/System/Library/PrivateFrameworks/AppPredictionFoundation.framework/XPCServices/AppPredictionIntentsHelperService.xpc/AppPredictionIntentsHelperService`

```diff

-627.11.0.0.0
+627.11.0.1.0
   __TEXT.__text: 0x2ad8
   __TEXT.__auth_stubs: 0x1c0
   __TEXT.__objc_stubs: 0x260
   __TEXT.__objc_methlist: 0x23c
-  __TEXT.__const: 0x80
+  __TEXT.__const: 0x88
   __TEXT.__objc_methname: 0x461
   __TEXT.__cstring: 0x2c1
   __TEXT.__objc_classname: 0x7d

   __TEXT.__unwind_info: 0x200
   __DATA_CONST.__auth_got: 0xe8
   __DATA_CONST.__got: 0x30
   __DATA_CONST.__const: 0x600
   __DATA_CONST.__objc_classlist: 0x10
   __DATA_CONST.__objc_protolist: 0x18
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_protorefs: 0x8
   __DATA_CONST.__objc_superrefs: 0x8
   __DATA.__objc_const: 0x438
   __DATA.__objc_selrefs: 0x198
   __DATA.__objc_ivar: 0x4
   __DATA.__objc_data: 0xa0
   __DATA.__data: 0x120
   __DATA.__bss: 0x2f0
   - /System/Library/Frameworks/EventKit.framework/EventKit
   - /System/Library/Frameworks/Foundation.framework/Foundation

   - /System/Library/PrivateFrameworks/LinkMetadata.framework/LinkMetadata
   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: E51621AF-11BA-3F08-BCC3-B940AAE0FB7E
+  UUID: 1A53BFF3-AA8C-39E7-B4F9-B88D51BD1188
   Functions: 164
   Symbols:   48
   CStrings:  147

```

#### imagent

>  `/System/Library/PrivateFrameworks/IMCore.framework/imagent.app/imagent`

```diff

-1450.500.221.2.9
+1450.500.221.2.14
   __TEXT.__text: 0x571a8
   __TEXT.__auth_stubs: 0x1790
   __TEXT.__objc_stubs: 0x7260
   __TEXT.__objc_methlist: 0x3008
   __TEXT.__const: 0x1470
   __TEXT.__gcc_except_tab: 0x3974
   __TEXT.__cstring: 0x163c
   __TEXT.__oslogstring: 0x669b
   __TEXT.__objc_methname: 0xb8f9
   __TEXT.__objc_classname: 0x865

   - /usr/lib/swift/libswift_Concurrency.dylib
   - /usr/lib/swift/libswiftos.dylib
   - /usr/lib/swift/libswiftsimd.dylib
-  UUID: ED0782FA-B808-3CF6-AF15-812B4062706E
+  UUID: A01A11A5-3727-332E-9A0E-A865F497CC32
   Functions: 1254
   Symbols:   562
   CStrings:  2467
CStrings:
+ "18:01:09"
+ "Apr 14 2026"
- "01:26:58"
- "Mar  6 2026"

```

#### com.apple.Siri.ActionPredictionNotifications

>  `/System/Library/UserNotifications/Bundles/com.apple.Siri.ActionPredictionNotifications.bundle/com.apple.Siri.ActionPredictionNotifications`

```diff

-627.11.0.0.0
+627.11.0.1.0
   __TEXT.__text: 0x1f94
   __TEXT.__auth_stubs: 0x50
-  __TEXT.__const: 0x60
+  __TEXT.__const: 0x68
   __TEXT.__cstring: 0x295
   __TEXT.__unwind_info: 0x1d8
   __DATA_CONST.__auth_got: 0x28
   __DATA_CONST.__const: 0x600
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA.__bss: 0x2f0
   - /System/Library/Frameworks/Foundation.framework/Foundation
   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: 247BE9F5-1EB7-34B2-B6F6-A96FEDA62825
+  UUID: F28F3B40-C134-3389-A9A9-D436474614B1
   Functions: 141
   Symbols:   9
   CStrings:  50

```

#### duetexpertd

>  `/usr/libexec/duetexpertd`

```diff

-627.11.0.0.0
+627.11.0.1.0
   __TEXT.__text: 0x4a0
   __TEXT.__auth_stubs: 0x190
   __TEXT.__objc_stubs: 0x160
-  __TEXT.__const: 0x48
+  __TEXT.__const: 0x50
   __TEXT.__cstring: 0x35e
   __TEXT.__oslogstring: 0x4e
   __TEXT.__info_plist: 0x137

   __TEXT.__unwind_info: 0x60
   __DATA_CONST.__auth_got: 0xd0
   __DATA_CONST.__got: 0x70
   __DATA_CONST.__const: 0x80
   __DATA_CONST.__cfstring: 0x220
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__linkguard: 0xe
   __DATA.__objc_selrefs: 0x58
   - /System/Library/Frameworks/CoreFoundation.framework/CoreFoundation
   - /System/Library/Frameworks/EventKit.framework/EventKit
   - /System/Library/Frameworks/Foundation.framework/Foundation

   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libobjc.A.dylib
   - /usr/lib/libsqlite3.dylib
-  UUID: 0F1CA663-F168-3239-B0AF-963C2D1FF8C0
+  UUID: 0AF2603A-400A-3F96-9BCF-84E10B9E5086
   Functions: 3
   Symbols:   45
   CStrings:  51

```


</details>

### iBoot

| iOS | Version |
| :-- | :------ |
| 26.4.1 *(23E254)* | mBoot-18000.102.4 |
| 26.4.2 *(23E261)* | mBoot-18000.102.4 |

## DSC

### WebKit

| iOS | Version |
| :-- | :------ |
| 26.4.1 *(23E254)* | 624.1.16.10.6 |
| 26.4.2 *(23E261)* | 624.1.16.10.6 |

### Dylibs

#### ⬆️ Updated (12)

<details>
  <summary><i>View Updated</i></summary>



#### ActionPredictionHeuristics

>  `/System/Library/PrivateFrameworks/ActionPredictionHeuristics.framework/ActionPredictionHeuristics`

```diff

-627.11.0.0.0
+627.11.0.1.0
   __TEXT.__text: 0x6400
   __TEXT.__auth_stubs: 0x440
   __TEXT.__objc_methlist: 0x32c
-  __TEXT.__const: 0x80
+  __TEXT.__const: 0x88
   __TEXT.__gcc_except_tab: 0x230
   __TEXT.__cstring: 0x51c
   __TEXT.__oslogstring: 0x87e
   __TEXT.__unwind_info: 0x2d8
   __TEXT.__objc_classname: 0xe4
   __TEXT.__objc_methname: 0xc85
   __TEXT.__objc_methtype: 0x3c4
   __TEXT.__objc_stubs: 0xb40
   __DATA_CONST.__got: 0x180
   __DATA_CONST.__const: 0x220
   __DATA_CONST.__objc_classlist: 0x18
   __DATA_CONST.__objc_protolist: 0x28
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_selrefs: 0x3b8
   __DATA_CONST.__objc_protorefs: 0x10
   __DATA_CONST.__objc_superrefs: 0x10
   __AUTH_CONST.__auth_got: 0x230
   __AUTH_CONST.__const: 0x660
   __AUTH_CONST.__cfstring: 0x1a0
   __AUTH_CONST.__objc_const: 0x630
   __DATA.__objc_ivar: 0x38
   __DATA.__data: 0x1e0
   __DATA.__bss: 0x2c0
   __DATA_DIRTY.__objc_data: 0xf0
   __DATA_DIRTY.__bss: 0x40
   - /System/Library/Frameworks/CoreFoundation.framework/CoreFoundation
   - /System/Library/Frameworks/Foundation.framework/Foundation

   - /System/Library/PrivateFrameworks/ProactiveSupport.framework/ProactiveSupport
   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: 048BBABC-9D46-3074-9F59-77F9A033CAC3
+  UUID: A5F28961-BB8A-3A2B-B168-C9E0266FF9D2
   Functions: 213
   Symbols:   879
   CStrings:  311

```

#### ActionPredictionHeuristicsInternal

>  `/System/Library/PrivateFrameworks/ActionPredictionHeuristicsInternal.framework/ActionPredictionHeuristicsInternal`

```diff

-627.11.0.0.0
+627.11.0.1.0
   __TEXT.__text: 0x40f34
   __TEXT.__auth_stubs: 0x8a0
   __TEXT.__objc_methlist: 0x2a34
-  __TEXT.__const: 0x328
+  __TEXT.__const: 0x330
   __TEXT.__cstring: 0x31ca
   __TEXT.__gcc_except_tab: 0xeb0
   __TEXT.__oslogstring: 0x6d8c
   __TEXT.__dlopen_cstrs: 0x1a0
   __TEXT.__unwind_info: 0x1060
   __TEXT.__objc_classname: 0xc98
   __TEXT.__objc_methname: 0x7d30
   __TEXT.__objc_methtype: 0x121e
   __TEXT.__objc_stubs: 0x6e00
   __DATA_CONST.__got: 0x8c8
   __DATA_CONST.__const: 0xc98
   __DATA_CONST.__objc_classlist: 0x320
   __DATA_CONST.__objc_catlist: 0x8
   __DATA_CONST.__objc_protolist: 0x40
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_selrefs: 0x1ea8
   __DATA_CONST.__objc_protorefs: 0x8
   __DATA_CONST.__objc_superrefs: 0x230
   __DATA_CONST.__objc_arraydata: 0x130
   __AUTH_CONST.__auth_got: 0x460
   __AUTH_CONST.__const: 0x980
   __AUTH_CONST.__cfstring: 0x34e0
   __AUTH_CONST.__objc_const: 0x9b38
   __AUTH_CONST.__objc_arrayobj: 0x210
   __AUTH_CONST.__objc_intobj: 0x90
   __AUTH.__objc_data: 0x690
   __DATA.__objc_ivar: 0x2fc
   __DATA.__data: 0x340
   __DATA.__bss: 0x2e0
   __DATA_DIRTY.__objc_data: 0x18b0
   __DATA_DIRTY.__data: 0x40
   __DATA_DIRTY.__bss: 0x120
   - /System/Library/Frameworks/Contacts.framework/Contacts

   - /System/Library/PrivateFrameworks/VoiceShortcutClient.framework/VoiceShortcutClient
   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: BFAA311A-8A13-3B90-832A-00888FF864D7
+  UUID: 276918C2-607E-34C7-B227-BFA277934DD0
   Functions: 1215
   Symbols:   5195
   CStrings:  2810

```

#### AppPredictionClient

>  `/System/Library/PrivateFrameworks/AppPredictionClient.framework/AppPredictionClient`

```diff

-627.11.0.0.0
+627.11.0.1.0
-  __TEXT.__text: 0x199ea8
+  __TEXT.__text: 0x19a42c
   __TEXT.__auth_stubs: 0xea0
-  __TEXT.__objc_methlist: 0x18d84
+  __TEXT.__objc_methlist: 0x18de4
   __TEXT.__const: 0x6f8
-  __TEXT.__cstring: 0x1bc5f
+  __TEXT.__cstring: 0x1bc85
   __TEXT.__oslogstring: 0x17b19
   __TEXT.__gcc_except_tab: 0x22b0
   __TEXT.__dlopen_cstrs: 0x42d
   __TEXT.__ustring: 0x18a
-  __TEXT.__unwind_info: 0x6f38
+  __TEXT.__unwind_info: 0x6f50
   __TEXT.__objc_classname: 0x3bce
-  __TEXT.__objc_methname: 0x349a7
+  __TEXT.__objc_methname: 0x34a9d
-  __TEXT.__objc_methtype: 0x67d6
+  __TEXT.__objc_methtype: 0x6805
-  __TEXT.__objc_stubs: 0x1cde0
+  __TEXT.__objc_stubs: 0x1cf20
   __DATA_CONST.__got: 0x1718
   __DATA_CONST.__const: 0x63c8
   __DATA_CONST.__objc_classlist: 0xe40
   __DATA_CONST.__objc_catlist: 0x90
   __DATA_CONST.__objc_protolist: 0x268
   __DATA_CONST.__objc_imageinfo: 0x8
-  __DATA_CONST.__objc_selrefs: 0x9ff0
+  __DATA_CONST.__objc_selrefs: 0xa038
   __DATA_CONST.__objc_protorefs: 0xb0
   __DATA_CONST.__objc_superrefs: 0xc48
   __DATA_CONST.__objc_arraydata: 0xaf8
   __AUTH_CONST.__auth_got: 0x760
   __AUTH_CONST.__auth_ptr: 0x8
-  __AUTH_CONST.__const: 0x2a80
+  __AUTH_CONST.__const: 0x2ac0
-  __AUTH_CONST.__cfstring: 0x15380
+  __AUTH_CONST.__cfstring: 0x153e0
-  __AUTH_CONST.__objc_const: 0x45f38
+  __AUTH_CONST.__objc_const: 0x45f98
   __AUTH_CONST.__objc_intobj: 0xa20
   __AUTH_CONST.__objc_arrayobj: 0x6d8
   __AUTH_CONST.__objc_doubleobj: 0x10
   __AUTH_CONST.__objc_dictobj: 0x168
   __AUTH.__objc_data: 0x4330
-  __DATA.__objc_ivar: 0x1c7c
+  __DATA.__objc_ivar: 0x1c88
   __DATA.__data: 0x1cf0
   __DATA.__bss: 0x390
   __DATA_DIRTY.__objc_data: 0x4b50
   __DATA_DIRTY.__data: 0x88
   __DATA_DIRTY.__bss: 0x2c8
   - /System/Library/Frameworks/Contacts.framework/Contacts

   - /usr/lib/libarchive.2.dylib
   - /usr/lib/libobjc.A.dylib
   - /usr/lib/libz.1.dylib
-  UUID: 634FFD6C-E956-3D9D-8F0A-F3BFE981D4CF
+  UUID: 4B098232-A975-34F6-86D2-4F9B6FDA769B
-  Functions: 10834
+  Functions: 10845
-  Symbols:   35817
+  Symbols:   35854
-  CStrings:  16113
+  CStrings:  16134
 
Symbols:
+ -[ATXMissedNotificationRankingBiomeStream deleteAllEvents]
+ -[ATXPBUserNotification bodyLength]
+ -[ATXPBUserNotification hasBodyLength]
+ -[ATXPBUserNotification hasSubtitleLength]
+ -[ATXPBUserNotification hasTitleLength]
+ -[ATXPBUserNotification setBodyLength:]
+ -[ATXPBUserNotification setHasBodyLength:]
+ -[ATXPBUserNotification setHasSubtitleLength:]
+ -[ATXPBUserNotification setHasTitleLength:]
+ -[ATXPBUserNotification setSubtitleLength:]
+ -[ATXPBUserNotification setTitleLength:]
+ -[ATXPBUserNotification subtitleLength]
+ -[ATXPBUserNotification titleLength]
+ -[ATXUserNotification setBodyLength:]
+ -[ATXUserNotification setSubtitleLength:]
+ -[ATXUserNotification setTitleLength:]
+ -[ATXUserNotificationDigestBiomeStream deleteAllEvents]
+ -[ATXUserNotificationLoggingEvent jsonDict]
+ OBJC_IVAR_$_ATXPBUserNotification._bodyLength
+ OBJC_IVAR_$_ATXPBUserNotification._subtitleLength
+ OBJC_IVAR_$_ATXPBUserNotification._titleLength
+ _OBJC_IVAR_$_ATXUserNotification._bodyLength
+ _OBJC_IVAR_$_ATXUserNotification._subtitleLength
+ _OBJC_IVAR_$_ATXUserNotification._titleLength
+ ___55-[ATXUserNotificationDigestBiomeStream deleteAllEvents]_block_invoke
+ ___58-[ATXMissedNotificationRankingBiomeStream deleteAllEvents]_block_invoke
+ _objc_msgSend$bodyLength
+ _objc_msgSend$hasBodyLength
+ _objc_msgSend$hasSubtitleLength
+ _objc_msgSend$hasTitleLength
+ _objc_msgSend$setBodyLength:
+ _objc_msgSend$setSubtitleLength:
+ _objc_msgSend$setTitleLength:
+ _objc_msgSend$subtitleLength
+ _objc_msgSend$titleLength
+ _objc_msgSend$unsignedLongLongValue
- -[ATXPBUserNotification body]
- -[ATXPBUserNotification hasBody]
- -[ATXPBUserNotification hasSubtitle]
- -[ATXPBUserNotification hasTitle]
- -[ATXPBUserNotification setBody:]
- -[ATXPBUserNotification setSubtitle:]
- -[ATXPBUserNotification setTitle:]
- -[ATXPBUserNotification subtitle]
- -[ATXPBUserNotification title]
- OBJC_IVAR_$_ATXPBUserNotification._body
- OBJC_IVAR_$_ATXPBUserNotification._subtitle
- OBJC_IVAR_$_ATXPBUserNotification._title
CStrings:
+ "&G3"
+ "TQ,N,V_bodyLength"
+ "TQ,N,V_subtitleLength"
+ "TQ,N,V_titleLength"
+ "_bodyLength"
+ "_subtitleLength"
+ "_titleLength"
+ "hasBodyLength"
+ "hasSubtitleLength"
+ "hasTitleLength"
+ "setBodyLength:"
+ "setHasBodyLength:"
+ "setHasSubtitleLength:"
+ "setHasTitleLength:"
+ "setSubtitleLength:"
+ "setTitleLength:"
+ "unsignedLongLongValue"
+ "{?=\"appSpecifiedScore\"b1\"badge\"b1\"bodyLength\"b1\"numberOfNotificationsInStack\"b1\"positionInStack\"b1\"recordTimestamp\"b1\"subtitleLength\"b1\"timestamp\"b1\"titleLength\"b1\"attachmentType\"b1\"priorityStatus\"b1\"summaryStatus\"b1\"urgency\"b1\"isGroupMessage\"b1\"isMessage\"b1\"isNotificationSummaryEnabled\"b1\"isPartOfStack\"b1\"isPriorityNotificationEnabled\"b1\"isStackSummary\"b1\"isSummarized\"b1}"
- "T@\"NSString\",&,N,V_body"
- "hasBody"
- "{?=\"appSpecifiedScore\"b1\"badge\"b1\"numberOfNotificationsInStack\"b1\"positionInStack\"b1\"recordTimestamp\"b1\"timestamp\"b1\"attachmentType\"b1\"priorityStatus\"b1\"summaryStatus\"b1\"urgency\"b1\"isGroupMessage\"b1\"isMessage\"b1\"isNotificationSummaryEnabled\"b1\"isPartOfStack\"b1\"isPriorityNotificationEnabled\"b1\"isStackSummary\"b1\"isSummarized\"b1}"

```

#### AppPredictionFoundation

>  `/System/Library/PrivateFrameworks/AppPredictionFoundation.framework/AppPredictionFoundation`

```diff

-627.11.0.0.0
+627.11.0.1.0
   __TEXT.__text: 0x1f5ec
   __TEXT.__auth_stubs: 0x690
   __TEXT.__objc_methlist: 0x1ea4
   __TEXT.__const: 0x428
   __TEXT.__gcc_except_tab: 0x49c
-  __TEXT.__cstring: 0x23a9
+  __TEXT.__cstring: 0x23d2
   __TEXT.__oslogstring: 0x1fb9
   __TEXT.__unwind_info: 0xb58
   __TEXT.__objc_classname: 0x5ad
   __TEXT.__objc_methname: 0x5657
   __TEXT.__objc_methtype: 0x9b2
   __TEXT.__objc_stubs: 0x39a0
   __DATA_CONST.__got: 0x310
-  __DATA_CONST.__const: 0xcf0
+  __DATA_CONST.__const: 0xcf8
   __DATA_CONST.__objc_classlist: 0x198
   __DATA_CONST.__objc_catlist: 0x60
   __DATA_CONST.__objc_protolist: 0x48
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_selrefs: 0x1428
   __DATA_CONST.__objc_protorefs: 0x8
   __DATA_CONST.__objc_superrefs: 0xe8
   __AUTH_CONST.__auth_got: 0x358
   __AUTH_CONST.__auth_ptr: 0x8
   __AUTH_CONST.__const: 0x980
-  __AUTH_CONST.__cfstring: 0x21c0
+  __AUTH_CONST.__cfstring: 0x21e0
   __AUTH_CONST.__objc_const: 0x89a8
   __AUTH_CONST.__objc_intobj: 0x48
   __AUTH_CONST.__objc_doubleobj: 0x10
   __AUTH.__objc_data: 0xbe0
   __DATA.__objc_ivar: 0x1d0
   __DATA.__data: 0x360
   __DATA.__bss: 0x2f0
   __DATA_DIRTY.__objc_data: 0x410
   __DATA_DIRTY.__bss: 0x68
   - /System/Library/Frameworks/CoreFoundation.framework/CoreFoundation
   - /System/Library/Frameworks/CoreLocation.framework/CoreLocation

   - /System/Library/PrivateFrameworks/ProtocolBuffer.framework/ProtocolBuffer
   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: 3A728CE2-1258-34D1-9CA5-A24EF18D17B0
+  UUID: 2D5B33EB-E469-31E9-A0C9-376A458A0107
   Functions: 991
-  Symbols:   3712
+  Symbols:   3713
-  CStrings:  1804
+  CStrings:  1806
 
Symbols:
+ __kATXBiomeNotificationPurgeCompleteKey
CStrings:
+ "biomeNotificationPurgeComplete_174515357"

```

#### AppPredictionInternal

>  `/System/Library/PrivateFrameworks/AppPredictionInternal.framework/AppPredictionInternal`

```diff

-627.11.0.0.0
+627.11.0.1.0
-  __TEXT.__text: 0x4a0f0c
+  __TEXT.__text: 0x4a10a4
   __TEXT.__auth_stubs: 0x40e0
-  __TEXT.__objc_methlist: 0x38d44
+  __TEXT.__objc_methlist: 0x38d4c
   __TEXT.__const: 0x423a
   __TEXT.__cstring: 0x58a72
-  __TEXT.__oslogstring: 0x3b0c9
+  __TEXT.__oslogstring: 0x3b139
   __TEXT.__gcc_except_tab: 0xfea0
   __TEXT.__dlopen_cstrs: 0x1d2
   __TEXT.__ustring: 0x90
   __TEXT.__swift5_typeref: 0x13ae
   __TEXT.__constg_swiftt: 0x1c98
   __TEXT.__swift5_reflstr: 0xb94
   __TEXT.__swift5_fieldmd: 0xf7c
   __TEXT.__swift5_proto: 0x13c
   __TEXT.__swift5_types: 0x194
   __TEXT.__swift_as_entry: 0x124
   __TEXT.__swift_as_ret: 0x10c
   __TEXT.__swift5_assocty: 0x240
   __TEXT.__swift5_capture: 0x71c
   __TEXT.__swift5_protos: 0x24
   __TEXT.__swift5_builtin: 0x64
   __TEXT.__swift5_mpenum: 0x8
   __TEXT.__unwind_info: 0xf428
   __TEXT.__eh_frame: 0x2774
   __TEXT.__objc_classname: 0x9a2a
-  __TEXT.__objc_methname: 0xaefbc
+  __TEXT.__objc_methname: 0xaefdc
   __TEXT.__objc_methtype: 0x18444
-  __TEXT.__objc_stubs: 0x4d9e0
+  __TEXT.__objc_stubs: 0x4da00
-  __DATA_CONST.__got: 0x39b8
+  __DATA_CONST.__got: 0x39c0
   __DATA_CONST.__const: 0xbfb8
   __DATA_CONST.__objc_classlist: 0x1f88
   __DATA_CONST.__objc_catlist: 0x138
   __DATA_CONST.__objc_protolist: 0x4d8
   __DATA_CONST.__objc_imageinfo: 0x8
-  __DATA_CONST.__objc_selrefs: 0x1be90
+  __DATA_CONST.__objc_selrefs: 0x1be98
   __DATA_CONST.__objc_protorefs: 0xb0
   __DATA_CONST.__objc_superrefs: 0x1520
   __DATA_CONST.__objc_arraydata: 0x1298
   __AUTH_CONST.__auth_got: 0x2088
   __AUTH_CONST.__auth_ptr: 0x5b8
   __AUTH_CONST.__const: 0x8b90
   __AUTH_CONST.__cfstring: 0x3aa40
   __AUTH_CONST.__objc_const: 0x83c38
   __AUTH_CONST.__objc_intobj: 0x3378
   __AUTH_CONST.__objc_arrayobj: 0x1068
   __AUTH_CONST.__objc_dictobj: 0xf0
   __AUTH_CONST.__objc_floatobj: 0x30
   __AUTH_CONST.__objc_doubleobj: 0x40
   __AUTH.__objc_data: 0x53f8
   __AUTH.__data: 0x2198
   __DATA.__objc_ivar: 0x4ae8
   __DATA.__data: 0x3d98
   __DATA.__bss: 0x2908
   __DATA.__common: 0x128
   __DATA_DIRTY.__objc_data: 0xef70
   __DATA_DIRTY.__data: 0xa48
   __DATA_DIRTY.__bss: 0xb68
   __DATA_DIRTY.__common: 0x98
   - /System/Library/Frameworks/Accelerate.framework/Accelerate

   - /usr/lib/swift/libswift_StringProcessing.dylib
   - /usr/lib/swift/libswiftos.dylib
   - /usr/lib/swift/libswiftsimd.dylib
-  UUID: 8F790799-CB95-3F25-902B-B373C006F5D6
+  UUID: C66CC4AE-35D5-3058-A686-B4B375382EE7
-  Functions: 25674
+  Functions: 25675
-  Symbols:   77861
+  Symbols:   77865
-  CStrings:  42931
+  CStrings:  42933
 
Symbols:
+ -[ATXNotificationAndSuggestionDatabase _purgeNotificationBiomeStreamsIfNeeded]
+ GCC_except_table173
+ GCC_except_table178
+ ___47-[ATXNotificationAndSuggestionDatabase analyze]_block_invoke.341
+ ___47-[ATXNotificationAndSuggestionDatabase analyze]_block_invoke.341.cold.1
+ ___53-[ATXNotificationAndSuggestionDatabase deleteAllData]_block_invoke.289
+ ___53-[ATXNotificationAndSuggestionDatabase deleteAllData]_block_invoke.289.cold.1
+ ___53-[ATXNotificationAndSuggestionDatabase deleteAllData]_block_invoke.290
+ ___53-[ATXNotificationAndSuggestionDatabase deleteAllData]_block_invoke.290.cold.1
+ ___64-[ATXNotificationAndSuggestionDatabase currentActiveSuggestions]_block_invoke.204
+ ___64-[ATXNotificationAndSuggestionDatabase currentActiveSuggestions]_block_invoke.204.cold.1
+ ___68-[ATXNotificationAndSuggestionDatabase updateNotificationFromEvent:]_block_invoke.131
+ ___68-[ATXNotificationAndSuggestionDatabase updateNotificationFromEvent:]_block_invoke_2.132
+ ___68-[ATXNotificationAndSuggestionDatabase updateNotificationFromEvent:]_block_invoke_3.133
+ ___68-[ATXNotificationAndSuggestionDatabase updateNotificationFromEvent:]_block_invoke_3.133.cold.1
+ ___79-[ATXNotificationAndSuggestionDatabase allBundleIdsOfNotificationsOnLockscreen]_block_invoke.286
+ ___79-[ATXNotificationAndSuggestionDatabase allBundleIdsOfNotificationsOnLockscreen]_block_invoke.286.cold.1
+ ___84-[ATXNotificationAndSuggestionDatabase allNotificationsFromBundleId:sinceTimestamp:]_block_invoke.276
+ ___84-[ATXNotificationAndSuggestionDatabase allNotificationsFromBundleId:sinceTimestamp:]_block_invoke.276.cold.1
+ ___89-[ATXNotificationAndSuggestionDatabase pruneSuggestionsBasedOnHardLimitsWithXPCActivity:]_block_invoke.317
+ ___89-[ATXNotificationAndSuggestionDatabase pruneSuggestionsBasedOnHardLimitsWithXPCActivity:]_block_invoke.326
+ ___89-[ATXNotificationAndSuggestionDatabase pruneSuggestionsBasedOnHardLimitsWithXPCActivity:]_block_invoke.333
+ ___89-[ATXNotificationAndSuggestionDatabase pruneSuggestionsBasedOnHardLimitsWithXPCActivity:]_block_invoke_2.327
+ ___89-[ATXNotificationAndSuggestionDatabase pruneSuggestionsBasedOnHardLimitsWithXPCActivity:]_block_invoke_2.327.cold.1
+ ___89-[ATXNotificationAndSuggestionDatabase pruneSuggestionsBasedOnHardLimitsWithXPCActivity:]_block_invoke_2.335
+ ___89-[ATXNotificationAndSuggestionDatabase pruneSuggestionsBasedOnHardLimitsWithXPCActivity:]_block_invoke_2.335.cold.1
+ ___91-[ATXNotificationAndSuggestionDatabase pruneNotificationsBasedOnHardLimitsWithXPCActivity:]_block_invoke.304
+ ___91-[ATXNotificationAndSuggestionDatabase pruneNotificationsBasedOnHardLimitsWithXPCActivity:]_block_invoke_2.306
+ ___91-[ATXNotificationAndSuggestionDatabase pruneNotificationsBasedOnHardLimitsWithXPCActivity:]_block_invoke_2.306.cold.1
+ ___block_literal_global.197
+ ___block_literal_global.229
+ ___block_literal_global.282
+ ___block_literal_global.288
+ ___block_literal_global.308
+ ___block_literal_global.322
+ ___block_literal_global.329
+ ___block_literal_global.337
+ ___block_literal_global.343
+ __kATXBiomeNotificationPurgeCompleteKey
+ _objc_msgSend$_purgeNotificationBiomeStreamsIfNeeded
- GCC_except_table172
- GCC_except_table177
- ___47-[ATXNotificationAndSuggestionDatabase analyze]_block_invoke.337
- ___47-[ATXNotificationAndSuggestionDatabase analyze]_block_invoke.337.cold.1
- ___53-[ATXNotificationAndSuggestionDatabase deleteAllData]_block_invoke.285
- ___53-[ATXNotificationAndSuggestionDatabase deleteAllData]_block_invoke.285.cold.1
- ___53-[ATXNotificationAndSuggestionDatabase deleteAllData]_block_invoke.286
- ___53-[ATXNotificationAndSuggestionDatabase deleteAllData]_block_invoke.286.cold.1
- ___64-[ATXNotificationAndSuggestionDatabase currentActiveSuggestions]_block_invoke.200
- ___64-[ATXNotificationAndSuggestionDatabase currentActiveSuggestions]_block_invoke.200.cold.1
- ___68-[ATXNotificationAndSuggestionDatabase updateNotificationFromEvent:]_block_invoke.127
- ___68-[ATXNotificationAndSuggestionDatabase updateNotificationFromEvent:]_block_invoke_2.128
- ___68-[ATXNotificationAndSuggestionDatabase updateNotificationFromEvent:]_block_invoke_3.129
- ___68-[ATXNotificationAndSuggestionDatabase updateNotificationFromEvent:]_block_invoke_3.129.cold.1
- ___79-[ATXNotificationAndSuggestionDatabase allBundleIdsOfNotificationsOnLockscreen]_block_invoke.282
- ___79-[ATXNotificationAndSuggestionDatabase allBundleIdsOfNotificationsOnLockscreen]_block_invoke.282.cold.1
- ___84-[ATXNotificationAndSuggestionDatabase allNotificationsFromBundleId:sinceTimestamp:]_block_invoke.272
- ___84-[ATXNotificationAndSuggestionDatabase allNotificationsFromBundleId:sinceTimestamp:]_block_invoke.272.cold.1
- ___89-[ATXNotificationAndSuggestionDatabase pruneSuggestionsBasedOnHardLimitsWithXPCActivity:]_block_invoke.313
- ___89-[ATXNotificationAndSuggestionDatabase pruneSuggestionsBasedOnHardLimitsWithXPCActivity:]_block_invoke.322
- ___89-[ATXNotificationAndSuggestionDatabase pruneSuggestionsBasedOnHardLimitsWithXPCActivity:]_block_invoke.329
- ___89-[ATXNotificationAndSuggestionDatabase pruneSuggestionsBasedOnHardLimitsWithXPCActivity:]_block_invoke_2.323
- ___89-[ATXNotificationAndSuggestionDatabase pruneSuggestionsBasedOnHardLimitsWithXPCActivity:]_block_invoke_2.323.cold.1
- ___89-[ATXNotificationAndSuggestionDatabase pruneSuggestionsBasedOnHardLimitsWithXPCActivity:]_block_invoke_2.331
- ___89-[ATXNotificationAndSuggestionDatabase pruneSuggestionsBasedOnHardLimitsWithXPCActivity:]_block_invoke_2.331.cold.1
- ___91-[ATXNotificationAndSuggestionDatabase pruneNotificationsBasedOnHardLimitsWithXPCActivity:]_block_invoke.296
- ___91-[ATXNotificationAndSuggestionDatabase pruneNotificationsBasedOnHardLimitsWithXPCActivity:]_block_invoke_2.302
- ___91-[ATXNotificationAndSuggestionDatabase pruneNotificationsBasedOnHardLimitsWithXPCActivity:]_block_invoke_2.302.cold.1
- ___block_literal_global.187
- ___block_literal_global.189
- ___block_literal_global.225
- ___block_literal_global.278
- ___block_literal_global.284
- ___block_literal_global.304
- ___block_literal_global.318
- ___block_literal_global.325
- ___block_literal_global.333
- ___block_literal_global.339
CStrings:
+ "ATXNotificationAndSuggestionDatabase: Purging private notification streams to remove persisted text content"
+ "_purgeNotificationBiomeStreamsIfNeeded"

```

#### AppPredictionUIFoundation

>  `/System/Library/PrivateFrameworks/AppPredictionUIFoundation.framework/AppPredictionUIFoundation`

```diff

-627.11.0.0.0
+627.11.0.1.0
   __TEXT.__text: 0x26f8
   __TEXT.__auth_stubs: 0x1e0
   __TEXT.__objc_methlist: 0x20
-  __TEXT.__const: 0x68
+  __TEXT.__const: 0x70
   __TEXT.__cstring: 0x2e9
   __TEXT.__oslogstring: 0xfa
   __TEXT.__unwind_info: 0x1f8
   __TEXT.__objc_classname: 0x16
   __TEXT.__objc_methname: 0x32f
   __TEXT.__objc_methtype: 0x1b
   __TEXT.__objc_stubs: 0x300
   __DATA_CONST.__got: 0x90
   __DATA_CONST.__const: 0x98
   __DATA_CONST.__objc_classlist: 0x8
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_selrefs: 0xc8
   __AUTH_CONST.__auth_got: 0xf8
   __AUTH_CONST.__const: 0x5e0
   __AUTH_CONST.__cfstring: 0x60
   __AUTH_CONST.__objc_const: 0x90
   __AUTH.__objc_data: 0x50
   __DATA.__bss: 0x2f0
   - /System/Library/Frameworks/CoreFoundation.framework/CoreFoundation
   - /System/Library/Frameworks/Foundation.framework/Foundation

   - /System/Library/PrivateFrameworks/ProactiveSuggestionClientModel.framework/ProactiveSuggestionClientModel
   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: 2BB57293-4292-3F9F-A969-557F587750F1
+  UUID: E57B0733-B248-37C2-B6A2-F5F6D4104F30
   Functions: 151
   Symbols:   532
   CStrings:  88

```

#### IMSharedUtilities

>  `/System/Library/PrivateFrameworks/IMSharedUtilities.framework/IMSharedUtilities`

```diff

-1450.500.221.2.9
+1450.500.221.2.14
-  __TEXT.__text: 0x321b20
+  __TEXT.__text: 0x321d28
   __TEXT.__auth_stubs: 0x4fc0
   __TEXT.__objc_methlist: 0x16568
   __TEXT.__const: 0x1bb48
-  __TEXT.__cstring: 0x23f17
+  __TEXT.__cstring: 0x23f47
-  __TEXT.__gcc_except_tab: 0xafd4
+  __TEXT.__gcc_except_tab: 0xaffc
-  __TEXT.__oslogstring: 0x1bdd5
+  __TEXT.__oslogstring: 0x1be15
   __TEXT.__dlopen_cstrs: 0x61b
   __TEXT.__ustring: 0x41a
   __TEXT.__swift5_typeref: 0x6704
   __TEXT.__swift5_reflstr: 0x5cc3
   __TEXT.__swift5_assocty: 0x1c18
   __TEXT.__constg_swiftt: 0x5d28
   __TEXT.__swift5_fieldmd: 0x6e34
   __TEXT.__swift5_builtin: 0x258
   __TEXT.__swift5_proto: 0x1a08
   __TEXT.__swift5_types: 0x710
   __TEXT.__swift5_protos: 0xa4
   __TEXT.__swift5_capture: 0x139c
   __TEXT.__swift_as_entry: 0x340
   __TEXT.__swift_as_ret: 0x2ec
   __TEXT.__swift5_mpenum: 0x18
-  __TEXT.__unwind_info: 0xe5d0
+  __TEXT.__unwind_info: 0xe5e0
   __TEXT.__eh_frame: 0xd774
   __TEXT.__objc_classname: 0x3e1b
   __TEXT.__objc_methname: 0x3b09b
   __TEXT.__objc_methtype: 0x8c54
   __TEXT.__objc_stubs: 0x1ce20
   __DATA_CONST.__got: 0x1960
   __DATA_CONST.__const: 0x63b8
   __DATA_CONST.__objc_classlist: 0xc40
   __DATA_CONST.__objc_catlist: 0xd8
   __DATA_CONST.__objc_protolist: 0x3f8
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_selrefs: 0xbeb8
   __DATA_CONST.__objc_protorefs: 0x178
   __DATA_CONST.__objc_superrefs: 0x5e8
   __DATA_CONST.__objc_arraydata: 0x1918
   __AUTH_CONST.__auth_got: 0x27f0
   __AUTH_CONST.__auth_ptr: 0x18c0
   __AUTH_CONST.__const: 0x14a70
-  __AUTH_CONST.__cfstring: 0x20fa0
+  __AUTH_CONST.__cfstring: 0x21000
   __AUTH_CONST.__objc_const: 0x225a8
   __AUTH_CONST.__objc_intobj: 0x8b8
   __AUTH_CONST.__objc_arrayobj: 0x588
   __AUTH_CONST.__objc_dictobj: 0xa0
   __AUTH_CONST.__objc_doubleobj: 0x10
   __AUTH.__objc_data: 0x61a0
   __AUTH.__data: 0x5788
   __DATA.__objc_ivar: 0xe6c
   __DATA.__data: 0x94d0
   __DATA.__bss: 0x324d0
   __DATA.__common: 0x108
   __DATA_DIRTY.__objc_data: 0x2428
   __DATA_DIRTY.__data: 0xe78
   __DATA_DIRTY.__bss: 0x1038
   __DATA_DIRTY.__common: 0x20
   - /System/Library/Frameworks/AVFoundation.framework/AVFoundation

   - /usr/lib/swift/libswift_StringProcessing.dylib
   - /usr/lib/swift/libswiftos.dylib
   - /usr/lib/swift/libswiftsimd.dylib
-  UUID: F29C6B2A-61F6-32C3-B955-F42B045906D4
+  UUID: 34548AD5-80C8-394A-8960-9C594FADBA4B
-  Functions: 18684
+  Functions: 18686
-  Symbols:   3774
+  Symbols:   3776
-  CStrings:  21352
+  CStrings:  21359
 
Symbols:
+ _IMServerBagValueForKnownSender
+ _IMSharedHelperPayloadByStrippingServerBagKeys
CStrings:
+ "%@-%@-r1"
+ "Server bag set, stripping payload keys %@ for sender (known: %{BOOL}d)"
+ "known-sender"
+ "unknown-sender"

```

#### IMTranscoderAgent

>  `/System/Library/PrivateFrameworks/IMTranscoderAgent.framework/IMTranscoderAgent`

```diff

-1450.500.221.2.9
+1450.500.221.2.14
   __TEXT.__text: 0x1f55c
   __TEXT.__auth_stubs: 0xbb0
   __TEXT.__objc_methlist: 0xac4
   __TEXT.__const: 0x2c2
   __TEXT.__gcc_except_tab: 0x24a4
   __TEXT.__cstring: 0xc13
   __TEXT.__oslogstring: 0x5179
   __TEXT.__dlopen_cstrs: 0x64
   __TEXT.__unwind_info: 0x5b8
   __TEXT.__objc_classname: 0x1d9
   __TEXT.__objc_methname: 0x3a62
   __TEXT.__objc_methtype: 0xb2a
   __TEXT.__objc_stubs: 0x2ac0
   __DATA_CONST.__got: 0x5d0
   __DATA_CONST.__const: 0x660
   __DATA_CONST.__objc_classlist: 0x80
   __DATA_CONST.__objc_protolist: 0x18
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_selrefs: 0xc88
   __DATA_CONST.__objc_protorefs: 0x8
   __DATA_CONST.__objc_superrefs: 0x48
   __DATA_CONST.__objc_arraydata: 0x258
   __AUTH_CONST.__auth_got: 0x5e8
   __AUTH_CONST.__auth_ptr: 0x8
   __AUTH_CONST.__const: 0x140
   __AUTH_CONST.__cfstring: 0xb00
   __AUTH_CONST.__objc_const: 0x1130
   __AUTH_CONST.__objc_intobj: 0xd8
   __AUTH_CONST.__objc_arrayobj: 0x48
   __AUTH_CONST.__objc_doubleobj: 0x1c0
   __AUTH_CONST.__objc_dictobj: 0x50
   __DATA.__objc_ivar: 0x90
   __DATA.__data: 0x120
   __DATA.__bss: 0x88
   __DATA_DIRTY.__objc_data: 0x500
   __DATA_DIRTY.__bss: 0x10
   - /System/Library/Frameworks/AVFoundation.framework/AVFoundation
   - /System/Library/Frameworks/Accelerate.framework/Accelerate

   - /usr/lib/libMobileGestalt.dylib
   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: A7090FA3-B72A-353C-83B1-542C95D6BFE2
+  UUID: 44F4693C-B126-3A98-9D82-5CCCE6038081
   Functions: 275
   Symbols:   406
   CStrings:  1241
CStrings:
+ "17:51:24"
+ "Apr 14 2026"
- "01:19:12"
- "Mar  6 2026"

```

#### PaperBoardUI

>  `/System/Library/PrivateFrameworks/PaperBoardUI.framework/PaperBoardUI`

```diff

-304.4.14.101.0
+304.4.14.102.0
   __TEXT.__text: 0x880f0
   __TEXT.__auth_stubs: 0x1030
   __TEXT.__objc_methlist: 0xa2dc
   __TEXT.__const: 0x838
   __TEXT.__cstring: 0x7f04
   __TEXT.__oslogstring: 0x49b8
   __TEXT.__gcc_except_tab: 0x10bc
   __TEXT.__dlopen_cstrs: 0x1a6
   __TEXT.__unwind_info: 0x2e00
   __TEXT.__objc_classname: 0x1611
   __TEXT.__objc_methname: 0x18414
   __TEXT.__objc_methtype: 0x41c7
   __TEXT.__objc_stubs: 0x121a0
   __DATA_CONST.__got: 0x960
   __DATA_CONST.__const: 0x29d8
   __DATA_CONST.__objc_classlist: 0x3d0
   __DATA_CONST.__objc_catlist: 0x60
   __DATA_CONST.__objc_protolist: 0x210
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_selrefs: 0x54b0
   __DATA_CONST.__objc_protorefs: 0x10
   __DATA_CONST.__objc_superrefs: 0x348
   __DATA_CONST.__objc_arraydata: 0x1c8
   __AUTH_CONST.__auth_got: 0x828
   __AUTH_CONST.__auth_ptr: 0x10
   __AUTH_CONST.__const: 0xbe0
   __AUTH_CONST.__cfstring: 0x64e0
   __AUTH_CONST.__objc_const: 0x1ce20
   __AUTH_CONST.__objc_arrayobj: 0xa8
   __AUTH_CONST.__objc_dictobj: 0x1b8
   __AUTH_CONST.__objc_intobj: 0x150
   __AUTH_CONST.__objc_doubleobj: 0x90
   __AUTH.__objc_data: 0x23f0
   __AUTH.__data: 0x8
   __DATA.__objc_ivar: 0xa7c
   __DATA.__data: 0x18e0
   __DATA.__bss: 0x450
   __DATA_DIRTY.__objc_data: 0x230
   __DATA_DIRTY.__bss: 0x20
   - /System/Library/Frameworks/AVFoundation.framework/AVFoundation
   - /System/Library/Frameworks/CoreFoundation.framework/CoreFoundation

   - /usr/lib/libMobileGestalt.dylib
   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: CE91B2C6-D8EE-343A-B59C-AFC7CF056DDE
+  UUID: 6916F3D4-D4E1-3BF4-B7F1-5898351DDA3F
   Functions: 4093
   Symbols:   14072
   CStrings:  6667
CStrings:
+ "Apr 17 2026 15:17:57"
- "Mar  2 2026 21:28:33"

```

#### PosterFuturesKit

>  `/System/Library/PrivateFrameworks/PosterFuturesKit.framework/PosterFuturesKit`

```diff

-304.4.14.101.0
+304.4.14.102.0
-  __TEXT.__text: 0x16d8c
+  __TEXT.__text: 0x1717c
-  __TEXT.__auth_stubs: 0x7c0
+  __TEXT.__auth_stubs: 0x7d0
-  __TEXT.__objc_methlist: 0x2134
+  __TEXT.__objc_methlist: 0x213c
   __TEXT.__const: 0xd0
-  __TEXT.__cstring: 0x891
+  __TEXT.__cstring: 0x933
-  __TEXT.__gcc_except_tab: 0x58c
+  __TEXT.__gcc_except_tab: 0x59c
-  __TEXT.__oslogstring: 0x4b4
+  __TEXT.__oslogstring: 0x568
   __TEXT.__dlopen_cstrs: 0x66
-  __TEXT.__unwind_info: 0xae0
+  __TEXT.__unwind_info: 0xb00
   __TEXT.__objc_classname: 0x615
-  __TEXT.__objc_methname: 0x31e0
+  __TEXT.__objc_methname: 0x31e8
-  __TEXT.__objc_methtype: 0xa26
+  __TEXT.__objc_methtype: 0xa53
-  __TEXT.__objc_stubs: 0x24e0
+  __TEXT.__objc_stubs: 0x24c0
   __DATA_CONST.__got: 0x290
   __DATA_CONST.__const: 0xd38
   __DATA_CONST.__objc_classlist: 0x1a8
   __DATA_CONST.__objc_catlist: 0x10
   __DATA_CONST.__objc_protolist: 0x80
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_selrefs: 0xde0
-  __DATA_CONST.__objc_superrefs: 0x100
+  __DATA_CONST.__objc_superrefs: 0x108
-  __AUTH_CONST.__auth_got: 0x3f0
+  __AUTH_CONST.__auth_got: 0x3f8
   __AUTH_CONST.__auth_ptr: 0x8
   __AUTH_CONST.__const: 0x480
-  __AUTH_CONST.__cfstring: 0x680
+  __AUTH_CONST.__cfstring: 0x660
-  __AUTH_CONST.__objc_const: 0xa258
+  __AUTH_CONST.__objc_const: 0xa278
   __AUTH.__objc_data: 0x870
-  __DATA.__objc_ivar: 0x13c
+  __DATA.__objc_ivar: 0x140
   __DATA.__data: 0x620
   __DATA.__bss: 0x2e8
   __DATA_DIRTY.__objc_data: 0x820
   __DATA_DIRTY.__bss: 0x60
   - /System/Library/Frameworks/CoreFoundation.framework/CoreFoundation
   - /System/Library/Frameworks/Foundation.framework/Foundation

   - /System/Library/PrivateFrameworks/SoftLinking.framework/SoftLinking
   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: 0C3084AE-DC6D-3DDF-AE9D-1445DCF64007
+  UUID: 6D1299D4-040A-3574-BF99-3224EC118DE0
-  Functions: 830
+  Functions: 834
-  Symbols:   3140
+  Symbols:   3146
-  CStrings:  952
+  CStrings:  957
 
Symbols:
+ -[PFTFutureResult init]
+ GCC_except_table44
+ _OBJC_IVAR_$_PFTFutureResult._lock
+ _OBJC_IVAR_$_PFTFutureResult._lock_error
+ _OBJC_IVAR_$_PFTFutureResult._lock_result
+ __BSIsInternalInstall
+ __OBJC_$_PROP_LIST_PFTFuture.181
+ ___66+[PFTFuture recover:withBlock:onErrorScheduler:schedulerProvider:]_block_invoke.12
+ ___66+[PFTFuture recover:withBlock:onErrorScheduler:schedulerProvider:]_block_invoke_3.cold.1
+ ___71+[PFTFuture flatMap:withBlock:continuationScheduler:schedulerProvider:]_block_invoke.8
+ ___71+[PFTFuture flatMap:withBlock:continuationScheduler:schedulerProvider:]_block_invoke_2.10
+ ___71+[PFTFuture flatMap:withBlock:continuationScheduler:schedulerProvider:]_block_invoke_2.cold.1
- _OBJC_IVAR_$_PFTFutureResult._error
- _OBJC_IVAR_$_PFTFutureResult._result
- __OBJC_$_PROP_LIST_PFTFuture.178
- ___66+[PFTFuture recover:withBlock:onErrorScheduler:schedulerProvider:]_block_invoke_4
- ___71+[PFTFuture flatMap:withBlock:continuationScheduler:schedulerProvider:]_block_invoke_3
- ___71+[PFTFuture flatMap:withBlock:continuationScheduler:schedulerProvider:]_block_invoke_4
- _objc_msgSend$setResult:
CStrings:
+ "+[PFTFuture flatMap:withBlock:continuationScheduler:schedulerProvider:]_block_invoke_2"
+ "+[PFTFuture recover:withBlock:onErrorScheduler:schedulerProvider:]_block_invoke_3"
+ "T@\"NSError\",C,N"
+ "T@,&,N"
+ "_lock_error"
+ "_lock_result"
+ "flatMap continuation returned nil — this is a programming error. Call stack: %{public}@"
+ "recover continuation returned nil — this is a programming error. Call stack: %{public}@"
+ "{os_unfair_lock_s=\"_os_unfair_lock_opaque\"I}"
- "T@\"NSError\",C,N,V_error"
- "T@,&,N,V_result"

```

#### PosterLegibilityKit

>  `/System/Library/PrivateFrameworks/PosterLegibilityKit.framework/PosterLegibilityKit`

```diff

-304.4.14.101.0
+304.4.14.102.0
-  __TEXT.__text: 0x1be40
+  __TEXT.__text: 0x1be64
   __TEXT.__auth_stubs: 0xd00
   __TEXT.__objc_methlist: 0x1bf4
   __TEXT.__const: 0x330
   __TEXT.__cstring: 0xf2a
   __TEXT.__oslogstring: 0xf13
   __TEXT.__gcc_except_tab: 0x70c
   __TEXT.__unwind_info: 0x918
   __TEXT.__objc_classname: 0x4fb
-  __TEXT.__objc_methname: 0x49ff
+  __TEXT.__objc_methname: 0x4a0a
   __TEXT.__objc_methtype: 0xd84
-  __TEXT.__objc_stubs: 0x39a0
+  __TEXT.__objc_stubs: 0x39c0
   __DATA_CONST.__got: 0x388
   __DATA_CONST.__const: 0x8a0
   __DATA_CONST.__objc_classlist: 0x100
   __DATA_CONST.__objc_catlist: 0x50
   __DATA_CONST.__objc_protolist: 0x70
   __DATA_CONST.__objc_imageinfo: 0x8
-  __DATA_CONST.__objc_selrefs: 0x1210
+  __DATA_CONST.__objc_selrefs: 0x1218
   __DATA_CONST.__objc_superrefs: 0xe8
   __AUTH_CONST.__auth_got: 0x690
   __AUTH_CONST.__auth_ptr: 0x8
   __AUTH_CONST.__const: 0x2e0
   __AUTH_CONST.__cfstring: 0x11a0
   __AUTH_CONST.__objc_const: 0x4f98
   __AUTH_CONST.__objc_intobj: 0x48
   __AUTH.__objc_data: 0x230
   __DATA.__objc_ivar: 0x224
   __DATA.__data: 0x540
   __DATA.__bss: 0x148
   __DATA_DIRTY.__objc_data: 0x7d0
   __DATA_DIRTY.__bss: 0x88
   - /System/Library/Frameworks/Accelerate.framework/Accelerate
   - /System/Library/Frameworks/CoreFoundation.framework/CoreFoundation

   - /usr/lib/libMobileGestalt.dylib
   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: B427C366-ACD1-38E7-AE36-A084DFDE649E
+  UUID: 7A7CD13A-C2E7-399F-B171-8C4C73314537
   Functions: 690
-  Symbols:   2864
+  Symbols:   2865
-  CStrings:  1389
+  CStrings:  1390
 
Symbols:
+ _objc_msgSend$isFinished
CStrings:
+ "isFinished"

```

#### VisualActionPredictionCore

>  `/System/Library/PrivateFrameworks/VisualActionPredictionCore.framework/VisualActionPredictionCore`

```diff

-627.11.0.0.0
+627.11.0.1.0
   __TEXT.__text: 0x9bb10
   __TEXT.__auth_stubs: 0x2950
   __TEXT.__objc_methlist: 0x57c
-  __TEXT.__const: 0x45e8
+  __TEXT.__const: 0x45f8
   __TEXT.__cstring: 0x1170
   __TEXT.__constg_swiftt: 0x12a0
   __TEXT.__swift5_typeref: 0x173e
   __TEXT.__swift5_builtin: 0x28
   __TEXT.__swift5_reflstr: 0x16c5
   __TEXT.__swift5_fieldmd: 0x158c

   __TEXT.__oslogstring: 0x243a
   __TEXT.__swift5_capture: 0x420
   __TEXT.__swift5_proto: 0x2f8
   __TEXT.__swift_as_entry: 0x138
   __TEXT.__swift_as_ret: 0xfc
   __TEXT.__swift5_protos: 0x14
   __TEXT.__swift5_mpenum: 0x8
   __TEXT.__unwind_info: 0x1a00
   __TEXT.__eh_frame: 0x4b10
   __TEXT.__objc_classname: 0x70b
   __TEXT.__objc_methname: 0x1bf5
   __TEXT.__objc_methtype: 0x576
   __TEXT.__objc_stubs: 0xc40
   __DATA_CONST.__got: 0x940
   __DATA_CONST.__const: 0xa8
   __DATA_CONST.__objc_classlist: 0xd0
   __DATA_CONST.__objc_protolist: 0x70
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_selrefs: 0x558
   __DATA_CONST.__objc_protorefs: 0x38
   __DATA_CONST.__objc_superrefs: 0x8
   __AUTH_CONST.__auth_got: 0x14b0
   __AUTH_CONST.__auth_ptr: 0x700
   __AUTH_CONST.__const: 0x2280
   __AUTH_CONST.__objc_const: 0x3538
   __AUTH.__objc_data: 0x160
   __AUTH.__data: 0x2f8
   __DATA.__objc_ivar: 0x4
   __DATA.__data: 0xd18
   __DATA.__common: 0x50
   __DATA.__bss: 0x5220
   __DATA_DIRTY.__objc_data: 0x940
   __DATA_DIRTY.__data: 0x1fb0
   __DATA_DIRTY.__bss: 0xc90
   __DATA_DIRTY.__common: 0x40
   - /System/Library/Frameworks/AppIntents.framework/AppIntents

   - /usr/lib/swift/libswift_Concurrency.dylib
   - /usr/lib/swift/libswiftos.dylib
   - /usr/lib/swift/libswiftsimd.dylib
-  UUID: 1922BC22-7D84-33CD-8ACD-3AC36B4B2A53
+  UUID: 8A920994-8C15-3B66-8D1A-7438E9E2BF23
   Functions: 1775
   Symbols:   1172
   CStrings:  638

```


</details>

## EOF