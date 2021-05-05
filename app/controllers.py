from flask import Blueprint, request, redirect, flash, session, make_response
from .forms import LoginForm
from .db import db
from .models import User, Evaluation
import hashlib, json

controller = Blueprint("controllers", __name__, url_prefix="/controller")


@controller.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        resp = redirect("/")
        loginForm = LoginForm()
        if loginForm.validate_on_submit():
            if loginForm.username.data == "admin" and loginForm.password.data == "admin":
                return redirect("/admin")
            else:
                password = hashlib.md5(bytes(loginForm.password.data, encoding="utf-8")).hexdigest()
                result = User.query.filter(User.username == loginForm.username.data,
                                           User.password_hash == password).first()
                if result is None:
                    flash("Incorrect account password")
                    return redirect("/login")
                else:
                    if loginForm.remember_me.data:
                        resp.set_cookie("user", result.username, max_age=3600)
                        session['user'] = result.username
                        session['email'] = result.email
                        session['id'] = result.id
                        return resp
                    else:
                        session['user'] = result.username
                        session['email'] = result.email
                        session['id'] = result.id
                        return redirect("/")
    elif request.method == "GET":
        return "login"


@controller.route("/register", methods=['POST'])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        username = request.form.get("username")

        if password1 == password2:
            result = User.query.filter(User.username == username).first()
            if result is None:
                gmail = User.query.filter(User.email == email).first()
                if gmail is None:
                    password = hashlib.md5(bytes(password1, encoding="utf-8")).hexdigest()
                    user = User(username=username, email=email, password_hash=password)
                    db.session.add(user)
                    db.session.commit()
                    flash("login was successful")
                    return redirect("/")
                else:
                    flash("email already exists")
                    return redirect("/login")
            else:
                flash("Account number already exists")
                return redirect("/login")
        else:
            flash("Two different passwords")
            return redirect("/login")


@controller.route("/eval", methods=["POST"])
def eval():
    q1 = request.form.get("q1")
    q2 = request.form.get("q2")
    q3 = request.form.getlist("q3")
    q4 = request.form.getlist("q4")
    q5 = request.form.getlist("q5")
    desc = request.form.get("desc")
    d = {
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "q4": q4,
        "q5": q5,
        "desc": desc
    }
    sec = 0
    if q1 == "Very concerned":
        sec = sec + 20
    if q2 == "make much account of":
        sec = sec + 20
    if len(q3) == 2:
        if "Newspapers" in q3 and "Microblog" in q3:
            sec = sec + 20

    if len(q4) == 2:
        if "Respiratory droplet transmission" in q4 and "Contact communication" in q4:
            sec = sec + 20

    if len(q5) == 2:
        if "Chlorine containing disinfectant" in q5 and "Cryopreservation" in q5:
            sec = sec + 20

    session["sec"] = sec
    result = Evaluation(marks=sec, body=json.dumps(d), user_id=session.get("id"))
    db.session.add(result)
    db.session.commit()
    return redirect("/pf")
