# main.py
from fastapi import FastAPI, HTTPException
from bson import ObjectId
import schemas
from database import student_collection

app = FastAPI(title="Student CRUD API (MongoDB)")

def response_success(message: str, data=None):
    return {
        "status": "success",
        "message": message,
        "data": data
    }

def student_helper(student) -> dict:
    """Convert Mongo document to dict for response"""
    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "email": student["email"],
        "department": student["department"],
        "year_of_study": student["year_of_study"],
        "roll_no": student["roll_no"]
    }

@app.post("/students/")
def create_student(student: schemas.StudentCreate):
    if student_collection.find_one({"email": student.email}):
        return {"status": "error", "message": "A student with this email already exists", "data": None}
    
    student_dict = student.dict()
    student_dict.pop("password")  # Optional: store password hashed if needed
    result = student_collection.insert_one(student_dict)
    new_student = student_collection.find_one({"_id": result.inserted_id})
    return response_success("Student created successfully", student_helper(new_student))


@app.get("/students/")
def read_students():
    students = student_collection.find()
    return response_success(
        "Students retrieved successfully",
        [student_helper(s) for s in students]
    )


@app.get("/students/{student_id}")
def read_student(student_id: str):
    student = student_collection.find_one({"_id": ObjectId(student_id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return response_success("Student retrieved successfully", student_helper(student))


@app.put("/students/{student_id}")
def update_student(student_id: str, updated_student: schemas.StudentCreate):
    if student_collection.find_one({"email": updated_student.email, "_id": {"$ne": ObjectId(student_id)}}):
        return {"status": "error", "message": "A student with this email already exists", "data": None}
    
    updated_data = updated_student.dict()
    updated_data.pop("password")  # optional
    
    result = student_collection.update_one({"_id": ObjectId(student_id)}, {"$set": updated_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student = student_collection.find_one({"_id": ObjectId(student_id)})
    return response_success("Student updated successfully", student_helper(student))


@app.delete("/students/{student_id}")
def delete_student(student_id: str):
    result = student_collection.delete_one({"_id": ObjectId(student_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return response_success("Student deleted successfully")
