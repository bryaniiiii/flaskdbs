from flask import Flask, jsonify
import os
from sqlalchemy import create_engine
import sqlalchemy

app = Flask(__name__)

# DEFINE THE DATABASE CREDENTIALS
user = 'root'
password = ''
host = 'localhost'
port = 3306
database = 'bank'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bank'

# PYTHON FUNCTION TO CONNECT TO THE MYSQL DATABASE AND
# RETURN THE SQLACHEMY ENGINE OBJECT
def get_connection():
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        ).connect()
    )

url = "mysql://root:@localhost/bank"

@app.route('/')
def index():
    engine = create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        ))
    connection = engine.connect()
    metadata = sqlalchemy.MetaData()
    bank = sqlalchemy.Table('bankaccount', metadata, autoload=True, autoload_with=engine)
    print(bank.columns.keys())
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})




if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
