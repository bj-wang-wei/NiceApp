from datetime import datetime
import pytz
from nicegui import ui, app, Client
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
import pages.index
from pages.login import show as show_login
from core.settings import TORTOISE_ORM, STORAGE_SECRET, LANGUAGE, APP_NAME, TIME_ZONE,BASE_DIR
from tortoise import Tortoise
from typing import Optional
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
# from db.crud.init_data import init_data 

unrestricted_page_routes = {"/login"}
page_routes = [
    "/",
    "/pages/log",
    "/pages/user",
    "/pages/role",
    "/pages/chart",
]


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        now_timestamp = datetime.now(pytz.timezone(TIME_ZONE)).timestamp()
        user_timestamp = app.storage.user.get("timestamp", 0)
        if (now_timestamp - user_timestamp) > 60 * 60 :
            app.storage.user.update({"authenticated": False, "timestamp": 0})
        if not app.storage.user.get("authenticated", False):
            if (request.url.path in page_routes and request.url.path not in unrestricted_page_routes):
                # if request.url.path in page_routes:
                #     app.storage.user.update({"referrer_path": request.url.path})
                # else:
                #     app.storage.user.update({"referrer_path": "/"})
                app.storage.user.update({"referrer_path": request.url.path})
                return RedirectResponse("/login")
        return await call_next(request)


app.add_middleware(AuthMiddleware)


@ui.page("/login")
async def login():
    await show_login()

async def init_db() -> None:
    await Tortoise.init(TORTOISE_ORM)
    await Tortoise.generate_schemas()


async def close_db() -> None:
    await Tortoise.close_connections()

async def handel_startup():
    await init_db()
    # await init_data()

async def handel_shutdown():
    await close_db()

app.on_startup(handel_startup)
app.on_shutdown(handel_shutdown)

app.add_static_files("/static", "static")

# ui.run(storage_secret=STORAGE_SECRET)

ui.run(
    host="0.0.0.0",
    port=8000,
    storage_secret=STORAGE_SECRET,
    title=APP_NAME,
    language=LANGUAGE,
    favicon="favicon.ico",
    on_air=True
)
