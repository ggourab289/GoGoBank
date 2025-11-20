from flask import  jsonify
class ResponseMessageHandler:
    @staticmethod
    def success_message(message: str, data:dict = None) -> dict:
        return jsonify({"status" : "Success","message": message,"Data" : data}), 200

    @staticmethod
    def error_message(message: str, status_code: int = 500) -> dict:
        return jsonify({"Status" : "Error","Message": message}), status_code