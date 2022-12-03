from flask import Flask, jsonify
import os
import sqlalchemy as db
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:lgy1DWXo2pvvFQeEix6x@containers-us-west-83.railway.app:7790/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)


class BankAccount(db.Model):
    __tablename__ = 'BankAccount'
    AccountID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, primary_key=True)
    AccountType = db.Column(db.VARCHAR(255), nullable=True)
    AccountBalance = db.Column(db.DECIMAL(10, 2), nullable=True)

    def __init__(self, AccountID, UserID, AccountType, AccountBalance):
        self.AccountID = AccountID
        self.UserID = UserID
        self.AccountType = AccountType
        self.AccountBalance = AccountBalance

    def json(self):
        return {"AccountID":self.AccountID, "UserID":self.UserID, "AccountType":self.AccountType, "AccountBalance": self.AccountBalance}


@app.route('/account/<string:UserID>', methods=["GET"])
def retrieve_accounts(UserID):
    try:
        bank_account_list = BankAccount.query.filter_by(UserID=UserID).all()
        if len(bank_account_list):
            return jsonify(
                {
                "code": 200,
                "data": {
                    "bank_account": [bank_account.json() for bank_account in bank_account_list]
                    }
                }
            )
    except:
        return jsonify(
            {
                "code": 404,
                "message": "There are no bank accounts."
            }
        ), 404
    
@app.route('/account/<string:UserID>/<string:AccountID>', methods=["GET"])
def retrieve_accounts_by_account_id(UserID,AccountID):
    try:
        bank_account = BankAccount.query.filter_by(UserID=UserID).filter_by(AccountID=AccountID).one()
        if (bank_account):
            return jsonify(
                {
                "code": 200,
                "data": bank_account.json()
                }
            )
    except:
        return jsonify(
            {
                "code": 404,
                "message": "There are no bank accounts."
            }
        ), 404

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=1010))