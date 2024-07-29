from contextlib import asynccontextmanager
from app.core.config import CONFIG
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, user, cdkey, errors, speech_to_text
from app.crud.user import init_user
from app.core.log import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_user()
    yield


app = FastAPI(
    title=CONFIG.APP.NAME,
    description=CONFIG.APP.DESCRIPTION,
    version=CONFIG.APP.VERSION,
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(cdkey.router, prefix="/api")
app.include_router(errors.router, prefix="/api")
app.include_router(speech_to_text.router, prefix="/api")
