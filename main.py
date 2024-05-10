from fastapi import FastAPI, Depends, HTTPException, status, Request, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse

from globals import Globals

def redirect(url: str):
    return RedirectResponse(url=url)


from colors import blue, green, red, yellow


colors_in_list = [blue, green, red, yellow]


from users.routes import router as users_router
from recipies.routes import router as recipies_router
from reviews.routes import router as reviews_router



app = FastAPI()

app.include_router(users_router, prefix="/users")
app.include_router(recipies_router, prefix="/recipies")
app.include_router(reviews_router, prefix="/reviews")



@app.get("/")
def root():
    return RedirectResponse("/recipies")


@app.get("/like_button")
def like_button():
    return FileResponse("images/like.png")

@app.get("/unLike_button")
def liked_button():
    return FileResponse("images/unLiked.png")



site = "http://127.0.0.1:8000"

Globals.G_routes = [route.path for route in app.routes]

for index, link in enumerate(Globals.G_routes):
    color = colors_in_list[index%len(colors_in_list)]
    print(color(f"{site}{link }"))


#run command: uvicorn main:app --reload