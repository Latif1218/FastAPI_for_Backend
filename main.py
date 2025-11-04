from fastapi import FastAPI, HTTPException, status, Response
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


@app.get("/course/{id}")
def get_course(id:int):
    cursor.execute("""SELECT * FROM course WHERE "id" = %s""",(str(id),))
    course = cursor.fetchone()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Course with Id:{id} was not found"
        )
    return{"course_detail": course}



@app.delete("/course/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(id: int):
    cursor.execute("""DELETE FROM course WHERE id = %s returning * """,(str(id),))
    delete_course = cursor.fetchone()
    conn.commit()
    if delete_course == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"course with id: {id} does not exixt")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


from fastapi import HTTPException

@app.put("/course/{id}")
def update_course(id: int, course: Course):
    cursor.execute(
        """UPDATE course 
           SET name = %s, instructor = %s, duration = %s, website = %s 
           WHERE id = %s RETURNING *""",
        (course.name, course.instructor, course.duration, str(course.website), id)
    )

    updated_course = cursor.fetchone()
    conn.commit()

    if not updated_course:
        raise HTTPException(
            status_code=404,
            detail=f"Course with id: {id} not found"
        )

    return {"data": updated_course}

    
    