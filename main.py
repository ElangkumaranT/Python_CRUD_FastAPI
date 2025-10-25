from fastapi import FastAPI
from controllers import student_controller

app = FastAPI(title="Student CRUD API (MongoDB)")
app.include_router(student_controller.router)
