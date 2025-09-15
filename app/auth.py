from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app.models import User, db

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template("login.html", error="Todos los campos son obligatorios.")

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("profile"))
        else:
            return render_template("login.html", error="Credenciales inválidas")

    return render_template("login.html")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        avatar_url = request.form.get("avatar_url") or "/static/avatar.png"

        if not username or not password:
            return render_template("signup.html", error="Todos los campos son obligatorios.")

        if User.query.filter_by(username=username).first():
            return render_template("signup.html", error="Ese nombre de usuario ya existe.")

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, avatar_url=avatar_url)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))

    return render_template("signup.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
