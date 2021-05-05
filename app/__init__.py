from flask import Flask, request, session, render_template
from .routes import routes
from .controllers import controller
from .db import db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os
from .models import User

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.secret_key = "123456"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(BASE_DIR, "my.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.register_blueprint(routes)
app.register_blueprint(controller)
db.init_app(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)


@app.errorhandler(404)
def page_not_found_404(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found_500(e):
    return render_template("500.html"), 500


app.register_error_handler(404, page_not_found_404)
app.register_error_handler(500, page_not_found_500)

@app.before_request
def before():
    user = request.cookies.get("user")
    if user:
        result = User.query.filter(User.username == user).first()
        session["id"] = result.id
        session["user"] = result.username
        session["email"] = result.email
