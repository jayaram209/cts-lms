def format_courses(courses):
    if courses is None:
        response = {"status": "courses not available"}
        return response
    return [
        dict(
            course_name=course.course_name,
            course_duration=course.course_duration,
            course_description=course.course_description,
            technology=course.technology,
            launch_url=course.launch_url,
        )
        for course in courses or []
    ]
