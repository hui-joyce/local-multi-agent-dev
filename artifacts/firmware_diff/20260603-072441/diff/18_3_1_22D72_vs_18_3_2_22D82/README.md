# 18.3.1 (22D72) .vs 18.3.2 (22D82)

## Inputs

- `iPhone17,1_18.3.1_22D72_Restore.ipsw`
- `iPhone17,1_18.3.2_22D82_Restore.ipsw`

## Kernel

### Version

| iOS | Version | Build | Date |
| :-- | :------ | :---- | :--- |
| 18.3.1 *(22D72)* | 24.3.0 | 11215.82.4~20 | Thu, 16Jan2025 03:00:11 PST |
| 18.3.2 *(22D82)* | 24.3.0 | 11215.82.4~20 | Thu, 16Jan2025 03:00:11 PST |

## MachO

### ⬆️ Updated (12)

<details>
  <summary><i>View Updated</i></summary>

#### PasswordsSettings

>  `/System/Library/PreferenceBundles/PasswordsSettings.bundle/PasswordsSettings`

```diff

-7620.2.4.10.7
+7620.2.4.10.8
   __TEXT.__text: 0x7ce0
   __TEXT.__auth_stubs: 0x910
   __TEXT.__objc_methlist: 0x19c

   __TEXT.__eh_frame: 0x108
   __DATA_CONST.__auth_got: 0x488
   __DATA_CONST.__got: 0x1f0
-  __DATA_CONST.__auth_ptr: 0x168
+  __DATA_CONST.__auth_ptr: 0x150
   __DATA_CONST.__const: 0x238
   __DATA_CONST.__objc_classlist: 0x20
   __DATA_CONST.__objc_protolist: 0x30

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 5840067A-0C69-3699-9F3E-5148BA7BCB68
+  UUID: 7A6F3EDF-8B5D-3999-B92B-375DD99FE787
   Functions: 147
   Symbols:   156
   CStrings:  214

```

#### maild

>  `/System/Library/PrivateFrameworks/EmailDaemon.framework/maild`

```diff

-3826.400.131.2.14
+3826.400.131.2.15
   __TEXT.__text: 0xbd554
   __TEXT.__auth_stubs: 0x1230
   __TEXT.__objc_stubs: 0x16300

   __TEXT.__const: 0x1d0
   __TEXT.__oslogstring: 0x927e
   __TEXT.__ustring: 0x72
-  __TEXT.__info_plist: 0x581
+  __TEXT.__info_plist: 0x586
   __TEXT.__unwind_info: 0x6828
   __DATA_CONST.__auth_got: 0x928
   __DATA_CONST.__got: 0x1210

   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libc++.1.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: 91C6DFCD-CB77-3120-B94A-9013852694E4
+  UUID: A6F2C8D2-A404-3ED3-B2AC-C134F531877A
   Functions: 4070
   Symbols:   899
   CStrings:  8189

```

#### SearchIndexer

>  `/System/Library/PrivateFrameworks/Message.framework/XPCServices/SearchIndexer.xpc/SearchIndexer`

```diff

-3826.400.131.2.14
-  __TEXT.__text: 0x5de424
+3826.400.131.2.15
+  __TEXT.__text: 0x5e1c3c
   __TEXT.__auth_stubs: 0x4390
   __TEXT.__objc_stubs: 0x140
   __TEXT.__objc_methlist: 0x198
-  __TEXT.__cstring: 0x8e89
+  __TEXT.__cstring: 0x8e59
   __TEXT.__swift5_entry: 0x8
-  __TEXT.__const: 0x42ff0
+  __TEXT.__const: 0x43040
   __TEXT.__swift5_typeref: 0xe1f9
   __TEXT.__swift5_capture: 0x7edc
-  __TEXT.__constg_swiftt: 0xb91c
+  __TEXT.__constg_swiftt: 0xb908
   __TEXT.__swift5_reflstr: 0xd5a9
   __TEXT.__swift5_fieldmd: 0x12160
   __TEXT.__swift5_proto: 0x2398
   __TEXT.__swift5_types: 0x1434
   __TEXT.__swift5_assocty: 0x1620
-  __TEXT.__oslogstring: 0xeb80
+  __TEXT.__oslogstring: 0xeb20
   __TEXT.__swift5_builtin: 0xb18
   __TEXT.__swift5_mpenum: 0x7f8
   __TEXT.__swift5_protos: 0x74

   __TEXT.__objc_methtype: 0x3e5
   __TEXT.__gcc_except_tab: 0x10c
   __TEXT.__unwind_info: 0x130a8
-  __TEXT.__eh_frame: 0x193a0
+  __TEXT.__eh_frame: 0x19368
   __DATA_CONST.__auth_got: 0x21d8
   __DATA_CONST.__got: 0xb40
-  __DATA_CONST.__auth_ptr: 0x3050
-  __DATA_CONST.__const: 0x48770
+  __DATA_CONST.__auth_ptr: 0x3058
+  __DATA_CONST.__const: 0x486e0
   __DATA_CONST.__cfstring: 0x20
-  __DATA_CONST.__objc_classlist: 0x1a0
+  __DATA_CONST.__objc_classlist: 0x198
   __DATA_CONST.__objc_catlist: 0x8
   __DATA_CONST.__objc_protolist: 0x100
   __DATA_CONST.__objc_imageinfo: 0x8
   __DATA_CONST.__objc_protorefs: 0x80
-  __DATA.__objc_const: 0x4c20
+  __DATA.__objc_const: 0x4b90
   __DATA.__objc_selrefs: 0x798
-  __DATA.__objc_data: 0x980
-  __DATA.__data: 0x11de8
+  __DATA.__objc_data: 0x930
+  __DATA.__data: 0x11e58
   __DATA.__bss: 0x45dc0
-  __DATA.__common: 0xcf8
+  __DATA.__common: 0xce8
   - /System/Library/Frameworks/Accounts.framework/Accounts
   - /System/Library/Frameworks/Contacts.framework/Contacts
   - /System/Library/Frameworks/CoreData.framework/CoreData

   - /usr/lib/swift/libswiftos.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: E1584255-7FB2-3105-93E4-3D306DC172C9
-  Functions: 29355
+  UUID: EDDE4E6D-1A2C-391E-8E0E-BC11A8BF0D1E
+  Functions: 29368
   Symbols:   446
-  CStrings:  2988
+  CStrings:  2985
 
CStrings:
+ "[%.*hhx] Did mark %ld more mailboxes as sync complete."
+ "[%.*hhx] [{%.*hx}-%{sensitive,mask.mailbox}s] Did mark as sync complete."
- "[%.*hhx-%{public}s] %{sensitive,mask.mailbox}s ."
- "[%.*hhx-%{public}s] Did mark %ld more mailboxes as sync complete."
- "[%.*hhx-%{public}s] [{%.*hx}-%{sensitive,mask.mailbox}s] Did mark as sync complete."
- "_TtCV13IMAP2Behavior5State6Logger"
- "l"

```

#### MobileMail

>  `/private/var/staged_system_apps/MobileMail.app/MobileMail`

```diff

-3826.400.131.2.14
+3826.400.131.2.15
   __TEXT.__text: 0x45b5a4
   __TEXT.__auth_stubs: 0x6180
   __TEXT.__objc_stubs: 0x40600

   __TEXT.__eh_frame: 0x2910
   __DATA_CONST.__auth_got: 0x30d0
   __DATA_CONST.__got: 0x3768
-  __DATA_CONST.__auth_ptr: 0x1ed8
+  __DATA_CONST.__auth_ptr: 0x1e28
   __DATA_CONST.__const: 0x15490
   __DATA_CONST.__cfstring: 0xe4c0
   __DATA_CONST.__objc_classlist: 0xe00

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: AEDAC9DC-A89E-377D-9924-E7EC23BB40B4
+  UUID: 3B828154-3F1A-31B9-926E-1189B3CC8DC8
   Functions: 20689
   Symbols:   4081
   CStrings:  22919

```

#### SafariWidgetExtension

>  `/private/var/staged_system_apps/MobileSafari.app/PlugIns/SafariWidgetExtension.appex/SafariWidgetExtension`

```diff

-7620.2.4.10.7
+7620.2.4.10.8
   __TEXT.__text: 0x4bcac
   __TEXT.__auth_stubs: 0x1560
   __TEXT.__cstring: 0x308a

   __TEXT.__eh_frame: 0x1dac
   __DATA_CONST.__auth_got: 0xab0
   __DATA_CONST.__got: 0x548
-  __DATA_CONST.__auth_ptr: 0xc90
+  __DATA_CONST.__auth_ptr: 0xc88
   __DATA_CONST.__const: 0x1778
   __DATA_CONST.__objc_classlist: 0x8
   __DATA_CONST.__objc_imageinfo: 0x8

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 1A97F2DD-729D-39A9-8F35-2880348ED896
+  UUID: 60F259F1-4276-32F3-8354-DD877AD8F357
   Functions: 2039
   Symbols:   137
   CStrings:  279

```

#### AuthenticationServicesAgent

>  `/usr/libexec/AuthenticationServicesAgent`

```diff

-7620.2.4.10.7
+7620.2.4.10.8
   __TEXT.__text: 0x143b8
   __TEXT.__auth_stubs: 0x1000
   __TEXT.__objc_stubs: 0x1d00

   __TEXT.__swift5_proto: 0xc
   __TEXT.__swift5_types: 0x4
   __TEXT.__swift5_capture: 0x24
-  __TEXT.__info_plist: 0x62b
+  __TEXT.__info_plist: 0x630
   __TEXT.__unwind_info: 0x350
   __TEXT.__eh_frame: 0x80
   __DATA_CONST.__auth_got: 0x810

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: EF98BD34-219C-3CD2-A31C-05DAC23A5F76
+  UUID: 8F09A997-C199-35C4-98E1-47977BBE9F7F
   Functions: 297
   Symbols:   456
   CStrings:  590

```

#### com.apple.Safari.History

>  `/usr/libexec/com.apple.Safari.History`

```diff

-7620.2.4.10.7
+7620.2.4.10.8
   __TEXT.__text: 0x44
   __TEXT.__auth_stubs: 0x30
-  __TEXT.__info_plist: 0x6f0
+  __TEXT.__info_plist: 0x6f5
   __TEXT.SandboxProfile: 0x15ac
   __TEXT.__unwind_info: 0x58
   __DATA_CONST.__auth_got: 0x18

   - /System/Library/PrivateFrameworks/SafariShared.framework/SafariShared
   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: B2106E4E-0825-35BC-AA5D-E62D7C9B8570
+  UUID: 2A028A41-BD12-3730-B149-717F023872C4
   Functions: 1
   Symbols:   5
   CStrings:  0

```

#### mobileactivationd

>  `/usr/libexec/mobileactivationd`

```diff

-1015.60.1.0.0
-  __TEXT.__text: 0x1fdb78
+1015.82.2.0.0
+  __TEXT.__text: 0x1fdedc
   __TEXT.__auth_stubs: 0x10a0
   __TEXT.__objc_stubs: 0x2ec0
   __TEXT.__objc_methlist: 0xa80
   __TEXT.__const: 0x46351
-  __TEXT.__cstring: 0xd7fb
+  __TEXT.__cstring: 0xd8b7
   __TEXT.__objc_methname: 0x3ce7
   __TEXT.__oslogstring: 0xe5a
   __TEXT.__objc_classname: 0x1b4

   __TEXT.__dlopen_cstrs: 0x24c
   __TEXT.__ustring: 0x4
   __TEXT.__info_plist: 0x109
-  __TEXT.__unwind_info: 0x1118
+  __TEXT.__unwind_info: 0x1120
   __TEXT.__eh_frame: 0x1108
   __DATA_CONST.__auth_got: 0x860
   __DATA_CONST.__got: 0x488
   __DATA_CONST.__auth_ptr: 0x40
   __DATA_CONST.__const: 0xdf30
-  __DATA_CONST.__cfstring: 0xc020
+  __DATA_CONST.__cfstring: 0xc0e0
   __DATA_CONST.__objc_classlist: 0x50
   __DATA_CONST.__objc_catlist: 0x18
   __DATA_CONST.__objc_protolist: 0x48

   __DATA_CONST.__objc_protorefs: 0x8
   __DATA_CONST.__objc_superrefs: 0x40
   __DATA_CONST.__objc_intobj: 0x258
-  __DATA_CONST.__objc_arraydata: 0x450
+  __DATA_CONST.__objc_arraydata: 0x458
   __DATA_CONST.__objc_arrayobj: 0x90
   __DATA.__objc_const: 0x23c8
   __DATA.__objc_selrefs: 0xd50

   - /usr/lib/libSystem.B.dylib
   - /usr/lib/liblockdown.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: D61474CD-664C-3DC3-AB2A-0ADB7E6474C2
-  Functions: 1297
-  Symbols:   9161
-  CStrings:  4335
+  UUID: D94C72F8-F316-3335-83B4-0693FBCBF8A5
+  Functions: 1300
+  Symbols:   9176
+  CStrings:  4350
 
Symbols:
+ /AppleInternal/Library/BuildRoots/ab3efd37-e438-11ef-ae41-de23e2c06a38/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/amd/libDER.a(DER_Decode.o)
+ /AppleInternal/Library/BuildRoots/ab3efd37-e438-11ef-ae41-de23e2c06a38/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libCoreTrust.a(CMS.o)
+ /AppleInternal/Library/BuildRoots/ab3efd37-e438-11ef-ae41-de23e2c06a38/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libCoreTrust.a(CTEvaluate.o)
+ /AppleInternal/Library/BuildRoots/ab3efd37-e438-11ef-ae41-de23e2c06a38/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libCoreTrust.a(CTEvaluateBAA.o)
+ /AppleInternal/Library/BuildRoots/ab3efd37-e438-11ef-ae41-de23e2c06a38/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libCoreTrust.a(CryptoUtils.o)
+ /AppleInternal/Library/BuildRoots/ab3efd37-e438-11ef-ae41-de23e2c06a38/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libCoreTrust.a(DERUtils.o)
+ /AppleInternal/Library/BuildRoots/ab3efd37-e438-11ef-ae41-de23e2c06a38/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libCoreTrust.a(X509Certificate.o)
+ /AppleInternal/Library/BuildRoots/ab3efd37-e438-11ef-ae41-de23e2c06a38/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libCoreTrust.a(X509Chain.o)
+ /AppleInternal/Library/BuildRoots/ab3efd37-e438-11ef-ae41-de23e2c06a38/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libCoreTrust.a(X509Policy.o)
+ /AppleInternal/Library/BuildRoots/ab3efd37-e438-11ef-ae41-de23e2c06a38/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libaks.a(acl_keys.o)
+ /AppleInternal/Library/BuildRoots/ab3efd37-e438-11ef-ae41-de23e2c06a38/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libaks.a(aks_pack.o)
+ /AppleInternal/Library/BuildRoots/ab3efd37-e438-11ef-ae41-de23e2c06a38/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libaks.a(der_utils.o)
+ /AppleInternal/Library/BuildRoots/ab3efd37-e438-11ef-ae41-de23e2c06a38/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libaks.a(firebloom_hacks.o)
+ /AppleInternal/Library/BuildRoots/ab3efd37-e438-11ef-ae41-de23e2c06a38/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libaks.a(libaks_client.o)
+ /AppleInternal/Library/BuildRoots/ab3efd37-e438-11ef-ae41-de23e2c06a38/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libaks.a(libaks_internal.o)
+ /AppleInternal/Library/BuildRoots/ab3efd37-e438-11ef-ae41-de23e2c06a38/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libaks.a(libaks_ref_key.o)
+ GCC_except_table25
+ __block_literal_global.203
+ _validateCertificateOID
+ _validateCertificateOIDArray
+ _validateOIDKeyUsageProperties
- /AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/amd/libDER.a(DER_Decode.o)
- /AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libCoreTrust.a(CMS.o)
- /AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libCoreTrust.a(CTEvaluate.o)
- /AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libCoreTrust.a(CTEvaluateBAA.o)
- /AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libCoreTrust.a(CryptoUtils.o)
- /AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libCoreTrust.a(DERUtils.o)
- /AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libCoreTrust.a(X509Certificate.o)
- /AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libCoreTrust.a(X509Chain.o)
- /AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libCoreTrust.a(X509Policy.o)
- /AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libaks.a(acl_keys.o)
- /AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libaks.a(aks_pack.o)
- /AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libaks.a(der_utils.o)
- /AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libaks.a(firebloom_hacks.o)
- /AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libaks.a(libaks_client.o)
- /AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libaks.a(libaks_internal.o)
- /AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/lib/libaks.a(libaks_ref_key.o)
- GCC_except_table22
- __block_literal_global.185
CStrings:
+ "1015.82.2"
+ "5"
+ "Absinthe/2.0 iOS Device Activator (MobileActivation-1015.82.2 built on Mar  5 2025 at 03:06:41)"
+ "Empty OID list."
+ "Failed to query OID %@."
+ "Failed to validate %@."
+ "Failed to validate OID %@."
+ "Failed to validate OID(s): %@"
+ "Missing 'sepClient' property."
+ "iOS Device Activator (MobileActivation-1015.82.2)"
+ "validateCertificateOID"
+ "validateCertificateOIDArray"
+ "validateOIDKeyUsageProperties"
- "1015.60.1"
- "Absinthe/2.0 iOS Device Activator (MobileActivation-1015.60.1 built on Jan 16 2025 at 03:56:05)"
- "Existing %@ is missing required OID(s) (%@)."
- "iOS Device Activator (MobileActivation-1015.60.1)"

```

#### passwordbreachd

>  `/usr/libexec/passwordbreachd`

```diff

-7620.2.4.10.7
+7620.2.4.10.8
   __TEXT.__text: 0x6c
   __TEXT.__auth_stubs: 0x50
-  __TEXT.__info_plist: 0x5d7
+  __TEXT.__info_plist: 0x5dc
   __TEXT.__unwind_info: 0x58
   __DATA_CONST.__auth_got: 0x28
   __DATA_CONST.__got: 0x10

   - /System/Library/PrivateFrameworks/SafariShared.framework/SafariShared
   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: 6C8AD77D-7401-3785-A8D6-58BC60524D4C
+  UUID: 4BD8322E-1766-36B3-BE71-85E755CF1310
   Functions: 1
   Symbols:   9
   CStrings:  0

```

#### safarifetcherd

>  `/usr/libexec/safarifetcherd`

```diff

-7620.2.4.10.7
+7620.2.4.10.8
   __TEXT.__text: 0x9c1c
   __TEXT.__auth_stubs: 0x7e0
   __TEXT.__objc_stubs: 0x2420

   __TEXT.__objc_methtype: 0x2358
   __TEXT.__oslogstring: 0xfe8
   __TEXT.__dlopen_cstrs: 0x4e
-  __TEXT.__info_plist: 0x580
+  __TEXT.__info_plist: 0x587
   __TEXT.__unwind_info: 0x498
   __DATA_CONST.__auth_got: 0x408
   __DATA_CONST.__got: 0x2b8

   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libc++.1.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: 5C5DD0BB-84DF-348B-B5B3-1B6E25A06ADC
+  UUID: 055A36CC-E448-3902-A184-318F8A4FB3FE
   Functions: 261
   Symbols:   226
   CStrings:  1037

```

#### webbookmarksd

>  `/usr/libexec/webbookmarksd`

```diff

-7620.2.4.10.7
+7620.2.4.10.8
   __TEXT.__text: 0x15728
   __TEXT.__auth_stubs: 0x9b0
   __TEXT.__objc_stubs: 0x3300

   __TEXT.__oslogstring: 0x1fb6
   __TEXT.__objc_classname: 0x271
   __TEXT.__objc_methtype: 0x614
-  __TEXT.__info_plist: 0x57d
+  __TEXT.__info_plist: 0x584
   __TEXT.__unwind_info: 0x628
   __DATA_CONST.__auth_got: 0x4f0
   __DATA_CONST.__got: 0x620

   - /usr/lib/libc++.1.dylib
   - /usr/lib/liblockdown.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: 34C9262A-E9D0-3321-B220-68D7E74966E5
+  UUID: CFBEC373-043E-3CEC-AFFF-B7189DD1266C
   Functions: 455
   Symbols:   365
   CStrings:  937

```

#### webinspectord

>  `/usr/libexec/webinspectord`

```diff

-7620.2.4.10.7
+7620.2.4.10.8
   __TEXT.__text: 0x994
   __TEXT.__auth_stubs: 0x270
   __TEXT.__objc_stubs: 0xa0

   __TEXT.__swift5_fieldmd: 0x10
   __TEXT.__swift5_capture: 0x10
   __TEXT.__swift5_types: 0x4
-  __TEXT.__info_plist: 0x522
+  __TEXT.__info_plist: 0x527
   __TEXT.__unwind_info: 0xb0
   __DATA_CONST.__auth_got: 0x140
   __DATA_CONST.__got: 0x38

   - /usr/lib/swift/libswiftos.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 4466CE98-91B0-3530-B952-21F9DC3B9E74
+  UUID: BA1CB955-87DE-3437-8FE5-F4DF32AFA928
   Functions: 19
   Symbols:   76
   CStrings:  23

```


</details>

### iBoot

| iOS | Version |
| :-- | :------ |
| 18.3.1 *(22D72)* | iBoot-11881.80.57 |
| 18.3.2 *(22D82)* | iBoot-11881.80.57 |

## DSC

### WebKit

| iOS | Version |
| :-- | :------ |
| 18.3.1 *(22D72)* | 620.2.4.10.7 |
| 18.3.2 *(22D82)* | 620.2.4.10.8 |

### Dylibs

#### ⬆️ Updated (7)

<details>
  <summary><i>View Updated</i></summary>

#### _AuthenticationServices_SwiftUI

>  `/System/Library/Frameworks/_AuthenticationServices_SwiftUI.framework/_AuthenticationServices_SwiftUI`

```diff

-620.2.4.10.7
+620.2.4.10.8
   __TEXT.__text: 0xd95c
   __TEXT.__auth_stubs: 0xa30
   __TEXT.__objc_methlist: 0x190

   __DATA_CONST.__objc_selrefs: 0xf8
   __DATA_CONST.__objc_protorefs: 0x40
   __AUTH_CONST.__auth_got: 0x518
-  __AUTH_CONST.__auth_ptr: 0x408
+  __AUTH_CONST.__auth_ptr: 0x410
   __AUTH_CONST.__const: 0xbb8
   __AUTH_CONST.__objc_const: 0x958
   __AUTH.__objc_data: 0x478

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 41BED8ED-7BFF-3AB4-9B8C-9CC50CA7373A
+  UUID: 9BE599BC-C7BA-39EA-9ADF-307C87626DD2
   Functions: 530
   Symbols:   440
   CStrings:  135

```

#### AuthenticationServicesCore

>  `/System/Library/PrivateFrameworks/AuthenticationServicesCore.framework/AuthenticationServicesCore`

```diff

-620.2.4.10.7
+620.2.4.10.8
   __TEXT.__text: 0xb990c
   __TEXT.__auth_stubs: 0x21e0
   __TEXT.__objc_methlist: 0x2758

   __DATA_CONST.__objc_superrefs: 0xf0
   __DATA_CONST.__objc_arraydata: 0x10
   __AUTH_CONST.__auth_got: 0x1100
-  __AUTH_CONST.__auth_ptr: 0x6d8
+  __AUTH_CONST.__auth_ptr: 0x6f8
   __AUTH_CONST.__const: 0x56c0
   __AUTH_CONST.__cfstring: 0x1e40
   __AUTH_CONST.__objc_const: 0x7c08

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: BD1E6B7C-EF1C-3D45-9146-30334DA50736
+  UUID: E73EA684-EFE1-3D28-A8AD-89A90313F566
   Functions: 4430
   Symbols:   4839
   CStrings:  2557

```

#### DeviceIdentity

>  `/System/Library/PrivateFrameworks/DeviceIdentity.framework/DeviceIdentity`

```diff

-1015.60.1.0.0
+1015.82.2.0.0
   __TEXT.__text: 0x1b4ec
   __TEXT.__auth_stubs: 0x880
   __TEXT.__objc_methlist: 0x1f4

   __DATA_CONST.__objc_selrefs: 0x490
   __DATA_CONST.__objc_protorefs: 0x8
   __DATA_CONST.__objc_superrefs: 0x8
-  __DATA_CONST.__objc_arraydata: 0x448
+  __DATA_CONST.__objc_arraydata: 0x450
   __AUTH_CONST.__auth_got: 0x450
   __AUTH_CONST.__auth_ptr: 0x10
   __AUTH_CONST.__const: 0x100

   - /usr/lib/libMobileGestalt.dylib
   - /usr/lib/libSystem.B.dylib
   - /usr/lib/libobjc.A.dylib
-  UUID: 4EF03DF7-E49F-3617-8236-644E8A7CF412
+  UUID: 3C940CD2-7728-36C2-83BD-B27C06A73AF9
   Functions: 244
   Symbols:   1186
   CStrings:  1388
CStrings:
+ "iOS Device Activator (MobileActivation-1015.82.2)"
- "iOS Device Activator (MobileActivation-1015.60.1)"

```

#### Message

>  `/System/Library/PrivateFrameworks/Message.framework/Message`

```diff

-3826.400.131.2.14
-  __TEXT.__text: 0xb7c39c
+3826.400.131.2.15
+  __TEXT.__text: 0xb7fda8
   __TEXT.__auth_stubs: 0x7df0
   __TEXT.__objc_methlist: 0x11ab4
   __TEXT.__gcc_except_tab: 0x386e8
-  __TEXT.__const: 0x4ac40
-  __TEXT.__cstring: 0x3016e
-  __TEXT.__oslogstring: 0x24300
+  __TEXT.__const: 0x4ac90
+  __TEXT.__cstring: 0x3012e
+  __TEXT.__oslogstring: 0x242a0
   __TEXT.__ustring: 0x23ca
   __TEXT.__swift5_typeref: 0x12311
   __TEXT.__swift5_capture: 0x31370
-  __TEXT.__constg_swiftt: 0xd6f8
+  __TEXT.__constg_swiftt: 0xd6e4
   __TEXT.__swift5_builtin: 0xdac
   __TEXT.__swift5_reflstr: 0xea79
   __TEXT.__swift5_fieldmd: 0x14888

   __TEXT.__swift5_protos: 0x74
   __TEXT.__swift5_mpenum: 0x7f0
   __TEXT.__unwind_info: 0x23e10
-  __TEXT.__eh_frame: 0x1e560
+  __TEXT.__eh_frame: 0x1e528
   __TEXT.__objc_classname: 0x2a4e
   __TEXT.__objc_methname: 0x2e581
   __TEXT.__objc_methtype: 0x67df
   __TEXT.__objc_stubs: 0x24660
   __DATA_CONST.__got: 0x2c80
   __DATA_CONST.__const: 0x15600
-  __DATA_CONST.__objc_classlist: 0xb38
+  __DATA_CONST.__objc_classlist: 0xb30
   __DATA_CONST.__objc_catlist: 0x68
   __DATA_CONST.__objc_protolist: 0x550
   __DATA_CONST.__objc_imageinfo: 0x8

   __DATA_CONST.__objc_superrefs: 0x680
   __DATA_CONST.__objc_arraydata: 0xf58
   __AUTH_CONST.__auth_got: 0x3f10
-  __AUTH_CONST.__auth_ptr: 0x3170
-  __AUTH_CONST.__const: 0xa5e88
+  __AUTH_CONST.__auth_ptr: 0x3168
+  __AUTH_CONST.__const: 0xa5df8
   __AUTH_CONST.__cfstring: 0x184a0
-  __AUTH_CONST.__objc_const: 0x26ec0
+  __AUTH_CONST.__objc_const: 0x26e30
   __AUTH_CONST.__objc_arrayobj: 0xb88
   __AUTH_CONST.__objc_intobj: 0xa08
   __AUTH_CONST.__objc_dictobj: 0x78
-  __AUTH.__objc_data: 0x5298
-  __AUTH.__data: 0xaf60
+  __AUTH.__objc_data: 0x5248
+  __AUTH.__data: 0xafc0
   __DATA.__objc_ivar: 0x13a4
-  __DATA.__data: 0xe920
+  __DATA.__data: 0xe930
   __DATA.__crash_info: 0x40
   __DATA.__bss: 0x4e518
-  __DATA.__common: 0xf48
+  __DATA.__common: 0xf38
   __DATA_DIRTY.__objc_data: 0x1900
   __DATA_DIRTY.__data: 0x18
   __DATA_DIRTY.__bss: 0x410

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: E01C656F-3AFF-39F8-AA3B-3B79462AA3AF
-  Functions: 54937
-  Symbols:   43334
-  CStrings:  20319
+  UUID: 3AAFF7D7-ACAF-370B-9B13-0C989720D679
+  Functions: 54952
+  Symbols:   43329
+  CStrings:  20316
 
Symbols:
+ _symbolic _____ 13IMAP2Behavior5StateV6LoggerV
- __DATA__TtCV13IMAP2Behavior5State6Logger
- __IVARS__TtCV13IMAP2Behavior5State6Logger
- __METACLASS_DATA__TtCV13IMAP2Behavior5State6Logger
- ___swift_memcpy312_8
- _symbolic _____ 13IMAP2Behavior5StateV6LoggerC
CStrings:
+ "[%.*hhx] Did mark %ld more mailboxes as sync complete."
+ "[%.*hhx] [{%.*hx}-%{sensitive,mask.mailbox}s] Did mark as sync complete."
- "[%.*hhx-%{public}s] %{sensitive,mask.mailbox}s ."
- "[%.*hhx-%{public}s] Did mark %ld more mailboxes as sync complete."
- "[%.*hhx-%{public}s] [{%.*hx}-%{sensitive,mask.mailbox}s] Did mark as sync complete."
- "_TtCV13IMAP2Behavior5State6Logger"
- "l"

```

#### MobileSafari

>  `/System/Library/PrivateFrameworks/MobileSafari.framework/MobileSafari`

```diff

-620.2.4.10.7
+620.2.4.10.8
   __TEXT.__text: 0x3a2418
   __TEXT.__auth_stubs: 0x4b50
   __TEXT.__objc_methlist: 0x12388

   __DATA_CONST.__objc_superrefs: 0x6a0
   __DATA_CONST.__objc_arraydata: 0x258
   __AUTH_CONST.__auth_got: 0x25c0
-  __AUTH_CONST.__auth_ptr: 0x2050
+  __AUTH_CONST.__auth_ptr: 0x1dd8
   __AUTH_CONST.__const: 0x13270
   __AUTH_CONST.__cfstring: 0x86e0
   __AUTH_CONST.__objc_const: 0x330d8

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: AEBAC6EB-7F0D-3004-A42B-759AE3526BFB
+  UUID: 52D21FC9-C3C0-36DB-ABB1-EE209C19491D
   Functions: 18338
   Symbols:   28335
   CStrings:  14478

```

#### PasswordManagerUI

>  `/System/Library/PrivateFrameworks/PasswordManagerUI.framework/PasswordManagerUI`

```diff

-7620.2.4.10.7
+7620.2.4.10.8
   __TEXT.__text: 0x46129c
   __TEXT.__auth_stubs: 0x5e70
   __TEXT.__objc_methlist: 0x1508

   __DATA_CONST.__objc_protorefs: 0x100
   __DATA_CONST.__objc_superrefs: 0x20
   __AUTH_CONST.__auth_got: 0x2f48
-  __AUTH_CONST.__auth_ptr: 0x4418
+  __AUTH_CONST.__auth_ptr: 0x4000
   __AUTH_CONST.__const: 0x14508
   __AUTH_CONST.__cfstring: 0x4c0
   __AUTH_CONST.__objc_const: 0xa468

   - /usr/lib/swift/libswiftsimd.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: 53F19AC3-10D2-313B-A514-8F232C591C89
+  UUID: 20E26E8C-D996-35D3-98EB-4E6B4C2F54B0
   Functions: 18192
   Symbols:   8065
   CStrings:  3471

```

#### WebCore

>  `/System/Library/PrivateFrameworks/WebCore.framework/WebCore`

```diff

-620.2.4.10.7
-  __TEXT.__text: 0x2b2a44c
+620.2.4.10.8
+  __TEXT.__text: 0x2b2a48c
   __TEXT.__auth_stubs: 0xcfb0
   __TEXT.__objc_methlist: 0x49c4
   __TEXT.__gcc_except_tab: 0x21980

   - /usr/lib/swift/libswiftos.dylib
   - /usr/lib/swift/libswiftsys_time.dylib
   - /usr/lib/swift/libswiftunistd.dylib
-  UUID: C9C6867B-968B-3F1C-A69B-CC0BFD96352C
+  UUID: 90659609-DA85-391B-B0DC-712012852624
   Functions: 118871
   Symbols:   261522
   CStrings:  33166
CStrings:
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/ARM64Assembler.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/AbstractSlotVisitorInlines.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/ArgList.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/ArrayBuffer.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/ArrayBufferView.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/DataView.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/DisallowVMEntry.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/ExceptionScope.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/ExecutableAllocator.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/GenericTypedArrayViewInlines.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/IndexingHeader.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/JSArray.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/JSArrayBufferViewInlines.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/JSCPtrTag.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/JSCast.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/JSObject.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/JSObjectInlines.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/MacroAssemblerARM64.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/SecureARM64EHashPinsInlines.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/WebKitAdditions/EventHandlerIOSTouch.cpp"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/CheckedRef.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/CompletionHandler.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/ConcurrentPtrHashSet.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/Deque.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/JSONValues.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/Markable.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/ObjectIdentifier.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/Ref.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/RefPtr.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/StdLibExtras.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/ThreadSafeWeakHashSet.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/ThreadSpecific.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/TrailingArray.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/TypeCasts.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/cf/TypeCastsCF.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/text/StringBuilder.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/text/StringConcatenate.h"
+ "/AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/text/StringImpl.h"
+ "void JSC::SecureARM64EHashPins::forEachPage(Function) [Function = (lambda at /AppleInternal/Library/BuildRoots/bec4bd69-fa04-11ef-b2a1-3e0a6b9ba2ed/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/SecureARM64EHashPinsInlines.h:65:17)]"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/ARM64Assembler.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/AbstractSlotVisitorInlines.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/ArgList.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/ArrayBuffer.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/ArrayBufferView.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/DataView.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/DisallowVMEntry.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/ExceptionScope.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/ExecutableAllocator.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/GenericTypedArrayViewInlines.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/IndexingHeader.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/JSArray.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/JSArrayBufferViewInlines.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/JSCPtrTag.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/JSCast.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/JSObject.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/JSObjectInlines.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/MacroAssemblerARM64.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/SecureARM64EHashPinsInlines.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/WebKitAdditions/EventHandlerIOSTouch.cpp"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/CheckedRef.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/CompletionHandler.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/ConcurrentPtrHashSet.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/Deque.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/JSONValues.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/Markable.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/ObjectIdentifier.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/Ref.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/RefPtr.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/StdLibExtras.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/ThreadSafeWeakHashSet.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/ThreadSpecific.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/TrailingArray.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/TypeCasts.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/cf/TypeCastsCF.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/text/StringBuilder.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/text/StringConcatenate.h"
- "/AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/usr/local/include/wtf/text/StringImpl.h"
- "void JSC::SecureARM64EHashPins::forEachPage(Function) [Function = (lambda at /AppleInternal/Library/BuildRoots/774ff07e-d344-11ef-9a16-36218cb420d5/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.3.Internal.sdk/System/Library/PrivateFrameworks/JavaScriptCore.framework/PrivateHeaders/SecureARM64EHashPinsInlines.h:65:17)]"

```


</details>

## EOF
