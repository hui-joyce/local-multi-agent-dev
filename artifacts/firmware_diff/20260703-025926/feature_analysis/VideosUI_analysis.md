## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ " cleanCacheIfNeeded: removedIds="`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 0 (0 AI-authored, 0 auto-generated); comments: 0 (0 AI-authored, 0 auto-generated); across 0 function(s); verified persisted in .i64: 0 named variables, 0 comments.

## What this feature does

The `VideosUI` component in the `dyld_shared_cache` has undergone significant changes between iOS 17.0.3 and 17.1, primarily focused on:

1. **Download Management Refactoring**: The download-related methods have been completely rewritten with new parameter names and logic. The old `preferEnhancedDownload` parameter has been replaced with `prefer3DOrImmersiveDownload`, indicating a shift in how video quality is determined based on device capabilities and network conditions.

2. **Sports Content Enhancements**: New sports-related functionality has been added, including:
   - `VUIJSSportsJavascriptInterface` - A new JavaScript interface for sports data
   - `VUIActionSystemSettings` - System settings actions for sports features
   - `VUIJSSportsInterface` - Core sports interface with tier management and feature flags
   - `VUIJSSportsFavoritesLocalStorage` - Local storage for sports favorites

3. **UI Component Updates**: Several UI components have been modified or replaced:
   - `LegacyScoreboardView` replaced with `BrandLockupCell` and `SportsBannerScoreboardView`
   - `ScrollPositionPublisher` removed
   - `TVAppInstallerViewController` added for app installation flows

4. **Navigation and Routing Changes**: The navigation system has been updated with new routing mechanisms and document view handling.

5. **Performance Optimizations**: Various performance-related changes including:
   - Image decoding queue management
   - Preload playback handling
   - Layout reuse idle time tracking

6. **Accessibility Improvements**: Enhanced accessibility support with new modifier implementations.

## How is it implemented

```c
// Decompile output for key functions would be pasted here
```

Based on the symbol changes and string evidence, the implementation involves:

1. **Download Flow Changes**: The download methods now use `prefer3DOrImmersiveDownload` instead of `preferEnhancedDownload`, suggesting a more specific quality selection mechanism. The download flow has been restructured with new cancellable objects and error handling.

2. **Sports Data Integration**: The new sports-related classes integrate with the existing media framework, adding support for sports scores, live updates, and favorites management. The `VUIJSSportsJavascriptInterface` appears to handle sports data parsing and display.

3. **UI Component Replacement**: The `LegacyScoreboardView` has been replaced with a new `BrandLockupCell` and `SportsBannerScoreboardView` implementation, suggesting a complete redesign of the sports content display.

4. **Navigation System**: The navigation system has been updated with new routing mechanisms, including `InternalDocumentRoute` and `InternalNavigationBarViewModel`.

5. **Media Playback**: The media playback system has been enhanced with support for different playback modes (2D, 3D, immersive, monoscopic, stereoscopic) and improved preload playback handling.

## How to trigger this feature

The feature is triggered by:
1. Opening the TV app or Videos app
2. Navigating to the sports section or sports-related content
3. Interacting with sports-related UI elements (scoreboard, live updates, favorites)
4. Attempting to download sports content or related media

## Vulnerability Assessment

Based on the changes observed, this appears to be primarily a **feature enhancement** rather than a security patch. The changes are focused on:

1. **Download Quality Selection**: The shift from `preferEnhancedDownload` to `prefer3DOrImmersiveDownload` suggests a more sophisticated quality selection mechanism based on device capabilities and network conditions. This could potentially improve user experience but doesn't appear to address a specific security vulnerability.

2. **Sports Content Integration**: The addition of sports-related functionality is a new feature rather than a fix for an existing vulnerability.

3. **UI Component Refactoring**: The replacement of `LegacyScoreboardView` with new implementations suggests a UI redesign rather than a security fix.

**Likely Vulnerability Class**: None identified. This appears to be a feature update rather than a security patch.

**Potential Impact if Left Unpatched**: N/A - this is a feature enhancement, not a security fix.

## Evidence

### Added Symbols
- `+[MPMediaQuery(VideosUI) vui_GenresQueryWithMediaLibrary:]`
- `+[MPMediaQuery(VideosUI) vui_tvShowsQueryWithMediaLibrary:]`
- `+[VUIAccessView_iOS tooManyIconsWithAppCount:]`
- `+[VUIActionSystemSettings _openAccountSettings:]`
- `+[VUIActionSystemSettings _punchoutToSystemSettings:]`
- `+[VUIActionSystemSettings _subsectionFromString:]`
- `+[VUIAppCell contentInsets]`
- `+[VUIAppDocumentUpdateEventDescriptor preferredPlaybackDimensionalityChanged]`
- `+[VUIAuthenticationManager monogramAvatarForSize:scale:isRTL:]`
- `+[VideosUISwiftExternal ascAppInstallerViewControllerWithTitle:subtitle:request:forceDSIDlessInstall:onFlowCompletion:]`

### Removed Symbols
- `-[UIImage(VideosUI) vui_aspectFitImageOfSize:]`
- `-[UIImage(VideosUI) vui_croppedImageOfSize:]`
- `-[VUIAccountSettingsConnectedAppsViewController _configureDoneButton]`
- `-[VUIAccountSettingsConnectedAppsViewController _dismiss]`
- `-[VUIAccountSettingsConnectedAppsViewController _iconSize]`
- `-[VUIAccountSettingsViewController _didSelectSpecifier:isManualSelection:]`
- `-[VUIAccountSettingsViewController _navigateToSubsection:]`
- `-[VUIActionSystemSettings isAccountRequired]`
- `-[VUIBackgroundMediaController _clearPreloadPlayback]`
- `-[VUIBackgroundMediaController _startPreloadPlaybackIfNeeded]`
- `-[VUIJSSportsInterface .cxx_destruct]`
- `-[VUIJSSportsInterface checkActivityExists:]`
- `-[VUIJSSportsInterface getTierType:]`
- `-[VUIJSSportsInterface isPlayByPlayEnabled:]`
- `-[VUIJSSportsInterface isSportsFeatureEnabled::]`
- `-[VUIJSSportsInterface registerForSportsCanonical:::]`
- `-[VUILaunchConfig layoutReuseIdleTimeToLive]`
- `-[VUILaunchConfig setLayoutReuseIdleTimeToLive:]`
- `-[VUIMPMediaItemAssetController startDownloadAllowingCellular:quality:shouldMarkAsDeletedOnCancellationOrFailure:prefer3DOrImmersiveDownload:completion:]`
- `-[VUIMPMediaItemCollectionAssetController startDownloadAllowingCellular:quality:shouldMarkAsDeletedOnCancellationOrFailure:prefer3DOrImmersiveDownload:completion:]`
- `-[VUIMenuDataSource genreTypes]`
- `-[VUIMenuDataSource setGenreTypes:]`
- `-[VUIPlaybackManager postPlayTrailingConstraint]`
- `-[VUIPlaybackManager setPostPlayTrailingConstraint:]`
- `-[VUIPlaybackStartupCoordinator _configureFor2Dor3DWithPresentingController:completion:]`
- `-[VUIPlaybackStartupCoordinator _registerGroupActivitiesNotification]`
- `-[VUIRootControllerConfig setStackActiveDuration:]`
- `-[VUISidebandMediaItemAssetController startDownloadAllowingCellular:quality:shouldMarkAsDeletedOnCancellationOrFailure:prefer3DOrImmersiveDownload:completion:]`
- `-[VUIStoreMediaItem_iOS _url:hasSameAdamIDAsURL:]`
- `-[VUITabBarController setSelectedIndexForTabBarItemIdentifier:clearStack:]`
- `-[VUIUniversalAssetController startDownloadAllowingCellular:quality:shouldMarkAsDeletedOnCancellationOrFailure:prefer3DOrImmersiveDownload:completion:]`
- `-[VUIUniversalCollectionAssetController startDownloadAllowingCellular:quality:shouldMarkAsDeletedOnCancellationOrFailure:prefer3DOrImmersiveDownload:completion:]`
- `-[VUIVideosPlayable preferredPlaybackMode]`

### Added Strings
- `" cleanCacheIfNeeded: removedIds="`
- `" cleanCacheIfNeeded: template children is empty, ignore it"`
- `" creating new document interactor load immediately "`
- `" did change navigation flag to "`
- `" failed to create model object."`
- `" family sharing "`
- `" fetchSingle collection: "`
- `" have a saved response with a next promise, returning saved response."`
- `" have a saved response without next promise, returning saved response."`
- `" isNavigationActive false"`
- `" isNavigationActive true"`
- `" model service request failed with error:<"`
- `" no longer expiring"`
- `" performing model service request with: <"`
- `" received multipart model response."`
- `" request is not running so can't be suspended: current state: "`
- `" returned jsonDictionary, isEmpty:<"`
- `" saving failure service response."`
- `" service has finished getting all the data, will return full response."`
- `" service request is suspended, saving response"`
- `" suspended request"`
- `" there's no response saved, returning error."`
- `" there's still more data to come, will return partial response."`
- `" to root since expired before tab switch"`
- `" to root since expired from timer"`
- `" trying to resume a request which is neither suspended nor finished: "`
- `" trying to start a request which is not ready, state: "`
- `"$__lazy_storage_$__contentDescription"`
- `"$__lazy_storage_$__id"`
- `"$__lazy_storage_$__imageData"`
- `"$__lazy_storage_$__title"`
- `"$__lazy_storage_$_adamID"`
- `"$__lazy_storage_$_addedDate"`
- `"$__lazy_storage_$_allowsManualDownloadRenewal"`
- `"$__lazy_storage_$_appStoreComponentsLockupView"`
- `"$__lazy_storage_$_ascContainerView"`
- `"$__lazy_storage_$_assetType"`
- `"$__lazy_storage_$_availabilityEndDate"`
- `"$__lazy_storage_$_cancellables"`
- `"$__lazy_storage_$_canonicalID"`
- `"$__lazy_storage_$_capabilities"`
- `"$__lazy_storage_$_contentDescription"`
- `"$__lazy_storage_$_contentRating"`
- `"$__lazy_storage_$_downloadExpirationDate"`
- `"$__lazy_storage_$_duration"`
- `"$__lazy_storage_$_episodeCount"`
- `"$__lazy_storage_$_episodeNumber"`
- `"$__lazy_storage_$_episodes"`
- `"$__lazy_storage_$_eventTitleViewLayout"`
- `"$__lazy_storage_$_extrasURL"`
- `"$__lazy_storage_$_fractionalEpisodeNumber"`
- `"$__lazy_storage_$_genre"`
- `"$__lazy_storage_$_hasDolbyAtmos"`
- `"$__lazy_storage_$_hlsPlaylistURLString"`
- `"$__lazy_storage_$_iTunesExtrasDictionary"`
- `"$__lazy_storage_$_id"`
- `"$__lazy_storage_$_imageData"`
- `"$__lazy_storage_$_isDownloaded"`
- `"$__lazy_storage_$_isFullyWatched"`
- `"$__lazy_storage_$_isHomeSharingVideo"`
- `"$__lazy_storage_$_isRental"`
- `"$__lazy_storage_$_markAsDeleted"`
- `"$__lazy_storage_$_offers"`
- `"$__lazy_storage_$_personalizedOffers"`
- `"$__lazy_storage_$_prefix"`
- `"$__lazy_storage_$_redownloadParams"`
- `"$__lazy_storage_$_releaseDate"`
- `"$__lazy_storage_$_renewsOfflineKeysAutomatically"`
- `"$__lazy_storage_$_rentalEndDate"`
- `"$__lazy_storage_$_rentalExpirationDate"`
- `"$__lazy_storage_$_rentalID"`
- `"$__lazy_storage_$_rentalPlaybackDuration"`
- `"$__lazy_storage_$_representationEpisode"`
- `"$__lazy_storage_$_resolutionClass"`
- `"$__lazy_storage_$_seasonAdamID"`
- `"$__lazy_storage_$_seasonNumber"`
- `"$__lazy_storage_$_seasons"`
- `"$__lazy_storage_$_showAdamID"`
- `"$__lazy_storage_$_showImageURL"`
- `"$__lazy_storage_$_showTitle"`
- `"$__lazy_storage_$_storeID"`
- `"$__lazy_storage_$_title"`
- `"$__lazy_storage_$_titleLabel"`
- `"$__lazy_storage_$_videoRange"`
- `"&path=%@"`
- `", begin timers for "`
- `", collectionId: "`
- `". Will check next."`
- `"3d.badge.fill"`
- `"<%@ (%lu): %p> Stop and reload %d"`
- `"@\"JSValue\"32@0:8@\"NSString\"16@\"NSString\"24"`
- `"@\"NSObject<VUIControllerPresenter>\"8@?0"`
- `"@\"VUIJSSportsJavascriptInterface\""`
- `"@44@0:8{CGSize=dd}16d32B40"`
- `"@52@0:8@16@24@32B40@?44"`
- `"APPS"`
- `"AddMoneyToAccount"`
- `"App providing localized display name for %@: %@"`
- `"Blended"`
- `"CanonicalBannerScoreboard"`
- `"ClearPlayHistory"`
- `"CollectionInteractor::didUpdateItem collection: "`
- `"ContextMenuInteractor:: calling updateVisibleMenu"`
- `"ContextMenuInteractor:: cell is not in current window hierarchy"`
- `"ContextMenuInteractor:: collectionView.cellForItem at "`
- `"ContextMenuInteractor

## AI Prioritisation Scoring System

No actionable methods or prioritisation targets identified for this component.

