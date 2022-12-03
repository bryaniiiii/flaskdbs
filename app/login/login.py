from app.auth_middleware.auth_middleware import generate_token
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import jwt
import datetime
from flask import Flask, jsonify, make_response, session
import os
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
    def json(self):
        return {
            "UserID":self.UserID,
            "Username":self.Username,
            "Password":self.Password,
            "Firstname":self.Firstname,
            "Lastname":self.Lastname,
            "Email":self.Email,
            "Address":self.Address,
            "OptIntoPhyStatements":self.OptIntoPhyStatements
        }
class Login(Resource):


    def post(self):
        args = login_args.parse_args()
        exists = bool(UserModel.query.filter_by(Username=args['username'],Password=args['password']).first())
        if exists:
            user = UserModel.query.filter_by(Username=args['username'],Password=args['password']).first()
            token = generate_token(args['username'])
            return jsonify({'token': token,'UserID': user.UserID})
        else:
            return jsonify({'message': 'Unable to verify'})