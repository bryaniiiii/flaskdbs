from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import jwt
import datetime
from flask import Flask, jsonify, make_response, session
import os
from dotenv import load_dotenv
from sharemodels import db

login_args = reqparse.RequestParser()
login_args.add_argument("username", type=str, help="Username is required", required=True,location='values')
login_args.add_argument("password", type=str, help="Password is required", required=True,location='values')




SECRET_KEY = os.getenv('SECRET_KEY')


class UserModel(db.Model):
    __tablename__ = "User"
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(20))
    Password = db.Column(db.String(20))
    Firstname = db.Column(db.String(255))
    Lastname = db.Column(db.String(255))
    Email = db.Column(db.String(255))
    Address = db.Column(db.String(255))
    OptIntoPhyStatements = db.Column(db.Boolean)

class Login(Resource):


    def post(self):
        args = login_args.parse_args()
        user = UserModel.query.filter_by(Username=args['username'],Password=args['password']).first()
        if user:
            token = jwt.encode({
                'user': args['username'],
                'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=30)

            }, SECRET_KEY,algorithm="HS256"
            )
            return jsonify({'token': token, 'userId': user.UserID})
        else:
            return jsonify({'message': 'Unable to verify'})