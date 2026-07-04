## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "%@: Path (%@) dir-stat clone size (%lld) is greater than dir-stat physical size (%lld)"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 40 (0 AI-authored, 40 auto-generated); comments: 8 (0 AI-authored, 8 auto-generated); across 11 function(s); verified persisted in .i64: 149 named variables, 21 comments.

## What this feature does

The `spaceattributiond` binary is a system daemon responsible for tracking and managing space attribution (storage usage) for cloned files and directories on iOS devices. This feature was introduced in iOS 17.1 (Version 2) to enhance storage management capabilities, specifically focusing on:

1. **Clone Detection and Management**: The system now tracks "clone" relationships between files/directories (files that share the same data blocks). This is evident from the new strings like "dir-stat clone size", "clonePath", "clonesInfo", and the `SACloneInfo` class.

2. **Telemetry Reporting**: New telemetry strings such as "lastDailyActivitySentTelemetryDate", "lastUserSentTelemetryDate", and "daily-activity-time-info" indicate the system now reports space attribution activity to Apple's servers.

3. **Activity Tracking**: The feature tracks when users interact with cloned content, with strings like "isActivity" and "zeroSizeAppsFiltering" suggesting it monitors user behavior around duplicate content.

4. **Storage Optimization**: The feature appears to identify and potentially manage duplicate data to optimize storage usage, as suggested by the clone detection logic and size comparisons.

## How is it implemented

```c
void __cdecl dispatch_apply(size_t iterations, dispatch_queue_t queue, void *block)
{
  _dispatch_apply(iterations, queue, block);
}

bool __cdecl +[SACloneTreeWalker isNodeID:oldestForDStreamID:forVolPath:](
        id id_a1,
        SEL sel_a2,
        unsigned __int64 n_a3,
        unsigned __int64 n_a4,
        id id_a5)
{
  id id_v8; // x0
  int *int_v9; // x0
  __int64 n_v10; // x21
  NSObject *nsobject_v11; // x20
  bool flag_v12; // w20
  char *str_v13; // x0
  __int64 n_v14; // x0
  __int64 n_v15; // x22
  unsigned __int64 n_v16; // x23
  NSObject *nsobject_v17; // x21
  unsigned __int64 n_v18; // x27
  __int64 n_v19; // x13
  int n_v20; // w11
  __int64 n_v21; // x12
  char *str_v22; // x13
  __int64 n_v23; // x14
  bool flag_v24; // zf
  _QWORD n_v26[2]; // [xsp+8h] [xbp-908h] BYREF
  unsigned __int64 n_v27; // [xsp+18h] [xbp-8F8h]
  __int64 n_v28; // [xsp+20h] [xbp-8F0h]
  __int128 n_v29; // [xsp+28h] [xbp-8E8h] BYREF
  char *clone_map_buffer; // [xsp+38h] [xbp-8D8h]
  statfs statfs_buf; // [xsp+40h] [xbp-8D0h] BYREF

  id_v8 = objc_retain(id_a5);
  bzero(&statfs_buf, 0x878u);
  if ( statfs((const char *)objc_msgSend(objc_retainAutorelease(id_a5), "UTF8String"), &statfs_buf) )
  {
    int_v9 = __error();
    n_v10 = (unsigned int)*int_v9;
    nsobject_v11 = (NSObject *)objc_retainAutoreleasedReturnValue((id)SALog(int_v9));
    if ( os_log_type_enabled(nsobject_v11, OS_LOG_TYPE_ERROR) )
      sub_100041C24(n_v10, nsobject_v11);
LABEL_4:
    objc_release(nsobject_v11);
    flag_v12 = 0;
    goto LABEL_35;
  }
  str_v13 = (char *)malloc_type_malloc(0x1D4C0u, 0x1000040504FFAC1uLL);
  if ( !str_v13 )
  {
    nsobject_v11 = (NSObject *)objc_retainAutoreleasedReturnValue((id)SALog(0));
    if ( os_log_type_enabled(nsobject_v11, OS_LOG_TYPE_ERROR) )
      sub_100041C94(nsobject_v11);
    goto LABEL_4;
  }
  n_v26[0] = 0x100000001LL;
  clone_map_buffer = str_v13;
  n_v29 = xmmword_100050900;
  n_v27 = 0;
  n_v28 = 0;
  n_v26[1] = n_a4;
  HIDWORD(n_v29) = 120000;
  n_v14 = fsctl(statfs_buf.f_mntonname, 0xC0384A74, n_v26, 1u);
  if ( (_DWORD)n_v14 )
  {
    n_v15 = n_v14;
    n_v16 = -1;
LABEL_8:
    nsobject_v17 = (NSObject *)objc_retainAutoreleasedReturnValue((id)SALog(n_v14));
    if ( os_log_type_enabled(nsobject_v17, OS_LOG_TYPE_ERROR) )
      sub_100041AC4((char *)&n_v29 + 12, n_v15, nsobject_v17);
    objc_release(nsobject_v17);
  }
  else
  {
    n_v18 = 0;
    n_v16 = -1;
    while ( HIDWORD(n_v29) >= 0x18 )
    {
      if ( HIDWORD(n_v29) != 24 )
      {
        n_v19 = 0;
        n_v20 = 24;
        while ( *(_QWORD *)&clone_map_buffer[n_v19] == n_a4 )
        {
          n_v21 = *(_QWORD *)&clone_map_buffer[n_v19 + 16];
          if ( n_v21 )
          {
            str_v22 = &clone_map_buffer[n_v19 + 48];
            n_v23 = n_v21;
            while ( 1 )
            {
              n_v18 = *((_QWORD *)str_v22 - 3);
              if ( (*str_v22 & 1) == 0 && n_v18 < n_v16 )
              {
                n_v16 = *((_QWORD *)str_v22 - 3);
                if ( n_v18 < n_a3 )
                  break;
              }
              str_v22 += 32;
              if ( !--n_v23 )
                goto LABEL_26;
            }
            n_v16 = *((_QWORD *)str_v22 - 3);
            goto LABEL_29;
          }
LABEL_26:
          n_v19 = (unsigned int)(n_v20 + 32 * n_v21);
          n_v20 = n_v19 + 24;
          if ( n_v19 + 24 >= (unsigned __int64)HIDWORD(n_v29) )
            goto LABEL_16;
        }
        break;
      }
LABEL_16:
      n_v27 = n_v18;
      HIDWORD(n_v29) = 120000;
      n_v14 = fsctl(statfs_buf.f_mntonname, 0xC0384A74, n_v26, 1u);
      if ( (_DWORD)n_v14 )
      {
        n_v15 = n_v14;
        goto LABEL_8;
      }
    }
  }
LABEL_29:
  if ( n_v16 )
    flag_v24 = n_v16 == n_a3;
  else
    flag_v24 = 0;
  flag_v12 = flag_v24;
LABEL_35:
  objc_release(id_a5);
  return flag_v12;
}

id objc_msgSend_addCloneInfo_(void *a1, const char *a2, ...)
{
  return objc_msgSend(a1, "addCloneInfo:");
}

id objc_msgSend_isNodeID_oldestForDStreamID_forVolPath_(void *a1, const char *a2, ...)
{
  return objc_msgSend(a1, "isNodeID:oldestForDStreamID:forVolPath:");
}

void __cdecl +[SACloneTreeWalker processCloneMapOnVol:pathList:appSizeBreakdownList:volumesInfo:collectClonesPaths:reply:](
        id id_a1,
        SEL sel_a2,
        id id_a3,
        id id_a4,
        id id_a5,
        id id_a6,
        bool flag_a7,
        id id_a8)
{
  _BOOL4 flag_v9; // w21
  id id_v13; // x22
  id id_v15; // x0
  id id_v16; // x0
  id id_v17; // x0
  id id_v18; // x0
  NSObject *nsobject_v19; // x20
  int *int_v20; // x0
  __int64 n_v21; // x20
  NSObject *nsobject_v22; // x21
  NSErrorDomain nserrordomai_v23; // x2
  __int64 n_v24; // x3
  NSError *nserror_v25; // x20
  void *void_v26; // x20
  void *void_v27; // x26
  NSError *nserror_v28; // x21
  char *str_v29; // x0
  void *void_v30; // x19
  __int64 n_v31; // x0
  __int64 n_v32; // x24
  NSObject *nsobject_v33; // x21
  NSErrorDomain nserrordomai_v34; // x2
  __int64 n_v35; // x3
  NSObject *nsobject_v36; // x20
  unsigned __int64 n_v37; // x23
  __int64 n_v38; // x25
  int n_v39; // w8
  __int64 n_v40; // x21
  bool flag_v41; // zf
  __int64 n_v42; // x19
  int n_v43; // w9
  void *void_v44; // x28
  char *str_v45; // x22
  __int64 n_v46; // x21
  __int64 n_v47; // x28
  void **void_v48; // x22
  void *void_v49; // x19
  __int64 n_v50; // x21
  __int64 n_v51; // x24
  void *void_v52; // x20
  __int64 n_v53; // x20
  void *void_v54; // x0
  unsigned __int64 n_v55; // x19
  __int64 n_v56; // x21
  void *void_v57; // x24
  __int64 n_v58; // x20
  NSObject *nsobject_v59; // x21
  void *void_v60; // [xsp+18h] [xbp-9A8h]
  id id_v61; // [xsp+20h] [xbp-9A0h]
  int n_v62; // [xsp+2Ch] [xbp-994h]
  char *str_v63; // [xsp+30h] [xbp-990h]
  char *str_v64; // [xsp+38h] [xbp-988h]
  unsigned __int64 n

## AI Prioritisation Scoring System

No actionable methods or prioritisation targets identified for this component.

