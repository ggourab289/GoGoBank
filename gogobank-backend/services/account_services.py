from resources.db import DB_HANDLER,ACCOUNTS
from models.exception import UserDataError 
from models.response_message import ResponseMessageHandler
from models.account import AccountSchema

class AccountServices:

    @staticmethod
    def validate_user_input(user_input:dict,validation_keys:list)->bool:
        '''Validate user input for required fields'''
        for key in validation_keys:
            if key not in user_input:
                raise UserDataError(f"Missing required field: {key}")
        return True

    @staticmethod
    def create_account(user_input):
        '''Create a new account after validating input and checking for duplicates'''
        AccountServices.validate_user_input(user_input, ['name', 'pan', 'mobile', 'address'])
        if not DB_HANDLER.search_account(user_input.get('pan'),'pan'):
            account = DB_HANDLER.add_account(
                AccountSchema.from_dict(user_input)
            )
            return ResponseMessageHandler.success_message("Account created successfully", data={"account_id": account.acc_id})
        raise UserDataError("Account with this PAN already exists")

    @staticmethod
    def get_balance( user_input):
        '''Retrieve account balance by id or aadhaar'''
        AccountServices.validate_user_input(user_input, ['id_number','id_name'])
        account =  DB_HANDLER.search_account(user_input.get('id_number'),user_input.get('id_name'))
        if account:
            return ResponseMessageHandler.success_message(
                message="Account balance retrieved successfully",
                data={"balance": account.balance}
            )
        raise UserDataError("Account not found")
    
    @staticmethod
    def get_user_details(user_input):
        '''Retrieve full account details by id or aadhaar'''
        AccountServices.validate_user_input(user_input, ['id_number','id_name'])
        account =  DB_HANDLER.search_account(user_input.get('id_number'),user_input.get('id_name'))
        if account:
            return ResponseMessageHandler.success_message(
                message="Account details retrieved successfully",
                data=account.to_dict()
            )
        raise UserDataError("Account not found")

    def deposit(self, user_input, amount):
        '''Deposit amount into account '''
        AccountServices.validate_user_input(user_input,['key','search_type'])
        account=DB_HANDLER.search_account(user_input.get('key'),user_input.get('search_type')) 
        if account:
            account.balance += amount
            return ResponseMessageHandler.success_message(
                message="Amount deposited successfully",
                data={"new_balance": account.balance}
            )
        raise UserDataError("Account not found")
        
        

    @staticmethod
    def get_all_accounts():
        '''Retrieve all accounts'''
        accounts = [account.to_dict() for account in ACCOUNTS]
        return accounts

    def withdraw(self, user_input, amount):
        '''Withdraw amount from account '''
        AccountServices.validate_user_input(user_input,['key','search_type'])
        account=DB_HANDLER.search_account(user_input.get('key'),user_input.get('search_type'))
        if account:
            if account.balance >= amount:
                account.balance -= amount
                return ResponseMessageHandler.success_message(
                    message="Amount withdrawn successfully",
                    data={"new_balance": account.balance}
                )
            else:
                raise UserDataError("Insufficient balance")
        raise UserDataError("Account not found")

    def delete_account(self, user_input):
        '''Delete account by id'''
        AccountServices.validate_user_input(user_input,['key','search_type'])
        account=DB_HANDLER.search_account(user_input.get('key'),user_input.get('search_type'))
        if account:
            DB_HANDLER.delete_account(account)
            return ResponseMessageHandler.success_message("Account deleted successfully")
        raise UserDataError("Account not found")