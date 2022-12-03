from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import jwt
import datetime
from flask import Flask, jsonify, make_response, session
import os
from dotenv import load_dotenv
from sharemodels import db







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



