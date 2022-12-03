from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import jwt
import datetime
from flask import Flask, jsonify, make_response, session
import os
from app.middleware.auth_middleware import generate_token
from app.models.UserModel import UserModel
from dotenv import load_dotenv

login_args = reqparse.RequestParser()
login_args.add_argument("username", type=str, help="Username is required", required=True,location='values')
login_args.add_argument("password", type=str, help="Password is required", required=True,location='values')




SECRET_KEY = os.getenv('SECRET_KEY')

class Login(Resource):


    def post(self):
        args = login_args.parse_args()
        exists = bool(UserModel.query.filter_by(Username=args['username'],Password=args['password']).first())
        if exists:
            token = generate_token(args['username'])
            return jsonify({'token': token})
        else:
            return jsonify({'message': 'Unable to verify'})