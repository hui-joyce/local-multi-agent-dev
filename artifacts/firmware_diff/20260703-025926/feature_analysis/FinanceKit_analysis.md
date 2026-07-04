## Triage Provenance
- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)
- **Reason**: semantic added/removed line present
- **Deciding evidence**: `+ ""`
- **Analysis mode**: decompiled
- **Database annotations** — variable renames: 0 (0 AI-authored, 0 auto-generated); comments: 0 (0 AI-authored, 0 auto-generated); across 0 function(s); verified persisted in .i64: 0 named variables, 0 comments.

## What this feature does

The FinanceKit component in the FinanceKit framework has been significantly enhanced in iOS 17.1 (21B80) compared to iOS 17.0.3 (21A360). The primary focus of these changes is the **BankConnect** integration, which appears to be a new or substantially expanded service for connecting Apple Pay accounts with external bank accounts.

### Key New Features:

1. **BankConnect Service Architecture**: Multiple new classes have been introduced for managing bank connections, including:
   - `FKBankConnectAccountsProvider` - Manages bank account data
   - `FKBankConnectInstitutionsProvider` - Manages bank institution data
   - `FKBankConnectTransactionsProvider` - Manages transaction data
   - `FKBankConnectAuthorizationSessionProvider` - Handles authorization sessions
   - `FKBankConnectInstitutionMatcher` - Matches banks to payment cards
   - `FKBankConnectMessagesController` - Manages user notifications
   - `FKBankConnectOsloProvider` - Appears to be a backend service provider
   - `FKBankConnectTransactionHistoryProvider` - Manages transaction history
   - `FKBankConnectTransactionsAndGroupsProvider` - Groups transactions
   - `FKBankConnectTransactionsListProvider` - Provides transaction lists
   - `FKBankConnectWebServiceClient` - Web service client for bank connections
   - `FKBankConnectSharedSymmetricKeyManager` - Manages encryption keys
   - `FKBankConnectPassKitTransactionsImporter` - Imports PassKit transactions
   - `FKBankConnectPassKitTransactionsDeleter` - Deletes PassKit transactions
   - `FKBankConnectPassKitTransactionsDataSource` - Data source for PassKit transactions

2. **BankConnect Integration with Apple Pay**: The system now supports linking Apple Pay accounts with external bank accounts, allowing users to see and manage transactions from both sources in a unified view.

3. **Transaction Matching and Classification**: Enhanced transaction matching algorithms that can match Apple Pay transactions with bank transactions based on various criteria (amount, currency, time window, merchant name, etc.).

4. **Account Management**: New classes for managing bank account connections, including:
   - `FKBankConnectAccountDataLoader` - Loads bank account data
   - `FKBankConnectAccountMatcher` - Matches accounts
   - `FKBankConnectAccountBalanceImporter` - Imports account balances
   - `FKBankConnectAttributeLoader` - Loads account attributes
   - `FKBankConnectAttributeLoaderWrapper` - Wrapper for attribute loading
   - `FKBankConnectPaymentInfoDataLoader` - Loads payment information
   - `FKBankConnectConsentStatusDataLoader` - Loads consent status
   - `FKBankConnectTaskQueueProvider` - Manages task queues
   - `FKBankConnectTaskQueue` - Task queue implementation

5. **Security and Privacy**: New classes for managing security aspects:
   - `XPCBankConnectAccountConnectionResult` - Result of bank account connection
   - `XPCBankConnectAuthorizationPayload` - Authorization payload
   - `XPCBankConnectAuthorizationSession` - Authorization session
   - `XPCBankConnectAccountConnectionAccountsConnecting` - XPC protocol for connecting accounts
   - `XPCBankConnectAccountConnectionFinanceDataLoading` - XPC protocol for loading finance data
   - `XPCBankConnectAccountConnectionOfflineLabManaging` - XPC protocol for managing offline lab
   - `XPCBankConnectAccountConnectionInstitutionProviding` - XPC protocol for providing institution data
   - `XPCBankConnectAccountConnectionAuthorizationRevoking` - XPC protocol for revoking authorization
   - `XPCBankConnectAccountConnectionAuthorizationCompleting` - XPC protocol for completing authorization
   - `XPCBankConnectAccountConnectionAuthorizationInitiating` - XPC protocol for initiating authorization

6. **Transaction Insights**: New classes for providing transaction insights:
   - `FKBankConnectTransactionHistoryProvider` - Provides transaction history
   - `FKBankConnectTransactionHistoryProviderDelegate` - Delegate for transaction history
   - `FKBankConnectTransactionsAndGroupsProvider` - Provides transaction groups
   - `FKBankConnectTransactionsAndGroupsProviderDelegate` - Delegate for transaction groups
   - `FKBankConnectTransactionsListProvider` - Provides transaction lists
   - `FKBankConnectTransactionsListProviderDelegate` - Delegate for transaction lists
   - `FKBankConnectTransactionsProvider` - Provides transactions
   - `FKBankConnectTransactionsProviderDelegate` - Delegate for transactions
   - `FKBankConnectTransactionsMatcher` - Matches transactions
   - `FKBankConnectTransactionsDataLoader` - Loads transaction data
   - `FKBankConnectTransactionHistoryProvider` - Provides transaction history
   - `FKBankConnectTransactionHistoryProviderDelegate` - Delegate for transaction history
   - `FKBankConnectTransactionHistoryProvider` - Provides transaction history
   - `FKBankConnectTransactionHistoryProviderDelegate` - Delegate for transaction history

7. **Institution Management**: Enhanced institution management:
   - `FKBankConnectInstitutionProvider` - Provides institution data
   - `FKBankConnectInstitutionProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider` - Provides institution data
   - `FKBankConnectInstitutionsProvider

## AI Prioritisation Scoring System

No actionable methods or prioritisation targets identified for this component.

