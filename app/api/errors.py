from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Dict, List
from app import crud, schemas, models
from app.core import dependencies, utils
from app.schemas import ErrorCode, ErrorDetail

router = APIRouter(prefix="", tags=["errors"])


@router.get("/errors", response_model=List[ErrorDetail])
async def get_error_definitions():
    """返回所有错误定义及其信息"""
    error_definitions = [ErrorDetail.from_error_code(error) for error in ErrorCode]
    return error_definitions
