from nicegui import ui, app, events
from router import Router
from pages.system.user import show as user
from pages.dash.home import show as home
from pages.dash.chart import show as chart
from pages.system.log import show as log
from pages.system.role import show as role
from core.settings import APP_NAME, DEFAULT_AVATAR, AVATAR_PATH

# from db.crud.menu import get_menus
from db.crud.user import login, reset_password, update_user,get_user_by_id
from db.crud.role import get_role_menus
from core.utility import save_upload_file, delete_file, set_user_timestamp,get_locString
import uuid
import os

_ = get_locString()
@ui.page("/")
@ui.page("/pages/{_:path}")
async def index():
    # region page add router

    router = Router()

    # page add router
    @router.add("/")
    async def show_home():
        await home()

    @router.add("/pages/chart")
    async def show_chart():
        await chart()

    @router.add("/pages/log")
    async def show_log():
        await log()

    @router.add("/pages/role")
    async def show_role():
        await role()

    @router.add("/pages/user")
    async def show_user():
        await user()

    # router open page
    def open(page_name):
        set_user_timestamp()
        if page_name == "home":
            router.open(show_home)
        elif page_name == "chart":
            router.open(show_chart)
        elif page_name == "log":
            router.open(show_log)
        elif page_name == "role":
            router.open(show_role)
        elif page_name == "user":
            router.open(show_user)

    # endregion
    # region function

    dark = ui.dark_mode()

    menus: list = await get_role_menus(app.storage.user.get("username", ""))

    def enable_dark_mode(isDarkMode: bool):
        if isDarkMode:
            dark.enable()
            app.storage.user.update({"darkMode": True})
            light_button.visible = True
            dark_button.visible = False
        else:
            dark.disable()
            app.storage.user.update({"darkMode": False})
            light_button.visible = False
            dark_button.visible = True

    async def change_password():
        if (
            password_old.value == ""
            or password_new.value == ""
            or password_confirm.value == ""
        ):
            ui.notify(
                _("Please fill in the information completely"),
                type="warning",
                position="top",
            )
        elif password_new.value != password_confirm.value:
            ui.notify(
                _("The two password inputs are inconsistent"),
                type="warning",
                position="top",
            )
        else:
            username = app.storage.user.get("username", "")
            if await login(username, password_old.value):
                if reset_password(username, password_new.value):
                    change_password_dialog.close()
                    ui.notify(
                        _("password has been updated"), type="positive", position="top"
                    )
                else:
                    ui.notify(
                        _("Failed to change password, please try again"),
                        type="warning",
                        position="top",
                    )
            else:
                ui.notify(
                    _("The old password is wrong, please try again"),
                    type="warning",
                    position="top",
                )

    def logout():
        app.storage.user.update({"authenticated": False})
        ui.navigate.to("/login")

    async def get_current_user():
        user_id = app.storage.user.get("user_id", "")
        user = await get_user_by_id(user_id)
        name.value = user.name
        name.update()
        email.value = user.email
        email.update()
        mobile.value = user.mobile
        mobile.update()
        avatar.set_source(user.avatar)
        avatar.force_reload()
        user_avatar.set_source(user.avatar)
        user_avatar.force_reload()

    async def upload_avatar(e: events.UploadEventArguments):
        username = app.storage.user.get("username", "")
        random_uuid = uuid.uuid4()
        _, extension = os.path.splitext(e.name)
        file_name = f"{AVATAR_PATH}{username}-{random_uuid}{extension}"
        if await save_upload_file(e.content, file_name):
            avatar.set_source(file_name)
            avatar.force_reload()
            avatar_upload_dialog.close()
        else:
            ui.notify(
                _("Avatar upload failed, please try again"), type="warning", position="top"
            )

    async def user_info_save():
        user_id = app.storage.user.get("user_id", "")
        if await update_user(
            id=user_id,
            name=name.value,
            mobile=mobile.value,
            email=email.value,
            avatar=avatar.source,
        ):
            if user_avatar.source != avatar.source:
                if user_avatar.source != DEFAULT_AVATAR:
                    await delete_file(user_avatar.source)
                user_avatar.set_source(avatar.source)
                user_avatar.force_reload()

            ui.notify(
                _("User information modified successfully"),
                type="positive",
                position="top",
            )
            user_info_dialog.close()
            await get_current_user()
        else:
            ui.notify(
                _("Modification of user information failed, please try again"),
                type="warning",
                position="top",
            )

    async def user_info_cancel():
        if user_avatar.source != avatar.source:
            await delete_file(avatar.source)
            avatar.set_source(user_avatar.source)
            avatar.force_reload()
        user_info_dialog.close()

    # endregion code
    # region ui

    with ui.dialog() as avatar_upload_dialog, ui.card():
        ui.upload(
            label=_("Upload Avatar"),
            on_upload=lambda e: upload_avatar(e),
            max_file_size=2_000_000,
        ).props("accept='.png,.jpg,.jpeg'")

    with ui.dialog().props("persistent") as user_info_dialog, ui.card().classes("p-0"):
        with ui.element("div").classes(
            " bg-sky-100 dark:bg-sky-950 w-full h-12 pl-4 pt-2 m-0"
        ):
            ui.label(_("Personal Information")).classes(
                "font-semibold text-base text-slate-600 dark:text-slate-200 mt-1"
            )
        with ui.grid(columns=3).classes("pl-4 pr-4 pb-4 pt-0"):
            with ui.column().classes("row-span-3 items-center"):
                avatar = ui.image("").classes("w-26 h-26 mt-5")
                ui.button(_("Change Avatar"), on_click=avatar_upload_dialog.open).props(
                    "outline rounded"
                )
            name = (
                ui.input(
                    label=_("*Name"),
                )
                .props("size=35")
                .classes("col-span-2 h-8")
            )

            mobile = (
                ui.input(label=_("Moblile"))
                .props("size=35")
                .classes("col-span-2 h-8")
            )

            email = ui.input(label=_("E-mail")).props("size=35").classes("col-span-2 h-8")

            with ui.row().classes("col-span-3 pt-4"):
                ui.button(_("Save"), on_click=lambda: user_info_save()).props(
                    "push glossy"
                )
                ui.button(_("Close"), on_click=lambda: user_info_cancel()).props(
                    "push glossy "
                )

    with ui.dialog().props("persistent") as change_password_dialog, ui.card().classes(
        "p-0"
    ):
        with ui.element("div").classes(
            " bg-sky-100 dark:bg-sky-950 w-full h-12 pl-4 pt-2 m-0"
        ):
            ui.label(_("Change Password")).classes(
                "font-semibold text-base text-slate-600 dark:text-slate-200 mt-1"
            )
        with ui.element("div").classes("pl-4 pb-4 pr-4"):
            with ui.row():
                password_old = ui.input(
                    _("old password"), password=True, password_toggle_button=True
                ).props("size=55")
            with ui.row():
                password_new = ui.input(
                    _("new password"), password=True, password_toggle_button=True
                ).props("size=55")
            with ui.row():
                password_confirm = ui.input(
                    _("confirm password"), password=True, password_toggle_button=True
                ).props("size=55")
            with ui.row().classes("mt-4"):
                ui.button(_("Save"), on_click=lambda: change_password()).props(
                    "push glossy"
                )
                ui.button(_("Close"), on_click=change_password_dialog.close).props(
                    "push glossy "
                )

    # add header
    with ui.header(elevated=True).classes(
        "bg-sky-200 dark:bg-sky-950 items-center justify-between w-full h-[50px] p-0"
    ):
        with ui.row():
            with ui.button(on_click=lambda: left_drawer.toggle()).props(
                "flat dense round"
            ).classes("ml-3"):
                ui.icon("menu").classes("text-gray-700 dark:text-gray-200")
                ui.tooltip(_("Toggle sidebar")).classes("text-xs")
            ui.label(APP_NAME).classes("text-gray-700 dark:text-gray-200 text-xl pt-1")
        with ui.row():
            with ui.button(
                icon="light_mode", on_click=lambda: enable_dark_mode(False)
            ).props("flat dense round ").classes("text-grey-2 mr-0") as light_button:
                ui.tooltip(_("Switch to light mode")).classes("text-xs")
            with ui.button(
                icon="dark_mode", on_click=lambda: enable_dark_mode(True)
            ).props("flat dense round ").classes("text-grey-8 mr-0") as dark_button:
                ui.tooltip(_("Switch to dark mode")).classes("text-xs")
            with ui.avatar(
                # "img:/static/images/avatar.png",
                size="md",
                color="transparent",
            ).classes("mr-3 -ml-5"):
                user_avatar = ui.image("/static/avatar/default_avatar.png").classes(
                    "w-6 h-6"
                )
                ui.tooltip(_("Menu")).classes("text-xs")
                with ui.menu() as menu:
                    with ui.menu_item(on_click=user_info_dialog.open):
                        ui.icon("person", size="sm").classes("pt-0.5")
                        ui.label(_("Personal Information")).classes("pl-2 pt-1")
                    with ui.menu_item(on_click=change_password_dialog.open):
                        ui.icon("key", size="sm").classes("pt-0.5")
                        ui.label(_("Change Password")).classes("pl-2 pt-1")
                    ui.separator()
                    with ui.menu_item(on_click=lambda: logout()):
                        ui.icon("logout", size="sm").classes("pt-0.5")
                        ui.label(_("Logout")).classes("pl-2 pt-1")

    # add left drawer
    with ui.left_drawer(bottom_corner=True, bordered=True).classes("p-0 ").props(
        "width=260"
    ) as left_drawer:
        with ui.scroll_area().classes("fit"):
            for menu in menus:
                with ui.list().classes("w-full mt-0"):
                    ui.item_label(_(menu.list_label)).props("header").classes(
                        "text-bold text-xl"
                    )
                    for item in menu.list_item:
                        with ui.item(
                            on_click=lambda item=item: open(item["page_name"]),
                        ):
                            with ui.item_section().props("avatar"):
                                ui.icon(item["icon"])
                            with ui.item_section():
                                ui.item_label(_(item["label"]))
                ui.separator().classes("w-full")

    # this places the content which should be displayed
    router.frame().classes("w-full p-2 ")
    # endregion ui
    # region code
    if app.storage.user.get("darkMode", False) == False:
        enable_dark_mode(False)
    else:
        enable_dark_mode(True)

    await get_current_user()
    # endregion
