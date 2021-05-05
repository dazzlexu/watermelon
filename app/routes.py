
from flask import render_template, flash, redirect, url_for, Blueprint, session
from app.forms import LoginForm
from .models import User, Evaluation
import json

routes = Blueprint("routes", __name__)

@routes.route('/')
@routes.route('/index')
def index():
    if session.get("user"):
        s = 1
    else:
        s = 0
    return render_template('index.html', s=s)


@routes.route('/data')
def data():
    if session.get("user"):
        s = 1
    else:
        s = 0
    return render_template('globalData.html', s=s)


@routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@routes.route('/evaluation')
def evaluation():
    user = session.get("user")
    if user:
        s = 1
    else:
        s = 0
    if user is None:
        form = LoginForm()
        return render_template('login.html', form=form)
    else:
        return render_template('evaluation.html', s=s)


@routes.route('/prevention')
def prevention():
    if session.get("user"):
        s = 1
    else:
        s = 0
    return render_template('prevention.html', s=s)


@routes.route('/symptoms')
def symptoms():
    if session.get("user"):
        s = 1
    else:
        s = 0
    return render_template('symptoms.html', s=s)

@routes.route("/pf")
def pf():
    sec = session.get("sec")
    return render_template('pf.html', sec=sec)

@routes.route("/admin")
def admin():
    result = Evaluation.query.all()
    arr = []
    for res in result:
        res.body = json.loads(res.body)
        arr.append(res)
    return render_template("admin.html", result=arr)


@routes.route("/logout")
def logout():
    session["user"] = None
    session["email"] = None
    session["id"] = None
    resp = redirect("/")
    resp.set_cookie("user", "", max_age=0)
    return resp



