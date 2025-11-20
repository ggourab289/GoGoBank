from models.exception import UserDataError
ACCOUNTS = []  # In-memory database for demonstration purposes

class DB_HANDLER:
    @staticmethod
    def search_account(key:str,search_type:str):
        if search_type not in ['acc_id','pan']:
            raise UserDataError("Invalid search type")
        for account in ACCOUNTS:
            if getattr(account,search_type) == key:
                return account
        return None

    @staticmethod
    def add_account(account_data):
        ACCOUNTS.append(account_data)
        return account_data

    @staticmethod
    def update_account(account_id, update_data):
        
    @staticmethod
    def delete_account(account_id):
        pass
