## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "%@ not in metadata"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 8 (0 AI-authored, 8 auto-generated); comments: 10 (0 AI-authored, 10 auto-generated); across 10 function(s); verified persisted in .i64: 182 named variables, 10 comments.

## What this feature does

The `PeopleSuggester` framework is responsible for generating and managing intelligent suggestions for the Share Sheet in iOS, leveraging machine learning models to predict relevant contacts, apps, and messages based on user context. The update introduces significant changes to the configuration management and feature extraction pipeline, specifically adding support for contact embedding configurations and new feature extraction mechanisms.

## How is it implemented

```c
__int64 *+[_PSConfig _configs]()
{
  _QWORD v1[5]; // [xsp+8h] [xbp-28h] BYREF

  v1[0] = off_1DFB8DEE0;
  v1[1] = 3221225472LL;
  v1[2] = __21___PSConfig__configs__block_invoke;
  v1[3] = &__block_descriptor_40_e5_v8__0l;
  v1[4] = MEMORY[0x1A785BD50]();
  if ( _configs_onceToken != -1 )
    sub_1A5766180(&_configs_onceToken, v1);
  return &_configs_configs;
}

__int64 *__fastcall +[_PSConfig _loadPlistNamed:](__int64 n_a1)
{
  __int64 plistName; // x19
  __int64 n_v3; // x21
  __int64 n_v4; // x20
  void *void_v5; // x0
  void *void_v6; // x0
  void *void_v7; // x0
  void *plistPath; // x21
  __int64 n_v9; // x0
  __int64 n_v10; // x0
  void *void_v11; // x0
  void *void_v12; // x23
  __int64 n_v13; // x24
  __int64 n_v14; // x0
  __int64 n_v17; // [xsp+8h] [xbp-C8h] BYREF
  _OWORD n_v18[6]; // [xsp+10h] [xbp-C0h] BYREF
  __int128 n_v19; // [xsp+70h] [xbp-60h]
  __int128 n_v20; // [xsp+80h] [xbp-50h]
  __int128 n_v21; // [xsp+90h] [xbp-40h]
  __int64 vars8; // [xsp+D8h] [xbp+8h]

  plistName = MEMORY[0x1A785BEA0]();
  n_v3 = MEMORY[0x1A785BD50](n_a1);
  n_v4 = MEMORY[0x1A785BC20]();
  void_v5 = objc_msgSend(off_1D826AD98, "bundleForClass:", MEMORY[0x1A785BD10](n_v3));
  void_v6 = objc_msgSend((id)MEMORY[0x1A785BC50](void_v5), "URLForResource:withExtension:", plistName, &stru_1DFBA7370);
  void_v7 = objc_msgSend((id)MEMORY[0x1A785BC50](void_v6), "path");
  plistPath = (void *)MEMORY[0x1A785BC50](void_v7);
  n_v9 = MEMORY[0x1A785BDD0]();
  MEMORY[0x1A785BDC0](n_v9);
  n_v20 = 0u;
  n_v21 = 0u;
  n_v19 = 0u;
  memset(n_v18, 0, sizeof(n_v18));
  if ( (unsigned int)sub_1A5766880(objc_msgSend(plistPath, "fileSystemRepresentation"), n_v18) )
  {
    if ( (unsigned int)MEMORY[0x1A785C050](off_1DFB8DF28, 17) )
      +[_PSConfig _loadPlistNamed:].cold.3(plistName);
    goto LABEL_4;
  }
  if ( (__int64)n_v19 >= 4096
    && MEMORY[0x1A785BC50](objc_msgSend(off_1D826B458, "dictionaryWithPath:error:", plistPath, 0)) )
  {
    goto LABEL_5;
  }
  void_v11 = objc_msgSend((id)MEMORY[0x1A785BBE0](off_1D826ADA0), "initFileURLWithPath:", plistPath);
  if ( !void_v11 )
  {
    if ( (unsigned int)MEMORY[0x1A785C050](off_1DFB8DF28, 17) )
      +[_PSConfig _loadPlistNamed:].cold.1(plistName);
LABEL_4:
    if ( !(unsigned int)MEMORY[0x1A785B720]() )
      goto LABEL_5;
    goto LABEL_18;
  }
  n_v17 = 0;
  void_v12 = objc_msgSend((id)MEMORY[0x1A785BBE0](off_1D826AF30), "initWithContentsOfURL:error:", void_v11, &n_v17);
  n_v13 = MEMORY[0x1A785BFA0]();
  if ( void_v12 )
    goto LABEL_15;
  if ( (unsigned int)MEMORY[0x1A785C050](off_1DFB8DF28, 17) )
    +[_PSConfig _loadPlistNamed:].cold.2(plistName, n_v13);
  if ( !(unsigned int)MEMORY[0x1A785B720]() )
  {
LABEL_15:
    n_v14 = MEMORY[0x1A785BDE0]();
    MEMORY[0x1A785BDC0](n_v14);
LABEL_5:
    MEMORY[0x1A785BDB0]();
    n_v10 = sub_1A5766350(n_v4);
    MEMORY[0x1A785BD80](n_v10);
    if ( ((vars8 ^ (2 * vars8)) & 0x4000000000000000LL) != 0 )
      __break(0xC471u);
    JUMPOUT(0x1A785BC30LL);
  }
LABEL_18:
  MEMORY[0x1A785B820]();
  return +[_PSConfig _configs]();
}

void +[_PSConfig contactEmbeddingConfig]()
{
  __int64 vars8; // [xsp+8h] [xbp+8h]

  +[_PSConfig _configs]();
  if ( ((vars8 ^ (2 * vars8)) & 0x4000000000000000LL) != 0 )
    __break(0xC471u);
  JUMPOUT(0x1A785BE70LL);
}

void +[_PSConfig defaultConfig]()
{
  __int64 vars8; // [xsp+8h] [xbp+8h]

  +[_PSConfig _configs]();
  if ( ((vars8 ^ (2 * vars8)) & 0x4000000000000000LL) != 0 )
    __break(0xC471u);
  JUMPOUT(0x1A785BE70LL);
}

void +[_PSConfig messagesPinningConfig]()
{
  __int64 vars8; // [xsp+8h] [xbp+8h]

  +[_PSConfig _configs]();
  if ( ((vars8 ^ (2 * vars8)) & 0x4000000000000000LL) != 0 )
    __break(0xC471u);
  JUMPOUT(0x1A785BE70LL);
}

void +[_PSConfig vocab]()
{
  __int64 vars8; // [xsp+8h] [xbp+8h]

  +[_PSConfig _configs]();
  if ( ((vars8 ^ (2 * vars8)) & 0x4000000000000000LL) != 0 )
    __break(0xC471u);
  JUMPOUT(0x1A785BE70LL);
}

void __fastcall +[_PSFeaturePreprocessor extractFeatureValuesFromFeatureObjects:](__int64 a1)
{
  void *v2; // x19
  __int64 v3; // x21
  __int64 v4; // x0
  __int64 v5; // x19
  __int64 v6; // x0
  _QWORD v7[6]; // [xsp+0h] [xbp-50h] BYREF
  __int64 vars8; // [xsp+58h] [xbp+8h]

  v2 = (void *)MEMORY[0x1A785BEC0]();
  v3 = MEMORY[0x1A785BC50](objc_msgSend(off_1D826ADA8, "generalChannel"));
  if ( (unsigned int)MEMORY[0x1A785C050](v3, 2) )
    +[_PSFeaturePreprocessor extractFeatureValuesFromFeatureObjects:].cold.2(v3);
  MEMORY[0x1A785BDB0]();
  v4 = MEMORY[0x1A785BD30](off_1D826ADC8);
  v7[0] = off_1DFB8DEE0;
  v7[1] = 3221225472LL;
  v7[2] = __65___PSFeaturePreprocessor_extractFeatureValuesFromFeatureObjects___block_invoke;
  v7[3] = &unk_1DFB8F5C0;
  v7[5] = a1;
  v7[4] = MEMORY[0x1A785BE50](v4);
  MEMORY[0x1A785BD80](objc_msgSend(v2, "enumerateKeysAndObjectsUsingBlock:", v7));
  v5 = MEMORY[0x1A785BC50](objc_msgSend(off_1D826ADA8, "generalChannel"));
  if ( (unsigned int)MEMORY[0x1A785C050](v5, 2) )
    +[_PSFeaturePreprocessor extractFeatureValuesFromFeatureObjects:].cold.1(v5);
  v6 = MEMORY[0x1A785BD80]();
  MEMORY[0x1A785BE30](v6);
  if ( ((vars8 ^ (2 * vars8)) & 0x4000000000000000LL) != 0 )
    __break(0xC471u);
  JUMPOUT(0x1A785BC30LL);
}
```

The implementation shows a refactored configuration loading system. The `_PSConfig` class now manages multiple configuration types (contact embedding, default, messages pinning, vocab) through a centralized `_configs` dictionary. The `_loadPlistNamed:` method has been significantly enhanced to handle plist loading with proper error handling, file system representation checks, and dictionary loading. A new `contactEmbeddingConfig` method was added, indicating the introduction of contact embedding features. The `extractFeatureValuesFromFeatureObjects:` method now uses a block-based enumeration to extract feature values from feature objects, suggesting a more flexible feature extraction mechanism.

## How to trigger this feature

The feature is triggered when the Share Sheet is displayed and suggestions need to be generated. The configuration loading happens lazily through the `_configs` dictionary, which is populated by calling the appropriate config loading methods (`contactEmbeddingConfig`, `defaultConfig`, `messagesPinningConfig`, `vocab`). The

## AI Prioritisation Scoring System

No actionable methods or prioritisation targets identified for this component.

