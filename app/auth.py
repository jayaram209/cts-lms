from flask import Blueprint, request
from flask_jwt_extended import create_access_token, verify_jwt_in_request

from app.models import UserModel, db
from app.validations import TokenGenerationValidation, UserCreateValidation

auth_blueprint = Blueprint("auth_blueprint", __name__)


@auth_blueprint.route("/api/v1.0/lms/token", methods=["GET", "POST"])
def login():
    data = TokenGenerationValidation(**request.get_json(silent=True) or {})

    try:
        user_obj = (
            UserModel.query.filter(UserModel.email == data.email)
            .order_by(UserModel.id.desc())
            .first()
        )
        assert user_obj and user_obj.check_password(
            data.password
        ), "Invalid UserName/Password"

        # if the user is valid we will give them a JWT token.
        access_token = create_access_token(identity=data.email)
        response = {"access_token": access_token}
        return response

    except Exception as err:
        return {"error": err.__str__()}, 400


@auth_blueprint.route("/api/v1.0/lms/company/register", methods=["POST"])
def create_user():
    try:
        data = UserCreateValidation(**request.get_json(silent=True) or {})
        if UserModel.query.filter_by(email=data.email).first():
            return {"error": "EMail Already Used"}, 400
        user = UserModel(email=data.email, username=data.username)
        user.set_password(data.password)
        db.session.add(user)
        db.session.commit()
        return {"user": "OK"}

    except Exception as err:
        return {"error": err.__str__()}, 400


@auth_blueprint.route("/api/v1.0/lms/validatetoken", methods=["POST"])
def validate_token():
    verify_jwt_in_request()
    return {"token": "Valid"}
