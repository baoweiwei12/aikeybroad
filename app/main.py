from contextlib import asynccontextmanager

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError
from app.core.config import CONFIG
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, user, cdkey, errors, speech, chat, api_config
from app.crud.user import init_user
from app.core.log import logging
from app.schemas.errors import ErrorCode, ErrorDetail


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

app.mount(
    "/uploaded_files", StaticFiles(directory="uploaded_files"), name="uploaded_files"
)
app.include_router(errors.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(cdkey.router, prefix="/api")
app.include_router(speech.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(api_config.router, prefix="/api")


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
