from datetime import timedelta

from flask import Flask, jsonify, render_template
from flask_jwt_extended import JWTManager, jwt_required
from pydantic import ValidationError

from app.auth import auth_blueprint
from app.courses import course_blueprint
from app.models import db

api = Flask(__name__)
api.register_blueprint(auth_blueprint)
api.register_blueprint(course_blueprint)


api.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testdb.db"
api.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api.config["JSON_SORT_KEYS"] = False
api.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

api.app_context().push()
db.init_app(api)
db.create_all()

api.config["JWT_SECRET_KEY"] = "please-remember-to-change-me"
api.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
jwt = JWTManager(api)


@api.errorhandler(ValidationError)
def handle_pydantic_validation_errors(e):
    """
    Format all the errors coming from the pydantic validation
    and return to the format which is easy to understand
    and ignore the unneeded fields.
    :return: json
    """
    return jsonify({err["loc"][0]: err["msg"] for err in e.errors()})


@api.route("/")
def home():
    return render_template('home.html')


if __name__ == "__main__":
    api.run(host="0.0.0.0", port=5000, debug=True)
