from fastapi import FastAPI, Depends, HTTPException, status, Request, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List, Optional
from fastapi.templating import Jinja2Templates


from .dadabase_interactions import get_recipies

router = APIRouter()
templates = Jinja2Templates(directory="templates")



@router.get("/recipies")
def get_recipies(request: Request):
    recipies = get_recipies()
    return 