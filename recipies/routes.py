from fastapi import FastAPI, Depends, HTTPException, status, Request, APIRouter, Query, Form
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List, Optional
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from typing import Dict
import json

from globals import Globals
import recipies.database_interactions as recipies_db

router = APIRouter()
templates = Jinja2Templates(directory="recipies/templates")


class Recipe(BaseModel):
    name: str
    ingredients: dict[str, str]
    instructions: str
    total_time_to_make: int


@router.get("/")
def get_recipies(request: Request):
    recipies = recipies_db.get_100_most_recent_recipies(user_id=1)
    links = Globals.get_routes(Globals)
    print(f"links: {links}")
    return templates.TemplateResponse("recipies.html", {"request": request, "recipies": recipies, "links": links})


@router.get("/time_to_make/{min_time}/{max_time}")
def get_recipies(request: Request, min_time: int, max_time: int):
    user_id = 1
    links = Globals.get_routes(Globals)
    recipies = recipies_db.get_recipies_by_time_to_make(user_id, min_time, max_time)
    return templates.TemplateResponse("recipies.html", {"request": request, "recipies": recipies, "links": links})




@router.post("/create")
def create_recipie(request: Request, name: str = Form(...), ingrediants_str: str = Form(...), instructions: str = Form(...), total_time_to_make: int = Form(...), cost_to_make: int = Form(...)):
    print(f"ingrediants_str: {ingrediants_str}")
    # try:
    ingrediants = json.loads(ingrediants_str)
    # except json.decoder.JSONDecodeError:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ingrediants must be json string")
    recipies_db.create_recipie(name, ingrediants, instructions, total_time_to_make, cost_to_make)
    return {"message": "recipie created"}



@router.get("/create")
def create_recipie(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


@router.get("/image/{id}")
def create_recipie(request: Request, id: int):
    file_name = f"download-{id}.jpg"
    full_path = f"recipies/static/images/{file_name}"
    return FileResponse(full_path)


@router.get("/like/{recipie_id}/{user_id}")
def like_recipie(request: Request, recipie_id: int, user_id: int):
    recipies_db.like_recipie(user_id, recipie_id)
    return templates.TemplateResponse("htmx/liked.html", {"request": request, "user_id": user_id, "recipie_id": recipie_id})

@router.get("/unLike/{recipie_id}/{user_id}")
def like_recipie(request: Request, recipie_id: int, user_id: int):
    recipies_db.unlike_recipie(user_id, recipie_id)
    return templates.TemplateResponse("htmx/unLiked.html", {"request": request, "user_id": user_id, "recipie_id": recipie_id})
 




@router.get("/liked/{user_id}")
def get_liked_recipies(request: Request, user_id: int):
    recipies = recipies_db.get_liked_recipies(user_id)
    return templates.TemplateResponse("recipies.html", {"request": request, "recipies": recipies})
