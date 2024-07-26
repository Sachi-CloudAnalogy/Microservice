import bcrypt
from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_user, LoginManager
from mongodb import models, MongoDBLibrary
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize MongoDB
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
    todos = db_lib.get_all_todos()
    return render_template("home.html", todos=todos)

@app.route("/todo", methods=['GET', 'POST'])
def todo():
    if request.method == "POST":
        task = request.form.get("task")
        status = request.form.get("status")
        date = datetime.strptime(request.form.get("date"), "%Y-%m-%d")
        if task and status and date:
            db_lib.insert_todo(task, status, date)
            return redirect(url_for('home'))
        else:
            return "All fields are required !!"
    else:
        return render_template("todo.html")

@app.route("/todo/<todo_id>/update", methods=['GET', 'POST'])
def update_todo(todo_id):
    if request.method == "POST":
        task = request.form.get("task")
        status = request.form.get("status")
        date = datetime.strptime(request.form.get("date"), "%Y-%m-%d")
        if task and status and date:
            update_data = {"task": task, "status": status, "date": date}
            db_lib.update_todo_by_id(todo_id, update_data)
            return redirect(url_for('home'))
        else:
            return "All fields are required !!"
    else:
        todo = db_lib.get_todo_by_id(todo_id)
        return render_template("update_todo.html", todo=todo)

@app.route("/todo/<todo_id>/delete", methods=['POST'])
def delete_todo(todo_id):
    db_lib.delete_todo_by_id(todo_id)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
