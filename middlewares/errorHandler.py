from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import psycopg2
from starlette.requests import Request
from starlette.responses import Response


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except HTTPException as e:
        return e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
