import os
from flask import Flask, jsonify, make_response, session
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
from functools import wraps
import mysql.connector
from login.login import UserModel
from login.login import Login
from sharemodels import db





app = Flask(__name__)

api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:lgy1DWXo2pvvFQeEix6x@containers-us-west-83.railway.app:7790/railway"
db.init_app(app)


@app.route('/')
def index():
    result = UserModel.query.filter_by(UserID=1).first()
    return {"message": result.UserID}

api.add_resource(Login, "/login")


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
