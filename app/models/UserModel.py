from sharemodels import db

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