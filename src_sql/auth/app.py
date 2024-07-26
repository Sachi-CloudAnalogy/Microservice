import bcrypt
from flask import Flask, render_template, request
from flask_login import LoginManager, login_user
from my_database_lib import db, models


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sfdc@localhost:5432/Microservice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if email and password:
            existing_user = models.User.query.filter_by(username=email).first()
            if existing_user:
                if bcrypt.checkpw(password.encode('utf-8'), existing_user.password.encode('utf-8')):
                    # login_user(existing_user)
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
            existing = models.User.query.filter_by(username=email).first()
            if existing:
                return "Username already exist !!"
            else:
                new_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')       
                new_user = models.User(username=email, password=new_pass, name=name, gender=gender)
                db.session.add(new_user)
                db.session.commit()
                return "Sucessfully Registered !!"
        else:
            return "All the fields are required !!"      
    else:    
        return render_template("register.html")     

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)
    