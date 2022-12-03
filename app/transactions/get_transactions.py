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


class TransactionAccount(db.Model):
    __tablename__ = 'ScheduledTransactions'
    TransactionID = db.Column(db.Integer, primary_key=True)
    AccountID = db.Column(db.Integer, primary_key=True)
    ReceivingAccountID = db.Column(db.Integer, nullable=True)
    Date = db.Column(db.VARCHAR(255), nullable=True)
    TransactionAmount = db.Column(db.DECIMAL(10, 2), nullable=True)

    def __init__(self, TransactionID, AccountID, ReceivingAccountID, Date, TransactionAmount):
        self.TransactionID = TransactionID
        self.AccountID = AccountID
        self.ReceivingAccountID = ReceivingAccountID
        self.Date = Date
        self.TransactionAmount = TransactionAmount

    def json(self):
        return {"TransactionID":self.TransactionID, "AccountID":self.AccountID, "ReceivingAccountID":self.ReceivingAccountID, "Date": self.Date, "TransactionAmount": self.TransactionAmount}


@app.route('/account/<string:TransactionID>', methods=["GET"])
def retrieve_accounts(UserID):
    try:
        bank_account_list = TransactionAccount.query.filter_by(UserID=UserID).all()
        if len(bank_account_list):
            return jsonify(
                {
                "code": 200,
                "data": {
                        bank_account_list.json()
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
    


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=1012))