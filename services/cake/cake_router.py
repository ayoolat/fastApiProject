import json
from typing import List

import jsonpickle
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from starlette import status

from database.database import get_db
from schema import cake
from schema.response import ResponseDTO, PagedList
from services.cake.dependency import upload_cake_image, add_new_cake, get_all_cake
from services.respond import Respond

router = APIRouter(tags=['Cake'])


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=ResponseDTO[cake.Cake])
async def add_cake(request: cake.Cake, db: Session = Depends(get_db)):
    response = await add_new_cake(request, db)
    return response


@router.post("/upload", status_code=status.HTTP_200_OK, response_model=ResponseDTO[str])
async def upload_image(file: UploadFile):
    image = await upload_cake_image(file)
    return image


@router.get("/all", status_code=status.HTTP_200_OK, response_model=ResponseDTO[PagedList[cake.Cake]])
async def get_all(skip: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    cakes = await get_all_cake(db, skip, limit)
    return cakes
