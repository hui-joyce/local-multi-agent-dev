## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ " %@ <%@:%@>"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 3 (3 AI-authored, 0 auto-generated); comments: 1 (0 AI-authored, 1 auto-generated); across 1 function(s); verified persisted in .i64: 6 named variables, 1 comments.
- **Apple Security Notes**: matches advisory component `Core Recents` — Apple confirms a security-relevant change here; this analysis examines the likely vulnerability patch.

## What this feature does

The `CoreRecents` framework in iOS 17.1 (21B80) introduces a new sanitization mechanism for recent contact descriptions, replacing the verbose, potentially sensitive output format with a cleaner, more privacy-preserving alternative. The new implementation adds the `appendSanitizedDescriptionTo:` method to the `CRRecentContact` class, which constructs a description string that masks sensitive identifiers and limits metadata exposure.

## How is it implemented

```c
void *__fastcall -[CRRecentContact appendSanitizedDescriptionTo:](__int64 self, __int64 n_a2, void *stringBuilder)
{
  __int64 n_v5; // x0
  unsigned int n_v6; // w0
  const char *str_v7; // x8

  n_v5 = MEMORY[0x1AE15A5B0]();
  objc_msgSend(stringBuilder, "appendFormat:", &stru_1E0103820, MEMORY[0x1AE15A470](n_v5), self);
  if ( *(_QWORD *)(self + 112) == 0x7FFFFFFFFFFFFFFFLL )
    objc_msgSend(stringBuilder, "appendString:", &stru_1E0103840);
  else
    objc_msgSend(stringBuilder, "appendFormat:", &stru_1E0103860, *(_QWORD *)(self + 112));
  if ( *(_QWORD *)(self + 16) == 0x7FFFFFFF )
    objc_msgSend(stringBuilder, "appendString:", &stru_1E0103880);
  else
    objc_msgSend(stringBuilder, "appendFormat:", &stru_1E01038A0, *(_QWORD *)(self + 16));
  objc_msgSend(stringBuilder, "appendFormat:", &stru_1E01038C0, objc_msgSend(*(id *)(self + 72), "count"));
  n_v6 = (unsigned int)objc_msgSend((id)self, "isGroup");
  str_v7 = "n";
  if ( n_v6 )
    str_v7 = "y";
  return objc_msgSend(stringBuilder, "appendFormat:", &stru_1E01038E0, str_v7);
}
```

The implementation follows a structured approach to sanitizing contact descriptions:

1. **Initial Format Construction**: The method starts by appending a formatted string containing the contact's name and a placeholder for the contact ID (`%@ <%@:%@>`).

2. **Contact ID Handling**: It checks if the contact ID field (offset 112) contains a sentinel value (`0x7FFFFFFFFFFFFFFFLL`). If so, it appends the literal string `<null-contact-id>`. Otherwise, it appends the actual contact ID in the format `cid=<value>`.

3. **Recent ID Handling**: Similarly, it checks the recent ID field (offset 16). If it contains the sentinel value, it appends `<null-recent-id>`. Otherwise, it appends the recent ID in the format `rid=<value>`.

4. **Metadata Count**: It retrieves the count of metadata keys associated with the contact and appends this information.

5. **Group Indicator**: It checks whether the contact is a group member via the `isGroup` selector. Based on the result, it appends either "y" or "n" to indicate group membership.

The final output is a sanitized description string that replaces the previous verbose format with a more concise, privacy-conscious representation.

## How to trigger this feature

The feature is triggered automatically whenever the `CoreRecents` framework generates or displays recent contact information. Specifically:

- When the system needs to display a recent contact in the Recents UI or any other context where recent contacts are shown.
- When the `CRRecentContact` object is instantiated and its description is requested through the `appendSanitizedDescriptionTo:` method.
- The method is called on the `CRRecentContact` instance, passing a `stringBuilder` object to accumulate the sanitized description.

The trigger is implicit in the framework's operation and does not require explicit user action. It is part of the normal workflow for handling recent contacts in the system.

## Vulnerability Assessment

**Security-relevant change**: The diff introduces a new sanitization mechanism for contact descriptions, replacing a verbose, potentially sensitive output format with a cleaner, more privacy-preserving alternative. The old format included detailed metadata (dates, multiple metadata keys, verbose identifiers) that could expose sensitive information. The new format masks null IDs and limits metadata exposure.

**Patch mechanism**: The new implementation uses conditional checks to replace sensitive values with placeholder strings:
- Null contact IDs are replaced with `<null-contact-id>`
- Null recent IDs are replaced with `<null-recent-id>`
- Group membership is indicated with a simple "y" or "n"
- The overall format is simplified to ` %@ <%@:%@>` instead of the verbose format

**Evidence**: 
- New method `appendSanitizedDescriptionTo:` is added (symbol in diff)
- New strings for sanitized placeholders are added (e.g., `<%@ %p`, `cid=%lld`, `rid=%lld`, `cid=<null-contact-id>`, `rid=<null-recent-id>`)
- Old verbose format strings are removed (e.g., `"<%@: %p> (rid=%@) (cid=%@) dates={%@}, %lu metadata key%s, isGroup=%s"`)
- The binary diff shows the new method and related strings are present in the new version but absent in the old version
- The decompiled code shows explicit checks for sentinel values and conditional string appending

**Potential impact if left unpatched**: The old implementation could expose sensitive information including:
- Exact contact IDs and recent IDs
- Detailed metadata keys and their values
- Precise dates and timestamps
- Verbose descriptions that could be used for fingerprinting or tracking

This is a **privacy enhancement** rather than a traditional security vulnerability fix. It reduces the amount of personally identifiable information (PII) that could be exposed through recent contact descriptions.

## Evidence

1. **New Symbols**:
   - `-[CRRecentContact appendSanitizedDescriptionTo:]` - The new sanitization method
   - `_objc_msgSend$appendSanitizedDescriptionTo:` - The corresponding message send stub
   - New block literals (`___block_literal_global.305`, `.308`, `.321`)

2. **Removed Symbols**:
   - `-[CRRecentContact sanitizedDescription]` - The old unsanitized method
   - `_objc_msgSend$sanitizedDescription` - The corresponding message send stub

3. **New Strings**:
   - ` %@ <%@:%@>` - Simplified contact name format
   - `cid=%lld` - Contact ID format
   - `cid=<null-contact-id>` - Placeholder for null contact ID
   - `rid=%lld` - Recent ID format
   - `rid=<null-recent-id>` - Placeholder for null recent ID
   - `isGroup=%s` - Group indicator format

4. **Removed Strings**:
   - `"%@, %@ <%@:%@>"` - Old verbose format
   - `"<%@: %p> (rid=%@) (cid=%@) dates={%@}, %lu metadata key%s, isGroup=%s"` - Old detailed format
   - `"<null-contact-id>"` and `"<null-recent-id>"` - Old placeholder formats

5. **Binary Diff**:
   - Framework version changed from 1209.0.0.0.0 to 1210.0.0.0.0
   - Text segment sizes increased slightly
   - Objective-C method list and stubs updated
   - String table updated (new strings added, old strings removed)
   - UUID changed (new build)
   - Function count increased from 287 to 288 (one new function added)
   - Symbol count increased from 1234 to 1238
   - String count increased from 770 to 779
   - Removed dylib dependencies (`CoreFoundation`, `Foundation`, `libicucore.A.dylib`, `libobjc.A.dylib`, `libsqlite3.dylib`)

6. **Decompiled Code**:
   - Shows explicit checks for sentinel values (`0x7FFFFFFFFFFFFFFFLL`)
   - Conditional string appending based on whether values are present
   - Uses `appendFormat:` and `appendString:` to build the sanitized description
   - Implements the group indicator logic with a simple "y"/"n" string

## AI Prioritisation Scoring System

- **Security Notes Correlation + Binary Diff Analysis + Decompilation**
  - **Tier**: TIER_2
  - **Category**: Privacy Enhancement
  - **Reasoning**: This change implements a privacy enhancement by sanitizing contact descriptions to reduce PII exposure. The new implementation masks null IDs, limits metadata, and simplifies the output format. While not a critical security boundary fix, it has observable runtime behavior (different description format) and addresses privacy concerns. The evidence is strong: new sanitization method, new placeholder strings, removal of verbose format, and decompiled code showing explicit privacy-preserving logic.

