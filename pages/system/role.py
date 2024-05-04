from nicegui import ui, events
from core.settings import TABLE_PAGE_SIZE
from db.crud.role import (
    get_roles,
    delete_role_by_id,
    get_role_by_name,
    update_role,
    create_role,
)
from db.crud.user import get_user_count_by_role
from db.crud.menu import get_menus
from core.log import logger
import json
from core.utility import get_locString

_ = get_locString()


async def show():
    # region function

    columns = [
        {
            "name": "NAME",
            "label": _("Role Name"),
            "field": "name",
            "sortable": True,
            "align": "left",
            "style": "width: 150px",
        },
        {
            "name": "PERMISSIONS",
            "label": _("Permissions"),
            "field": "permissions",
            "sortable": True,
            "align": "left",
            "style": "width: 700px; text-wrap: wrap",
        },
        {
            "name": "CREATED_AT",
            "label": _("Creation Time"),
            "field": "created_at",
            "align": "left",
            "sortable": True,
            "style": "width: 100px",
        },
        {
            "name": "UPDATED_AT",
            "label": _("Update Time"),
            "field": "updated_at",
            "align": "left",
            "sortable": True,
            "style": "width: 100px",
        },
    ]

    async def row_edit(e: events.GenericEventArguments):
        current_edit_id.text = e.args["id"]
        name.value = e.args["name"]
        permissions_tree._props["ticked"] = e.args["permissions"]
        permissions_tree.update()
        name.update()
        dialog_title.text = _("Edit Role")
        data_dialog.open()

    async def row_delete(e: events.GenericEventArguments):
        s1 = _("Are you sure you want to delete the role")
        confirm_text.set_text(f"{s1} <{e.args['name']}> ?")
        result = await confirm
        if result == "Yes":
            if await check_role_not_have_user(e.args["id"]) == False:
                return
            await delete_role_by_id(e.args["id"])
            s1 = _("Delete role")
            logger.info(f"{s1} <{e.args['name']}>")
            await refresh()
        confirm.close()

    async def row_add():
        current_edit_id.text = ""
        name.value = ""
        name.update()
        permissions_tree._props["ticked"] = []
        permissions_tree.update()
        dialog_title.text = _("Add Role")
        data_dialog.open()

    async def role_delete():
        if check_table_selected() == False:
            return
        confirm_text.set_text(_("Delete the selected role ?"))
        result = await confirm
        if result == "Yes":
            for item in table.selected:
                if await check_role_not_have_user(item["id"]) == False:
                    continue
                await delete_role_by_id(item["id"])
                s1 = _("Delete role")
                logger.info(f"{s1} <{item['name']}>")
            await refresh()
        confirm.close()

    async def refresh():
        roles = await get_roles()
        for role in roles:
            permissions = []
            for permission in role.permissions:
                permissions.append(_(permission))
            role.permissions = permissions
            role.id = str(role.id)
            role.created_at = role.created_at.strftime("%Y-%m-%d %H:%M:%S")
            role.updated_at = role.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        table.rows = [vars(role) for role in roles]
        table.selected.clear()
        table.update()

    async def get_all_permissions():
        permissions = []
        menus = await get_menus()
        for menu in menus:
            children = []
            for item in menu.list_item:
                child = {
                    "id": _(item["label"]),
                }
                children.append(child)
            permission = {"id": _(menu.list_label), "children": children}
            permissions.append(permission)
        permissions_tree._props["nodes"] = permissions
        permissions_tree.update()
        return permissions

    async def role_update():
        await update_role(
            id=current_edit_id.text,
            name=name.value,
            permissions=permissions_tree._props["ticked"],
        )
        s1 = _("Update role")
        logger.info(f"{s1} <{name.value}>")
        await refresh()

    async def role_create():
        await create_role(
            name=name.value.strip(),
            permissions=permissions_tree._props["ticked"],
        )
        s1 = _("Add role")
        logger.info(f"{s1} <{name.value}>")
        await refresh()

    async def save_role():
        name.value = name.value.strip()
        if name.value == "":
            ui.notify(_("Role name not be empty !"), position="top", type="warning")
            return
        if dialog_title.text == _("Add Role"):
            role = await get_role_by_name(name.value)
            if role == None:
                await role_create()
                data_dialog.close()
            else:
                ui.notify(
                    _("The role already exists, please re-enter"),
                    position="top",
                    type="warning",
                )
        else:
            role = await get_role_by_name(name.value)
            if role != None:
                if str(role.id) != current_edit_id.text:
                    ui.notify(
                        _("The role already exists, please re-enter"),
                        position="top",
                        type="warning",
                    )
                    return
            await role_update()
            data_dialog.close()

    def check_table_selected() -> bool:
        if len(table.selected) == 0:
            ui.notify(
                _("Please select the role to delete."), position="top", type="warning"
            )
            return False
        return True

    async def check_role_not_have_user(role_id) -> bool:
        if await get_user_count_by_role(role_id=role_id) == 0:
            return True
        else:
            ui.notify(
                _("The role already has a user and cannot be deleted."),
                position="top",
                type="warning",
            )
            return False

    # endregion
    # region ui

    ui.label(_("Role Management")).classes("text-2xl pb-4")

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
        with ui.splitter().classes("pl-4 pr-4 pb-4 w-full") as splitter:
            current_edit_id = ui.label("").props("hidden")
            with splitter.before:
                with ui.row():
                    name = ui.input(
                        _("*Role Name"),
                        # validation={
                        #     "必填": lambda value: (
                        #         "Too short" if len(value) < 1 else None
                        #     )
                        # },
                    ).classes("w-11/12")
                with ui.row().classes("pb-2"):
                    ui.button(
                        _("Save"), on_click=lambda: save_role(), icon="save"
                    ).props("push glossy ")
                    ui.button(
                        _("Close"), on_click=data_dialog.close, icon="close"
                    ).props("push glossy ")
            with splitter.after:
                permissions_tree = ui.tree([], label_key="id", tick_strategy="leaf")

    with ui.card().classes("shadow-0 border h-[calc(100vh-150px)]"):
        with ui.table(
            columns=columns,
            rows=[],
            pagination=TABLE_PAGE_SIZE,
            row_key="id",
            selection="multiple",
        ).classes("w-full") as table:
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
                        on_click=lambda: role_delete(),
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
                <q-checkbox dense v-model="props.selected" style="margin-right: 30px"/>
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
                <q-checkbox dense v-model="props.selected" style="margin-right: 30px"/>
                <q-btn size="sm" color="yellow-600" round dense icon="edit"
                    @click="() => $parent.$emit('row_edit', props.row)" style="margin-right: 10px"
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
            <q-td  v-for="col in props.cols" :key="col.name" :props="props" >
                {{ col.value }}
            </q-td>
        </q-tr>
        """,
    )

    table.on("row_delete", row_delete)
    table.on("row_edit", row_edit)
    # endregion
    # region code
    await refresh()
    await get_all_permissions()
    # endregion
