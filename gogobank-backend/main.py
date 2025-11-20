from flask import Flask, request, jsonify, render_template
from models.exception import UserDataError
from models.response_message import ResponseMessageHandler
from services.account_services import AccountServices
import logging 

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET'])
def main_ui():
    return render_template('index.html'), 200

@app.route('/create',methods=['POST'])
def create_account():
    try:
        return AccountServices.create_account(request.get_json())
    except UserDataError as ude:
        return ResponseMessageHandler.error_message(str(ude),402)
    except Exception as e:
        logging.error(f"Error in create_account: {str(e)}")
        return ResponseMessageHandler.error_message("Sorry! There is some server side problem",500)

@app.route("/all_accounts", methods=['GET'])
def all_accounts():
    try:
        accounts = AccountServices.get_all_accounts()
        return ResponseMessageHandler.success_message(
            message="All accounts retrieved successfully",
            data={"accounts": accounts}
        )
    except Exception as e:
        logging.error(f"Error in all_accounts: {str(e)}")
        return ResponseMessageHandler.error_message("Sorry! There is some server side problem",500)


@app.route('/find', methods=['GET'])
def find_account():
    try:
        return AccountServices.get_user_details(request.args)
    except UserDataError as ude:
        return ResponseMessageHandler.error_message(str(ude),402)
    except Exception as e:
        logging.error(f"Error in find_account: {str(e)}")
        return ResponseMessageHandler.error_message("Sorry! There is some server side problem",500)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
