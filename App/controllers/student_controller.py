from fastapi import APIRouter
from App import schemas
from App.services import student_service

router = APIRouter(prefix="/students", tags=["Students"])

def response_success(message: str, data=None):
    return {"status": "success", "message": message, "data": data}

@router.post("/")
def create_student(student: schemas.StudentCreate):
    result = student_service.create_student(student.dict())
    return response_success("Student created successfully", result)

@router.get("/")
def read_students():
    result = student_service.get_all_students()
    return response_success("Students retrieved successfully", result)

@router.get("/{student_id}")
def read_student(student_id: str):
    result = student_service.get_student(student_id)
    return response_success("Student retrieved successfully", result)

@router.put("/{student_id}")
def update_student(student_id: str, student: schemas.StudentCreate):
    result = student_service.update_student(student_id, student.dict())
    return response_success("Student updated successfully", result)

@router.delete("/{student_id}")
def delete_student(student_id: str):
    result = student_service.delete_student(student_id)
    return response_success("Student deleted successfully", result)
