from pydantic import BaseModel, EmailStr

class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    department: str
    year_of_study: int
    roll_no: str
    password: str
