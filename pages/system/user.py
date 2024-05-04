from nicegui import ui, events
from core.settings import TABLE_PAGE_SIZE
from db.crud.user import (
    get_users,
    delete_user_by_id,
    update_user,
    create_user,
    get_user_by_username,
)
from db.crud.role import get_roles, get_role_by_id
from core.log import logger
from core.settings import PASS_MASK
from core.utility import get_locString

_ = get_locString()


async def show():
    # region function
    columns = [
        {
            "name": "USERNAME",
            "label": _("User Name"),
            "field": "username",
            "sortable": True,
            "align": "left",
            "style": "width: 100px",
        },
        {
            "name": "NAME",
            "label": _("Name"),
            "field": "name",
            "sortable": True,
            "align": "left",
            "style": "width: 150px",
        },
        {
            "name": "MOBILE",
            "label": _("Moblile"),
            "field": "mobile",
            "sortable": True,
            "align": "left",
        },
        {
            "name": "EMAIL",
            "label": _("E-mail"),
            "field": "email",
            "sortable": True,
            "align": "left",
            "style": "width: 150px",
        },
        {
            "name": "ROLE_NAME",
            "label": _("Role"),
            "field": "role_name",
            "sortable": True,
            "align": "left",
            "style": "width: 150px",
        },
        {
            "name": "CREATED_AT",
            "label": _("Creation Time"),
            "field": "created_at",
            "align": "left",
            "sortable": True,
        },
        {
            "name": "UPDATED_AT",
            "label": _("Update Time"),
            "field": "updated_at",
            "align": "left",
            "sortable": True,
        },
    ]

    async def row_edit(e: events.GenericEventArguments):
        current_edit_id.text = e.args["id"]
        username.value = e.args["username"]
        password.value = PASS_MASK
        name.value = e.args["name"]
        mobile.value = e.args["mobile"]
        email.value = e.args["email"]
        role_select.value = e.args["role_id"]
        is_admin.value = e.args["is_admin"]

        username.update()
        password.update()
        name.update()
        mobile.update()
        email.update()
        role_select.update()
        is_admin.update()

        dialog_title.text = _("Edit User")
        data_dialog.open()

    async def row_delete(e: events.GenericEventArguments):
        s1 = _("Are you sure you want to delete the user")
        confirm_text.set_text(f"{s1} <{e.args['username']}> ?")
        result = await confirm
        if result == "Yes":
            if e.args["is_admin"]:
                ui.notify(
                    _("The user is an administrator and cannot be deleted."),
                    position="top",
                    type="warning",
                )
                return
            await delete_user_by_id(e.args["id"])
            s1 = _("Delete user")
            logger.info(f"{s1} <{e.args['name']}>")
        await refresh()
        confirm.close()

    async def row_add():
        current_edit_id.text = ""
        username.value = ""
        password.value = ""
        name.value = ""
        mobile.value = ""
        email.value = ""
        role_select.value = ""
        is_admin.value = False

        username.update()
        password.update()
        name.update()
        mobile.update()
        email.update()
        role_select.update()
        is_admin.update()

        dialog_title.text = _("Add User")
        data_dialog.open()

    async def user_delete():
        if check_table_selected() == False:
            return
        confirm_text.set_text(_("Are you sure you want to delete the selected users ?"))
        result = await confirm
        if result == "Yes":
            for item in table.selected:
                if item["is_admin"]:
                    ui.notify(
                        _("The user is an administrator and cannot be deleted."),
                        position="top",
                        type="warning",
                    )
                    continue
                await delete_user_by_id(item["id"])
                s1 = _("Delete user")
                logger.info(f"{s1} <{item['name']}>")
            await refresh()
        confirm.close()

    async def get_role_options():
        options = {}
        roles = await get_roles()
        for role in roles:
            options[str(role.id)] = role.name
        role_select.set_options(options)
        role_select.update()

    async def refresh():
        users = await get_users()
        for user in users:
            user.id=str(user.id)
            user.created_at = user.created_at.strftime("%Y-%m-%d %H:%M:%S")
            user.updated_at = user.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            if user.role_id:
                user.role_id = str(user.role_id)
                user.role_name = role_select.options[user.role_id]
        table.rows = [vars(user) for user in users]
        table.selected.clear()
        table.update()

    async def user_update():
        await update_user(
            id=current_edit_id.text,
            username=username.value.strip(),
            name=name.value.strip(),
            password=password.value.strip(),
            mobile=mobile.value,
            email=email.value,
            is_admin=is_admin.value,
            role=await get_role_by_id(role_select.value),
        )
        s1 = _("Update user")
        logger.info(f"{s1} <{username.value.strip()}>")
        await refresh()

    async def user_create():
        await create_user(
            username=username.value.strip(),
            name=name.value.strip(),
            password=password.value.strip(),
            mobile=mobile.value,
            email=email.value,
            is_admin=is_admin.value,
            role=await get_role_by_id(role_select.value),
        )
        s1 = _("Add user")
        logger.info(f"{s1} <{name.value}>")
        await refresh()

    async def save_user():
        if (
            name.value.strip() == ""
            or username.value.strip() == ""
            or password.value.strip() == ""
            or role_select.value == None
        ):
            ui.notify(
                _("The data is incomplete, please fill it in again"),
                position="top",
                type="warning",
            )
            return
        if dialog_title.text == _("Add User"):
            user = await get_user_by_username(username.value)
            if user == None:
                await user_create()
                data_dialog.close()
            else:
                ui.notify(
                    _("The username already exists, please re-enter"),
                    position="top",
                    type="warning",
                )
        else:
            user = await get_user_by_username(username.value.strip())
            if user != None:
                if str(user.id) != current_edit_id.text.strip():
                    ui.notify(
                        _("The username already exists, please re-enter"),
                        position="top",
                        type="warning",
                    )
                    return
            await user_update()
            data_dialog.close()

    def check_table_selected() -> bool:
        if len(table.selected) == 0:
            ui.notify(
                _("Please select the user to delete."), position="top", type="warning"
            )
            return False
        return True

    # endregion
    # region ui

    ui.label(_("User Management")).classes("text-2xl pb-4")

    with ui.dialog().props("persistent") as confirm, ui.card().classes(
        " items-center w-fit"
    ):
        ui.label(_("Prompt Message")).classes("text-h8")
        ui.separator()
        confirm_text = ui.label("")
        with ui.row():
            ui.button(_("Yes"), on_click=lambda: confirm.submit("Yes")).props(
                "push glossy "
            )
            ui.button(_("No"), on_click=lambda: confirm.submit("No")).props(
                "push glossy "
            )

    with ui.dialog().props("persistent") as data_dialog, ui.card().classes(
        "p-0 w-full"
    ):
        with ui.element("div").classes(
            " bg-sky-100 dark:bg-sky-950 w-full h-12 pl-4 pt-2 m-0"
        ):
            dialog_title = ui.label("").classes(
                "font-semibold text-base text-slate-600 dark:text-slate-200 mt-1"
            )
        current_edit_id = ui.label("").classes("hidden")
        with ui.grid(columns=2).classes("pl-4 pr-4 pb-4 w-full"):
            username = ui.input(label=_("*User Name"))
            password = ui.input(
                label=_("*Password"),
                password=True,
                password_toggle_button=True,
            )
            name = ui.input(label=_("*Name"))
            mobile = ui.input(label=_("Moblile"))
            email = ui.input(label=_("E-mail"))
            role_select = ui.select(
                label=_("*Role"),
                options=[],
            )
            with ui.row():
                ui.button(_("Save"), on_click=lambda: save_user(), icon="save").props(
                    "push glossy "
                )
                ui.button(_("Close"), on_click=data_dialog.close, icon="close").props(
                    "push glossy "
                )
            is_admin = ui.switch(_("Is Administrator"))
    with ui.card().classes("shadow-0 border h-[calc(100vh-150px)]"):
        with ui.table(
            columns=columns,
            rows=[],
            pagination=TABLE_PAGE_SIZE,
            row_key="id",
            selection="multiple",
        ).classes("text-body1 w-full") as table:
            with table.add_slot("top-left"):
                with ui.button_group().props("push glossy outline"):
                    ui.button(
                        _("Add"),
                        on_click=lambda: row_add(),
                        icon="add",
                        color="emerald-600",
                    ).props("push text-color=white")
                    ui.button(
                        _("Delete"),
                        on_click=lambda: user_delete(),
                        icon="delete",
                        color="red-600",
                    ).props("push text-color=white")
                    ui.button(
                        _("Refresh"),
                        on_click=lambda: refresh(),
                        icon="refresh",
                        color="sky-600",
                    ).props("push text-color=white")

    table.add_slot(
        "header",
        r"""
        <q-tr :props="props">      
            <q-th style="text-align: left; width: 100px">
                <q-checkbox dense v-model="props.selected"  style="margin-right: 30px"/>
        """
        + _("Action")
        + r"""
            </q-th>
            <q-th auto-width  v-for="col in props.cols" :key="col.name" :props="props">
                {{ col.label }}
            </q-th>
        </q-tr>
        """,
    )
    table.add_slot(
        "body",
        r"""
        <q-tr :props="props">     
            <q-td style="text-align: left; width: 100px" >
                <q-checkbox dense v-model="props.selected"  style="margin-right: 30px"/>
                <q-btn size="sm" color="yellow-600" round dense icon="edit"
                    @click="() => $parent.$emit('row_edit', props.row)"  style="margin-right: 10px"
                >
                    <q-tooltip class="text-xs">
        """
        + _("Edit Data")
        + r"""
                    </q-tooltip>
                </q-btn>
                <q-btn size="sm" color="red-600" round dense icon="delete"
                    @click="() => $parent.$emit('row_delete', props.row)"
                >
                    <q-tooltip class="text-xs">
        """
        + _("Delete Data")
        + r"""
                    </q-tooltip>
                </q-btn>
            </q-td>
            <q-td auto-width v-for="col in props.cols" :key="col.name" :props="props" >
                {{ col.value }}
            </q-td>
        </q-tr>
        """,
    )

    table.on("row_delete", row_delete)
    table.on("row_edit", row_edit)

    # endregion
    # region code
    await get_role_options()
    await refresh()
    # endregion
