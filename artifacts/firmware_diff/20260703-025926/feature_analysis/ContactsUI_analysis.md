## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "CNPhotoPickerListCollectionViewCell"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 0 (0 AI-authored, 0 auto-generated); comments: 0 (0 AI-authored, 0 auto-generated); across 0 function(s); verified persisted in .i64: 0 named variables, 0 comments.

## What this feature does

The ContactsUI component has undergone significant changes related to poster and avatar management, particularly focusing on visual identity features like posters, avatars, and fingerprinting. The new version introduces several new classes and methods for handling poster configurations, visual fingerprints, and sensitive content blurring.

Key new features include:
- **Poster Configuration Reading**: New classes like `CNPhotosPosterConfigurationReader` for parsing poster configurations from images
- **Visual Fingerprinting**: Enhanced fingerprinting capabilities with `CNAvatarPosterCarouselLikenessFingerprint` for matching avatars and posters
- **Sensitive Content Handling**: New `CNSensitiveContentBlurView` for blurring sensitive content in posters
- **Avatar Poster Carousel**: New carousel functionality for displaying avatar and poster pairs
- **Onboarding Flow**: New onboarding flows for poster and avatar setup

## How is it implemented

The implementation involves several new classes and their associated methods:

```c
// CNPhotosPosterConfigurationReader
// Reads and parses poster configuration from image data
// Extracts face rectangles, image data, and configuration metadata

// CNAvatarPosterCarouselLikenessFingerprint
// Generates and compares visual fingerprints for avatar-poster pairs
// Supports secure coding for archiving

// CNSensitiveContentBlurView
// Blurs sensitive content in posters based on configuration
// Manages blur visibility and animation

// CNAvatarPosterCarouselFingerprintCache
// Caches visual fingerprints for efficient comparison
// Manages cache keys and invalidation

// CNPosterEditOptionsViewController
// Handles editing of poster and avatar pairs
// Manages edit flow and state transitions
```

The implementation uses a combination of:
- Image processing for extracting face rectangles and generating fingerprints
- Configuration parsing for poster metadata
- Cache management for performance optimization
- View controller hierarchy for UI presentation

## How to trigger this feature

The feature is triggered when:
1. User views a contact card with poster/avatar information
2. User initiates poster/avatar editing flow
3. System needs to display or compare poster configurations
4. User interacts with onboarding screens for poster/avatar setup

## Vulnerability Assessment

**Vulnerability Class**: Potential Information Disclosure / Privacy Leak

**Old Code Vulnerability**:
- The old implementation used `CNAvatarPosterCarouselLikenessFingerprintPosterSnapshotImpl` which had less robust fingerprinting
- Missing proper sensitive content blurring mechanisms
- Less comprehensive cache management for fingerprints
- Some methods like `fallbackTextForContact:` were removed, potentially leaving gaps in error handling

**New Code Mitigations**:
- Added `CNSensitiveContentBlurView` for proper blurring of sensitive content
- Enhanced fingerprinting with `CNAvatarPosterCarouselLikenessFingerprint` for better matching
- Improved cache management with `CNAvatarPosterCarouselFingerprintCache`
- Better error handling with new error messages like "Could not load portrait layer stack"
- Added proper cleanup mechanisms for temporary poster data

**Potential Impact if Left Unpatched**:
- Privacy leaks through insufficient sensitive content blurring
- Inefficient fingerprint matching leading to incorrect avatar-poster associations
- Memory leaks from improper cache management
- Poor user experience with missing fallbacks and error states

## Evidence

**New Classes Added**:
- `CNPhotosPosterConfigurationReader` - Reads poster configurations from images
- `CNAvatarPosterCarouselLikenessFingerprint` - Enhanced fingerprinting for avatar-poster matching
- `CNSensitiveContentBlurView` - Blurs sensitive content in posters
- `CNAvatarPosterCarouselFingerprintCache` - Caches visual fingerprints
- `CNPosterEditOptionsViewController` - Handles poster/avatar editing
- `CNPosterOnboardingSettingsAnimationViewController` - Onboarding flow for posters

**New Methods**:
- `fingerprintForPosterConfiguration:` - Generates fingerprints from poster configurations
- `visualFingerprintForSnapshotImage:` - Extracts visual fingerprints from images
- `invalidateFingerprintsForContactIdentifiers:` - Clears cached fingerprints
- `updateSensitiveContentBlurVisibility:` - Manages blur visibility
- `saveCurrentVisualIdentityIfNeeded` - Saves visual identity data

**Removed Classes**:
- `CNWallpaperGalleryMemojiItemProvider` - Replaced with new poster configuration system
- `CNAvatarPosterCarouselLikenessFingerprintPosterSnapshotImpl` - Replaced with improved implementation

**String Evidence**:
- "ContactsUI.CNSensitiveContentBlurView" - New sensitive content blurring class
- "Using fingerprint generated from poster UUID" - New fingerprinting mechanism
- "Contact has a current shared photo: %d" - New shared photo tracking
- "Could not load portrait layer stack" - New error handling

**Symbol Evidence**:
- New symbols for poster configuration reading and fingerprinting
- New methods for sensitive content blurring
- Enhanced cache management methods

## AI Prioritisation Scoring System

- **visual_fingerprinting_and_sensitive_content_blurring**
  - **Tier**: TIER_1
  - **Category**: privacy_security
  - **Reasoning**: This change introduces critical privacy and security improvements through enhanced visual fingerprinting for avatar-poster matching and new sensitive content blurring mechanisms. The removal of old fingerprinting implementations and addition of proper blurring functionality addresses potential privacy leaks. The changes affect core contact poster/avatar functionality which has observable runtime behavior and direct privacy implications.

