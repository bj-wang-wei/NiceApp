from db.model.menu import Menu


async def create_menu(list_label: str, list_item: list, order: int) -> Menu:
    return await Menu.create(list_label=list_label, list_item=list_item, order=order)


async def get_menus() -> list[Menu]:
    return await Menu.all().order_by("order")


async def get_menu_by_id(id: str) -> Menu:
    return await Menu.get(id=id)

async def clear_menus():
    await Menu.all().delete()