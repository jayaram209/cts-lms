from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.models import CourseModel, db
from app.utils import format_courses
from app.validations import CoursesValidation

course_blueprint = Blueprint("course_blueprint", __name__)


@course_blueprint.route("/api/v1.0/lms/courses/add/", methods=["POST"])
@jwt_required()
def create():
    try:

        filed_courses = []
        added_courses = []
        data = request.get_json(silent=True) or {}
        if isinstance(data, dict):
            json_request = [CoursesValidation(**data)]
        else:
            json_request = [CoursesValidation(**da) for da in data]
        for content in json_request:
            course = CourseModel(**content.dict())
            db.session.add(course)
            db.session.commit()
            added_courses.append(content.dict())

        response = jsonify(
            {
                "courses failed to add": filed_courses,
                "courses added successfully": added_courses,
            }
        )
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.status_code = 200
        return response

    except Exception as err:
        return {"error": err.__str__()}, 400


@course_blueprint.route(
    "/api/v1.0/lms/courses/delete/<course_name>/", methods=["DELETE"]
)
@jwt_required()
def delete(course_name):
    try:
        course = CourseModel.query.filter_by(course_name=course_name).first()
        assert course, "Valid Course is required to delete"
        db.session.delete(course)
        db.session.commit()
        return {"status": "Course Deleted Successfully"}
    except Exception as err:
        return {"error": err.__str__()}, 400


@course_blueprint.route("/api/v1.0/lms/courses/getall", methods=["GET"])
@jwt_required()
def get_all_courses():
    try:
        courses = CourseModel.query.all()
        json_data = format_courses(courses)
        assert json_data, "No Courses Available for the technology specified"
        response = jsonify(json_data)
        response.status_code = 200
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    except Exception as err:
        return {"error": err.__str__()}, 400


@course_blueprint.route("/api/v1.0/lms/courses/info/<technology>/", methods=["GET"])
@jwt_required()
def get_course_details(technology):
    try:
        courses = CourseModel.query.filter_by(technology=technology)
        json_data = format_courses(courses)
        assert json_data, "No Courses Available for the technology specified"
        return json_data
    except Exception as err:
        return {"error": err.__str__()}, 400


@course_blueprint.route(
    "/api/v1.0/lms/courses/get/<technology>/<durationFromRange>/<durationToRange>",
    methods=["GET"],
)
@jwt_required()
def get_courses_by_duration(technology, durationFromRange, durationToRange):  # noqa
    try:
        courses = CourseModel.query.filter(CourseModel.technology == technology).filter(
                CourseModel.course_duration.between(int(durationFromRange), int(durationToRange)))
        json_data = format_courses(courses)

        assert json_data, "No Courses Available for the technology and duration specified"
        response = jsonify(json_data)
        response.status_code = 200
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    except Exception as err:
        return {"error": err.__str__()}, 400
