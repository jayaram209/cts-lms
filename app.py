import json
from flask import Flask, request, jsonify
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager

import json
from models import UserModel, db, login, CourseModel

api = Flask(__name__)

api.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb.db'
api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api.config['JSON_SORT_KEYS'] = False
api.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

api.app_context().push()
db.init_app(api)
db.create_all()

api.config["JWT_SECRET_KEY"] = "please-remember-to-change-me"
api.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(api)

@api.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response

@api.route('/token', methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if email != "test" or password != "test":
        return {"msg": "Wrong email or password"}, 401

    access_token = create_access_token(identity=email)
    response = {"access_token":access_token}
    return response

@api.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

@api.route('/profile')
@jwt_required()
def my_profile():
    response_body = {
        "name": "Nagato",
        "about": "Hello! I'm a full stack developer that loves python and javascript"
    }
    return response_body


@api.route('/api/v1.0/lms/courses/add/', methods=['POST'])
@jwt_required()
def create():
    try:
        json_request = request.json
    except Exception as e:
        json_request = json.loads(request.data.decode('utf-8'))
    filed_courses = []
    added_courses = []
    if type(json_request) != list:
        json_request = [json_request]
    if type(json_request) == list:
        for content in json_request:
            course_name = content.get('course_name')
            course_duration = content.get('course_duration')
            course_description = content.get('course_description')
            technology = content.get('technology')
            launch_url = content.get('launch_url')
            if (len(course_name) >= 20) and (len(course_description) >= 100) and (type(course_duration) == int) and \
                    (technology is not None) and (launch_url is not None):
                course = CourseModel(course_name, course_duration, course_description, technology, launch_url)
                db.session.add(course)
                db.session.commit()
                added_courses.append(course_name)
            else:
                filed_courses.append(course_name)
        response = jsonify({'courses failed to add': filed_courses, 'courses added successfully': added_courses})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.status_code = 200
        return response


@api.route('/api/v1.0/lms/courses/delete/<course_name>', methods=['DELETE'])
@jwt_required()
def delete(course_name):
    course = CourseModel.query.filter_by(course_name=course_name).first()
    if request.method == 'DELETE':
        if course:
            db.session.delete(course)
            db.session.commit()
            response = jsonify('Course Deleted Successfully')
            response.status_code = 200
            return response


@api.route('/api/v1.0/lms/courses/getall', methods=['GET'])
@jwt_required()
def getAllCourses():
    courses = CourseModel.query.all()
    json_data = []
    for course in courses:
        d = dict()
        d['course_name'] = course.course_name
        d['course_duration'] = course.course_duration
        d['course_description'] = course.course_description
        d['technology'] = course.technology
        d['launch_url'] = course.launch_url
        json_data.append(d)
    if not json_data:
        return jsonify({'Status_message': 'No Courses Available for the technology specified'})
    else:
        response = jsonify(json_data)
        response.status_code = 200
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


@api.route('/api/v1.0/lms/courses/info/<technology>/', methods=['GET'])
@jwt_required()
def getCourseDetails(technology):
    courses = CourseModel.query.filter_by(technology=technology)
    json_data = []
    for course in courses:
        d = dict()
        d['course_name'] = course.course_name
        d['course_duration'] = course.course_duration
        d['course_description'] = course.course_description
        d['technology'] = course.technology
        d['launch_url'] = course.launch_url
        json_data.append(d)
    if not json_data:
        response = jsonify({'Status_message': 'No Courses Available for the technology specified'})
        response.status_code = 200
        return response
    else:
        response = jsonify(json_data)
        response.status_code = 200
        return response


@api.route('/api/v1.0/lms/courses/get/<technology>/<durationFromRange>/<durationToRange>', methods=['GET'])
@jwt_required()
def getCoursesByDuration(technology, durationFromRange, durationToRange):
    courses = CourseModel.query.filter(CourseModel.technology == technology).filter(
        CourseModel.course_duration.between(durationFromRange, durationToRange))
    json_data = []
    if courses:
        for course in courses:
            d = dict()
            d['course_name'] = course.course_name
            d['course_duration'] = course.course_duration
            d['course_description'] = course.course_description
            d['technology'] = course.technology
            d['launch_url'] = course.launch_url
            json_data.append(d)
    if not json_data:
        return jsonify({'Status_message': 'No Courses Available for the technology and duration specified'})
    else:
        response = jsonify(json_data)
        response.status_code = 200
        return response

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=5000, debug=False)