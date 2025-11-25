from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl, EmailStr
from datetime import datetime



# Define request body schema
class CourseCreate(BaseModel):
    name: str
    instructor: str
    duration: float
    website: HttpUrl


class CourseResponse(CourseCreate):
    id : int

    class Config:
        orm_model = True



class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserRes(BaseModel):
    id: int
    email : EmailStr
    created_at : datetime

    class Config:
        orrm_model = True