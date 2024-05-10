from fastapi import FastAPI, Depends, HTTPException, status, Request, APIRouter, Form
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List, Optional
from utils.database import connect_to_db
from fastapi.templating import Jinja2Templates


from globals import Globals

router = APIRouter()
templates = Jinja2Templates(directory="reviews/templates")




@router.get("/")
def read_reviews(request: Request):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT content, users.username FROM reviews inner join users on reviews.posted_by = users.id;")
    reviews = cursor.fetchall()
    connection.close()
    return templates.TemplateResponse("reviews.html", {"request": request, "reviews": reviews})




@router.post("/create")
def create_review(request: Request, content: str = Form(...), posted_by: int = Form(...)):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO reviews (content, posted_by) VALUES (%s, %s);", (content, posted_by))
    connection.commit()
    connection.close()
    return {"message": "review created"}

