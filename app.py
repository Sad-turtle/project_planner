import os
import psycopg2
from flask import Flask, render_template, request, session, g, url_for, redirect
import bcrypt
import json
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1@localhost:5433/project_planning'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Dashboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    dashboard_id = db.Column(db.Integer, db.ForeignKey('dashboard.id'), nullable=False)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    done = db.Column(db.Boolean, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        user = User(username=username, email=email, password=hashed_password.decode("utf-8"))

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))
    else:
        # render register template
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        print(user)
        if user:
            hashed_password = user.password.encode("utf-8")
            print(hashed_password)
            print(password.encode("utf-8"))
            print(bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()))
            print(bcrypt.checkpw(password.encode("utf-8"), hashed_password))
            if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
                return redirect("/")
        return render_template("login.html", error_message="Invalid credentials")

    else:
        # render login template
        return render_template("login.html")


#@app.route("/dashboard_<dash_id>/project_<proj_id>/")
#def projects(id):
#    return id
#
#
#@app.route("/projects/<id>/<taskid>")
#def task():
#    return


@app.route("/todo")
def todolist():
    to_do = Task.query.all()
    return render_template("todolist.html", todo_list=to_do)

@app.route("/add/todo", methods=["POST"])
def add_todo():
    name = request.form.get("name")
    new_task = Task(name=name, done=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect("/todo1")


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Task.query.get(todo_id)
    todo.done = not todo.done
    db.session.commit()
    return redirect("/todo1")


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Task.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect("/todo1")


if __name__ == "__main__":
    app.run(host="192.168.0.119", port="8080")

