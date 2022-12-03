from flask import Flask, jsonify, request
import os
import sqlalchemy as db
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

app = Flask(__name__)

# LOCAL URI
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bank'

# RAILWAY URI
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
    Comment = db.Column(db.VARCHAR(255), nullable=True)

    def __init__(self, TransactionID, AccountID, ReceivingAccountID, Date, TransactionAmount, Comment):
        self.TransactionID = TransactionID
        self.AccountID = AccountID
        self.ReceivingAccountID = ReceivingAccountID
        self.Date = Date
        self.TransactionAmount = TransactionAmount
        self.Comment = Comment

    def json(self):
        return {"TransactionID":self.TransactionID, "AccountID":self.AccountID, "ReceivingAccountID":self.ReceivingAccountID, "Date": self.Date, "TransactionAmount": self.TransactionAmount, "Comment": self.Comment}


# GET TRANSACTIONS BY ACCOUNT_ID
@app.route('/transactions/<string:AccountID>', methods=["GET"])
def retrieve_transactions_by_user(AccountID):
    try:
        transaction_lists = TransactionAccount.query.filter_by(AccountID=AccountID).all()
        print(transaction_lists)
        if len(transaction_lists):
            return jsonify(
                {
                "code": 200,
                "data": {
                    "transaction_lists": [transaction_list.json() for transaction_list in transaction_lists]
                    }
                }
            )
    except:
        return jsonify(
            {
                "code": 404,
                "message": "There are no transactions."
            }
        ), 404

# GET 1 TRANSACTION
@app.route('/transactions/<string:AccountID>/<string:TransactionID>', methods=["GET"])
def retrieve_transaction_by_transaction_id(AccountID, TransactionID):
    try:
        transaction_list = TransactionAccount.query.filter_by(AccountID=AccountID, TransactionID=TransactionID).one()
        print(transaction_list)
        if (transaction_list):
            return jsonify(
                {
                "code": 200,
                "data": transaction_list.json()
                }
            )
    except:
        return jsonify(
            {
                "code": 404,
                "message": "There are no transactions."
            }
        ), 404

@app.route('/transactions/insertz', methods = ['POST'])
def insert_z():
    print(request.method)
    print(request.get_json())
    return "hi", 200

# POST 1 TRANSACTION
@app.route('/transactions/insert/', methods=["POST"])
def insert_transaction():
    try:
    
        if request.method == "POST":
            # print("Request:", request.get_json())
            data = request.get_json()
            TransactionID = data['TransactionID']
            AccountID = data['AccountID']
            if (TransactionAccount.query.filter_by(AccountID=AccountID) and TransactionAccount.query.filter_by(TransactionID=TransactionID)).first():
                return jsonify({
                    "code": 400,
                    "message": "Transaction already exists"
                }
                ), 400

            Date = data['Date']
            TransactionAmount = data['TransactionAmount']
            ReceivingAccountID = data['ReceivingAccountID']
            Comment = data['Comment']
            transaction = TransactionAccount(
                TransactionID=TransactionID, 
                AccountID=AccountID,
                ReceivingAccountID=ReceivingAccountID,
                Date = Date,
                TransactionAmount=TransactionAmount,
                Comment= Comment)

            db.session.add(transaction)
            db.session.commit()

            return jsonify({
                "code": 200,
                "data": transaction.json(),
                "message": "Added Transaction"
            }
            ), 200

    except Exception as e:
        return jsonify(
            {
                "code": 404,
                "message": "Error inserting transactions."
            }
        ), 404


# DELETE 1 TRANSACTION
@app.route('/transactions/delete/', methods=["DELETE"])
def delete_transaction_by_transaction_id():
    try:
        if request.method == "DELETE":
            data = request.get_json()
            TransactionID = data['TransactionID']
            AccountID = data['AccountID']
            transaction = TransactionAccount.query.filter_by(AccountID=AccountID, TransactionID=TransactionID).first()
            # print(transaction)
           
            if (transaction):
                db.session.delete(transaction)
                db.session.commit()
                return jsonify(
                    {
                    "code": 200,
                    "data": transaction.json()
                    }
                ), 200
            else:
                return jsonify({
                    "code": 400,
                    "message": "cannot find transaction."
                }), 400
    except Exception as e:
        return jsonify(
            {
                "code": 404,
                "message": e
            }
        ), 404

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=1012))