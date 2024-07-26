from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, _id, email, password, name, gender):
        self.id = str(_id)  # Ensure id is a string for Flask-Login
        self.email = email
        self.password = password
        self.name = name
        self.gender = gender

    @staticmethod
    def from_mongo_doc(doc):
        return User(
            _id=doc["_id"],
            email=doc["email"],
            password=doc["password"],
            name=doc["name"],
            gender=doc["gender"]
        )
