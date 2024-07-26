import bcrypt
from flask import Flask, render_template, request
from flask_login import login_user, LoginManager
from pymongo.errors import DuplicateKeyError
from mongodb import models, MongoDBLibrary


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize MongoDB
# XHyZVbDB8nRF9IYl
mongo_uri = "mongodb+srv://root:XHyZVbDB8nRF9IYl@cluster.4qlbuab.mongodb.net/"
db_name = "Microservice"
db_lib = MongoDBLibrary(mongo_uri, db_name)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    user = db_lib.find_one("users", {"_id": user_id})
    if user:
        return models.User(**user)
    return None

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if email and password:
            existing_user = db_lib.find_one("users", {"email": email})
            if existing_user:
                if bcrypt.checkpw(password.encode('utf-8'), existing_user["password"].encode('utf-8')):
                    user = models.User.from_mongo_doc(existing_user)
                    login_user(user)
                    return "Successfully logged in !!"
                else:
                    return "Wrong password !!"
            else:
                return "Not a registered user, need to register first!!"
        else:
            return "Both fields are required !!"
    else:
        return render_template("login.html")

    
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")
        gender = request.form.get("gender")
        if email and password and name and gender:
            existing = db_lib.find_one("users", {"email": email})
            if existing:
                return "Username already exists !!"
            else:
                new_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                new_user = {
                    "email": email,
                    "password": new_pass,
                    "name": name,
                    "gender": gender
                }
                try:
                    db_lib.insert_one("users", new_user)
                    return "Successfully Registered !!"
                except DuplicateKeyError:
                    return "Username already exists !!"
        else:
            return "All fields are required !!"
    else:
        return render_template("register.html")
  

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)