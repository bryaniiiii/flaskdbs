from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
# from flask_serialize import FlaskSerialize


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
    OptIntoPhyStatements = db.Column(db.INTEGER(), nullable=True)

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
    @app.route("/user/<int:UserID>", methods=['GET'])
    def getUserDetails(UserID):

        try:
            userDetails = User.query.filter_by(UserID=UserID).first()
            
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

    # PUT User Details by User ID 
    @app.route("/user/<int:UserID>", methods=['PUT'])
    def update_user_details(UserID):
        try:

            userDetails = User.query.filter_by(UserID=UserID).first()
            user_data = request.get_json()
            
            userDetails.Address = user_data['Address'];
            userDetails.Email = user_data['Email'];
            userDetails.Firstname = user_data['Firstname'];
            userDetails.Lastname = user_data['Lastname'];
            userDetails.OptIntoPhyStatements = user_data['OptIntoPhyStatements'];
            userDetails.Password = user_data['Password'];
            userDetails.UserID = user_data['UserID'];
            userDetails.Username = user_data['Username'];

            # userDetails.update(user_data)

            print(userDetails)
            print(type(userDetails))
            print(user_data)
            # users = [user.serialize() for user in db.view()
            db.session.commit()

            # user_data = {
            #     address,
            #     email,
            #     firstname,
            #     lastname,
            #     optIntoPhyStatements,
            #     password,
            #     userID,
            #     username
            # }

        # for a_user in users:
        #     try:
        #         if a_user['UserID'] == userID:
        #             userDetails = user(
        #                 address,
        #                 email,
        #                 firstname,
        #                 lastname,
        #                 optIntoPhyStatements,
        #                 password,
        #                 userID,
        #                 username
        #             )
        #             db.update(user)

            return jsonify({
                # 'res': user_data.serialize(),
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

                

        # try:
        #     userlist = User.query.filter_by(UserID=UserID).one()
        #     if not userlist:
        #         return jsonify(
        #             {
        #                 "code": 404,
        #                 "data": {
        #                     "UserID": UserID
        #                 },
        #                 "message": "UserID has not been updated"
        #             }
        #         ), 404

        #     # update status
        #     data = request.get_json()
        #     if data['status']:
        #         userlist.status = data['status']
        #         db.session.commit()
        #         return jsonify(
        #             {
        #                 "code": 200,
        #                 "data": userlist.json(),
        #                 "message": "User with User ID " + str(UserID) + " has been updated"
        #             }
        #         ), 200
        # except Exception as e:
        #     return jsonify(
        #         {
        #             "code": 500,
        #             "data": {
        #                 "UserID": UserID
        #             },
        #             "message": "An error occurred while updating the user. " + str(e)
        #         }
        #     ), 500


if __name__ == '__main__':
    app.run(port=5003, debug=True)
