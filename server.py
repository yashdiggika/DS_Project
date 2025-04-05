import socket
import threading
import time
from tabulate import tabulate
import logging
import json
import os

# --------------------- Configuration and Logging Setup ---------------------

# Set up logging (this logs to the console with timestamps)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Load configuration from a JSON file if it exists; otherwise use defaults.
config_file = 'config.json'
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
else:
    config = {
        "port": 9876,
        "interest_rate": 0.05,         # 5% interest rate for loan accounts
        "auto_interest_interval": 60   # auto-apply interest every 60 seconds
    }

# --------------------- Bank Class Definition ---------------------

class Bank:
    def __init__(self):
        # List of accounts. Each account is a dictionary containing:
        # acct_num, acct_type, init_acct_holder, acct_holder, balance, history, lock
        self.accounts = [
            {'acct_num': 1001, 'acct_type': 'checking', 'init_acct_holder': 'Alice',
             'acct_holder': ['Alice', 'Jason', 'David'], 'balance': 2100, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1002, 'acct_type': 'loan', 'init_acct_holder': 'Alice',
             'acct_holder': ['Alice', 'Jason', 'David'], 'balance': -300, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1003, 'acct_type': 'checking', 'init_acct_holder': 'Bob',
             'acct_holder': ['Bob', 'Ivan', 'Kevin'], 'balance': 3500, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1004, 'acct_type': 'loan', 'init_acct_holder': 'Bob',
             'acct_holder': ['Bob', 'Ivan', 'Paul'], 'balance': -900, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1005, 'acct_type': 'checking', 'init_acct_holder': 'Charlie',
             'acct_holder': ['Charlie', 'Dave'], 'balance': 9100, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1006, 'acct_type': 'loan', 'init_acct_holder': 'Charlie',
             'acct_holder': ['Charlie', 'Dave', 'Gary'], 'balance': -3200, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1007, 'acct_type': 'checking', 'init_acct_holder': 'Dave',
             'acct_holder': ['Dave', 'Thomas', 'Henry'], 'balance': 200, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1008, 'acct_type': 'loan', 'init_acct_holder': 'Dave',
             'acct_holder': ['Dave', 'James', 'Gary'], 'balance': -300, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1009, 'acct_type': 'checking', 'init_acct_holder': 'Frank',
             'acct_holder': ['Frank', 'Grace', 'Charlie'], 'balance': 4000, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1010, 'acct_type': 'loan', 'init_acct_holder': 'Frank',
             'acct_holder': ['Frank', 'Adam', 'Steven'], 'balance': -900, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1011, 'acct_type': 'checking', 'init_acct_holder': 'Grace',
             'acct_holder': ['Grace', 'Adam', 'Heidi'], 'balance': 3000, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1012, 'acct_type': 'loan', 'init_acct_holder': 'Grace',
             'acct_holder': ['Grace', 'Robert', 'Larry'], 'balance': -100, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1013, 'acct_type': 'checking', 'init_acct_holder': 'Heidi',
             'acct_holder': ['Heidi', 'Mark', 'Kate'], 'balance': 500, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1014, 'acct_type': 'loan', 'init_acct_holder': 'Heidi',
             'acct_holder': ['Heidi', 'Ivan', 'Dave'], 'balance': -200, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1015, 'acct_type': 'checking', 'init_acct_holder': 'Ivan',
             'acct_holder': ['Ivan', 'Charlie', 'Bob'], 'balance': 5000, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1016, 'acct_type': 'loan', 'init_acct_holder': 'Ivan',
             'acct_holder': ['Ivan', 'Michael', 'Mark'], 'balance': -2100, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1017, 'acct_type': 'checking', 'init_acct_holder': 'John',
             'acct_holder': ['John', 'Raymond', 'Dave'], 'balance': 6200, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1018, 'acct_type': 'loan', 'init_acct_holder': 'John',
             'acct_holder': ['John', 'Frank', 'Justin'], 'balance': -2000, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1019, 'acct_type': 'checking', 'init_acct_holder': 'Kate',
             'acct_holder': ['Kate', 'Kevin', 'Justin'], 'balance': 5200, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1020, 'acct_type': 'loan', 'init_acct_holder': 'Kate',
             'acct_holder': ['Kate', 'Thomas', 'James'], 'balance': -1800, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1021, 'acct_type': 'checking', 'init_acct_holder': 'James',
             'acct_holder': ['James', 'John', 'Grace'], 'balance': 8700, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1022, 'acct_type': 'loan', 'init_acct_holder': 'James',
             'acct_holder': ['James', 'Larry', 'Alice'], 'balance': -700, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1023, 'acct_type': 'checking', 'init_acct_holder': 'Michael',
             'acct_holder': ['Michael', 'Jason', 'Eve'], 'balance': 7400, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1024, 'acct_type': 'loan', 'init_acct_holder': 'Michael',
             'acct_holder': ['Michael', 'Ivan', 'Gary'], 'balance': -4900, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1025, 'acct_type': 'checking', 'init_acct_holder': 'Robert',
             'acct_holder': ['Robert', 'Frank', 'Grace'], 'balance': 8400, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1026, 'acct_type': 'loan', 'init_acct_holder': 'Robert',
             'acct_holder': ['Robert', 'Ivan', 'Justin'], 'balance': -400, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1027, 'acct_type': 'checking', 'init_acct_holder': 'William',
             'acct_holder': ['William', 'Alice', 'Heidi'], 'balance': 6600, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1028, 'acct_type': 'loan', 'init_acct_holder': 'William',
             'acct_holder': ['William', 'Justin', 'Henry'], 'balance': -5000, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1029, 'acct_type': 'checking', 'init_acct_holder': 'David',
             'acct_holder': ['David', 'Raymond', 'Bob'], 'balance': 2400, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1030, 'acct_type': 'loan', 'init_acct_holder': 'David',
             'acct_holder': ['David', 'Kate', 'Mark'], 'balance': -200, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1031, 'acct_type': 'checking', 'init_acct_holder': 'Thomas',
             'acct_holder': ['Thomas', 'Charlie', 'Dave'], 'balance': 8700, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1032, 'acct_type': 'loan', 'init_acct_holder': 'Thomas',
             'acct_holder': ['Thomas', 'Grace', 'Robert'], 'balance': -2900, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1033, 'acct_type': 'checking', 'init_acct_holder': 'Mark',
             'acct_holder': ['Mark', 'Steven', 'Justin'], 'balance': 7800, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1034, 'acct_type': 'loan', 'init_acct_holder': 'Mark',
             'acct_holder': ['Mark', 'Paul', 'Bob'], 'balance': -5900, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1035, 'acct_type': 'checking', 'init_acct_holder': 'Steven',
             'acct_holder': ['Steven', 'Grace', 'William'], 'balance': 2400, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1036, 'acct_type': 'loan', 'init_acct_holder': 'Steven',
             'acct_holder': ['Steven', 'David', 'Justin'], 'balance': -1900, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1037, 'acct_type': 'checking', 'init_acct_holder': 'Paul',
             'acct_holder': ['Paul', 'Charlie', 'Steven'], 'balance': 7800, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1038, 'acct_type': 'loan', 'init_acct_holder': 'Paul',
             'acct_holder': ['Paul', 'Eve', 'Dave'], 'balance': -2500, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1039, 'acct_type': 'checking', 'init_acct_holder': 'Kevin',
             'acct_holder': ['Kevin', 'Kate', 'Larry'], 'balance': 4400, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1040, 'acct_type': 'loan', 'init_acct_holder': 'Kevin',
             'acct_holder': ['Kevin', 'Ivan', 'James'], 'balance': -800, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1041, 'acct_type': 'checking', 'init_acct_holder': 'Jason',
             'acct_holder': ['Jason', 'Adam', 'Henry'], 'balance': 1400, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1042, 'acct_type': 'loan', 'init_acct_holder': 'Jason',
             'acct_holder': ['Jason', 'Raymond', 'William'], 'balance': -200, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1043, 'acct_type': 'checking', 'init_acct_holder': 'Gary',
             'acct_holder': ['Gary', 'Larry', 'Ivan'], 'balance': 3400, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1044, 'acct_type': 'loan', 'init_acct_holder': 'Gary',
             'acct_holder': ['Gary', 'Frank', 'James'], 'balance': -900, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1045, 'acct_type': 'checking', 'init_acct_holder': 'Larry',
             'acct_holder': ['Larry', 'Frank', 'Heidi'], 'balance': 5400, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1046, 'acct_type': 'loan', 'init_acct_holder': 'Larry',
             'acct_holder': ['Larry', 'William', 'David'], 'balance': -300, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1047, 'acct_type': 'checking', 'init_acct_holder': 'Justin',
             'acct_holder': ['Justin', 'John', 'Dave'], 'balance': 3400, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1048, 'acct_type': 'loan', 'init_acct_holder': 'Justin',
             'acct_holder': ['Justin', 'Charlie', 'Alice'], 'balance': -1500, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1049, 'acct_type': 'checking', 'init_acct_holder': 'Raymond',
             'acct_holder': ['Raymond', 'Henry', 'James'], 'balance': 9400, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1050, 'acct_type': 'loan', 'init_acct_holder': 'Raymond',
             'acct_holder': ['Raymond', 'Steven', 'Mark'], 'balance': -6900, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1051, 'acct_type': 'checking', 'init_acct_holder': 'Adam',
             'acct_holder': ['Adam', 'Charlie', 'Michael'], 'balance': 5400, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1052, 'acct_type': 'loan', 'init_acct_holder': 'Adam',
             'acct_holder': ['Adam', 'Larry', 'Jason'], 'balance': -4600, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1053, 'acct_type': 'checking', 'init_acct_holder': 'Henry',
             'acct_holder': ['Henry', 'Henry', 'James'], 'balance': 8300, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1054, 'acct_type': 'loan', 'init_acct_holder': 'Henry',
             'acct_holder': ['Henry', 'Steven', 'Mark'], 'balance': -1800, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1055, 'acct_type': 'checking', 'init_acct_holder': 'Eve',
             'acct_holder': ['Eve', 'Michael', 'Justin'], 'balance': 2200, 'history': [], 'lock': threading.Lock()},
            {'acct_num': 1056, 'acct_type': 'loan', 'init_acct_holder': 'Eve',
             'acct_holder': ['Eve', 'William', 'Alice'], 'balance': -400, 'history': [], 'lock': threading.Lock()}
        ]

    def create_account(self, data_dict):
        # Check if the user already has an account
        for account in self.accounts:
            if account['init_acct_holder'] == data_dict['user']:
                return "One person can only create one account"
        # Check if the account number specified by the user is already in use
        for account in self.accounts:
            if int(account['acct_num']) == int(data_dict['acct_num']):
                return f"The account number has been used by {account['init_acct_holder']}"
        # Create new account
        new_account = {
            'acct_num': int(data_dict['acct_num']),
            'acct_type': 'checking',
            'init_acct_holder': data_dict['user'],
            'acct_holder': [data_dict['user']],
            'balance': int(data_dict.get('amount', 0)),
            'history': [],
            'lock': threading.Lock()
        }
        # Add new account to the list
        self.accounts.append(new_account)
        return f"Successfully created checking account for {data_dict['user']} with account number {int(data_dict['acct_num'])}。"

    def show_bank(self, data_dict):
        # Check if the user is 'Audit'
        if data_dict['user'] != 'Audit':
            return "Access denied: only Audit can view all bank accounts"
        # Prepare data for table format
        table_data = []
        for account in self.accounts:
            row = [
                account['acct_num'],
                account['acct_type'],
                account['init_acct_holder'],
                ', '.join(account['acct_holder']),
                account['balance'],
                account['history']
            ]
            table_data.append(row)
        headers = ["acct_num", "acct_type", "init_holder", "acct_holder", "balance", "history"]
        formatted_table = tabulate(table_data, headers=headers, tablefmt="plain")
        return f"All account information is as follows:\n{formatted_table}"

    def show_accountholders(self, data_dict):
        # Check if the user is the account initiate holder
        for account in self.accounts:
            if account['acct_num'] == int(data_dict['acct_num']):
                if account['init_acct_holder'] == data_dict['user']:
                    holders = ", ".join(account['acct_holder'])
                    return f"All the account holders for account {data_dict['acct_num']} are: {holders}"
                else:
                    return "Only the account initiate holder has access to view all account holders"
        return "The account number was not found"

    def deposit(self, data_dict):
        for account in self.accounts:
            if account['acct_num'] == int(data_dict['acct_num']):
                amount = int(data_dict.get('amount', 0))
                if amount < 0:
                    return "Deposit amount must be positive"
                elif amount == 0:
                    return f"The current balance for account {data_dict['acct_num']} is {account['balance']} dollars"
                account['lock'].acquire()
                logging.info("Locking account %s for deposit", account['acct_num'])
                try:
                    time.sleep(3)
                    account['balance'] += amount
                    account['history'].append((data_dict['user'], 'deposit', amount))
                    return f"Successfully deposited {amount} dollars into account {data_dict['acct_num']}, current balance is {account['balance']} dollars"
                finally:
                    account['lock'].release()
                    logging.info("Unlocked account %s after deposit", account['acct_num'])
        return "The account number was not found"

    def withdraw(self, data_dict):
        for account in self.accounts:
            if account['acct_num'] == int(data_dict['acct_num']):
                amount = int(data_dict.get('amount', 0))
                if amount < 0:
                    return "The withdrawal amount must be a positive number"
                elif amount == 0:
                    return f"The current balance for account {data_dict['acct_num']} is {account['balance']} dollars"
                if data_dict['user'] not in account['acct_holder']:
                    return "Only the account holder can withdraw"
                if account['balance'] < amount:
                    return f"The account balance is insufficient and the current balance is {account['balance']}"
                account['lock'].acquire()
                logging.info("Locking account %s for withdrawal", account['acct_num'])
                try:
                    time.sleep(3)
                    account['balance'] -= amount
                    account['history'].append((data_dict['user'], 'withdraw', amount))
                    return f"{data_dict['user']} successfully withdrew {amount} dollars from account {data_dict['acct_num']}. Current balance is {account['balance']}"
                finally:
                    account['lock'].release()
                    logging.info("Unlocked account %s after withdrawal", account['acct_num'])
        return "The account number was not found"

    def transfer_to(self, data_dict):
        amount = int(data_dict.get('amount', 0))
        if amount <= 0:
            return "The transfer amount must be a positive number"
        user_account = None
        for account in self.accounts:
            if account['init_acct_holder'] == data_dict['user']:
                user_account = account
                break
        if user_account is None:
            return "The user must be an initiate cardholder of an account in the bank in order to perform a transfer operation"
        target_account = None
        for account in self.accounts:
            if account['acct_num'] == int(data_dict['acct_num']):
                target_account = account
                break
        if target_account is None:
            return "Target account does not exist"
        if user_account['balance'] < amount:
            return f"The account balance is insufficient and the current balance is {user_account['balance']}"
        first_lock, second_lock = (user_account, target_account) if user_account['acct_num'] < target_account['acct_num'] else (target_account, user_account)
        first_lock['lock'].acquire()
        logging.info("Locking account %s for transfer", first_lock['acct_num'])
        second_lock['lock'].acquire()
        logging.info("Locking account %s for transfer", second_lock['acct_num'])
        try:
            time.sleep(3)
            user_account['balance'] -= amount
            target_account['balance'] += amount
            user_account['history'].append((data_dict['user'], 'transfer_out', amount, data_dict['acct_num']))
            target_account['history'].append((data_dict['user'], 'transfer_in', amount, user_account['acct_num']))
            return (f"{data_dict['user']} successfully transferred {amount} dollars from account {user_account['acct_num']} "
                    f"to account {data_dict['acct_num']}. Current balance for source account is {user_account['balance']} and target account is {target_account['balance']}.")
        finally:
            first_lock['lock'].release()
            logging.info("Unlocked account %s after transfer", first_lock['acct_num'])
            second_lock['lock'].release()
            logging.info("Unlocked account %s after transfer", second_lock['acct_num'])

    def pay_loan_check(self, data_dict):
        acct_num = int(data_dict['acct_num'])
        amount = int(data_dict.get('amount', 0))
        if amount <= 0:
            return "Repayment amount must be positive"
        for account in self.accounts:
            if account['acct_num'] == acct_num:
                if account['acct_type'] != 'loan':
                    return "The target account is not a loan account and cannot do repayment operation."
                if data_dict['user'] not in account['acct_holder']:
                    return "Only account holders can make repayments on this loan account"
                account['lock'].acquire()
                logging.info("Locking loan account %s for repayment (check)", account['acct_num'])
                try:
                    account['balance'] += amount
                    account['history'].append((data_dict['user'], 'pay_loan', amount))
                    return f"{data_dict['user']} successfully paid {amount} dollars to account {acct_num}. Current loan is {account['balance']}"
                finally:
                    account['lock'].release()
                    logging.info("Unlocked loan account %s after repayment (check)", account['acct_num'])
        return "The loan account was not found"

    def pay_loan_transfer_to(self, data_dict):
        acct_num = int(data_dict['acct_num'])
        amount = int(data_dict.get('amount', 0))
        if amount <= 0:
            return "Repayment amount must be positive"
        user_account = None
        for account in self.accounts:
            if account['init_acct_holder'] == data_dict['user'] and account['acct_type'] == 'checking':
                user_account = account
                break
        if user_account is None:
            return "The user's initial checking account has not been found and the repayment operation cannot be performed."
        if user_account['balance'] < amount:
            return f"Insufficient balance, current balance is {user_account['balance']}"
        loan_account = None
        for account in self.accounts:
            if account['acct_num'] == acct_num:
                if account['acct_type'] == 'loan':
                    loan_account = account
                    break
        if loan_account is None:
            return "Loan account not found"
        if data_dict['user'] not in loan_account['acct_holder']:
            return "Only loan account holders can make repayment"
        first_lock, second_lock = (user_account, loan_account) if user_account['acct_num'] < loan_account['acct_num'] else (loan_account, user_account)
        first_lock['lock'].acquire()
        logging.info("Locking account %s for loan transfer", first_lock['acct_num'])
        second_lock['lock'].acquire()
        logging.info("Locking account %s for loan transfer", second_lock['acct_num'])
        try:
            user_account['balance'] -= amount
            loan_account['balance'] += amount
            user_account['history'].append((data_dict['user'], 'transfer_to_loan', amount, acct_num))
            loan_account['history'].append((data_dict['user'], 'loan_payment_received', amount, user_account['acct_num']))
            return (f"{data_dict['user']} successfully transferred {amount} dollars from account {user_account['acct_num']} for repayment. "
                    f"Current loan for account {acct_num} is {loan_account['balance']}")
        finally:
            first_lock['lock'].release()
            logging.info("Unlocked account %s after loan transfer", first_lock['acct_num'])
            second_lock['lock'].release()
            logging.info("Unlocked account %s after loan transfer", second_lock['acct_num'])

    def show_history(self, data_dict):
        acct_num = int(data_dict['acct_num'])
        for account in self.accounts:
            if account['acct_num'] == acct_num:
                if data_dict['user'] not in account['acct_holder']:
                    return "Only account holders can view the operation history of the account"
                if not account['history']:
                    return f"Account {acct_num} doesn't have any history now"
                history_records = "\n".join([str(record) for record in account['history']])
                return f"The operation history of account {acct_num} is \n{history_records}"
        return "The account number was not found"

    # --------------------- Additional Improvements ---------------------

    def apply_interest(self):
        """Apply interest rate to all loan accounts."""
        interest_rate = config.get("interest_rate", 0.05)
        for account in self.accounts:
            if account['acct_type'] == 'loan':
                account['lock'].acquire()
                try:
                    old_balance = account['balance']
                    new_balance = int(old_balance * (1 + interest_rate))
                    account['history'].append(("System", "interest", new_balance - old_balance))
                    account['balance'] = new_balance
                    logging.info("Applied interest to loan account %s: old balance %s, new balance %s", account['acct_num'], old_balance, new_balance)
                finally:
                    account['lock'].release()

    def apply_interest_command(self, data_dict):
        """Command handler to manually trigger interest calculation."""
        if data_dict['user'] != 'Audit':
            return "Only Audit can apply interest."
        self.apply_interest()
        return "Interest applied to all loan accounts."

    def show_history_filtered(self, data_dict):
        """Show transaction history filtered by an operation type (if provided)."""
        acct_num = int(data_dict['acct_num'])
        operation_filter = data_dict.get('operation', None)
        for account in self.accounts:
            if account['acct_num'] == acct_num:
                if data_dict['user'] not in account['acct_holder']:
                    return "Only account holders can view the operation history of the account"
                filtered_history = []
                for record in account['history']:
                    if operation_filter is None or (len(record) >= 2 and record[1] == operation_filter):
                        filtered_history.append(record)
                if not filtered_history:
                    return f"No transactions found for operation '{operation_filter}' in account {acct_num}"
                history_records = "\n".join([str(record) for record in filtered_history])
                return f"The filtered operation history of account {acct_num} is \n{history_records}"
        return "The account number was not found"

# --------------------- End of Bank Class ---------------------

def handle_client(client_socket, bank):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        pairs = data.decode().split()
        data_dict = dict(pair.split('=') for pair in pairs)
        if len(data_dict) < 3:
            response = "Invalid request format."
            client_socket.send(response.encode())
            continue
        logging.info("Request received: user=%s command=%s account=%s, amount=%s",
                     data_dict['user'], data_dict['command'], data_dict['acct_num'], data_dict.get('amount', 0))
        if data_dict['command'] == 'create_account':
            response = bank.create_account(data_dict)
            client_socket.send(response.encode())
            client_socket.send(b"END")
        elif data_dict['command'] == 'show_bank':
            response = bank.show_bank(data_dict)
            for i in range(0, len(response), 1024):
                client_socket.send(response[i:i + 1024].encode())
            client_socket.send(b"END")
            continue
        elif data_dict['command'] == 'show_accountholders':
            response = bank.show_accountholders(data_dict)
            client_socket.send(response.encode())
            client_socket.send(b"END")
        elif data_dict['command'] == 'deposit':
            response = bank.deposit(data_dict)
            client_socket.send(response.encode())
            client_socket.send(b"END")
        elif data_dict['command'] == 'withdraw':
            response = bank.withdraw(data_dict)
            client_socket.send(response.encode())
            client_socket.send(b"END")
        elif data_dict['command'] == 'transfer_to':
            response = bank.transfer_to(data_dict)
            client_socket.send(response.encode())
            client_socket.send(b"END")
        elif data_dict['command'] == 'pay_loan_check':
            response = bank.pay_loan_check(data_dict)
            client_socket.send(response.encode())
            client_socket.send(b"END")
        elif data_dict['command'] == 'pay_loan_transfer_to':
            response = bank.pay_loan_transfer_to(data_dict)
            client_socket.send(response.encode())
            client_socket.send(b"END")
        elif data_dict['command'] == 'show_history':
            response = bank.show_history(data_dict)
            client_socket.send(response.encode())
            client_socket.send(b"END")
        elif data_dict['command'] == 'apply_interest':
            response = bank.apply_interest_command(data_dict)
            client_socket.send(response.encode())
            client_socket.send(b"END")
        elif data_dict['command'] == 'show_history_filtered':
            response = bank.show_history_filtered(data_dict)
            client_socket.send(response.encode())
            client_socket.send(b"END")
        else:
            response = "Invalid command."
            client_socket.send(response.encode())
            client_socket.send(b"END")
        logging.info("Request handled: %s", data_dict['command'])
        time.sleep(1)
    client_socket.close()

def interest_thread(bank):
    while True:
        time.sleep(config.get("auto_interest_interval", 60))
        bank.apply_interest()
        logging.info("Auto-applied interest to all loan accounts.")

# --------------------- Main Server Setup ---------------------

HOST = socket.gethostbyname(socket.gethostname())
PORT = config.get("port", 9876)
ADDR = (HOST, PORT)
bank = Bank()

# Start the auto-interest thread as a daemon thread.
auto_interest = threading.Thread(target=interest_thread, args=(bank,), daemon=True)
auto_interest.start()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)
server_socket.listen()
logging.info("Server listening on host %s on port %s...", HOST, PORT)

while True:
    client_socket, addr = server_socket.accept()
    logging.info("Client connected from %s", addr)
    thread = threading.Thread(target=handle_client, args=(client_socket, bank))
    thread.start()
    logging.info("%s thread connections running...", threading.active_count() - 1)
