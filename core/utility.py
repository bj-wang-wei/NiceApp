from cryptography.fernet import Fernet
from datetime import timedelta, datetime
import pytz
from core.settings import TIME_ZONE, LANGUAGE,BASE_DIR
from nicegui import app
import pandas as pd
from io import BytesIO
from captcha.image import ImageCaptcha
from PIL import Image
import random
import string
import aiofiles
import aiofiles.os
import os
import gettext
from fastapi import UploadFile
from core.log import logger


def excel2bytes(data, columns):
    df = pd.DataFrame(data, columns=columns)
    excel_bytes = BytesIO()
    df.to_excel(excel_bytes, index=False)
    excel_bytes.seek(0)
    return excel_bytes.getvalue()

def bytes2dict(data, columns,types):
    df = pd.read_excel(data, dtype=types)
    if compare_lists(columns, list(df.columns)):
        return df.to_dict("records")
    else:
        return []

def seconds_to_time(seconds):
    # 创建一个timedelta对象
    delta = timedelta(seconds=seconds)

    # 使用dt.days、dt.seconds等获取相应的值
    days, seconds = delta.days, delta.seconds
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return f"{days}天{hours}小时{minutes}分钟"
    if hours > 0:
        return f"{hours}小时{minutes}分钟"
    if minutes > 0:
        return f"{minutes}分钟"
    # if seconds > 0:
    #     return f"{seconds}秒"
    return "小于1分钟"

def encrypt(key, text):
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(text.encode()).decode()

def decrypt(key, text):
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(text.encode()).decode()

def fmt_time(date):
    return date.strftime("%Y-%m-%d %H:%M")

def set_user_timestamp():
    app.storage.user.update(
        {
            "timestamp": int(
                datetime.now(pytz.timezone(TIME_ZONE)).timestamp()
            ),
        }
    )

def date_to_timestamp(date):
    return int(datetime.strptime(date.strftime("%Y-%m-%d"), "%Y-%m-%d").timestamp() * 1000)

def timestamp_to_date(timestamp):
    return datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d")

def compare_lists(list1, list2):
    return set(list1) == set(list2)

def generate_captcha(code_length=4, width=200, height=80):
    # captcha_text = "".join(
    #     random.choices(string.ascii_uppercase + string.digits, k=code_length)
    # )
    captcha_text = "".join(
        random.choices("ABCDEFGHIJKLMNPQRSTUVWXYZ123456789", k=code_length)
    )
    image = ImageCaptcha(width=width, height=height)
    data = image.generate(captcha_text)
    pil_image = Image.open(data)
    return (captcha_text, pil_image)

def utc2Local(utc_time):
    return utc_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(TIME_ZONE))

def get_absolute_path(relatively_path):
    absolute_path = BASE_DIR
    path_list = relatively_path.split("/")
    for path in path_list:
        absolute_path = os.path.join(absolute_path, path)
    return absolute_path

async def save_upload_file(in_file: UploadFile, out_file_path: str):
    try:
        out_file_path=get_absolute_path(out_file_path)    
        if os.path.exists(os.path.dirname(out_file_path)) == False:
            await aiofiles.os.makedirs(os.path.dirname(out_file_path), exist_ok=True)
        async with aiofiles.open(out_file_path, "wb") as out_file:
            while content := in_file.read():
                await out_file.write(content)
        return True
    except Exception as e:
        logger.debug(e)
        return False

async def delete_file(filename: str):
    try:
        filename=get_absolute_path(filename)    
        if os.path.exists(filename):
            await aiofiles.os.remove(filename)
        return True
    except Exception as e:
        logger.debug(e)
        return False

def get_locString():
    lang=LANGUAGE.replace("-","_")
    translation = gettext.translation("resource", ("locale/"), languages=[lang])
    return translation.gettext
