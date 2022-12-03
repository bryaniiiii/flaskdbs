from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import jwt
import datetime
from flask import Flask, jsonify, make_response, session
import os
from dotenv import load_dotenv
from sharemodels import db




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



