from bson import ObjectId, errors as bson_errors
from fastapi import HTTPException
from database import student_collection

def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "email": student["email"],
        "department": student["department"],
        "year_of_study": student["year_of_study"],
        "roll_no": student["roll_no"]
    }

def create_student(student_data):
    try:
        if student_collection.find_one({"email": student_data["email"]}):
            raise HTTPException(status_code=400, detail="Email already exists")
        student_data.pop("password", None)
        result = student_collection.insert_one(student_data)
        student = student_collection.find_one({"_id": result.inserted_id})
        return student_helper(student)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_all_students():
    try:
        students = student_collection.find()
        return [student_helper(s) for s in students]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_student(student_id: str):
    try:
        student = student_collection.find_one({"_id": ObjectId(student_id)})
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student_helper(student)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid student ID")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def update_student(student_id: str, updated_data):
    try:
        if student_collection.find_one({"email": updated_data["email"], "_id": {"$ne": ObjectId(student_id)}}):
            raise HTTPException(status_code=400, detail="Email already exists")
        updated_data.pop("password", None)
        result = student_collection.update_one({"_id": ObjectId(student_id)}, {"$set": updated_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")
        student = student_collection.find_one({"_id": ObjectId(student_id)})
        return student_helper(student)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid student ID")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def delete_student(student_id: str):
    try:
        result = student_collection.delete_one({"_id": ObjectId(student_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")
        return {"message": "Student deleted successfully"}
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid student ID")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
