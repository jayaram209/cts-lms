Steps to run the project locally
- install python in the system
- create a Directory LMSFlask
    - LMSFlask
- create virtual environment inside Directory (cmd: python -m venv env_flask) which will create a environment as below
    - LMSFlask
        - env_flask (environment is created)
- move the project files to Directory LMSFlask
    - LMSFlask
        - env_flask (environment is created)
        - app.py
        - models.py
        - requirements.txt
        - testdb.db
- activate virtual environment (Linux - source env_flask/bin/activate, Windows - .\venv\Scripts\activate)
- install requirements (pip install -r requirements.txt)
- run the command python app.py to run the flask app

REST ENDPOINTS:
    - /api/v1.0/lms/company/register
    - /api/v1.0/lms/courses/info/<technology>
    - /api/v1.0/lms/courses/getall
    - /api/v1.0/lms/courses/delete/<coursename>
    - /api/v1.0/lms/courses/add/<coursename>
    - /api/v/1.0/lms/courses/get/<technology>/<durationFromRange>/<durationToRange>

sample data:
[
    {
        "course_name": "Backend-Python-WEB Development-2022-FSE",
        "course_duration": 480,
        "course_description": "Backend-Python-WEB Development-2022-FSE:Level-3 Coding and MCQs-Advanced programming in python and Datas structres",
        "technology": "Python",
        "launch_url": "https://flask.palletsprojects.com/en/2.2.x/"
    },
    {
        "course_name": "Platform-Cloud-AWS-2022-FSE",
        "course_duration": 720,
        "course_description": " Platform-Cloud-AWS-2022-FSE:Level-3 Coding and MCQs-Advanced programming in python and Datas structres",
        "technology": "Cloud",
        "launch_url": "https://docs.aws.amazon.com/"
    }
]
  EX:
    - /api/v1.0/lms/company/register
    - /api/v1.0/lms/courses/info/Platform
    - /api/v1.0/lms/courses/getall
    - /api/v1.0/lms/courses/delete/Platform-Cloud-Azure-2022-FSE
    - /api/v1.0/lms/courses/add/
    - /api/v/1.0/lms/courses/get/<Platform>/<500>/<1000>

