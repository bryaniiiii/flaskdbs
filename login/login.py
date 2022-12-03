from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()




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