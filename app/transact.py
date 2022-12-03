from flask import Flask, jsonify
import os
from sqlalchemy import create_engine
import sqlalchemy


app = Flask(__name__)

# DEFINE THE DATABASE CREDENTIALS
# user = 'root'
# password = ''
# host = 'localhost'
# port = 3306
# database = 'bank'

# DEFINE RAILWAY
# 'mysql://root:lgy1DWXo2pvvFQeEix6x@containers-us-west-83.railway.app:7790/railway'
user = 'root'
password = 'lgy1DWXo2pvvFQeEix6x'
host = 'containers-us-west-83.railway.app'
port = 7790
database = 'railway'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bank'

# PYTHON FUNCTION TO CONNECT TO THE MYSQL DATABASE AND
# RETURN THE SQLACHEMY ENGINE OBJECT
def get_connection():
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        ).connect()
    )

@app.route('/')
def index():
    engine = create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        ))
    connection = engine.connect()
    metadata = sqlalchemy.MetaData()
    bank = sqlalchemy.Table('bankaccount', metadata, autoload=True, autoload_with=engine)
    print(bank.params())
    print(bank.columns.keys())
    transact = sqlalchemy.Table('scheduledtransactions', metadata, autoload=True, autoload_with=engine)
    print(transact.columns.keys())
    usertable = sqlalchemy.Table('user', metadata, autoload=True, autoload_with=engine)
    print(usertable.columns.keys())

    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route('/account/<string:UserID>', methods=["GET"])
def retrieve_accounts(UserID):
    try:
        engine = create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        ))
        connection = engine.connect()
        metadata = sqlalchemy.MetaData()
        bank = sqlalchemy.Table('bankaccount', metadata, autoload=True, autoload_with=engine)
        
        bank_account_list = BankAccount.query.filter_by(UserID=UserID).all()
        if len(bank_account_list):
            return jsonify(
                {
                "code": 200,
                "data": {
                    bank_account_list
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
    app.run(debug=True, port=os.getenv("PORT", default=5000))
