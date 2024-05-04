from db.model.user import User
from db.model.role import Role
from core.settings import PASS_SCRET, PASS_MASK, DEFAULT_AVATAR
from core.utility import encrypt, decrypt
from tortoise.exceptions import DoesNotExist
from tortoise.query_utils import Prefetch
from core.utility import fmt_time


async def create_user(
    username: str,
    password: str,
    name: str,
    mobile: str,
    email: str,
    avatar: str = DEFAULT_AVATAR,
    is_admin: bool = False,
    role: Role = None,
) -> User:
    return await User.create(
        username=username,
        password=encrypt(PASS_SCRET, password),
        name=name,
        mobile=mobile,
        email=email,
        avatar=avatar,
        is_admin=is_admin,
        role=role,
    )


async def get_user_by_id(id: str) -> User:
    try:
        user = (
            await User.filter(id=id)
            .first()
        )

        if user:
            return user
        return None
    except DoesNotExist:
        return None


async def get_user_by_username(username: str) -> User:
    try:
        user = await User.filter(username=username).first()
        if user:
            return user
        return None
    except DoesNotExist:
        return None


async def get_user_count_by_role(role_id: str) -> User:
    try:
        user_count = await User.filter(role=role_id).count()
        return user_count
    except DoesNotExist:
        return 0


async def get_users() -> list[User]:
    try:
        users = (
            await User.all()
            # .prefetch_related(Prefetch("role", queryset=Role.all().only("id", "name")))
            .only(
                "id",
                "username",
                "name",
                "mobile",
                "email",
                "avatar",
                "is_admin",
                "role_id",
                "created_at",
                "updated_at",
            )
            .order_by("username")
        )
        if users:
            return users
        return None
    except DoesNotExist:
        return None


async def delete_user_by_id(id: str) -> User:
    return await User.filter(id=id).delete()


async def update_user(**kwargs) -> User:
    if "id" in kwargs:
        user = await User.filter(id=kwargs["id"]).first()
        if user:
            if "username" in kwargs:
                user.username = kwargs["username"]
            if "password" in kwargs and kwargs["password"] != PASS_MASK:
                user.password = encrypt(PASS_SCRET, kwargs["password"])
            if "name" in kwargs:
                user.name = kwargs["name"]
            if "mobile" in kwargs:
                user.mobile = kwargs["mobile"]
            if "email" in kwargs:
                user.email = kwargs["email"]
            if "is_admin" in kwargs:
                user.is_admin = kwargs["is_admin"]
            if "avatar" in kwargs:
                user.avatar = kwargs["avatar"]
            if "role" in kwargs:
                user.role = kwargs["role"]
            await user.save()
            return user
        else:
            return None
    else:
        return None


async def login(username: str, password: str) -> User:
    user = await get_user_by_username(username)
    if user:
        if decrypt(PASS_SCRET, user.password) == password:
            return user
    return None


async def reset_password(username: str, password: str) -> bool:
    user = await User.filter(username=username).update(
        password=encrypt(PASS_SCRET, password)
    )
    if user is None:
        return False
    return True


async def get_role_by_username(username: str) -> list:
    try:
        user = await User.get(username=username)
        if user:
            return await user.role
    except DoesNotExist:
        return None


async def clear_users():
    await User.all().delete()
