from datetime import datetime
import pytz
from typing import Optional
from fastapi.responses import RedirectResponse
from nicegui import app, ui
from db.crud.user import login as check_login
from core.settings import TIME_ZONE, APP_NAME, DEGUG
from core.utility import generate_captcha, get_locString
from core.log import logger

_ = get_locString()


async def show() -> Optional[RedirectResponse]:
    # region function

    def refresh_captcha():
        code, image = generate_captcha()
        app.storage.user.update({"captcha_code": code})
        captcha_image.set_source(image)
        if DEGUG:
            username.value = "admin"
            password.value = "Admin.123"
            captcha_code.value = code

    async def try_login() -> None:
        code = app.storage.user.get("captcha_code")
        if code.lower() == captcha_code.value.lower():
            user = await check_login(username.value, password.value)
            if user:
                s1 = _("User")
                s2 = _("Login to the system successfully")
                logger.info(f"{s1} <{username.value}> {s2} ")
                app.storage.user.update(
                    {
                        "username": username.value,
                        "user_id": str(user.id),
                        "authenticated": True,
                        "timestamp": int(
                            datetime.now(pytz.timezone(TIME_ZONE)).timestamp()
                        ),
                    }
                )
                ui.open(
                    app.storage.user.get("referrer_path", "/")
                )  # go back to where the user wanted to go
            else:
                ui.notify(
                    _("user name or password error"), type="warning", position="top"
                )
                s1 = _("user")
                s2 = _("Failed to log in to the system")
                logger.info(f"{s1} <{username.value}> {s2} ")
        else:
            ui.notify(
                _("Verification code is wrong, please re-enter"),
                type="warning",
                position="top",
            )

    # endregion
    # region ui
    ui.query("body").classes("bg-gradient-to-t from-stone-300 to-stone-100")
    with ui.header(elevated=True).classes(
        "bg-sky-200 items-center w-full h-[50px] p-0"
    ):
        ui.image("/static/images/logo.png").classes("h-8 w-8 ml-2 ")
        ui.label(APP_NAME).classes("text-gray-600 text-xl -ml-2")

    with ui.card().classes("absolute-center rounded-lg -mt-[150px]"):
        ui.label(_("Sign In")).classes("text-gray-700  text-2xl")
        ui.separator()
        username = (
            ui.input(
                _("User Name"),
                validation={"Too short": lambda value: len(value) >= 1},
            )
            .on(
                "keydown.enter",
                lambda: ui.run_javascript(
                    f"getElement({password.id}).$refs.qRef.focus()"
                ),
            )
            .props("size=60")
            .classes("px-3")
        )
        password = (
            ui.input(_("Password"), password=True, password_toggle_button=True)
            .on(
                "keydown.enter",
                lambda: ui.run_javascript(
                    f"getElement({captcha_code.id}).$refs.qRef.focus()"
                ),
            )
            .props("size=55")
            .classes("px-3")
        )
        with ui.row():
            captcha_code = (
                ui.input(_("Captcha code"))
                .props("size=38")
                .classes("px-3")
                .on("keydown.enter", lambda: try_login())
            )
            captcha_image = ui.interactive_image().classes("w-36 h-12 -ml-5 mt-2")
        ui.button(
            _("Login"),
            on_click=lambda: try_login(),
            color="sky-200",
        ).classes(
            "w-11/12 ml-5 mt-3 "
        ).props("push text-color=gray-600")
        captcha_image.on("click", lambda: refresh_captcha())

    # endregion
    # region code

    refresh_captcha()

    if app.storage.user.get("authenticated", False):
        return RedirectResponse("/")

    return None

    # endregion
