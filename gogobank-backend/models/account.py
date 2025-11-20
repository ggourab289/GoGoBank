import uuid
class AccountSchema:
    def __init__(self,acc_id,name,pan,email,mobile,address,balance):
        self.acc_id = acc_id
        self.name = name
        self.pan = pan
        self.email = email
        self.mobile = mobile
        self.address = address
        self.balance = balance

    def to_dict(self):
        return {
            "id": self.acc_id,
            "name": self.name,
            "pan": self.pan,
            "email": self.email,
            "mobile": self.mobile,
            "address": self.address,
            "balance": self.balance
        }
    @staticmethod
    def from_dict(data:dict):
        return AccountSchema(
            acc_id=uuid.uuid4().hex,
            name=data.get('name'),
            pan=data.get('pan'),
            email=data.get('email'),
            mobile=data.get('mobile'),
            address=data.get('address'),
            balance=data.get('balance',0)
        )

