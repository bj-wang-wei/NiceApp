from datetime import datetime, date
from typing import Union
from db.model.log import Log
from nicegui import app


async def create_log(log_text: str, level: str) -> Log:
    username = app.storage.user.get("username", "None")
    return await Log.create(log_text=log_text, level=level, username=username)


async def get_logs() -> list[Log]:
    return (
        await Log.all()
        .order_by("-created_at")
        .values("log_text", "level", "username", "created_at")
    )


async def get_logs_by_created(created: Union[datetime, date]) -> list[Log]:
    if type(created) != datetime:
        created = datetime.strptime(created, "%Y-%m-%d")
    start_date = datetime(created.year, created.month, created.day, 0, 0, 0)
    end_date = datetime(created.year, created.month, created.day, 23, 59, 59)
    return (
        await Log.filter(created_at__gte=start_date, created_at__lte=end_date)
        .order_by("-created_at")
    )


async def get_logs_between_created(
    start_date: Union[datetime, date],
    end_date: Union[datetime, date],
    page_number: int,
    page_size: int,
) -> list[Log]:
    if type(start_date) != datetime:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    if type(end_date) != datetime:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
    end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
    if page_number < 1:
        logs = (
            await Log.filter(created_at__gte=start_date, created_at__lte=end_date)
            .order_by("-created_at")
        )
    else:
        offset = (page_number - 1) * page_size
        logs = (
            await Log.filter(created_at__gte=start_date, created_at__lte=end_date)
            .offset(offset)
            .limit(page_size)
            .order_by("-created_at")
        )
    totalRows = await Log.filter(
        created_at__gte=start_date, created_at__lte=end_date
    ).count()
    return logs, totalRows


async def del_logs_by_created(created: Union[datetime, date]) -> None:
    if type(created) != datetime:
        created = datetime.strptime(created, "%Y-%m-%d")
    start_date = datetime(created.year, created.month, created.day, 0, 0, 0)
    end_date = datetime(created.year, created.month, created.day, 23, 59, 59)
    
    await Log.filter(created_at__gte=start_date, created_at__lte=end_date).delete()


async def del_logs_between_created(
    start_date: Union[datetime, date], end_date: Union[datetime, date]
) -> None:

    if type(start_date) != datetime:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    if type(end_date) != datetime:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
    end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
    
    await Log.filter(created_at__gte=start_date, created_at__lte=end_date).delete()
