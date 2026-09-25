from fastapi import FastAPI

from database.db import Base, engine
from models.employee import Employee

from routers.employees import router as employee_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Employee Management API",
    version="1.0.0"
)


app.include_router(employee_router)


@app.get("/")
def root():
    return {
        "message": "Employee Management API is running"
    }