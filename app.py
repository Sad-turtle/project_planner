import os
import psycopg2
from flask import Flask, render_template, request, session, g, url_for, redirect
import bcrypt
import json
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Yernar2001@localhost/project_planning'
#app.config['']
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False )
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"Task(id={self.id}, name={self.name})"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='project_planning',
                            user="postgres",
                            password="1")
    return conn


def load_user_data(filename):
    with open(file=filename) as file:
        data = json.load(file)
        return data


def validate_user(username, password):
    user_data = load_user_data("users.json")
    for user_entry in user_data:
        if user_entry["username"] == username:
            stored_password = user_entry["password"].encode("utf-8")
            entered_password = password.encode("utf-8")
            if bcrypt.checkpw(entered_password, stored_password):
                return True
    return False


def save_in_txt(username, hash, email):
    user_data = {
        "username": username,
        "email": email,
        "password": hash.decode("utf-8")
    }
    existing_data = load_user_data("users.json")
    existing_data.append(user_data)
    with open(file="users.json", mode="w") as file:
        json.dump(existing_data, file)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # handle registration form
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()) # hash password
        # here write datas to txt
        save_in_txt(username, hashed_password, email)
        # also add error handling
        return redirect(url_for("login"))
    else:
        # render register template
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # handle registration form
        username = request.form["username"]
        password = request.form["password"]

        if validate_user(username, password):
            return redirect("/")
        else:
            return render_template("login.html", error_message="Invalid credentials")
        # add sessions
        # session["user_id"] = user.id

    else:
        # render login template
        return render_template("login.html")


@app.route("/projects")
def projects():
    return


@app.route("/projects/<id>/<taskid>")
def task():
    return


#@app.route("/todo1")
#def todolist():
#    to_do = Task.query.all()
#    return render_template("todolist.html", todo_list=to_do)
#
#@app.route("/add/todo", methods=["POST"])
#def add_todo():
#    name = request.form.get("name")
#    new_task = Task(name=name, done=False)
#    db.session.add(new_task)
#    db.session.commit()
#    return redirect("/todo1")
#
#
#@app.route("/update/<int:todo_id>")
#def update(todo_id):
#    todo = Task.query.get(todo_id)
#    todo.done = not todo.done
#    db.session.commit()
#    return redirect("/todo1")
#
#
#@app.route("/delete/<int:todo_id>")
#def delete(todo_id):
#    todo = Task.query.get(todo_id)
#    db.session.delete(todo)
#    db.session.commit()
#    return redirect("/todo1")


if __name__ == "__main__":
    app.run(host="192.168.0.119", port="8080")

