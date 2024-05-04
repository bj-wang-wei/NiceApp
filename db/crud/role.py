from db.model.role import Role
from db.crud.user import get_role_by_username
from db.crud.menu import get_menus
from tortoise.exceptions import DoesNotExist
from core.utility import get_locString

_ = get_locString()


async def create_role(name: str, permissions: dict) -> Role:
    return await Role.create(name=name, permissions=permissions)


async def get_roles() -> list[Role]:
    try:
        roles = await Role.all().order_by("name")
        if roles:
            return roles
        return None      
    except DoesNotExist:
        return None


async def get_role_by_name(name: str) -> Role:
    try:
        role = await Role.filter(name=name).first()
        if role:
            return role
        return None
    except DoesNotExist:
        return None


async def get_role_by_id(id: str) -> Role:
    try:
        role = await Role.filter(id=id).first()
        if role:
            return role
        return None
    except DoesNotExist:
        return None


async def update_role(**kwargs) -> Role:
    if "id" in kwargs:
        role = await Role.filter(id=kwargs["id"]).first()
        if role:
            if "name" in kwargs:
                role.name = kwargs["name"]
            if "permissions" in kwargs:
                role.permissions = kwargs["permissions"]
            await role.save()
            return role
        else:
            return None
    else:
        return None


async def delete_role_by_id(id: str) -> Role:
    return await Role.filter(id=id).delete()

async def get_role_menus(username: str):
    menus = []
    role = await get_role_by_username(username)
    all_menus = await get_menus()
    for menu in all_menus:
        list_item = []
        for item in menu.list_item:
            if _(item["label"]) in role.permissions:
                list_item.append(item)
        if len(list_item) > 0:
            menu.list_item = list_item
            menus.append(menu)
    return menus

async def clear_role():
    await Role.all().delete()
