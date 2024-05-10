from fastapi import FastAPI, Depends, HTTPException, status, Request, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import FileResponse


router = APIRouter()



@router.get("/image/{id}")
def images(request: Request, id: int):
    folder_path = "users/static/images/"
    full_path = f"{folder_path}download-{id}.jpg"
    return FileResponse(full_path)
    
    