from pydantic import AnyUrl, BaseModel, EmailStr


class TokenGenerationValidation(BaseModel):
    email: EmailStr
    password: str


class UserCreateValidation(BaseModel):
    email: EmailStr
    username: str
    password: str


class CoursesValidation(BaseModel):
    course_name: str
    course_duration: int
    course_description: str
    technology: str
    launch_url: AnyUrl
