from flask import Flask, request, jsonify, render_template
from models.exception import UserDataError
from models.response_message import ResponseMessageHandler
from services.account_services import AccountServices
import uuid
import logging 



who_visited = []
accounts = [
    {
        "aadhaar": "3340",
        "balance": 3457,
        "id": "4d0bff55-f8ac-4dad-86fd-dd6cebbcb434",
        "name": "sayak"
    },
    {
        "aadhaar": "9109",
        "balance": 1000,
        "id": "feb5e8db-8ec4-4be3-be9d-e256786a4254",
        "name": "gourab"
    }
]

# @app.route('/hello', methods=['POST'])
# def hello():
#     """
#     Endpoint that takes input from request body and returns a JSON response
#     Expected request body: {"name": "value"}
#     """
#     try:
#         data = request.get_json()
        
#         if not data:
#             return jsonify({"error": "No JSON data provided"}), 400
        
#         # Get the input from request body
#         input_value = data.get('input', 'World')
        
#         # Return JSON response
#         response = {
#             "message": f"Hello, {input_value}!",
#             "status": "success",
#             "input_received": input_value
#         }
        
#         return jsonify(response), 200
    
#     except Exception as e:
#         return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/health', methods=['GET'])
def beche_achi_ki():
    """Health check endpoint"""
    return "<h1>Beche achi</h1>", 200

def _check_if_already_exists(aadhaar: str) -> bool:
    for account in accounts:
        if account.get('aadhaar') == aadhaar:
            return True
    return False



@app.route('/create',methods=['POST'])
def create_account():
    """Create a new account with provided name and initial balance"""
    data = request.get_json()

    name = data.get('name')
    aadhaar = data.get('aadhaar')
    initial_balance = data.get('balance', 0.0)

    if name is None or aadhaar is None:
        return jsonify({"error": "Name and Aadhaar are required"}), 400

    acc_id = str(uuid.uuid4())
    if _check_if_already_exists(aadhaar):
        return jsonify({"error": "Account with this Aadhaar already exists"}), 400
    accounts.append(
        {
            "id": acc_id,
            "name": name,
            "aadhaar": aadhaar,
            "balance": initial_balance
        }
    )
    return jsonify(
        {
            "message": "Account created successfully",
            "account_id": acc_id,
        }
    )
def _find_account(id):
    for account in accounts:
        if account.get('id') == id:
            return account
    return None

@app.route('/find', methods=['POST'])
def find_account():
    """Find an account by Aadhaar number"""
    data = request.get_json()
    id = data.get('id')

    if not id:
        return jsonify({"error": "id is required"}), 400

    account=_find_account(id)
    if account:
        return jsonify(account), 200

    return jsonify({"error": "Account not found"}), 404

@app.route('/accounts', methods=['GET'])
def all_accounts():
    """Retrieve all accounts"""
    return jsonify(accounts), 200
    



    if not name:
        return jsonify({"error": "Name is required"}), 400

    account = {
        "name": name,
        "balance": initial_balance
    }
    accounts.append(account)

    return jsonify({"message": "Account created successfully", "account": account}), 201

@app.route('/deposit', methods=['PUT'])
def deposit_money():
    """Deposit amount into an account"""
    data = request.get_json()
    id = data.get('id')
    amount = data.get('amount')

    if not id:
        return jsonify({"error": "id is required"}), 400
    if amount is None or amount <= 100:
        return jsonify({"error": "Valid amount is required"}), 400

    account = _find_account(id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    account['balance'] += amount

    return jsonify({"message": "Deposit successful", "new_balance": account['balance']}), 200

@app.route('/withdraw', methods=['PUT'])
def withdraw_money():
    """Withdraw amount from an account"""
    data = request.get_json()
    id = data.get('id')
    amount = data.get('amount')

    if not id:
        return jsonify({"error": "id is required"}), 400
    if amount is None or amount <= 100:
        return jsonify({"error": "Valid amount is required"}), 400

    account = _find_account(id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    if account['balance'] < amount:
        return jsonify({"error": "Insufficient balance"}), 400

    account['balance'] -= amount

    return jsonify({"message": "Withdrawal successful", "new_balance": account['balance']}), 200

@app.route('/delete', methods=['DELETE'])
def delete_account():
    """Delete an account by ID"""
    data = request.get_json()
    id = data.get('id')

    if not id:
        return jsonify({"error": "id is required"}), 400

    account = _find_account(id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    accounts.remove(account)
    return jsonify({"message": "Account deleted successfully"}), 200