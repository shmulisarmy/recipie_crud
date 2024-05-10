from fastapi import FastAPI, Depends, HTTPException, status, Request, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List, Optional


from users.routes import router as users_router
from recipies.routes import router as recipies_router


app = FastAPI()

app.include_router(users_router, prefix="/users")
app.include_router(recipies_router, prefix="/recipies")



#run command: uvicorn main:app --reload