## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "\n                \thasReadMeSummary: %@\n                \thasReadMe: %@\n                \thasLicenseAgreement: %@\n                \thasIconImageName: %@\n                \thasIconImage: %@\n   `
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 55 (0 AI-authored, 55 auto-generated); comments: 15 (0 AI-authored, 15 auto-generated); across 15 function(s); verified persisted in .i64: 84 named variables, 15 comments.

## What this feature does

The `SoftwareUpdateServices` framework in iOS 17.1 introduces a new "Wombat" constraint monitoring system designed to manage disk space requirements for software updates. This feature replaces the previous `SUManagerClient`-centric update scheduling with a more sophisticated, constraint-aware approach.

The new system consists of two primary components:

1. **`SUInstallationConstraintMonitorWombat`**: A new class that monitors disk space constraints and manages the "wombat" flag (a boolean indicating whether sufficient space exists for an update). It tracks unsatisfied constraints, polls for constraint satisfaction, and responds to system notifications when the wombat state changes.

2. **`SUManagerClient`**: The updated client that now queries for mandatory software updates and schedules them with error handling. It has been enhanced to work with the new constraint monitoring system.

The feature also introduces a new `SUAutoInstallForecast` class that appears to predict auto-installation opportunities based on end dates and expiration logic.

## How is it implemented

```c
__int64 __fastcall -[SUAutoInstallFailureNotification .cxx_destruct](__int64 a1)
{
  return sub_1FF196BB8(a1 + 16, 0);
}

void *__fastcall -[SUAutoInstallForecast _isForecastExpired](void *a1)
{
  void *v2; // x2
  __int64 vars8; // [xsp+18h] [xbp+8h]

  v2 = objc_msgSend(a1, "suEndDate");
  if ( ((vars8 ^ (2 * vars8)) & 0x4000000000000000LL) != 0 )
    __break(0xC471u);
  return objc_msgSend(a1, "_isDateExpired:", v2);
}

__int64 __fastcall -[SUDownload isPromoted](__int64 a1)
{
  return *(unsigned __int8 *)(a1 + 32);
}

__int64 __fastcall -[SUDownload setPromoted:](__int64 result, __int64 a2, char a3)
{
  *(_BYTE *)(result + 32) = a3;
  return result;
}

void *__fastcall -[SUInstallationConstraintMonitorWombat _queue_pollSatisfied](__int64 a1)
{
  _BOOL8 v2; // x2
  __int64 vars8; // [xsp+18h] [xbp+8h]

  MEMORY[0x1FFA32750](*(_QWORD *)(a1 + 8));
  v2 = objc_msgSend(*(id *)(a1 + 48), "attributeForKey:", *(_QWORD *)off_236365720) == *(void **)off_236365858;
  if ( ((vars8 ^ (2 * vars8)) & 0x4000000000000000LL) != 0 )
    __break(0xC471u);
  return objc_msgSend((id)a1, "_set_queue_wombatEnabled:", v2);
}

void *__fastcall -[SUInstallationConstraintMonitorWombat _set_queue_wombatEnabled:](__int64 a1, __int64 a2, int a3)
{
  void *result; // x0
  __int64 v6; // x20
  __CFString *v7; // x8
  __int64 v8; // x0
  int v9; // [xsp+0h] [xbp-40h] BYREF
  __int64 v10; // [xsp+4h] [xbp-3Ch]
  __int16 v11; // [xsp+Ch] [xbp-34h]
  __CFString *v12; // [xsp+Eh] [xbp-32h]
  __int64 v13; // [xsp+18h] [xbp-28h]

  v13 = *(_QWORD *)off_2363657D0;
  result = (void *)MEMORY[0x1FFA32750](*(_QWORD *)(a1 + 8));
  if ( *(unsigned __int8 *)(a1 + 56) != a3 )
  {
    *(_BYTE *)(a1 + 56) = a3;
    v6 = SULogInstallConstraints(result);
    if ( (unsigned int)MEMORY[0x1FFA33220](v6, 0) )
    {
      if ( *(_BYTE *)(a1 + 56) )
        v7 = &stru_236376C70;
      else
        v7 = &stru_236376C50;
      v9 = 138412546;
      v10 = a1;
      v11 = 2112;
      v12 = v7;
      MEMORY[0x1FFA32C70](&dword_1FF153000, v6, 0, "%@ - is wombat constraint changed (satisfied? %@)", &v9, 22);
    }
    result = objc_msgSend(
               objc_msgSend((id)a1, "delegate"),
               "installationConstraintMonitor:constraintsDidChange:",
               a1,
               objc_msgSend((id)a1, "representedConstraints"));
  }
  if ( *(_QWORD *)off_2363657D0 != v13 )
  {
    v8 = MEMORY[0x1FFA32C40](result);
    return (void *)-[SUInstallationConstraintMonitorWombat unsatisfiedConstraints](v8);
  }
  return result;
}

__int64 -[SUInstallationConstraintMonitorWombat _wombatEnabledDidChange:].cold.1()
{
  __int64 v0; // x0
  __int64 result; // x0
  __int64 v2; // x0
  __int64 v3; // x1
  __int64 v4; // [xsp+18h] [xbp-8h]

  v0 = OUTLINED_FUNCTION_1();
  OUTLINED_FUNCTION_0_0("-[SUInstallationConstraintMonitorWombat _wombatEnabledDidChange:]", v0);
  result = MEMORY[0x1FFA32C60](&dword_1FF153000);
  if ( *(_QWORD *)off_2363657D0 != v4 )
  {
    v2 = MEMORY[0x1FFA32C40](result);
    return -[SUInstallationConstraintMonitorWombat _wombatEnabledDidChange:].cold.2(v2, v3);
  }
  return result;
}

__int64 -[SUInstallationConstraintMonitorWombat _wombatEnabledDidChange:].cold.2()
{
  __int64 v0; // x0
  __int64 result; // x0
  __int64 v2; // x0
  __int64 v3; // [xsp+18h] [xbp-8h]

  v0 = OUTLINED_FUNCTION_1();
  OUTLINED_FUNCTION_0_0("-[SUInstallationConstraintMonitorWombat _wombatEnabledDidChange:]", v0);
  result = MEMORY[0x1FFA32C60](&dword_1FF153000);
  if ( *(_QWORD *)off_2363657D0 != v3 )
  {
    v2 = MEMORY[0x1FFA32C40](result);
    return -[_SUInstallationConstraintBlockObserverToken initWithObserver:].cold.1(v2, v3);
  }
  return result;
}

__int64 __fastcall -[SUInstallationConstraintMonitorWombat initOnQueue:withDownload:](
        __int64 a1,
        __int64 a2,
        __int64 a3,
        __int64 a4)
{
  id *v7; // x0
  id *v8; // x19
  __int64 v10; // x0
  __int64 v11; // x1
  void *v12; // x2
  _QWORD v13[2]; // [xsp+0h] [xbp-40h] BYREF
  __int64 v14; // [xsp+10h] [xbp-30h] BYREF
  __int64 v15; // [xsp+18h] [xbp-28h]

  v15 = *(_QWORD *)off_2363657D0;
  MEMORY[0x1FFA32750](a3);
  v13[0] = a1;
  v13[1] = off_22FAC2B60;
  v7 = (id *)MEMORY[0x1FFA32F70](v13, 0x184F48978uLL, a3, 4096, a4);
  v8 = v7;
  if ( v7 )
  {
    *((_BYTE *)v7 + 56) = 0;
    v7[6] = 0;
    v7[6] = objc_msgSend(off_22FAC2888, "sharedInstance");
    v14 = *(_QWORD *)off_236365728;
    objc_msgSend(
      v8[6],
      "setAttribute:forKey:error:",
      objc_msgSend(off_22FAC2680, "arrayWithObjects:count:", &v14, 1),
      *(_QWORD *)off_236365718,
      0);
    objc_msgSend(
      objc_msgSend(off_22FAC2880, "defaultCenter"),
      "addObserver:selector:name:object:",
      v8,
      0x184F4B7D4uLL,
      *(_QWORD *)off_236365728,
      v8[6]);
    v7 = (id *)objc_msgSend(v8, "_queue_pollSatisfied");
  }
  if ( *(_QWORD *)off_2363657D0 == v15 )
    return (__int64)v8;
  v10 = MEMORY[0x1FFA32C40](v7);
  return -[SUInstallationConstraintMonitorWombat _wombatEnabledDidChange:](v10, v11, v12);
}

void *__fastcall -[SUInstallationConstraintMonitorWombat unsatisfiedConstraints](__int64 a1)
{
  __int64 vars8; // [xsp+18h] [xbp+8h]

  MEMORY[0x1FFA32750](*(_QWORD *)(a1 + 8));
  if ( !*(_BYTE *)(a1 + 56) )
    return 0;
  if ( ((vars8 ^ (2 * vars8)) & 0x4000000000000000LL) != 0 )
    __break(0xC471u);
  return objc_msgSend((id)a1, "representedConstraints");
}

void *__fastcall -[SUManagerClient currentAutoInstallOperationForecast:](void *a1, __int64 a2, __int64 a3)
{
  void *v6; // [xsp+0h] [xbp-90h]
  _QWORD v7[6]; // [xsp+10h] [xbp-80h] BYREF
  _QWORD v8[6]; // [xsp+40h] [xbp-50h] BYREF

  v6 = objc_msgSend(a1, "_bundleIdentifier");
  SULogInfo(&stru_23637B7F0);
  v8[0] = off_2363657B0;
  v8[1] = 3221225472LL;
  v8[2] = __55__SUManagerClient_currentAutoInstallOperationForecast___block_invoke;
  v8[3] = &unk_2363665E8;
  v8[4] = a1;
  v8[5] = a3;
  v7[0] = off_236

## AI Prioritisation Scoring System

No actionable methods or prioritisation targets identified for this component.

