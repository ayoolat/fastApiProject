import io
import os
import uuid
from typing import List

import aiofiles
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from repositories.cake import add_cake, get_one_cake, get_all_cakes, count_all_cakes, count_cake, cake_update, \
    cake_delete
from schema import cake
from schema.response import PagedList
from services.cake.updateCake import CakeUpdate
from services.cake.upload import upload_to_aws
from services.respond import Respond


async def add_new_cake(payload: cake.Cake, db: Session):
    payload.name = capitalize_words(payload.name)
    new_cake = await add_cake(payload, db)
    respond = Respond[cake.Cake]()
    return respond.response(
        body=new_cake,
        code=201,
        message="Cake add successful"
    )


async def upload_cake_image(file: UploadFile):
    _, ext = os.path.splitext(file.filename)

    if file.content_type.find("image"):
        raise HTTPException(status_code=406, detail="Only .jpeg or .png  files allowed")
    file_name = f'{uuid.uuid4().hex}{ext}'

    contents = file.file.read()
    temp_file = io.BytesIO()
    temp_file.write(contents)
    temp_file.seek(0)

    s3_file = upload_to_aws(temp_file, f'pastries/{file_name}')
    respond = Respond[str]()
    return respond.response(
        body=f'https://cake-shop-1234.s3.eu-west-3.amazonaws.com/{s3_file}',
        code=201,
        message='Image upload successful'
    )


async def get_cake(id: int, db: Session):
    cake_object = await get_one_cake(db, id)
    respond = Respond[cake.Cake]()
    return respond.response(
        body=cake_object,
        code=200,
        message="Cake query successful"
    )


async def update_cake(payload: CakeUpdate, db: Session):
    if payload.name is not None:
        payload.name = capitalize_words(payload.name)
    cake_object = await cake_update(db, payload)
    respond = Respond[cake.Cake]()
    return respond.response(
        body=cake_object,
        code=200,
        message="Cake query successful"
    )


async def delete_cake(payload: CakeUpdate, db: Session):
    await count_cake(db, payload.id)
    cake_object = await cake_delete(db, payload.id)
    respond = Respond[bool]()
    return respond.response(
        body=True,
        code=200,
        message="Cake successfully deleted"
    )


async def get_all_cake(db: Session, skip: int, limit: int):
    cakes = await get_all_cakes(db, skip, limit)
    paged_list = PagedList(
        data=cakes,
        total_count=await count_all_cakes(db),
        page=skip
    )
    respond = Respond[PagedList[cake.Cake]]()
    return respond.response(
        body=paged_list,
        code=200,
        message="Cake query successful"
    )


def capitalize_words(string):
    words = string.split()
    capitalized_words = [word.capitalize() for word in words]
    return " ".join(capitalized_words)
