from nicegui import ui, app, events
from core.settings import TABLE_PAGE_SIZE
from db.crud.log import get_logs_between_created, del_logs_between_created
from core.log import logger
from core.utility import get_locString
import datetime

_ = get_locString()
async def show():  
    # region function

    table_data = {
        "rows": [],
        "columns": [
            {
                "name": "LOG_TEXT",
                "label": _("Log Text"),
                "field": "log_text",
                "sortable": True,
                "align": "left",
                "style": "text-wrap: wrap",
            },
            {
                "name": "LEVEL",
                "label": _("Level"),
                "field": "level",
                "sortable": True,
                "align": "left",
            },
            {
                "name": "USERNAME",
                "label": _("Operation User"),
                "field": "username",
                "sortable": True,
                "align": "left",
            },
            {
                "name": "CREATED_AT",
                "label": _("Timestamp"),
                "field": "created_at",
                "align": "left",
                "sortable": True,
            },
        ],
        "pagination": {
            "rowsPerPage": TABLE_PAGE_SIZE,
            "page": 0,
            "rowsNumber": 0,
        },
    }

    async def refresh(page_number: int = 1):
        start_date = app.storage.user.get("log_start_date", datetime.date.today())
        end_date = app.storage.user.get("log_end_date", datetime.date.today())
        if not start_date or not end_date:
            return
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        logs, total = await get_logs_between_created(
            start_date=start_date,
            end_date=end_date,
            page_number=page_number,
            page_size=TABLE_PAGE_SIZE,
        )
        for log in logs:
            log.id=str(log.id)
            log.created_at = log.created_at.strftime("%Y-%m-%d %H:%M:%S")
        table_data["rows"] = [vars(log) for log in logs]
        table_data["pagination"] = {
            "rowsPerPage": TABLE_PAGE_SIZE,
            "page": page_number,
            "rowsNumber": total,
        }
        paginated_table.refresh()

    async def clear():
        start_date = app.storage.user.get("log_start_date", datetime.date.today())
        end_date = app.storage.user.get("log_end_date", datetime.date.today())
        result = await confirm
        if result == "Yes":
            s1 = "Clear logs from"
            s2 = "to"
            logger.info(f"{s1} {start_date} {s2} {end_date} ")
            await del_logs_between_created(start_date=start_date, end_date=end_date)
            await refresh()
        confirm.close()

    async def do_pagination(e: events.GenericEventArguments):
        await refresh(e.args["pagination"]["page"])

    @ui.refreshable
    def paginated_table():
        with ui.card().classes("shadow-0 border h-[calc(100vh-150px)]"):
            with ui.table(
                columns=table_data["columns"],
                rows=table_data["rows"],
                pagination=table_data["pagination"],
            ).classes("text-body1 w-full") as table:
                with table.add_slot("top-left"):
                    with ui.input(
                        _("Start Date"),
                    ).bind_value(app.storage.user, "log_start_date") as start_date:
                        with start_date.add_slot("append"):
                            ui.icon("edit_calendar").on(
                                "click", lambda: start_menu.open()
                            ).classes("cursor-pointer")
                        with ui.menu() as start_menu:
                            ui.date().bind_value(start_date)
                    with ui.input(
                        _("End Date"),
                    ).bind_value(
                        app.storage.user, "log_end_date"
                    ).classes("ml-4") as end_date:
                        with end_date.add_slot("append"):
                            ui.icon("edit_calendar").on(
                                "click", lambda: end_menu.open()
                            ).classes("cursor-pointer")
                        with ui.menu() as end_menu:
                            ui.date().bind_value(end_date)
                    with ui.button_group().props("push glossy").classes("ml-4 mt-2"):
                        ui.button(
                            _("Clear"),
                            on_click=lambda: clear(),
                            icon="delete",
                            color="red-600",
                        ).props("push text-color=white")
                        ui.button(
                            _("Refresh"),
                            on_click=lambda: refresh(),
                            icon="refresh",
                            color="sky-600",
                        ).props("push text-color=white")
            table.on("request", do_pagination)
    # endregion
    # region ui

    ui.label(_("Log Management")).classes("text-2xl pb-4")

    with ui.dialog().props("persistent") as confirm, ui.card().classes(
        " items-center w-fit"
    ):
        ui.label(_("Prompt Message")).classes("text-h8")
        ui.separator()
        ui.label(_("Are you sure you want to clear the log ?"))
        with ui.row():
            ui.button(_("Yes"), on_click=lambda: confirm.submit("Yes")).props(
                "push glossy "
            )
            ui.button(_("No"), on_click=lambda: confirm.submit("No")).props("push glossy ")

    # endregion
    # region code

    paginated_table()
    await refresh()

    # endregion
