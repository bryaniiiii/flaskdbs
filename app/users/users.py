from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
# limiter = Limiter(
#     app,
#     key_func=get_remote_address,
#     default_limits=["2000 per day", "500 per hour"]
# )
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/ESD5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/bank'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

class User(db.Model):
    __tablename__ = 'User'
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.VARCHAR(20), nullable=True)
    Password = db.Column(db.VARCHAR(20), nullable=True)
    Firstname = db.Column(db.VARCHAR(255), nullable=True)
    Lastname = db.Column(db.VARCHAR(255), nullable=True)
    Email = db.Column(db.VARCHAR(255), nullable=True)
    Address = db.Column(db.VARCHAR(255), nullable=True)
    OptIntoPhyStatements = db.Column(db.BOOLEAN(), nullable=True)

    def __init__(self, UserID, Username, Password, Firstname, Lastname, Email, Address, OptIntoPhyStatements):
        self.UserID = UserID
        self.Username = Username
        self.Password = Password
        self.Firstname = Firstname
        self.Lastname = Lastname
        self.Email = Email
        self.Address = Address
        self.OptIntoPhyStatements = OptIntoPhyStatements

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

    # GET User Details by User ID 
    @app.route("/user/<string:UserID>", methods=['GET'])
    def getUserDetails(UserID):

        try:
            userDetails = User.query.filter_by(UserID=UserID)
            
            if userDetails:
                return jsonify(
                    {
                        "code": 200,
                        "data": userDetails.json()
                    }
            )

        except:
            return jsonify(
                {
                    "code": 404,
                    "message": "User with " + str(UserID) + " is not found"
                }
        ), 404

    # POST User Details by User ID 


if __name__ == '__main__':
    app.run(port=5002, debug=True)
