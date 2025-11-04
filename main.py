from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# Define request body schema
class Course(BaseModel):
    name: str
    instructor: str
    duration: float
    website: HttpUrl

# Database connection
while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='aiquest',
            user='postgres',
            password='4321',
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Successfully connected to database")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error:", error)
        time.sleep(2)


@app.post("/post")
def create_post(post: Course):
    try:
        cursor.execute(
            """INSERT INTO course (name, instructor, duration, website)
            VALUES (%s, %s, %s, %s) RETURNING *""",
            (post.name, post.instructor, post.duration, str(post.website))
        )
        new_post = cursor.fetchone()
        conn.commit()
        return {"data": new_post}
    except Exception as e:
        conn.rollback()
        print("❌ Error inserting data:", e)
        return {"error": str(e)}

@app.get("/course")
def studymart():
    return {"backend": "for self"}

@app.get("/")
def aiquest():
    cursor.execute("""SELECT * FROM course""")
    data = cursor.fetchall()
    return {"data":data}



@app.get("/fastapi/api")
def fastapi():
    return {"backend": "for self"}
