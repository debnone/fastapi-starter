from fastapi import FastAPI
from sqlalchemy.orm import Session
from fastapi.params import Depends
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from . import utils
from .database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware

# 🔽  Here we old  meyhods to create the database
# 🔽 now no need because we use alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

