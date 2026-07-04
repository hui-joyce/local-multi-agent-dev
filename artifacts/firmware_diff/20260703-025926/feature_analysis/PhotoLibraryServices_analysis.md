## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ "%@-copy"`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 0 (0 AI-authored, 0 auto-generated); comments: 0 (0 AI-authored, 0 auto-generated); across 0 function(s); verified persisted in .i64: 0 named variables, 0 comments.

## What this feature does

The `PhotoLibraryServices` component has undergone significant changes between iOS 17.0.3 and 17.1, primarily focused on **Photo Stream (MPS) removal and Photo Library (iCPL) migration**. Key changes include:

1. **Photo Stream (MPS) Removal**: Multiple strings and symbols related to Photo Stream have been removed, including:
   - `PLPhotoStreamsHelper` and related Photo Stream functionality
   - Photo Stream asset management, publishing, and deletion
   - Photo Stream account settings and synchronization
   - Photo Stream image limits and derivative handling

2. **Photo Library (iCPL) Enhancement**: New symbols and strings indicate enhanced Photo Library functionality:
   - `PLSyndicationRuntimeEnabled` - New syndication runtime feature
   - `PLCaptureDeferredPhotoProcessor` - New deferred photo processing
   - `PLDelayedSaveActions` - New delayed save actions for wallpaper albums
   - `PLMigrationHistory` - Enhanced migration history with hardware model and device unique ID tracking
   - `PLPersistentHistoryUtilities` - New persistent history utilities

3. **Deferred Photo Processing**: New deferred photo processing capabilities:
   - `PLCaptureDeferredPhotoProcessor` - Captures and processes deferred photos
   - `PLDeferredPhotoFinalizer` - Finalizes deferred photos with various recovery mechanisms
   - `PLDeferredPhotoPendingAssetRecord` - Manages pending deferred photo assets

4. **Wallpaper Suggestion Management**: New mechanisms for managing wallpaper suggestions:
   - `PLDelayedSaveActions` - Handles delayed save actions for wallpaper user and favorite albums
   - Assets for wallpaper removal and reload tracking

5. **Migration and Data Management**: Enhanced migration and data management:
   - `PLModelMigrator` - Enhanced migration with hardware model and device unique ID
   - `PLResourceInstaller` - Enhanced image request hints with one-time thumbnail rebuild
   - `PLAssetJournalEntryPayload` - Enhanced asset journal entry payload

6. **Photo Library Loading and Management**: Improved photo library loading and management:
   - `PLPhotoLibrary` - Enhanced photo library with DCIM entry, deferred intermediates, and unknown deferred intermediates
   - `PLPrimaryResourceDataStore` - Enhanced resource data store with task locking and transition
   - `PLThumbnailManager` - Enhanced thumbnail management with urgent cache delete

7. **Photo Stream to Photo Library Transition**: Strings indicate the transition from Photo Stream to Photo Library:
   - `"%{public}@: SPL Change: Disabling My Photo Stream of previous SPL at %@"`
   - `"%{public}@: SPL Change: Finished disabling MPS"`
   - `Disabling My Photo Stream due to switching SPL.`

8. **Photo Stream Asset Management**: Removal of Photo Stream asset management:
   - `-[PLAssetsSaver deletePhotoStreamData]` - Removed Photo Stream data deletion
   - `-[PLImageWriter _enablePhotoStreamJob:completion:]` - Removed Photo Stream job enabling
   - `-[PLImageWriter _processDeletePhotoStreamAssetsWithUUIDs:withReason:completion:]` - Removed Photo Stream asset deletion processing
   - `-[PLImageWriter _processReenqueueAssetUUIDsToPhotoStreamJob:completion:]` - Removed Photo Stream asset reenqueue processing
   - `-[PLImageWriter _processSavePhotoStreamImageToCameraRollJob:completion:]` - Removed Photo Stream image save processing

9. **Photo Stream Account Management**: Removal of Photo Stream account management:
   - `-[PLAssetsdConnectionAuthorization isPhotosPickerClient]` - Removed Photos Picker client check
   - `-[PLAssetsdConnectionAuthorization isPreferencesClient]` - Removed Preferences client check
   - `-[PLBackgroundJobService serviceState]` - Removed service state management

10. **Photo Stream Synchronization**: Removal of Photo Stream synchronization:
    - `-[PLPhotoStreamsHelper deletePhotoStreamAssetsWithLibraryServiceManager:withReason:jobStreamID:completion:]` - Removed Photo Stream asset deletion
    - `-[PLPhotoStreamsHelper deletePhotoStreamData]` - Removed Photo Stream data deletion
    - `-[PLPhotoStreamsHelper deletePhotoStreamAssetsWithUUIDs:streamID:]` - Removed Photo Stream asset deletion by UUID
    - `-[PLPhotoStreamsHelper deletePhotoStreamDataForStreamID:]` - Removed Photo Stream data deletion by stream ID

11. **Photo Stream Publishing**: Removal of Photo Stream publishing:
    - `-[PLPhotoSharingHelper downloadAsset:cloudPlaceholderKind:shouldPrioritize:shouldExtendTimer:]` - Removed Photo Stream asset download
    - `-[PLPhotoSharingHelper acceptPendingInvitationForAlbum:completionHandler:]` - Removed Photo Stream invitation acceptance
    - `-[PLPhotoSharingHelper markPendingInvitationAsSpamForAlbum:completionHandler:]` - Removed Photo Stream invitation spam marking

12. **Photo Stream Limits**: Removal of Photo Stream limits:
    - `PhotoStreamsFriendImageLimit` - Removed friend image limit
    - `PhotoStreamsMaxPixelsForDerivative` - Removed max pixels for derivative
    - `PhotoStreamsOwnImageLimit` - Removed own image limit
    - `PhotoStreamsSubscriptionsLimit` - Removed subscriptions limit

13. **Photo Stream Metadata**: Removal of Photo Stream metadata:
    - `savePhotoStreamMetadata:forAsset:` - Removed Photo Stream metadata save
    - `savePhotoStreamMetadata:forAsset: could not find master hash in metadata %@` - Removed Photo Stream metadata save error handling

14. **Photo Stream Hash Management**: Removal of Photo Stream hash management:
    - `psHashAsString:` - Removed Photo Stream hash as string
    - `psHashForData:` - Removed Photo Stream hash for data
    - `savePhotoStreamMetadata:forAsset: could not find master hash in metadata %@` - Removed Photo Stream master hash retrieval

15. **Photo Stream Visibility**: Removal of Photo Stream visibility management:
    - `shouldHideAvalanchesFromPhotoStream` - Removed Photo Stream avalanche hiding
    - `shouldPublishScreenShhots` - Removed Photo Stream screenshot publishing

16. **Photo Stream Account Settings**: Removal of Photo Stream account settings:
    - `photoStreamAccountSettingsChanged` - Removed Photo Stream account settings change
    - `photoStreamsEnabledForPhotoLibraryBundle:` - Removed Photo Stream enabled for photo library bundle
    - `photoStreamsEnabledForPhotoLibraryURL:` - Removed Photo Stream enabled for photo library URL
    - `photoStreamsPublishStreamID` - Removed Photo Stream publish stream ID

17. **Photo Stream Synchronization State**: Removal of Photo Stream synchronization state:
    - `lastPhotoStreamUpdateDate` - Removed last Photo Stream update date
    - `fetchMPSStateWithBaseAvailabilityURL:personID:originalLibrarySize:completionBlock:` - Removed Photo Stream state fetch
    - `fetchMPSStateWithLibrary:completion:` - Removed Photo Stream state fetch
    - `handleMPSStateIfNecessaryInLibrary:` - Removed Photo Stream state handling

18. **Photo Stream Server Configuration**: Removal of Photo Stream server configuration:
    - `serverSideConfigurationForPersonID:` - Removed Photo Stream server configuration
    - `server provided supportedAssets limits %@` - Removed Photo Stream supported assets limits

19. **Photo Stream Deletion**: Removal of Photo Stream deletion:
    - `initiateDeletionOfOriginalAssets` - Removed Photo Stream original asset deletion
    - `initiateDeletionOfPhotoStreamAssets` - Removed Photo Stream asset deletion
    - `initiateDeletionOfPhotoStreamAssets:` - Removed Photo Stream asset deletion
    - `deletePhotoStreamAssetsWithLibraryServiceManager:withReason:completion:` - Removed Photo Stream asset deletion
    - `deletePhotoStreamAssetsWithUUIDs:streamID:` - Removed Photo Stream asset deletion by UUID
    - `deletePhotoStreamDataForStreamID:` - Removed Photo Stream data deletion by stream ID

20. **Photo Stream Publishing State**: Removal of Photo Stream publishing state:
    - `kPLPhotoStreamPublishStateDidEnqueue` - Removed Photo Stream publish state did enqueue
    - `kPLPhotoStreamPublishStateKey` - Removed Photo Stream publish state key
    - `kPLPhotoStreamPublishStateWillEnqueue` - Removed Photo Stream publish state will enqueue
    - `will call msconnection enqueueAssetCollections with %@` - Removed Photo Stream asset collection enqueue
    - `will call msconnection pollForSubscriptionUpdatesForPersonID %@` - Removed Photo Stream subscription updates poll

21. **Photo Stream Hash Calculation**: Removal of Photo Stream hash calculation:
    - `hashForAsset:` - Removed Photo Stream hash calculation
    - `computeAssetHashesForManagedObjectContext:` - Removed Photo Stream asset hash computation
    - `computeCloudAssetHashesForManagedObjectContext:` - Removed Photo Stream cloud asset hash computation
    - `computeHashForAsset:` - Removed Photo Stream hash computation

22. **Photo Stream Duplicate Management**: Removal of Photo Stream duplicate management:
    - `analyzeDupesWithNormalInserts:cloudInserts:completionHandler:` - Removed Photo Stream duplicate analysis
    - `analyzeDupesForCloudInsertsForManagedObjectContext:` - Removed Photo Stream cloud insert duplicate analysis
    - `analyzeDupesForNormalInsertsForManagedObjectContext:` - Removed Photo Stream normal insert duplicate analysis
    - `analyzeDupesForRebuild` - Removed Photo Stream duplicate analysis rebuild
    - `analyzeNormalAssetsForManagedObjectContext:` - Removed Photo Stream normal asset analysis

23. **Photo Stream Duplicate Insert Management**: Removal of Photo Stream duplicate insert management:
    - `_dupeAnalysisCloudInserts` - Removed Photo Stream cloud insert duplicate analysis
    - `_dupeAnalysisNormalInserts` - Removed Photo Stream normal insert duplicate analysis
    - `dupeAnalysisCloudInserts` - Removed Photo Stream cloud insert duplicate analysis
    - `dupeAnalysisNormalInserts` - Removed Photo Stream normal insert duplicate analysis

24. **Photo Stream Duplicate Photo Management**: Removal of Photo Stream duplicate photo management:
    - `duplicatePhotoStreamPhotosForPhotos:` - Removed Photo Stream duplicate photo management
    - `maskForFetchingDuplicatePhotoStreamPhotosForPhotos` - Removed Photo Stream duplicate photo fetching mask

25. **Photo Stream Duplicate Photo Stream Count**: Removal of Photo Stream duplicate photo stream count:
    - `__duplicatePhotoStreamCount` - Removed Photo Stream duplicate photo stream count
    - `_duplicatePhotoStreamCount` - Removed Photo Stream duplicate photo stream count
    - `duplicatePhotoStreamCount` - Removed Photo Stream duplicate photo stream count
    - `set_duplicatePhotoStreamCount:` - Removed Photo Stream duplicate photo stream count setter

26. **Photo Stream Duplicate Photo Stream Limit**: Removal of Photo Stream duplicate photo stream limit:
    - `friendsLimit` - Removed Photo Stream friends limit
    - `imageLimitForFriendStream` - Removed Photo Stream friend image limit
    - `imageLimitForOwnStream` - Removed Photo Stream own image limit
    - `imageLimitsByAssetType` - Removed Photo Stream image limits by asset type
    - `mme.streams.client.maxAssetsToDisplay` - Removed Photo Stream max assets to display
    - `mme.streams.client.maxFriends` - Removed Photo Stream max friends
    - `mme.streams.client.maxPhotosShared` - Removed Photo Stream max photos shared
    - `PhotoStreamsFriendImageLimit` - Removed Photo Stream friend image limit
    - `PhotoStreamsMaxPixelsForDerivative` - Removed Photo Stream max pixels for derivative
    - `PhotoStreamsOwnImageLimit` - Removed Photo Stream own image limit
    - `PhotoStreamsSubscriptionsLimit` - Removed Photo Stream subscriptions limit
    - `subscriptionsLimit` - Removed Photo Stream subscriptions limit
    - `using hard coded imageLimitForFriendStream` - Removed Photo Stream friend image limit hard coding
    - `using hard coded imageLimitForOwnStream` - Removed Photo Stream own image limit hard coding
    - `using hard coded subscriptionsLimit` - Removed Photo Stream subscriptions limit hard coding

27. **Photo Stream Duplicate Photo Stream Visibility**: Removal of Photo Stream duplicate photo stream visibility:
    - `shouldHideAvalanchesFromPhotoStream` - Removed Photo Stream avalanche hiding
    - `shouldPublishScreenShhots` - Removed Photo Stream screenshot publishing

28. **Photo Stream Duplicate Photo Stream Upload**: Removal of Photo Stream duplicate photo stream upload:
    - `isValidUploadAsset:type:fileSize:` - Removed Photo Stream duplicate photo stream upload validation
    - `uti %@ and fileSize %@ are not valid for uploading, did not enqueue asset` - Removed Photo Stream duplicate photo stream upload validation error

29. **Photo Stream Duplicate Photo Stream Download**: Removal of Photo Stream duplicate photo stream download:
    - `downloadAsset:cloudPlaceholderKind:shouldPrioritize:shouldExtendTimer:` - Removed Photo Stream duplicate photo stream download
    - `savePhotoStreamImage:imageData:properties:completionBlock:` - Removed Photo Stream duplicate photo stream image save

30. **Photo Stream Duplicate Photo Stream Metadata**: Removal of Photo Stream duplicate photo stream metadata:
    - `savePhotoStreamMetadata:forAsset:` - Removed Photo Stream duplicate photo stream metadata save
    - `savePhotoStreamMetadata:forAsset: could not find master hash in metadata %@` - Removed Photo Stream duplicate photo stream metadata save error handling

31. **Photo Stream Duplicate Photo Stream Hash**: Removal of Photo Stream duplicate photo stream hash:
    - `psHashAsString:` - Removed Photo Stream duplicate photo stream hash as string
    - `psHashForData:` - Removed Photo Stream duplicate photo stream hash for data
    - `savePhotoStreamMetadata:forAsset: could not find master hash in metadata %@` - Removed Photo Stream duplicate photo stream master hash retrieval

32. **Photo Stream Duplicate Photo Stream Visibility State**: Removal of Photo Stream duplicate photo stream visibility state:
    - `shouldHideAvalanchesFromPhotoStream` - Removed Photo Stream duplicate photo stream avalanche hiding
    - `shouldPublishScreenShhots` - Removed Photo Stream duplicate photo stream screenshot publishing

33. **Photo Stream

## AI Prioritisation Scoring System

No actionable methods or prioritisation targets identified for this component.

