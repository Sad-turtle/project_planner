import os
import psycopg2
from flask import Flask, render_template, request, session, g, url_for, redirect
import bcrypt
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


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    done = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


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
        if user:
            hashed_password = user.password.encode("utf-8")
            if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
                return redirect(url_for("dashboard", user_id=user.id))
        return render_template("login.html", error_message="Invalid credentials")

    else:
        # render login template
        return render_template("login.html")


@app.route("/dashboard/<user_id>")
def dashboard(user_id):
    user = User.query.get(user_id)
    dashboard = Dashboard.query.filter_by(user_id=user_id).first()
    to_do = Task.query.all()
    if user:
        if not dashboard:
            dashboard = Dashboard(name="My Dashboard", user_id=user_id)
            db.session.add(dashboard)
            db.session.commit()
        return render_template("dashboard.html", user=user, dashboard=dashboard, todo_list=to_do)
    else:
        return "User not found"


#@app.route("/dashboard/<user_id>/todo")
#def todolist():
#    to_do = Task.query.all()
#    return render_template("todolist.html", todo_list=to_do)


@app.route("/dashboard/<user_id>/add", methods=["POST"])
def add_todo(user_id):
    name = request.form.get("name")
    new_task = Task(name=name, done=False, user_id=user_id)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("dashboard", user_id=user_id))


@app.route("/dashboard/<user_id>/update/<int:todo_id>")
def update_todo(user_id, todo_id):
    todo = Task.query.filter_by(id=todo_id).first()
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for("dashboard", user_id=user_id))


@app.route("/dashboard/<user_id>/delete/<int:todo_id>")
def delete_todo(user_id, todo_id):
    todo = Task.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("dashboard", user_id=user_id))


if __name__ == "__main__":
    app.run(host="192.168.0.119", port="8080")

