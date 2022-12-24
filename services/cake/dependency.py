import os
import uuid

import aiofiles
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from repositories.cake import add_cake, get_one_cake, get_all_cakes
from schema import cake
from services.cake.upload import upload_to_aws


async def add_new_cake(payload: cake.Cake, db: Session):
    new_cake = await add_cake(payload, db)
    return new_cake


async def upload_cake_image(file: UploadFile):
    _, ext = os.path.splitext(file.filename)
    content = await file.read()
    if file.content_type.find("image"):
        raise HTTPException(status_code=406, detail="Only .jpeg or .png  files allowed")
    file_name = f'{uuid.uuid4().hex}{ext}'
    async with aiofiles.open(os.path.join("cakes/", file_name), mode='wb') as f:
        await f.write(content)
    s3_file = upload_to_aws(file, file_name)
    return s3_file


async def get_cake(id: int, db: Session):
    cake_object = await get_one_cake(db, id)
    return cake_object


async def get_all_cake(db: Session, skip: int, limit: int):
    cakes = await get_all_cakes(db, skip, limit)
    return cakes
