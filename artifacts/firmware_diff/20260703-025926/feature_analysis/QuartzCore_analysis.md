## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "21B75"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 23 (2 AI-authored, 21 auto-generated); comments: 8 (4 AI-authored, 4 auto-generated); across 4 function(s); verified persisted in .i64: 23 named variables, 13 comments.

## What this feature does

The updates to `QuartzCore` in version 17.1 (21B80) introduce enhanced display bandwidth management, improved frame rate throttling logic, and new diagnostic capabilities for display performance. The framework now includes more granular checks for display bandwidth limits, specifically regarding surface detachment and frame rate adjustments based on thermal, power, and accessibility states. Additionally, the update adds support for "Film Grain" scaling capabilities and integrates tailspin diagnostics to track display glitches.

## How is it implemented


### Decompilation at `0x184130d50`

```c
__int64 __fastcall `anonymous namespace'::check_capture_entitlements(
        __int64 this,
        audit_token_t *audit_token,
        int *int_a3,
        bool *flag_a4,
        bool *flag_a5,
        bool *flag_a6)
{
  __int16 n_v6; // w20
  __int128 n_v11; // q0
  unsigned int n_v12; // w24
  const audit_token_t *constauditto_v13; // x1
  const audit_token_t *constauditto_v14; // x1
  _anonymous_namespace_ *anonymousnam_v15; // x0
  unsigned int *unsignedint_v16; // x1
  unsigned int n_v17; // w2
  __int128 n_v18; // [xsp+0h] [xbp-60h] BYREF
  __int128 n_v19; // [xsp+10h] [xbp-50h]
  __int64 n_v20; // [xsp+28h] [xbp-38h]

  n_v20 = *MEMORY[0x1E6782818];
  if ( this )
  {
    n_v6 = (__int16)flag_a6;
    n_v11 = *(_OWORD *)(this + 16);
    n_v18 = *(_OWORD *)this;
    n_v19 = n_v11;
    audit_token->val[0] = 0;
    n_v12 = DWORD1(n_v19);
    if ( DWORD1(n_v19) != (unsigned int)MEMORY[0x186BCB5E0](this, audit_token, int_a3, flag_a4)
      && (CA::Render::Server::audit_token_cache_lookup((CA::Render::Server *)&n_v18, constauditto_v13) & 1) == 0 )
    {
      audit_token->val[0] = n_v12;
    }
    if ( (CA::Render::Server::audit_token_cache_lookup((CA::Render::Server *)&n_v18, constauditto_v13) & 8) != 0 )
    {
      *(_BYTE *)int_a3 = (n_v6 & 2) == 0;
      *flag_a4 = (n_v6 & 0x20) != 0;
    }
    this = CA::Render::Server::audit_token_cache_lookup((CA::Render::Server *)&n_v18, constauditto_v14);
    if ( (this & 0x800) != 0 )
      *flag_a5 = HIBYTE(n_v6) & 1;
  }
  if ( *MEMORY[0x1E6782818] != n_v20 )
  {
    anonymousnam_v15 = (_anonymous_namespace_ *)MEMORY[0x186BCAF30]();
    return `anonymous namespace'::get_max_context_level(anonymousnam_v15, unsignedint_v16, n_v17);
  }
  return this;
}
```

### Decompilation at `0x18420c9f4`

```c
__int64 __fastcall CA::WindowServer::IOMFBDisplay::minimum_frame_duration_changed(CA::WindowServer::IOMFBDisplay *this)
{
  __int64 vars8; // [xsp+18h] [xbp+8h]

  if ( (*((_DWORD *)this + 160) & 0x100) != 0 )
  {
    MEMORY[0x186BCBF00]((char *)this + 28256);
    CA::WindowServer::IOMFBDisplay::recompute_server_frame_interval_locked(this);
    MEMORY[0x186BCBF30]((char *)this + 28256);
  }
  if ( ((vars8 ^ (2 * vars8)) & 0x4000000000000000LL) != 0 )
    __break(0xC471u);
  return CA::WindowServer::Display::post_display_changed(this);
}
```

### Decompilation at `0x1840378ec`

```c
__int64 __fastcall CA::WindowServer::IOMFBDisplay::exceeds_disp_bandwidth_limits_p(
        CA::WindowServer::IOMFBDisplay *this,
        CA::WindowServer::Surface *surface,
        __int64 n_a3,
        const CA::Rect *constcarect_a4,
        const CA::Rect *constcarect_a5)
{
  _QWORD *qword_v11; // x24

  if ( (BYTE2(xmmword_1ED76D28C) & 1) != 0 )
    return 0;
  if ( *((_BYTE *)this + 27248) == 1 )
  {
    if ( (CA::WindowServer::IOMFBDisplay::detach_exceeds_display_bandwidth_limits_p(
            this,
            surface,
            constcarect_a4,
            constcarect_a5,
            constcarect_a5)
        & 1) != 0 )
      return 1;
    qword_v11 = (_QWORD *)*((_QWORD *)this + 5);
    if ( qword_v11 )
    {
      while ( !(*(unsigned int (__fastcall **)(_QWORD))(**(_QWORD **)(*qword_v11 + 96LL) + 688LL))(*(_QWORD *)(*qword_v11 + 96LL))
           || ((*(__int64 (__fastcall **)(_QWORD, CA::WindowServer::IOMFBDisplay *, CA::WindowServer::Surface *, __int64, const CA::Rect *, const CA::Rect *))(**(_QWORD **)(*qword_v11 + 96LL) + 696LL))(
                 *(_QWORD *)(*qword_v11 + 96LL),
                 this,
                 surface,
                 n_a3,
                 constcarect_a4,
                 constcarect_a5)
             & 1) == 0 )
      {
        qword_v11 = (_QWORD *)qword_v11[1];
        if ( !qword_v11 )
          return 0;
      }
      return 1;
    }
  }
  return 0;
}
```

### Decompilation at `0x184003ec8`

```c
__int64 __fastcall __CADeviceSupportsFilmGrain_block_invoke(__int64 n_a1, const __CFString *cfstr_a2)
{
  __int64 result; // x0

  result = CA::ScalerUtil::has_capability((CA::ScalerUtil *)&stru_1EF3B3900, cfstr_a2);
  CADeviceSupportsFilmGrain::has_capability = result;
  return result;
}
```

The implementation centers on the `CA::WindowServer::IOMFBDisplay` class, which manages display-specific hardware interactions. 

The bandwidth checking logic has been significantly expanded. The function `exceeds_disp_bandwidth_limits_p` now performs a multi-stage validation process. It first checks a global flag to determine if bandwidth checks are enabled. If enabled, it verifies if a surface detachment would exceed defined bandwidth thresholds by iterating through a linked list of display objects and invoking capability checks on each. This ensures that UI-related bandwidth and detachment-related bandwidth are strictly monitored against hardware limits.

The frame rate throttling logic has been updated to incorporate more environmental factors. The system now evaluates thermal state, low-power mode, and accessibility settings to dynamically adjust frame rate limits. This is supported by new diagnostic logging that tracks the specific reasons for throttling.

The `check_capture_entitlements` function has been updated to handle audit token caching more robustly. It uses a lookup mechanism to verify process entitlements, ensuring that capture operations are only permitted if the calling process has the necessary permissions, with specific flags for different capture modes.

Finally, the "Film Grain" support is implemented via a capability-check pattern, where the system queries the scaler utility to determine if the hardware supports film grain scaling, caching the result for subsequent operations.

## How to trigger this feature

- **Bandwidth Limits**: Triggered automatically by the WindowServer when surface configurations change or when a display detachment is requested. The system evaluates the current bandwidth usage against the hardware-defined limits.
- **Frame Rate Throttling**: Triggered by changes in the device's thermal state, toggling of Low Power Mode, or changes in accessibility settings that require frame rate adjustments.
- **Entitlement Checks**: Triggered whenever a process attempts to perform a screen capture or access sensitive display buffers, requiring the system to validate the process's audit token.

## Vulnerability Assessment

The changes in `QuartzCore` appear to be a mix of performance optimization and security hardening. The introduction of `check_capture_entitlements` and the refinement of audit token lookups suggest a tightening of the security boundary around screen capture and display buffer access. By explicitly checking entitlements and caching the results, the system reduces the risk of unauthorized processes accessing sensitive display data.

The bandwidth checking logic, while primarily for performance and stability, also acts as a safety mechanism to prevent hardware-level resource exhaustion. The addition of explicit "bail out" conditions and bounds checking (e.g., the "Out of bounds access" string) indicates a focus on memory safety and preventing potential overflows in complex rendering paths, such as cubic curve subdivision. These changes mitigate potential stability issues that could be leveraged for denial-of-service or, in extreme cases, memory corruption.

## Evidence

- **Strings**: `CA_DISABLE_BANDWIDTH_CHECK`, `Display %d gpBandwidth Exceeded`, `pos < (size ()) && "Out of bounds access"`, `Setting frame rate throttle=%i due to thermal=%i`.
- **Symbols**: `__ZN12_GLOBAL__N_126check_capture_entitlementsEP13audit_token_tRiRbS3_S3_j`, `__ZN2CA12WindowServer12IOMFBDisplay31exceeds_disp_bandwidth_limits_pEPNS0_7SurfaceEjPKNS_4RectES6_`.
- **Binary Diff**: Significant increase in `__TEXT` and `__DATA` segments, reflecting the addition of new logic for bandwidth management and diagnostic tracking.

## AI Prioritisation Scoring System

- **feature_analysis**
  - **Tier**: TIER_1
  - **Category**: security_hardening
  - **Reasoning**: The update introduces critical security boundary checks for screen capture entitlements and adds memory-safety bounds checking in rendering paths, alongside significant changes to hardware-level resource management.

