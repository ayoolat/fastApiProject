from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import psycopg2
from starlette.requests import Request
from starlette.responses import Response


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail=str(e))
