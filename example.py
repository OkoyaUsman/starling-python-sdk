"""
Example usage of the Starling Bank Python SDK.

This file demonstrates how to use various endpoints of the SDK.
"""

from starling import StarlingClient
from datetime import datetime, timedelta

# Initialize the client
# Replace with your actual access token
ACCESS_TOKEN = "your_access_token_here"

# For production
client = StarlingClient(access_token=ACCESS_TOKEN)

# For sandbox/testing
# client = StarlingClient(access_token=ACCESS_TOKEN, sandbox=True)


def example_accounts():
    """Example: Working with accounts."""
    print("=== Accounts Examples ===")
    
    # Get all accounts
    accounts = client.accounts.get_accounts()
    print(f"Found {len(accounts.get('accounts', []))} accounts")
    
    if accounts.get('accounts'):
        account_uid = accounts['accounts'][0]['accountUid']
        
        # Get account balance
        balance = client.accounts.get_balance(account_uid)
        print(f"Cleared balance: {balance.get('clearedBalance', {}).get('minorUnits', 0) / 100}")
        
        # Get account identifiers
        identifiers = client.accounts.get_identifiers(account_uid)
        print(f"Account number: {identifiers.get('accountIdentifier')}")
        print(f"Sort code: {identifiers.get('bankIdentifier')}")
        
        # Check if funds are available
        confirmation = client.accounts.get_confirmation_of_funds(
            account_uid=account_uid,
            target_amount_in_minor_units=10000  # £100.00
        )
        print(f"Funds available: {confirmation.get('requestedAmountAvailableToSpend')}")


def example_transactions():
    """Example: Working with transactions."""
    print("\n=== Transaction Examples ===")
    
    # Get accounts first
    accounts = client.accounts.get_accounts()
    if not accounts.get('accounts'):
        print("No accounts found")
        return
    
    account_uid = accounts['accounts'][0]['accountUid']
    category_uid = accounts['accounts'][0]['defaultCategory']
    
    # Get recent transactions
    changes_since = datetime.now() - timedelta(days=7)
    transactions = client.feed.get_feed_items(
        account_uid=account_uid,
        category_uid=category_uid,
        changes_since=changes_since
    )
    
    feed_items = transactions.get('feedItems', [])
    print(f"Found {len(feed_items)} transactions")
    
    if feed_items:
        # Get details of first transaction
        first_item = feed_items[0]
        feed_item_uid = first_item.get('feedItemUid')
        
        if feed_item_uid:
            details = client.feed.get_feed_item(
                account_uid=account_uid,
                category_uid=category_uid,
                feed_item_uid=feed_item_uid
            )
            print(f"Transaction: {details.get('counterPartyName')}")
            print(f"Amount: £{details.get('amount', {}).get('minorUnits', 0) / 100}")
            
            # Update spending category
            # client.feed.update_spending_category(
            #     account_uid=account_uid,
            #     category_uid=category_uid,
            #     feed_item_uid=feed_item_uid,
            #     spending_category="GROCERIES"
            # )


def example_payments():
    """Example: Working with payments."""
    print("\n=== Payment Examples ===")
    
    # Get accounts
    accounts = client.accounts.get_accounts()
    if not accounts.get('accounts'):
        print("No accounts found")
        return
    
    account_uid = accounts['accounts'][0]['accountUid']
    category_uid = accounts['accounts'][0]['defaultCategory']
    
    # Get payees
    payees = client.payees.get_payees()
    payee_list = payees.get('payees', [])
    print(f"Found {len(payee_list)} payees")
    
    # Get standing orders
    standing_orders = client.payments.get_standing_orders(
        account_uid=account_uid,
        category_uid=category_uid
    )
    print(f"Found {len(standing_orders.get('standingOrders', []))} standing orders")
    
    # Example: Create a payment (commented out for safety)
    # payment = client.payments.create_payment(
    #     account_uid=account_uid,
    #     category_uid=category_uid,
    #     external_identifier=str(uuid.uuid4()),
    #     reference="Test payment",
    #     amount={"currency": "GBP", "minorUnits": 1000},  # £10.00
    #     destination_payee_account_uid="payee-account-uid"
    # )


def example_savings_goals():
    """Example: Working with savings goals."""
    print("\n=== Savings Goals Examples ===")
    
    # Get accounts
    accounts = client.accounts.get_accounts()
    if not accounts.get('accounts'):
        print("No accounts found")
        return
    
    account_uid = accounts['accounts'][0]['accountUid']
    
    # Get savings goals
    goals = client.savings_goals.get_savings_goals(account_uid)
    goal_list = goals.get('savingsGoalList', [])
    print(f"Found {len(goal_list)} savings goals")
    
    # Example: Create a savings goal (commented out for safety)
    # goal = client.savings_goals.create_savings_goal(
    #     account_uid=account_uid,
    #     name="Holiday Fund",
    #     currency="GBP",
    #     target={"currency": "GBP", "minorUnits": 100000}  # £1000.00
    # )
    # 
    # if goal.get('success'):
    #     savings_goal_uid = goal.get('savingsGoalUid')
    #     
    #     # Add money to savings goal
    #     transfer_uid = str(uuid.uuid4())
    #     result = client.savings_goals.add_money(
    #         account_uid=account_uid,
    #         savings_goal_uid=savings_goal_uid,
    #         transfer_uid=transfer_uid,
    #         amount={"currency": "GBP", "minorUnits": 5000},  # £50.00
    #         reference="Monthly savings"
    #     )


def example_account_holder():
    """Example: Working with account holder information."""
    print("\n=== Account Holder Examples ===")
    
    # Get account holder info
    account_holder = client.account_holders.get_account_holder()
    print(f"Account holder type: {account_holder.get('accountHolderType')}")
    
    # Get account holder name
    name = client.account_holders.get_account_holder_name()
    print(f"Account holder name: {name.get('accountHolderName')}")
    
    # Try to get individual details
    try:
        individual = client.account_holders.get_individual()
        print(f"Individual: {individual.get('firstName')} {individual.get('lastName')}")
    except Exception as e:
        print(f"Could not get individual details: {e}")


if __name__ == "__main__":
    print("Starling Bank Python SDK Examples")
    print("=" * 50)
    
    # Uncomment the examples you want to run
    # Make sure you have a valid access token set
    
    # example_accounts()
    # example_transactions()
    # example_payments()
    # example_savings_goals()
    # example_account_holder()
    
    print("\nNote: Examples are commented out. Uncomment and set ACCESS_TOKEN to use.")