from db.crud.menu import clear_menus,create_menu
from db.crud.role import clear_role, create_role
from db.crud.user import clear_users, create_user
from core.utility import get_locString

_ = get_locString()

async def init_data() -> None:
    await clear_menus()
    await create_menu(
        _("System"),
        [
            {"icon": "group", "label": _("Role"), "page_name": "role"},
            {"icon": "person", "label": _("User"), "page_name": "user"},
            {"icon": "view_list", "label": _("Log"), "page_name": "log"},
        ],
        99,
    )
    await create_menu(
        _("Dashboard"),
        [
            {"icon": "home", "label": _("Home"), "page_name": "home"},
            {"icon": "ssid_chart", "label": _("Chart"), "page_name": "chart"},
        ],
        0,
    )

    await clear_role()
    role = await create_role(
        _("System"),
        [_("Home"), _("Chart"), _("Role"), _("User"), _("Log")],
    )

    await clear_users()
    await create_user(
        username="admin",
        password="Admin.123",
        name=_("administrator"),
        mobile="",
        email="",
        is_admin=True,
        role=role,
    )
