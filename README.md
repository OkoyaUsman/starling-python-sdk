# Starling Bank Python SDK

A comprehensive Python wrapper for the Starling Bank API. This SDK provides easy-to-use methods for interacting with all up to date Starling Bank API endpoints.

> **⚠️ Disclaimer:** This library is unofficial, and not associated formally with Starling Bank. It is a hobbyist project by myself.

## Features

- ✅ Complete coverage of all Starling Bank API endpoints
- 🎯 Type hints for better IDE support
- 🔒 OAuth2 authentication support
- 🧪 Sandbox environment support
- 📝 Comprehensive error handling
- 🚀 Easy to use and well-documented

## Installation

```bash
pip install starling-sdk
```

Or install from source:

```bash
git clone https://github.com/okoyausman/starling-python-sdk.git
cd starling-python-sdk
pip install -e .
```

## Quick Start

```python
from starling import StarlingClient

# Initialize the client with your access token
client = StarlingClient(access_token="your_access_token")

# Or use sandbox environment
client = StarlingClient(access_token="your_access_token", sandbox=True)

# Get accounts
accounts = client.accounts.get_accounts()

# Get account balance
balance = client.accounts.get_balance(account_uid="your-account-uid")

# Get transactions
from datetime import datetime, timedelta
transactions = client.feed.get_feed_items(
    account_uid="your-account-uid",
    category_uid="your-category-uid",
    changes_since=datetime.now() - timedelta(days=30)
)
```

## API Coverage

This SDK implements all Starling Bank API endpoints:

### Accounts
- Get accounts
- Get account balance
- Get account identifiers
- Get confirmation of funds
- Download feed export

### Account Holders
- Get account holder information
- Business account holder details
- Individual account holder details
- Joint account holder details
- Sole trader details
- Profile images

### Addresses
- Get addresses
- Update address

### Cards
- Get cards
- Update card controls (lock, ATM, online, POS, mobile wallet, gambling, magstripe, currency switch)

### Direct Debit Mandates
- Get mandates
- Get mandate details
- Get mandate payments
- Cancel mandate

### Transaction Feed
- Get feed items
- Get transactions between dates
- Get settled transactions
- Get feed item details
- Update spending category
- Update user note
- Manage attachments
- Manage receipts
- Round-up functionality

### Identity
- Get token identity
- Get authorising individual
- Logout

### Payments
- Create payment
- Get payment order
- Get payment order payments
- Standing orders (create, update, cancel, get upcoming payments)

### Payees
- Get payees
- Create payee
- Update payee
- Delete payee
- Manage payee accounts
- Get scheduled payments
- Get payment history
- Get payee image

### Savings Goals
- Get savings goals
- Create savings goal
- Update savings goal
- Delete savings goal
- Add money
- Withdraw money
- Manage recurring transfers
- Get savings goal photo

### Settle Up
- Get Settle Up profile

### Spaces
- Get spaces
- Get spending space
- Get space photo

## Usage Examples

### Accounts

```python
# Get all accounts
accounts = client.accounts.get_accounts()

# Get account balance
balance = client.accounts.get_balance(account_uid="account-uid")

# Check if funds are available
confirmation = client.accounts.get_confirmation_of_funds(
    account_uid="account-uid",
    target_amount_in_minor_units=10000  # £100.00 in pence
)
```

### Transactions

```python
from datetime import datetime, timedelta

# Get recent transactions
transactions = client.feed.get_feed_items(
    account_uid="account-uid",
    category_uid="category-uid",
    changes_since=datetime.now() - timedelta(days=7)
)

# Get transactions between dates
transactions = client.feed.get_transactions_between(
    account_uid="account-uid",
    category_uid="category-uid",
    min_transaction_timestamp=datetime(2023, 1, 1),
    max_transaction_timestamp=datetime(2023, 12, 31)
)

# Update spending category
client.feed.update_spending_category(
    account_uid="account-uid",
    category_uid="category-uid",
    feed_item_uid="feed-item-uid",
    spending_category="GROCERIES"
)
```

### Payments

```python
import uuid

# Create a payment
payment = client.payments.create_payment(
    account_uid="account-uid",
    category_uid="category-uid",
    external_identifier=str(uuid.uuid4()),
    reference="Payment reference",
    amount={"currency": "GBP", "minorUnits": 1000},  # £10.00
    destination_payee_account_uid="payee-account-uid"
)

# Create a standing order
standing_order = client.payments.create_standing_order(
    account_uid="account-uid",
    category_uid="category-uid",
    external_identifier=str(uuid.uuid4()),
    reference="Monthly rent",
    amount={"currency": "GBP", "minorUnits": 50000},  # £500.00
    standing_order_recurrence={
        "recurrenceRule": "MONTHLY",
        "recurrenceRuleUid": "recurrence-rule-uid"
    },
    destination_payee_account_uid="payee-account-uid"
)
```

### Savings Goals

```python
import uuid

# Create a savings goal
goal = client.savings_goals.create_savings_goal(
    account_uid="account-uid",
    name="Holiday Fund",
    currency="GBP",
    target={"currency": "GBP", "minorUnits": 100000}  # £1000.00
)

# Add money to savings goal
transfer_uid = str(uuid.uuid4())
result = client.savings_goals.add_money(
    account_uid="account-uid",
    savings_goal_uid="savings-goal-uid",
    transfer_uid=transfer_uid,
    amount={"currency": "GBP", "minorUnits": 5000},  # £50.00
    reference="Monthly savings"
)
```

## Error Handling

The SDK provides specific exception types for different error scenarios:

```python
from starling import (
    StarlingClient,
    StarlingAuthenticationError,
    StarlingForbiddenError,
    StarlingNotFoundError,
    StarlingBadRequestError,
    StarlingServerError,
)

try:
    balance = client.accounts.get_balance(account_uid="account-uid")
except StarlingAuthenticationError:
    print("Authentication failed - check your access token")
except StarlingForbiddenError:
    print("You don't have permission to access this resource")
except StarlingNotFoundError:
    print("Resource not found")
except StarlingBadRequestError as e:
    print(f"Bad request: {e}")
except StarlingServerError:
    print("Server error - please try again later")
```

## OAuth Scopes

Different endpoints require different OAuth scopes. Make sure your access token has the required scopes:

- `account:read` - Read account information
- `balance:read` - Read account balance
- `transaction:read` - Read transactions
- `transaction:edit` - Edit transactions
- `pay-local:create` - Create payments
- `savings-goal:read` - Read savings goals
- `savings-goal:create` - Create savings goals
- And many more...

See the [Starling Bank API documentation](https://developer.starlingbank.com/) for the complete list of scopes.

## Sandbox Environment

To use the sandbox environment for testing:

```python
client = StarlingClient(
    access_token="your_sandbox_access_token",
    sandbox=True
)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This library is unofficial, and not associated formally with Starling Bank. It is a hobbyist project by myself. Use at your own risk. Always refer to the official [Starling Bank API documentation](https://developer.starlingbank.com/) for the most up-to-date information.

## Support

For issues and questions:
- Open an issue on GitHub
- Check the [Starling Bank API documentation](https://developer.starlingbank.com/)