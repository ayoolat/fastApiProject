from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from database.models import cake
from database.models import cart
from database.models import order
from database.models import user
from database.database import engine

from firebase_admin import credentials, initialize_app

from middlewares.errorHandler import catch_exceptions_middleware
from services.auth import auth_router
from services.cake import cake_router
from cli import app as cli
from services.cart import cart_router
from services.orders import order_router

cred = credentials.Certificate("./firebase-json.json")
initialize_app(cred)

app = FastAPI()

allow_all = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_all,
    allow_credentials=True,
    allow_methods=allow_all,
    allow_headers=allow_all
)
app.middleware('http')(catch_exceptions_middleware)

cake.Base.metadata.create_all(engine)
cart.Base.metadata.create_all(engine)
order.Base.metadata.create_all(engine)
user.Base.metadata.create_all(engine)

app.include_router(auth_router.router)
app.include_router(cake_router.router)
app.include_router(cart_router.router)
app.include_router(order_router.router)

if __name__ == '__main__': cli()
