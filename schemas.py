from pydantic import BaseModel, EmailStr

class StudentBase(BaseModel):
    name: str
    email: EmailStr
    department: str
    year_of_study: int
    roll_no: str

class StudentCreate(StudentBase):
    password: str  # password is only required on creation

class Student(StudentBase):
    id: int

    model_config = {
        "from_attributes": True  # <-- Pydantic V2 replacement for orm_mode
    }
