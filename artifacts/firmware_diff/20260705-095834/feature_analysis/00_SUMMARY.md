# Feature Analysis Summary — iOS 26.4.2

- **Total components in diff**: 66  (**HIGH_SIGNAL**: 11, **LOW_SIGNAL**: 55)
- **Analysed** (report written): 11  |  **Apple Security Notes matches**: 3  |  **Suppressed TIER_3**: 0  |  **HIGH_SIGNAL not analysed** (budget/security filter): 0

Tier shown is the LLM-assigned tier for analysed components, otherwise a deterministic estimate from the security score (4=Apple Security Notes, 3=hard indicator, 2=security vocabulary, 1=code change, 0=asset/UI/log).

## 🔴 Apple Security Notes matches — highest priority

| Component | Tier | Sec score | Apple Security Notes | Report |
|---|---|---|---|---|
| AppNotificationsLoggingClient | TIER_1 | 4 | `Notification Services` | [report](AppNotificationsLoggingClient_analysis.md) |
| IMAccountNotificationPlugin | TIER_1 | 4 | `Notification Services` | [report](IMAccountNotificationPlugin_analysis.md) |
| com.apple.Siri.ActionPredictionNotifications | TIER_3 | 4 | `Notification Services` | [report](com.apple.Siri.ActionPredictionNotifications_analysis.md) |

## Analysed components (reports written)

| Component | Tier | Sec score | Apple Security Notes | Report |
|---|---|---|---|---|
| AppNotificationsLoggingClient | TIER_1 | 4 | `Notification Services` | [report](AppNotificationsLoggingClient_analysis.md) |
| IMAccountNotificationPlugin | TIER_1 | 4 | `Notification Services` | [report](IMAccountNotificationPlugin_analysis.md) |
| PosterFuturesKit | TIER_1 | 1 | — | [report](PosterFuturesKit_analysis.md) |
| iMessage | TIER_1 | 1 | — | [report](iMessage_analysis.md) |
| AppPredictionClient | TIER_2 | 1 | — | [report](AppPredictionClient_analysis.md) |
| AppPredictionInternal | TIER_2 | 1 | — | [report](AppPredictionInternal_analysis.md) |
| IMSharedUtilities | TIER_2 | 1 | — | [report](IMSharedUtilities_analysis.md) |
| com.apple.Siri.ActionPredictionNotifications | TIER_3 | 4 | `Notification Services` | [report](com.apple.Siri.ActionPredictionNotifications_analysis.md) |
| AppPredictionFoundation | TIER_3 | 1 | — | [report](AppPredictionFoundation_analysis.md) |
| PosterLegibilityKit | TIER_3 | 1 | — | [report](PosterLegibilityKit_analysis.md) |
| PaperBoardUI | TIER_3 | 0 | — | [report](PaperBoardUI_analysis.md) |

## LOW_SIGNAL — excluded (55, metadata/timestamp churn only)

<details><summary>Show 55 components</summary>

- ActionPredictionHeuristics
- ActionPredictionHeuristicsInternal
- AppPredictionIntentsHelperService
- AppPredictionToolsInternal
- AppPredictionUI
- AppPredictionUIFoundation
- AppPredictionUIWidget
- BubbleKit
- ChatKit
- CommunicationDetails
- ContextualSuggestionClient
- FaceTime
- HeroDataClient
- HeuristicInterpreter
- IMAssistantCore
- IMCore
- IMCorePipeline
- IMDMessageServices
- IMDPersistence
- IMDaemonCore
- IMRCSTransfer
- IMSharedUI
- IMTranscoderAgent
- IMTranscoding
- IMTransferAgent
- IMTransferAgentClient
- MMCSServices
- Messages
- MessagesCloudSync
- MessagesComplication
- MessagesDataMigrator
- MessagesSettingsUI
- MessagesSupport
- PosterBoard
- PosterBoardServices
- PosterBoardUI
- PosterBoardUIServices
- PosterFoundation
- PosterKit
- PosterModel
- PosterPlatformSupport
- PosterUIFoundation
- ProactiveBlendingLayer_iOS
- ProactiveCDNDownloader
- ProactiveContextClient
- ProactiveMagicalMoments
- ProactivePredictionClient
- ProactivePredictionFoundation
- ProactiveSuggestionClientModel
- VisualActionPrediction
- VisualActionPredictionCore
- VisualActionPredictionSupport
- duetexpertd
- iMessageApps
- imagent

</details>
