import os

from flask import Flask, jsonify, make_response, session,request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
from functools import wraps
import mysql.connector
from app.login.login import UserModel
from app.login.login import Login
from app.account.get_account_info import BankAccount
from sharemodels import db
from flask_cors import CORS, cross_origin






app = Flask(__name__)

api = Api(app)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:lgy1DWXo2pvvFQeEix6x@containers-us-west-83.railway.app:7790/railway"
app.config['CORS_HEADERS'] = 'Content-Type'
db.init_app(app)


@app.route('/')
def index():
    result = UserModel.query.filter_by(UserID=1).first()
    return {"message": result.UserID}


@app.route("/user/<string:UserID>", methods=['GET'])
def getUserDetails(UserID):

        # try:
        userDetails = UserModel.query.filter_by(UserID=UserID).one()
        
        if userDetails:
            return jsonify(
                {
                    "code": 200,
                    "data": userDetails.json()
                }
        )

        # except:
        #     return jsonify(
        #         {
        #             "code": 404,
        #             "message": "User with " + str(UserID) + " is not found"
        #         }
        # ), 404




# PUT User Details by User ID 
@app.route("/user/<string:UserID>", methods=['PUT'])
def update_user_details(UserID):
        try:

            userDetails = UserModel.query.filter_by(UserID=UserID).first()
            user_data = request.get_json()
            
            userDetails.Address = user_data['Address']
            userDetails.Email = user_data['Email']
            userDetails.Firstname = user_data['Firstname']
            userDetails.Lastname = user_data['Lastname']
            userDetails.OptIntoPhyStatements = user_data['OptIntoPhyStatements']
            userDetails.Password = user_data['Password']
            userDetails.UserID = user_data['UserID']
            userDetails.Username = user_data['Username']


            db.session.commit()

            return jsonify({

                'status': '200',
                'msg': f'Success updating the user with the UserID {UserID}!'
            }) 
        except:
            return jsonify(
            {
                "code": 500,
                "data": {
                    "UserID": UserID
                },
                "message": "An error occurred while updating the user. "
            }
        ), 500

                



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

api.add_resource(Login, "/login")



if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("$PORT", default=5000))
