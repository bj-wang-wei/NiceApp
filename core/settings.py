from pathlib import Path

DEGUG: bool = True

APP_NAME = "Nice App"

BASE_DIR = Path(__file__).resolve().parent.parent

STORAGE_SECRET: str = "lKeItSyRaVaTrAkAtNmPsCfIpVnWyGtM"

LANGUAGE: str = "en-US"

# LANGUAGE: str = "zh-CN"

TABLE_PAGE_SIZE: int = 10

TIME_ZONE="Asia/Shanghai"

AVATAR_PATH :str ="/static/avatar/"

DEFAULT_AVATAR: str = f"{AVATAR_PATH}default_avatar.png"

LOG_NAME: str = "app.log"

PASS_SCRET: bytes = b"umphKMDOnHZDI_sIyDpBgy4t_o9qI1YxMcSr3Am5G0c="

PASS_MASK: str = "yU9@rI5&"

# sqlite
SQLITE_DATABASE_URL: str = "sqlite://base/nice.sqlite"

# postgresql
PG_DATABASE_URL: str = (
    "postgres://postgres:postgres@127.0.0.1:5432/nice_sys?schema=nice"
)
# tortoise orm config
TORTOISE_ORM = {
    "connections": {
        "default": SQLITE_DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": ["db.model", "aerich.models"],
            "default_connection": "default",
        },
    },
    "use_tz": False,
    "timezone": "Asia/Shanghai",
}
